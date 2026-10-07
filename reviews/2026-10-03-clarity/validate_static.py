#!/usr/bin/env python3
"""Check the edited HTML, its local resources, and the batch's slide accounting."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
import hashlib, json, re, subprocess, tempfile
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
if (HERE/'remaining-manifest.json').exists():
 raise SystemExit(subprocess.call(['python3',str(HERE/'validate_all.py')]))
manifest=json.loads((HERE/'batch1-manifest.json').read_text())
slide_map=json.loads((HERE/'slide-map.json').read_text())
errors=[];results=[]
class Inspect(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.links=[];self.slides=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.append(a['id'])
  for k in ('src','href','poster'):
   if a.get(k):self.links.append(a[k])
  if tag=='section' and 'slide' in a.get('class','').split():self.slides.append(a)
for file,expected_hash in manifest['outputs'].items():
 source=(ROOT/file).read_text();p=Inspect();p.feed(source)
 if hashlib.sha256(source.encode()).hexdigest()!=expected_hash:errors.append(file+': content differs from manifest')
 duplicates=[x for x,n in Counter(p.ids).items() if n>1]
 if duplicates:errors.append(file+': duplicate IDs '+str(duplicates))
 for href in p.links:
  u=urlsplit(href)
  if u.scheme or u.netloc or not u.path:continue
  if not (ROOT/unquote(u.path)).exists():errors.append(file+': missing resource '+href)
 for n,a in enumerate(p.slides,1):
  if not a.get('data-label') or not a.get('data-speaker-notes'):errors.append(f'{file} slide {n}: missing label/notes')
 sections=re.findall(r'<section\b[^>]*>.*?</section>',source,re.S)
 for n,s in enumerate(sections,1):
  num=re.search(r'<span class="snum">(\d+)</span>',s)
  if num and int(num[1])!=n:errors.append(f'{file} slide {n}: wrong printed number')
  if re.search(r'\bslide \d+\b', re.sub(r'<[^>]+>',' ',s),re.I):errors.append(f'{file} slide {n}: stale numeric prose reference')
 for script in re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',source,re.S):
  if not script.strip():continue
  with tempfile.NamedTemporaryFile(suffix='.js',mode='w') as f:
   f.write(script);f.flush();r=subprocess.run(['node','--check',f.name],capture_output=True,text=True)
   if r.returncode:errors.append(file+': script syntax: '+r.stderr)
 results.append({'file':file,'slides':len(p.slides),'links_inspected':len(p.links),'notes':True,'numbering':True,'script_syntax':True})
for deck,slides in slide_map.items():
 expected=manifest['metrics'][deck]['before_slides']
 if sorted(s['original'] for s in slides)!=list(range(1,expected+1)):errors.append(deck+': incomplete original slide map')
 if sorted(s['main'] for s in slides if s['main'])!=list(range(1,manifest['metrics'][deck]['after_slides']+1)):errors.append(deck+': incomplete main slide map')
# Preserve all seven untouched decks and the shared runtime/style files.
unchanged=['agentic-engineering.html','subagents-prompt-caching.html','cost-and-context.html','orchestrating-agents.html','measuring-what-works.html','best-practices.html','working-smarter.html','ember_design_system/deck-stage.js','ember_design_system/styles.css']
for file in unchanged:
 before=subprocess.check_output(['git','show',manifest['baseline']+':'+file],cwd=ROOT)
 if (ROOT/file).read_bytes()!=before:errors.append('Unexpected change: '+file)
report={'results':results,'unchanged_files':unchanged,'errors':errors}
(HERE/'static-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
