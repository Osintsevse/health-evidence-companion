"""Offline raw genotype intake into a NEW private SQLite staging directory.

No annotations, diagnoses, network, ledger writes, or sequence expansion.
Only declared CSV/TSV schemas and standard single-sample textual VCF are supported.
"""
import argparse
import csv
from contextlib import closing
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sqlite3
import tempfile
import zipfile

MAX_BYTES = 100 * 1024 * 1024
PUBLIC_ROOT = Path(__file__).resolve().parents[3]
TEXT_SUFFIXES = {'.txt', '.tsv', '.csv', '.vcf'}


def load_source(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('Source exceeds 100 MiB limit')
    with path.open('rb') as stream:
        original = stream.read(MAX_BYTES + 1)
    if len(original) > MAX_BYTES:
        raise ValueError('Source exceeds 100 MiB limit')
    member = None
    payload = original
    if zipfile.is_zipfile(io.BytesIO(original)):
        with zipfile.ZipFile(io.BytesIO(original)) as archive:
            entries = archive.infolist()
            if len(entries) != 1:
                raise ValueError('ZIP must contain exactly one supported text file')
            entry = entries[0]
            name = entry.filename.replace('\\', '/')
            parts = PurePosixPath(name)
            mode = entry.external_attr >> 16
            if (entry.is_dir() or parts.is_absolute() or '..' in parts.parts
                    or ':' in name or (mode & 0o170000) == 0o120000
                    or Path(name).suffix.lower() not in TEXT_SUFFIXES
                    or entry.flag_bits & 1):
                raise ValueError('Unsafe or unsupported ZIP member')
            if entry.file_size > MAX_BYTES or entry.file_size / max(entry.compress_size, 1) > 100:
                raise ValueError('ZIP size or compression ratio exceeds limits')
            with archive.open(entry) as stream:
                payload = stream.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                raise ValueError('Expanded source exceeds limit')
            member = entry.filename
    elif path.suffix.lower() not in TEXT_SUFFIXES:
        raise ValueError('Unsupported source extension')
    text = payload.decode('utf-8-sig', errors='strict')
    if '\x00' in text:
        raise ValueError('Binary source is not supported')
    return original, payload, text, member


def header_key(value):
    return re.sub(r'[^a-z0-9]', '', value.lower())


def parse(text):
    comments, records, schema, names = [], [], None, None
    for number, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        if raw.startswith('##') or (raw.startswith('#') and not raw.startswith('#CHROM\t')):
            comments.append(raw)
            continue
        if schema is None:
            if raw.startswith('#CHROM\t'):
                names = raw.split('\t')
                if (names[:8] != ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO']
                        or len(names) != 10 or names[8] != 'FORMAT'
                        or not any(c.startswith('##fileformat=VCFv4.') for c in comments)):
                    raise ValueError('Expected standard single-sample VCF with FORMAT')
                schema = 'vcf_single_sample'
            else:
                delimiter = ',' if ',' in raw else '\t'
                names = next(csv.reader([raw], delimiter=delimiter))
                keys = [header_key(n) for n in names]
                if delimiter == ',' and keys == ['rsid', 'chromosome', 'position', 'result']:
                    schema = 'declared_four_column_csv'
                elif delimiter == '\t' and keys == ['rsid', 'chromosome', 'position', 'allele1', 'allele2']:
                    schema = 'declared_five_column_tsv'
                else:
                    raise ValueError('Unsupported declared header; no vendor schema guessing')
            continue
        fields = raw.split('\t') if schema != 'declared_four_column_csv' else next(csv.reader([raw]))
        flags, alleles = [], None
        row = {'line': number, 'raw_row': raw, 'fields': fields, 'flags': flags}
        if len(fields) != len(names):
            flags.append('invalid_column_count')
        else:
            if schema == 'vcf_single_sample':
                chrom, position, rsid, ref, alt = fields[:5]
                row.update(ref_raw=ref, alt_raw=alt, quality_raw=fields[5], filter_raw=fields[6],
                           info_raw=fields[7], format_raw=fields[8], sample_name_raw=names[9])
                if fields[6] == '.':
                    flags.append('filters_not_applied')
                if fields[6] not in {'PASS', '.'}:
                    flags.append('filtered_vcf_call')
                if fields[5] == '.':
                    flags.append('quality_unavailable')
                formats, values = fields[8].split(':'), fields[9].split(':')
                if len(formats) != len(values):
                    flags.append('invalid_sample_field_count')
                if len(formats) != len(set(formats)):
                    flags.append('invalid_format')
                gt = values[formats.index('GT')] if 'GT' in formats and formats.index('GT') < len(values) else None
                row['genotype_raw'] = gt
                if gt is None:
                    flags.append('missing_gt')
                else:
                    tokens = re.split(r'[/|]', gt)
                    candidates = [ref] + ([] if alt == '.' else alt.split(','))
                    alleles = []
                    for token in tokens:
                        if token == '.':
                            alleles.append(None)
                            flags.append('no_call')
                        elif token.isdigit() and int(token) < len(candidates):
                            alleles.append(candidates[int(token)])
                        else:
                            flags.append('invalid_gt')
                            alleles.append(None)
                    row['phased'] = '|' in gt
            else:
                rsid, chrom, position = fields[:3]
                gt = fields[3] if len(fields) == 4 else None
                row['genotype_raw'] = gt
                alleles = fields[3:5] if len(fields) == 5 else None
                if gt is not None:
                    if re.fullmatch(r'[ACGTID-]{2}', gt.upper()):
                        alleles = list(gt)
                    elif gt in {'', '--', '00', 'NN', '.', './.'}:
                        flags.append('no_call')
                    else:
                        flags.append('unresolved_genotype')
            row.update(rsid_raw=rsid, chromosome_raw=chrom, position_raw=position)
            if not position.isdigit() or int(position) < 1:
                flags.append('invalid_position')
            if alleles is not None:
                if schema != 'vcf_single_sample' and any(
                        a is not None and a.upper() not in {'A', 'C', 'G', 'T', 'I', 'D', '', '-', '0', 'N', '.'}
                        for a in alleles):
                    flags.append('unsupported_allele_token')
                if any(a is None or a.upper() in {'', '-', '0', 'N', '.'} for a in alleles):
                    flags.append('no_call')
                if any(a and (a.upper() in {'I', 'D'} or a.startswith('<') or '[' in a or ']' in a or a == '*') for a in alleles):
                    flags.append('symbolic_allele_unexpanded')
            row['alleles'] = alleles
        row['flags'] = sorted(set(flags))
        records.append(row)
    if schema is None:
        raise ValueError('Missing supported header')
    # Preserve all rows and mark BOTH sides of a disagreement at a locus.
    seen = {}
    for row in records:
        if 'chromosome_raw' not in row:
            continue
        key = row['chromosome_raw'], row['position_raw']
        signature = (row.get('genotype_raw'), row.get('ref_raw'), row.get('alt_raw'), tuple(row.get('alleles') or []))
        group = seen.setdefault(key, [])
        if len(group) >= 1000:
            raise ValueError('More than 1000 observations at one locus; review required')
        group.append((row, signature))
    for group in seen.values():
        if len(group) > 1:
            flag = ('conflicting_duplicate_locus' if len({sig for _, sig in group}) > 1
                    else 'duplicate_locus')
            for row, _ in group:
                row['flags'] = sorted(set(row['flags'] + [flag]))
    assembly = [c for c in comments if re.search(r'assembly|reference|build', c, re.I)]
    strand = [c for c in comments if re.search(r'strand|forward|reverse', c, re.I)]
    return records, {'format': schema, 'comments_raw': comments, 'assembly_raw': assembly,
                     'strand_raw': strand, 'assembly': 'unknown', 'strand': 'unknown',
                     'row_count': len(records), 'unresolved_rows': sum(bool(r['flags']) for r in records)}


def stage(source, output):
    output = Path(output).resolve()
    if output == PUBLIC_ROOT or PUBLIC_ROOT in output.parents:
        raise ValueError('Staging output must be outside the public repository')
    if output.exists():
        raise FileExistsError('Output already exists; overwrites are forbidden')
    original, payload, text, member = load_source(source)
    rows, metadata = parse(text)
    metadata.update(source_sha256=hashlib.sha256(original).hexdigest(),
                    payload_sha256=hashlib.sha256(payload).hexdigest(), zip_member_raw=member,
                    source_name_raw=Path(source).name, source_bytes=len(original),
                    purpose='private_staging_only_no_clinical_interpretation')
    # Temp directory shares the destination filesystem; publish only a complete transaction.
    temporary = Path(tempfile.mkdtemp(prefix='.genetic-staging-', dir=output.parent))
    try:
        with closing(sqlite3.connect(temporary / 'staging.sqlite')) as db:
            db.execute('CREATE TABLE metadata (key TEXT PRIMARY KEY, value_json TEXT NOT NULL)')
            db.execute('CREATE TABLE observations (source_line INTEGER PRIMARY KEY, row_json TEXT NOT NULL)')
            db.executemany('INSERT INTO metadata VALUES (?, ?)', [(k, json.dumps(v)) for k, v in metadata.items()])
            db.executemany('INSERT INTO observations VALUES (?, ?)', [(r['line'], json.dumps(r)) for r in rows])
            db.commit()
        (temporary / 'source.original').write_bytes(original)
        (temporary / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
        if output.exists():
            raise FileExistsError('Output appeared during staging')
        os.rename(temporary, output)
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)
    return metadata


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path, help='New private staging directory outside public repo')
    args = parser.parse_args()
    stage(args.source, args.output)
