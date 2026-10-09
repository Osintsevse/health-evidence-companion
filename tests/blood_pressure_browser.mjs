import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
// Optional Playwright test: no real health data or network access.
const assert=require('node:assert/strict');
const path=require('node:path');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.BP_PLAYWRIGHT_MODULE||'playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.BP_BROWSER_CHANNEL?{channel:process.env.BP_BROWSER_CHANNEL}:{})});
 let network=0;const errors=[];
 try{for(const locale of ['en','ru']){
  const page=await browser.newPage();page.on('pageerror',e=>errors.push(e.message));
  await page.route(/^https?:/,route=>{network++;return route.abort()});
  await page.goto(pathToFileURL(path.join(process.argv[2],locale,'index.html')).href+'#vitals');
  const guide=page.locator('.bp-guide');assert.equal(await guide.getAttribute('open'),null);
  assert.equal(await page.locator('[data-bp-filter]').inputValue(),'all');
  assert.equal(await page.locator('.bp-table tbody tr').count(),5);
  const rows=await page.locator('.bp-table tbody tr').allTextContents();
  assert.ok(rows[0].includes('108')&&rows[0].includes('62')&&rows[0].includes('79'));
  assert.ok(rows[1].includes('136')&&rows[1].includes('83'));assert.ok(!rows[1].includes('79'));
  const markers=page.locator('[data-bp-index="3"]');assert.equal(await markers.count(),3);
  const fills=await markers.locator('path').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('fill')));assert.equal(fills[0],fills[1]);assert.notEqual(fills[1],fills[2]);
  for(const component of ['sys','dia','pulse']){
   await page.locator(`[data-bp-index="3"][data-bp-component="${component}"]`).hover();
   const text=await page.locator('.bp-reading').textContent();assert.ok(text.includes('151')&&text.includes('54')&&text.includes('72'));
   assert.ok(text.includes(locale==='ru'?'\u041d\u0438\u0437\u043a\u043e\u0435':'Low'));assert.ok(text.includes(locale==='ru'?'\u0412\u044b\u0441\u043e\u043a\u0438\u0439 \u0434\u0438\u0430\u043f\u0430\u0437\u043e\u043d':'High range'));
  }
  await markers.first().focus();await page.keyboard.press('Enter');assert.ok((await page.locator('.bp-reading').textContent()).includes('151'));
  await page.locator('[data-bp-filter]').selectOption('abpm');assert.equal(await page.locator('.bp-table tbody tr').count(),1);
  assert.ok((await page.locator('.bp-table').textContent()).includes('10:15'));
  await page.locator('[data-bp-filter]').selectOption('all');await guide.locator('summary').click();
  assert.notEqual(await guide.getAttribute('open'),null);assert.ok((await guide.textContent()).includes(locale==='ru'?'\u041a\u043e\u0440\u043e\u0442\u043a\u043e\u0432\u0430':'Korotkoff'));
  await page.setViewportSize({width:390,height:844});
  assert.ok(await guide.evaluate(n=>n.getBoundingClientRect().bottom<=document.querySelector('.bp-panel').getBoundingClientRect().top));
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth),false);
  assert.ok((await page.locator('#main').textContent()).includes('999'));assert.ok((await page.locator('#main').textContent()).includes('MAP'));
  await page.close();
 }}finally{await browser.close()}
 assert.deepEqual(errors,[]);assert.equal(network,0);
 process.stdout.write(JSON.stringify({locales:['en','ru'],network_requests:network,page_errors:errors,readings_per_locale:5}));
})().catch(e=>{console.error(e);process.exitCode=1});
