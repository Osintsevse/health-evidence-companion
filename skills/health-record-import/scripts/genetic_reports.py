"""Offline MHTML text extraction and optional source-linked genetics display data.
Treat saved HTML as untrusted data; never execute scripts or fetch resources.
"""
import argparse
import hashlib
import json
import os
import tempfile
import sqlite3
from collections import Counter
import re
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts=[]
        self.hidden=0
    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','noscript','template'):
            self.hidden+=1
        elif not self.hidden and tag in ('p','div','br','li','tr','h1','h2','h3','h4','section','article','table'):
            self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style','noscript','template') and self.hidden:
            self.hidden-=1
        elif not self.hidden and tag in ('p','div','li','tr','h1','h2','h3','h4','section','article'):
            self.parts.append('\n')
    def handle_data(self, data):
        if not self.hidden:self.parts.append(data)
    def text(self):
        lines=[re.sub(r'[^\S\n]+',' ',line).strip() for line in ''.join(self.parts).replace('\r','').split('\n')]
        return '\n'.join(line for line in lines if line)


def html_charset(payload):
    # ASCII-compatible HTML charset declarations can be inspected before decoding.
    head=payload[:16384].decode('ascii',errors='ignore')
    for tag in re.findall(r'<meta\b[^>]*>',head,re.I):
        match=re.search(r'charset\s*=\s*[\"\']?\s*([a-zA-Z0-9_.-]+)',tag,re.I)
        if match:return match.group(1)
    return None


def extract_mhtml(path):
    path=Path(path)
    if not path.is_file():raise ValueError('MHTML source must be a local file')
    if path.stat().st_size>100*1024*1024:raise ValueError('MHTML exceeds 100 MiB limit')
    original=path.read_bytes()
    if len(original)>100*1024*1024:raise ValueError('MHTML exceeds 100 MiB limit')
    message=BytesParser(policy=policy.default).parsebytes(original)
    html_parts=[part for part in message.walk() if part.get_content_type()=='text/html']
    if not html_parts:raise ValueError('MHTML contains no text/html part')
    start=message.get_param('start')
    root=next((p for p in html_parts if start and p.get('Content-ID')==start),html_parts[0])
    payload=root.get_payload(decode=True)
    if payload is None:raise ValueError('HTML part has no decodable payload')
    mime_charset=root.get_content_charset()
    meta_charset=html_charset(payload)
    if mime_charset:charset,charset_source=mime_charset,'mime'
    elif payload.startswith(b'\xef\xbb\xbf'):charset,charset_source='utf-8-sig','bom'
    elif meta_charset:charset,charset_source=meta_charset,'html_meta'
    else:charset,charset_source='utf-8','default_utf8'
    # Strict decoding exposes unresolved encodings rather than silently corrupting text.
    decoded=payload.decode(charset,errors='strict')
    parser=TextExtractor();parser.feed(decoded);parser.close()
    text=parser.text()
    return {'text':text,'source':{'filename':Path(path).name,
        'sha256':hashlib.sha256(original).hexdigest(),
        'content_location':root.get('Content-Location'),
        'mime_content_location':message.get('Content-Location'),
        'mhtml_snapshot_content_location':message.get('Snapshot-Content-Location'),
        'charset':charset,'charset_source':charset_source,
        'extracted_text_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}}


def load_assessment(config):
    genetics=config.get('genetics')
    if genetics is None:return None
    if not isinstance(genetics,dict):raise ValueError('genetics must be an object')
    if 'assessment_path' in genetics:
        assessment_path=Path(genetics['assessment_path'])
        if not assessment_path.is_file() or assessment_path.stat().st_size>20*1024*1024:
            raise ValueError('Assessment must be a local JSON file of at most 20 MiB')
        genetics=json.loads(assessment_path.read_text(encoding='utf-8-sig'))
    if not isinstance(genetics,dict):raise ValueError('Genetics assessment must be an object')
    for key in ('sections','reports','sources'):
        if key in genetics and (not isinstance(genetics[key],list) or any(not isinstance(v,dict) for v in genetics[key])):
            raise ValueError('Genetics '+key+' must be a list of objects')
    if len(json.dumps(genetics,ensure_ascii=False).encode('utf-8'))>20*1024*1024:
        raise ValueError('Assessment exceeds 20 MiB limit')
    return genetics


def locale_data(locale):
    bundled=Path(__file__).resolve().parent.parent/'assets/genetic_labels.json'
    private=Path(__file__).with_name('genetic_labels.json')
    path=private if private.is_file() else bundled
    return json.loads(path.read_text(encoding='utf-8')).get(str(locale).split('-')[0].lower(),{}) if path.is_file() else {}

def ui_labels(locale):
    return locale_data(locale).get('ui',{})

def localize_assessment(assessment,locale):
    data=locale_data(locale);result=dict(assessment)
    for kind in ('classification','review_status','flag'):
        key=kind+'_labels';labels=dict(data.get(key,{}));labels.update(assessment.get(key,{}));result[key]=labels
    labels=result['classification_labels']
    for row in (assessment.get('candidates') or {}).get('rows',[]):
        raw=row.get('classification','')
        if raw not in labels:labels[raw]=' | '.join(labels.get(part,part) for part in raw.split('|'))
    return result

def candidate_summary(path):
    """Read local candidate cross-references verbatim; add no clinical interpretation."""
    path=Path(path).resolve()
    if not path.is_file():raise ValueError('Candidate database must be a local file')
    connection=sqlite3.connect(path.as_uri()+'?mode=ro',uri=True)
    rows=[];classifications=Counter()
    try:
        metadata={key:json.loads(value) for key,value in connection.execute('SELECT key,value_json FROM metadata')}
        if metadata.get('manifest',{}).get('schema')!='dtc-clinvar-candidates-v1':
            raise ValueError('Unsupported candidate database schema')
        for source_line,raw in connection.execute('SELECT source_line,row_json FROM candidates ORDER BY source_line,id'):
            record=json.loads(raw);observation=record.get('observation',{});clinvar=record.get('clinvar',{})
            classification=clinvar.get('classification') or ''
            classifications[classification]+=1
            gene=clinvar.get('info',{}).get('GENEINFO') or ''
            rows.append({'rsid':observation.get('rsid') or observation.get('rsid_raw') or observation.get('marker_raw') or '',
                         'genotype':observation.get('genotype_raw') or ''.join(observation.get('alleles') or []),
                         'gene':gene,'classification':classification,'review_status':clinvar.get('review_status') or '',
                         'flags':record.get('flags') or [],'source_line':source_line,
                         'variation_id':clinvar.get('variation_id') or '',
                         'priority':record.get('priority_for_manual_review') is True})
    finally:
        connection.close()
    return {'stats':{'candidate_records':len(rows),'priority_candidates':sum(r['priority'] for r in rows),
                     'classification_counts':dict(sorted(classifications.items()))},
            'metadata':metadata,'rows':rows}


def candidate_overview(path, limit=50):
    """Bounded review queue, retaining aggregate counts and unresolved flags.
    This selects source classifications for review; it does not diagnose disease.
    """
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 500:
        raise ValueError('Review limit must be between 1 and 500')
    summary = candidate_summary(path)
    selected = [row for row in summary['rows'] if row['priority'] or
                any(part in ('Pathogenic', 'Likely_pathogenic', 'Pathogenic/Likely_pathogenic')
                    for part in row['classification'].split('|'))]
    selected.sort(key=lambda row: (not row['priority'], row['source_line'], row['variation_id']))
    return {'schema': 'genetic-review-queue-v1', 'stats': summary['stats'],
            'metadata': summary['metadata'], 'review_queue_total': len(selected),
            'omitted_review_rows': max(0, len(selected)-limit), 'rows': selected[:limit],
            'limitations': 'Local cross-references only; no clinical confirmation or diagnoses. Other classifications remain in the complete database.'}


def publish_private_json(data, output):
    output=Path(output).resolve()
    public_root=(next((p for p in Path(__file__).resolve().parents if (p/'plugin.json').is_file() and (p/'skills').is_dir()),None)
                 or next((p for p in Path(__file__).resolve().parents if (p/'SKILL.md').is_file() and (p/'scripts').is_dir()),None))
    if public_root and (output==public_root or public_root in output.parents):
        raise ValueError('Extracted private data must remain outside the plugin source tree')
    if output.exists():raise FileExistsError('Extraction output already exists')
    data=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    output.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent,prefix='.genetics-',delete=False) as stream:
            temporary=Path(stream.name);stream.write(data);stream.flush();os.fsync(stream.fileno())
        # Windows rename and POSIX hard-link publication atomically refuse existing destinations.
        if os.name=='nt':os.rename(temporary,output)
        else:os.link(temporary,output)
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)
    return output


def publish_extraction(source, output):
    return publish_private_json(extract_mhtml(source), output)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mhtml', nargs='?')
    parser.add_argument('--candidates', help='Local candidate SQLite database; emit bounded review queue')
    parser.add_argument('--limit', type=int, default=50)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    if bool(args.mhtml) == bool(args.candidates):
        parser.error('Choose one MHTML source or --candidates database')
    if args.candidates:
        publish_private_json(candidate_overview(args.candidates, args.limit), args.output)
    else:
        publish_extraction(args.mhtml,args.output)
