"""Local-only, exact forward SNP annotation of staged DTC array calls.

Download is a separate public-only operation. Annotation never uses a network.
This is a candidate cross-reference, not a diagnosis or clinical variant call.
"""
import argparse
import datetime
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import urllib.parse
import urllib.request

VERSION = '1.2'
BASE = 'https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh37/'
PUBLIC_ROOT = (next((p for p in Path(__file__).resolve().parents
                     if (p/'plugin.json').is_file() and (p/'skills').is_dir()), None)
               or next((p for p in Path(__file__).resolve().parents
                        if (p/'SKILL.md').is_file() and (p/'scripts').is_dir()), None))


def external_output(path):
    resolved = Path(path).resolve()
    if PUBLIC_ROOT and (resolved == PUBLIC_ROOT or PUBLIC_ROOT in resolved.parents):
        raise ValueError('Reference caches and private outputs must be outside the public repository')
    return resolved


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def download(url, output):
    """Fetch one dated public snapshot and its official MD5, never input genotypes."""
    if not re.fullmatch(re.escape(BASE) + r'clinvar_[0-9]{8}\.vcf\.gz', url):
        raise ValueError('Only dated HTTPS NCBI ClinVar GRCh37 snapshots are allowed')
    output = external_output(output)
    if output.exists() or Path(str(output) + '.manifest.json').exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    class StrictRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            if newurl != req.full_url:
                raise ValueError('Public download redirects are refused')
            return super().redirect_request(req, fp, code, msg, headers, newurl)
    opener = urllib.request.build_opener(StrictRedirect())
    with opener.open(url + '.md5', timeout=120) as response:
        checksum_data = response.read(16385)
        if len(checksum_data) > 16384:
            raise ValueError('Oversized checksum sidecar')
        checksum_text = checksum_data.decode('ascii')
    filename = url.rsplit('/', 1)[1]
    checksums = []
    for line in checksum_text.splitlines():
        m = re.fullmatch(r'([a-fA-F0-9]{32})\s+\*?(\S+)', line.strip())
        if m and m.group(2).rsplit('/', 1)[-1] == filename:
            checksums.append(m.group(1).lower())
    if len(checksums) != 1:
        raise ValueError('Official MD5 must name exactly the requested snapshot')
    temporary = Path(str(output) + '.part')
    owns_temporary = False
    try:
        with temporary.open('xb') as stream:
            owns_temporary = True
            with opener.open(url, timeout=120) as response:
                byte_count = 0
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    byte_count += len(chunk)
                    if byte_count > 1024 * 1024 * 1024:
                        raise ValueError('Public snapshot exceeds 1 GiB download limit')
                    stream.write(chunk)
        if digest(temporary, 'md5') != checksums[0]:
            raise ValueError('Official MD5 mismatch')
        sha256 = digest(temporary)
        if os.name == 'nt':
            temporary.rename(output)
        else:
            os.link(temporary, output)
            temporary.unlink()
        manifest = {'schema': 'clinvar-public-download-v1', 'url': url,
                    'downloaded_utc': now(), 'official_md5': checksums[0],
                    'sha256': sha256, 'bytes': output.stat().st_size,
                    'assembly': 'GRCh37', 'md5_role': 'transport-integrity; not authenticity signature'}
        write_json(str(output) + '.manifest.json', manifest)
        return manifest
    finally:
        if owns_temporary and temporary.exists():
            temporary.unlink()


def chromosome(value):
    value = str(value).removeprefix('chr').upper()
    return {'23': 'X', '24': 'Y', 'M': 'MT'}.get(value, value)


def parse_info(raw):
    result = {}
    for part in raw.split(';'):
        key, separator, value = part.partition('=')
        if key in result:
            raise ValueError('Repeated VCF INFO key')
        result[key] = value if separator else True
    return result


def build_index(vcf, output):
    """Stream gzip VCF; preserve every biallelic forward SNP record separately."""
    output = external_output(output)
    if output.exists():
        raise FileExistsError(output)
    source = {'sha256': digest(vcf), 'assembly': 'GRCh37', 'indexed_utc': now(),
              'tool_version': VERSION, 'policy': 'biallelic ACGT SNPs only; no complement/liftover'}
    sidecar = Path(str(vcf) + '.manifest.json')
    if sidecar.exists():
        public = json.loads(sidecar.read_text(encoding='utf-8'))
        if public.get('sha256') != source['sha256'] or public.get('assembly') != 'GRCh37':
            raise ValueError('Download manifest mismatch')
        source['download'] = public
    db = sqlite3.connect(output)
    try:
        db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
        db.execute('CREATE TABLE variants(chrom TEXT,pos INTEGER,ref TEXT,alt TEXT,variation_id TEXT,source_line INTEGER,info_json TEXT,raw_vcf TEXT)')
        headers = []
        batch = []
        counts = {'records': 0, 'indexed_snps': 0, 'excluded_non_biallelic_snp': 0}
        with gzip.open(vcf, 'rt', encoding='utf-8') as stream:
            for line_number, line in enumerate(stream, 1):
                if line.startswith('#'):
                    headers.append(line.rstrip())
                    continue
                fields = line.rstrip('\r\n').split('\t')
                if len(fields) < 8:
                    raise ValueError('Malformed VCF record at line %d' % line_number)
                counts['records'] += 1
                chrom, pos, identifier, ref, alt = fields[:5]
                if ref not in 'ACGT' or alt not in 'ACGT' or len(ref) != 1 or len(alt) != 1 or ref == alt:
                    counts['excluded_non_biallelic_snp'] += 1
                    continue
                info = parse_info(fields[7])
                info['_VCF_FILTER'] = fields[6]
                batch.append((chromosome(chrom), int(pos), ref, alt, identifier, line_number, json.dumps(info), line.rstrip()))
                counts['indexed_snps'] += 1
                if len(batch) >= 5000:
                    db.executemany('INSERT INTO variants VALUES(?,?,?,?,?,?,?,?)', batch)
                    batch.clear()
        reference = '\n'.join(h for h in headers if h.startswith('##reference=') or h.startswith('##contig='))
        if 'GRCh37' not in reference or 'GRCh38' in reference:
            raise ValueError('VCF header must explicitly identify GRCh37 only')
        db.executemany('INSERT INTO variants VALUES(?,?,?,?,?,?,?,?)', batch)
        db.execute('CREATE INDEX coordinates ON variants(chrom,pos)')
        source.update(counts=counts, vcf_headers=headers)
        db.execute('INSERT INTO metadata VALUES(?,?)', ('manifest', json.dumps(source)))
        db.commit()
        return source
    except BaseException:
        db.close()
        output.unlink(missing_ok=True)
        raise
    finally:
        db.close()


def candidate_flags(info, row_flags):
    flags = list(row_flags)
    classification = str(info.get('CLNSIG', ''))
    review = str(info.get('CLNREVSTAT', ''))
    if ('conflict' in classification.lower() or
            ('conflict' in review.lower() and 'no_conflicts' not in review.lower())
            or info.get('CLNSIGCONF')):
        flags.append('conflicting_classifications')
    if info.get('CLNVI'):
        pass  # Identifier cross-references are not quality flags.
    if info.get('_VCF_FILTER') not in (None, '.', 'PASS'):
        flags.append('vcf_filter_not_pass')
    if not classification:
        flags.append('no_germline_classification')
    if review not in ('practice_guideline', 'reviewed_by_expert_panel',
                      'criteria_provided,_multiple_submitters,_no_conflicts'):
        flags.append('review_below_multiple_submitters_no_conflicts')
    if info.get('CLNSIGINCL') or 'individual_variant' in review:
        flags.append('included_haplotype_or_genotype_assertion')
    return sorted(set(flags))


def build_flags(row, info, source_line, ref, alt):
    """Shared candidate policy for fresh annotation and local policy rechecks."""
    flags = candidate_flags(info, row.get('flags') or [])
    alleles = row.get('alleles') or []
    if row.get('line',source_line) != source_line:
        flags.append('staging_source_line_inconsistent')
    if any(base not in (ref,alt) for base in alleles):
        flags.append('genotype_contains_allele_outside_record')
    if not alleles or alt not in alleles:
        flags.append('alternate_not_present_in_stored_observation')
    if len(alleles) not in (1,2):
        flags.append('unsupported_allele_token_count')
    identifier = re.fullmatch(r'rs([0-9]+)',str(row.get('rsid_raw','')))
    public_rs = info.get('RS')
    if identifier and public_rs is not None:
        aliases = set(re.split(r'[,|]',str(public_rs)))
        if identifier.group(1) not in aliases:
            flags.append('marker_identifier_disagrees_with_reference')
    return sorted(set(flags))


def priority_for_review(info, flags):
    return not flags and str(info.get('CLNSIG','')) in (
        'Pathogenic','Likely_pathogenic','Pathogenic/Likely_pathogenic')


def token_metadata(match, alleles):
    """Raw genotype token counts never establish biological copy number/ploidy."""
    match['alternate_token_count'] = alleles.count(match['alternate'])
    match['alternate_copies_is_legacy_token_count'] = True
    match['copy_number_not_established'] = True
    return match


def annotate(staging, index, output, assembly, strand):
    if assembly != 'GRCh37' or strand != 'forward':
        raise ValueError('Require operator-confirmed GRCh37 and forward strand; no inference')
    output = external_output(output)
    if output.exists() or Path(str(output)+'.manifest.json').exists():
        raise FileExistsError(output)
    staged = sqlite3.connect(Path(staging).resolve().as_uri() + '?mode=ro', uri=True)
    ref = sqlite3.connect(Path(index).resolve().as_uri() + '?mode=ro', uri=True)
    out = sqlite3.connect(output)
    counts = {'rows': 0, 'candidate_records': 0, 'priority_candidates': 0,
              'excluded_unusable_calls': 0, 'no_alt_candidate_rows': 0,
              'identifier_disagreement_candidates': 0}
    try:
        metadata = {k: json.loads(v) for k, v in staged.execute('SELECT key,value_json FROM metadata')}
        reference_manifest = json.loads(ref.execute("SELECT value_json FROM metadata WHERE key='manifest'").fetchone()[0])
        if reference_manifest.get('assembly') != assembly:
            raise ValueError('Reference assembly mismatch')
        # Explicit incompatible staging metadata cannot be overridden by CLI declarations.
        declared = str(metadata.get('assembly', 'unknown')).lower()
        if declared not in ('unknown', 'grch37', 'build37', 'hg19', 'none'):
            raise ValueError('Staging assembly incompatible or unresolved')
        declared_strand = str(metadata.get('strand', 'unknown')).lower()
        if declared_strand not in ('unknown', 'forward', 'plus', 'none'):
            raise ValueError('Staging strand incompatible or unresolved')
        raw_declarations = json.dumps({k:v for k,v in metadata.items() if k in
            ('assembly_raw','strand_raw','comments','comments_raw','headers','header_comments')}).lower()
        if re.search(r'grch[ _-]?(?:36|38)|build[ _-]?(?:36|38)|hg(?:18|38)',raw_declarations):
            raise ValueError('Raw staging declarations contradict GRCh37')
        if re.search(r'\b(reverse|minus)\b',raw_declarations):
            raise ValueError('Raw staging declarations contradict forward strand')
        out.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
        out.execute('CREATE TABLE candidates(id INTEGER PRIMARY KEY,source_line INTEGER,row_json TEXT NOT NULL)')
        for source_line, raw in staged.execute('SELECT source_line,row_json FROM observations ORDER BY source_line'):
            row = json.loads(raw)
            counts['rows'] += 1
            alleles = row.get('alleles') or []
            if not alleles or any(a not in ('A','C','G','T') for a in alleles):
                counts['excluded_unusable_calls'] += 1
                continue
            try:
                pos = int(row['position_raw'])
            except (ValueError, TypeError, KeyError):
                counts['excluded_unusable_calls'] += 1
                continue
            chrom = chromosome(row.get('chromosome_raw', ''))
            matched = False
            for r, a, identifier, vcf_line, info_raw, raw_vcf in ref.execute('SELECT ref,alt,variation_id,source_line,info_json,raw_vcf FROM variants WHERE chrom=? AND pos=?', (chrom,pos)):
                if a not in alleles:
                    continue
                matched = True
                info = json.loads(info_raw)
                flags = build_flags(row,info,source_line,r,a)
                sig = str(info.get('CLNSIG', ''))
                priority = priority_for_review(info,flags)
                record = {'source_line': source_line, 'observation': row,
                          'match': {'assembly': assembly, 'strand': strand, 'chromosome': chrom, 'position': pos,
                                    'reference': r, 'alternate': a, 'alternate_copies': alleles.count(a),
                                    'all_genotype_alleles_compatible': all(base in (r,a) for base in alleles)},
                          'clinvar': {'variation_id': identifier, 'classification': sig,
                                      'review_status': info.get('CLNREVSTAT'), 'info': info,
                                      'source_vcf_line': vcf_line, 'raw_vcf': raw_vcf},
                          'flags': sorted(set(flags)), 'priority_for_manual_review': priority,
                          'interpretation': 'Unconfirmed array candidate; no diagnosis; laboratory confirmation required before clinical use'}
                token_metadata(record['match'],alleles)
                out.execute('INSERT INTO candidates(source_line,row_json) VALUES(?,?)', (source_line,json.dumps(record,ensure_ascii=False)))
                counts['candidate_records'] += 1
                counts['priority_candidates'] += int(priority)
                counts['identifier_disagreement_candidates'] += int('marker_identifier_disagrees_with_reference' in flags)
            if not matched:
                counts['no_alt_candidate_rows'] += 1
        manifest = {'schema': 'dtc-clinvar-candidates-v1', 'created_utc': now(), 'tool_version': VERSION,
                    'operator_declarations': {'assembly': assembly, 'strand': strand},
                    'chromosome_normalization': 'chr prefix; 23=X,24=Y,M=MT; 25/26 not interpreted',
                    'staging_sha256': digest(staging), 'staging_metadata': metadata,
                    'reference_manifest': reference_manifest, 'counts': counts,
                    'limitations': ['DTC array calls are not whole genome sequencing or clinical confirmation',
                                    'No complement, liftover, imputation, phasing, indel or structural matching',
                                    'ALT absence and missing ClinVar matches do not exclude disease',
                                    'Review status is distinct from classification; no phenotype or inheritance assessment',
                                    'Discordant rs identifiers require review; merged or unknown aliases are not resolved',
                                    'Allele token counts do not establish copy number or biological ploidy']}
        out.execute('INSERT INTO metadata VALUES(?,?)', ('manifest',json.dumps(manifest,ensure_ascii=False)))
        out.commit()
        write_json(str(output)+'.manifest.json',manifest)
        return manifest
    except BaseException:
        out.close()
        output.unlink(missing_ok=True)
        raise
    finally:
        staged.close()
        ref.close()
        out.close()


def recheck_candidates(source, output):
    """Reapply current candidate policy locally without rejoining array or ClinVar."""
    source = Path(source)
    output = external_output(output)
    sidecar = Path(str(output)+'.manifest.json')
    if output.exists() or sidecar.exists():
        raise FileExistsError(output)
    source_hash = digest(source)
    original = sqlite3.connect(source.resolve().as_uri()+'?mode=ro',uri=True)
    revised = sqlite3.connect(output)
    try:
        prior_manifest = json.loads(original.execute("SELECT value_json FROM metadata WHERE key='manifest'").fetchone()[0])
        declarations = prior_manifest.get('operator_declarations',{})
        if declarations.get('assembly') != 'GRCh37' or declarations.get('strand') != 'forward':
            raise ValueError('Recheck requires previously confirmed GRCh37 forward candidates')
        revised.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value_json TEXT NOT NULL)')
        revised.execute('CREATE TABLE candidates(id INTEGER PRIMARY KEY,source_line INTEGER,row_json TEXT NOT NULL)')
        counts = dict(prior_manifest.get('counts',{}))
        counts.update(candidate_records=0,priority_candidates=0,identifier_disagreement_candidates=0)
        for identifier,line,raw in original.execute('SELECT id,source_line,row_json FROM candidates ORDER BY id'):
            record = json.loads(raw)
            row = record['observation']
            info = record['clinvar']['info']
            match = record['match']
            flags = build_flags(row,info,line,match['reference'],match['alternate'])
            record['flags'] = flags
            record['priority_for_manual_review'] = priority_for_review(info,flags)
            token_metadata(match,row.get('alleles') or [])
            revised.execute('INSERT INTO candidates VALUES(?,?,?)',(identifier,line,json.dumps(record,ensure_ascii=False)))
            counts['candidate_records'] += 1
            counts['priority_candidates'] += int(record['priority_for_manual_review'])
            counts['identifier_disagreement_candidates'] += int('marker_identifier_disagrees_with_reference' in flags)
        manifest = dict(prior_manifest)
        manifest.update(created_utc=now(),tool_version=VERSION,counts=counts,
                        derived_from={'sha256':source_hash,'previous_tool_version':prior_manifest.get('tool_version'),
                                      'operation':'offline candidate policy recheck; no array or reference rejoin'},
                        policy={'version':VERSION,'priority':'Pathogenic/Likely_pathogenic; no flags; germline review at least multiple submitters no conflicts'})
        limitations = list(manifest.get('limitations',[]))
        for text in ('Discordant rs identifiers require review; merged or unknown aliases are not resolved',
                     'Allele token counts do not establish copy number or biological ploidy'):
            if text not in limitations:
                limitations.append(text)
        manifest['limitations'] = limitations
        revised.execute('INSERT INTO metadata VALUES(?,?)',('manifest',json.dumps(manifest,ensure_ascii=False)))
        revised.commit()
        if revised.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
            raise ValueError('Rechecked SQLite integrity validation failed')
        write_json(sidecar,manifest)
        return manifest
    except BaseException:
        revised.close()
        output.unlink(missing_ok=True)
        sidecar.unlink(missing_ok=True)
        raise
    finally:
        original.close()
        revised.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    p = subs.add_parser('download'); p.add_argument('--url', required=True); p.add_argument('--output', required=True)
    p = subs.add_parser('index'); p.add_argument('--vcf', required=True); p.add_argument('--output', required=True)
    p = subs.add_parser('annotate'); p.add_argument('--staging', required=True); p.add_argument('--index', required=True); p.add_argument('--output', required=True)
    p.add_argument('--assembly', required=True, choices=['GRCh37']); p.add_argument('--strand', required=True, choices=['forward'])
    p = subs.add_parser('recheck'); p.add_argument('--source',required=True); p.add_argument('--output',required=True)
    args = vars(parser.parse_args()); command = args.pop('command')
    action = {'download':download,'index':build_index,'annotate':annotate,'recheck':recheck_candidates}[command]
    result = action(**args)
    print(json.dumps(result.get('counts', {'completed':command}), ensure_ascii=False))


if __name__ == '__main__':
    main()
