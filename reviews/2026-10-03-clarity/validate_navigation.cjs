const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'../..'),out=process.env.QA_OUTPUT||'/private/tmp/agentic-talks-remaining-qa';
const {pathToFileURL}=require('node:url');const url=f=>pathToFileURL(path.join(root,f)).href;
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true,chromiumSandbox:true});const report={chooser:[],roundTrips:[],screenshots:[],errors:[]};
 try{
  const page=await browser.newPage();page.on('pageerror',e=>report.errors.push(e.message));
  for(const viewport of [{width:390,height:844},{width:1280,height:720},{width:1920,height:1080}]){
   await page.setViewportSize(viewport);await page.goto(url('index.html'));await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('a.card').count(),9);
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);assert.equal(overflow,false);
   const cards=await page.locator('a.card').evaluateAll(es=>es.map(e=>({href:e.getAttribute('href'),text:e.querySelector('.meta').textContent})));
   for(const c of cards){const f=c.href.replace('./','');assert.ok(fs.existsSync(path.join(root,f)));const n=(fs.readFileSync(path.join(root,f),'utf8').match(/<section\b/g)||[]).length;assert.ok(c.text.startsWith(n+' slides'));}
   await page.screenshot({path:path.join(out,'chooser-'+viewport.width+'.png'),fullPage:true});report.chooser.push({viewport,cards:9,overflow:false});
  }
  await page.setViewportSize({width:1920,height:1080});
  let metrics={};for(const mf of ['batch2-manifest.json','remaining-manifest.json'])Object.assign(metrics,JSON.parse(fs.readFileSync(path.join(__dirname,mf),'utf8')).metrics);
  for(const [name,m] of Object.entries(metrics)){
   await page.goto(url(name+'.html')+'#'+(m.after_slides-1));await page.waitForFunction(()=>document.querySelector('section[data-deck-active]'));
   await page.locator('section[data-deck-active] a[href="'+name+'-reference.html"]').click();
   await page.waitForURL('**/'+name+'-reference.html');await page.waitForFunction(()=>document.querySelector('section[data-deck-active]'));
   assert.equal(await page.locator('deck-stage > section').count(),m.reference_slides);
   await page.locator('section[data-deck-active] a[href="'+name+'.html"]').first().click();
   await page.waitForURL('**/'+name+'.html');await page.waitForFunction(()=>document.querySelector('section[data-deck-active]'));
   report.roundTrips.push({deck:name,mainToReference:true,referenceToMain:true});
  }
  for(const [file,n] of [['agentic-engineering',16],['subagents-prompt-caching',3],['working-smarter',2],['measuring-what-works',12]]){
   await page.goto(url(file+'.html')+'#'+n);await page.waitForFunction(()=>document.querySelector('section[data-deck-active]'));
   await page.addStyleTag({content:'.reveal{animation:none!important;transition:none!important}'});await page.evaluate(async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));});
   const shot=file+'-'+n+'-1920.png';await page.screenshot({path:path.join(out,shot)});report.screenshots.push(shot);
  }
  await page.goto(url('agentic-engineering.html')+'#19');await page.waitForFunction(()=>document.querySelector('section[data-deck-active] video')?.readyState>=2);
  await page.locator('section[data-deck-active] video').evaluate(v=>{v.pause();v.currentTime=Math.min(4,v.duration/2)});await page.waitForTimeout(150);
  await page.screenshot({path:path.join(out,'subagent-video-midpoint.png')});report.screenshots.push('subagent-video-midpoint.png');
 }finally{await browser.close();fs.writeFileSync(path.join(out,'navigation-results.json'),JSON.stringify(report,null,2)+'\n');}
 console.log(JSON.stringify(report,null,2));assert.equal(report.errors.length,0);
})().catch(e=>{console.error(e);process.exitCode=1});
