"""Read-only numerical review and source-linked chart projection; no diagnosis or forecasting."""
import datetime, decimal, hashlib, json, math, re
D=decimal.Decimal
REVIEWED={'verified_from_source','user_confirmed'}
NUM=r'[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)'
def number(v):
 try:
  d=D(str(v).replace(',','.'))
  return d if d.is_finite() else None
 except decimal.InvalidOperation:return None

def day(v):
 if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):return None
 try:return datetime.date.fromisoformat(v)
 except ValueError:return None

def reference(r,overrides):
 """Only complete unambiguous simple syntax or a reviewed exact-source override."""
 raw=r.get('reference_range_raw') or ''
 if r.get('reference_unit_raw') and r.get('reference_unit_raw')!=r.get('unit_raw'):
  return {'low':None,'high':None,'raw':raw,'kind':'reference_unit_mismatch'}
 override=overrides.get(r['entry_id'])
 if override:
  if override.get('raw')!=raw:raise ValueError('Reference override no longer matches source')
  return {**override,'reviewed_override':True}
 lo,hi=number(r.get('reference_low')),number(r.get('reference_high'))
 if lo is not None and hi is not None and lo>hi:
  return {'low':None,'high':None,'raw':raw,'kind':'invalid_interval'}
 if lo is not None or hi is not None:
  return {'low':str(lo) if lo is not None else None,'high':str(hi) if hi is not None else None,'low_inclusive':True,'high_inclusive':True,'raw':raw,'kind':'interval'}
 raw_clean=raw.strip().replace('\u2212','-').replace('\u2013','-').replace('\u2264','<=').replace('\u2265','>=')
 m=re.fullmatch(r'\(?\s*('+NUM+r')\s*-\s*('+NUM+r')\s*\)?',raw_clean)
 if m and number(m[1])<=number(m[2]):
  return {'low':str(number(m[1])),'high':str(number(m[2])),'low_inclusive':True,'high_inclusive':True,'raw':raw,'kind':'interval'}
 m=re.fullmatch(r'([<>]=?)\s*('+NUM+r')',raw_clean)
 if m:
  return {'low':str(number(m[2])) if m[1].startswith('>') else None,'high':str(number(m[2])) if m[1].startswith('<') else None,'low_inclusive':m[1]=='>=','high_inclusive':m[1]=='<=','raw':raw,'kind':'limit'}
 return {'low':None,'high':None,'raw':raw,'kind':'unparsed'}

def flag(v,ref):
 lo,hi=number(ref.get('low')),number(ref.get('high'))
 if lo is not None and (v<lo or (v==lo and not ref.get('low_inclusive',True))):return 'below'
 if hi is not None and (v>hi or (v==hi and not ref.get('high_inclusive',True))):return 'above'
 return 'within' if lo is not None or hi is not None else 'unknown'

def category(r):
 n=r.get('_display',{})
 if any(x in (r.get('method_raw') or '').lower() for x in ['ultrasound','\u0443\u0437\u0438','spirom']):return 'investigations'
 if n.get('category'):return n['category']
 if r.get('unit_raw') in ('kg','cm','\u043a\u0433','\u0441\u043c','\xb0C','mmHg','bpm') or any(x in (r.get('method_raw') or '').lower() for x in ['abpm','measurement','office vital','owner measurement']):return 'vitals'
 s=(r.get('specimen_raw') or '').lower()
 return 'urine' if s in ('u','urine') or '\u043c\u043e\u0447' in s else 'stool' if 'stool' in s or '\u043a\u0430\u043b' in s else 'blood'

def fingerprint(rows):
 return hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def build_dashboard(model,config):
 families={};excluded=[];overrides=config.get('lab_reference_overrides',{})
 asof=day(model.get('as_of'))
 for r in model['tables']['observations']:
  n=r.get('_display',{});cat=category(r)
  if cat not in ('blood','urine','stool','vitals','investigations'):continue
  key=n.get('row_key') or json.dumps([cat,r['analyte_name_raw'],r.get('unit_raw'),r.get('specimen_raw'),r.get('method_raw')],ensure_ascii=False)
  f=families.setdefault(key,{'key':key,'name':n.get('label') or r['analyte_name_raw'],'unit':n.get('unit') or r.get('unit_raw') or '', 'category':cat,'component':n.get('component') or r['analyte_name_raw'],'points':[],'excluded':[]})
  reason=None;date=day(r.get('event_date'));v=number(r.get('numeric_value'))
  if r.get('review_status') not in REVIEWED:reason='unreviewed'
  elif not date or r.get('event_date_precision')!='day':reason='imprecise_date'
  elif asof and date>asof:reason='future_date'
  elif r.get('comparator')!='=':reason='non_exact'
  elif v is None:reason='non_numeric'
  elif r.get('record_status')!='active':reason='inactive'
  if reason:
   x={'entry_id':r['entry_id'],'reason':reason,'source':r};excluded.append(x);f['excluded'].append(x);continue
  if not math.isfinite(float(v)):
   x={'entry_id':r['entry_id'],'reason':'non_finite_plot_value','source':r};excluded.append(x);f['excluded'].append(x);continue
  factor=number(n.get('factor','1'))
  if factor is None or factor<=0:raise ValueError('Invalid reviewed display factor')
  shown=number(n.get('display_numeric_value')) if n else v
  if shown is None or shown!=v*factor:raise ValueError('Display value must match reviewed factor')
  if not math.isfinite(float(shown)):
   x={'entry_id':r['entry_id'],'reason':'non_finite_plot_value','source':r};excluded.append(x);f['excluded'].append(x);continue
  ref=reference(r,overrides);stat=flag(v,ref)
  display_ref={**ref,'low':float(number(ref['low'])*factor) if number(ref.get('low')) is not None else None,'high':float(number(ref['high'])*factor) if number(ref.get('high')) is not None else None}
  context=[r.get('specimen_raw'),r.get('method_raw'),r.get('laboratory_raw')]
  p={'id':r['entry_id'],'date':date.isoformat(),'value':float(shown),'display_value':str(shown),'raw_value':r['raw_value'],'raw_unit':r.get('unit_raw'),'reference':display_ref,'reference_status':stat,'printed_flag':r.get('flag_raw'),'context':context,'source':r}
  f['points'].append(p)
 for f in families.values():
  f['points'].sort(key=lambda p:(p['date'],p['id']))
  f['latest']=f['points'][-1] if f['points'] else None
  f['trend']=None
  # Same-date multiplicity cannot identify a unique latest or previous collection.
  ps=f['points']
  if len(ps)>=2 and len([p for p in ps if p['date']==ps[-1]['date']])==1:
   previous=[p for p in ps if p['date']<ps[-1]['date']]
   if previous:
    p=previous[-1];q=ps[-1]
    if len([x for x in previous if x['date']==p['date']])==1 and all(q['context']) and p['context']==q['context']:
     f['trend']={'from':p['date'],'to':q['date'],'delta':float(D(q['display_value'])-D(p['display_value'])),'entry_ids':[p['id'],q['id']],'status':'same_recorded_context_not_clinically_validated'}
  f['historical_flags']=[p for p in ps if p['reference_status'] in ('above','below') or p.get('printed_flag')]
 items=sorted(families.values(),key=lambda f:(f['category'],f['name'].casefold(),f['unit']))
 return {'version':'1.0','as_of':model.get('as_of'),'series':items,'excluded':excluded,'point_count':sum(len(f['points']) for f in items),'labels':config.get('lab_dashboard_labels',{}),'presets':config.get('lab_presets',[]),'default_components':config.get('lab_dashboard_default_components',[]),'default_from':config.get('lab_default_from'),'questionnaire':config.get('health_questionnaire',[])}


def review_fingerprint(model):
 return fingerprint({'tables':model['tables'],'medication_reconciliation':model.get('medication_reconciliation'),'current_medications':model.get('current_medications'),'context':model.get('context')})

def attach_assessment(model,config):
 import copy
 report=copy.deepcopy(model.get('health_review') or config.get('health_review'))
 if report:
  report['stale']=report.get('source_fingerprint')!=review_fingerprint(model)
  ids={r['entry_id'] for rs in model['tables'].values() for r in rs}
  if any(id not in ids for item in report.get('items',[]) for id in item.get('entry_ids',[])):report['stale']=True
 model['health_review']=report
 return model
