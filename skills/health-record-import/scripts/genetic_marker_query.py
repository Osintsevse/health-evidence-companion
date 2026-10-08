"""Private identifier inventory with optional offline public locus cross-reference."""
import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile

PUBLIC_ROOT = (next((p for p in Path(__file__).resolve().parents
                     if (p/'plugin.json').is_file() and (p/'skills').is_dir()), None)
               or next((p for p in Path(__file__).resolve().parents
                        if (p/'SKILL.md').is_file() and (p/'scripts').is_dir()), None))


def coordinate(row):
    try:
        c = str(row['chromosome_raw']).removeprefix('chr').upper()
        c = {'23':'X','24':'Y','M':'MT'}.get(c,c)
        p = int(row['position_raw'])
        return (c,p) if p > 0 else None
    except (KeyError,ValueError,TypeError):
        return None


def marker_query(staging, rsids, reference_index=None, assembly=None, strand=None):
    """Literal identifier rows and reference-locus rows remain separate; no allele inference."""
    rsids = list(dict.fromkeys(rsids))
    if not 1 <= len(rsids) <= 10000 or any(not isinstance(x,str) or not x or len(x)>128 for x in rsids):
        raise ValueError('Require 1-10000 identifiers of at most 128 characters')
    hits = {x:[] for x in rsids}
    reference_hits = {x:[] for x in rsids}
    locus_hits = {x:[] for x in rsids}
    locus_owners = {}
    reference_manifest = None
    if reference_index is not None:
        if assembly != 'GRCh37' or strand != 'forward':
            raise ValueError('Reference-locus inventory requires GRCh37 and forward declarations')
        numeric_ids = {}
        for identifier in rsids:
            match = re.fullmatch(r'rs([0-9]+)',identifier)
            if match:
                numeric_ids.setdefault(match.group(1),[]).append(identifier)
        with closing(sqlite3.connect(Path(reference_index).resolve().as_uri()+'?mode=ro',uri=True)) as reference:
            reference_manifest = json.loads(reference.execute("SELECT value_json FROM metadata WHERE key='manifest'").fetchone()[0])
            if reference_manifest.get('assembly') != 'GRCh37':
                raise ValueError('Reference index assembly must be GRCh37')
            # One public index scan, including comma/pipe separated rs aliases.
            query = "SELECT chrom,pos,ref,alt,variation_id,source_line,json_extract(info_json,'$.RS') FROM variants WHERE json_extract(info_json,'$.RS') IS NOT NULL"
            for c,p,r,a,vid,line,raw_rs in reference.execute(query):
                for number in set(re.split(r'[,|]',str(raw_rs))):
                    for identifier in numeric_ids.get(number,[]):
                        reference_hits[identifier].append({'chromosome':c,'position':p,'reference':r,'alternate':a,'variation_id':vid,'source_vcf_line':line})
                        loc = coordinate({'chromosome_raw':c,'position_raw':p})
                        locus_owners.setdefault(loc,set()).add(identifier)
    staging_path = Path(staging)
    with closing(sqlite3.connect(staging_path.resolve().as_uri()+'?mode=ro',uri=True)) as db:
        metadata = {k:json.loads(v) for k,v in db.execute('SELECT key,value_json FROM metadata')}
        if reference_index is not None:
            known_assembly = str(metadata.get('assembly','unknown')).lower()
            known_strand = str(metadata.get('strand','unknown')).lower()
            if known_assembly not in ('unknown','grch37','build37','hg19','none') or known_strand not in ('unknown','forward','plus','none'):
                raise ValueError('Staging declarations contradict reference-locus inventory')
            declarations = json.dumps({k:v for k,v in metadata.items() if k in ('assembly_raw','strand_raw','comments','comments_raw','headers','header_comments')}).lower()
            if re.search(r'grch[ _-]?(?:36|38)|build[ _-]?(?:36|38)|hg(?:18|38)|\b(?:reverse|minus)\b',declarations):
                raise ValueError('Raw staging declarations contradict GRCh37 forward')
        selected_loci = set()
        for source_line,raw in db.execute('SELECT source_line,row_json FROM observations ORDER BY source_line'):
            row = json.loads(raw)
            loc = coordinate(row)
            if row.get('rsid_raw') in hits:
                hits[row['rsid_raw']].append(row)
                if loc is not None:
                    selected_loci.add(loc)
            for identifier in locus_owners.get(loc,[]):
                locus_hits[identifier].append(row)
        neighbours = []
        for source_line,raw in db.execute('SELECT source_line,row_json FROM observations ORDER BY source_line'):
            row = json.loads(raw)
            if coordinate(row) in selected_loci and row.get('rsid_raw') not in hits:
                neighbours.append(row)
    sha = hashlib.sha256()
    with staging_path.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):
            sha.update(chunk)
    markers = []
    for identifier in sorted(rsids):
        status = 'observed' if hits[identifier] else ('identifier_absent_locus_observed' if locus_hits[identifier] else 'absent_from_export')
        markers.append({'rsid':identifier,'status':status,'observations':hits[identifier],
                        'reference_records':reference_hits[identifier],
                        'observations_at_reference_loci':locus_hits[identifier]})
    return {'schema':'private-marker-query-v2','staging_sha256':sha.hexdigest(),'staging_metadata':metadata,
            'markers':markers,'other_observations_at_selected_loci':neighbours,
            'reference_manifest':reference_manifest,
            'operator_declarations':{'assembly':assembly,'strand':strand} if reference_index else None,
            'limitations':['Identifier absence does not establish an unmeasured locus or allele absence',
                           'Reference-locus rows are coordinate cross-references only, without allele equivalence or clinical inference',
                           'All original calls and flags are preserved',
                           'Public ClinVar SNP index is incomplete; rs aliases may be missing']}


def write_private(output, data):
    path = Path(output).resolve()
    if PUBLIC_ROOT and (path == PUBLIC_ROOT or PUBLIC_ROOT in path.parents):
        raise ValueError('Private marker output must be outside the public repository')
    if path.exists():
        raise FileExistsError(path)
    descriptor,temporary = tempfile.mkstemp(prefix='.marker-',suffix='.tmp',dir=path.parent)
    try:
        with os.fdopen(descriptor,'w',encoding='utf-8') as stream:
            json.dump(data,stream,ensure_ascii=False,indent=2)
        if os.name == 'nt':
            os.rename(temporary,path)
        else:
            os.link(temporary,path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--staging',required=True)
    parser.add_argument('--rsid',action='append',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--reference-index')
    parser.add_argument('--assembly',choices=['GRCh37'])
    parser.add_argument('--strand',choices=['forward'])
    args=parser.parse_args()
    result=marker_query(args.staging,args.rsid,args.reference_index,args.assembly,args.strand)
    write_private(args.output,result)
    print(json.dumps({'markers':len(result['markers']),'completed':True}))


if __name__ == '__main__': main()
