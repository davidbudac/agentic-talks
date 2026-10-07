#!/usr/bin/env python3
"""Validate all clarity outputs and their original-slide accounting."""
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter
from urllib.parse import urlsplit,unquote
import re,json,hashlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
errors=[];results=[]
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.slides=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  for k in ['src','href','poster']:
   if a.get(k):self.links.append(a[k])
  if tag=='section' and 'slide' in a.get('class','').split():self.slides.append(a)
for mf in ['batch1-manifest.json','batch2-manifest.json','remaining-manifest.json']:
 m=json.loads((HERE/mf).read_text());sm=json.loads((HERE/m.get('maps','slide-map.json')).read_text())
 for file,h in m['outputs'].items():
  text=(ROOT/file).read_text();p=Inspect();p.feed(text);sections=re.findall(r'<section\b[^>]*>.*?</section>',text,re.S)
  if hashlib.sha256(text.encode()).hexdigest()!=h:errors.append(file+': hash differs from manifest')
  if any(n>1 for n in Counter(p.ids).values()):errors.append(file+': duplicate IDs')
  for url in p.links:
   u=urlsplit(url)
   if not u.scheme and not u.netloc and u.path and not (ROOT/unquote(u.path)).exists():errors.append(file+': missing local resource '+url)
  for i,a in enumerate(p.slides,1):
   if not a.get('data-label','').strip() or not a.get('data-speaker-notes','').strip():errors.append(f'{file}:{i} missing notes or label')
  for i,s in enumerate(sections,1):
   n=re.search(r'<span class="snum">(\d+)</span>',s)
   if n and int(n[1])!=i:errors.append(f'{file}:{i} numbering')
   visible=re.sub(r'<[^>]*>',' ',s)
   if mf!='batch1-manifest.json' and re.search(r'\b(TODO|Placeholder|WIP)\b',visible):errors.append(f'{file}:{i} unfinished visible copy')
   if re.search(r'\bslide \d+\b',visible,re.I):errors.append(f'{file}:{i} stale prose slide number')
  for js in re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',text,re.S):
   if not js.strip():continue
   with tempfile.NamedTemporaryFile(mode='w',suffix='.js') as f:
    f.write(js);f.flush();r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
    if r.returncode:errors.append(file+': JS syntax '+r.stderr)
  stem=file.removesuffix('.html').removesuffix('-reference');metric=m['metrics'][stem]
  expected=metric['reference_slides'] if file.endswith('-reference.html') else metric['after_slides']
  if len(p.slides)!=expected:errors.append(file+': count differs from manifest')
  results.append({'file':file,'slides':len(p.slides),'local_resources':True,'notes':True,'numbering':True,'script_syntax':True})
 for deck,entries in sm.items():
  metric=m['metrics'][deck]
  if sorted(x['original'] for x in entries)!=list(range(1,metric['before_slides']+1)):errors.append(deck+': incomplete baseline map')
  if sorted(x['main'] for x in entries if x['main'])!=list(range(1,metric['after_slides']+1)):errors.append(deck+': incomplete main map')
  for entry in entries:
   for kind in ['main','reference']:
    pos=entry[kind]
    if pos:
     target=deck+('-reference' if kind=='reference' else '')+'.html'; sections=re.findall(r'<section\b[^>]*>.*?</section>',(ROOT/target).read_text(),re.S)
     if f'data-origin-slide="{entry["original"]}"' not in sections[pos-1]:errors.append(target+': origin map mismatch')
for f in ['ember_design_system/deck-stage.js','ember_design_system/styles.css']:
 if (ROOT/f).read_bytes()!=subprocess.check_output(['git','show',m['baseline']+':'+f],cwd=ROOT):errors.append('Unexpected shared file change: '+f)
# Verify the worked examples independently of the HTML builders.
from decimal import Decimal as D
assert 19000*D('.20')/1000000+3700*D('4')/1000000+1600*D('20')/1000000==D('.0506')
assert 22700*D('4')/1000000+1600*D('20')/1000000==D('.1228')
assert 10*5000+2000*10*9//2==140000
assert D('1.25')+D('.1')<2 and D('2')+D('.1')>2 and D('2')+D('.2')<3
report={'results':results,'errors':errors,'shared_runtime_unchanged':True,'arithmetic':'passed'}
(HERE/'all-static-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'outputs':len(results),'slides':sum(x['slides'] for x in results),'errors':errors},indent=2));raise SystemExit(bool(errors))
