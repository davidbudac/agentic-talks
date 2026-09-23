#!/usr/bin/env python3
"""Build three static v2 decks from the preserved original presentation shells.

Run from any directory: PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_first_three_v2.py
Edit slide content below; shared original deck styles and stage remain untouched.
The visual layer (helpers, drawn diagrams and CSS) follows visual-mockups-v2.html:
fill the stage, draw one idea per slide, make evidence huge, keep wayfinding and rhythm.
"""
from pathlib import Path
from html import escape as esc
from urllib.parse import urlparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'reviews/first-three-v2'


def plain(text):
    return re.sub(r'<[^>]+>', '', text)


# ── ICONS ──────────────────────────────────────────────────────────────
# Stroke icons on a 120×120 grid; colour comes from CSS `color`.
ICONS = {
 'doc': '<path d="M20 26 V108 H70" opacity=".45"/><path d="M32 12 H78 L100 34 V100 H32 Z"/><path d="M78 12 V34 H100"/><path d="M46 52 H86 M46 66 H86 M46 80 H72"/>',
 'media': '<rect x="12" y="12" width="96" height="66" rx="8"/><path d="M12 68 L42 42 L62 60 L76 48 L108 74"/><circle cx="84" cy="32" r="8"/><path d="M22 100 V108 M36 94 V114 M50 98 V110 M64 90 V118 M78 96 V112 M92 100 V108" stroke-width="6"/>',
 'actions': '<circle cx="40" cy="42" r="28" stroke-width="12" stroke-dasharray="11 11" stroke-linecap="butt"/><circle cx="40" cy="42" r="22" class="bg"/><circle cx="40" cy="42" r="8"/><path d="M72 42 H102 V84"/><path d="M92 76 L102 88 L112 76"/><rect x="60" y="94" width="48" height="20" rx="5"/><path d="M60 104 H22 V74"/>',
 'sheet': '<rect x="14" y="18" width="92" height="84" rx="8"/><path d="M14 42 H106 M14 66 H106 M44 18 V102"/>',
 'report': '<path d="M24 10 H76 L98 32 V110 H24 Z"/><path d="M76 10 V32 H98"/><path d="M42 92 V76 M60 92 V58 M78 92 V70" stroke-width="9"/>',
 'brief': '<rect x="22" y="20" width="76" height="90" rx="8"/><rect x="42" y="10" width="36" height="18" rx="5" class="bg"/><path d="M38 52 H82 M38 68 H82 M38 84 H66"/>',
 'trace': '<circle cx="30" cy="32" r="16"/><rect x="72" y="72" width="34" height="34" rx="6"/><path d="M46 38 C70 44 62 76 70 84" stroke-dasharray="3 10"/><path d="M58 76 L70 86 L76 72"/>',
 'search': '<circle cx="50" cy="50" r="32"/><path d="M74 74 L106 106" stroke-width="11"/>',
 'decide': '<path d="M60 112 V66 L28 28 M60 66 L92 28"/><path d="M22 46 L26 24 L46 26"/><path d="M74 26 L94 24 L98 46"/>',
 'chat': '<path d="M14 20 H106 V80 H54 L32 102 V80 H14 Z"/><path d="M34 42 H86 M34 58 H70"/>',
 'loop': '<path d="M100 60 A40 40 0 1 1 88 31"/><path d="M92 8 L90 32 L66 30"/>',
 'stack': '<rect x="34" y="10" width="68" height="82" rx="6" opacity=".45"/><rect x="18" y="26" width="68" height="84" rx="6" class="bg"/><path d="M32 50 H72 M32 66 H72 M32 82 H58"/>',
 'lock': '<rect x="22" y="52" width="76" height="58" rx="8"/><path d="M38 52 V38 A22 22 0 0 1 82 38 V52"/><path d="M60 72 V88"/>',
 'star': '<path d="M60 12 L72 44 L106 46 L80 68 L88 102 L60 84 L32 102 L40 68 L14 46 L48 44 Z"/>',
 'slides': '<rect x="10" y="16" width="100" height="68" rx="6"/><path d="M60 84 V104 M38 108 H82"/><path d="M26 36 H64 M26 52 H54"/><rect x="72" y="42" width="24" height="28" rx="3"/>',
 'variants': '<rect x="12" y="12" width="44" height="44" rx="6"/><rect x="64" y="12" width="44" height="44" rx="6"/><rect x="12" y="64" width="44" height="44" rx="6"/><rect x="64" y="64" width="44" height="44" rx="6"/><circle cx="34" cy="34" r="10"/><path d="M74 46 L86 22 L98 46 Z"/><path d="M22 96 L34 76 L46 96"/><path d="M74 86 H98"/>',
 'template': '<rect x="12" y="12" width="96" height="96" rx="8"/><path d="M26 32 H74" stroke-width="9"/><rect x="26" y="50" width="68" height="42" rx="4" stroke-dasharray="7 7"/>',
 'browser': '<rect x="8" y="16" width="104" height="88" rx="8"/><path d="M8 38 H112"/><path d="M20 27 H22 M30 27 H32" stroke-width="7"/><path d="M26 60 H72 M26 78 H58"/>',
 'mail': '<rect x="10" y="26" width="100" height="70" rx="6"/><path d="M12 30 L60 66 L108 30"/>',
 'sparkle': '<path d="M60 10 C64 44 76 56 110 60 C76 64 64 76 60 110 C56 76 44 64 10 60 C44 56 56 44 60 10 Z"/>',
 'person': '<circle cx="60" cy="36" r="20"/><path d="M22 110 C22 82 40 68 60 68 C80 68 98 82 98 110"/>',
 'team': '<circle cx="44" cy="40" r="16"/><path d="M12 104 C12 80 26 68 44 68 C62 68 76 80 76 104"/><circle cx="82" cy="34" r="13" opacity=".6"/><path d="M84 60 C100 60 110 72 110 94" opacity=".6"/>',
 'upload': '<path d="M60 84 V16 M34 42 L60 16 L86 42"/><path d="M14 74 V104 H106 V74"/>',
 'link': '<rect x="8" y="42" width="62" height="36" rx="18"/><rect x="50" y="42" width="62" height="36" rx="18"/>',
 'panel': '<rect x="8" y="16" width="104" height="88" rx="8"/><path d="M74 16 V104"/><path d="M22 38 H60 M22 54 H60 M22 70 H48"/><path d="M86 40 H100 M86 56 H100"/>',
 'folder': '<path d="M10 28 V98 H110 V42 H58 L46 28 Z"/>',
 'key': '<circle cx="34" cy="60" r="20"/><path d="M54 60 H110 M96 60 V80 M80 60 V76"/>',
 'suite': '<rect x="12" y="12" width="42" height="42" rx="8"/><rect x="66" y="12" width="42" height="42" rx="8"/><rect x="12" y="66" width="42" height="42" rx="8"/><path d="M87 68 C89 82 94 86 108 87 C94 89 89 94 87 108 C85 94 80 89 66 87 C80 86 85 82 87 68 Z"/>',
 'card': '<rect x="8" y="24" width="104" height="72" rx="8"/><path d="M8 46 H112" stroke-width="10"/><path d="M22 78 H52"/>',
 'coins': '<ellipse cx="60" cy="30" rx="40" ry="14"/><path d="M20 30 V58 C20 66 38 72 60 72 C82 72 100 66 100 58 V30"/><path d="M20 58 V86 C20 94 38 100 60 100 C82 100 100 94 100 86 V58"/>',
 'clock': '<circle cx="60" cy="60" r="48"/><path d="M60 28 V60 L82 74"/>',
 'flask': '<path d="M44 12 H76"/><path d="M52 12 V46 L22 100 C19 106 22 110 29 110 H91 C98 110 101 106 98 100 L68 46 V12"/><path d="M34 82 H86"/>',
 'warn': '<path d="M60 12 L112 104 H8 Z"/><path d="M60 46 V72"/><path d="M60 88 V90" stroke-width="9"/>',
 'pencil': '<path d="M18 102 L26 74 L84 16 L104 36 L46 94 Z"/><path d="M72 28 L92 48"/>',
 'tick': '<path d="M16 62 L46 92 L104 28" stroke-width="12"/>',
 'cross': '<path d="M26 26 L94 94 M94 26 L26 94" stroke-width="11"/>',
 'terminal': '<rect x="8" y="16" width="104" height="88" rx="8"/><path d="M26 46 L44 60 L26 74"/><path d="M54 76 H86"/>',
 'gear': '<circle cx="60" cy="60" r="22"/><path d="M60 12 V28 M60 92 V108 M12 60 H28 M92 60 H108 M26 26 L37 37 M83 83 L94 94 M94 26 L83 37 M37 83 L26 94"/>',
 'codefile': '<path d="M24 10 H76 L98 32 V110 H24 Z"/><path d="M76 10 V32 H98"/><path d="M50 58 L38 72 L50 86 M72 58 L84 72 L72 86"/>',
 'code': '<path d="M38 30 L10 60 L38 90 M82 30 L110 60 L82 90 M70 18 L50 102"/>',
 'stop': '<path d="M40 8 H80 L112 40 V80 L80 112 H40 L8 80 V40 Z"/><path d="M40 60 H80" stroke-width="12"/>',
 'redirect': '<path d="M16 100 C16 52 42 36 92 36"/><path d="M72 16 L94 36 L72 56"/>',
 'book': '<path d="M60 26 C46 16 26 14 10 18 V100 C26 96 46 98 60 108 C74 98 94 96 110 100 V18 C94 14 74 16 60 26 Z"/><path d="M60 26 V108"/>',
 'pin': '<path d="M42 12 H78 L72 46 L94 66 H26 L48 46 Z"/><path d="M60 66 V112"/>',
 'globe': '<circle cx="60" cy="60" r="48"/><ellipse cx="60" cy="60" rx="20" ry="48"/><path d="M12 60 H108"/>',
 'dial': '<circle cx="60" cy="66" r="42"/><path d="M60 66 L86 40" stroke-width="8"/><path d="M60 12 V20 M12 66 H20 M100 66 H108 M26 32 L32 38 M94 32 L88 38"/>',
 'checklist': '<rect x="10" y="14" width="24" height="24" rx="5"/><path d="M46 26 H110"/><rect x="10" y="48" width="24" height="24" rx="5"/><path d="M46 60 H110"/><rect x="10" y="82" width="24" height="24" rx="5"/><path d="M46 94 H96"/><path d="M15 26 L21 32 L31 19"/><path d="M15 60 L21 66 L31 53"/>',
 'exit': '<path d="M70 12 H22 V108 H70"/><path d="M48 60 H110 M90 40 L110 60 L90 80"/>',
 'diff': '<rect x="10" y="12" width="100" height="96" rx="8"/><path d="M28 40 H56 M42 26 V54"/><path d="M64 82 H92"/>',
 'target': '<circle cx="60" cy="60" r="48"/><circle cx="60" cy="60" r="30"/><circle cx="60" cy="60" r="10"/>',
 'question': '<path d="M36 40 C36 14 84 14 84 40 C84 60 60 58 60 80"/><path d="M60 100 V102" stroke-width="10"/>',
 'list': '<path d="M40 28 H108 M40 60 H108 M40 92 H90"/><circle cx="18" cy="28" r="5"/><circle cx="18" cy="60" r="5"/><circle cx="18" cy="92" r="5"/>',
 'flag': '<path d="M22 112 V12"/><path d="M22 16 H98 L84 40 L98 64 H22"/>',
 'restore': '<path d="M30 70 A36 36 0 1 0 38 36"/><path d="M16 22 L38 36 L24 58"/>',
 'agent': '<rect x="18" y="34" width="84" height="66" rx="14"/><path d="M60 14 V34"/><circle cx="60" cy="12" r="5"/><circle cx="44" cy="62" r="7"/><circle cx="76" cy="62" r="7"/><path d="M46 84 H74"/>',
 'eye': '<path d="M6 60 C28 24 92 24 114 60 C92 96 28 96 6 60 Z"/><circle cx="60" cy="60" r="17"/>',
 'cloud': '<path d="M30 92 C12 92 8 70 24 64 C20 44 44 36 54 48 C60 28 94 30 92 56 C110 56 112 92 90 92 Z" stroke-dasharray="8 8"/>',
 'box': '<path d="M60 10 L108 34 V86 L60 110 L12 86 V34 Z"/><path d="M12 34 L60 58 L108 34 M60 58 V110"/>',
 'merge': '<path d="M16 16 C16 58 60 56 60 82 M104 16 C104 58 60 56 60 82 M60 16 V82 V110"/><path d="M44 94 L60 110 L76 94"/>',
 'scale': '<path d="M60 14 V104 M36 108 H84 M20 30 H100"/><path d="M20 30 L6 68 H34 Z M100 30 L86 68 H114 Z"/>',
 'pause': '<path d="M44 24 V96 M76 24 V96" stroke-width="13"/>',
 'data': '<ellipse cx="60" cy="26" rx="42" ry="14"/><path d="M18 26 V94 C18 102 36 108 60 108 C84 108 102 102 102 94 V26"/><path d="M18 60 C18 68 36 74 60 74 C84 74 102 68 102 60"/>',
 'bulb': '<path d="M42 84 C42 70 26 62 26 42 A34 34 0 0 1 94 42 C94 62 78 70 78 84 Z"/><path d="M44 98 H76 M50 110 H70"/>',
}


def icon(name, cls=''):
    return f'<svg viewBox="0 0 120 120" class="ic {cls}" aria-hidden="true">{ICONS[name]}</svg>'


def sicon(name, cx, cy, size, cls=''):
    h = size / 2
    return f'<svg x="{cx-h:g}" y="{cy-h:g}" width="{size:g}" height="{size:g}" viewBox="0 0 120 120" class="ic {cls}">{ICONS[name]}</svg>'


_IDS = {}


def uid(prefix):
    _IDS[prefix] = _IDS.get(prefix, 0) + 1
    return f'{prefix}{_IDS[prefix]}'


def marker(mid, cls='mk-a', size=4):
    return f'<marker id="{mid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="{size}" markerHeight="{size}" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" class="{cls}"/></marker>'


def svg(w, h, inner, label=None, cls=''):
    a11y = f'role="img" aria-label="{esc(label, quote=True)}"' if label else 'aria-hidden="true"'
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" {a11y}>{inner}</svg>'


# ── BASE HELPERS (upgraded) ─────────────────────────────────────────────
def p(text, cls=''):
    return f'<p class="lead {cls}">{text}</p>'


def cards(*items, icons=None, cls=''):
    """Filled tiles: icon (optional), index, big title anchored low, body."""
    out = []
    for i, (t, b) in enumerate(items):
        ic = icon(icons[i]) if icons else ''
        out.append(f'<div class="v-tile"><div class="top">{ic}<span>{i+1:02}</span></div><h3>{t}</h3><p>{b}</p></div>')
    return f'<div class="v-tiles n{len(items)} {cls}">' + ''.join(out) + '</div>'


def stations(items, icons=None, hot=(), ok=(), back=None, label=None):
    """Route with stations: a coral rail, big circles with drawn icons, headline stops."""
    n = len(items)
    W, r = 1728, {2: 120, 3: 116, 4: 110, 5: 92}[n]
    top = 138 if back else 64
    cy = top + r
    H = cy + r + 8
    xs = [W / n * (i + .5) for i in range(n)]
    s = []
    if back:
        m = uid('mk')
        s.append(f'<defs>{marker(m, "mk-c")}</defs>')
    s.append(f'<line class="rl-base" x1="4" y1="{cy}" x2="{W-4}" y2="{cy}"/>')
    s.append(f'<line class="rl-on" x1="{xs[0]:g}" y1="{cy}" x2="{xs[-1]:g}" y2="{cy}"/>')
    if back:
        a, b, lab = back
        x1, x2, y = xs[a] - 30, xs[b] + 30, top - 6
        s.append(f'<path class="rl-back" d="M{x1:g} {y} C{x1:g} 20 {x2:g} 20 {x2:g} {y}" marker-end="url(#{m})"/>')
        mid, peak = (x1 + x2) / 2, .25 * y + .75 * 20
        s.append(f'<rect class="rl-bg" x="{mid-150:g}" y="{peak-24:g}" width="300" height="48" rx="24"/><text class="rl-bl" x="{mid:g}" y="{peak+9:g}" text-anchor="middle">{lab}</text>')
    else:
        s += [f'<text class="rl-n" x="{x:g}" y="40" text-anchor="middle">{i+1:02}</text>' for i, x in enumerate(xs)]
    for i, x in enumerate(xs):
        s.append(f'<circle class="rl-c{" hot" if i in hot else ""}" cx="{x:g}" cy="{cy}" r="{r}"/>')
        if icons:
            s.append(sicon(icons[i], x, cy, r * .98, ('ok ' if i in ok else '') + ('hot' if i in hot else '')))
        else:
            s.append(f'<text class="rl-num" x="{x:g}" y="{cy+22}" text-anchor="middle">{i+1:02}</text>')
    label = label or 'Sequence: ' + ' → '.join(plain(t) for t, _ in items)
    stops = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in items)
    return f'<div class="v-stn n{n}">' + svg(W, H, ''.join(s), label, 'rail') + f'<div class="stops">{stops}</div></div>'


def flow(*items):
    return stations(items)


PY_TOKEN = re.compile(r"(?P<c>#[^\n]*)|(?P<s>'[^'\n]*'|\"[^\"\n]*\")|(?P<k>\b(?:def|return|from|import)\b)|(?P<n>\b\d+(?:\.\d+)?\b)|(?P<x>[\s\S])")


def pyhl(src):
    out, buf = [], ''
    for m in PY_TOKEN.finditer(src):
        if m.lastgroup == 'x':
            buf += m.group()
            continue
        if buf:
            out.append(esc(buf))
            buf = ''
        out.append(f'<span class="{m.lastgroup}">{esc(m.group())}</span>')
    return ''.join(out) + esc(buf)


def window(title, body, kind='term', cls=''):
    return (f'<div class="v-win {kind} {cls}"><div class="tbar"><i class="r"></i><i class="y"></i><i class="g"></i>'
            f'<span>{title}</span></div><div class="wbody">{body}</div></div>')


def code(text, title='code', hl=False, cls=''):
    return window(title, pyhl(text) if hl else esc(text), 'term', cls)


def split(left, right, cls=''):
    return f'<div class="split {cls}"><div class="v2-stack">{left}</div><div class="v2-stack">{right}</div></div>'


def table(headers, rows):
    return '<table class="tbl"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in row) + '</tr>' for row in rows) + '</tbody></table>'


def callout(title, text, extra=''):
    return f'<div class="kcard"><div class="big">{title}</div>{extra}<p>{text}</p></div>'


def _where(url):
    if url.startswith('http'):
        return urlparse(url).netloc.replace('www.', '')
    return url


def links(*items):
    """Reference list: title, where it lives, arrow. Two columns when long."""
    rows = ''.join(f'<a href="{url}" target="_blank" rel="noopener"><span class="lt">{t}</span><span class="ld">{_where(url)}</span><span class="la" aria-hidden="true">↗</span></a>' for t, url in items)
    return f'<div class="v-refs n{len(items)}">{rows}</div>'


def linkcards(*items):
    """Big link cards: (title, url, icon, kicker)."""
    out = ''.join(f'<a class="v-lcard" href="{url}" target="_blank" rel="noopener">{icon(ic)}<span class="kk">{k}</span><span class="lt">{t}</span><span class="ld">{_where(url)} <b aria-hidden="true">↗</b></span></a>' for t, url, ic, k in items)
    return f'<div class="v-lcards n{len(items)}">{out}</div>'


VIDEO_SIZE = {'agent-loop-dark': (1152, 912), 'subagents-dark': (1176, 756)}


def video(name, caption, steps=None, cls=''):
    w, h = VIDEO_SIZE[name]
    side = ''
    if steps:
        side = '<ol class="vm-steps">' + ''.join(f'<li><span>{i:02}</span>{s}</li>' for i, s in enumerate(steps, 1)) + '</ol>'
    return (f'<figure class="v2-media {cls}"><video muted loop playsinline preload="metadata" width="{w}" height="{h}" poster="assets/v2/{name}.svg" aria-label="{esc(caption)}"><source src="assets/anim/{name}.mp4" type="video/mp4"></video>'
            f'<div class="vm-side">{side}{"" if steps else f"<figcaption>{caption}</figcaption>"}<button type="button" class="v2-play" data-video-toggle aria-pressed="false">Play animation</button></div></figure>')


def panels(*items, cls=''):
    """Side-by-side panels: (illustration, title, body[, kicker])."""
    out = []
    for it in items:
        ill, t, b = it[:3]
        k = f'<span class="kk">{it[3]}</span>' if len(it) > 3 else ''
        out.append(f'<div class="v-panel"><div class="illus">{ill}</div>{k}<h3>{t}</h3><p>{b}</p></div>')
    return f'<div class="v-panels n{len(items)} {cls}">' + ''.join(out) + '</div>'


def rows(*items, cls=''):
    """Full-width rows: (icon, title, body)."""
    out = ''.join(f'<div class="v-row">{icon(ic)}<h3>{t}</h3><p>{b}</p></div>' for ic, t, b in items)
    return f'<div class="v-rows {cls}">{out}</div>'


def mini(on):
    names = ['Failure', 'Evidence', 'Change', 'Check']
    li = ''.join(f'<li class="{"on" if i == on else ("done" if i < on else "")}"><i></i>{n}</li>' for i, n in enumerate(names, 1))
    return f'<ol class="mini" aria-label="Checkpoint {on} of 4: {names[on-1]}">{li}</ol>'


PROBLEMS = 7


def tracker(n):
    """Problem wayfinding for talk 03. Numbers are drawn by CSS counters; the label carries the meaning."""
    done = n > PROBLEMS
    li = ''.join(f'<li class="{"on" if i == n else ("done" if i < n else "")}"></li>' for i in range(1, PROBLEMS + 1))
    label = f'All {PROBLEMS} problems covered' if done else f'Problem {n} of {PROBLEMS}'
    return f'<ol class="ptrack" role="img" aria-label="{label}">{li}</ol>'


def slide(title, body, notes, origin, chapter='', dark=False, foot='', **kw):
    return dict(title=title, body=body, notes=notes, origin=origin, chapter=chapter, dark=dark, foot=foot, **kw)


def title(name, subtitle, audience, notes):
    return dict(title=name.replace('<br>', ' '), hero=name, subtitle=subtitle, audience=audience, notes=notes, origin='1', chapter='Start')


# ── REFERENCE DESIGNS FROM THE MOCK-UP ─────────────────────────────────
def failing_test():
    return f'''<div class="v-fail">{window('failing test', '''<div class="tcall"><span class="k">gross</span>(<span class="s">'100'</span>, <span class="s">'0.21'</span>)</div>
<div class="vs"><div class="val exp"><span class="lab"><i></i>expected</span><span class="num">121.00</span></div><div class="neq">≠</div><div class="val act"><span class="lab"><i></i>actual</span><span class="num">100.00</span></div></div>''')}
<p class="task">Find the cause, apply the supplied rate and <b>preserve the tests.</b></p></div>'''


def x_chip(ok, label):
    path = 'M12 38 L30 56 L62 18' if ok else 'M16 16 L58 58 M58 16 L16 58'
    return f'<div class="tst {"ok" if ok else "x"}"><svg viewBox="0 0 74 74" aria-hidden="true"><path d="{path}"/></svg><span>{label}</span></div>'


def checkpoint1():
    term = window('prepared fixture result', '<span class="p">$</span> python3 -m unittest -v\n\n<span class="dim">Ran 3 tests</span>\n<span class="fail">FAILED (failures=2)</span>')
    chips = x_chip(False, 'fails') + x_chip(False, 'fails') + x_chip(True, 'zero rate')
    return f'<div class="v-cp1">{term}<div><div class="tests" role="img" aria-label="Two tests fail; the zero-rate case passes">{chips}</div><p class="lead">The fixture <b>ignores tax.</b> The zero-rate case already passes.</p></div></div>'


def model_harness():
    m1, m2 = uid('mk'), uid('mk')
    art = f'''<defs>{marker(m1, 'mk-c', 4.2)}{marker(m2, 'mk-t', 4.2)}</defs>
<line x1="518" y1="170" x2="782" y2="170" class="ln-c" marker-end="url(#{m1})"/>
<text x="650" y="140" text-anchor="middle" class="t-acc">action proposal</text>
<line x1="782" y1="300" x2="518" y2="300" class="ln-t" marker-end="url(#{m2})"/>
<text x="650" y="350" text-anchor="middle" class="t-mut">context + results</text>
<g class="ln-dim"><path d="M1363 230 C1410 230 1405 138 1450 138"/><path d="M1363 230 L1450 260"/><path d="M1363 230 C1410 230 1405 382 1450 382"/></g>
<circle cx="1363" cy="230" r="9" class="f-coral"/>
<text x="1589" y="70" text-anchor="middle" class="t-cap">PERMITTED TOOLS</text>
<path d="M2 470 V494 H1726 V470" class="ln-dim"/>
<rect x="534" y="478" width="660" height="34" class="f-bg"/>
<text x="864" y="504" text-anchor="middle" class="t-cap">AGENT · THE TWO TOGETHER, ITERATING</text>'''
    return f'''<div class="v-mh">{svg(1728, 520, art, 'The model sends an action proposal to the harness; the harness runs permitted tools and returns context and results. Together, iterating, they form the agent.')}
<div class="box model"><span class="k">Chooses</span><h3>Model</h3><p>Proposes an answer or an action from the information it receives.</p></div>
<div class="box harness"><span class="k">Executes</span><h3>Harness</h3><p>Supplies context, runs permitted tools and returns their results.</p></div>
<div class="tool" style="top:99px">read file</div><div class="tool" style="top:221px">edit file</div><div class="tool" style="top:343px">run tests</div></div>'''


def claim_chain():
    m = uid('mk')
    art = f'''<defs>{marker(m, 'mk-c')}</defs>
<g class="ch-card"><rect x="1" y="1" width="500" height="358" rx="20"/><rect x="614" y="1" width="500" height="358" rx="20"/><rect x="1227" y="1" width="500" height="358" rx="20"/></g>
<g class="t-cap"><text x="40" y="56">ANSWER</text><text x="654" y="56">CITATION</text><text x="1267" y="56">SOURCE</text></g>
<g class="f-bar"><rect x="40" y="96" width="420" height="16" rx="8"/><rect x="40" y="136" width="380" height="16" rx="8"/><rect x="40" y="186" width="80" height="16" rx="8"/>
<rect x="40" y="236" width="410" height="16" rx="8"/><rect x="40" y="276" width="330" height="16" rx="8"/><rect x="40" y="316" width="220" height="16" rx="8"/></g>
<rect x="132" y="172" width="258" height="44" rx="8" class="hl-box"/><rect x="146" y="186" width="230" height="16" rx="8" class="f-coral"/>
<circle cx="424" cy="180" r="20" class="f-coral"/><text x="424" y="188" text-anchor="middle" class="t-on">1</text>
<rect x="654" y="92" width="100" height="66" rx="12" class="f-coral"/><text x="704" y="136" text-anchor="middle" class="t-on big">[1]</text>
<rect x="776" y="106" width="290" height="16" rx="8" class="f-mut"/><rect x="776" y="134" width="190" height="12" rx="6" class="f-bar"/>
<line x1="654" y1="186" x2="1074" y2="186" class="ln-dim"/>
<g class="t-cap"><text x="654" y="236">source</text><text x="654" y="282">date</text><text x="654" y="328">scope</text></g>
<g class="f-bar"><rect x="780" y="222" width="250" height="16" rx="8"/><rect x="780" y="268" width="130" height="16" rx="8"/><rect x="780" y="314" width="220" height="16" rx="8"/></g>
<g class="f-bar"><rect x="1267" y="96" width="420" height="16" rx="8"/><rect x="1267" y="136" width="390" height="16" rx="8"/><rect x="1267" y="286" width="410" height="16" rx="8"/><rect x="1267" y="316" width="250" height="16" rx="8"/></g>
<rect x="1253" y="166" width="448" height="100" rx="10" class="hl-box"/>
<rect x="1267" y="188" width="400" height="16" rx="8" class="f-coral"/><rect x="1267" y="226" width="300" height="16" rx="8" class="f-coral"/>
<circle cx="1694" cy="168" r="26" class="ok-dot"/><path d="M1681 169 L1691 179 L1708 159" class="ok-tick"/>
<path d="M446 180 C540 180 560 125 646 125" class="ln-c" marker-end="url(#{m})"/>
<path d="M1040 230 C1150 230 1150 216 1245 216" class="ln-c" marker-end="url(#{m})"/>'''
    steps = ''.join(f'<div><span class="n">{i:02}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([('Answer', 'Find the claim you may rely on.'), ('Citation', 'Open the source behind it.'), ('Evidence', 'Check that the source supports the claim.')], 1))
    return '<div class="v-chain">' + svg(1728, 360, art, 'A highlighted claim in an answer links to its citation, which links to the source passage that supports it.') + f'<div class="steps">{steps}</div></div>'


def buried():
    bars = [('74', 'log'), ('92', 'log'), ('58', 'dead end'), ('78', 'the contract', 1), ('86', 'outdated assumption'), ('66', 'log'), ('96', 'log'), ('52', 'dead end'), ('80', 'log'),
            ('70', 'relevant code', 1), ('88', 'outdated assumption'), ('60', 'dead end'), ('94', 'log'), ('82', 'current evidence', 1), ('70', 'log'), ('84', 'dead end')]
    b = ''.join(f'<div class="{"u" if len(x) > 2 else ""}" style="width:{x[0]}%">{x[1]}</div>' for x in bars)
    return f'''<div class="v-ctx" role="img" aria-label="Working context after exploring: the contract, relevant code and current evidence are buried among logs, dead ends and outdated assumptions."><div class="cap"><span>Working context</span><span>after exploring</span></div><div class="bars">{b}</div></div>
<p class="keep"><span>→</span> Keep the working set useful<small>Retain the contract, relevant code and current evidence.</small></p>'''


def cache_vs_compaction():
    pid, m = uid('hatch'), uid('mk')
    cache = f'''<defs><pattern id="{pid}" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="16" height="16" class="f-soft"/><rect width="6" height="16" class="f-coral" opacity=".28"/></pattern>{marker(m, 'mk-a')}</defs>
<g class="t-cap"><text x="0" y="24">REQUEST 1</text><text x="0" y="160">REQUEST 2</text></g>
<rect x="1" y="38" width="760" height="70" rx="10" class="bx-mid"/><text x="380" y="82" text-anchor="middle" class="t-mut">prefix</text>
<rect x="776" y="38" width="200" height="70" rx="10" class="bx-dash"/><text x="876" y="82" text-anchor="middle" class="t-faint">new turn</text>
<rect x="1" y="174" width="760" height="70" rx="10" fill="url(#{pid})" class="bx-hot"/>
<rect x="214" y="192" width="332" height="36" rx="18" class="f-bg"/><text x="380" y="218" text-anchor="middle" class="t-acc">same prefix · reused</text>
<rect x="776" y="174" width="280" height="70" rx="10" class="bx-dash"/><text x="916" y="218" text-anchor="middle" class="t-faint">new turn</text>
<path d="M530 112 V166" class="ln-a" marker-end="url(#{m})"/><path d="M230 112 V166" class="ln-a" marker-end="url(#{m})"/>'''
    widths = [(1, 96), (105, 64), (177, 120), (305, 80), (393, 140), (541, 70), (619, 110), (737, 90), (835, 130), (973, 76), (1057, 160)]
    hist = ''.join(f'<rect x="{x}" y="38" width="{w}" height="70" rx="8"/>' for x, w in widths)
    comp = f'''<g class="t-cap"><text x="0" y="24">HISTORY</text></g><g class="bx-mid">{hist}</g>
<path d="M1 112 L1 170 L300 170 L1216 112 Z" class="f-coral" opacity=".1"/>
<rect x="1" y="174" width="300" height="70" rx="10" class="f-ink"/><text x="151" y="218" text-anchor="middle" class="t-paper">summary</text>
<g class="lost"><rect x="560" y="186" width="54" height="40" rx="6" transform="rotate(-10 587 206)"/><rect x="636" y="198" width="40" height="34" rx="6" transform="rotate(12 656 215)"/><rect x="694" y="182" width="46" height="36" rx="6" transform="rotate(-4 717 200)"/></g>
<text x="770" y="218" class="t-danger">details may be lost</text>'''
    return f'''<div class="v-cc"><div class="row"><div><h3>Caching</h3><p>Reuses eligible computation; can reduce cost and latency.</p></div>{svg(1218, 250, cache, 'Caching: request 2 reuses the same prefix as request 1, followed by a new turn.')}</div>
<div class="row"><div><h3>Compaction</h3><p>Replaces history with a shorter summary; can lose details.</p></div>{svg(1218, 250, comp, 'Compaction: a long history becomes a short summary; some details may be lost.')}</div></div>'''


def accepted_chart():
    def m(label, a, b, wa, wb, tag=''):
        return (f'<div class="m"><div class="lab">{label}{tag}</div><div class="br"><i class="A" style="width:{wa}%"></i><b>{a}</b></div>'
                f'<div class="br"><i class="B" style="width:{wb}%"></i><b>{b}</b></div></div>')
    chart = (m('Model + tool cost', '$6', '$10', 48, 80, '<small>headline</small>') + m('Accepted tasks, out of 10', '6', '10', 48, 80)
             + m('Model + tool cost per accepted task', '$1', '$1', 80, 80, '<small class="hot">equal</small>') + m('Review time, total', '40 min', '15 min', 80, 30))
    return f'''<div class="v-acc"><div role="img" aria-label="Illustrative trial. Setup A: $6 model and tool cost, 6 of 10 accepted, $1 per accepted task, 40 minutes review. Setup B: $10, 10 of 10, $1 per accepted task, 15 minutes review.">
<div class="legend"><b>Illustrative trial</b><span><i class="A"></i>Setup A</span><span><i class="B"></i>Setup B</span></div>{chart}</div>
<div class="call"><span class="k">Model + tool cost per accepted task</span><div class="big">$1 <span class="eq">=</span> $1</div><div class="hr"></div>
<span class="k">Review time with Setup B</span><div class="big o">−25<small>min</small></div><p>Same model and tool cost per accepted task, but B accepts 10 of 10 and A only 6.</p></div></div>'''


# ── BESPOKE VISUALS ───────────────────────────────────────────────────
def node(cx, cy, r, ic, cls='nd'):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}"/>' + sicon(ic, cx, cy, r * 1.05)


def io_task():
    files = ''.join(f'<div class="f">{icon(i)}<span>{t}</span></div>' for i, t in [('sheet', 'csv'), ('report', 'report'), ('brief', 'brief')])
    m = uid('mk')
    arrow = svg(160, 60, f'<defs>{marker(m, "mk-c", 3)}</defs><line x1="8" y1="30" x2="140" y2="30" class="ln-c thick" marker-end="url(#{m})"/>', cls='io-arrow')
    out = f'''<svg viewBox="0 0 260 300" class="io-doc" role="img" aria-label="A draft report: one number checked, one gap visible">
<path d="M20 10 H190 L240 60 V290 H20 Z" class="d-page"/><path d="M190 10 V60 H240" class="d-page"/>
<rect x="48" y="44" width="110" height="18" rx="9" class="f-ink2"/>
<rect x="48" y="100" width="130" height="30" rx="4" class="f-coral"/><circle cx="206" cy="115" r="17" class="ok-dot"/><path d="M198 115 L204 121 L214 109" class="ok-tick sm"/>
<rect x="48" y="150" width="160" height="30" rx="4" class="f-coral"/>
<rect x="48" y="200" width="160" height="30" rx="4" class="gap"/><text x="128" y="222" text-anchor="middle" class="t-acc sm">gap</text>
<rect x="48" y="252" width="120" height="12" rx="6" class="f-bar"/></svg>'''
    return (p('Turn this month’s files into a review someone can use.') +
            f'''<div class="v-io"><div class="io-p"><span class="kk">Inputs</span><div class="files">{files}</div><p>A results CSV, last month’s report and a short brief.</p></div>{arrow}
<div class="io-p out"><span class="kk">Output</span><div class="outrow">{out}<p>A draft report with checked numbers and visible gaps.</p></div></div></div>''')


def report():
    return '''<div class="v2-report"><div class="v2-report-head">QUARTERLY REVIEW <span>Teaching example · synthetic data</span></div>
<div class="rp-grid"><div><h3>April–May grew. June is incomplete.</h3>
<div class="v2-bars" role="img" aria-label="Completed orders: April 80, May 120, June missing"><div><span>April</span><i style="--bar-width:66.67%"></i><b>80</b></div><div><span>May</span><i style="--bar-width:100%"></i><b>120</b></div><div><span>June</span><i class="missing"></i><b class="miss">Missing</b></div></div></div>
<div class="rp-side"><p>Completed orders · May vs April: <span class="rp-big">+50%</span></p><div class="v2-report-flag">''' + icon('warn') + '''Q2 total withheld until June is supplied.</div></div></div></div>'''


def brief_window(lines, marks, title='brief'):
    body = ''.join(f'<div class="ln{" mk" if i in marks else ""}"><span class="no">{i}</span><span class="tx">{esc(t)}</span>{"<b>check</b>" if i in marks else ""}</div>' for i, t in enumerate(lines, 1))
    return window(title, body, 'paper', 'v-brief')


def chat_vs_agent():
    ma, mb, mc, md = uid('mk'), uid('mk'), uid('mk'), uid('mk')
    chat = f'''<defs>{marker(ma, 'mk-t')}{marker(mb, 'mk-m')}</defs>
<g class="t-cap" text-anchor="middle"><text x="100" y="24">you</text><text x="350" y="24">chat</text><text x="600" y="24">your files</text></g>
{node(100, 140, 62, 'person')}{node(350, 140, 62, 'chat')}{node(600, 140, 62, 'folder', 'nd soft')}
<line x1="176" y1="120" x2="268" y2="120" class="ln-t" marker-end="url(#{ma})"/><line x1="268" y1="162" x2="176" y2="162" class="ln-t" marker-end="url(#{ma})"/>
<path d="M100 212 C100 268 600 268 600 216" class="ln-m dash" marker-end="url(#{mb})"/>'''
    agent = f'''<defs>{marker(mc, 'mk-t')}{marker(md, 'mk-c')}</defs>
<g class="t-cap" text-anchor="middle"><text x="100" y="24">you</text><text x="350" y="24">agent</text><text x="600" y="24">your files</text></g>
{node(100, 140, 62, 'person')}
<circle cx="350" cy="140" r="88" class="ring"/><path d="M335 53 A88 88 0 0 1 433 110" class="ln-c" marker-end="url(#{md})"/>
{node(350, 140, 62, 'loop', 'nd hot')}{node(600, 140, 62, 'folder', 'nd soft')}
<line x1="176" y1="140" x2="252" y2="140" class="ln-t" marker-end="url(#{mc})"/><line x1="448" y1="140" x2="524" y2="140" class="ln-c" marker-end="url(#{md})"/>
<text x="486" y="196" text-anchor="middle" class="t-acc sm">tools</text>'''
    return panels((svg(700, 280, chat, 'Chat: you ask and receive an answer, then carry the work into your files yourself.'), 'Chat', 'You ask for help, then carry the work into your files.'),
                  (svg(700, 280, agent, 'Agent: it loops through tools and results, acting on your files.'), 'Agent', 'It uses tools, reads the results and carries on with the task.'), cls='wide')


def cycle(items, icons, label, exit_label=None):
    """A drawn loop: nodes on a ring with arrows, plus a numbered legend."""
    n = len(items)
    cx, cy, R, r = 330, 330, 240, 88
    import math
    angs = [-90 + 360 / n * i for i in range(n)]
    pts = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in angs]
    m, mx = uid('mk'), uid('mk')
    s = [f'<defs>{marker(m, "mk-c", 3.4)}{marker(mx, "mk-m", 3.4)}</defs>', f'<circle cx="{cx}" cy="{cy}" r="{R}" class="ring"/>']
    gap = math.degrees((r + 18) / R)
    for i in range(n):
        a1, a2 = angs[i] + gap, angs[i] + 360 / n - gap
        x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
        x2, y2 = cx + R * math.cos(math.radians(a2)), cy + R * math.sin(math.radians(a2))
        s.append(f'<path d="M{x1:.1f} {y1:.1f} A{R} {R} 0 0 1 {x2:.1f} {y2:.1f}" class="ln-c thick" marker-end="url(#{m})"/>')
    if exit_label:
        x, y = pts[-1]
        s.append(f'<path d="M{x-r-6:.1f} {y:.1f} H{x-r-120:.1f}" class="ln-m dash" marker-end="url(#{mx})"/>')
    for i, (x, y) in enumerate(pts):
        s.append(node(round(x, 1), round(y, 1), r, icons[i], 'nd' + (' hot' if i == 0 else '')))
    if exit_label:
        x, y = pts[-1]
        s.append(f'<text x="{x-r-66:.1f}" y="{y-24:.1f}" text-anchor="middle" class="t-mut sm">{exit_label}</text>')
    legend = ''.join(f'<li><span>{i:02}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(items, 1))
    return f'<div class="v-cycle n{n}">' + svg(660, 660, ''.join(s), label) + f'<ol>{legend}</ol></div>'


def context_supply():
    m = uid('mk')
    chips = ''
    for i, (ic, t) in enumerate([('stack', 'sources'), ('lock', 'constraints'), ('star', 'examples')]):
        y = 20 + i * 140
        chips += f'<rect x="2" y="{y}" width="330" height="104" rx="18" class="bx-card"/>' + sicon(ic, 60, y + 52, 64) + f'<text x="112" y="{y+62}" class="t-strong">{t}</text>'
        chips += f'<path d="M334 {y+52} C440 {y+52} 450 230 530 230" class="ln-c" marker-end="url(#{m})"/>'
    art = f'<defs>{marker(m, "mk-c", 3.4)}</defs>{chips}' + node(660, 230, 116, 'sparkle', 'nd') + '<text x="660" y="396" text-anchor="middle" class="t-cap">ASSISTANT</text>'
    return (p('The assistant needs the sources, constraints and examples relevant to this task.') +
            '<div class="v-sup">' + svg(800, 420, art, 'Sources, constraints and examples flow into the assistant.') +
            callout('Give it enough to work with', 'A clear brief and the right files help more than a longer prompt.') + '</div>')


def ill_sources():
    bars = ''.join(f'<rect x="{440+i*22}" y="{130-h/2}" width="12" height="{h}" rx="6" class="f-coral"/>' for i, h in enumerate([30, 70, 110, 60, 140, 90, 40, 120, 80, 50, 100, 30]))
    return svg(720, 260, f'''<rect x="80" y="20" width="170" height="210" rx="10" class="bx-mid"/><rect x="56" y="36" width="170" height="210" rx="10" class="bx-mid"/>
<rect x="32" y="52" width="170" height="196" rx="10" class="bx-card"/><rect x="54" y="84" width="120" height="12" rx="6" class="f-bar"/><rect x="54" y="112" width="130" height="12" rx="6" class="f-coral"/>
<rect x="54" y="140" width="100" height="12" rx="6" class="f-bar"/><rect x="54" y="168" width="126" height="12" rx="6" class="f-bar"/><rect x="54" y="196" width="80" height="12" rx="6" class="f-bar"/>
<path d="M280 130 H400" class="ln-c thick dash"/>{bars}''')


def ill_present():
    m = uid('mk')
    return svg(720, 260, f'''<defs>{marker(m, 'mk-c', 3.4)}</defs>
<g class="f-bar"><circle cx="46" cy="60" r="8"/><rect x="66" y="52" width="160" height="16" rx="8"/><circle cx="70" cy="104" r="7"/><rect x="88" y="96" width="120" height="14" rx="7"/>
<circle cx="70" cy="144" r="7"/><rect x="88" y="136" width="140" height="14" rx="7"/><circle cx="46" cy="190" r="8"/><rect x="66" y="182" width="130" height="16" rx="8"/></g>
<line x1="262" y1="130" x2="360" y2="130" class="ln-c thick" marker-end="url(#{m})"/>
<rect x="390" y="30" width="310" height="200" rx="14" class="bx-card"/><rect x="418" y="60" width="170" height="20" rx="10" class="f-ink2"/>
<rect x="418" y="100" width="120" height="12" rx="6" class="f-bar"/><rect x="418" y="124" width="100" height="12" rx="6" class="f-bar"/>
<rect x="560" y="100" width="116" height="104" rx="8" class="f-coral"/>''')


def ill_explore():
    shapes = [
        '<circle cx="{x}" cy="{y}" r="30" class="f-coral"/>', '<path d="M{x0} {y1} L{x} {y0} L{x1} {y1} Z" class="f-mut"/>',
        '<rect x="{x0}" y="{y0}" width="64" height="60" rx="30" class="f-soft2"/>', '<path d="M{x0} {y} Q{x} {y0} {x1} {y} T{x2} {y}" class="ln-c thick"/>',
        '<rect x="{x0}" y="{y0}" width="64" height="60" rx="6" class="f-coral" opacity=".55"/>', '<circle cx="{x}" cy="{y}" r="30" class="bx-dash2"/>']
    out = ''
    for i, sh in enumerate(shapes):
        cx, cy = 120 + (i % 3) * 240, 70 + (i // 3) * 130
        out += f'<rect x="{cx-100}" y="{cy-55}" width="200" height="110" rx="12" class="bx-card"/>'
        out += sh.format(x=cx, y=cy, x0=cx - 32, x1=cx + 32, x2=cx + 60, y0=cy - 30, y1=cy + 30)
    return svg(720, 260, out)


def ill_template():
    out = ''
    for i, v in enumerate(['01', '02', '03']):
        x = 20 + i * 235
        out += f'<rect x="{x}" y="10" width="205" height="240" rx="12" class="bx-card"/><rect x="{x+22}" y="34" width="120" height="18" rx="9" class="f-coral"/>'
        out += f'<text x="{x+22}" y="150" class="t-num">{v}</text><rect x="{x+22}" y="186" width="160" height="12" rx="6" class="f-bar"/><rect x="{x+22}" y="210" width="110" height="12" rx="6" class="f-bar"/>'
    return svg(720, 260, out)


def app_owner():
    m = uid('mk')
    screens = ''.join(f'<rect x="{60+i*250}" y="120" width="190" height="130" rx="10" class="bx-mid"/><rect x="{80+i*250}" y="142" width="110" height="14" rx="7" class="f-bar"/><rect x="{80+i*250}" y="170" width="150" height="54" rx="6" class="bx-card"/>' for i in range(3))
    arrows = ''.join(f'<line x1="{254+i*250}" y1="185" x2="{304+i*250}" y2="185" class="ln-c thick" marker-end="url(#{m})"/>' for i in range(2))
    art = f'''<defs>{marker(m, 'mk-c', 3.2)}</defs><rect x="20" y="20" width="780" height="420" rx="18" class="bx-card"/><path d="M20 70 H800" class="ln-dim"/>
<circle cx="52" cy="45" r="8" class="f-bar"/><circle cx="80" cy="45" r="8" class="f-bar"/><circle cx="108" cy="45" r="8" class="f-bar"/>
<text x="410" y="108" text-anchor="middle" class="t-acc sm">main journey</text>{screens}{arrows}
<path d="M155 250 V330 H370" class="ln-m dash"/><path d="M655 250 V330 H450" class="ln-m dash"/><path d="M405 250 V300" class="ln-m dash"/>
<g transform="translate(362 300) scale(.72)" class="ic stroke-a">{ICONS['data']}</g><text x="530" y="384" class="t-mut sm">data</text>'''
    gates = rows(('eye', 'Before sharing', 'Check the main journey and what data it stores.'), ('person', 'Before relying on it', 'Have someone own access, testing and maintenance.'), cls='gates')
    return f'<div class="v-app"><div class="v2-stack">{svg(820, 460, art, "An app draft: screens linked by a main journey, storing data.")}{p("Tools such as Lovable can produce a working app from a brief.", "sm")}</div>{gates}</div>'


def access_scope():
    m = uid('mk')
    art = f'''<defs>{marker(m, 'mk-c', 3.4)}</defs>{node(110, 200, 86, 'link', 'nd')}<text x="110" y="330" text-anchor="middle" class="t-cap">CONNECTION</text>
<path d="M196 190 C300 190 300 90 400 90" class="ln-c thick" marker-end="url(#{m})"/><path d="M196 210 C300 210 300 310 400 310" class="ln-c thick" marker-end="url(#{m})"/>
<rect x="412" y="40" width="380" height="100" rx="18" class="bx-card"/>{sicon('folder', 466, 90, 60)}<text x="516" y="100" class="t-strong">read a folder</text>
<rect x="412" y="260" width="380" height="100" rx="18" class="bx-card"/>{sicon('mail', 466, 310, 60)}<text x="516" y="320" class="t-strong">send an email</text>
{sicon('lock', 760, 44, 44, 'lk')}{sicon('lock', 760, 264, 44, 'lk')}'''
    badges = ''.join(f'<span>{icon(i)}{t}</span>' for i, t in [('key', 'account'), ('folder', 'data'), ('gear', 'actions')])
    return split(p('Reading a folder and sending an email are different permissions.') + svg(800, 400, art, 'One connection can carry two different permissions: read a folder, send an email.'),
                 callout('Check the scope', 'Which account, which data and which actions are you granting?', f'<div class="badges">{badges}</div>'), cls='v-acs')


def story(kicker_items, illus, cls=''):
    txt = ''.join(f'<div class="st-i"><span class="kk">{k}</span><p>{t}</p></div>' for k, t in kicker_items)
    return f'<div class="v-story {cls}"><div class="st-t">{txt}</div><div class="st-ill">{illus}</div></div>'


def ill_vend():
    return svg(640, 520, f'''<rect x="30" y="20" width="250" height="470" rx="20" class="bx-card"/><rect x="58" y="52" width="150" height="290" rx="8" class="bx-mid"/>
<g class="f-coral"><rect x="76" y="76" width="36" height="46" rx="6"/><rect x="128" y="76" width="36" height="46" rx="6" opacity=".6"/><rect x="76" y="150" width="36" height="46" rx="6" opacity=".6"/><rect x="128" y="150" width="36" height="46" rx="6"/><rect x="76" y="224" width="36" height="46" rx="6"/><rect x="128" y="224" width="36" height="46" rx="6" opacity=".6"/></g>
<rect x="226" y="60" width="32" height="70" rx="6" class="bx-mid"/><rect x="226" y="150" width="32" height="32" rx="16" class="bx-mid"/><rect x="70" y="386" width="170" height="54" rx="10" class="bx-mid"/>
<line x1="330" y1="470" x2="630" y2="470" class="ln-dim"/>
<rect x="360" y="130" width="100" height="340" rx="6" class="f-mut"/><rect x="500" y="250" width="100" height="220" rx="6" class="f-coral"/>
<line x1="350" y1="130" x2="620" y2="130" class="ln-m dash"/>
<text x="410" y="508" text-anchor="middle" class="t-cap">COST</text><text x="550" y="508" text-anchor="middle" class="t-cap">PRICE</text>''', 'A vending machine; the selling price bar sits below the cost bar.')


def ill_funnel():
    import random
    rnd = random.Random(7)
    dots = ''
    for i in range(26):
        x, y = rnd.randint(30, 300), rnd.randint(40, 380)
        dots += f'<circle cx="{x}" cy="{y}" r="{rnd.choice([10, 13, 16])}" class="{"f-coral" if i % 3 == 0 else "f-mut"}" opacity="{rnd.choice([.55, .8, 1])}"/>'
    m = uid('mk')
    return svg(700, 470, f'''<defs>{marker(m, 'mk-c', 3.4)}</defs>{dots}<path d="M340 30 L500 170 V250 L340 390 Z" class="bx-dash2"/>
<line x1="500" y1="210" x2="548" y2="210" class="ln-c thick" marker-end="url(#{m})"/>
<circle cx="620" cy="210" r="62" class="nd"/>{sicon('flask', 620, 210, 70)}<circle cx="664" cy="160" r="22" class="ok-dot"/><path d="M654 160 L661 167 L674 152" class="ok-tick sm"/>
<text x="165" y="440" text-anchor="middle" class="t-cap">HYPOTHESES</text><text x="620" y="320" text-anchor="middle" class="t-cap">TESTED</text>''', 'Many proposed hypotheses narrow to a few that researchers test in experiments.')


def matrix():
    hid = uid('hatch')
    art = f'''<defs><pattern id="{hid}" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="18" height="18" class="f-bg"/><rect width="5" height="18" class="f-bar"/></pattern></defs>
<rect x="100" y="20" width="340" height="230" rx="10" fill="url(#{hid})" class="bx-q"/><rect x="450" y="20" width="340" height="230" rx="10" fill="url(#{hid})" class="bx-q"/>
<rect x="100" y="260" width="340" height="230" rx="10" class="bx-good"/><rect x="450" y="260" width="340" height="230" rx="10" fill="url(#{hid})" class="bx-q"/>
<text x="270" y="384" text-anchor="middle" class="t-good">first trial</text>
<rect x="505" y="112" width="230" height="46" rx="23" class="f-bg"/><text x="620" y="144" text-anchor="middle" class="t-mut">poor start</text>
<path d="M100 516 H790" class="ln-t"/><path d="M76 490 V20" class="ln-t"/>
<text x="445" y="556" text-anchor="middle" class="t-cap">EASY → HARD TO JUDGE</text>
<text x="44" y="255" text-anchor="middle" class="t-cap" transform="rotate(-90 44 255)">EASY → HARD TO UNDO</text>'''
    return f'<div class="v-mx">' + svg(800, 570, art, 'Two-by-two grid: only tasks that are easy to judge and easy to undo make a good first trial.') + rows(('question', 'Hard to judge', 'You cannot tell whether the result is correct.'), ('warn', 'Hard to undo', 'A mistake would already have reached customers or changed records.')) + '</div>'


def boundaries():
    lim = ''.join(f'<li>{icon("cross")}{t}</li>' for t in ['installs', 'credentials', 'messages', 'publication'])
    return f'''<div class="v-bound"><div class="ws"><span class="kk">Workspace</span><p>Use a disposable copy of the demo files.</p>
<div class="act"><span class="kk">Actions</span><p>Allow this task’s edits and test commands.</p><div class="chips"><span>{icon('pencil')}edit</span><span>{icon('terminal')}test</span></div></div></div>
<div class="lim"><span class="kk">Limits</span><p>No installs, credentials, messages or publication.</p><ul>{lim}</ul></div></div>'''


def tool_call():
    m, m2 = uid('mk'), uid('mk')
    art = f'''<defs>{marker(m, 'mk-c', 3.4)}{marker(m2, 'mk-t', 3.4)}</defs>
<rect x="40" y="70" width="330" height="170" rx="24" class="f-ink"/><text x="205" y="138" text-anchor="middle" class="t-paper lg">Model</text><text x="205" y="186" text-anchor="middle" class="t-onmut">chooses</text>
<rect x="700" y="70" width="330" height="170" rx="24" class="bx-hot soft"/><text x="865" y="138" text-anchor="middle" class="t-strong lg">Harness</text><text x="865" y="186" text-anchor="middle" class="t-acc">executes</text>
<path d="M1370 60 H1560 L1620 120 V270 H1370 Z" class="bx-card"/><path d="M1560 60 V120 H1620" class="bx-card"/><text x="1400" y="112" class="t-strong mono">invoice.py</text>
<g class="f-coral"><rect x="1400" y="150" width="170" height="14" rx="7"/><rect x="1400" y="180" width="130" height="14" rx="7"/><rect x="1400" y="210" width="190" height="14" rx="7"/></g>
<line x1="380" y1="120" x2="686" y2="120" class="ln-c thick" marker-end="url(#{m})"/>
<rect x="416" y="60" width="238" height="40" rx="20" class="f-bg"/><text x="535" y="89" text-anchor="middle" class="t-strong mono">read invoice.py</text>
<line x1="1040" y1="160" x2="1356" y2="160" class="ln-c thick" marker-end="url(#{m})"/><text x="1198" y="140" text-anchor="middle" class="t-acc">opens</text>
<path d="M1495 280 C1495 360 205 360 205 254" class="ln-t thick" marker-end="url(#{m2})"/>
<rect x="690" y="318" width="360" height="44" rx="22" class="f-bg"/><text x="870" y="349" text-anchor="middle" class="t-strong">contents → evidence</text>
'''
    stops = ''.join(f'<div><span class="n">{i:02}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([('Request', 'Read invoice.py.'), ('Execution', 'The harness opens the file.'), ('Result', 'The model receives its contents.')], 1))
    return '<div class="v-seq">' + svg(1728, 380, art, 'The model requests a file read; the harness opens invoice.py; the contents return to the model.') + f'<div class="steps">{stops}</div></div>'


def code_explains():
    src = "def gross(net, tax_rate):\n    return Decimal(net).quantize(\n        Decimal('0.01'), rounding=ROUND_HALF_UP\n    )\n"
    body = pyhl(src).replace('tax_rate', '<u>tax_rate</u>', 1) + '\n<span class="flag"># tax_rate is accepted but never used</span>'
    return window('before/invoice.py · excerpt', body, 'term', 'v-editor')


def context_now():
    bands = ''.join(f'<div class="band">{icon(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in [('target', 'Task', 'The requested behaviour and boundaries.'), ('search', 'Evidence', 'The code, failures and relevant project rules.'), ('list', 'History', 'Earlier messages and results retained by the harness.')])
    m = uid('mk')
    arrow = svg(150, 60, f'<defs>{marker(m, "mk-c", 3)}</defs><line x1="6" y1="30" x2="130" y2="30" class="ln-c thick" marker-end="url(#{m})"/>', cls='io-arrow')
    return f'<div class="v-now"><div class="frame"><span class="cap">Context · what the model can use now</span>{bands}</div>{arrow}<div class="mdl">{icon("sparkle")}<b>Model</b></div></div>'


def ctx_panel(label, items):
    b = ''.join(f'<div class="{"u" if u else ""}" style="width:{w}%"></div>' for w, u in items)
    return f'<div class="v-ctxp"><span class="cap">{label}</span><div class="bars">{b}</div></div>'


def more_info():
    few = [(78, 1), (64, 1), (84, 1)]
    many = [(74, 0), (92, 0), (58, 0), (78, 1), (86, 0), (66, 0), (96, 0), (52, 0), (70, 1), (88, 0), (60, 0), (82, 1), (70, 0)]
    pan = f'<div class="v-two" role="img" aria-label="The same task, relevant files and evidence are easy to find in a small context and hard to find in a crowded one.">{ctx_panel("easy to find", few)}{ctx_panel("harder to find", many)}</div>'
    return p('Keep the task, relevant files and current evidence easy to find.') + f'<div class="v-more">{pan}' + callout('Watch the behaviour', 'Repeated mistakes or lost constraints are reasons to inspect the context.') + '</div>'


def handoff():
    m = uid('mk')
    blocks = ''.join(f'<rect x="{40+i*44}" y="130" width="38" height="70" rx="6" class="{"f-coral" if i in (2, 6, 9) else "f-bar"}"/>' for i in range(11))
    art = f'''<defs>{marker(m, 'mk-c', 3.4)}</defs><text x="40" y="112" class="t-cap">SESSION · LONG</text>{blocks}
<line x1="540" y1="165" x2="652" y2="165" class="ln-c thick" marker-end="url(#{m})"/>
<path d="M680 60 H920 L970 110 V270 H680 Z" class="bx-card"/><path d="M920 60 V110 H970" class="bx-card"/>
<text x="706" y="118" class="t-cap">decisions</text><text x="706" y="178" class="t-cap">files</text><text x="706" y="238" class="t-cap">remaining</text>
<g class="f-coral"><rect x="706" y="130" width="200" height="12" rx="6"/><rect x="706" y="190" width="160" height="12" rx="6"/><rect x="706" y="250" width="120" height="12" rx="6" opacity=".6"/></g>
<line x1="990" y1="165" x2="1172" y2="165" class="ln-c thick" marker-end="url(#{m})"/>
<text x="1196" y="112" class="t-cap">FRESH SESSION</text><rect x="1196" y="130" width="38" height="70" rx="6" class="f-coral"/><rect x="1240" y="130" width="38" height="70" rx="6" class="f-bar"/>
<rect x="1284" y="130" width="38" height="70" rx="6" class="bx-dash"/><rect x="1328" y="130" width="38" height="70" rx="6" class="bx-dash"/>
<circle cx="1540" cy="165" r="78" class="ok-dot"/><path d="M1504 167 L1530 193 L1578 139" class="ok-tick lg"/>'''
    steps = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in [('Summarise', 'Record decisions, files and remaining work.'), ('Restart', 'Start a fresh session from the note.'), ('Verify', 'Check that the note kept what matters.')])
    return '<div class="v-hand">' + svg(1728, 300, art, 'A long session is summarised into a note of decisions, files and remaining work; a fresh session starts from it and is verified.') + f'<div class="steps">{steps}</div></div>'


def thinking():
    ev = ''.join(icon(i) for i in ['diff', 'terminal', 'tick'])
    return f'''<div class="v-think"><div class="th th-a">{icon('cloud')}<h3>Useful for orientation</h3><p>It may explain a proposed approach or an uncertainty.</p></div>
<div class="neq" aria-hidden="true">≠</div><div class="th th-b"><div class="evs">{ev}</div><h3>Evidence of the result</h3><p>Check the changed file, the command output and the test results.</p></div></div>'''


def diff_view():
    rows_ = [('del', '-', "total = Decimal(net)", 'before'), ('add', '+', "total = Decimal(net) * (Decimal('1') + Decimal(<b>tax_rate</b>))", 'after'), ('ctx', ' ', '', ''), ('ctx', ' ', '<span class="c"># Keep the final two-decimal rounding.</span>', '')]
    body = ''.join(f'<div class="dl {k}"><span class="g">{g}</span><span class="tx">{t if "<" in t else esc(t)}</span><span class="tg">{tag}</span></div>' for k, g, t, tag in rows_)
    return window('conceptual change · invoice.py', body, 'term', 'v-diff')


def test_cards():
    out = ''.join(f'<div class="tc"><span class="kk">case</span><div class="cs">{c}</div><span class="kk">expected result</span><div class="ex">{e}</div>{icon("tick")}</div>' for c, e in [('100 at 0.21', '121.00'), ('100 at 0', '100.00'), ('0.50 at 0.21', '0.61')])
    return f'<div class="v-tests">{out}</div>' + p('The three invoice tests pass on the reference fix.')


def review_list():
    return rows(('diff', 'Diff', 'Does the change match the requested behaviour?'), ('terminal', 'Checks', 'Did the tests run, and are they unchanged?'), ('target', 'Scope', 'Did anything unrelated change?'), cls='checklist')


def interrupt():
    m, m2 = uid('mk'), uid('mk')
    s1 = f'''<path d="M20 200 H180 C260 200 300 150 360 80" class="ln-c thick"/><path d="M360 80 L420 20" class="ln-m dash"/><path d="M180 200 H500" class="ln-dim dash"/>
{sicon('stop', 380, 70, 96, 'stp')}'''
    s2 = f'''<path d="M20 200 H180 C260 200 300 150 360 80" class="ln-m"/><circle cx="190" cy="200" r="30" class="ring-c"/>{sicon('search', 250, 110, 120)}<path d="M180 200 H500" class="ln-dim dash"/>'''
    s3 = f'''<defs>{marker(m, 'mk-c', 3.4)}</defs><path d="M20 200 H180" class="ln-m"/><path d="M180 200 C280 200 300 200 420 200" class="ln-c thick" marker-end="url(#{m})"/>{sicon('target', 470, 200, 80)}<circle cx="180" cy="200" r="12" class="f-coral"/>'''
    cells = ''.join(f'<div class="ir">{svg(520, 260, s, lab)}<h3>{t}</h3><p>{d}</p></div>' for s, t, d, lab in [
        (s1, 'Stop', 'Pause changes outside the task.', 'A run veers off course and is stopped.'),
        (s2, 'Inspect', 'Find the first wrong assumption.', 'Look back at the point where the run first went wrong.'),
        (s3, 'Redirect', 'Supply the missing fact or narrow the task.', 'Restart from that point towards the target.')])
    return f'<div class="v-int">{cells}</div>'


def rules_file():
    body = '<span class="h"># Project instructions</span>\n- Tests: <b>python3 -m unittest -v</b>\n- Use Decimal for invoice calculations.\n- Preserve tests and keep edits within the task.\n- Ask before installing dependencies.'
    m = uid('mk')
    ses = ''.join(f'<rect x="140" y="{30+i*120}" width="300" height="84" rx="42" class="{"bx-hot soft" if i == 2 else "bx-card"}"/><text x="290" y="{82+i*120}" text-anchor="middle" class="t-strong">session {i+1}</text><path d="M20 {72+i*120} H126" class="ln-c" marker-end="url(#{m})"/>' for i in range(3))
    art = f'<defs>{marker(m, "mk-c", 3.4)}</defs><path d="M20 40 V312" class="ln-c thick"/>{ses}'
    return f'<div class="v-rules">{window("instructions file", body, "paper", "v-brief md")}<div class="rs"><span class="kk">Loaded again</span>{svg(460, 360, art, "The same instructions file is loaded by session 1, 2 and 3.")}</div></div>'


def ill_rules(skill):
    m = uid('mk')
    tasks = ''
    for i in range(3):
        y = 30 + i * 90
        on = (not skill) or i == 1
        tasks += f'<rect x="460" y="{y}" width="220" height="66" rx="14" class="{"bx-hot soft" if on else "bx-dash"}"/><text x="570" y="{y+42}" text-anchor="middle" class="{"t-strong" if on else "t-faint"}">{"relevant task" if skill and i == 1 else "task"}</text>'
        if on:
            tasks += f'<path d="M250 {140} C350 140 350 {y+33} 446 {y+33}" class="ln-c" marker-end="url(#{m})"/>'
    ic = 'book' if skill else 'pin'
    return svg(700, 280, f'<defs>{marker(m, "mk-c", 3.4)}</defs><rect x="20" y="60" width="230" height="160" rx="18" class="f-ink"/>{sicon(ic, 135, 140, 90, "inv")}{tasks}')


def reach():
    return f'''<div class="v-reach"><div class="zone in"><span class="kk">This repo</span>{icon('codefile')}<h3>Local tool</h3><p>Read files or run tests.</p></div>
<div class="gate"><div class="lockc">{icon('lock')}</div><h3>Permission</h3><p>Allow only the access this task needs.</p></div>
<div class="zone out"><span class="kk">Outside</span>{icon('globe')}<h3>Connected tool</h3><p>Query another system through an API, CLI or MCP server.</p></div></div>'''


def one_agent():
    return (p('Use an interface you can inspect: its changes, commands, permissions and results.') +
            f'''<div class="v-one"><div class="ex"><span class="kk">Examples</span><p>Claude Code or Codex, in the interface your team supports.</p><div class="chips"><span>{icon('terminal')}Claude Code</span><span>{icon('terminal')}Codex</span></div></div>
<div class="q"><span class="kk">First decision</span><p>Can it do this task within the access you are willing to grant?</p>{icon('question')}</div></div>''')


def demo_vs_repeat():
    m = uid('mk')
    one = f'''<defs>{marker(m, 'mk-c', 3.4)}</defs><rect x="40" y="95" width="300" height="80" rx="16" class="bx-mid"/><text x="190" y="145" text-anchor="middle" class="t-strong">one task</text>
<line x1="352" y1="135" x2="500" y2="135" class="ln-c thick" marker-end="url(#{m})"/><circle cx="580" cy="135" r="56" class="ok-dot"/><path d="M552 137 L572 157 L610 113" class="ok-tick lg"/>'''
    marks = ['ok', 'x', 'ok', 'part', 'ok', 'x']
    runs = ''
    for i, k in enumerate(marks):
        y = 18 + i * 42
        w = [300, 240, 330, 200, 280, 250][i]
        runs += f'<rect x="40" y="{y}" width="{w}" height="30" rx="8" class="f-bar"/>'
        cx = w + 80
        if k == 'ok':
            runs += f'<circle cx="{cx}" cy="{y+15}" r="15" class="ok-dot"/>'
        elif k == 'x':
            runs += f'<circle cx="{cx}" cy="{y+15}" r="15" class="f-coral"/>'
        else:
            runs += f'<circle cx="{cx}" cy="{y+15}" r="15" class="ring-c"/><path d="M{cx} {y} A15 15 0 0 1 {cx} {y+30} Z" class="f-coral"/>'
    many = runs + f'{sicon("clock", 600, 135, 110)}<text x="600" y="232" text-anchor="middle" class="t-cap">REVIEW TIME</text>'
    return panels((svg(700, 270, one, 'One task, one inspected result.'), 'In the demo', 'One task, a few files and a result you can inspect.'),
                  (svg(700, 270, many, 'Repeated runs with varying outcomes: passes, failures and partial results, plus review time.'), 'In repeated work', 'Changing inputs, partial failures, review time and uncertain outcomes.'), cls='wide')


def csv_hero():
    q = lambda t: f'<span class="hq">{esc(t)}</span>'
    body = ('<span class="dim">invoice_id,customer,net,tax_rate,gross</span>\n'
            f'INV-001,{q(chr(34) + "North, Ltd" + chr(34))},100.00,0.21,<span class="s">121.00</span>\n'
            f'INV-002,{q(chr(34) + "Studio " + chr(34) * 2 + "A" + chr(34) * 3)},0.50,0.21,<span class="s">0.61</span>')
    return p('Add CSV export to the invoice calculation from talk 02.') + window('invoices.csv · excerpt', body, 'term', 'v-csv')


def unspecified():
    rows_ = ''.join(f'<div class="fr"><span>{t}</span><i>?</i></div>' for t in ['columns', 'rounding', 'quoting', 'empty input'])
    return f'<div class="v-spec"><div class="sh">“Add export”</div><span class="kk">Unspecified</span><div class="fields">{rows_}</div><p class="sub">Columns, rounding, quoting and empty input.</p></div>'


def contract():
    rs = [('Five named columns, input order preserved', 'Read the exported rows back'), ('Use the existing calculation rule', 'Check known totals and rounding'), ('Commas, quotes and newlines survive', 'Round-trip special customer names'), ('Empty input still has a header', 'Export an empty collection')]
    body = ''.join(f'<div class="cr"><span class="no">{i:02}</span><p class="rq">{a}</p><svg viewBox="0 0 80 40" class="ar" aria-hidden="true"><path d="M4 20 H66 M52 8 L68 20 L52 32"/></svg><p class="ck">{icon("tick")}{b}</p></div>' for i, (a, b) in enumerate(rs, 1))
    return f'<div class="v-contract"><div class="hd"><span>Requirement</span><span>Observable check</span></div>{body}</div>'


def structure():
    m = uid('mk')
    direct = f'<defs>{marker(m, "mk-c", 3.4)}</defs><circle cx="60" cy="80" r="26" class="f-ink2"/><line x1="96" y1="80" x2="330" y2="80" class="ln-c thick" marker-end="url(#{m})"/><circle cx="380" cy="80" r="32" class="ok-dot"/><path d="M364 81 L376 93 L398 67" class="ok-tick"/>'
    wf = ''.join(f'<rect x="{10+i*108}" y="56" width="72" height="48" rx="10" class="bx-mid"/>' + (f'<rect x="{88+i*108}" y="40" width="8" height="80" rx="4" class="f-coral"/>' if i < 3 else '') for i in range(4))
    ex = f'''<circle cx="40" cy="80" r="16" class="f-ink2"/><path d="M56 80 C110 80 110 30 170 30 H230" class="ln-m"/><path d="M56 80 H200 C250 80 250 130 300 130" class="ln-m"/>
<path d="M200 80 C260 80 270 70 340 70" class="ln-c thick"/><path d="M170 30 C200 30 210 14 240 14" class="ln-m"/>
<g class="xmark"><path d="M232 22 L248 38 M248 22 L232 38"/><path d="M302 122 L318 138 M318 122 L302 138"/><path d="M244 6 L256 18 M256 6 L244 18"/></g>{sicon('target', 380, 70, 60)}'''
    tiles = ''.join(f'<div class="v-tile">{svg(440, 160, a)}<h3>{t}</h3><p>{d}</p></div>' for a, t, d in [(direct, 'Direct change', 'A small, clear edit with a simple check.'), (wf, 'Workflow', 'Known stages and acceptance gates.'), (ex, 'Agent exploration', 'The next useful step depends on what it finds.')])
    return f'<div class="v-tiles n3 diag">{tiles}</div>'


def exit_zero():
    ch = ''.join(f'<span>{icon("question")}{t}</span>' for t in ['wrong tests', 'skipped case', 'weaker requirement'])
    return window('checks', '<span class="dim">exit code:</span> <span class="zero">0</span>', 'term', 'v-zero') + f'<div class="v-qs">{ch}</div>'


def claim_check():
    ev = '<div class="cmp"><code>"North, Ltd"</code><span>=</span><code>"North, Ltd"</code>' + icon('tick') + '</div>'
    def arrow():
        m = uid('mk')
        return svg(90, 60, f'<defs>{marker(m, "mk-c", 3)}</defs><line x1="4" y1="30" x2="74" y2="30" class="ln-c thick" marker-end="url(#{m})"/>', cls='io-arrow')
    return f'''<div class="v-claim"><div class="c1"><span class="q" aria-hidden="true">“</span><h3>Claim</h3><p>Customer names survive export.</p></div>{arrow()}
<div class="c1"><h3>Evidence</h3>{ev}<p>Parse the CSV and compare the original strings.</p></div>{arrow()}
<div class="c1 bnd">{icon('sheet')}<h3>Boundary</h3><p>This does not check every spreadsheet’s interpretation.</p></div></div>'''


def calc_code():
    src = "total = Decimal(net) * (Decimal('1') + Decimal(tax_rate))\nreturn total.quantize(\n    Decimal('0.01'), rounding=ROUND_HALF_UP\n)"
    body = pyhl(src).replace('ROUND_HALF_UP', '<mark>ROUND_HALF_UP</mark>')
    return window('invoice.py · reference fix', body, 'term', 'v-editor calc') + '<div class="v-anno">' + icon('tick') + '<span>explicit rounding rule · verify against it</span></div>'


def tests_and_artifact():
    tests = ['test_empty_input_still_has_header', 'test_roundtrip_special_characters_and_totals', 'test_round_once_half_up', 'test_supplied_rate', 'test_zero_rate']
    lines = ''.join(f'{t} <span class="dim">...</span> <span class="ok">ok</span>\n' for t in tests)
    term = window('after/ · excerpt', f'<span class="p">$</span> python3 -m unittest -v\n{lines}\n<span class="dim">Ran 5 tests</span>  <span class="okb">OK</span>', 'term', 'v-okterm')
    rows_ = ['invoice_id,customer,net,tax_rate,gross', 'INV-001,"North, Ltd",100.00,0.21,121.00', '<span class="hl">INV-002,"Studio ""A""",<u>0.50</u>,<u>0.21</u>,<u>0.61</u></span>', 'INV-003,"Line', 'break",100.00,0,100.00']
    body = '\n'.join(r if r.startswith('<') else esc(r) for r in rows_)
    art = window('invoices.csv', body, 'term', 'v-csvwin') + f'<div class="v-bycheck">{icon("tick")}<span>0.50 × 1.21 = 0.605 → <b>0.61</b> (half up)</span></div>'
    return f'<div class="v-ta"><div>{term}</div><div class="v-tr">{art}</div></div>' + p('Match each test to a contract line. Then open the file and recompute one total.', 'sm')


def two_actor():
    chips = ''.join(f'<span>{t}</span>' for t in ['patch', 'commands run', 'output', 'unresolved questions'])
    m = uid('mk')
    arrow = svg(200, 120, f'<defs>{marker(m, "mk-c", 3)}</defs><line x1="10" y1="70" x2="176" y2="70" class="ln-c thick" marker-end="url(#{m})"/><text x="93" y="44" text-anchor="middle" class="t-acc">evidence</text>', cls='io-arrow big')
    return f'''<div class="v-actors"><div class="actor ag">{icon('agent')}<h3>Agent produces</h3><p>The patch, commands run, output and unresolved questions.</p><div class="chips">{chips}</div></div>{arrow}
<div class="actor rv">{icon('person')}<h3>Reviewer decides</h3><p>Whether the evidence meets the contract and the change is ready.</p><div class="gate">{icon('tick')}{icon('restore')}</div></div></div>'''


def stage_context():
    cols = [('Inspect', ['entry points', 'failing case', 'repository map']), ('Build', ['contract', 'target files', 'project rules']), ('Verify', ['contract', 'patch', 'independent checks']), ('Review', ['evidence', 'risks', 'unresolved questions'])]
    out = ''.join(f'<div class="sc"><h3>{t}</h3>' + ''.join(f'<span class="{"hot" if c == "contract" else ""}">{c}</span>' for c in cs) + '</div>' for t, cs in cols)
    return f'<div class="v-stages" role="img" aria-label="Useful inputs per stage. Inspect: entry points, failing case and repository map. Build: contract, target files and project rules. Verify: contract, patch and independent checks. Review: evidence, risks and unresolved questions."><div class="k">Stage · useful inputs</div>{out}</div>'


def handoff_note():
    kv = [('Task', 'add invoice CSV export.'), ('Rule', 'apply supplied rate; round once, half up.'), ('Files', 'invoice.py, export.py, test_export.py.'), ('Done', 'quoting and empty-input cases pass.'), ('Open', 'production input validation is out of scope.'), ('Next', 'inspect the diff and exported sample.')]
    body = ''.join(f'<div class="kv"><b>{k}:</b><span>{esc(v)}</span></div>' for k, v in kv)
    return window('handoff note', body, 'paper', 'v-note')


def budget():
    m = uid('mk')
    segs = ''
    x = 0
    for i, w in enumerate([210, 190, 170]):
        segs += f'<rect x="{x+2}" y="70" width="{w-6}" height="90" rx="10" class="f-coral" opacity="{[1, .75, .5][i]}"/><text x="{x+w/2}" y="124" text-anchor="middle" class="t-on">try {i+1}</text>'
        x += w
    art = f'''<text x="0" y="40" class="t-cap">BUDGET</text><rect x="2" y="70" width="716" height="90" rx="10" class="bx-dash"/>{segs}
<line x1="640" y1="44" x2="640" y2="186" class="ln-stop"/><text x="640" y="224" text-anchor="middle" class="t-acc">limit</text>'''
    qs = rows(('search', 'Inspect', 'What failed?'), ('redirect', 'Change', 'What new evidence or approach will help?'), ('stop', 'Stop', 'What limit ends the run?'), cls='compact')
    return svg(720, 240, art, 'Three attempts consume most of the budget before the limit.') + qs


def retry_tree():
    rs = [('loop', 'Transient tool error', 'Retry within a small explicit limit'), ('search', 'Same failed check again', 'Inspect cause; require a changed approach'), ('pause', 'Missing access or requirement', 'Pause for the owner'), ('stop', 'Time or cost budget reached', 'Stop and return partial work with evidence')]
    body = ''.join(f'<div class="tr"><p class="f">{a}</p><svg viewBox="0 0 80 40" class="ar" aria-hidden="true"><path d="M4 20 H66 M52 8 L68 20 L52 32"/></svg><div class="nx">{icon(i)}<p>{b}</p></div></div>' for i, a, b in rs)
    return f'<div class="v-tree"><div class="root">{icon("warn")}<span>Failure</span></div><div class="branches"><div class="hd"><span>Failure</span><span>Next step</span></div>{body}</div></div>'


def recovery():
    m, m2 = uid('mk'), uid('mk')
    art = f'''<defs>{marker(m, 'mk-c', 3.4)}{marker(m2, 'mk-t', 3.4)}</defs>
<line x1="80" y1="170" x2="1300" y2="170" class="ln-t thick"/>{sicon('flag', 90, 110, 100)}
<g class="cp"><path d="M560 146 L584 170 L560 194 L536 170 Z"/><path d="M780 146 L804 170 L780 194 L756 170 Z"/><path d="M1000 146 L1024 170 L1000 194 L976 170 Z"/></g>
<circle cx="1300" cy="170" r="46" class="f-coral"/><path d="M1282 152 L1318 188 M1318 152 L1282 188" class="x-inv"/>
<path d="M1350 150 C1440 110 1520 100 1650 100" class="ln-c thick" marker-end="url(#{m})"/><text x="1660" y="84" text-anchor="end" class="t-acc">resume</text>
<path d="M1300 222 C1260 300 1080 300 1010 206" class="ln-t dash" marker-end="url(#{m2})"/><text x="1160" y="318" text-anchor="middle" class="t-mut">restore</text>
<text x="90" y="236" text-anchor="middle" class="t-cap">BASELINE</text><text x="780" y="236" text-anchor="middle" class="t-cap">CHECKPOINTS</text>'''
    steps = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in [('Before', 'Record the baseline and isolate the work.'), ('During', 'Keep edits scoped and checkpoints understandable.'), ('After failure', 'Inspect the partial diff; resume or restore deliberately.')])
    return '<div class="v-rec">' + svg(1728, 330, art, 'Timeline: a recorded baseline, understandable checkpoints, a failure, then either resume or restore to a checkpoint.') + f'<div class="steps">{steps}</div></div>'


def fraction():
    chips = ''.join(f'<span>{t}</span>' for t in ['attempts', 'tool use', 'model charges', 'review time'])
    return f'''<div class="v-frac" role="img" aria-label="Cost of the task, including attempts, tool use, model charges and review time, divided by accepted results."><div class="num"><span class="kk">Count the task</span><p>Attempts, tool use, model charges and review time.</p><div class="chips">{chips}</div></div>
<div class="bar"><span>÷</span></div><div class="den"><span class="kk">Count accepted results</span><p>How many met the same quality bar?</p></div></div>'''


def delegate():
    lines = [('Task:', 'review CSV quoting and empty-input behaviour.'), ('Read:', 'export.py and test_export.py.'), ('', 'Do not edit files.'), ('Return:', 'finding, file reference and reproducing input.'), ('', 'State what you did not check.')]
    body = ''.join(f'<div class="ln{" lk" if not k and "edit" in v else ""}"><span class="tx">{"<b>" + k + "</b> " if k else ""}{esc(v)}</span>{icon("lock") if not k and "edit" in v else ""}</div>' for k, v in lines)
    m, m2 = uid('mk'), uid('mk')
    art = f'''<defs>{marker(m, 'mk-c', 3.4)}{marker(m2, 'mk-t', 3.4)}</defs>{node(90, 90, 70, 'agent')}{node(90, 330, 70, 'search', 'nd soft')}
<text x="180" y="98" class="t-strong">lead</text><text x="180" y="338" class="t-strong">reviewer</text><text x="180" y="376" class="t-mut sm">read-only</text>
<path d="M70 166 V250" class="ln-c thick" marker-end="url(#{m})"/><path d="M112 252 V168" class="ln-t thick" marker-end="url(#{m2})"/>
<text x="130" y="200" class="t-acc sm">brief</text><text x="130" y="232" class="t-mut sm">evidence back</text>'''
    return f'<div class="v-deleg">{window("reviewer brief", body, "paper", "v-brief dl")}' + svg(420, 420, art, 'The lead sends a brief to a read-only reviewer, which returns evidence.') + '</div>'


def fan_in():
    m = uid('mk')
    art = f'<defs>{marker(m, "mk-c", 3.4)}</defs>' + ''.join(f'<rect x="4" y="{8+i*104}" width="280" height="84" rx="16" class="bx-mid"/>{sicon("agent", 56, 50+i*104, 56)}<text x="98" y="{61+i*104}" class="t-strong">worker</text><path d="M290 {50+i*104} C370 {50+i*104} 370 154 450 154" class="ln-c thick" marker-end="url(#{m})"/>' for i in range(3))
    items = ''.join(f'<div class="fi{" hot" if h else ""}">{icon(ic)}<h3>{t}</h3><p>{d}</p></div>' for ic, t, d, h in [('merge', 'Integrator', 'Resolves conflicts and checks the combined result.', 1), ('person', 'Reviewer', 'Accepts the final change against the contract.', 0)])
    return f'<div class="v-fan"><div class="wk">{svg(470, 310, art, "Three workers feed one integrator.")}<h3>Workers</h3><p>Own separate scopes and return evidence.</p></div>{items}</div>'


def procedure():
    steps = ['Read the export contract.', 'Run invoice and CSV tests.', 'Inspect the diff and exported sample.', 'Report evidence and remaining gaps.', 'Leave acceptance to the reviewer.']
    li = ''.join(f'<li class="{"own" if i == 5 else ""}"><span>{i}.</span>{s}{icon("person") if i == 5 else ""}</li>' for i, s in enumerate(steps, 1))
    return window('skill · procedure', f'<div class="h"># Invoice export review</div><ol>{li}</ol>', 'paper', 'v-skill')


def way_back():
    m, m2 = uid('mk'), uid('mk')
    xs = [216, 648, 1080, 1512]
    names = ['Contract', 'Build', 'Verify', 'Review']
    icons_ = ['doc', 'code', 'tick', 'person']
    cy = 190
    art = f'<defs>{marker(m, "mk-c", 3.4)}{marker(m2, "mk-t", 3.4)}</defs><line x1="216" y1="{cy}" x2="1512" y2="{cy}" class="ln-c xthick"/>'
    art += f'<path d="M1080 {cy+114} C1080 390 648 390 648 {cy+120}" class="ln-c dash thick" marker-end="url(#{m})"/>'
    art += f'<path d="M648 {cy-114} C648 14 216 14 216 {cy-120}" class="ln-t dash thick" marker-end="url(#{m2})"/>'
    for x, ic in zip(xs, icons_):
        art += node(x, cy, 110, ic, 'nd')
    art += '<rect x="594" y="342" width="540" height="48" rx="24" class="f-bg"/><text x="864" y="375" text-anchor="middle" class="t-acc">Failed check: diagnose within budget.</text>'
    art += '<rect x="166" y="10" width="532" height="48" rx="24" class="f-bg"/><text x="432" y="43" text-anchor="middle" class="t-strong mono">Missing requirement: ask the owner.</text>'
    stops = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in [('Contract', 'Agree on the check.'), ('Build', 'Make a scoped change.'), ('Verify', 'Return evidence.'), ('Review', 'Accept or return it.')])
    return '<div class="v-stn n4 v-way">' + svg(1728, 400, art, 'Contract, build, verify, review. A failed check returns to build within budget; a missing requirement goes back to the owner at the contract stage.', 'rail') + f'<div class="stops">{stops}</div></div>'


def deck_cards():
    # WIP status as of September 2026; keep in step with the decks themselves.
    items = [('04', 'Subagents &amp; prompt caching', 'subagents-prompt-caching.html', False), ('05', 'Cost &amp; context', 'cost-and-context.html', True), ('06', 'Orchestrating agents', 'orchestrating-agents.html', True), ('07', 'Measuring what works', 'measuring-what-works.html', True), ('08', 'Claude Design', 'claude-design.html', True), ('09', 'AI graph engineering', 'ai-graph-engineering.html', False)]
    out = ''.join(f'<a class="dk" href="{u}" target="_blank" rel="noopener"><span class="no">{n}<span class="sep"> · </span></span><span class="lt">{t}{" <span class=wip>WIP</span>" if w else ""}</span><span class="ld">{u} <b aria-hidden="true">↗</b></span></a>' for n, t, u, w in items)
    return f'<div class="v-decks">{out}</div>'


# TALK 01: choose a tool by the work and the evidence it returns.
TOOLBOX = [
 title('The AI<br>Toolbox', 'Find a useful tool. Check the work it returns.', '01 · No coding needed · v2', 'Promise a practical way to choose a tool and check what it gives back. There is no market tour. One ordinary review task runs through the whole talk.'),
 slide('Start with a task you already do', io_task(), 'Ask everyone to pick a recurring task they know well enough to review; they will come back to it at the end. Our example uses synthetic data. It is not a customer case, and no particular product produced it.', '2, 21–23', 'One real task'),
 slide('The draft: a number to check and a gap to flag', report(), 'Show the report before you name any vendor. April has 80 completed orders, May 120, and June is missing. The 50% compares two complete months and says nothing about the quarter. We wrote this report for the talk and anyone can download it; it is not a screenshot of a vendor run.', '23 → new artifact', 'One real task', foot='<a href="examples/v2/review-report.html" target="_blank" rel="noopener">Open the report</a> · <a href="examples/v2/review-data.csv" download>Download its CSV</a>'),
 slide('A useful brief names the checks', brief_window(['Use the CSV and last month’s structure.', 'Show where each number came from.', 'Flag missing data; do not estimate it.', 'Keep the draft to one page.', 'Save a new file for me to review.'], {2, 3}), 'A brief shapes the output but cannot make the tool follow it, so you still inspect the result. Point to lines 2 and 3: they ask for the evidence you will check. If there is time, open the CSV and show the blank June value.', '23, 25', 'One real task'),
 slide('Check it before you share it', stations([('Trace', 'Do the numbers match the source?'), ('Inspect', 'Are gaps and assumptions visible?'), ('Decide', 'What is ready to share?')], ['trace', 'search', 'decide']), 'For our report: recompute 120 divided by 80, minus one. Confirm June is missing. Then decide whether an April–May interim report is what was asked for. A polished chart can still answer the wrong question.', '24–25, 39', 'One real task', dark=True),
 slide('Some tools answer. Others take steps.', chat_vs_agent(), 'Use this as a rough distinction; plenty of products do both. Chat apps can include agent features, and an agent may still stop to ask a question or wait for your approval.', '5–6', 'What changed'),
 slide('An agent works in a loop', cycle([('Choose', 'Pick the next useful action.'), ('Act', 'A tool reads or changes something.'), ('Check', 'Use the result to decide what follows.')], ['decide', 'gear', 'search'], 'A loop: choose the next action, act with a tool, check the result, repeat until stopping.', 'stop'), 'For our report, the loop reads the CSV, calculates the comparison, writes the draft and inspects it. It also needs a point where it stops. Many image and voice generators run a single step; an agent might call one as a tool inside a larger task.', '6–9', 'What changed'),
 slide('Your files supply the context', context_supply(), 'Context is the information the tool can use while it produces an answer. Products handle earlier conversation differently: some resend it, some summarise it, some retrieve parts of it. So avoid saying they all resend everything. The practical question for the room is what this tool can see.', '7–8', 'What changed'),
 slide('Choose by the job', cards(('Documents', 'Draft, compare, summarise and present.'), ('Media', 'Create images, audio or short video.'), ('Actions', 'Build a small app or connect repeated steps.'), icons=['doc', 'media', 'actions'], cls='jobs'), 'The rest of the talk follows these three jobs. Research sits under documents because what it produces is evidence to inspect. The products named are examples of each category; we are not ranking them.', '27, 40', 'The toolbox', dark=True),
 slide('Start with an assistant you can use at work', cards(('Claude', 'Work with source files and draft an output.'), ('ChatGPT', 'Explore a question, analyse data and make a draft.'), ('Gemini', 'Use an assistant alongside your Google work.'), icons=['doc', 'report', 'panel']), 'Three general assistants as examples. The right one is usually whichever your organisation has approved, with the integrations and limits that come with it. Plans differ in what they include. Current links are in the handout.', '11–19 → compressed', 'Documents'),
 slide('Document work has two different needs', panels((ill_sources(), 'Understand the sources', 'Gemini Notebook: explore supplied material and listen to an Audio Overview.'), (ill_present(), 'Present the material', 'Gamma or Canva: turn an outline into a presentation you can edit.')), 'Some people still know Gemini Notebook as NotebookLM; Google renamed it in July 2026, and the old links still work. A sourced summary and a designed deck are different outputs. Check where a claim came from before you spend time on its layout. An Audio Overview can contain errors, so use it to get oriented and then go back to the source.', '17, 24, 35, 37', 'Documents'),
 slide('Check one important claim all the way back', claim_chain(), 'A citation tells you where to look; it does not prove the claim. Read enough around the cited passage to check its scope and date. If the source is missing, will not open or does not support the claim, mark the claim unresolved.', '24, 37', 'Research', dark=True),
 slide('For media, decide what must stay exact', panels((ill_explore(), 'Explore a look', 'Generate alternatives for an image or a short scene.'), (ill_template(), 'Keep a template', 'Use fixed layouts for labels, numbers and repeated versions.')), 'Generating new looks and filling a fixed template are different jobs. Check brand colours and text in both. Rendering from code keeps a layout fixed; it cannot tell you the brand rules were followed.', '29–34', 'Media'),
 slide('An agent wrote this animation as code', video('agent-loop-dark', 'The agent loop animation: an agent wrote the code, the code draws every frame, and a person checked the result.', steps=['The code draws every frame', 'It is saved alongside these slides', 'Change a word and render again', 'A person still checked the result']), 'Play it. An agent wrote this animation as code, using a tool called Remotion that turns code into video. Because it is code, fixing a label or the timing means editing a line and rendering a fresh copy; nobody redraws it by hand. Writing it did not make it right, so someone still watched it before it went into these slides. Narration is a separate job, with text-to-speech tools such as ElevenLabs: check the pronunciation and get permission before cloning anyone’s voice.', '30–32 → actual repository artifact', 'Media', dark=True),
 slide('An app draft still needs an owner', app_owner(), 'An app is software that runs, whoever built it. Build the prototype on synthetic data. A working demo tells you nothing about security, correctness or who will maintain it.', '28', 'Apps'),
 slide('Automate the repeatable part', stations([('Trigger', 'A new report arrives.'), ('Draft', 'Summarise the changes.'), ('Review', 'A person approves the message.')], ['mail', 'sparkle', 'person'], hot=(2,)), 'An illustrative workflow; we have not deployed it. Tools such as Zapier connect the steps. If a fixed rule can route the report, use the rule and save AI for the step that has to read and interpret the content.', '38, 54', 'Automation'),
 slide('Three ways to give it your work', cards(('Upload', 'Give the assistant selected files.'), ('Connect', 'Let it reach an approved data source.'), ('Work in the app', 'Use an assistant beside the document.'), icons=['upload', 'link', 'panel']), 'Back to the review report: upload the CSV, connect the source it comes from, or work inside the spreadsheet. Each route gives the assistant a different amount of access. Pick the smallest one that covers the task.', '47–55 → compressed', 'Access'),
 slide('A connection grants access', access_scope(), 'If someone asks about MCP: it is one standard for connecting assistants to tools and data. Connecting through it does not grant permission to everything on the other side. This audience needs the access decision; leave protocol details to talk 02.', '48–49', 'Access', dark=True),
 slide('Check your existing tools first', cards(('Microsoft 365', 'Copilot in Word, Excel, Outlook and Teams, if your licence includes it.'), ('Google Workspace', 'Gemini in Gmail, Docs and Sheets, if your administrator has turned it on.'), icons=['suite', 'panel']), 'Microsoft 365 Copilot and Gemini in Workspace are the examples. What you get depends on your licence and your administrator’s settings, so check your own account before anyone buys another subscription. Keep prices out of this slide.', '50–55', 'Access'),
 slide('Budget for attempts and review', '<div class="v-legend"><span>What you pay for</span><span>What to check</span></div>' + rows(('card', 'Subscription', '<span class="kk">check</span> Usage limits and required features'), ('coins', 'Credits', '<span class="kk">check</span> How many attempts one usable result takes'), ('team', 'Team access', '<span class="kk">check</span> Seats, admin controls and data settings'), ('clock', 'Your time', '<span class="kk">check</span> Review, corrections and rework'), cls='grid2 budget'), 'The same monthly fee buys different things from different suppliers, so ask what your plan includes. Compare what one usable result costs, review time included; the headline fee tells you less.', '4, 18–19, 39', 'Cost'),
 slide('A shop agent took real actions and lost money', story([('What happened', 'In Project Vend, an AI agent running a small office shop found suppliers and changed its stock. It also sold items below cost.'), ('What to learn', 'Judge an agent by the business result as well as the steps it completed.')], ill_vend()), 'From the first Project Vend report by Anthropic and Andon Labs, June 2025. The agent also invented payment details. Say it lost money, not that it went bankrupt, and present it as one experiment rather than a picture of every agent deployment. The second report, in December 2025, found that newer models and better tools largely ended the losing weeks, yet staff could still manipulate the agent into poor decisions, so the lesson holds.', '42', 'Two useful stories', dark=True, foot='<a href="https://www.anthropic.com/research/project-vend-1" target="_blank" rel="noopener">Source: Anthropic &amp; Andon Labs · June 2025</a>'),
 slide('Research ideas still need experiments', story([('What happened', 'Google’s AI co-scientist proposed hypotheses that researchers assessed and tested.'), ('What to learn', 'Use AI to widen the search. Keep the evidence standard for the conclusion.')], ill_funnel()), 'Google Research, February 2025. The system helped researchers generate and refine hypotheses, and laboratory experiments still did the validating. A hypothesis proposed in days does not replace years of experiments.', '43', 'Two useful stories', foot='<a href="https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/" target="_blank" rel="noopener">Source: Google Research · February 2025</a>'),
 slide('Some tasks are poor starting points', matrix(), 'This rule is for a first trial: pick a familiar draft task where a person checks the result. A specialised production system can handle harder cases, but buying one is a separate decision from trying a general assistant.', '25, 39, 45', 'Choose a first task'),
 slide('Try one familiar task this week', stations([('Choose', 'A small job you can review.'), ('Brief', 'Give sources, an example and a check.'), ('Compare', 'Was the result useful after corrections?')], ['target', 'brief', 'scale']), 'Bring back the task everyone picked at the start. Count the whole effort, review included. If corrections eat the time you saved, stop or switch tools. One product is enough to start with.', '56–57 → one close', 'Your next step', dark=True, cls='beat'),
 slide('Take these with you', linkcards(('Tool selection handout', 'reviews/first-three-v2/TOOLBOX-HANDOUT.md', 'book', 'Handout'), ('Example report', 'examples/v2/review-report.html', 'report', 'Artifact'), ('Next: use an agent on a bounded task', 'agentic-ai-v2.html', 'agent', 'Talk 02')), 'Take questions here. The next three slides are reference links for later. The handout covers more tools than the talk had room for.', '40, 55–57', 'Questions'),
 slide('Reference · document tools', links(('Claude', 'https://claude.com/product/overview'), ('ChatGPT', 'https://chatgpt.com/overview/'), ('Gemini', 'https://gemini.google/overview/'), ('Gemini Notebook', 'https://notebook.google/')), 'Examples, in no particular order. For current features, availability and data settings, check the vendor page and ask your administrator.', '58 → curated', 'Reference', cls='ref'),
 slide('Reference · create and connect', links(('Gamma', 'https://gamma.app/'), ('Canva', 'https://www.canva.com/canva-ai/'), ('ElevenLabs', 'https://elevenlabs.io/text-to-speech'), ('Lovable', 'https://lovable.dev/'), ('Zapier', 'https://zapier.com/')), 'The handout adds questions to ask when choosing. It leaves prices out on purpose, because they change faster than the handout will.', '59 → curated', 'Reference', cls='ref'),
 slide('Reference · evidence and access', links(('Project Vend', 'https://www.anthropic.com/research/project-vend-1'), ('Project Vend: phase two', 'https://www.anthropic.com/research/project-vend-2'), ('AI co-scientist', 'https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/'), ('Microsoft 365 Copilot', 'https://www.microsoft.com/en-us/microsoft-365-copilot/business'), ('MCP introduction', 'https://modelcontextprotocol.io/docs/getting-started/intro')), 'Sources for the two stories, including the December 2025 follow-up to Project Vend, and the access examples. The source log in the repository (SOURCES.md) separates facts from examples and recommendations.', '58–59 → curated', 'Reference', cls='ref'),
]

# TALK 02: one task, one agent, observable evidence.
INTRO = [
 title('Agentic<br>AI', 'Give an agent a task. Understand and check its work.', '02 · Developers new to agents · v2', 'The audience knows files and tests but has not used a coding agent. The invoice task is small on purpose, so you can follow every step in front of them.'),
 slide('One failing test, one bounded task', failing_test(), 'These values come from the checked-in fixture. The 21% rate is a teaching input, not tax advice. Getting this one input right is only the first check.', '2, 13', 'The task'),
 slide('Set the boundaries before you start', boundaries(), 'Show the real workspace and permission settings. Leave approval prompts on for anything outside the task, and do not switch to bypass mode to save time on stage. A separate folder keeps the work scoped, but it is not a security sandbox.', '33–34 moved before demo', 'Before the demo', dark=True),
 slide('Give it the outcome and the checks', window('prompt', ''.join(f'<div class="ln"><span class="no">{i}</span><span class="tx">{esc(t)}</span></div>' for i, t in enumerate(['Fix the failing invoice tests. Explain the cause.', 'Apply the supplied rate; round once, half up.', 'Preserve the tests. Work only in this demo folder.', 'Do not install or publish anything.', 'Run python3 -m unittest -v.', 'Show the result and the diff.'], 1)), 'paper', 'v-brief prompt'), 'The full prompt is in examples/v2/invoice/README.md. Before the talk, copy before/ to a throwaway directory. Start the agent now, after the boundaries slide, and read each approval request before you accept it. If you cannot run live, use the prepared checkpoints.', '4, 40 → concrete prompt', 'Start the demo', foot='<a href="examples/v2/invoice/README.md" target="_blank" rel="noopener">Demo setup and fallback</a>'),
 slide('Four places to stop and look', stations([('Failure', 'What broke?'), ('Evidence', 'What did it read?'), ('Change', 'What did it edit?'), ('Check', 'What passed?')], ['warn', 'search', 'pencil', 'tick'], ok=(3,), label='Four checkpoints: failure, evidence, change, check'), 'We chose these four stops for teaching; a real agent may take a different path. If it finishes early, walk through the completed trace. If it stalls, switch to the prepared fixtures and tell the audience you have switched.', '4, 12, 15, 30, 33 → coordinated callbacks', 'The route'),
 slide('The model <span class="o">chooses</span>; the harness <span class="o">executes</span>', model_harness(), 'The agent is the two together, iterating on a task. The model never runs Python itself: it asks, and the harness runs the tool. The word harness earns its place because it explains why the same model behaves differently in different products.', '6, 10', 'Two parts'),
 slide('The agent repeats that exchange', video('agent-loop-dark', 'Choose an action, run the tool, read the result, then continue or stop', steps=['Choose an action', 'Run the tool', 'Read the result', 'Continue or stop']), 'If the live run has made a tool call, show it now. Use the animation to connect model, harness and tool, and describe only what it shows; do not narrate an imagined live result. The failure output comes next.', '12', 'The loop', dark=True),
 slide('Checkpoint 1 · the failure is evidence', checkpoint1(), 'This is the prepared fallback, run from before/. The real output also has test names and tracebacks; the slide shows an excerpt. Ask the room what the agent should read next. If the live output differs, say how, rather than claiming it matches.', '2, 13 → checked fallback', 'Inspect the run', foot='Prepared fixture result · not an agent trace', head=mini(1)),
 slide('A tool call leaves something you can inspect', tool_call(), 'Show the file-read entry in the live trace, or open before/invoice.py. Providers format tool calls differently. The evidence is the result the harness returned; the model saying it read the file proves nothing.', '11–13', 'Tools'),
 slide('Checkpoint 2 · the code explains the failure', code_explains(), 'The excerpt drops the type annotations and docstring; the full source is in before/invoice.py. A zero rate changes nothing, so that test passes even with the bug. The two nonzero cases fail, and that pattern points at the unused tax_rate.', '9, 11 → same task', 'Inspect the run', head=mini(2)),
 slide('Context is what the model can use now', context_now(), 'Context covers more than the latest message. Products may retrieve or summarise earlier material, so do not say every request resends every previous token, or that the product stores nothing between turns.', '7–11, 28 → compressed', 'Context'),
 slide('Too much context hides what matters', more_info(), 'There is no universal 40% or 50% threshold. When quality drops depends on the model, the task and the content. Leaving out a file the agent needs can hurt as much as loading material it does not.', '29–30', 'Context'),
 slide('When a session loses the thread', handoff(), 'Describe compaction as a summary that can drop details, and go no further. Caching changes reused computation and billing; it will not bring back a dropped fact. Subagents come up in talks 03 and 04, so skip them here.', '31–32, 40', 'Context'),
 slide('Verify against evidence, whatever the reasoning says', thinking(), 'Reasoning can help the model with the task, but the text you see is not a faithful record of why it acted; Anthropic’s research on reasoning reports found models leave things out. Keep it practical: review the evidence and do not accept a confident explanation in its place.', '14–15', 'Reasoning', dark=True),
 slide('Checkpoint 3 · inspect the change', diff_view(), 'A simplified diff: before/ has no total variable, which only appears in after/invoice.py. Open the real diff and confirm the rate comes from the argument. A fix that hard-codes 121 or weakens the tests fails review.', '13 → patch review', 'Inspect the run', head=mini(3)),
 slide('Checkpoint 4 · check more than one case', test_cards(), 'Prepared result from running python3 -m unittest test_invoice -v in after/. The three cases cover the fixture’s stated behaviour, which falls well short of real billing rules. The export tests belong to talk 03.', '13, 40 → independent checks', 'Inspect the run', foot='Prepared fixture result · three invoice tests', head=mini(4)),
 slide('Passing tests are part of the review', review_list(), 'If you ran live, open the agent’s real output. An agent can report success after skipping a command or editing a test. You, the reviewer, decide whether the evidence is enough.', '33, 40–41 → stronger finish', 'Review'),
 slide('If it goes wrong, interrupt early', interrupt(), 'If the changes are wrong, read the diff, then go back to a checkpoint you understand or restore the throwaway copy. Do not reach for a reset command that could wipe unrelated work. Retrying the same prompt with no new information rarely helps.', 'new failure recovery', 'Recovery', dark=True),
 slide('Rules in a file load into every session', rules_file(), 'Use the file your harness reads: CLAUDE.md for Claude Code, AGENTS.md for tools that support it. The model reads these instructions, but they do not enforce access. Some products also keep memory notes, so check what gets loaded.', '35–36', 'Project knowledge'),
 slide('Put recurring procedures in a skill', panels((ill_rules(False), 'Project rules', 'Short facts and boundaries needed across tasks.'), (ill_rules(True), 'Skill', 'A reusable procedure loaded for the relevant task.')), 'A release checklist makes a good example. A skill is a set of instructions, with supporting files if it needs them. How it loads and gets invoked depends on the harness. Leave plugin packaging for a later talk.', '37', 'Project knowledge'),
 slide('Tools can reach outside the repo', reach(), 'MCP standardises part of how assistants connect to outside tools and data. You still need authentication, and connecting a system does not make access to it safe. Our demo has no reason to reach outside the repo.', '38–39', 'Connected tools'),
 slide('Start with one approved agent', one_agent(), 'Model choice can wait until people can pick a task and judge the result. Availability and account features change, so send people to the product documentation for setup.', '17–27 → one practical choice', 'Getting started'),
 slide('Your first session, in five steps', stations([('Describe', 'Name the outcome.'), ('Provide', 'Give relevant context.'), ('Limit', 'Set access and scope.'), ('Inspect', 'Read the change.'), ('Verify', 'Run the checks.')], ['target', 'stack', 'lock', 'search', 'tick'], ok=(4,)), 'Go back to the invoice task and ask the room to match each step to what the agent did. This routine is the takeaway; stop teaching after it.', '40–41 → one close', 'Your next step', dark=True, cls='beat'),
 slide('Try the fixture, then a task of your own', linkcards(('Demo files, prompt and fallback', 'examples/v2/invoice/README.md', 'codefile', 'Practice'), ('Next: engineer a repeatable workflow', 'agentic-engineering-v2.html', 'loop', 'Talk 03'), ('Choose a tool for a different kind of work', 'ai-toolbox-v2.html', 'actions', 'Talk 01')), 'Take questions. The fixture is small enough to read end to end. For a first real task, pick work you already understand and can check.', '41 → practice', 'Questions'),
 slide('Reference · operating an agent', links(('Claude Code: how it works', 'https://code.claude.com/docs/en/how-claude-code-works'), ('Claude Code: permissions', 'https://code.claude.com/docs/en/permissions'), ('Claude Code: project memory', 'https://code.claude.com/docs/en/memory'), ('Claude Code: skills', 'https://code.claude.com/docs/en/skills')), 'These are Claude Code documents; other harnesses differ. Check the current documentation for exact controls.', '42–43 → curated', 'Reference', cls='ref'),
 slide('Reference · context and evidence', links(('Effective context engineering', 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'), ('Reasoning reports and their limits', 'https://www.anthropic.com/research/reasoning-models-dont-say-think'), ('MCP introduction', 'https://modelcontextprotocol.io/docs/getting-started/intro'), ('Building effective agents', 'https://www.anthropic.com/engineering/building-effective-agents')), 'Sources for the concepts in this talk. The fixture and its test results are our own evidence and say nothing about any provider.', '42–43 → curated', 'Reference', cls='ref'),
]

# TALK 03: an evolution of the workflow, with one invoice-export example.
ENGINEERING = [
 title('Agentic<br>Engineering', 'Build a workflow you can verify and recover.', '03 · Developers going deeper · v2', 'The audience knows model, harness, tools and context from talk 02. This talk is about making the process repeatable. Each chapter takes one way the invoice-export workflow fails and fixes it.'),
 slide('Repeated work is harder than the demo', demo_vs_repeat(), 'Aim for work you can accept on evidence and recover when it fails. Maximum autonomy is not the goal. One good transcript says little about how the next run will go.', '2, 23–25 → new framing', 'The problem'),
 slide('The example: invoice CSV export', csv_hero(), 'An excerpt from the reference CSV; the full file also has a customer name with a newline in it. The implementation assumes validated rows. Production validation and spreadsheet formula handling are separate requirements that we leave out.', 'new running example', 'The task', foot='<a href="examples/v2/invoices.csv" download>Download the reference CSV</a>'),
 slide('Recap: the system you are engineering', cycle([('Context', 'Task, rules and evidence.'), ('Model', 'Proposes the next step.'), ('Tools', 'Perform permitted actions.'), ('Result', 'Changes what the system knows.')], ['stack', 'sparkle', 'gear', 'report'], 'A loop: context feeds the model, the model proposes a step, tools act, and the result changes the context.'), 'Keep this to one slide. You control what information the system receives, what it may do, and how you check the results.', '3–21 → recap', 'The machine'),
 slide('Problem 1 · “Add export” leaves too much open', unspecified(), 'Ask the room what they would need before they could review an export. This is a contract problem before it is a model problem, and more reasoning effort will not settle an ambiguous request.', '25 → expanded contract', 'Define the work', dark=True, layout='problem', pnum=1, plead='<span class="kk">Consequence</span>A plausible implementation may still miss the requirement.'),
 slide('Write the acceptance contract first', contract(), 'These four requirements are the ones the checked-in fixture implements. We kept the set small so every line is testable. Say plainly that production requirements are missing; this is not a billing system.', '23–25 → explicit contract', 'Define the work'),
 slide('Decide how much structure the task needs', structure(), 'These are options, and nobody has to climb from one to the next. A workflow can contain agent-driven stages. Pick the simplest one that meets the contract and lets you explain the result.', '20, 48', 'Choose the process'),
 slide('Make the stages and ownership visible', stations([('Inspect', 'Locate code and tests.'), ('Plan', 'Resolve the contract.'), ('Build', 'Make the bounded change.'), ('Verify', 'Run independent checks.'), ('Review', 'Accept or send back.')], ['search', 'list', 'code', 'tick', 'person'], hot=(4,), back=(4, 2, 'send back')), 'The workflow for our export. Name one person who owns integration and acceptance. The next slides cover what evidence and recovery look like at each gate.', '46–48 → core workflow', 'The workflow'),
 slide('Problem 2 · a green command can mislead', exit_zero(), 'An exit code tells you the command finished without an error. Whether the tests cover the contract is a separate question. No prompt can stop an agent from satisfying a weaker check; independent checks and review are how you catch it.', '23–25', 'Check the evidence', dark=True, layout='problem', pnum=2, plead='Exit code 0 says the command finished. It does not say what was tested.'),
 slide('Give every claim a check', claim_check(), 'The reference test uses a comma, embedded quotes and a newline. Parsing the file with Python’s CSV reader tests the serialisation in a way that eyeballing the text cannot. Formula-like input stays outside this fixture’s contract.', '23–25 → example verification', 'Check the evidence'),
 slide('Put the calculation in code with an explicit rule', calc_code(), 'When the calculation is specified, write it as code. The agent can read and change that code; you verify it against the stated rounding rule. This is the reference fix from talk 02, and the exporter reuses it.', '15, 25 → deterministic tool example', 'Check the evidence'),
 slide('Inspect the tests and the file they produce', tests_and_artifact(), 'Prepared result from after/, trimmed to the test names. Read the names against the contract: the two export tests cover the round trip and the empty file, and the three invoice tests cover the rate and the rounding. Then open the file itself. Check that the header lists the five columns in order, and work out one total by hand: 0.50 at 21% is 0.605, which rounds half up to 0.61. We generated the CSV with the same code; it is neither a benchmark nor a recorded agent run.', '23–25 → checked evidence', 'Check the evidence', foot='Prepared reference result · five tests'),
 slide('Keep acceptance separate from implementation', two_actor(), 'A second model can help review, but it may share the first one’s blind spots. Where it matters, keep acceptance checks where the implementing agent cannot edit them. In this workflow a person makes the call.', '24–25, 42 → review ownership', 'Check the evidence'),
 slide('Problem 3 · the useful facts get buried', buried(), 'Do not describe attention as a fixed budget split equally between tokens. Irrelevant material can make retrieval worse and distract the model; how much depends on the model and the task.', '26–34 → context diagnosis', 'Manage context', dark=True, layout='problem', pnum=3, plead='Exploration accumulates logs, dead ends and outdated assumptions.'),
 slide('Give each stage the context it needs', stage_context(), 'This split is our design; no harness does it for you. Each fresh stage needs enough context to keep earlier decisions, and a short handoff helps only if it carries the facts that matter.', '18, 27, 36, 46', 'Manage context'),
 slide('Write a handoff note before restarting', handoff_note(), 'A handoff note for the reference fixture. It keeps file references and open scope questions and leaves out pages of tool output. The new session should check the note against the files before relying on it.', '34, 50–51 → useful handoff', 'Manage context'),
 slide('Caching and compaction solve different problems', cache_vs_compaction(), 'Billing rules, cache lifetimes and the handling of reasoning all vary by provider and model. Do not claim that requests must be byte-identical, that caches stay warm indefinitely, or that thinking is always kept or always stripped. Talk 04 covers the mechanics.', '31–34 → two distinctions', 'Manage context'),
 slide('Problem 4 · retries consume the budget', budget(), 'Set a limit so a retry loop cannot keep editing forever. A flaky tool, a misunderstanding and an unmet requirement each need a different response.', '22, 24 → bounded retries', 'Recover', dark=True, layout='problem', pnum=4, plead='A failed attempt should change the next decision.'),
 slide('Set a retry policy before the run', retry_tree(), 'A policy sketch, not a setting you switch on. Pick the actual numbers for your environment. When a run stops, it should keep the evidence it gathered and report the task as unfinished.', '22–25 → stop policy', 'Recover'),
 slide('Record a baseline you can return to', recovery(), 'A branch or worktree isolates edits. It does nothing for credentials or network access, so isolate the environment separately when you need to. Do not reset a shared workspace that has uncommitted changes; you may destroy unrelated work.', '24, 44 → recovery boundary', 'Recover'),
 slide('Problem 5 · cheap tokens can buy costly work', fraction(), 'Neither bigger nor smaller models are always cheaper. Compare the whole process on representative tasks with the same acceptance criteria. Subscription limits and API charges measure different things.', '29–31, 38–45 → cost per accepted task', 'Choose the model', dark=True, layout='problem', pnum=5, plead=''),
 slide('Measure the cost per accepted task', accepted_chart(), 'The numbers are invented to show the arithmetic; they measure no real model. Both setups spend one dollar of model and tool cost per accepted task. Add review time, as problem 5 says, and B is cheaper: ten accepted tasks for 15 minutes of review against six for 40. Keep failures, latency and review time visible as their own numbers too, so one total cannot hide them.', '30, 38 → labelled comparison', 'Choose the model', foot='Illustrative numbers · not vendor measurements', tsize=80),
 slide('Change one dial and measure again', stations([('Baseline', 'A few representative tasks and fixed checks.'), ('Trial', 'Change model or reasoning effort.'), ('Compare', 'Acceptance, cost, time and review burden.')], ['flag', 'dial', 'scale'], hot=(1,)), 'Put common tasks and failure-prone cases in the set, and run each enough times to see the variation. Rerun the trial when the model, prompt or tools change. Any ranking of named models you get is temporary.', '37–45 → evaluation method', 'Choose the model'),
 slide('Problem 6 · one agent carries too much', video('subagents-dark', 'A separate worker investigates and sends evidence back. Token counts in the animation are illustrative.', cls='stacked'), 'Delegation helps when an investigation can be split off, or when running work in parallel saves time. It costs coordination, handoffs and money, and this small export does not need it. The 80k and 200 token counts in the animation are illustrative; nobody measured them on this example.', '35–36', 'Delegate selectively', dark=True, layout='problem', pnum=6, plead=''),
 slide('Delegate an outcome with a boundary', delegate(), 'A reviewer brief for the same export. Check the reviewer’s findings before you act on them; a short conclusion with no evidence does not count.', '42–44 → bounded delegation', 'Delegate selectively'),
 slide('Parallel work still needs integration', fan_in(), 'Read-only reviews combine easily; parallel edits to the same files do not. Give independent edits their own worktrees, then run the tests again on the combined result.', '44–48 → integration', 'Delegate selectively'),
 slide('Problem 7 · useful lessons disappear', rows(('pin', 'Keep a rule', 'A short constraint needed across tasks.'), ('checklist', 'Keep a procedure', 'A skill for a recurring workflow.'), ('link', 'Keep evidence', 'A decision note linked to the relevant code or test.'), cls='keepers'), 'A solved task rarely deserves a permanent note. Keep what will change how the next task goes, and prune stale instructions every so often. Plugin distribution can wait.', '49–58 → durable knowledge', 'Make it repeatable', dark=True, layout='problem', pnum=7, plead=''),
 slide('Write one small procedure people can inspect', procedure(), 'An example skill body; a real package would add provider-specific files. Make the procedure readable and useful before you share it. It cannot enforce permissions or guarantee a complete review.', '51–58 → one reusable procedure', 'Make it repeatable'),
 slide('The complete workflow has a way back', way_back(), 'Walk the invoice export through once. This rail folds Inspect and Plan from the earlier workflow into Contract. When new evidence overturns a decision, go back to the stage that made it. If the budget runs out, keep the partial result and mark it incomplete. The run succeeds when a reviewer accepts the evidence against the contract.', '46–48, 59 → synthesis', 'Bring it together', track=PROBLEMS + 1),
 slide('Improve one workflow this week', rows(('doc', 'Write the contract', 'What must be true when the task is done?'), ('tick', 'Add the evidence', 'Which check can establish it?'), ('exit', 'Add the exit', 'How will you stop and recover when it fails?'), cls='closing'), 'This is the one action to leave with. Push for a small change to a workflow people already run, before anyone adds fleets of agents or a plugin marketplace.', '59 → concrete close', 'Your next step', dark=True, cls='beat'),
 slide('Go deeper where your work needs it', deck_cards(), 'Take questions. We re-checked all six deep dives against their sources in September 2026. The ones marked WIP are still being written, so expect gaps there.', 'new series handoff', 'Questions'),
 slide('Reference · workflows and evaluation', links(('Building effective agents', 'https://www.anthropic.com/engineering/building-effective-agents'), ('Demystifying evals for AI agents', 'https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents'), ('Effective context engineering', 'https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents'), ('Fixture, tests and reference implementation', 'examples/v2/invoice/README.md')), 'Sources for the design distinctions. The workflow, the retry table and the cost comparison are our teaching designs; none is a measured production result. SOURCES.md and VALIDATION.md record the evidence for this edition.', '60 → curated', 'Reference', cls='ref'),
]

CSS = r'''
/* ═══ V2 VISUAL LAYER ═══════════════════════════════════════════════
   deck-stage owns viewport scaling; everything here is fixed 1920×1080 px.
   Reference: visual-mockups-v2.html. Colours are Ember tokens only. */
.v2{--h2-size:88px;--h3-size:52px;--lead-size:42px;--body-size:34px;--small-size:26px;--code-size:36px;
  --icbg:var(--s-card-bg);--v-fail:#ff6b4f}
.v2 .slide-content{padding:60px 96px 96px;justify-content:flex-start;gap:0}
.v2 .slide-head{align-items:center;gap:40px;margin-bottom:40px;padding-bottom:22px;border-bottom:1px solid var(--s-line);flex:none}
.v2 .snum{font-size:52px}
.v2 .crumb{font-size:26px;letter-spacing:.1em;min-width:220px}
.v2 h2{font-size:var(--h2-size);line-height:1.02;letter-spacing:-.03em;margin:0;max-width:none;flex:none}
.v2 .v2-body{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:36px;padding-top:32px}
.v2 .note{flex:none;margin-top:18px;font:500 24px/1.3 var(--font-mono);letter-spacing:.03em;color:var(--s-muted)}
.v2 .lead{font-size:var(--lead-size);line-height:1.35;max-width:none;color:var(--s-text)}
.v2 .lead.sm{font-size:36px}
.v2 .lead b,.v2 .v-row p b{color:var(--s-accent);font-weight:600}
.v2 a{color:var(--s-accent);text-underline-offset:.18em}
.v2 a:focus-visible{outline:3px solid var(--s-accent);outline-offset:8px}
.v2 svg{overflow:visible}
.v2 svg text{font-family:var(--font-mono)}
.v2 .ic{fill:none;stroke:currentColor;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;color:var(--s-accent)}
.v2 .ic .bg{fill:var(--icbg)}
.v2 .kk{display:block;font:600 24px/1.2 var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent)}
.v2 .chips{display:flex;flex-wrap:wrap;gap:14px}
.v2 .chips span{display:inline-flex;align-items:center;gap:12px;font:500 28px var(--font-mono);color:var(--s-text);background:var(--s-bg);border:2px solid var(--s-card-border);border-radius:40px;padding:10px 24px}
.v2 .chips .ic{width:34px;height:34px}
.v2-stack{display:flex;flex-direction:column;gap:32px;min-width:0}
.v2 .split{gap:72px;align-items:center}

/* beats: coral edge for problem and closing slides */
.v2.beat::before,.v2.pbeat::before{content:"";position:absolute;left:0;top:0;bottom:0;width:16px;background:var(--coral);z-index:2}
.v2.beat .slide-content{padding-left:120px}

/* svg vocabulary */
.v2 .mk-a{fill:var(--s-accent)} .v2 .mk-c{fill:var(--coral)} .v2 .mk-t{fill:var(--s-text)} .v2 .mk-m{fill:var(--s-muted)}
.v2 .ln-c{stroke:var(--coral);stroke-width:6;fill:none}
.v2 .ln-a{stroke:var(--s-accent);stroke-width:4;fill:none}
.v2 .ln-t{stroke:var(--s-text);stroke-width:5;fill:none}
.v2 .ln-m{stroke:var(--s-muted);stroke-width:4;fill:none}
.v2 .ln-dim{stroke:var(--s-line-strong);stroke-width:3;fill:none}
.v2 .thick{stroke-width:8} .v2 .xthick{stroke-width:12;stroke-linecap:round}
.v2 .dash{stroke-dasharray:14 12}
.v2 .ln-stop{stroke:var(--s-text);stroke-width:6;stroke-dasharray:6 8}
.v2 .ring{fill:none;stroke:var(--s-line-strong);stroke-width:4;stroke-dasharray:4 12;stroke-linecap:round}
.v2 .ring-c{fill:none;stroke:var(--coral);stroke-width:5}
.v2 .nd{fill:var(--ink);stroke:var(--s-bg);stroke-width:8}
.v2 .nd + .ic{color:var(--paper)}
.v2 .nd.hot{fill:var(--coral)} .v2 .nd.hot + .ic{color:var(--ink)}
.v2 .nd.soft{fill:var(--s-card-bg);stroke:var(--s-card-border);stroke-width:3} .v2 .nd.soft + .ic{color:var(--s-accent)}
.v2.dark .nd{fill:var(--ink-2);stroke:var(--coral);stroke-width:4} .v2.dark .nd + .ic{color:var(--coral)}
.v2.dark .nd.hot{fill:var(--coral)} .v2.dark .nd.hot + .ic{color:var(--ink)}
.v2 .f-coral{fill:var(--coral)} .v2 .f-ink{fill:var(--ink)} .v2 .f-ink2{fill:var(--s-text)} .v2 .f-bar{fill:var(--s-bar)}
.v2 .f-mut{fill:var(--s-muted)} .v2 .f-bg{fill:var(--s-bg)} .v2 .f-soft{fill:var(--coral-soft)} .v2 .f-soft2{fill:var(--coral-tint)}
.v2.dark .f-ink{fill:var(--ink-3);stroke:var(--line-dark);stroke-width:2}
.v2 .bx-card{fill:var(--s-card-bg);stroke:var(--s-card-border);stroke-width:2}
.v2 .bx-mid{fill:var(--s-box-mid);stroke:var(--s-line-strong);stroke-width:2}
.v2 .bx-dash{fill:none;stroke:var(--s-line-strong);stroke-width:2;stroke-dasharray:8 7}
.v2 .bx-dash2{fill:none;stroke:var(--s-muted);stroke-width:3;stroke-dasharray:10 9}
.v2 .bx-hot{stroke:var(--coral);stroke-width:3}
.v2 .bx-hot.soft{fill:var(--s-callout-bg)}
.v2 .hl-box{fill:rgba(255,92,53,.18);stroke:var(--coral);stroke-width:2.5}
.v2 .ch-card rect{fill:var(--s-card-bg);stroke:var(--s-card-border);stroke-width:2}
.v2 .ok-dot{fill:var(--positive-on-dark)} .v2.light .ok-dot{fill:var(--positive)}
.v2 .ok-tick{fill:none;stroke:var(--ink);stroke-width:6;stroke-linecap:round;stroke-linejoin:round} .v2 .ok-tick.sm{stroke-width:4} .v2 .ok-tick.lg{stroke-width:11}
.v2 .gap{fill:none;stroke:var(--coral);stroke-width:3;stroke-dasharray:8 6}
.v2 .lost{fill:none;stroke:var(--danger);stroke-width:2;stroke-dasharray:6 5;opacity:.75}
.v2 .xmark path{stroke:var(--coral);stroke-width:5;stroke-linecap:round}
.v2 .x-inv{stroke:var(--ink);stroke-width:9;stroke-linecap:round}
.v2 .cp path{fill:var(--s-bg);stroke:var(--s-text);stroke-width:5}
.v2 .t-cap{font:500 22px var(--font-mono);letter-spacing:.12em;fill:var(--s-faint);text-transform:uppercase}
.v2 .t-acc{font:600 28px var(--font-mono);fill:var(--s-accent);letter-spacing:.03em}
.v2 .t-mut{font:500 28px var(--font-mono);fill:var(--s-muted)}
.v2 .t-faint{font:500 24px var(--font-mono);fill:var(--s-faint)}
.v2 .t-strong{font:600 32px var(--font-body);fill:var(--s-text)}
.v2 .t-strong.mono,.v2 text.mono{font-family:var(--font-mono);font-size:28px}
.v2 .sm{font-size:24px}
.v2 .t-on{font:700 26px var(--font-mono);fill:var(--ink)} .v2 .t-on.big{font-size:32px}
.v2 .t-paper{font:600 30px var(--font-mono);fill:var(--paper);letter-spacing:.04em}
.v2 .t-paper.lg,.v2 .t-strong.lg{font:700 56px var(--font-display);letter-spacing:-.02em}
.v2 .t-onmut{font:500 28px var(--font-mono);fill:var(--on-dark-muted)}
.v2 .t-danger{font:600 28px var(--font-mono);fill:var(--danger)}
.v2 .t-num{font:700 84px var(--font-display);fill:var(--s-text);letter-spacing:-.03em}
.v2 .t-good{font:700 44px var(--font-display);fill:var(--coral-ink)}
.v2 .bx-good{fill:var(--coral-soft);stroke:var(--coral);stroke-width:3}
.v2 .bx-q{stroke:var(--s-line-strong);stroke-width:2}
.v2 .io-arrow{width:160px;height:60px;flex:none}

/* ── tiles ── */
.v-tiles{display:grid;gap:36px;flex:1;min-height:0;max-height:640px}
.v-tiles.n2,.v-tiles.n4{grid-template-columns:repeat(2,minmax(0,1fr))}
.v-tiles.n3{grid-template-columns:repeat(3,minmax(0,1fr))}
.v-tile{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-top:10px solid var(--coral);border-radius:6px 6px 22px 22px;padding:44px 48px 48px;display:flex;flex-direction:column;min-height:0;min-width:0}
.v-tile .top{display:flex;justify-content:space-between;align-items:flex-start}
.v-tile .top span{font:500 28px var(--font-mono);color:var(--s-faint);letter-spacing:.08em;margin-left:auto}
.v-tile .top .ic{width:170px;height:170px}
.v-tile h3{font:700 72px/1.02 var(--font-display);letter-spacing:-.03em;margin-top:auto;padding-top:24px;color:var(--s-text)}
.v-tiles.n3 .v-tile h3{font-size:64px}
.v-tile p{font-size:36px;line-height:1.35;color:var(--s-muted);margin-top:20px;min-height:2.7em}
.v-tiles.jobs .v-tile h3{font-size:84px}
.v-tiles.jobs .v-tile p{font-size:38px}
.v-tiles.diag .v-tile svg{width:100%;height:auto;margin-bottom:auto}
.v-tiles.diag .v-tile h3{font-size:56px}

/* ── stations rail ── */
.v-stn .rail{display:block;width:100%;height:auto}
.rail .rl-base{stroke:var(--s-line-strong);stroke-width:6;stroke-dasharray:4 14;stroke-linecap:round}
.rail .rl-on{stroke:var(--coral);stroke-width:12;stroke-linecap:round}
.rail .rl-c{fill:var(--ink);stroke:var(--s-bg);stroke-width:10}
.v2.dark .rail .rl-c{fill:var(--ink-2);stroke:var(--coral);stroke-width:5}
.rail .rl-c.hot,.v2.dark .rail .rl-c.hot{fill:var(--coral);stroke:var(--s-bg);stroke-width:10}
.rail .ic{color:var(--paper)}
.v2.dark .rail .ic{color:var(--coral)}
.rail .ic.hot,.v2.dark .rail .ic.hot{color:var(--ink)}
.rail .ic.ok,.v2.dark .rail .ic.ok{color:var(--positive-on-dark)}
.rail .rl-num{font:700 64px var(--font-display);fill:var(--paper)}
.v2.dark .rail .rl-num{fill:var(--coral)}
.rail .rl-n{font:500 30px var(--font-mono);fill:var(--s-accent);letter-spacing:.08em}
.rail .rl-back{fill:none;stroke:var(--coral);stroke-width:5;stroke-dasharray:14 10}
.rail .rl-bg{fill:var(--s-bg);stroke:var(--coral);stroke-width:2}
.rail .rl-bl{font:600 26px var(--font-mono);fill:var(--s-accent);letter-spacing:.06em}
.v-stn .stops{display:grid;text-align:center;margin-top:24px;gap:28px}
.v-stn.n2 .stops{grid-template-columns:repeat(2,1fr)} .v-stn.n3 .stops{grid-template-columns:repeat(3,1fr)}
.v-stn.n4 .stops{grid-template-columns:repeat(4,1fr)} .v-stn.n5 .stops{grid-template-columns:repeat(5,1fr)}
.v-stn .stops h3{font:700 72px/1.02 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-stn.n4 .stops h3{font-size:64px}
.v-stn.n5 .stops h3{font-size:52px}
.v-stn .stops p{font-size:38px;line-height:1.3;color:var(--s-muted);margin-top:14px}
.v-stn.n4 .stops p{font-size:36px}
.v-stn.n5 .stops p{font-size:32px}

/* ── wayfinding ── */
.mini{list-style:none;display:flex;align-items:center;font:500 24px var(--font-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--s-faint);margin:0 auto}
.mini li{display:flex;align-items:center;gap:14px}
.mini li+li::before{content:"";width:56px;height:3px;background:var(--s-line-strong);margin:0 18px;border-radius:2px}
.mini li i{width:22px;height:22px;border-radius:50%;border:3px solid var(--s-line-strong);display:block;background:var(--s-bg)}
.mini li.done{color:var(--s-muted)} .mini li.done i{border-color:var(--coral);background:var(--s-callout-bg)}
.mini li.on{color:var(--s-accent);font-weight:600}
.mini li.on i{background:var(--coral);border-color:var(--coral);box-shadow:0 0 0 7px rgba(255,92,53,.18)}
.ptrack{list-style:none;display:flex;align-items:center;gap:10px;margin:0 auto;font:600 20px var(--font-mono);color:var(--s-faint);counter-reset:prob}
.ptrack::before{content:"Problem";font:500 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;margin-right:10px}
.ptrack li{counter-increment:prob;width:40px;height:40px;border-radius:50%;border:2px solid var(--s-line-strong);display:flex;align-items:center;justify-content:center}
.ptrack li::before{content:counter(prob)}
.ptrack li.done{border-color:var(--coral);color:var(--s-accent)}
.ptrack li.on{background:var(--coral);border-color:var(--coral);color:var(--ink);box-shadow:0 0 0 6px rgba(255,92,53,.2)}

/* ── windows: terminal (evidence) and paper (briefs, notes) ── */
.v-win{border-radius:20px;overflow:hidden;min-width:0;flex:none}
.v-win.term{background:var(--term-bg);box-shadow:var(--shadow-terminal);border:1px solid #2a241b;color:var(--code-text)}
.v2.dark .v-win.term{border-color:var(--line-dark)}
.v-win .tbar{background:var(--term-bar);height:62px;display:flex;align-items:center;gap:12px;padding:0 26px}
.v-win .tbar i{width:18px;height:18px;border-radius:50%;display:block}
.v-win .tbar .r{background:var(--term-dot-red)} .v-win .tbar .y{background:var(--term-dot-yellow)} .v-win .tbar .g{background:var(--term-dot-green)}
.v-win .tbar span{font:500 22px var(--font-mono);color:var(--on-dark-faint);margin-left:14px;letter-spacing:.06em}
.v-win .wbody{padding:40px 56px 48px;font:500 38px/1.5 var(--font-mono);white-space:pre-wrap;overflow-wrap:anywhere}
.v-win.term .k{color:var(--code-keyword)} .v-win.term .s{color:var(--code-string)} .v-win.term .c{color:var(--code-comment)} .v-win.term .n{color:var(--code-number)}
.v-win.term .p{color:var(--coral)} .v-win.term .dim{color:var(--on-dark-muted)}
.v-win.term .fail{display:block;margin-top:10px;font:700 70px/1.1 var(--font-mono);color:var(--v-fail);letter-spacing:-.01em}
.v-win.term .okbig{display:block;margin-top:10px;font:700 110px/1 var(--font-mono);color:var(--positive-on-dark)}
.v-win.paper{background:var(--paper);border:2px solid var(--line-light);box-shadow:0 18px 50px rgba(0,0,0,.10);color:var(--text-strong)}
.v2.light .v-win.paper{background:#fbf8f2}
.v2.dark .v-win.paper{border-color:var(--line-dark)}
.v-win.paper .tbar{background:var(--paper-3)} .v-win.paper .tbar i{background:var(--line-light)}
.v-win.paper .tbar span{color:var(--text-muted)}
.v-brief .wbody{padding:30px 48px 36px;white-space:normal}
.v-brief .ln{display:grid;grid-template-columns:56px 1fr auto;align-items:center;gap:20px;padding:14px 0 14px 20px;font:500 38px/1.35 var(--font-mono);border-left:6px solid transparent}
.v-brief .ln + .ln{border-top:1px solid var(--line-light-2)}
.v-brief .ln .no{color:var(--text-faint);font-size:28px}
.v-brief .ln.mk{border-left-color:var(--coral);background:var(--coral-soft)}
.v-brief .ln b{font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--coral-ink);border:2px solid var(--coral);border-radius:20px;padding:4px 14px;margin-right:12px}
.v-brief.prompt .ln{font-size:36px;padding:10px 0 10px 20px}
.v-brief.md .wbody{white-space:pre-wrap;font-size:36px;line-height:1.6}
.v-brief.md .h,.v-skill .h{color:var(--coral-ink);font-weight:700}
.v-brief.md b{color:var(--coral-ink);font-weight:600}

/* ── mock pair 1: failing test ── */
.v-fail .tcall{font:500 50px/1 var(--font-mono);color:var(--code-text);padding:44px 64px 0}
.v-fail .wbody{padding:0}
.v-fail .vs{display:grid;grid-template-columns:1fr auto 1fr;align-items:end;gap:48px;padding:30px 64px 50px}
.v-fail .lab{display:flex;align-items:center;gap:14px;font:500 30px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--on-dark-faint);margin-bottom:10px}
.v-fail .lab i{width:18px;height:18px;border-radius:50%}
.v-fail .num{font:700 220px/.88 var(--font-display);letter-spacing:-.035em;display:block}
.v-fail .exp .num{color:var(--positive-on-dark)} .v-fail .exp .lab i{background:var(--positive-on-dark)}
.v-fail .act .num{color:var(--v-fail)} .v-fail .act .lab i{background:var(--v-fail)}
.v-fail .neq{font:500 140px/1 var(--font-display);color:var(--on-dark-faint);padding-bottom:22px}
.v-fail .task{font:400 48px/1.3 var(--font-body);margin-top:48px;color:var(--s-text)}
.v-fail .task b{color:var(--s-accent);font-weight:600}

/* ── mock pair 3: checkpoint 1 ── */
.v-cp1{display:grid;grid-template-columns:1.2fr 1fr;gap:72px;align-items:center}
.v-cp1 .wbody{font-size:38px;line-height:1.55;padding:40px 56px 50px}
.v-cp1 .tests{display:flex;gap:22px}
.tst{flex:1;border-radius:18px;padding:26px 0 22px;text-align:center;border:3px solid}
.tst svg{width:74px;height:74px;display:block;margin:0 auto 14px}
.tst svg path{fill:none;stroke:currentColor;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
.tst span{font:500 24px/1.2 var(--font-mono);letter-spacing:.06em;text-transform:uppercase}
.tst.x{border-color:var(--danger-on-dark);background:var(--coral-tint);color:var(--danger)}
.tst.ok{border-color:var(--positive);background:#e2f1dd;color:var(--positive-ink)}
.v-cp1 .lead{font-size:44px;margin-top:40px}

/* ── mock pair 4: model ⇄ harness ── */
.v-mh{position:relative;width:1728px;height:520px;flex:none}
.v-mh > svg{position:absolute;inset:0;width:1728px;height:520px}
.v-mh .ln-c,.v-mh .ln-t{stroke-width:7}
.v-mh .t-cap{font-size:22px}
.v-mh .box{position:absolute;top:30px;height:400px;border-radius:26px;padding:44px 48px;display:flex;flex-direction:column}
.v-mh .box .k{font:600 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase}
.v-mh .box h3{font:700 84px/1 var(--font-display);letter-spacing:-.03em;margin:18px 0 22px}
.v-mh .box p{font-size:33px;line-height:1.38}
.v-mh .model{left:0;width:500px;background:var(--ink);color:var(--on-dark)}
.v-mh .model .k{color:var(--coral)} .v-mh .model h3{color:var(--on-dark)} .v-mh .model p{color:var(--on-dark-muted)}
.v-mh .harness{left:800px;width:560px;background:var(--coral-soft);border:3px solid var(--coral);color:var(--s-text)}
.v-mh .harness .k{color:var(--coral-ink)}
.v-mh .tool{position:absolute;left:1450px;width:278px;height:78px;border-radius:40px;background:var(--paper-2);border:2px solid var(--line-light);display:flex;align-items:center;justify-content:center;font:500 29px var(--font-mono);color:var(--s-text)}

/* ── mock pair 6: claim chain ── */
.v-chain svg{display:block;width:100%;height:auto}
.v-chain .steps{display:grid;grid-template-columns:500px 500px 500px;justify-content:space-between;margin-top:26px}
.v-chain .steps .n,.v-seq .steps .n{font:500 26px var(--font-mono);color:var(--s-faint);letter-spacing:.08em}
.v-chain .steps h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--coral);margin:8px 0 12px}
.v-chain .steps p{font-size:34px;line-height:1.32;color:var(--s-muted)}
.v-chain .f-mut{fill:var(--on-dark-muted)}

/* ── mock pair 7: problem beat ── */
.v2.pbeat .slide-content{padding:60px 96px 96px 120px}
.pb{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1fr) 720px;column-gap:96px}
.pb-L{display:flex;flex-direction:column;justify-content:flex-end;min-width:0}
.pb-mega{font:700 360px/.8 var(--font-display);letter-spacing:-.05em;color:var(--coral)}
.pb-kick{display:block;font:600 30px var(--font-mono);letter-spacing:.2em;text-transform:uppercase;color:var(--coral);margin:0 0 22px 10px;line-height:1}
.v2.pbeat h2{font-size:84px;line-height:1.02;margin-top:40px}
.pb-lead{font-size:38px;line-height:1.38;color:var(--s-muted);margin-top:30px;max-width:30ch}
.pb-lead .kk{margin-bottom:10px}
.pb-R{display:flex;flex-direction:column;justify-content:center;gap:28px;min-width:0}
.v-ctx{border:2px dashed var(--line-dark);border-radius:22px;padding:30px 30px 34px;background:rgba(28,24,18,.7)}
.v-ctx .cap,.v-ctxp .cap{display:flex;justify-content:space-between;font:500 22px var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--s-faint);margin-bottom:22px}
.v-ctx .bars{display:flex;flex-direction:column;gap:9px}
.v-ctx .bars div{height:34px;border-radius:5px;background:var(--bar-dark);display:flex;align-items:center;padding:0 16px;font:500 18px var(--font-mono);letter-spacing:.06em;color:#7c7260;text-transform:uppercase;white-space:nowrap;overflow:hidden}
.v-ctx .bars div.u{background:var(--coral);color:var(--ink);font-weight:700;font-size:21px;height:42px}
.pb-R .keep{font:700 44px/1.1 var(--font-display);letter-spacing:-.02em;color:var(--on-dark)}
.pb-R .keep span{color:var(--coral)}
.pb-R .keep small{display:block;font:400 28px/1.35 var(--font-body);letter-spacing:0;color:var(--on-dark-muted);margin-top:12px}

/* ── mock pair 8: caching vs compaction ── */
.v-cc .row{display:grid;grid-template-columns:450px 1fr;gap:60px;align-items:center;padding:22px 0}
.v-cc .row+.row{border-top:1px solid var(--s-line)}
.v-cc h3{font:700 64px/1 var(--font-display);letter-spacing:-.03em;color:var(--s-accent)}
.v-cc p{font-size:33px;line-height:1.38;color:var(--s-text);margin-top:18px}
.v-cc svg{display:block;width:1218px;height:250px}
.v-cc .t-mut{font-size:26px;letter-spacing:.06em} .v-cc .t-faint{font-size:24px}
.v-cc .t-acc{font-size:26px} .v-cc .t-paper{font-size:26px} .v-cc .t-danger{font-size:26px}

/* ── mock pair 9: accepted work chart ── */
.v-acc{display:grid;grid-template-columns:1fr 620px;gap:80px;align-items:center}
.v-acc .legend{display:flex;gap:40px;font:500 26px var(--font-mono);letter-spacing:.06em;text-transform:uppercase;color:var(--s-muted);margin-bottom:12px}
.v-acc .legend span{display:flex;align-items:center;gap:12px}
.v-acc .legend i{width:26px;height:26px;border-radius:5px;display:block}
.v-acc .A{background:#8d8271} .v-acc .B{background:var(--coral)}
.v-acc .m{padding:10px 0 12px;border-top:1px solid var(--s-line)}
.v-acc .m .lab{font-size:30px;line-height:1.2;color:var(--s-text);margin-bottom:8px;display:flex;justify-content:space-between;align-items:baseline}
.v-acc .m .lab small{font:500 20px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--s-faint)}
.v-acc .m .lab small.hot{color:var(--s-accent)}
.v-acc .br{display:flex;align-items:center;gap:18px;height:34px}
.v-acc .br+.br{margin-top:6px}
.v-acc .br i{height:100%;border-radius:0 6px 6px 0;display:block}
.v-acc .br b{font:700 30px var(--font-display);color:var(--s-text);white-space:nowrap}
.v-acc .call{background:var(--ink);color:var(--on-dark);border-radius:0 26px 26px 0;padding:40px 52px 44px;border-left:10px solid var(--coral)}
.v-acc .call .k{display:block;font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--on-dark-faint)}
.v-acc .call .big{font:700 116px/.95 var(--font-display);letter-spacing:-.04em;margin-top:14px;white-space:nowrap}
.v-acc .call .big small{font:700 52px var(--font-display);letter-spacing:-.02em;margin-left:14px}
.v-acc .call .big .eq{color:var(--on-dark-faint);font-weight:500}
.v-acc .call .hr{height:1px;background:var(--line-dark);margin:26px 0 24px}
.v-acc .call .big.o{color:var(--coral)}
.v-acc .call p{font-size:30px;line-height:1.35;color:var(--on-dark-muted);margin-top:20px}

/* ── panels ── */
.v-panels{display:grid;gap:40px}
.v-panels.n2{grid-template-columns:repeat(2,minmax(0,1fr))}
.v-panel{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:24px;padding:40px 48px 46px;display:flex;flex-direction:column;min-width:0}
.v-panel .illus{height:270px;display:flex;align-items:center;justify-content:center;margin-bottom:26px}
.v-panel .illus svg{width:100%;height:100%}
.v-panel h3{font:700 64px/1.02 var(--font-display);letter-spacing:-.03em;color:var(--s-text)}
.v-panel p{font-size:36px;line-height:1.35;color:var(--s-muted);margin-top:16px}
.v-panel .kk{margin-bottom:12px}

/* ── rows ── */
.v-rows{display:flex;flex-direction:column;gap:22px}
.v-row{display:grid;grid-template-columns:120px 1fr;grid-template-rows:auto auto;column-gap:36px;align-items:center;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-left:10px solid var(--coral);border-radius:6px 22px 22px 6px;padding:30px 40px}
.v-row .ic{grid-row:1/3;width:110px;height:110px}
.v-row h3{font:700 54px/1.05 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-row p{font-size:34px;line-height:1.35;color:var(--s-muted);margin-top:8px}
.v-row p .kk{display:inline;font-size:22px;margin-right:10px}
.v-rows.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}
.v-rows.grid2 .v-row{padding:40px 44px;min-height:250px}
.v-rows.compact{gap:14px}
.v-rows.compact .v-row{padding:18px 28px;grid-template-columns:72px 1fr;column-gap:24px;background:var(--ink-2)}
.v-rows.compact .ic{width:64px;height:64px}
.v-rows.compact h3{font-size:40px} .v-rows.compact p{font-size:30px;margin-top:4px}
.v-rows.checklist .v-row{grid-template-columns:120px 300px 1fr;grid-template-rows:auto;padding:40px 48px}
.v-rows.checklist .v-row .ic{grid-row:auto}
.v-rows.checklist h3{font-size:64px} .v-rows.checklist p{font-size:40px;color:var(--s-text);margin:0}
.v-rows.keepers .v-row,.v-rows.closing .v-row{background:var(--ink-2)}
.v-rows.keepers{gap:26px} .v-rows.keepers .v-row{padding:36px 40px}
.v-rows.closing{gap:30px}
.v-rows.closing .v-row{grid-template-columns:130px 520px 1fr;grid-template-rows:auto;padding:44px 52px}
.v-rows.closing .v-row .ic{grid-row:auto;width:120px;height:120px}
.v-rows.closing h3{font-size:64px} .v-rows.closing p{font-size:42px;color:var(--on-dark);margin:0}
.v-rows.gates{gap:28px} .v-rows.gates .v-row{padding:36px 40px}

/* ── specific slides ── */
.v-io{display:grid;grid-template-columns:1fr 160px 1fr;align-items:center;gap:28px}
.io-p{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:24px;padding:40px 48px;display:flex;flex-direction:column;gap:22px;height:100%}
.io-p p{font-size:36px;line-height:1.35;color:var(--s-text)}
.io-p .files{display:flex;gap:30px}
.io-p .f{display:flex;flex-direction:column;align-items:center;gap:12px;font:500 24px var(--font-mono);color:var(--s-muted);text-transform:uppercase;letter-spacing:.08em}
.io-p .f .ic{width:120px;height:120px}
.io-p.out{border:3px solid var(--coral);background:var(--s-callout-bg)}
.io-p .outrow{display:grid;grid-template-columns:190px 1fr;gap:34px;align-items:center}
.io-doc{width:190px;height:auto}
.io-doc .d-page{fill:var(--paper);stroke:var(--s-text);stroke-width:4;stroke-linejoin:round}

.v2-report{padding:40px 52px 44px;border:2px solid var(--s-line-strong);background:var(--s-card-bg);border-radius:22px}
.v2-report-head{font:500 26px var(--font-mono);letter-spacing:.08em;color:var(--s-accent);display:flex;justify-content:space-between;margin-bottom:30px}
.v2-report-head span{color:var(--s-muted);font-size:24px;letter-spacing:.02em}
.rp-grid{display:grid;grid-template-columns:1fr 460px;gap:64px;align-items:end}
.v2-report h3{font:700 58px/1.05 var(--font-display);letter-spacing:-.025em;margin-bottom:36px;color:var(--s-text)}
.v2-bars{display:grid;gap:22px}
.v2-bars>div{display:grid;grid-template-columns:130px 1fr 200px;align-items:center;gap:26px;font-size:36px}
.v2-bars i{display:block;width:var(--bar-width);height:72px;background:var(--s-accent);border-radius:0 8px 8px 0}
.v2-bars i.missing{width:100%;height:72px;background:none;border:3px dashed var(--s-muted);border-radius:8px}
.v2-bars b{font:700 52px var(--font-display);color:var(--s-text)}
.v2-bars b.miss{font:600 34px var(--font-mono);color:var(--s-accent);text-transform:uppercase;letter-spacing:.06em}
.rp-side p{font-size:32px;line-height:1.3;color:var(--s-muted)}
.rp-big{display:block;font:700 150px/1 var(--font-display);letter-spacing:-.04em;color:var(--s-accent);margin-top:10px}
.v2-report-flag{display:flex;gap:18px;align-items:flex-start;font-size:32px;line-height:1.3;color:var(--s-text);border-top:1px solid var(--s-line);padding-top:26px;margin-top:30px}
.v2-report-flag .ic{width:56px;height:56px;flex:none}

.v-panels.wide .illus{height:280px}
.v-cycle{display:grid;grid-template-columns:600px 1fr;gap:90px;align-items:center}
.v-cycle svg{width:600px;height:600px}
.v-cycle ol{list-style:none;display:flex;flex-direction:column;gap:34px}
.v-cycle li{display:grid;grid-template-columns:90px 1fr;align-items:baseline;border-top:2px solid var(--s-line);padding-top:24px}
.v-cycle li span{font:500 30px var(--font-mono);color:var(--s-accent)}
.v-cycle h3{font:700 68px/1 var(--font-display);letter-spacing:-.03em;color:var(--s-text)}
.v-cycle li p{font-size:38px;line-height:1.3;color:var(--s-muted);margin-top:10px}
.v-cycle.n4 ol{gap:22px} .v-cycle.n4 li{padding-top:16px} .v-cycle.n4 h3{font-size:56px} .v-cycle.n4 li p{font-size:34px;margin-top:6px}
.v-sup{display:grid;grid-template-columns:800px 1fr;gap:72px;align-items:center}
.v-sup svg{width:800px;height:420px}
.v2 .kcard{padding:44px 52px}
.v2 .kcard .big{font-size:64px;line-height:1.05;letter-spacing:-.025em}
.v2 .kcard p{font-size:36px;line-height:1.38;margin-top:20px}
.v2 .kcard .badges{display:flex;gap:18px;margin-top:28px}
.v2 .kcard .badges span{display:flex;align-items:center;gap:12px;font:500 26px var(--font-mono);color:var(--s-text);text-transform:uppercase;letter-spacing:.06em;border:2px solid var(--s-card-border);border-radius:14px;padding:12px 18px}
.v2 .kcard .badges .ic{width:44px;height:44px}
.v-app{display:grid;grid-template-columns:820px 1fr;gap:64px;align-items:center}
.v-app svg{width:820px;height:auto}
.v-app .ic.stroke-a{stroke:var(--s-accent);color:var(--s-accent)}
.v-acs svg{width:100%;height:auto}
.v-acs .lk{color:var(--s-accent)}
.v-story{display:grid;grid-template-columns:1fr 640px;gap:80px;align-items:center}
.v-story .st-t{display:flex;flex-direction:column;gap:44px}
.v-story .st-i{border-left:8px solid var(--coral);padding-left:36px}
.v-story .st-i p{font-size:44px;line-height:1.3;color:var(--s-text);margin-top:14px}
.v-story .st-ill svg{width:100%;height:auto;max-height:520px}
.v-mx{display:grid;grid-template-columns:800px 1fr;gap:64px;align-items:center}
.v-mx svg{width:800px;height:auto}
.v-mx .v-row{padding:34px 36px}
.v-bound{display:grid;grid-template-columns:1.45fr 1fr;gap:48px;align-items:stretch}
.v-bound .ws{border:4px dashed var(--coral);border-radius:28px;padding:40px 48px;display:flex;flex-direction:column;gap:14px;background:rgba(255,92,53,.06)}
.v-bound p{font-size:38px;line-height:1.3;color:var(--s-text)}
.v-bound .act{margin-top:auto;background:var(--ink-2);border:2px solid var(--line-dark);border-radius:20px;padding:32px 36px;display:flex;flex-direction:column;gap:14px}
.v-bound .chips span{background:var(--ink);border-color:var(--positive-on-dark);color:var(--on-dark)}
.v-bound .chips .ic{color:var(--positive-on-dark)}
.v-bound .lim{border:2px solid var(--line-dark);border-radius:28px;padding:40px 44px;display:flex;flex-direction:column;gap:14px}
.v-bound ul{list-style:none;display:flex;flex-direction:column;gap:14px;margin-top:10px}
.v-bound li{display:flex;align-items:center;gap:20px;font:500 32px var(--font-mono);color:var(--on-dark-muted);text-decoration:line-through;text-decoration-color:rgba(255,92,53,.6)}
.v-bound li .ic{width:40px;height:40px;color:var(--coral)}
.v-seq svg{display:block;width:100%;height:auto}
.v-seq .steps,.v-hand .steps,.v-rec .steps{display:grid;grid-template-columns:repeat(3,1fr);gap:40px;margin-top:20px}
.v-seq .steps h3,.v-hand .steps h3,.v-rec .steps h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text);margin:6px 0 10px}
.v-seq .steps p,.v-hand .steps p,.v-rec .steps p{font-size:36px;line-height:1.3;color:var(--s-muted)}
.v-hand svg,.v-rec svg{display:block;width:100%;height:auto}
.v-hand .steps{text-align:left}
.v-editor .wbody{font-size:44px;line-height:1.55;padding:44px 60px 52px}
.v-editor u{text-decoration:none;border-bottom:6px solid var(--coral);color:var(--code-text)}
.v-editor .flag{display:inline-block;margin-top:14px;color:var(--v-fail);font-weight:700}
.v-editor mark{background:rgba(255,92,53,.22);color:var(--code-text);border-bottom:6px solid var(--coral);padding:0 6px}
.v-anno{display:flex;align-items:center;gap:18px;font:600 30px var(--font-mono);letter-spacing:.04em;color:var(--s-accent);margin-top:-6px}
.v-anno .ic{width:48px;height:48px}
.v-now{display:grid;grid-template-columns:1fr 150px 300px;gap:24px;align-items:center}
.v-now .frame{border:3px solid var(--coral);border-radius:28px;padding:30px 36px 20px;background:var(--s-callout-bg);display:flex;flex-direction:column}
.v-now .cap{font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);margin-bottom:6px}
.v-now .band{display:grid;grid-template-columns:90px 280px 1fr;align-items:center;gap:26px;padding:24px 0}
.v-now .band+.band{border-top:1px solid var(--line-card)}
.v-now .band .ic{width:80px;height:80px}
.v-now .band h3{font:700 56px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-now .band p{font-size:34px;line-height:1.3;color:var(--s-text)}
.v-now .mdl{width:300px;height:300px;border-radius:50%;background:var(--ink);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px}
.v-now .mdl .ic{width:110px;height:110px;color:var(--coral)}
.v-now .mdl b{font:700 52px var(--font-display);color:var(--paper)}
.v-more{display:grid;grid-template-columns:1fr 1fr;gap:56px;align-items:center}
.v-two{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.v-ctxp{border:2px dashed var(--s-line-strong);border-radius:20px;padding:24px 24px 26px;background:var(--s-card-bg);height:100%}
.v-ctxp .bars{display:flex;flex-direction:column;gap:8px}
.v-ctxp .bars div{height:26px;border-radius:5px;background:var(--s-bar)}
.v-ctxp .bars div.u{background:var(--coral);height:30px}
.v-think{display:grid;grid-template-columns:1fr 120px 1.25fr;align-items:center;gap:20px}
.v-think .th{border-radius:26px;padding:44px 48px;display:flex;flex-direction:column;gap:18px;height:100%}
.v-think .th-a{border:3px dashed var(--line-dark);color:var(--on-dark-muted)}
.v-think .th-a .ic{width:120px;height:120px;color:var(--on-dark-faint)}
.v-think .th-a h3{color:var(--on-dark-muted)}
.v-think .th-b{border:3px solid var(--coral);background:rgba(255,92,53,.08)}
.v-think .evs{display:flex;gap:22px} .v-think .evs .ic{width:110px;height:110px}
.v-think .evs .ic:last-child{color:var(--positive-on-dark)}
.v-think h3{font:700 60px/1.05 var(--font-display);letter-spacing:-.025em;color:var(--on-dark);margin-top:auto}
.v-think p{font-size:38px;line-height:1.35}
.v-think .neq{font:500 140px/1 var(--font-display);color:var(--on-dark-faint);text-align:center}
.v-diff .wbody{padding:28px 0 36px;white-space:normal}
.v-diff .dl{display:grid;grid-template-columns:80px 1fr 150px;align-items:center;font:500 40px/1.5 var(--font-mono);padding:12px 0;min-height:40px}
.v-diff .dl .g{text-align:center;font-weight:700}
.v-diff .dl .tg{font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;text-align:right;padding-right:40px}
.v-diff .del{background:rgba(255,95,87,.14);color:#ffb4a6} .v-diff .del .g,.v-diff .del .tg{color:var(--v-fail)}
.v-diff .add{background:rgba(127,220,138,.14);color:#c9f2cd} .v-diff .add .g,.v-diff .add .tg{color:var(--positive-on-dark)}
.v-diff .add b{color:var(--coral);font-weight:700;border-bottom:5px solid var(--coral)}
.v-diff .ctx .c{color:var(--code-comment)}
.v-tests{display:grid;grid-template-columns:repeat(3,1fr);gap:36px}
.v-tests .tc{position:relative;background:var(--s-card-bg);border:3px solid var(--positive);border-radius:24px;padding:36px 40px 40px}
.v-tests .tc .kk{color:var(--s-faint);font-size:22px}
.v-tests .cs{font:500 44px var(--font-mono);color:var(--s-text);margin:8px 0 26px}
.v-tests .ex{font:700 120px/1 var(--font-display);letter-spacing:-.035em;color:var(--positive-ink);margin-top:6px}
.v-tests .tc .ic{position:absolute;top:30px;right:30px;width:74px;height:74px;color:var(--positive)}
.v-int{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.v-int svg{width:100%;height:auto;margin-bottom:20px}
.v-int .ic{color:var(--on-dark)}
.v-int .ic.stp{color:var(--coral)}
.v-int h3{font:700 64px/1 var(--font-display);letter-spacing:-.025em;color:var(--on-dark)}
.v-int p{font-size:36px;line-height:1.3;color:var(--on-dark-muted);margin-top:14px}
.v-int .ln-m{stroke:var(--on-dark-faint)}
.v-rules{display:grid;grid-template-columns:1fr 470px;gap:64px;align-items:center}
.v-rules .rs svg{width:460px;height:auto;margin-top:18px}
.v-reach{display:grid;grid-template-columns:1fr 380px 1fr;gap:0;align-items:center;position:relative}
.v-reach::before{content:"";position:absolute;left:12%;right:12%;top:50%;border-top:6px dashed var(--coral);z-index:0}
.v-reach .zone{position:relative;z-index:1;border-radius:28px;padding:40px 44px;display:flex;flex-direction:column;gap:12px;min-height:470px}
.v-reach .zone.in{border:4px solid var(--s-text);background:var(--s-card-bg)}
.v-reach .zone.out{border:4px dashed var(--s-line-strong);background:var(--s-bg)}
.v-reach .zone .ic{width:120px;height:120px;margin:10px 0}
.v-reach h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-reach p{font-size:34px;line-height:1.32;color:var(--s-muted)}
.v-reach .gate{position:relative;z-index:1;text-align:center;padding:0 30px;display:flex;flex-direction:column;align-items:center;gap:10px}
.v-reach .lockc{width:180px;height:180px;border-radius:50%;background:var(--coral);display:flex;align-items:center;justify-content:center;box-shadow:0 0 0 14px var(--s-bg)}
.v-reach .lockc .ic{width:100px;height:100px;color:var(--ink)}
.v-reach .gate h3{margin-top:22px}
.v-reach .gate p{background:var(--s-bg)}
.v-one{display:grid;grid-template-columns:1fr 1.25fr;gap:44px}
.v-one .ex,.v-one .q{border-radius:26px;padding:44px 48px;display:flex;flex-direction:column;gap:18px}
.v-one .ex{background:var(--s-card-bg);border:1.5px solid var(--s-card-border)}
.v-one .ex p{font-size:36px;line-height:1.35;color:var(--s-text)}
.v-one .ex .chips{margin-top:auto}
.v-one .q{background:var(--ink);color:var(--on-dark);position:relative;border-left:12px solid var(--coral);border-radius:6px 26px 26px 6px}
.v-one .q .kk{color:var(--coral)}
.v-one .q p{font:700 60px/1.1 var(--font-display);letter-spacing:-.025em;color:var(--on-dark);max-width:17ch}
.v-one .q .ic{position:absolute;right:40px;bottom:40px;width:120px;height:120px;color:var(--coral);opacity:.9}
.v-panels.wide .v-panel .illus svg{max-width:720px}
.v-spec{background:var(--ink-2);border:2px solid var(--line-dark);border-radius:26px;padding:40px 44px}
.v-spec .sh{font:700 60px/1 var(--font-display);color:var(--on-dark);margin-bottom:28px}
.v-spec .fields{display:flex;flex-direction:column;gap:16px;margin:16px 0 24px}
.v-spec .fr{display:grid;grid-template-columns:1fr 150px;gap:20px;align-items:center;font:500 34px var(--font-mono);color:var(--on-dark-muted)}
.v-spec .fr i{font-style:normal;height:66px;border:3px dashed var(--coral);border-radius:12px;display:flex;align-items:center;justify-content:center;font:700 44px var(--font-display);color:var(--coral)}
.v-spec .sub{font-size:30px;line-height:1.35;color:var(--on-dark-muted)}
.v-contract .hd{display:grid;grid-template-columns:70px 1fr 90px 1fr;gap:24px;font:600 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);padding:0 36px 14px}
.v-contract .hd span:first-child{grid-column:2} .v-contract .hd span:last-child{grid-column:4}
.v-contract .cr{display:grid;grid-template-columns:70px 1fr 90px 1fr;gap:24px;align-items:center;padding:24px 36px;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:18px}
.v-contract .cr+.cr{margin-top:16px}
.v-contract .no{font:500 28px var(--font-mono);color:var(--s-faint)}
.v-contract .rq{font-size:36px;line-height:1.3;color:var(--s-text);font-weight:500}
.v-contract .ck{font:500 32px/1.3 var(--font-mono);color:var(--s-text);display:flex;align-items:center;gap:18px}
.v-contract .ck .ic{width:44px;height:44px;flex:none;color:var(--positive)}
.v2 .ar{width:80px;height:40px}
.v2 .ar path{fill:none;stroke:var(--coral);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.v-zero .wbody{font:500 48px/1.2 var(--font-mono);padding:40px 48px 44px}
.v-zero .zero{font:700 200px/1 var(--font-display);color:var(--positive-on-dark);vertical-align:middle;margin-left:20px}
.v-qs{display:flex;flex-direction:column;gap:14px}
.v-qs span{display:flex;align-items:center;gap:18px;font:500 32px var(--font-mono);color:var(--on-dark-muted);border:2px dashed var(--line-dark);border-radius:16px;padding:14px 24px}
.v-qs .ic{width:40px;height:40px;color:var(--coral)}
.v-claim{display:grid;grid-template-columns:1fr 90px 1.15fr 90px 1fr;align-items:stretch;gap:18px}
.v-claim .io-arrow{width:90px;align-self:center}
.v-claim .c1{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-top:10px solid var(--coral);border-radius:6px 6px 22px 22px;padding:40px 40px 44px;display:flex;flex-direction:column;gap:18px;position:relative}
.v-claim .c1.bnd{border:3px dashed var(--s-line-strong);border-top:10px dashed var(--s-line-strong);background:transparent}
.v-claim h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text);margin-top:auto}
.v-claim p{font-size:34px;line-height:1.35;color:var(--s-muted)}
.v-claim .q{font:700 200px/.6 var(--font-display);color:var(--coral);height:110px}
.v-claim .cmp{display:flex;flex-direction:column;align-items:flex-start;gap:6px;font:500 30px var(--font-mono);color:var(--s-text)}
.v-claim .cmp code{font:inherit;background:var(--code-bg);color:var(--code-string);padding:8px 16px;border-radius:10px}
.v-claim .cmp span{color:var(--s-accent);font-weight:700;padding-left:16px}
.v-claim .cmp .ic{width:54px;height:54px;color:var(--positive)}
.v-claim .bnd .ic{width:110px;height:110px;color:var(--s-muted)}
.v-editor.calc .wbody{font-size:46px}
.v-ta{display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:stretch}
.v-ta > div{display:flex;flex-direction:column;gap:22px;min-width:0}
.v-ta .v-win{flex:1}
.v-okterm .wbody{font-size:24px;line-height:1.6;padding:30px 36px 34px;overflow-wrap:normal}
.v-okterm .ok{color:var(--positive-on-dark);font-weight:700}
.v-okterm .okb{color:var(--positive-on-dark);font-weight:700;font-size:40px}
.v-csvwin .wbody{font-size:27px;line-height:1.6;padding:30px 36px 34px;overflow-wrap:normal}
.v-csvwin .hl{background:rgba(255,92,53,.18);box-shadow:0 0 0 6px rgba(255,92,53,.18);border-radius:4px}
.v-csvwin u{text-decoration:none;border-bottom:4px solid var(--coral)}
.v-bycheck{display:flex;align-items:center;gap:18px;font:600 32px var(--font-mono);color:var(--s-text)}
.v-bycheck b{color:var(--s-accent)}
.v-bycheck .ic{width:52px;height:52px;flex:none;color:var(--positive)}
.v-actors{display:grid;grid-template-columns:1fr 200px 1fr;align-items:center}
.v-actors .actor{border-radius:28px;padding:44px 48px;display:flex;flex-direction:column;gap:18px;min-height:480px}
.v-actors .ag{background:var(--ink);color:var(--on-dark)}
.v-actors .ag .ic{color:var(--coral);width:120px;height:120px}
.v-actors .ag h3{color:var(--on-dark)} .v-actors .ag p{color:var(--on-dark-muted)}
.v-actors .ag .chips span{background:var(--ink-2);color:var(--on-dark);border-color:var(--line-dark)}
.v-actors .rv{background:var(--coral-soft);border:3px solid var(--coral)}
.v-actors .rv > .ic{width:120px;height:120px}
.v-actors h3{font:700 64px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-actors p{font-size:36px;line-height:1.35;color:var(--s-text)}
.v-actors .gate{display:flex;gap:16px;margin-top:auto}
.v-actors .gate .ic{width:64px;height:64px;border-radius:50%;padding:12px;background:var(--paper)}
.v-actors .gate .ic:first-child{color:var(--positive)}
.v-stages{display:grid;grid-template-columns:repeat(4,1fr);gap:28px}
.v-stages .k{grid-column:1/-1;font:600 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);margin-bottom:-6px}
.v-stages .sc{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-top:10px solid var(--s-text);border-radius:6px 6px 22px 22px;padding:36px 32px 40px;display:flex;flex-direction:column;gap:16px;min-height:430px}
.v-stages h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text);margin-bottom:16px}
.v-stages .sc span{font:500 30px/1.25 var(--font-mono);color:var(--s-text);background:var(--s-bg);border:2px solid var(--s-card-border);border-radius:14px;padding:16px 20px}
.v-stages .sc span.hot{background:var(--coral);border-color:var(--coral);color:var(--ink);font-weight:600}
.v-note .wbody{white-space:normal;padding:28px 52px 36px}
.v-note .kv{display:grid;grid-template-columns:170px 1fr;gap:28px;align-items:baseline;padding:16px 0;font:500 36px/1.35 var(--font-mono)}
.v-note .kv+.kv{border-top:1px solid var(--line-light-2)}
.v-note .kv b{color:var(--coral-ink);font-weight:700}
.v-tree{display:grid;grid-template-columns:230px 1fr;gap:40px;align-items:center}
.v-tree .root{display:flex;flex-direction:column;align-items:center;gap:16px;background:var(--ink);border-radius:28px;padding:40px 20px;color:var(--paper);font:700 44px var(--font-display)}
.v-tree .root .ic{width:100px;height:100px;color:var(--coral)}
.v-tree .branches{border-left:6px solid var(--coral);padding-left:40px;display:flex;flex-direction:column;gap:16px}
.v-tree .hd{display:grid;grid-template-columns:1fr 80px 1.1fr;gap:24px;font:600 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent)}
.v-tree .hd span:last-child{grid-column:3}
.v-tree .tr{display:grid;grid-template-columns:1fr 80px 1.1fr;gap:24px;align-items:center}
.v-tree .tr .f{font-size:36px;line-height:1.3;color:var(--s-text);font-weight:500;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:16px;padding:22px 28px}
.v-tree .nx{display:flex;align-items:center;gap:22px}
.v-tree .nx .ic{width:64px;height:64px;flex:none}
.v-tree .nx p{font-size:34px;line-height:1.3;color:var(--s-text)}
.v-frac{display:flex;flex-direction:column;gap:0}
.v-frac .num,.v-frac .den{background:var(--ink-2);border:2px solid var(--line-dark);border-radius:24px;padding:36px 40px;display:flex;flex-direction:column;gap:14px}
.v-frac p{font-size:36px;line-height:1.3;color:var(--on-dark)}
.v-frac .chips span{background:var(--ink);color:var(--on-dark);border-color:var(--line-dark);font-size:26px;padding:8px 18px}
.v-frac .bar{position:relative;height:120px;display:flex;align-items:center;justify-content:center}
.v-frac .bar::before{content:"";position:absolute;left:0;right:0;top:50%;height:8px;margin-top:-4px;background:var(--coral);border-radius:4px}
.v-frac .bar span{position:relative;font:700 80px/1 var(--font-display);color:var(--coral);background:var(--ink);padding:0 26px}
.v-frac .den{border-color:var(--coral)}
.v-deleg{display:grid;grid-template-columns:1fr 420px;gap:56px;align-items:center}
.v-brief.dl .ln{grid-template-columns:1fr auto;padding:14px 20px;font-size:34px}
.v-brief.dl .ln b{all:unset;color:var(--coral-ink);font-weight:700}
.v-brief.dl .ln.lk{background:var(--coral-soft);border-left-color:var(--coral)}
.v-brief.dl .ln .ic{width:44px;height:44px;color:var(--coral-ink)}
.v-deleg > svg{width:420px;height:auto}
.v-fan{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:36px;align-items:stretch}
.v-fan .wk,.v-fan .fi{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:24px;padding:36px 40px;display:flex;flex-direction:column;gap:12px}
.v-fan .wk svg{width:100%;height:auto;margin-bottom:auto}
.v-fan .fi .ic{width:130px;height:130px;margin-bottom:auto}
.v-fan .fi.hot{border:3px solid var(--coral);background:var(--s-callout-bg)}
.v-fan h3{font:700 60px/1 var(--font-display);letter-spacing:-.025em;color:var(--s-text);margin-top:10px}
.v-fan p{font-size:34px;line-height:1.32;color:var(--s-muted)}
.v-skill .wbody{white-space:normal;padding:36px 56px 40px}
.v-skill .h{font:700 44px var(--font-mono);margin-bottom:18px}
.v-skill ol{list-style:none;display:flex;flex-direction:column;gap:6px}
.v-skill li{display:flex;align-items:center;gap:24px;font:500 38px/1.4 var(--font-mono);padding:10px 0}
.v-skill li span{display:inline-flex;align-items:center;justify-content:center;width:60px;height:60px;border-radius:50%;background:var(--ink);color:var(--paper);font:700 28px var(--font-mono);flex:none}
.v-skill li.own{background:var(--coral-soft);border-radius:14px;padding:10px 20px 10px 0;margin-left:-4px}
.v-skill li.own span{background:var(--coral);color:var(--ink)}
.v-skill li .ic{width:50px;height:50px;margin-left:auto;color:var(--coral-ink)}
.v2 .ic.inv{color:var(--coral)}
.v-way .rail .nd{fill:var(--ink);stroke:var(--s-bg);stroke-width:10}
.v-lcards{display:grid;gap:36px}
.v-lcards.n3{grid-template-columns:repeat(3,1fr)}
.v-lcard{display:flex;flex-direction:column;gap:16px;min-height:480px;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-top:10px solid var(--coral);border-radius:6px 6px 22px 22px;padding:44px 44px 48px;text-decoration:none;color:var(--s-text)}
.v-lcard:hover{border-color:var(--coral)}
.v-lcard .ic{width:130px;height:130px;margin-bottom:auto}
.v-lcard .lt{font:700 52px/1.08 var(--font-display);letter-spacing:-.025em;color:var(--s-text)}
.v-lcard .ld{font:500 24px/1.3 var(--font-mono);color:var(--s-muted);overflow-wrap:anywhere}
.v-lcard .ld b{color:var(--s-accent)}
.v-refs{display:grid;grid-template-columns:1fr;gap:0}
.v-refs a{display:grid;grid-template-columns:1fr auto;grid-template-rows:auto auto;column-gap:30px;align-items:center;padding:26px 8px;border-bottom:2px solid var(--s-line);text-decoration:none;color:var(--s-text)}
.v-refs a:first-child{border-top:2px solid var(--s-line)}
.v-refs a:hover .lt{color:var(--s-accent)}
.v-refs .lt{font:700 50px/1.1 var(--font-display);letter-spacing:-.02em}
.v-refs .ld{font:500 26px var(--font-mono);color:var(--s-muted);margin-top:8px;grid-column:1}
.v-refs .la{grid-row:1/3;grid-column:2;font:700 52px var(--font-display);color:var(--s-accent)}
.v-refs.n5 a{padding:18px 8px} .v-refs.n5 .lt{font-size:46px}
.v-decks{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}
.v-decks .dk{display:grid;grid-template-columns:170px 1fr;grid-template-rows:auto auto;column-gap:28px;align-items:center;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:22px;padding:34px 40px;text-decoration:none;color:var(--s-text);min-height:230px}
.v-decks .no{grid-row:1/3;font:700 120px/1 var(--font-display);letter-spacing:-.05em;color:var(--coral)}
.v-decks .lt{font:700 44px/1.1 var(--font-display);letter-spacing:-.02em}
.v-decks .ld{font:500 24px var(--font-mono);color:var(--s-muted);margin-top:10px}
.v-decks .ld b{color:var(--s-accent)}

/* ── video ── */
.v2-media{display:grid;grid-template-columns:auto 1fr;gap:64px;align-items:center;min-height:0;text-align:left}
.v2-media video{display:block;width:auto;height:600px;max-width:none;border-radius:18px;background:var(--ink-3)}
.v2-media .vm-side{display:flex;flex-direction:column;gap:30px;min-width:0}
.v2-media figcaption{font-size:34px;line-height:1.35;color:var(--s-muted)}
.vm-steps{list-style:none;display:flex;flex-direction:column;gap:18px}
.vm-steps li{display:flex;gap:24px;align-items:baseline;font:700 50px/1.1 var(--font-display);letter-spacing:-.02em;color:var(--s-text);border-top:2px solid var(--s-line);padding-top:18px}
.vm-steps li span{font:500 28px var(--font-mono);color:var(--coral);letter-spacing:.06em}
.v2-play{align-self:flex-start;white-space:nowrap;padding:16px 30px;font:600 26px var(--font-mono);letter-spacing:.04em;color:var(--s-accent);background:transparent;border:2px solid var(--s-accent);border-radius:40px;cursor:pointer}
.v2-play:hover{background:var(--s-callout-bg)}
.v2-play:focus-visible{outline:3px solid var(--s-accent);outline-offset:5px}
.v2-media.stacked{grid-template-columns:1fr;gap:22px}
.v2-media.stacked video{width:100%;height:auto}
.v2-media.stacked .vm-side{flex-direction:row;align-items:center;justify-content:space-between;gap:24px}
.v2-media.stacked figcaption{font-size:26px}


/* ── pass 2 sizing ── */
.io-p{padding:48px 56px;min-height:470px;justify-content:center}
.io-p .f .ic{width:150px;height:150px}
.io-p p{font-size:40px}
.io-p .outrow{grid-template-columns:230px 1fr}
.io-doc{width:230px}
.v-panel .illus{height:300px}
.v-panels.wide .illus{height:320px}
.v2-media video{height:640px}
.v2-media figcaption{font-size:40px}
.v-story{grid-template-columns:1fr 700px}
.v-refs a{padding:34px 8px}
.v-refs .lt{font-size:56px}
.v-refs.n5 a{padding:20px 8px} .v-refs.n5 .lt{font-size:50px}
.v-rows.checklist{gap:28px} .v-rows.checklist .v-row{padding:46px 48px}
.v-reach{align-items:start}
.v-reach::before{top:130px}
.v-reach .gate{padding-top:40px}
.v-one .ex,.v-one .q{min-height:430px}
.v-one .q p{font-size:68px}
.v2 .io-arrow.big{width:200px;height:120px}
.v-actors .actor{min-height:540px}
.v-actors .gate .ic{width:96px;height:96px;padding:18px}
.v-ctx{padding:24px 26px 26px}
.v-ctx .cap{margin-bottom:16px}
.v-ctx .bars{gap:7px}
.v-ctx .bars div{height:27px;font-size:16px}
.v-ctx .bars div.u{height:36px;font-size:20px}
.pb-R .keep{font-size:40px}
.v-brief.dl .ln{display:flex;justify-content:space-between}
.v-deleg{grid-template-columns:1fr 480px}
.v-deleg > svg{width:480px}
.v-deleg .t-strong{font-size:36px} .v-deleg .sm{font-size:26px}
.v-fan .wk svg{max-height:none}
.v-fan .fi .ic{width:120px;height:120px}
.v-skill li{padding:3px 0;font-size:36px}
.v-skill ol{gap:4px}
.v-skill .h{margin-bottom:10px}
.v-skill .wbody{padding:28px 56px 32px}
.v-rows.closing .v-row{grid-template-columns:130px 580px 1fr;padding:34px 52px}
.v-rows.closing h3{font-size:60px}
.v-decks .no .sep{font-size:0}
.v-decks .lt{font-size:46px}
.v-decks .dk{grid-template-columns:130px 1fr;min-height:0;padding:26px 36px}
.v-decks .no{font-size:92px}
.v-decks .ld{font-size:22px;margin-top:6px}
.v-decks .wip{display:inline-block;vertical-align:middle;margin-left:14px;font:600 20px/1 var(--font-mono);letter-spacing:.12em;color:var(--s-muted);border:2px solid var(--s-line-strong);border-radius:8px;padding:6px 10px}
.v-way .rail{max-height:420px}

.v-legend{display:flex;gap:40px;font:600 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);margin-bottom:-14px}
.v-legend span+span::before{content:"→ ";color:var(--s-faint)}
.v-acc .legend b{font-weight:600;color:var(--s-accent)}
.v-think .th{min-height:500px;padding:52px 56px}
.v-think h3{font-size:64px} .v-think p{font-size:40px}
/* reference slides: calmer title */
.v2.ref h2{font-size:80px}

.v2.title-slide .ts-hero h1{font-size:184px;line-height:.95}
.v2.title-slide .ts-sub{font-size:44px;max-width:45ch;line-height:1.35}
@media (prefers-reduced-motion:reduce){
 .v2 *,.v2 *::before,.v2 *::after{animation:none!important;transition:none!important}
}
/* Canvas scaling already handles short screens; hide only optional UI. */
@media (max-height:700px){.pui-controls{bottom:8px}}
@media (max-height:600px){.pui-controls button{padding:7px 10px}}
@media (max-height:500px){.pui-notes{max-height:50vh}}
'''

VIDEO_JS = '''
<script>
// Play only the active explainer; reduced-motion users start it explicitly.
(function(){
 const ds=document.querySelector('deck-stage');
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 ds.querySelectorAll('.v2-media').forEach(figure=>{
  const v=figure.querySelector('video'),button=figure.querySelector('[data-video-toggle]');
  function sync(){button.textContent=v.paused?'Play animation':'Pause animation';button.setAttribute('aria-pressed',String(!v.paused));}
  button.addEventListener('click',()=>{if(v.paused)v.play().catch(()=>{});else v.pause();});
  v.addEventListener('play',sync);v.addEventListener('pause',sync);sync();
 });
 function update(){
  ds.querySelectorAll('video').forEach(v=>{
   if(!v.closest('[data-deck-active]') || motion.matches){v.pause();return;}
   v.currentTime=0;v.play().catch(()=>{});
  });
 }
 ds.addEventListener('slidechange',update);motion.addEventListener('change',update);update();
})();
</script>
'''


def render(i, s, number):
    attrs = f'id="slide-{i}" data-label="{esc(plain(s["title"]), quote=True)}" data-speaker-notes="{esc(s["notes"], quote=True)}"'
    if 'hero' in s:
        return f'''<section class="slide dark title-slide v2" {attrs}>
<div class="ts-top"><span class="k">{s['audience']}</span><span class="meta">September 2026</span></div>
<div class="ts-hero"><h1>{s['hero']}<span class="dot">.</span></h1><p class="ts-sub">{s['subtitle']}</p></div>
<div class="ts-foot"><div class="ts-author"><a href="https://davidbudac.cz" target="_blank" rel="noopener">David Budáč</a></div><div class="ts-loopline">{number:02} / 03 · Revised edition</div></div></section>'''
    foot = f'<p class="note">{s["foot"]}</p>' if s['foot'] else ''
    cls = ('dark' if s['dark'] else 'light') + ' v2' + (' ' + s['cls'] if s.get('cls') else '')
    head = f'<div class="slide-head"><span class="snum">{i:02}</span>{s.get("head", "")}<div class="crumb">{s["chapter"]}</div></div>'
    style = f' style="--h2-size:{s["tsize"]}px"' if s.get('tsize') else ''
    if s.get('layout') == 'problem':
        heading = s['title'].split(' · ', 1)[1]
        heading = heading[0].upper() + heading[1:]
        lead = f'<p class="pb-lead">{s["plead"]}</p>' if s.get('plead') else ''
        return f'''<section class="slide {cls} pbeat" {attrs}>
<div class="slide-content">{head}<div class="pb"><div class="pb-L"><div class="pb-mega"><span class="pb-kick">Problem</span>{s['pnum']:02}</div>
<h2>{heading}</h2>{lead}</div><div class="pb-R">{s['body']}</div></div>{foot}</div></section>'''
    return f'''<section class="slide {cls}" {attrs}{style}>
<div class="slide-content">{head}
<h2>{s['title']}</h2><div class="v2-body">{s['body']}</div>{foot}</div></section>'''


def build(original, slides, number):
    text = (ROOT / original).read_text()
    head = text[:text.index('</head>')]
    head = re.sub(r'<title>.*?</title>', '<title>' + esc(slides[0]['title']) + ' · v2</title>', head, flags=re.S)
    # Self-host the existing bundled fonts; do not change the originals or shared CSS.
    head = re.sub(r'<link[^>]+(?:fonts.googleapis.com|fonts.gstatic.com)[^>]*>\s*', '', head)
    token_css = '\n'.join(f'<link rel="stylesheet" href="ember_design_system/tokens/{n}.css">' for n in ['colors', 'typography', 'spacing', 'effects'])
    head = head.replace('<link rel="stylesheet" href="ember_design_system/styles.css">', token_css)
    font_css = ''
    for family, prefix in [('Space Grotesk', 'space-grotesk'), ('IBM Plex Sans', 'ibm-plex-sans'), ('IBM Plex Mono', 'ibm-plex-mono')]:
        for weight in [400, 500, 600, 700]:
            font_css += f'@font-face{{font-family:"{family}";font-weight:{weight};font-style:normal;font-display:swap;src:url("remotion/public/fonts/{prefix}-{weight}.woff2") format("woff2")}}\n'
    head += '<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n' + font_css + CSS + '\n</style>\n</head>\n<body>\n'
    out = original.replace('.html', '-v2.html')
    # Wayfinding for talk 03: a problem tracker on every slide inside a problem chapter.
    current = 0
    for s in slides:
        if s.get('layout') == 'problem':
            current = s['pnum']
        if s.get('track'):
            s['head'] = tracker(s['track'])
            current = 0
        elif current and 'hero' not in s and 'head' not in s:
            s['head'] = tracker(current)
    sections = [render(i, s, number) for i, s in enumerate(slides, 1)]
    tail = text[text.index('</deck-stage>'):]
    # Replace the inherited unconditional video playback with active/reduced-motion handling.
    tail = re.sub(r'<script>\s*/\* restart embedded explainer videos.*?</script>', '', tail, flags=re.S)
    # Initialise presenter notes at the actual deep-linked slide, even before a nav event.
    tail = tail.replace('var current = 0, presenter = null, mouseT = null;', "var current = Math.max(0, Array.from(ds.children).findIndex(s => s.hasAttribute('data-deck-active'))), presenter = null, mouseT = null;")
    # Inherited presenter strings: no em dashes in visible text.
    tail = tail.replace('blocked the pop-up \u2014 allow', 'blocked the pop-up. Allow').replace('<title>Presenter \u2014 ', '<title>Presenter · ')
    tail = tail.rsplit('</body>', 1)[0] + VIDEO_JS + '\n</body>' + tail.rsplit('</body>', 1)[1]
    result = head + '<!-- Derived from ' + original + '; content source: scripts/build_first_three_v2.py -->\n<deck-stage width="1920" height="1080" no-rail>\n' + '\n\n'.join(sections) + '\n' + tail
    (ROOT / out).write_text(result)
    rows_ = ['# ' + slides[0]['title'] + ' · v2 slide map', '', f'{len(slides)} slides. Original references use physical section numbers; originals remain unchanged.', '', '| New | Title | Original material |', '|---|---|---|']
    notes = ['# ' + slides[0]['title'] + ' · v2 speaker notes', '', 'Navigation: arrows / Space; Home / End; N notes; P presenter window; F fullscreen. Direct links use # followed by the physical slide number.', '']
    for i, s in enumerate(slides, 1):
        rows_.append(f'| {i} | {plain(s["title"])} | {s["origin"]} |')
        notes += [f'## {i}. {plain(s["title"])}', '', s['notes'], '']
    (REVIEW / (out.replace('.html', '-map.md'))).write_text('\n'.join(rows_) + '\n')
    (REVIEW / (out.replace('.html', '-notes.md'))).write_text('\n'.join(notes).rstrip() + '\n')
    print(out, len(slides), 'slides')


def artifacts():
    folder = ROOT / 'examples/v2'
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'review-data.csv').write_text('month,completed_orders\nApril,80\nMay,120\nJune,\n')
    html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Example review report</title><style>
body{font-family:system-ui,sans-serif;background:#f8f5f0;color:#242019;margin:0;padding:clamp(20px,5vw,70px)}main{max-width:1000px;margin:auto}h1{font-size:clamp(30px,5vw,52px)}p,li{font-size:20px;line-height:1.5}table{border-collapse:collapse;width:100%;font-size:22px}td,th{text-align:left;padding:18px;border-bottom:1px solid #c7bfb2}.gap{color:#a93819}a{color:#a93819}aside{border-left:4px solid #a93819;padding-left:20px;margin-top:32px}footer{margin-top:40px;font-size:16px}</style>
<main><p>Teaching example · synthetic data · draft</p><h1>April–May grew. June is incomplete.</h1><table><thead><tr><th scope="col">Month</th><th scope="col">Completed orders</th></tr></thead><tbody><tr><th scope="row">April</th><td>80</td></tr><tr><th scope="row">May</th><td>120</td></tr><tr><th scope="row">June</th><td class="gap">Missing</td></tr></tbody></table><p>May increased by 40 completed orders compared with April: (120 − 80) / 80 = <strong>50%</strong>.</p><aside><h2>Review required</h2><p>A complete Q2 total cannot be calculated from this file. Supply June before presenting quarterly results.</p></aside><footer>Source: <a href="review-data.csv" download>review-data.csv</a>. Created for The AI Toolbox v2. This artifact demonstrates the desired output; it is not evidence of a particular vendor run.</footer></main></html>'''
    (folder / 'review-report.html').write_text(html + '\n')
    # Import only the committed reference fixture; there are no external side effects.
    import sys
    sys.path.insert(0, str(folder / 'invoice/after'))
    from export import export_invoices
    rows_ = [dict(invoice_id='INV-001', customer='North, Ltd', net='100.00', tax_rate='0.21'), dict(invoice_id='INV-002', customer='Studio "A"', net='0.50', tax_rate='0.21'), dict(invoice_id='INV-003', customer='Line\nbreak', net='100.00', tax_rate='0')]
    (folder / 'invoices.csv').write_text(export_invoices(rows_))
    # Posters match each video's aspect ratio so the frame does not jump when it loads.
    posters = ROOT / 'assets/v2'
    posters.mkdir(parents=True, exist_ok=True)
    for name, labels in [('agent-loop-dark', ['Choose action', 'Run tool', 'Read result']), ('subagents-dark', ['Bounded task', 'Separate worker', 'Evidence back'])]:
        w, h = VIDEO_SIZE[name]
        bw = (w - 160) // 3
        boxes = ''.join(f'<rect x="{40+i*(bw+40)}" y="{h//2-120}" width="{bw}" height="210" rx="18" fill="#211d16" stroke="#ff5c35" stroke-width="3"/><text x="{40+i*(bw+40)+bw//2}" y="{h//2-5}" text-anchor="middle" fill="#f8f5f0" font-size="34" font-family="sans-serif">{label}</text>' for i, label in enumerate(labels))
        poster = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="#0e0c08"/>{boxes}<text x="{w//2}" y="{h//2+180}" text-anchor="middle" fill="#ff5c35" font-size="28" font-family="sans-serif">Press play to view the animation</text></svg>'
        (posters / (name + '.svg')).write_text(poster + '\n')


def main():
    REVIEW.mkdir(parents=True, exist_ok=True)
    hashes = json.loads((REVIEW / 'original-hashes.json').read_text())
    for path in ['ai-toolbox.html', 'agentic-ai.html', 'agentic-engineering.html']:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == hashes[path], f'Original changed: {path}'
    artifacts()
    for n, (original, slides) in enumerate([('ai-toolbox.html', TOOLBOX), ('agentic-ai.html', INTRO), ('agentic-engineering.html', ENGINEERING)], 1):
        build(original, slides, n)


if __name__ == '__main__':
    main()
