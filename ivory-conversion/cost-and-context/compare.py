#!/usr/bin/env python3
"""Per-slide content comparison: cost-and-context.html (Ember) vs cost-and-context-ivory.html.
Compares data-label, data-origin-slide, raw data-speaker-notes (byte for byte), hrefs and
whitespace-normalised visible text. Also runs static template checks on the Ivory file."""
import re, sys, html
from html.parser import HTMLParser

SRC, DST = "cost-and-context.html", "cost-and-context-ivory.html"

def sections(raw):
    body = raw[raw.index("<deck-stage"):raw.index("</deck-stage>")]
    return re.findall(r"<section\b(.*?)>(.*?)</section>", body, re.S)

def attr(a, name):
    m = re.search(r'\b%s="([^"]*)"' % name, a, re.S)
    return m.group(1) if m else None

class Text(HTMLParser):
    def __init__(s): super().__init__(); s.t=[]; s.h=[]; s.skip=0
    def handle_starttag(s, tag, a):
        a=dict(a)
        if tag=="a": s.h.append(a.get("href"))
        if tag in ("video","source"): s.h.append("media:"+str(a.get("src")))
        if tag=="br": s.t.append(" ")
    def handle_data(s, d): s.t.append(d)
    def text(s): return re.sub(r"\s+"," ",html.unescape("".join(s.t))).strip()

def parse(raw):
    out=[]
    for a, inner in sections(raw):
        inner_nocomment = re.sub(r"<!--.*?-->","",inner,flags=re.S)
        p=Text(); p.feed(inner_nocomment)
        out.append(dict(label=attr(a,"data-label"), origin=attr(a,"data-origin-slide"),
                        notes=attr(a,"data-speaker-notes"), hrefs=p.h, text=p.text()))
    return out

src=parse(open(SRC,encoding="utf-8").read()); dst_raw=open(DST,encoding="utf-8").read(); dst=parse(dst_raw)
print(f"slides: source {len(src)}, ivory {len(dst)}")
fail=0
for i,(s,d) in enumerate(zip(src,dst),1):
    issues=[]
    for k in ("label","origin","notes"):
        if s[k]!=d[k]: issues.append(f"{k} differs:\n    src={s[k]!r}\n    ivy={d[k]!r}")
    sh=[h.replace("-light.mp4","-ivory.mp4") if h.startswith("media:") else h for h in s["hrefs"]]
    if sh!=d["hrefs"]: issues.append(f"hrefs differ: src={s['hrefs']} ivy={d['hrefs']}")
    st=re.sub(r"^\d+","",s["text"]) if i>1 else s["text"]  # drop hand-written Ember .snum digits
    ns, nd = re.sub(r"\s+","",st), re.sub(r"\s+","",d["text"])
    if ns!=nd:
        from collections import Counter
        ws, wd = Counter(re.findall(r"\w+|[^\w\s]",st)), Counter(re.findall(r"\w+|[^\w\s]",d["text"]))
        issues.append(f"visible text differs (ignoring whitespace). only in source: {dict(ws-wd)}; only in ivory: {dict(wd-ws)}")
    print(f"\n[{i:02d}] {s['label']} (origin {s['origin']}): " + ("IDENTICAL (label, origin, raw notes, hrefs, visible text ignoring whitespace)" if not issues else "DIFFERENCES"))
    for x in issues: print("  - "+x)
    if s["hrefs"]!=d["hrefs"]: print(f"  hrefs src: {s['hrefs']}\n  hrefs ivy: {d['hrefs']}")

print("\n== static checks on", DST)
links=re.findall(r"<link\b[^>]*>",dst_raw); scripts=re.findall(r"<script\b[^>]*>",dst_raw)
print("link tags:",links); print("script tags:",scripts)
print("inline <script> bodies:", len(re.findall(r"<script\b[^>]*>\s*[^<\s]",dst_raw)))
print("<style> elements:", len(re.findall(r"<style\b",dst_raw)))
print("style= attributes:", len(re.findall(r"\sstyle=",dst_raw)))
print("non-empty .snum:", len(re.findall(r'class="snum">[^<]',dst_raw)), "/ empty .snum:", len(re.findall(r'class="snum"></span>',dst_raw)))
print("dark/light/reveal/dot/ts- classes:", re.findall(r'class="[^"]*\b(dark|light|reveal|dot|ts-\w+|slide-content|kcard|fill|lead|extag)\b',dst_raw))
print("ember refs:", dst_raw.count("ember_design_system"), " fonts.googleapis:", dst_raw.count("googleapis"))
print("clay (.key) per slide:", [len(re.findall(r'\bkey\b',inner)) for _,inner in sections(dst_raw)])
print("notes per slide:", [len(re.findall(r'class="note"',inner)) for _,inner in sections(dst_raw)])
