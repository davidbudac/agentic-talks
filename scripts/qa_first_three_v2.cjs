/* Browser QA for the three v2 decks. Requires Playwright and installed Chrome.
 * PLAYWRIGHT_MODULE=/path/to/playwright node scripts/qa_first_three_v2.cjs
 * Starts a temporary localhost server. Screenshots go outside the repo.
 */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const assert = require('node:assert/strict');
const output = process.env.QA_OUTPUT || '/private/tmp/agentic-talks-v2-qa';
fs.mkdirSync(output,{recursive:true});
const decks = ['ai-toolbox-v2.html','agentic-ai-v2.html','agentic-engineering-v2.html'];
(async()=>{
 const root=process.cwd();
 const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.woff2':'font/woff2','.mp4':'video/mp4','.csv':'text/csv','.md':'text/plain'};
 const server=http.createServer((req,res)=>{
  const target=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));
  if(!target.startsWith(root+path.sep)||!fs.existsSync(target)||!fs.statSync(target).isFile()){res.writeHead(404);res.end();return;}
  const size=fs.statSync(target).size;const headers={'Content-Type':types[path.extname(target)]||'application/octet-stream','Accept-Ranges':'bytes'};
  const range=(req.headers.range||'').match(/^bytes=(\d+)-(\d*)$/);
  if(range){
   const start=Number(range[1]),end=range[2]?Math.min(Number(range[2]),size-1):size-1;
   if(start>=size||start>end){res.writeHead(416);res.end();return;}
   res.writeHead(206,{...headers,'Content-Range':`bytes ${start}-${end}/${size}`,'Content-Length':end-start+1});fs.createReadStream(target,{start,end}).pipe(res);
  }else{res.writeHead(200,{...headers,'Content-Length':size});fs.createReadStream(target).pipe(res);}
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base='http://127.0.0.1:'+server.address().port+'/';
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const results=[];
 for(const width of [1280,1920]){
  const context=await browser.newContext({viewport:{width,height:width*9/16},reducedMotion:'reduce'});
  for(const file of decks){
   const page=await context.newPage();const errors=[];const cancelledMedia=[];
   page.on('pageerror',e=>errors.push(e.message));
   page.on('requestfailed',r=>{const reason=r.failure().errorText;if(reason==='net::ERR_ABORTED'&&r.resourceType()==='media'){cancelledMedia.push(r.url());return;}errors.push(r.url()+': '+reason)});
   page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
   await page.goto(base+file);
   await page.evaluate(async()=>{await customElements.whenDefined('deck-stage');await document.fonts.ready});
   await page.waitForSelector('deck-stage:not([data-fonts-pending])');
   const count=await page.locator('deck-stage > section').count();
   const issues=[];const words=[];
   for(let i=0;i<count;i++){
    await page.evaluate(i=>document.querySelector('deck-stage').goTo(i),i);
    await page.waitForFunction(i=>document.querySelector('deck-stage > section[data-deck-active]')?.id===`slide-${i+1}`,i);
    await page.evaluate(async()=>{for(const v of document.querySelectorAll('section[data-deck-active] video')){
     v.preload='auto';v.pause();
     if(v.readyState<2)await new Promise((resolve,reject)=>{v.addEventListener('loadeddata',resolve,{once:true});v.addEventListener('error',()=>reject(Error('Video decode failed')),{once:true});setTimeout(()=>reject(Error('Video load timed out')),10000)});
     const end=Math.max(0,v.duration-0.7);
     await new Promise((resolve,reject)=>{v.addEventListener('seeked',resolve,{once:true});v.currentTime=end;setTimeout(()=>reject(Error('Video seek timed out')),10000)});
    }});
    const toggle=page.locator('section[data-deck-active] [data-video-toggle]');
    if(await toggle.count()){
     await toggle.click();
     await page.waitForFunction(()=>!document.querySelector('section[data-deck-active] video').paused);
     await page.waitForFunction(()=>document.querySelector('section[data-deck-active] [data-video-toggle]').getAttribute('aria-pressed')==='true');
     await toggle.click();
     await page.waitForFunction(()=>document.querySelector('section[data-deck-active] [data-video-toggle]').getAttribute('aria-pressed')==='false');
     assert(await page.evaluate(()=>document.querySelector('section[data-deck-active] video').paused));
     // Park the pointer so hover-revealed presenter controls do not appear in later screenshots.
     await page.mouse.move(0,0);await page.waitForTimeout(2000);
    }
    const state=await page.evaluate(()=>{
     const s=document.querySelector('deck-stage > section[data-deck-active]');
     const rect=s.getBoundingClientRect();const issues=[];
     for(const el of s.querySelectorAll('*')){
      if(el.matches('source,script,style'))continue;
      const r=el.getBoundingClientRect();if(!r.width||!r.height)continue;
      if(r.left<rect.left-2||r.right>rect.right+2||r.top<rect.top-2||r.bottom>rect.bottom+2)issues.push(`outside slide: ${el.tagName}.${el.className}`);
      if(/hidden|clip|auto|scroll/.test(getComputedStyle(el).overflowY) && el.clientHeight && el.scrollHeight>el.clientHeight+3 && !el.matches('video,svg'))issues.push(`vertical overflow: ${el.tagName}.${el.className}`);
      if(/hidden|clip|auto|scroll/.test(getComputedStyle(el).overflowX) && el.clientWidth && el.scrollWidth>el.clientWidth+3 && !el.matches('video,svg'))issues.push(`horizontal overflow: ${el.tagName}.${el.className}`);
     }
     // Compare text line boxes with clipping ancestors, including flex-shrunk content.
     const walker=document.createTreeWalker(s,NodeFilter.SHOW_TEXT);let n;
     while(n=walker.nextNode()){
      if(!n.textContent.trim()||n.parentElement.closest('script,style'))continue;
      const range=document.createRange();range.selectNodeContents(n);
      for(const r of range.getClientRects()){
       let a=n.parentElement;
       while(a&&a!==s.parentElement){
        const cs=getComputedStyle(a);if(/hidden|clip/.test(cs.overflow+cs.overflowX+cs.overflowY)){
         const box=a.getBoundingClientRect();
         if(r.left<box.left-2||r.right>box.right+2||r.top<box.top-2||r.bottom>box.bottom+2){issues.push('clipped text: '+n.textContent.trim().slice(0,70));break}
        }a=a.parentElement;
       }
      }
     }
     return {title:s.dataset.label,words:s.innerText.trim().split(/\s+/).length,issues:[...new Set(issues)]};
    });
    if(state.issues.length)issues.push({slide:i+1,...state});
    words.push(state.words);
    await page.screenshot({path:path.join(output,`${file.replace('.html','')}-${width}-${String(i+1).padStart(2,'0')}.png`)});
   }
   // Keyboard, hash, notes and presenter must work with the actual static deck.
   await page.keyboard.press('Home');
   assert.equal(await page.locator('section[data-deck-active]').getAttribute('id'),'slide-1');
   await page.keyboard.press('ArrowRight');
   assert.equal(await page.locator('section[data-deck-active]').getAttribute('id'),'slide-2');
   await page.keyboard.press('Space');
   assert.equal(await page.locator('section[data-deck-active]').getAttribute('id'),'slide-3');
   await page.goto('about:blank');
   await page.goto(base+file+'#8');
   await page.waitForSelector('deck-stage:not([data-fonts-pending])');
   await page.keyboard.press('n');
   assert.match(await page.locator('.pui-nhead').innerText(),/8 \/ /);
   await page.keyboard.press('n');
   const popupPromise=page.waitForEvent('popup');await page.keyboard.press('p');const popup=await popupPromise;
   await popup.waitForSelector('.pw');
   assert.match(await popup.locator('.cnt').innerText(),/^8 \/ /);
   await popup.locator('[data-nav="1"]').click();
   assert.equal(await page.locator('section[data-deck-active]').getAttribute('id'),'slide-9');
   await popup.close();
   const reduced=await page.evaluate(()=>[...document.querySelectorAll('video')].every(v=>v.paused));
   assert(reduced,'Reduced motion must not autoplay video');
   results.push({file,width,count,words:{min:Math.min(...words),max:Math.max(...words),average:Math.round(words.reduce((a,b)=>a+b,0)/count)},issues,errors,cancelledMedia,navigation:'pass',notes:'pass',presenter:'pass',reducedMotion:'pass'});
   console.log(file,width,'slides:',count,'issues:',issues.length,'errors:',errors.length);
   await page.close();
  }
  await context.close();
 }
 // Test normal-motion media activation and pausing off-slide.
 const page=await browser.newPage({viewport:{width:1280,height:720},reducedMotion:'no-preference'});
 await page.goto(base+'agentic-ai-v2.html#7');
 await page.waitForFunction(()=>{const v=document.querySelector('section[data-deck-active] video');return v&&!v.paused&&v.currentTime>0});
 await page.keyboard.press('ArrowRight');
 assert(await page.evaluate(()=>[...document.querySelectorAll('video')].every(v=>v.paused)));
 await page.close();
 // Check the chooser and report at desktop and narrow viewport sizes.
 const support=[];
 for(const file of ['first-three-v2.html','examples/v2/review-report.html']){
  for(const width of [1280,390]){
   const p=await browser.newPage({viewport:{width,height:width===390?844:720}});
   await p.goto(base+file);await p.evaluate(()=>document.fonts.ready);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),file+' horizontal overflow');
   await p.screenshot({path:path.join(output,file.replaceAll('/','-').replace('.html','')+'-'+width+'.png'),fullPage:true});
   support.push({file,width,overflow:'pass'});await p.close();
  }
 }
 // The deck shells and fonts should also load directly from disk without a server.
 const offline=[];
 for(const file of decks){
  const p=await browser.newPage({viewport:{width:1280,height:720},reducedMotion:'reduce'});
  await p.context().setOffline(true);
  await p.goto('file://'+path.join(process.cwd(),file)+'#3');
  await p.waitForSelector('deck-stage:not([data-fonts-pending])');
  assert.equal(await p.locator('section[data-deck-active]').getAttribute('id'),'slide-3');
  assert(await p.evaluate(()=>document.fonts.check('700 48px "Space Grotesk"')));
  offline.push({file,localLoad:'pass',fonts:'pass'});await p.close();
 }
 await browser.close();
 await new Promise(resolve=>server.close(resolve));
 fs.writeFileSync(path.join(output,'results.json'),JSON.stringify({results,support,offline,media:'active playback and off-slide pause pass'},null,2)+'\n');
 if(results.some(r=>r.issues.length||r.errors.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
