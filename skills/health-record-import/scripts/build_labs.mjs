// Host adapter: author a private XLSX from a generated model using Artifact Tool.
// No network, account access or clinical interpretation. Native import is a separate operation.
import fs from 'node:fs/promises';
import path from 'node:path';
import {Workbook,SpreadsheetFile} from '@oai/artifact-tool';
const args=process.argv.slice(2);
function arg(name){const i=args.indexOf(name);if(i<0||!args[i+1])throw Error('Missing '+name);return args[i+1]}
const model=JSON.parse(await fs.readFile(arg('--model'),'utf8'));
const output=arg('--output'),previewDir=arg('--preview-dir');
const L=model.labels;
const workbook=Workbook.create();
const literal=v=>typeof v==='string'&&/^[\s]*[=+\-@]/.test(v)?"'"+v:v;
const pad=(rows,width)=>rows.map(r=>{const a=r.map(literal);while(a.length<width)a.push(null);return a});
function sourceRow(r){return [r.event_date,r.analyte_name_raw,r.raw_value,r.unit_raw,r.reference_range_raw,r.flag_raw,r.specimen_raw,r.laboratory_raw,r.source_document_id,r.source_locator,r.review_status,r.uncertainties]}
function category(r){const s=(r.specimen_raw||'').toLowerCase();const m=(r.method_raw||'').toLowerCase();if(m.includes('abpm')||['mmHg','bpm'].includes(r.unit_raw))return 'vitals';if(m.includes('\u0443\u0437\u0438'))return 'investigations';if(s==='u'||s.includes('\u043c\u043e\u0447'))return 'urine';if(s.includes('\u043a\u0430\u043b'))return 'stool';return'blood'}
const rendered=[];
function writeSheet(name,headers,rows,widths){
 const sheet=workbook.worksheets.add(name);
 const values=pad([headers,...rows],headers.length);
 sheet.getRangeByIndexes(0,0,values.length,headers.length).values=values;
 const full=sheet.getRangeByIndexes(0,0,values.length,headers.length);
 full.format.font={name:'Arial',size:10,color:'#172638'};
 full.format.verticalAlignment='top';
 const head=sheet.getRangeByIndexes(0,0,1,headers.length);
 head.format.fill='#EEF1F4';head.format.font={name:'Arial',size:10,bold:true,color:'#172638'};
 head.format.wrapText=true;head.format.rowHeightPx=76;
 sheet.freezePanes.freezeRows(1);
 sheet.freezePanes.freezeColumns(Math.min(4,headers.length));
 for(let j=0;j<headers.length;j++)sheet.getRangeByIndexes(0,j,values.length,1).format.columnWidthPx=widths?.[j]||165;
 if(rows.length)sheet.getRangeByIndexes(1,0,rows.length,1).setNumberFormat('yyyy-mm-dd');
 rendered.push({sheet,name,rows:rows.length,cols:headers.length});return sheet;
}
for(const kind of ['blood','urine','stool']){
 const events=model.matrix.events.filter(r=>r.category===kind);
 if(!events.length)continue;
 const keys=new Set(events.flatMap(r=>Object.keys(r.cells)));
 const cols=model.matrix.columns.filter(c=>keys.has(c.key));
 const headers=[L.date,L.lab,L.specimen,L.source,...cols.map(c=>c.name+(c.unit?' ['+c.unit+']':'')+(c.specimen?' {'+c.specimen+'}':''))];
 const formats=[];
 const rows=events.map((event,i)=>{
  const date=/^\d{4}-\d{2}-\d{2}$/.test(event.date)?new Date(event.date+'T00:00:00Z'):event.date;
  const vals=[date,event.laboratory,event.specimen,event.document_ids.filter(Boolean).join('; ')||L.reported];
  for(const [j,c]of cols.entries()){
   const cell=event.cells[c.key]||[];
   if(!cell.length){vals.push(null);continue}
   if(cell.length===1&&cell[0].numeric_value!==null&&cell[0].comparator==='='){
    const r=cell[0],value=Number(r.numeric_value);if(!Number.isFinite(value))throw Error('Nonfinite value');vals.push(value);
    const places=(r.numeric_value.split('.')[1]||'').length;
    const flag=r.flag_raw?' "'+r.flag_raw.replaceAll('"','')+'"':'';
    formats.push({row:i+1,col:j+4,format:'0'+(places?'.'+'0'.repeat(places):'')+flag});
   }else vals.push(cell.map(r=>r.raw_value+(r.flag_raw?' '+r.flag_raw:'')).join(' / '));
  }return vals;
 });
 const sheet=writeSheet(L[kind],headers,rows,[125,240,130,200]);
 for(const f of formats)sheet.getCell(f.row,f.col).setNumberFormat(f.format);
}
const details=model.tables.observations.filter(r=>['blood','urine','stool'].includes(category(r)));
const headers=[L.date,L.sourceText,L.result,L.unit,L.reference,L.printedFlag,L.specimen,L.lab,L.source,L.details,L.dataStatus,L.note];
writeSheet(L.sourceNote,headers,details.map(r=>{const x=sourceRow(r);if(/^\d{4}-\d{2}-\d{2}$/.test(x[0]||''))x[0]=new Date(x[0]+'T00:00:00Z');return x}),[125,280,180,130,380,110,150,250,160,330,210,450]);
workbook.recalculate();
await fs.mkdir(previewDir,{recursive:true});
for(const r of rendered){
 const preview=await workbook.render({sheetName:r.name,range:'A1:H'+Math.min(r.rows+1,12),scale:1,format:'png'});
 await fs.writeFile(path.join(previewDir,r.name+'.png'),new Uint8Array(await preview.arrayBuffer()));
}
const check=await workbook.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},maxChars:1200});
await fs.mkdir(path.dirname(output),{recursive:true});
const xlsx=await SpreadsheetFile.exportXlsx(workbook);await xlsx.save(output);
await fs.writeFile(path.join(previewDir,'workbook_check.json'),JSON.stringify({sheets:rendered.map(({name,rows,cols})=>({name,rows,cols})),inspection:check.ndjson},null,2));
console.log(JSON.stringify({exported:true,sheets:rendered.map(({name,rows,cols})=>({name,rows,cols})),formula_error_scan:check.ndjson}));
