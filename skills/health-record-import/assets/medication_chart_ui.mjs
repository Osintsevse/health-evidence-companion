function renderMedicationTimeline(){
  const chartData=DATA.medication_chart||{events:DATA.medication_timeline||[],intervals:[],themes:[]},
    T={theme:'Topic',allTopics:'All topics',unassigned:'Other / no topic',medicine:'Medicine',allMedicines:'All medicines',
      records:'Record layer',use:'Use and effects',all:'Use and prescriptions',order:'Prescriptions',
      full:'Full history',four:'Last four years',one:'Last year',from:'From',to:'To',
      chart:'Medication time scale',period:'Reported course',window:'Imprecise date window',point:'Dated report',
      orderLegend:'Prescription',notTaken:'Not taken',ongoing:'Taking at last confirmation',
      note:'Solid bands show source-supported courses. Hatched edges/windows retain uncertain dates. Points show separate reports; gaps are not filled automatically. An arrow means a boundary is unknown.',
      topicNote:'Topics follow the context of care and sources; they are not an indication or drug-class classification.',
      help:'Select a band or point to see dose, evidence and original documents.',
      details:'Selected record',events:'All matching source records',undated:'Date unknown',
      noDates:'No dated events in the selected range.',noRecords:'No records match these filters.',
      unavailable:'Unknown',dose:'Dose',regimen:'Regimen',duration:'Reported duration',
      knownUntil:'Use confirmed on',start:'Start',end:'End',boundsUnknown:'Exact course boundaries are unknown',
      prescriptionsNote:'A prescription is not evidence of actual use.',
      durationHeading:'Durations without established boundaries',
      recorded:'Date of report',invalidRange:'Select an end date after the start date.',
      pan:'Scroll the time scale horizontally; medicine names stay visible.',previous:'Earlier',next:'Later',
      started:'Started',stopped:'Stopped',regimen_reported:'Reported use',benefit_reported:'Reported benefit',
      adverse_effect_reported:'Reported adverse effect',not_started:'Not taken',prescribed:'Prescribed',
      ...chartData.labels}, m=section('timeline'), tools=el('div',undefined,'toolbar med-controls');
  const select=(name,values)=>{const box=el('label',name,'med-control-label'),s=el('select');s.setAttribute('aria-label',name);for(const [v,t]of values){const o=el('option',t);o.value=v;s.append(o)}box.append(s);tools.append(box);return s};
  const topic=select(T.theme,[['',T.allTopics],...(chartData.themes||[]).map(t=>[t.id,t.label]),['__other',T.unassigned]]),
    medicine=select(T.medicine,[['',T.allMedicines]]),
    mode=select(T.records,[['use',T.use],['all',T.all],['order',T.order]]);
  topic.value=chartData.default_theme||'';
  const ranges=el('div',undefined,'toolbar med-ranges'), rangeButtons=[];
  let selectedRange='full';
  for(const [key,label]of [['full',T.full],['four',T.four],['one',T.one]]){
    const b=el('button',label,'control');b.type='button';b.dataset.medRange=key;
    b.onclick=()=>{selectedRange=key;setRange();draw()};ranges.append(b);rangeButtons.push(b);
  }
  function dateInput(label){const box=el('label',label,'med-control-label'),input=el('input');input.type='date';input.setAttribute('aria-label',label);box.append(input);ranges.append(box);input.onchange=()=>{selectedRange='custom';draw()};return input}
  const from=dateInput(T.from),to=dateInput(T.to),note=el('p',T.note,'notice'),topicNote=el('p',T.topicNote,'meta'),
    drawing=el('div'),selection=el('div',undefined,'panel med-selection'),history=el('details',undefined,'med-event-list');
  selection.dataset.medSelection='true';selection.setAttribute('aria-live','polite');selection.append(el('h3',T.details),el('p',T.help,'meta'));
  history.append(el('summary',T.events));const historyBody=el('div',undefined,'timeline');history.append(historyBody);
  const legend=el('div',undefined,'med-legend');
  for(const [kind,label]of [['period',T.period],['window',T.window],['point',T.point],['order',T.orderLegend],['not-started',T.notTaken],['ongoing',T.ongoing]]){
    const item=el('span'),swatch=el('i',undefined,'med-swatch '+kind);item.append(swatch,el('span',label));legend.append(item);
  }
  m.append(tools,ranges,topicNote,note,legend,drawing,selection,history);
  const DAY=86400000;
  function bounds(raw){
    if(raw&&/^\d{4}-\d{2}-\d{2}T/.test(raw)){const parts=raw.slice(0,10).split('-').map(Number),day=new Date(Date.UTC(parts[0],parts[1]-1,parts[2]));if(day.getUTCFullYear()!==parts[0]||day.getUTCMonth()!==parts[1]-1||day.getUTCDate()!==parts[2])return null;const t=Date.parse(raw);return Number.isFinite(t)?[t,t+1]:null}
    if(!raw||!/^\d{4}(-\d{2}(-\d{2})?)?$/.test(raw))return null;
    const parts=raw.split('-').map(Number),y=parts[0],mo=parts[1]||1,d=parts[2]||1,start=Date.UTC(y,mo-1,d);
    if(new Date(start).getUTCFullYear()!==y||new Date(start).getUTCMonth()!==mo-1||new Date(start).getUTCDate()!==d)return null;
    const end=parts.length===1?Date.UTC(y+1,0,1):parts.length===2?Date.UTC(y,mo,1):start+DAY;
    return[start,end];
  }
  const iso=value=>new Date(value).toISOString().slice(0,10), matchesTopic=r=>!topic.value||(topic.value==='__other'?!(r.themes||[]).length:(r.themes||[]).includes(topic.value));
  function eventSet(){return (chartData.events||[]).filter(r=>matchesTopic(r)&&(mode.value==='all'||mode.value===r.kind))}
  function groupCompare(a,b){const order=chartData.theme_group_order||[],ai=order.indexOf(a),bi=order.indexOf(b);return(ai<0?999:ai)-(bi<0?999:bi)||a.localeCompare(b,DATA.locale||'en')}
  function fillMedicines(){const previous=medicine.value;medicine.replaceChildren();for(const g of ['',...[...new Set(eventSet().map(r=>r.group))].sort(groupCompare)]){const o=el('option',g||T.allMedicines);o.value=g;medicine.append(o)}if([...medicine.options].some(o=>o.value===previous))medicine.value=previous}
  function setRange(){
    const events=eventSet().filter(r=>!medicine.value||medicine.value===r.group),values=events.map(r=>bounds(r.date)).filter(Boolean),
      asof=bounds(chartData.as_of||DATA.as_of||DATA.generated_at.slice(0,10));
    const latest=Math.max(...values.map(b=>b[1]),asof?asof[1]:0),earliest=values.length?Math.min(...values.map(b=>b[0])):latest-365*DAY;
    let first=Date.UTC(new Date(earliest).getUTCFullYear(),0,1);
    if(selectedRange==='four'||selectedRange==='one'){const end=new Date(latest-DAY);first=Date.UTC(end.getUTCFullYear()-(selectedRange==='four'?4:1),end.getUTCMonth(),end.getUTCDate())}
    from.value=iso(first);to.value=iso(latest-DAY);
  }
  topic.onchange=()=>{fillMedicines();if(selectedRange!=='custom')setRange();draw()};
  mode.onchange=()=>{fillMedicines();if(selectedRange!=='custom')setRange();draw()};
  medicine.onchange=()=>{if(selectedRange==='full')setRange();draw()};
  function describe(item,kind){
    selection.replaceChildren(el('h3',item.group),el('p',kind==='annotation'?item.label:((item.date||T.undated)+' · '+(item.kind==='order'?T.prescribed:T[item.event_type]||item.event_type)),'med-selected-heading'));
    if(kind==='annotation'){
      if(item.kind==='period')selection.append(el('p',T.start+': '+item.start+' · '+T.end+': '+item.end));
      if(item.duration_text)selection.append(el('p',T.duration+': '+item.duration_text));
      if(item.kind==='ongoing')selection.append(el('p',T.knownUntil+': '+item.confirmed_until+' · '+T.start+': '+(item.start||T.unavailable)));
      if(item.note)selection.append(el('p',item.note,'notice'));
      for(const e of item.evidence||[])selection.append(el('p',(e.date||T.undated)+' · '+(e.dose||e.regimen||e.product),'meta'),source(e.source));
    }else{
      if(item.dose)selection.append(el('p',T.dose+': '+item.dose));if(item.regimen)selection.append(el('p',T.regimen+': '+item.regimen));
      if(item.benefit)selection.append(el('p',item.benefit));if(item.adverse_effect)selection.append(el('p',item.adverse_effect));
      if(item.kind==='order')selection.append(el('p',T.prescriptionsNote,'notice'));
      if(item.source.uncertainties)selection.append(el('p',item.source.uncertainties,'meta'));
      selection.append(badge(item.source),source(item.source));
    }
  }
  function draw(){
    drawing.replaceChildren();historyBody.replaceChildren();for(const b of rangeButtons)b.classList.toggle('selected',b.dataset.medRange===selectedRange);
    const start=bounds(from.value)?.[0],end=bounds(to.value)?.[1];if(start===undefined||end===undefined||end<=start){drawing.append(el('p',T.invalidRange,'notice'));return}
    const events=eventSet().filter(r=>!medicine.value||r.group===medicine.value),annotations=(chartData.intervals||[]).filter(r=>mode.value!=='order'&&matchesTopic(r)&&(!medicine.value||r.group===medicine.value)),
      visible=events.filter(r=>{const b=bounds(r.date);return !b||b[0]<end&&b[1]>start}),
      insideAnnotation=r=>{const a=bounds(r.start||r.anchor_date||r.confirmed_until),b=bounds(r.end||r.anchor_date||r.confirmed_until);return !a||a[0]<end&&b[1]>start},periods=annotations.filter(insideAnnotation);
    const groups=[...new Set([...visible.map(r=>r.group),...periods.map(r=>r.group)])].sort(groupCompare),paletteGroups=[...new Set((chartData.events||[]).map(r=>r.group))].sort(groupCompare);
    if(!groups.length){drawing.append(el('p',T.noRecords,'empty'));return}
    const span=end-start,years=span/(365.25*DAY),wrap=el('div',undefined,'med-chart-viewport'),chart=el('div',undefined,'med-chart');
    let trackWidth=Math.max(820,Math.min(1800,years*120));
    wrap.dataset.medicationChart='true';wrap.setAttribute('aria-label',T.chart);wrap.tabIndex=0;wrap.append(chart);drawing.append(wrap);
    trackWidth=Math.max(trackWidth,wrap.clientWidth-205);chart.style.width=(205+trackWidth)+'px';
    const padding=9/trackWidth*100,position=value=>Math.max(padding,Math.min(100-padding,(value-start)/span*(100-2*padding)+padding)),ticks=[];
    const firstDate=new Date(start),step=years>3?12:years>1?3:1;
    for(let y=firstDate.getUTCFullYear(),month=years>3?0:firstDate.getUTCMonth();Date.UTC(y,month,1)<=end;month+=step){
      if(month>=12){y+=Math.floor(month/12);month%=12}const t=Date.UTC(y,month,1);if(t<start||t>=end)continue;
      const label=step===12?String(y):new Intl.DateTimeFormat(DATA.locale||'en',{month:'short',year:'2-digit',timeZone:'UTC'}).format(t);ticks.push({t,label});
    }
    const axisRow=el('div',undefined,'med-chart-row med-axis-row'),axis=el('div',undefined,'med-track med-axis');axisRow.append(el('div',T.medicine,'med-row-label'),axis);chart.append(axisRow);
    for(const tick of ticks){const node=el('span',tick.label,'med-axis-tick');node.style.left=position(tick.t)+'%';axis.append(node)}
    const colors=['#267e83','#466ec6','#9268ae','#b17635','#49875c','#bc6666','#547d9c','#858032'];
    for(const [index,group]of groups.entries()){
      const row=el('div',undefined,'med-chart-row'),label=el('div',undefined,'med-row-label'),track=el('div',undefined,'med-track');
      row.dataset.medicationGroup=group;row.style.setProperty('--med-color',colors[paletteGroups.indexOf(group)%colors.length]);label.append(el('strong',group));
      const rs=visible.filter(r=>r.group===group),last=rs.filter(r=>r.kind==='use'&&r.dose).at(-1);if(last)label.append(el('span',last.dose+' · '+(last.date||T.undated),'meta'));row.append(label,track);chart.append(row);
      for(const tick of ticks){const grid=el('i',undefined,'med-grid-line');grid.style.left=position(tick.t)+'%';track.append(grid)}
      const groupPeriods=periods.filter(r=>r.group===group);
      for(const item of groupPeriods){
        if(item.kind==='duration_only')continue;
        const unknownStart=!item.start,a=bounds(item.start||item.confirmed_until),b=bounds(item.end||item.confirmed_until);
        if(!a||!b)continue;
        let left=position(a[0]),right=position(b[1]);
        const pill=el('button',item.label,'med-period '+(item.kind==='ongoing'?'ongoing':'')+(item.start?.length!==10||item.end?.length!==10?' approximate':''));
        if(unknownStart){left=Math.max(0,left-48/trackWidth*100);pill.dataset.unknownStart='true'}
        pill.type='button';pill.dataset.medPeriod=item.id;pill.style.left=left+'%';pill.style.width=Math.max(18/trackWidth*100,right-left)+'%';pill.title=item.label+' · '+(item.note||'');pill.setAttribute('aria-label',group+' · '+pill.title);pill.onclick=()=>describe(item,'annotation');track.append(pill);
      }
      const counts=new Map();
      for(const r of rs){
        const date=bounds(r.date);if(!date)continue;
        const key=r.date,offset=counts.get(key)||0;counts.set(key,offset+1);
        const partial=r.date.length===4||r.date.length===7,type=r.kind==='order'?'order':r.event_type==='not_started'?'not-started':r.event_type?.includes('effect')||r.event_type==='benefit_reported'?'effect':'point',
          button=el('button',type==='not-started'?'×':type==='order'?'◇':type==='effect'?'·':'','med-event '+type+(partial?' window':''));
        button.type='button';button.dataset.medChartEntry=r.entry_id;button.dataset.medChartKind=r.kind;
        button.title=[r.date,r.product,T[r.event_type]||r.event_type,r.dose||r.regimen].filter(Boolean).join(' · ');button.setAttribute('aria-label',button.title);
        button.style.top=(partial?63+offset*20:56+offset*20)+'px';
        if(partial){button.style.left=position(date[0])+'%';button.style.width=Math.max(9/trackWidth*100,position(date[1])-position(date[0]))+'%';button.textContent=type==='not-started'?'× '+T.notTaken+' · '+r.date:type==='order'?'◇ '+r.date:r.date.length===4?r.regimen||r.date:''}
        else button.style.left=position((date[0]+date[1])/2)+'%';
        button.onclick=()=>describe(r,'event');track.append(button);
      }
      const max=Math.max(0,...counts.values());track.style.minHeight=Math.max(98,80+max*20)+'px';
      if(rs.some(r=>!r.date)){const undated=el('button',T.undated,'control med-undated');undated.type='button';undated.onclick=()=>{history.open=true;history.scrollIntoView({block:'nearest'})};label.append(undated)}
    }
    if(wrap.scrollWidth>wrap.clientWidth+2){const nav=el('div',undefined,'toolbar'),prior=el('button','← '+T.previous,'control'),next=el('button',T.next+' →','control');prior.type=next.type='button';prior.onclick=()=>wrap.scrollBy({left:-wrap.clientWidth*.8,behavior:'smooth'});next.onclick=()=>wrap.scrollBy({left:wrap.clientWidth*.8,behavior:'smooth'});nav.append(prior,next,el('span',T.pan,'meta'));drawing.insertBefore(nav,wrap);wrap.scrollLeft=wrap.scrollWidth-wrap.clientWidth;}
    const durationOnly=periods.filter(r=>r.kind==='duration_only');
    if(durationOnly.length){const panel=el('div',undefined,'panel med-duration-panel');panel.append(el('h3',T.durationHeading));for(const r of durationOnly){const button=el('button',r.group+' · '+r.duration_text+' · '+T.boundsUnknown,'control');button.type='button';button.onclick=()=>describe(r,'annotation');panel.append(button)}drawing.append(panel)}
    for(const r of visible){const a=el('article');a.dataset.medicationEntry=r.entry_id;a.dataset.medicationKind=r.kind;a.append(el('h3',(r.date||T.undated)+' · '+r.group),el('p',r.kind==='order'?T.prescribed:T[r.event_type]||r.event_type,'meta'));if(r.dose)a.append(el('p',T.dose+': '+r.dose));if(r.regimen)a.append(el('p',r.regimen));if(r.benefit)a.append(el('p',r.benefit));if(r.adverse_effect)a.append(el('p',r.adverse_effect));if(r.source.uncertainties)a.append(el('p',r.source.uncertainties,'meta'));a.append(badge(r.source),source(r.source));historyBody.append(a)}
    history.querySelector('summary').textContent=T.events+' ('+visible.length+')';
    selection.replaceChildren(el('h3',T.details),el('p',T.help,'meta'));
  }
  fillMedicines();setRange();draw();
}
