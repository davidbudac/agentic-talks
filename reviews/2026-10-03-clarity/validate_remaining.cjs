/* Run with PLAYWRIGHT_MODULE pointing to an installed Playwright package.
   Uses an isolated headless browser; never opens the user's browser profile. */
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '../..');
const out = process.env.QA_OUTPUT || '/private/tmp/agentic-talks-remaining-qa';
fs.mkdirSync(out, {recursive: true});
const decks = {};
for(const name of ['batch2-manifest.json','remaining-manifest.json']){const m=JSON.parse(fs.readFileSync(path.join(__dirname,name),'utf8'));for(const [deck,metric] of Object.entries(m.metrics)){decks[deck+'.html']=metric.after_slides;decks[deck+'-reference.html']=metric.reference_slides;}}
(async()=>{
  const browser = await chromium.launch({channel:'chrome',headless:true,chromiumSandbox:true});
  const report = {date:'2026-10-03',viewports:[],errors:[],screenshots:[],checks:[]};
  try {
    for (const viewport of [{width:1280,height:720},{width:1920,height:1080}]) {
      const context = await browser.newContext({viewport,reducedMotion:'reduce'});
      for (const [file,count] of Object.entries(decks)) {
        const page=await context.newPage();
        page.on('console',msg=>{if(msg.type()==='error' && !msg.text().includes('fonts.googleapis') && !msg.text().includes('ERR_INTERNET_DISCONNECTED'))report.errors.push({file,viewport,console:msg.text()});});
        page.on('pageerror',e=>report.errors.push({file,viewport,error:e.message}));
        await page.goto(pathToFileURL(path.join(root,file)).href);
        await page.waitForFunction(()=>customElements.get('deck-stage') && document.querySelector('deck-stage > section[data-deck-active]'));
        await page.addStyleTag({content:'.reveal{animation:none!important;transition:none!important}'});
        await page.evaluate(()=>document.fonts.ready);
        assert.equal(await page.locator('deck-stage > section').count(),count);
        const ids=await page.evaluate(()=>Array.from(document.querySelectorAll('[id]')).map(n=>n.id));
        assert.equal(new Set(ids).size,ids.length,`${file}: duplicate ids`);
        const missing=await page.evaluate(()=>Array.from(document.querySelectorAll('deck-stage > section')).filter(n=>!n.dataset.speakerNotes?.trim()).length);
        assert.equal(missing,0,`${file}: missing notes`);
        let bounds=[];
        for(let i=0;i<count;i++){
          await page.evaluate(i=>document.querySelector('deck-stage').goTo(i),i);
          await page.waitForFunction(i=>document.querySelectorAll('deck-stage > section')[i].hasAttribute('data-deck-active'),i);
          await page.evaluate(async()=>{await document.fonts.ready;await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));});
          if(await page.locator('deck-stage > section[data-deck-active] video').count()){
            await page.waitForFunction(()=>Array.from(document.querySelectorAll('deck-stage > section[data-deck-active] video')).every(v=>v.readyState>=2),null,{timeout:10000});
          }
          const bad=await page.evaluate(()=>{
            const slide=document.querySelector('deck-stage > section[data-deck-active]');
            const s=slide.getBoundingClientRect();const bad=[];
            for(const el of slide.querySelectorAll('h1,h2,h3,p,li,.code,.tile,table,.reference-banner,.slide-content,.diagram,svg,td,th')){
              const r=el.getBoundingClientRect();
              if(!r.width || !r.height)continue;
              if(r.left<s.left-2 || r.right>s.right+2 || r.top<s.top-2 || r.bottom>s.bottom+2)bad.push({type:'outside-slide',text:el.textContent.slice(0,100),rect:{x:r.x,y:r.y,w:r.width,h:r.height},slide:{x:s.x,y:s.y,w:s.width,h:s.height}});
              const style=getComputedStyle(el);
              if((['hidden','clip'].includes(style.overflowY) && el.scrollHeight>el.clientHeight+3) || (['hidden','clip'].includes(style.overflowX) && el.scrollWidth>el.clientWidth+3))bad.push({type:'element-overflow',text:el.textContent.slice(0,100)});
            }
            const walker=document.createTreeWalker(slide,NodeFilter.SHOW_TEXT);
            let node;while(node=walker.nextNode()){
              if(!node.textContent.trim() || node.parentElement.closest('svg,script,style'))continue;
              const range=document.createRange();range.selectNodeContents(node);
              for(const r of range.getClientRects())if(r.width && r.height && (r.left<s.left-2 || r.right>s.right+2 || r.top<s.top-2 || r.bottom>s.bottom+2))bad.push({type:'text-outside-slide',text:node.textContent.slice(0,100)});
            }
            return bad;
          });
          bounds.push(...bad.map(x=>({slide:i+1,...x})));
          if(viewport.width===1280 && ((!file.includes('reference') && [0,3,6,9,14,count-2].includes(i)) || (file.includes('reference') && [0,2,count-3].includes(i)))){
            const shot=`${file.replace('.html','')}-${String(i+1).padStart(2,'0')}-${viewport.width}.png`;
            await page.screenshot({path:path.join(out,shot)});report.screenshots.push(shot);
          }
        }
        report.viewports.push({file,viewport,slides:count,bounds});
        // Keyboard navigation and deep-link semantics.
        await page.keyboard.press('Home');
        await page.waitForFunction(()=>document.querySelector('deck-stage > section').hasAttribute('data-deck-active'));
        await page.keyboard.press('ArrowRight');
        await page.waitForFunction(()=>document.querySelectorAll('deck-stage > section')[1].hasAttribute('data-deck-active'));
        await page.keyboard.press('End');
        await page.waitForFunction(n=>document.querySelectorAll('deck-stage > section')[n-1].hasAttribute('data-deck-active'),count);
        await page.goto('about:blank');
        await page.goto(pathToFileURL(path.join(root,file)).href+'#3');
        await page.waitForFunction(()=>document.querySelectorAll('deck-stage > section')[2].hasAttribute('data-deck-active'));
        await page.keyboard.press('n');
        const notePanel=await page.evaluate(()=>Array.from(document.querySelectorAll('.open')).filter(n=>n.textContent.includes(document.querySelector('deck-stage > section[data-deck-active]').dataset.speakerNotes)).length);
        assert.ok(notePanel>0,`${file}: notes do not show current slide`);
        await page.keyboard.press('n');
        await page.keyboard.press('f');
        await page.waitForFunction(()=>document.fullscreenElement && document.querySelector('deck-stage').hasAttribute('no-rail'));
        await page.keyboard.press('f');
        await page.waitForFunction(()=>!document.fullscreenElement);
        const popupPromise=page.waitForEvent('popup');
        await page.keyboard.press('p');
        const popup=await popupPromise;
        await popup.waitForSelector('.pw-notes');
        const currentNotes=await page.locator('deck-stage > section[data-deck-active]').getAttribute('data-speaker-notes');
        assert.equal(await popup.locator('.pw-notes').textContent(),currentNotes);
        await popup.close();
        report.checks.push({file,viewport,keyboard:true,deepLink:true,notes:true,presenter:true,fullscreen:true,media:true,ids:true});
        await page.close();
      }
      await context.close();
    }
  } finally {await browser.close();fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify(report,null,2)+'\n');}
  const bounds=report.viewports.flatMap(x=>x.bounds.map(b=>({file:x.file,viewport:x.viewport,...b})));
  console.log(JSON.stringify({slidesChecked:report.viewports.reduce((n,x)=>n+x.slides,0),errors:report.errors,bounds,screenshots:report.screenshots.length,output:out},null,2));
  if(report.errors.length || bounds.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
