"""Compile public source metadata without changing canonical IDs or review dates."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def catalog(root=ROOT):
    medical=json.loads((root/'knowledge/sources.json').read_text(encoding='utf-8'))
    psychological=json.loads((root/'knowledge/psychology/sources.json').read_text(encoding='utf-8'))
    records=[]
    for source in medical:
        records.append({'namespace':'medical','id':source['id'], 'qualified_id':'medical:'+source['id'],
            'title':source['title'],'url':source['url'],'checked_on':source['checked_on'],
            'reading_status':source['retrieval_status'],'limitations':source['retrieval_status'],
            'purpose':source['use'],'region':source['region'], 'canonical_path':'knowledge/sources.json'})
    for source in psychological['sources']:
        records.append({'namespace':'psychology','id':source['id'],'qualified_id':'psychology:'+source['id'],
            'title':source['title'],'url':source['url'],'checked_on':source['checked_at'],
            'reading_status':source['access'],'limitations':source['limitations'],
            'purpose':source['use'],'region':'Original psychological source applicability; inspect canonical record',
            'canonical_path':'knowledge/psychology/sources.json'})
    identities=[row['qualified_id'] for row in records]
    if len(set(identities))!=len(identities):raise ValueError('Duplicate qualified source identifier')
    groups=defaultdict(list)
    for row in records:groups[row['url']].append(row['qualified_id'])
    return {'schema':'unified-source-catalog-v1','record_count':len(records),
        'unique_url_count':len(groups), 'records':records,
        'shared_urls':[{'url':url,'qualified_ids':ids} for url,ids in sorted(groups.items()) if len(ids)>1],
        'limitations':'Record and URL counts are not independent study counts. Import preserves historical reading scope, not a new literature review.'}

def update(root=ROOT):
    result=catalog(root)
    (root/'knowledge/source-catalog.json').write_text(json.dumps(result,ensure_ascii=True,indent=2)+'\n',encoding='utf-8',newline='\n')
    return result

if __name__=='__main__':
    result=update()
    print(json.dumps({'records':result['record_count'],'unique_urls':result['unique_url_count']}))
