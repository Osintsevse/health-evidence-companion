"""Conservative, finite bilingual display aliases. Never replace source fields or assign LOINC codes.
A display row is a browsing family, not proof of analytic/clinical interchangeability.
"""
import json,re
from decimal import Decimal,InvalidOperation
VERSION='1.0'
ALIASES={}
def add(component,label,names):
 for name in names:ALIASES[name.casefold()]=(component,label)
add('glucose','Glucose',['\u0413\u043b\u044e\u043a\u043e\u0437\u0430','Glukoza','Glucose'])
add('alt','ALT',['\u0410\u043b\u0410\u0422','\u0410\u041b\u0422','ALT','ALT (SGPT)'])
add('ast','AST',['\u0410\u0441\u0410\u0422','\u0410\u0421\u0422','AST','AST (SGOT)'])
add('ggt','GGT',['\u0413\u0430\u043c\u043c\u0430-\u0413\u0422','\u0413\u0413\u0422','GGT'])
add('creatinine','Creatinine',['\u041a\u0440\u0435\u0430\u0442\u0438\u043d\u0438\u043d','Kreatinin','Creatinine'])
add('urea','Urea',['\u041c\u043e\u0447\u0435\u0432\u0438\u043d\u0430','Urea'])
add('cholesterol_total','Total cholesterol',['\u0425\u043e\u043b\u0435\u0441\u0442\u0435\u0440\u0438\u043d','Holesterol','Total cholesterol'])
add('cholesterol_hdl','HDL cholesterol',['HDL holesterol','\u0425\u043e\u043b\u0435\u0441\u0442\u0435\u0440\u0438\u043d \u041b\u041f\u0412\u041f'])
add('cholesterol_ldl','LDL cholesterol',['LDL holesterol','\u0425\u043e\u043b\u0435\u0441\u0442\u0435\u0440\u0438\u043d \u041b\u041f\u041d\u041f'])
add('cholesterol_non_hdl','Non-HDL cholesterol',['non-HDL holesterol'])
add('triglycerides','Triglycerides',['Trigliceridi','\u0422\u0440\u0438\u0433\u043b\u0438\u0446\u0435\u0440\u0438\u0434\u044b'])
add('crp','C-reactive protein',['\u0421-\u0440\u0435\u0430\u043a\u0442\u0438\u0432\u043d\u044b\u0439 \u0431\u0435\u043b\u043e\u043a','C REAKTIVNI PROTEIN','CRP'])
add('sodium','Sodium',['Natrijum','\u041d\u0430\u0442\u0440\u0438\u0439'])
add('potassium','Potassium',['Kalijum','\u041a\u0430\u043b\u0438\u0439'])
add('tsh','TSH',['TSH','\u0422\u0422\u0413'])
add('ft4','Free T4',['FT4','\u04224 \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0439'])
add('ft3','Free T3',['FT3','\u04223 \u0441\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0439'])
add('hemoglobin','Hemoglobin',['Hemoglobin','\u0413\u0435\u043c\u043e\u0433\u043b\u043e\u0431\u0438\u043d','HGB'])
add('hematocrit','Hematocrit',['Hematokrit','\u0413\u0435\u043c\u0430\u0442\u043e\u043a\u0440\u0438\u0442','HCT'])
add('erythrocytes','Erythrocytes',['RBC','Eritrociti','\u042d\u0440\u0438\u0442\u0440\u043e\u0446\u0438\u0442\u044b'])
add('leukocytes','Leukocytes',['WBC','Leukociti','\u041b\u0435\u0439\u043a\u043e\u0446\u0438\u0442\u044b'])
add('platelets','Platelets',['PLT','Trombociti','\u0422\u0440\u043e\u043c\u0431\u043e\u0446\u0438\u0442\u044b'])
add('mcv','MCV',['MCV','MCV (\u0441\u0440. \u043e\u0431\u044a\u0435\u043c \u044d\u0440\u0438\u0442\u0440.)'])
add('mch','MCH',['MCH','MCH (\u0441\u0440. \u0441\u043e\u0434\u0435\u0440. Hb \u0432 \u044d\u0440.)'])
add('mchc','MCHC',['MCHC','\u041c\u0421H\u0421 (\u0441\u0440. \u043a\u043e\u043d\u0446. Hb \u0432 \u044d\u0440.)'])
add('rdw','RDW',['RDW','RDW (\u0448\u0438\u0440. \u0440\u0430\u0441\u043f\u0440\u0435\u0434. \u044d\u0440\u0438\u0442\u0440)'])
add('mpv','MPV',['MPV'])
add('esr','ESR (Westergren)',['SE','Sedimentacija','\u0421\u041e\u042d (\u043f\u043e \u0412\u0435\u0441\u0442\u0435\u0440\u0433\u0440\u0435\u043d\u0443)'])
for comp,label,sr,ru in [('neutrophils','Neutrophils','Neutrofili','\u041d\u0435\u0439\u0442\u0440\u043e\u0444\u0438\u043b\u044b'),('lymphocytes','Lymphocytes','Limfociti','\u041b\u0438\u043c\u0444\u043e\u0446\u0438\u0442\u044b'),('monocytes','Monocytes','Monociti','\u041c\u043e\u043d\u043e\u0446\u0438\u0442\u044b'),('eosinophils','Eosinophils','Eozinofili','\u042d\u043e\u0437\u0438\u043d\u043e\u0444\u0438\u043b\u044b'),('basophils','Basophils','Bazofili','\u0411\u0430\u0437\u043e\u0444\u0438\u043b\u044b')]:
 add(comp,label,[sr,sr+' %',sr+' aps.',ru+', %',ru+', \u0430\u0431\u0441.',ru+' (\u043e\u0431\u0449.\u0447\u0438\u0441\u043b\u043e), %'])
URINE={}
for comp,label,names in [('appearance','Appearance',['Izgled']),('color','Color',['Boja','\u0426\u0432\u0435\u0442']),('specific_gravity','Specific gravity',['Relativna gustina','Specifična težina']),('ph','pH',['Reakcija (pH)','pH']),('protein','Protein',['Proteini']),('urobilinogen','Urobilinogen',['Urobilinogen']),('bilirubin','Bilirubin',['Bilirubin']),('ketones','Ketones',['Ketoni']),('nitrites','Nitrites',['Nitriti']),('esterase','Leukocyte esterase',['Leukocitna esteraza']),('ascorbic_acid','Ascorbic acid',['Askorbinska kiselina']),('bacteria','Bacteria',['Bakterije']),('crystals','Crystals',['Kristali']),('mucus','Mucus',['Sluz']),('other','Other',['Ostalo'])]:
 for n in names:URINE[n.casefold()]=(comp,label)
UNIT_ALIASES={}
def unit(target,factor,*names):
 for name in names:UNIT_ALIASES[name]=(target,Decimal(factor))
unit('mmol/L','1','mmol/L','\u043c\u043c\u043e\u043b\u044c/\u043b');unit('umol/L','1','umol/L','µmol/L','μmol/L','\u043c\u043a\u043c\u043e\u043b\u044c/\u043b')
unit('U/L','1','U/L','\u0415\u0434/\u043b','\u0435\u0434/\u043b');unit('g/L','1','g/L','\u0433/\u043b');unit('g/L','10','g/dL','\u0433/\u0434\u043b')
unit('mg/L','1','mg/L','\u043c\u0433/\u043b');unit('pmol/L','1','pmol/L','\u043f\u043c\u043e\u043b\u044c/\u043b')
unit('mIU/L','1','uIU/mL','µIU/mL','mIU/L','\u043c\u0415\u0434/\u043b')
unit('10^9/L','1','10^9/L','10*9/L','\u0442\u044b\u0441/\u043c\u043a\u043b');unit('10^12/L','1','10^12/L','10*12/L','\u043c\u043b\u043d/\u043c\u043a\u043b')
unit('fL','1','fL','fl','\u0444\u043b');unit('pg','1','pg','\u043f\u0433');unit('mm/h','1','mm/h','mm/1h','\u043c\u043c/\u0447');unit('%','1','%')
unit('mL/min','1','ml/min.','ml/min');unit('mL/min/1.73m2','1','ml/min/1.73 m2')
FRACTIONS={'neutrophils','lymphocytes','monocytes','eosinophils','basophils'}
ORDINAL_URINE={'glucose','hemoglobin','protein','urobilinogen','bilirubin','ketones','nitrites','esterase','ascorbic_acid'}
def category(row):
 m=(row.get('method_raw') or '').lower();s=(row.get('specimen_raw') or '').lower()
 if 'abpm' in m:return 'vitals'
 if any(x in m for x in ('\u0443\u0437\u0438','ultrasound','spirom')):return 'investigations'
 if any(x in m for x in ('clinical measurement','office vital')) or row.get('unit_raw') in ('mmHg','bpm'):return 'vitals'
 if s in ('u','urine') or '\u043c\u043e\u0447' in s:return 'urine'
 if '\u043a\u0430\u043b' in s or 'stool' in s:return 'stool'
 return 'blood'
def normalize(row):
 cat=category(row);name=row['analyte_name_raw'];u=row.get('unit_raw') or '';spec=row.get('specimen_raw') or '';method=row.get('method_raw') or ''
 token=re.sub(r'^KS\s*-\s*','',name,flags=re.I).strip().casefold()
 mapping=(URINE.get(token) if cat=='urine' else None) or ALIASES.get(token)
 component,label=mapping or ('raw:'+name,name)
 target,factor=UNIT_ALIASES.get(u,(u,Decimal(1)))
 prop='quantitative' if u else 'unspecified';guard='';scope=cat
 if component in FRACTIONS:
  if target=='%':prop='number_fraction';label+=', %'
  elif target=='10^9/L':prop='number_concentration';label+=', absolute count'
  else:component='raw:'+name
 if component=='hematocrit' and u=='L/L':target='%';factor=Decimal(100);prop='volume_fraction'
 elif component=='hematocrit' and u=='%':prop='volume_fraction'
 if cat=='urine' and component in ORDINAL_URINE and u in ('','arb.jed.'):
  target='qualitative / arbitrary scale';prop='ordinal';factor=Decimal(1)
 if cat=='urine' and component in ('bacteria','crystals','mucus','other') and u in ('','/'):
  target='description';prop='narrative'
 if component=='esr':
  if token=='\u0441\u043e\u044d (\u043f\u043e \u0432\u0435\u0441\u0442\u0435\u0440\u0433\u0440\u0435\u043d\u0443)' or method.casefold() in ('wgr','westergren'):guard='Westergren'
  else:guard='method_unknown';label='ESR (method unknown)'
 if component.startswith('raw:'):guard=json.dumps([spec,method],ensure_ascii=False)
 # Any explicitly named special method stays distinct. This is a display family only.
 if re.search(r'\u044d\u043b\u0435\u043a\u0442\u0440\u043e\u0444\u043e\u0440|electrophor',method,re.I):guard=method
 if component=='cholesterol_ldl' and re.search(r'calc|\u0440\u0430\u0447\u0443\u043d|račun|friedewald',method,re.I):guard='calculated'
 key=json.dumps([cat,component,prop,target,guard],ensure_ascii=False)
 numeric=row.get('numeric_value');converted=None
 if numeric is not None and row.get('review_status') in ('verified_from_source','user_confirmed'):
  try:converted=format(Decimal(str(numeric))*factor,'f')
  except InvalidOperation:pass
 value=row['raw_value']
 if factor!=1 and converted is not None:
  value=converted.rstrip('0').rstrip('.') if '.' in converted else converted
  if row.get('comparator') not in (None,'='):value=str(row['comparator'])+value
  if '*' in row['raw_value']:value+='*'
 note='Browsing family only; analytic and clinical comparability are not established. Original specimen, method, result and reference remain available.'
 if not spec:note+=' Exact specimen is not recorded in the source row.'
 if factor!=1:note+=' Display conversion: '+u+' -> '+target+', factor '+str(factor)+'. The reference remains in source units.'
 return {'mapping_version':VERSION,'component':component,'row_key':key,'label':label,'unit':target,'factor':str(factor),'display_value':value,'display_numeric_value':converted,'property':prop,'category':cat,'method_guard':guard,'raw_name':name,'raw_unit':u,'raw_specimen':spec,'raw_method':method,'mapping_status':'display_group_only' if mapping else 'raw_identity_retained','comparability_status':'not_established','loinc_code':None,'note':note}
