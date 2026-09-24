#!/usr/bin/env python3
"""Build evals-workshop.html (the hands-on evals workshop deck).

Borrows the Ember <deck-stage> head styles and the presenter code from
measuring-what-works.html, then adds the workshop layer: a lab tracker in
every header, lab beats, "Do this" slides with a presenter-controlled time box,
debriefs and breaks. Run from anywhere; writes to the repo root.
"""
import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = (REPO / "measuring-what-works.html").read_text(encoding="utf-8")
OUT = REPO / "evals-workshop.html"
BOARD = "https://claude.ai/artifact/MgSgfU5azvZ7JpKynnGUrc"

head_start = SRC.index('<link rel="stylesheet" href="ember_design_system/tokens/colors.css">')
head_end = SRC.index("</head>")
BASE_HEAD = SRC[head_start:head_end]
tail_start = SRC.index('<script src="ember_design_system/deck-stage.js"></script>')
tail_end = SRC.rindex("</body>")
TAIL = SRC[tail_start:tail_end]

# ── presenter hooks: time box in the presenter bar, T key forwarded ──
def must_replace(s, old, new):
    assert old in s, old[:80]
    return s.replace(old, new, 1)

TAIL = must_replace(TAIL, "var pd = presenter.document;", "var pd = presenter.document;\n    window.__wsPresenter = presenter;")
TAIL = must_replace(TAIL, "'.pw-bar .tmr{cursor:pointer}.pw-bar .tmr b{color:var(--paper)}' +",
                    "'.pw-bar .tmr{cursor:pointer}.pw-bar .tmr b{color:var(--paper)}' +\n      '.pw-bar .tbx:empty{display:none}.pw-bar .tbx b{color:var(--coral)}' +")
TAIL = must_replace(TAIL, "'<span>clock <b class=\"ck\"></b></span>' +",
                    "'<span>clock <b class=\"ck\"></b></span>' +\n          '<span class=\"tbx\"></span>' +")
TAIL = must_replace(TAIL, "else if (e.key === 'End') { ds.goTo(slides().length - 1); }",
                    "else if (e.key === 'End') { ds.goTo(slides().length - 1); }\n      else if (e.key === 't' || e.key === 'T') { if (window.__wsTimer) window.__wsTimer.toggle(e.shiftKey); }")
TAIL = must_replace(TAIL, "else if (k === 'p') { openPresenter(); }",
                    "else if (k === 'p') { openPresenter(); }\n    else if (k === 't') { if (window.__wsTimer) window.__wsTimer.toggle(e.shiftKey); }")
TAIL = TAIL.replace("/* ─── Presenter aids: notes overlay (N), fullscreen (F), presenter window (P) ─── */",
                    "/* ─── Presenter aids: notes overlay (N), fullscreen (F), presenter window (P), time box (T) ─── */")

WS_CSS = r"""
<style id="ws-css">
/* ── Evals workshop layer ── */
.ws .slide-head{gap:28px}
.ws .crumb{min-width:260px}
.trk{list-style:none;display:flex;align-items:center;gap:10px;margin:0 auto;padding:0}
.trk .tl{font:600 22px var(--font-mono);letter-spacing:.14em;text-transform:uppercase;color:var(--s-faint);margin-right:10px}
.trk li{width:50px;height:50px;border-radius:50%;border:2.5px solid var(--s-line-strong);display:grid;place-items:center;
  font:600 24px/1 var(--font-mono);color:var(--s-faint);background:var(--s-bg)}
.trk li.done{border-color:var(--coral);color:var(--s-accent);background:var(--s-callout-bg)}
.trk li.on{background:var(--coral);border-color:var(--coral);color:var(--ink);box-shadow:0 0 0 7px rgba(255,92,53,.22)}
.title-slide .trk{margin:0}
.title-slide .trk li{width:44px;height:44px;font-size:22px}
.ws code{font-family:var(--font-mono);font-size:.88em;color:var(--s-accent)}
.do-card code,.mtx code,.deb-q code{white-space:nowrap}
.ws .v2-body{gap:32px}

/* lab beat */
.ws-beat::before{content:"";position:absolute;left:0;top:0;bottom:0;width:16px;background:var(--coral);z-index:2}
.ws-beat .slide-content{padding:60px 96px 80px 120px}
.ws-beat .slide-head{margin-bottom:0}
.bt{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1fr) 620px;column-gap:88px;align-items:end;padding-top:24px}
.bt-L{display:flex;flex-direction:column;justify-content:flex-end;min-width:0}
.bt-kick{display:block;font:600 30px var(--font-mono);letter-spacing:.2em;text-transform:uppercase;color:var(--coral);margin-left:8px}
.bt-mega{font:700 380px/.8 var(--font-display);letter-spacing:-.05em;color:var(--coral);margin-top:26px}
.ws-beat h2{font-size:100px;line-height:1;margin-top:40px}
.bt-goal{font-size:40px;line-height:1.32;color:var(--s-text);margin-top:26px;max-width:32ch;text-wrap:pretty}
.bt-R{display:flex;flex-direction:column;justify-content:space-between;align-self:stretch;min-height:0}
.bt-ic{align-self:flex-end;width:230px;height:230px;border-radius:50%;border:4px solid var(--coral);display:grid;place-items:center;background:rgba(255,92,53,.08)}
.bt-ic .ic{width:130px;height:130px;color:var(--coral)}
.bt-facts{display:flex;flex-direction:column;border-top:2px solid var(--line-dark)}
.bt-facts > div{padding:22px 0;border-bottom:2px solid var(--line-dark);display:grid;grid-template-columns:76px 1fr;gap:24px;align-items:center}
.bt-facts .ic{width:66px;height:66px;color:var(--coral)}
.bt-facts .kk{font-size:22px;color:var(--on-dark-faint);margin-bottom:6px}
.bt-facts p{font-size:32px;line-height:1.3;color:var(--on-dark)}
.bt-facts p.tb{font:700 60px/1 var(--font-display);letter-spacing:-.02em;color:var(--coral)}
.bt-facts p.tb small{font:500 26px var(--font-mono);letter-spacing:.04em;color:var(--on-dark-muted);margin-left:14px}

/* do this */
.ws-do h2{font-size:72px}
.ws-do .v2-body{padding-top:28px;justify-content:flex-start}
.do-grid{display:grid;grid-template-columns:minmax(0,1fr) 500px;gap:44px;align-items:stretch;flex:1;min-height:0}
.do-grid .v-win{display:flex;flex-direction:column;min-height:0}
.do-grid .v-win .wbody{font:500 27px/1.46 var(--font-mono);padding:24px 34px 28px;flex:1;min-height:0;white-space:pre-wrap}
.do-grid .v-win .wbody.sm{font-size:25px}
.do-side{display:flex;flex-direction:column;gap:22px;min-width:0}
.tbox{all:unset;box-sizing:border-box;display:block;cursor:pointer;background:var(--ink);color:var(--on-dark);border-radius:6px 6px 22px 22px;
  border-top:10px solid var(--coral);padding:24px 32px 26px;text-align:left}
.slide.dark .tbox{background:var(--ink-2);border-left:2px solid var(--line-dark);border-right:2px solid var(--line-dark);border-bottom:2px solid var(--line-dark)}
.tbox:focus-visible{outline:3px solid var(--coral);outline-offset:6px}
.tbox .kk{display:flex;justify-content:space-between;color:var(--on-dark-faint);font-size:22px}
.tbox .kk b{color:var(--coral);font-weight:600}
.tbox .tb-time{display:block;font:700 116px/1 var(--font-display);letter-spacing:-.03em;color:var(--coral);font-variant-numeric:tabular-nums;margin-top:10px}
.tbox .tb-bar{display:block;height:10px;background:var(--line-dark);border-radius:6px;overflow:hidden;margin:16px 0 12px}
.tbox .tb-bar i{display:block;height:100%;width:100%;background:var(--coral);border-radius:6px}
.tbox .tb-state{display:block;font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--on-dark-muted)}
.tbox.run .tb-state{color:var(--positive-on-dark)}
.tbox.over .tb-time{color:var(--v-fail)}
@media (prefers-reduced-motion:no-preference){
  [data-deck-active] .tbox.over .tb-time{animation:m7-pulse 1.4s ease-in-out infinite}
  .tbox .tb-bar i{transition:width .25s linear}
}
.do-card{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-left:10px solid var(--coral);border-radius:6px 22px 22px 6px;padding:22px 28px 24px}
.do-card .kk{margin-bottom:10px;font-size:22px}
.do-card p{font-size:28px;line-height:1.36;color:var(--s-text)}
.do-card p + p{margin-top:8px}
.do-card.quiet{border-left-color:var(--s-line-strong)}
.do-card.quiet .kk{color:var(--s-muted)}

/* debrief */
.deb-grid{display:grid;grid-template-columns:minmax(0,1fr) 640px;gap:64px;align-items:center;flex:1;min-height:0}
.deb-q{list-style:none;counter-reset:q;display:flex;flex-direction:column;gap:28px;padding:0}
.deb-q li{counter-increment:q;display:grid;grid-template-columns:72px 1fr;font-size:38px;line-height:1.3;color:var(--s-text)}
.deb-q li::before{content:counter(q,decimal-leading-zero);font:600 28px var(--font-mono);color:var(--s-accent);padding-top:8px}
.deb-q li b{color:var(--s-accent);font-weight:600}
.board-card{background:var(--ink);color:var(--on-dark);border-left:10px solid var(--coral);border-radius:6px 26px 26px 6px;padding:40px 46px 44px}
.slide.dark .board-card{background:var(--ink-2);border:2px solid var(--line-dark);border-left:10px solid var(--coral)}
.board-card .kk{color:var(--on-dark-faint)}
.board-card h3{font:700 52px/1.05 var(--font-display);letter-spacing:-.025em;color:var(--on-dark);margin-top:14px}
.board-card p{font-size:31px;line-height:1.36;color:var(--on-dark-muted);margin-top:16px}
.board-card p b{color:var(--on-dark);font-weight:600}
.v2 a.board-link{display:inline-flex;align-items:center;gap:14px;margin-top:28px;font:700 24px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;
  color:var(--ink);background:var(--coral);border-radius:40px;padding:14px 30px;text-decoration:none}
.board-link .ic{width:30px;height:30px;color:var(--ink);stroke-width:12}
.board-card .big{font:700 150px/.9 var(--font-display);letter-spacing:-.04em;color:var(--coral);margin-top:14px;white-space:nowrap}
.board-card .big small{font-size:52px;color:var(--on-dark);margin-left:12px;letter-spacing:-.02em}

/* break */
.ws-break .slide-content{padding:60px 96px 80px}
.brk{flex:1;min-height:0;display:grid;grid-template-columns:minmax(0,1fr) 560px;gap:96px;align-items:center}
.brk .ic.cup{width:200px;height:200px;color:var(--coral)}
.brk h2{font-size:220px;line-height:.9;letter-spacing:-.04em;margin-top:30px}
.brk .lead{font-size:44px;color:var(--on-dark-muted);margin-top:30px;max-width:30ch}
.brk .lead b{color:var(--on-dark)}
.brk .note{font-size:26px;margin-top:26px;max-width:52ch}
.ws .v-acc .m .lab small{font-size:22px}
.v-refs .la .ic{width:46px;height:46px;color:var(--s-accent);stroke-width:10}
.brk .tbox .tb-time{font-size:150px}

/* welcome */
.ws-agenda{display:grid;grid-template-columns:1fr 1fr;gap:0 64px}
.ws-agenda .col{display:flex;flex-direction:column}
.ag{display:grid;grid-template-columns:140px 64px 1fr auto;align-items:center;gap:20px;padding:17px 0;border-top:2px solid var(--s-line)}
.ag:last-child{border-bottom:2px solid var(--s-line)}
.ag time{font:600 30px var(--font-mono);color:var(--s-accent)}
.ag .dot{width:54px;height:54px;border-radius:50%;border:3px solid var(--coral);display:grid;place-items:center;font:700 26px var(--font-mono);color:var(--s-accent)}
.ag .dot.brk{border-style:dashed;border-color:var(--s-line-strong);color:var(--s-faint)}
.ag span.t{font:700 38px/1.1 var(--font-display);letter-spacing:-.02em;color:var(--s-text)}
.ag .tag{font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;border-radius:20px;padding:6px 14px;border:2px solid var(--s-line-strong);color:var(--s-muted)}
.ag .tag.m{border-color:var(--coral);color:var(--s-accent)}
.ag.b span.t{color:var(--s-muted);font-weight:500}
.duo{display:grid;grid-template-columns:1fr 1fr;gap:40px}
.lap{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:24px;padding:34px 42px 38px;display:flex;flex-direction:column;gap:6px}
.lap.hot{border:3px solid var(--coral);background:var(--s-callout-bg)}
.lap .lh{display:flex;align-items:center;gap:24px;margin-bottom:10px}
.lap .lh .ic{width:84px;height:84px;flex:none}
.lap h3{font:700 60px/1 var(--font-display);letter-spacing:-.03em}
.lap h3 code{font-size:.62em;color:var(--s-accent);display:block;margin-top:8px}
.lap .it{display:grid;grid-template-columns:150px 1fr;gap:18px;padding:12px 0;border-top:1.5px solid var(--s-line);font-size:31px;line-height:1.3}
.lap .it b{white-space:nowrap;font:600 22px var(--font-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--s-accent);padding-top:6px}
.steps3{list-style:none;display:flex;flex-direction:column;gap:22px;counter-reset:s;padding:0}
.steps3 li{counter-increment:s;display:grid;grid-template-columns:84px 1fr;align-items:baseline;font-size:36px;line-height:1.3;border-top:2px solid var(--s-line);padding-top:20px}
.steps3 li::before{content:counter(s,decimal-leading-zero);font:600 30px var(--font-mono);color:var(--s-accent)}
.two-col{display:grid;grid-template-columns:minmax(0,1fr) 640px;gap:64px;align-items:center}
.tasks{display:flex;flex-direction:column}
.tasks div{display:grid;grid-template-columns:420px 1fr;gap:28px;padding:15px 0;border-top:2px solid var(--s-line);align-items:baseline}
.tasks div:last-child{border-bottom:2px solid var(--s-line)}
.tasks code{font-size:28px;font-weight:600}
.tasks span{font-size:30px;line-height:1.3;color:var(--s-text)}
.tasks div.dim code{color:var(--s-muted)} .tasks div.dim span{color:var(--s-muted)}

/* concept pieces */
.cmp{display:flex;flex-direction:column;gap:34px}
.cmp .row{display:grid;grid-template-columns:260px 1fr;gap:30px;align-items:center}
.cmp .row b{font:700 44px var(--font-display);letter-spacing:-.02em;color:var(--s-text)}
.cmp .row b small{display:block;font:500 22px var(--font-mono);letter-spacing:.08em;text-transform:uppercase;color:var(--s-faint);margin-top:6px}
.cmp .bar{height:74px;border-radius:0 10px 10px 0;display:flex;align-items:center;padding:0 24px;font:700 34px var(--font-display);color:var(--ink);white-space:nowrap}
.cmp .bar.a{background:#8d8271}
.cmp .bar.b{background:var(--coral)}
.cmp p{grid-column:2;font-size:30px;line-height:1.32;color:var(--s-muted);margin-top:-14px}
.formula{background:var(--ink);color:var(--on-dark);border-radius:6px 26px 26px 6px;border-left:10px solid var(--coral);padding:40px 50px}
.formula .kk{color:var(--on-dark-faint)}
.formula .eq{display:grid;grid-template-columns:auto 1fr;gap:30px;align-items:center;margin-top:18px}
.formula .eq b{font:700 64px/1 var(--font-display);letter-spacing:-.03em;color:var(--coral)}
.formula .frac{display:flex;flex-direction:column;font:600 40px/1.3 var(--font-mono);white-space:nowrap}
.formula .frac span:first-child{border-bottom:3px solid var(--on-dark-muted);padding-bottom:8px}
.formula .frac span:last-child{padding-top:8px}
.ivl{display:flex;flex-direction:column;gap:30px}
.ivl .r{display:grid;grid-template-columns:360px 1fr;gap:30px;align-items:center}
.ivl .r > div:first-child b{display:block;font:700 44px/1.05 var(--font-display);letter-spacing:-.02em}
.ivl .r > div:first-child span{font:500 24px var(--font-mono);color:var(--s-muted)}
.ivl svg{width:100%;height:auto}
.mtx{width:100%;border-collapse:collapse;font:500 32px var(--font-mono)}
.mtx th{text-align:left;font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);padding:14px 20px;border-bottom:3px solid var(--coral)}
.mtx td{padding:20px;border-bottom:1.5px solid var(--s-line);color:var(--s-text)}
.mtx td.ok{color:var(--positive);font-weight:700}
.slide.dark .mtx td.ok{color:var(--positive-on-dark)}
.mtx td.bad{color:var(--v-fail);font-weight:700}
.mtx td small{display:block;font:400 24px var(--font-body);color:var(--s-muted);margin-top:4px}
.hard{display:flex;flex-direction:column;gap:20px}
.hard .h{display:grid;grid-template-columns:100px 1fr auto;gap:28px;align-items:center;background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-radius:22px;padding:24px 34px}
.hard .h .ic{width:84px;height:84px}
.hard .h h3{font:700 44px/1.05 var(--font-display);letter-spacing:-.02em}
.hard .h p{font-size:30px;line-height:1.3;color:var(--s-muted);margin-top:6px}
.hard .h .lvl{font:600 22px var(--font-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--s-accent);border:2px solid var(--coral);border-radius:20px;padding:6px 16px;white-space:nowrap}
.hard .h.weak .lvl{color:var(--s-muted);border-color:var(--s-line-strong)}
.v-stn.n5 .stops{grid-template-columns:repeat(5,1fr);gap:22px}
.v-stn.n5 .stops h3{font-size:46px}
.v-stn.n5 .stops p{font-size:29px;margin-top:10px}
.v-stn.n4 .stops p code{font-size:.85em}
.jd{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:stretch}
.jd .v-panel h3{font-size:54px}
.jd .v-panel p{font-size:32px}
.jd ul{list-style:none;display:flex;flex-direction:column;gap:18px;margin-top:10px;padding:0}
.jd li{font-size:31px;line-height:1.32;padding-left:40px;position:relative;color:var(--s-text)}
.jd li::before{content:"";position:absolute;left:0;top:.42em;width:18px;height:18px;background:var(--coral);clip-path:polygon(0 0,100% 50%,0 100%)}
.hn{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:32px}
.hn .v-panel{padding:34px 40px 40px}
.hn .big{font:700 72px/1 var(--font-display);letter-spacing:-.03em;color:var(--s-accent);margin:14px 0 6px;white-space:nowrap}
.hn h3{font-size:50px}
.hn .v-panel p{font-size:30px}
.ow{display:grid;grid-template-columns:minmax(0,1fr) 760px;gap:56px;align-items:stretch}
.ow .m7-facts p{font-size:32px}
.ow .m7-when{grid-template-columns:1fr;gap:22px}
.ow .m7-when .col{padding:28px 36px 30px}
.ow .m7-when h3{font-size:46px;margin:4px 0 8px}
.ow .m7-when p{font-size:30px;line-height:1.32;color:var(--s-text)}
.rc{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}
.rc > div{background:var(--s-card-bg);border:1.5px solid var(--s-card-border);border-top:8px solid var(--coral);border-radius:6px 6px 20px 20px;padding:24px 28px 28px;min-width:0}
.rc .kk{font-size:22px}
.rc p{font-size:28px;line-height:1.3;color:var(--s-text);margin-top:10px}
.rc > div.defs{background:var(--ink);border-top-color:var(--coral);color:var(--on-dark)}
.slide.dark .rc > div.defs{background:var(--ink-3)}
.rc .defs p{color:var(--on-dark);font-size:24px;margin-top:8px}
.rc .defs p b{color:var(--coral);font-family:var(--font-mono);font-weight:600}
.ws .v-refs .lt{font-size:46px}
.ws .v-refs a{padding:26px 8px}
.axis{width:100%;height:auto}
.rt{display:grid;grid-template-columns:1080px 1fr;gap:56px;align-items:center}
.rt .lead{font-size:36px}
</style>
"""

TIMER_JS = r"""
<script>
/* ─── Time box on "Do this" and break slides: T starts or pauses, Shift+T resets, click toggles.
   State lives per box, so a running box keeps counting while you show another slide. ─── */
(function(){
  var ds = document.querySelector('deck-stage');
  if (!ds) return;
  var state = {};
  function pad(n){ return (n < 10 ? '0' : '') + n; }
  function fmt(sec){ sec = Math.max(0, Math.ceil(sec)); return pad(Math.floor(sec / 60)) + ':' + pad(sec % 60); }
  function get(el){
    var id = el.getAttribute('data-tbox');
    if (!state[id]) { var t = (+el.getAttribute('data-min') || 10) * 60; state[id] = { total: t, left: t, running: false, last: 0 }; }
    return state[id];
  }
  function docs(){
    var d = [document], pw = window.__wsPresenter;
    try { if (pw && !pw.closed) d.push(pw.document); } catch (e) {}
    return d;
  }
  function label(st){
    if (st.left <= 0) return 'Time is up';
    if (st.running) return 'Running';
    return st.left < st.total ? 'Paused' : 'Ready';
  }
  function render(id){
    var st = state[id];
    docs().forEach(function(d){
      d.querySelectorAll('[data-tbox="' + id + '"]').forEach(function(b){
        b.querySelector('.tb-time').textContent = fmt(st.left);
        b.querySelector('.tb-state').textContent = label(st);
        b.querySelector('.tb-bar i').style.width = (100 * st.left / st.total).toFixed(2) + '%';
        b.classList.toggle('run', st.running);
        b.classList.toggle('over', st.left <= 0);
        b.setAttribute('aria-pressed', st.running ? 'true' : 'false');
      });
      var bar = d.querySelector('.pw-bar .tbx');
      if (bar) {
        var runs = Object.keys(state).filter(function(k){ return state[k].running; });
        bar.innerHTML = runs.length ? 'time box <b>' + fmt(state[runs[0]].left) + '</b>' : '';
      }
    });
  }
  setInterval(function(){
    var now = performance.now();
    Object.keys(state).forEach(function(id){
      var st = state[id];
      if (!st.running) return;
      st.left -= (now - st.last) / 1000; st.last = now;
      if (st.left <= 0) { st.left = 0; st.running = false; }
      render(id);
    });
  }, 250);
  function toggleBox(el, reset){
    var st = get(el), id = el.getAttribute('data-tbox');
    if (reset) { st.left = st.total; st.running = false; }
    else if (st.left <= 0) { st.left = st.total; st.running = true; }
    else { st.running = !st.running; }
    st.last = performance.now();
    render(id);
  }
  function activeBox(){
    var s = ds.querySelector(':scope > section[data-deck-active]');
    return s ? s.querySelector('[data-tbox]') : null;
  }
  window.__wsTimer = { toggle: function(reset){ var el = activeBox(); if (el) toggleBox(el, reset); } };
  document.addEventListener('click', function(e){
    var b = e.target && e.target.closest ? e.target.closest('[data-tbox]') : null;
    if (!b) return;
    e.preventDefault();
    toggleBox(b, e.shiftKey);
    b.blur(); /* keep Space for slide navigation */
  });
})();
</script>
"""

# ── icons (120 × 120, stroke) ──
IC = {
 "term": '<rect x="8" y="16" width="104" height="88" rx="8"/><path d="M26 46 L44 60 L26 74"/><path d="M54 76 H86"/>',
 "flask": '<path d="M44 12 H76"/><path d="M52 12 V46 L22 100 C19 106 22 110 29 110 H91 C98 110 101 106 98 100 L68 46 V12"/><path d="M34 82 H86"/>',
 "loop": '<path d="M100 60 A40 40 0 1 1 88 31"/><path d="M92 8 L90 32 L66 30"/>',
 "warn": '<path d="M60 12 L112 104 H8 Z"/><path d="M60 46 V72"/><path d="M60 88 V90" stroke-width="9"/>',
 "trace": '<circle cx="30" cy="32" r="16"/><rect x="72" y="72" width="34" height="34" rx="6"/><path d="M46 38 C70 44 62 76 70 84" stroke-dasharray="3 10"/><path d="M58 76 L70 86 L76 72"/>',
 "judge": '<path d="M60 14 V104 M36 108 H84 M20 30 H100"/><path d="M20 30 L6 68 H34 Z M100 30 L86 68 H114 Z"/>',
 "route": '<path d="M60 112 V66 L28 28 M60 66 L92 28"/><path d="M22 46 L26 24 L46 26"/><path d="M74 26 L94 24 L98 46"/>',
 "home": '<path d="M12 58 L60 16 L108 58"/><path d="M26 46 V106 H94 V46"/><path d="M50 106 V76 H70 V106"/>',
 "check": '<rect x="10" y="14" width="24" height="24" rx="5"/><path d="M46 26 H110"/><rect x="10" y="48" width="24" height="24" rx="5"/><path d="M46 60 H110"/><rect x="10" y="82" width="24" height="24" rx="5"/><path d="M46 94 H96"/><path d="M15 26 L21 32 L31 19"/><path d="M15 60 L21 66 L31 53"/>',
 "sheet": '<rect x="14" y="18" width="92" height="84" rx="8"/><path d="M14 42 H106 M14 66 H106 M44 18 V102"/>',
 "people": '<circle cx="44" cy="40" r="16"/><path d="M12 104 C12 80 26 68 44 68 C62 68 76 80 76 104"/><circle cx="82" cy="34" r="13" opacity=".6"/><path d="M84 60 C100 60 110 72 110 94" opacity=".6"/>',
 "gauge": '<circle cx="60" cy="66" r="42"/><path d="M60 66 L86 40" stroke-width="8"/><path d="M60 12 V20 M12 66 H20 M100 66 H108 M26 32 L32 38 M94 32 L88 38"/>',
 "doc": '<path d="M20 26 V108 H70" opacity=".45"/><path d="M32 12 H78 L100 34 V100 H32 Z"/><path d="M78 12 V34 H100"/><path d="M46 52 H86 M46 66 H86 M46 80 H72"/>',
 "cup": '<path d="M18 46 H90 V76 C90 94 76 106 58 106 H50 C32 106 18 94 18 76 Z"/><path d="M90 56 H98 C107 56 112 63 112 71 C112 80 105 86 96 86 H88"/><path d="M40 12 C34 20 46 26 40 34 M62 12 C56 20 68 26 62 34"/>',
 "board": '<rect x="10" y="14" width="44" height="40" rx="6"/><rect x="66" y="14" width="44" height="40" rx="6"/><rect x="10" y="66" width="100" height="40" rx="6"/>',
 "clock": '<circle cx="60" cy="60" r="46"/><path d="M60 32 V60 L80 72"/>',
 "lock": '<rect x="24" y="52" width="72" height="56" rx="8"/><path d="M38 52 V36 C38 22 48 14 60 14 C72 14 82 22 82 36 V52"/>',
 "cloud": '<path d="M34 92 H90 C104 92 112 82 112 70 C112 58 102 48 90 48 C88 32 76 22 60 22 C44 22 32 34 30 50 C18 52 8 60 8 72 C8 84 18 92 34 92 Z"/>',
 "laptop": '<rect x="22" y="22" width="76" height="52" rx="6"/><path d="M8 96 H112 L102 80 H18 Z"/>',
 "coins": '<ellipse cx="60" cy="30" rx="40" ry="14"/><path d="M20 30 V54 C20 62 38 68 60 68 C82 68 100 62 100 54 V30"/><path d="M20 54 V80 C20 88 38 94 60 94 C82 94 100 88 100 80 V54"/>',
 "eye": '<path d="M6 60 C26 28 94 28 114 60 C94 92 26 92 6 60 Z"/><circle cx="60" cy="60" r="16"/>',
 "shield": '<path d="M60 10 L104 26 V58 C104 84 86 102 60 112 C34 102 16 84 16 58 V26 Z"/><path d="M40 60 L54 74 L82 44"/>',
 "dice": '<rect x="16" y="16" width="88" height="88" rx="14"/><circle cx="40" cy="40" r="5"/><circle cx="80" cy="40" r="5"/><circle cx="60" cy="60" r="5"/><circle cx="40" cy="80" r="5"/><circle cx="80" cy="80" r="5"/>',
 "key": '<circle cx="36" cy="60" r="22"/><path d="M58 60 H112 M92 60 V80 M106 60 V74"/>',
 "arrow": '<path d="M24 96 L96 24 M44 24 H96 V76"/>',
 "git": '<circle cx="30" cy="24" r="12"/><circle cx="30" cy="96" r="12"/><circle cx="90" cy="46" r="12"/><path d="M30 36 V84 M90 58 C90 78 60 74 36 88"/>',
}

def icon(name, cls="", extra=""):
    return f'<svg viewBox="0 0 120 120" class="ic {cls}" aria-hidden="true"{extra}>{IC[name]}</svg>'

# ── header pieces ──
def tracker(on=None, done_upto=-1, small=False):
    lis = []
    for i in range(8):
        c = "on" if i == on else ("done" if i <= done_upto else "")
        lis.append(f'<li class="{c}">{i}</li>')
    return f'<ol class="trk" aria-label="Labs 0 to 7"><li class="tl" aria-hidden="true" style="width:auto;height:auto;border:0;background:none">Labs</li>{"".join(lis)}</ol>'

SLIDES = []

def esc(s):
    return html.escape(s, quote=True)

def add(label, notes, body, cls="light", extra_cls="", raw=False):
    SLIDES.append(dict(label=label, notes=notes, body=body, cls=cls, extra=extra_cls, raw=raw))

def head(crumb, on=None, done=-1):
    n = len(SLIDES) + 1
    return (f'<div class="slide-head"><span class="snum">{n:02d}</span>{tracker(on, done)}'
            f'<div class="crumb">{crumb}</div></div>')

def slide(crumb, title, inner, on=None, done=-1, note=None):
    nt = f'<p class="note">{note}</p>' if note else ""
    return (f'<div class="slide-content">{head(crumb, on, done)}<h2>{title}</h2>'
            f'<div class="v2-body">{inner}</div>{nt}</div>')

def term(title, body, cls=""):
    return (f'<div class="v-win term"><div class="tbar"><i class="r"></i><i class="y"></i><i class="g"></i><span>{title}</span></div>'
            f'<div class="wbody {cls}">{body}</div></div>')

def P(cmd, comment=""):
    c = f'  <span class="c"># {comment}</span>' if comment else ""
    return f'<span class="p">$</span> {cmd}{c}'

def C(text):
    return f'<span class="c"># {text}</span>'

def O(text):
    return f'<span class="dim">{text}</span>'

def tbox(tid, minutes, heading="Time box"):
    return (f'<button type="button" class="tbox" data-tbox="{tid}" data-min="{minutes}" aria-pressed="false" '
            f'aria-label="{heading}, {minutes} minutes. Press T to start or pause.">'
            f'<span class="kk"><span>{heading}</span><b>{minutes} min</b></span>'
            f'<span class="tb-time">{minutes:02d}:00</span><span class="tb-bar"><i></i></span>'
            f'<span class="tb-state">Ready</span></button>')

def card(kk, text, quiet=False):
    ps = "".join(f"<p>{t}</p>" for t in (text if isinstance(text, list) else [text]))
    return f'<div class="do-card{" quiet" if quiet else ""}"><span class="kk">{kk}</span>{ps}</div>'

def board_card(kk, h3, text, link=True):
    ps = "".join(f"<p>{t}</p>" for t in (text if isinstance(text, list) else [text]))
    ln = (f'<a class="board-link" href="{BOARD}" target="_blank" rel="noopener">Open the board '
          f'{icon("arrow")}</a>') if link else ""
    return f'<div class="board-card"><span class="kk">{kk}</span><h3>{h3}</h3>{ps}{ln}</div>'

BEAT_IC = {0: 'term', 1: 'flask', 2: 'loop', 3: 'warn', 4: 'trace', 5: 'judge', 6: 'route', 7: 'home'}

def beat(lab, kick, title, goal, facts, notes, label):
    fx = "".join(
        f'<div>{icon(ic)}<div><span class="kk">{k}</span><p class="{c}">{v}</p></div></div>'
        for ic, k, v, c in facts)
    body = (f'<div class="slide-content">{head(f"Lab {lab} · intro", lab, lab - 1)}'
            f'<div class="bt"><div class="bt-L"><span class="bt-kick">{kick}</span>'
            f'<div class="bt-mega" aria-hidden="true">{lab}</div><h2>{title}</h2>'
            f'<p class="bt-goal">{goal}</p></div><div class="bt-R"><div class="bt-ic">{icon(BEAT_IC[lab])}</div>'
            f'<div class="bt-facts">{fx}</div></div></div></div>')
    add(label, notes, body, cls="dark", extra_cls="ws-beat")

def do_slide(lab, title, termtitle, termbody, tid, minutes, cards, notes, label, termcls="", note=None, dark=False):
    inner = (f'<div class="do-grid">{term(termtitle, termbody, termcls)}'
             f'<div class="do-side">{tbox(tid, minutes)}{"".join(cards)}</div></div>')
    add(label, notes, slide(f"Lab {lab} · do this", title, inner, lab, lab - 1, note),
        cls="dark" if dark else "light", extra_cls="ws-do")

def debrief(lab, title, questions, bcard, notes, label, dark=False, crumb=None):
    qs = "".join(f"<li><span>{q}</span></li>" for q in questions)
    inner = f'<div class="deb-grid"><ol class="deb-q">{qs}</ol>{bcard}</div>'
    add(label, notes, slide(crumb or f"Lab {lab} · debrief", title, inner, lab, lab - 1),
        cls="dark" if dark else "light")

def brk(minutes, back, text, tid, done, notes, label, sub=''):
    body = (f'<div class="slide-content">{head("Break", None, done)}'
            f'<div class="brk"><div>{icon("cup", "cup")}<h2>Break</h2>'
            f'<p class="lead">{text}</p><p class="note">{sub}</p></div>'
            f'<div>{tbox(tid, minutes, "Back at " + back)}</div></div></div>')
    add(label, notes, body, cls="dark", extra_cls="ws-break")

def rail(stops, icons, hot_last=True, h=300):
    n = len(stops)
    W = 1728
    r = 116 if n <= 3 else (110 if n == 4 else 96)
    cy = 180 if n <= 3 else 170
    xs = [W * (2 * i + 1) / (2 * n) for i in range(n)]
    parts = [f'<line class="rl-base" x1="4" y1="{cy}" x2="1724" y2="{cy}"/>',
             f'<line class="rl-on" x1="{xs[0]:.0f}" y1="{cy}" x2="{xs[-1]:.0f}" y2="{cy}"/>']
    for i, x in enumerate(xs):
        parts.append(f'<text class="rl-n" x="{x:.0f}" y="40" text-anchor="middle">{i + 1:02d}</text>')
    for i, x in enumerate(xs):
        hot = hot_last and i == n - 1
        s = r * 0.98
        parts.append(f'<circle class="rl-c{" hot" if hot else ""}" cx="{x:.1f}" cy="{cy}" r="{r}"/>'
                     f'<svg x="{x - s / 2:.1f}" y="{cy - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" viewBox="0 0 120 120" '
                     f'class="ic{" hot" if hot else ""}">{IC[icons[i]]}</svg>')
    aria = "Sequence: " + ", then ".join(re.sub("<[^>]+>", "", t) for t, _ in stops)
    st = "".join(f"<div><h3>{t}</h3><p>{p}</p></div>" for t, p in stops)
    return (f'<div class="v-stn n{n}"><svg class="rail" viewBox="0 0 1728 {h}" role="img" aria-label="{esc(aria)}">'
            f'{"".join(parts)}</svg><div class="stops">{st}</div></div>')

# ════════════════════════════ SLIDES ════════════════════════════

# 1 · title
add("Evals, hands on",
    "Welcome people while they sit down and open a terminal in workshops/evals/lab. Say the promise in one sentence: by one o'clock every pair has measured a coding agent on real Java tasks, pooled the numbers with the room, and knows how to run the same eval on their own repository. Check that everyone has a partner and that both partners have a laptop open. If someone skipped the prework, pair them with a partner who did it; they can install things during lab 3, which calls no model. The badge says work in progress until the dry run on a Pro account has happened.",
    f'<div class="ts-top"><span class="k">Workshop · hands-on · half day</span>{tracker()}<span class="meta">September 2026</span></div>'
    '<div class="ts-hero"><div class="wip-badge">Work in progress · dry run pending</div><h1>Evals,<br>hands on<span class="dot">.</span></h1>'
    '<p class="ts-sub">Ten pairs, one Java repo and your own Claude Code plans. <b>Measure a coding agent</b>, pool the numbers on one board, and take a working eval home.</p></div>'
    '<div class="ts-foot"><div class="ts-author"><a href="https://davidbudac.cz" target="_blank" rel="noopener">David Budáč</a> · companion to talk 07, <b>Measuring What Works</b></div>'
    '<div class="ts-loopline"><span class="w">guess</span> <span class="a">·</span> <span class="w">measure</span> <span class="a">·</span> <span class="w">read</span> <span class="a">·</span> <span class="w">route</span></div></div>',
    cls="dark", extra_cls="title-slide", raw=True)

# 2 · outcomes
rows = [("sheet", "A measured answer", "Lean or bloated CLAUDE.md, decided by pass rate and cost per pass, pooled across ten pairs."),
        ("shield", "A checker you trust", "You break a weak grader on purpose, then harden it with hidden tests and a property check."),
        ("judge", "A judge you have tested", "Agreement with your own scores on eight commit messages, and the self-preference gap."),
        ("home", "An eval for your repo", "Three solved tasks from your git history, hidden tests and a CI job to run them.")]
inner = '<div class="v-rows grid2">' + "".join(
    f'<div class="v-row">{icon(i)}<h3>{h}</h3><p>{p}</p></div>' for i, h, p in rows) + "</div>"
add("What you take home",
    "Read the four outcomes and point at the board on the second screen: every number in the first three comes from this room, not from a vendor chart. Stress the fourth. The invoice app is a practice target; the value is running the same loop on your own code next week. Keep this under two minutes.",
    slide("Welcome · outcomes", "What you take home at 13:00", inner))

# 3 · the day
ag = [("09:10", "0", "Setup check", "offline"), ("09:20", "1", "Guess, then measure", "model"),
      ("09:55", "2", "Variance", "model"), ("10:25", "", "Break", ""), ("10:40", "3", "Break the grader", "offline"),
      ("11:15", "4", "Read the traces", "offline"), ("11:40", "", "Break", ""), ("11:50", "5", "Judge model", "model"),
      ("12:20", "6", "Route by the numbers", "model"), ("12:45", "7", "Take it home", "offline")]
def agrow(t, n, name, tag):
    b = not n
    dot = f'<span class="dot{" brk" if b else ""}">{n or "·"}</span>'
    tg = f'<span class="tag{" m" if tag == "model" else ""}">{tag}</span>' if tag else "<span></span>"
    return f'<div class="ag{" b" if b else ""}"><time>{t}</time>{dot}<span class="t">{name}</span>{tg}</div>'
inner = ('<div class="ws-agenda"><div class="col">' + "".join(agrow(*a) for a in ag[:5]) +
         '</div><div class="col">' + "".join(agrow(*a) for a in ag[5:]) + "</div></div>")
add("The day",
    "Walk the rhythm. Model runs come early, the offline labs sit in the middle so slow runs can finish, then the judge and the routing lab. Point out the two breaks. The times for labs that call a model are firm, because runs need wall-clock time; the discussion time is where you flex. If you start late, cut lab 7's in-room part to five minutes: the take-home guide covers it. The tracker in every slide header shows where we are.",
    slide("Welcome · the day", "Four hours in eight labs", inner, note="09:00 welcome · 13:00 close · model labs use your plan, offline labs use none, so slow runs can finish during labs 3 and 4"))

# 4 · pairs and ROLE
lap = lambda hot, h, role, items: (
    f'<div class="lap{" hot" if hot else ""}"><div class="lh">{icon("laptop")}<h3>{h}<code>{role}</code></h3></div>' +
    "".join(f'<div class="it"><b>{k}</b><span>{v}</span></div>' for k, v in items) + "</div>")
inner = ('<div class="duo">' +
         lap(False, "Laptop a", "ROLE=a", [("Labs 1-2", "the lean CLAUDE.md"), ("Lab 5", "the judge, with your hand scores"), ("Lab 6", "Sonnet, reusing your lean runs")]) +
         lap(True, "Laptop b", "ROLE=b", [("Labs 1-2", "the bloated CLAUDE.md"), ("Lab 5", "starts lab 6 in the background"), ("Lab 6", "Haiku, six short sessions")]) +
         '</div>')
add("Two laptops, one pair name",
    "This is the one piece of set-up that matters all day. Both partners run the setup check with the same PAIR name, so the board sees one pair. Every model lab then runs with ROLE=a on one laptop and ROLE=b on the other. That halves the wall-clock time and spreads the usage across two subscriptions: about 7 sessions on laptop a and 11 on laptop b. If one partner has a Max plan, give them laptop b. Watch for pairs that run without ROLE on both laptops: they spend double and get duplicate rows.",
    slide("Welcome · pairs", "Two laptops, one pair name", inner, note="Same name on both: PAIR=your-team ./check-setup.sh · then ROLE=a or ROLE=b in front of every lab"))

# 5 · budget
inner = ('<div class="m7-kpis"><div><b>~18</b><span>agent sessions per pair, all day</span></div>'
         '<div><b>≤ 11</b><span>on any one laptop, split with ROLE</span></div>'
         '<div><b>8</b><span>judge calls, about 1% of a session each</span></div></div>'
         '<div class="chips lg"><span><code>--dry-run</code> prints the plan, spends nothing</span>'
         '<span><code>LITE=1</code> roughly halves the runs</span><span><code>--sample</code> works offline</span>'
         '<span><code>--yes</code> skips the question</span></div>')
add("Your plan pays for the runs",
    "Be straight about usage: participants spend their own plan. Anthropic publishes no number for Pro, only a session limit that resets every five hours, a weekly limit, and that claude.ai and Claude Code share it. Say what your dry run showed: read /usage before and after record-facilitator-run.sh on a Pro account and quote the difference here. If it used more than about half a five-hour window, announce LITE=1 for the whole day now. Anyone who used Claude heavily this morning should take laptop a, which runs fewer sessions. Every runner prints its plan and asks before it spends.",
    slide("Welcome · usage", "Your plan pays for the runs", inner,
          note="Anthropic publishes no Pro limit · the facilitator's dry run on a Pro plan set today's defaults"))

# 6 · board
inner = ('<div class="two-col"><ol class="steps3">'
         '<li><span>Run <code>./export-results.sh --lab labN --latest</code> at the end of each model lab.</span></li>'
         '<li><span>Copy the lines it prints, one JSON object per run.</span></li>'
         '<li><span>Paste them into the board and press <b>Add to the board</b>.</span></li></ol>' +
         board_card("Live room board", "Labs 1, 2, 5 and 6",
                    ["Pasting the same lines twice is safe: the board keeps <b>one row per run</b>.",
                     "Labs 3, 4 and 7 stay on your laptop."]) + "</div>")
add("Every lab ends on one board",
    "Open the board on the second screen now and leave it open all day. Show the paste box and the pair-name field. Everyone can paste because the board is shared as Can interact; if someone sees a read-only page, they are signed out of claude.ai or the share setting is wrong, so fix it now instead of in lab 1. Pasting twice is safe because the board keys rows by pair, lab, variant, task and run. If you rehearsed with sample data, clear it or ignore the SYNTH pairs.",
    slide("Welcome · the board", "Every lab ends on one board", inner))

# 7 · the repo
tk = [("fix-date-parser", "05.09.2026 is read as 9 May"), ("jpy-rounding", "JPY missing; two decimals hard-coded"),
      ("report-sort-accents", "sorts by code point, ignores the Collator"), ("export-currency-column", "feature: a sixth CSV column (lab 3)"),
      ("fixtures-bom", "a UTF-8 BOM breaks the header", True), ("rename-customer-field", "refactor across callers", True)]
inner = ('<div class="two-col"><div class="tasks">' + "".join(
    f'<div class="{"dim" if len(t) > 2 else ""}"><code>{t[0]}</code><span>{t[1]}</span></div>' for t in tk) +
    '</div><div class="m7-side"><p class="lead sm"><b>invoice-app</b>: Java 21, JUnit 5, 57 green tests, and bugs the tests miss.</p>'
    '<p class="lead sm">A <b>hidden JUnit test</b> grades every run. The agent never sees it.</p></div></div>')
add("One Java repo",
    "Give them the target in one minute. invoice-app is a small Maven project, Java 21 and JUnit 5 and nothing else, with 57 passing tests and latent bugs the tests do not cover. Each task is an issue text. A hidden JUnit test, copied in only when grading, decides pass or fail, together with the repo's own tests. The agent works in a throwaway copy with a narrow allow-list: it cannot install packages, fetch URLs or push, and it never touches their own code or settings. The two dimmed tasks are in the kit for later practice.",
    slide("Welcome · the repo", "One Java repo with latent bugs", inner))

# ── Lab 0 ──
beat(0, "Lab 0 · setup check", "Prove your laptop is ready",
     "Every line of the setup check says PASS on both laptops, under the same pair name.",
     [("clock", "Time box", '10 min<small>09:10 to 09:20</small>', "tb"),
      ("gauge", "Model sessions", "None. It reads your sign-in and calls no model.", ""),
      ("board", "Board", "Nothing yet. Lab 1 is the first paste.", "")],
     "Most people ran this at home from the prework, so this is a re-run on venue Wi-Fi. It calls no model and costs nothing. Use the ten minutes to find the two or three laptops that are not ready, and fix them while everyone else reads the two CLAUDE.md files in claude-md/. If a pair cannot fix a laptop within ten minutes, they run every lab on the working laptop with no ROLE and LITE=1.",
     "Lab 0 · setup check")

do_slide(0, "Run the setup check on both laptops", "workshops/evals/lab",
         "\n".join([P("cd workshops/evals/lab"),
                    P("PAIR=your-team ./check-setup.sh", "both laptops, same name"),
                    O("Java and Maven"),
                    O("  [PASS] JDK 21 (openjdk version \"21.0.4\")"),
                    O("  [PASS] offline build and tests pass (./mvnw -q -o test)"),
                    O("  ..."),
                    O("  [PASS] signed in (claude.ai, plan: pro)"),
                    O("  [PASS] pair name saved to .pair: your-team"),
                    "",
                    O("Result: 11 passed, 0 failed, 0 warnings"),
                    O("You are ready. Nothing above called a model.")]),
         "l0", 8,
         [card("Paste to the board", "Nothing yet."),
          card("A FAIL line?", "Next slide has the fixes. Call the facilitator if it takes longer than two minutes.", quiet=True)],
         "Press T to start the time box; press it again to pause, Shift+T resets it. Ask both partners to run the same PAIR name, a short one without spaces, for example the pair's surnames. The first run downloads Maven and the dependencies; at the venue it should take under a minute because the prework cached them. Walk the room and look for FAIL lines. A WARN about uv is fine: the labs fall back to ENGINE=direct and produce the same files. A WARN about an API-key sign-in is not fine: that partner would pay per token, so help them sign in with the subscription.",
         "Lab 0 · do this")

fixes = [("JDK 21 missing", "Install Temurin 21 and open a new terminal."),
         ("Dependency prefetch", "Proxy? Fix <code>~/.m2/settings.xml</code>, then run <code>./mvnw dependency:go-offline</code> in <code>invoice-app</code> to see why."),
         ("uv or smevals", "Carry on. The labs fall back to <code>ENGINE=direct</code> with the same files."),
         ("Not signed in", "Run <code>claude</code> once and log in with Pro or Max, or <code>claude auth login</code>."),
         ("API key sign-in", "Runs would bill per token. Log in with the subscription instead.")]
inner = ('<table class="mtx"><thead><tr><th>The line says</th><th>Do this</th></tr></thead><tbody>' +
         "".join(f"<tr><td style=\"white-space:nowrap;font-weight:600\">{a}</td><td style=\"font-family:var(--font-body)\">{b}</td></tr>" for a, b in fixes) +
         "</tbody></table>")
add("Lab 0 · fixes",
    "Leave this slide up while people fix things. The Maven prefetch is the usual failure on corporate laptops: a proxy or a mirror in settings.xml. If it cannot be fixed in a few minutes, the pair runs everything on the partner's laptop without ROLE, and the broken laptop retries the prefetch on a phone hotspot during lab 3. Missing uv costs nothing, since the kit runs the same runner and checker without smevals. If claude auth status fails on a laptop that is signed in, the credentials may belong to another user account; run claude and log in again.",
    slide("Lab 0 · fixes", "Fix a FAIL line in two minutes", inner, 0, -1))

# ── Lab 1 ──
beat(1, "Lab 1 · guess, then measure", "Guess, then measure",
     "Bet on which CLAUDE.md is cheaper per passing run, post the bet, then run both.",
     [("clock", "Time box", '35 min<small>09:20 to 09:55</small>', "tb"),
      ("gauge", "Model sessions", "4 Sonnet per pair: 2 on each laptop", ""),
      ("board", "Board", "Your prediction first, then 4 runs", "")],
     "This is talk 07's opening argument turned into a bet. The point is to commit before seeing data, because afterwards everyone remembers having guessed right. Keep the intro to five minutes: the runs need wall-clock time. Mention that the prediction goes on the board before any run starts.",
     "Lab 1 · guess, then measure")

inner = ('<div class="cmp">'
         '<div class="row"><b>lean.md<small>~270 tokens</small></b><div class="bar a" style="width:8%"></div></div>'
         '<p>Rules, commands, conventions. Nothing else.</p>'
         '<div class="row"><b>bloated.md<small>~3,800 tokens</small></b><div class="bar b" style="width:100%">14× the tokens, same rules</div></div>'
         '<p>The same rules inside an architecture essay, a stale package list, old session notes, conventions stated twice and slightly contradicting, a glossary and a FAQ.</p>'
         '</div>')
add("Lab 1 · two CLAUDE.md files",
    "Both files carry the same rules. The bloated one wraps them in the material that piles up in real projects: an essay, a package list with stale entries, old session notes, conventions stated twice that slightly contradict each other, a glossary and a FAQ. Give pairs a minute to skim both in claude-md/. Do not say what you expect. Some people will argue that the bloated file explains more and saves exploration turns; that is a fair hypothesis, and it is what the lab tests.",
    slide("Lab 1 · the variants", "Two CLAUDE.md files, same rules", inner, 1, 0))

inner = ('<div class="two-col"><div class="formula"><span class="kk">The metric for the bet</span>'
         '<div class="eq"><b>cost per pass =</b><div class="frac"><span>total spend</span><span>passing runs</span></div></div></div>'
         '<ul class="m7-list"><li>No passing run means no cost per pass: that variant loses.</li>'
         '<li>Dollars are Claude Code\'s estimate at list prices. On Pro or Max you spend plan usage.</li>'
         '<li>One run per cell. The room pools about 20 per variant.</li></ul></div>')
add("Lab 1 · cost per pass",
    "Define the metric before the bet so nobody argues about it afterwards. Cost per pass divides everything a variant spent by the runs that passed. Cache reads make up around ninety percent of the tokens, so the dollar figure mostly tracks cache writes and output. On a subscription nothing is billed; the estimate is still the best common currency for comparing runs. Ten pairs times two tasks gives about twenty runs per variant on the board.",
    slide("Lab 1 · the metric", "Cheaper means cost per passing run", inner, 1, 0))

do_slide(1, "Post your guess, then run both variants", "both laptops",
         "\n".join([C("both laptops, the same guess: lean or bloated"),
                    P("./predict.sh lean"),
                    O("Prediction recorded: lean (pair your-team)"),
                    P("./export-results.sh --lab lab1 --latest", "paste the guess now"),
                    "",
                    P("ROLE=a ./lab1.sh", "laptop a: lean"),
                    P("ROLE=b ./lab1.sh", "laptop b: bloated"),
                    O("  Expected (sonnet)  2 sessions  ~$0.30-0.90  ~4-10 min"),
                    O("This calls Claude and uses your plan. Proceed? [y/N] y"),
                    O("Paste to the board: ./export-results.sh --lab lab1 --latest")]),
         "l1", 18,
         [card("Paste to the board", ["First the guess, straight away.", "Then both laptops paste their runs."]),
          card("Short on usage?", "<code>LITE=1</code> runs one task: one session per laptop.", quiet=True)],
         "Start the time box once most pairs have posted their guess. The prediction line goes to the board before any run, so nobody can adjust it later. Each laptop prints its plan and asks before it spends; answer y. Laptop b only has the bloated half, so its own summary cannot call the bet: the board does that in the debrief. Watch for pairs who run lab1.sh without ROLE on both laptops. If a run shows a harness error, it exports as passed null and the board leaves it out of pass rates; let it go. If a partner hits a usage limit, switch that laptop to LITE=1 or let the other laptop carry on.",
         "Lab 1 · do this")

debrief(1, "First: what did the room predict?",
        ["Hands up: who bet on <b>lean</b>? Who bet on <b>bloated</b>?",
         "Two pairs with opposite bets: defend yours in one sentence.",
         "Name one line in bloated.md you expect to help the agent, and one you expect to hurt."],
        board_card("On the board, lab 1 panel", "Bets only",
                   ["The panel shows the <b>prediction split</b> and hides the result until you press <b>Reveal the result</b>."]),
        "Build the suspense. Put the board on the projector: until you press Reveal the result, the lab 1 panel shows only the bets and how many runs are in. Take a show of hands as well, so pairs who have not posted yet still count. Let two pairs with opposite bets argue in one sentence each. The usual arguments are that lean leaves room in the context, and that bloated saves exploration turns. Both are testable. This slide also buys two minutes for pairs whose runs are still finishing.",
        "Lab 1 · debrief: predictions", dark=True)

debrief(1, "Then: what the room measured",
        ["Did the majority call it? How far apart were pass rate and tokens per run?",
         "Which pairs saw the opposite of the pooled result?",
         "On one run per cell, would you change your team's CLAUDE.md?"],
        board_card("On the board, lab 1 panel", "Pass rate and tokens",
                   ["Press <b>Reveal the result</b>: lean against bloated, every pair pooled, with pass rate, cost per pass and tokens per run."]),
        "Now press Reveal the result and read the panel out: the headline gives the prediction split, the pass rate per variant and how many times the tokens bloated used, and each variant's tile shows its cost per pass. Then turn it into lab 2's question. Each pair saw one run per cell, and some pairs will have seen the opposite of the pooled answer; that is variance, and it is the whole next lab. If the room's result is a tie, or contradicts talk 07, say so plainly: the room's data beats the deck. If fewer than half the pairs have posted, discuss what is there and come back to this panel after the break.",
        "Lab 1 · debrief: results")

# ── Lab 2 ──
beat(2, "Lab 2 · variance", "Variance",
     "Run one task three times per variant and see how far identical runs spread.",
     [("clock", "Time box", '30 min<small>09:55 to 10:25</small>', "tb"),
      ("gauge", "Model sessions", "6 Sonnet per pair: 3 on each laptop", ""),
      ("board", "Board", "6 runs, a dot each, per pair", "")],
     "One task, report-sort-accents, three runs per variant. Same prompt, same repo, same model: any difference between runs is the agent's own variance. Keep the intro short and get the runs started; the concept slides can play while they run if you are behind.",
     "Lab 2 · variance")

x = lambda cx, ok: (f'<circle cx="{cx}" cy="104" r="84" class="ok-dot"/><path d="M{cx - 34} 106 L{cx - 8} 132 L{cx + 38} 76" class="ok-tick lg"/>' if ok else
                    f'<circle cx="{cx}" cy="104" r="84" class="bx-mid"/><path d="M{cx - 28} 76 L{cx + 28} 132 M{cx + 28} 76 L{cx - 28} 132" class="xm"/>')
runs_svg = ('<svg viewBox="0 0 1728 240" role="img" aria-label="The same task run three times: pass, fail, pass.">' +
            "".join(x(c, ok) + f'<text x="{c}" y="228" text-anchor="middle" class="t-cap">run {i + 1}</text>'
                    for i, (c, ok) in enumerate([(288, True), (864, False), (1440, True)])) + "</svg>")
inner = (runs_svg + '<div class="m7-verdicts">'
         '<div class="vr"><span class="k">pass@3</span><span class="res ok"><svg viewBox="0 0 120 120" class="ic" aria-hidden="true"><path d="M16 62 L46 92 L104 28" stroke-width="12"/></svg>PASS</span><p>At least one run passed.<small>Can it do the task at all?</small></p></div>'
         '<div class="vr"><span class="k">pass^3</span><span class="res no">' + '<svg viewBox="0 0 120 120" class="ic" aria-hidden="true"><path d="M26 26 L94 94 M94 26 L26 94" stroke-width="11"/></svg>' + 'FAIL</span><p>Every run had to pass.<small>Can you leave it running unattended?</small></p></div></div>')
add("Lab 2 · pass@k and pass^k",
    "Talk 07 covered this, so keep it to a minute. pass@k asks whether the configuration can do the task at all. pass^k, from the tau-bench paper, asks whether every run passes, which is what you need before you let it run in CI or overnight. pass^k falls fast: an agent with a seventy percent pass rate passes three runs in a row only about a third of the time.",
    slide("Lab 2 · the concept", "pass@k and pass^k answer different questions", inner, 2, 1, note="pass^k: Yao et al., 2024, τ-bench · the board shows both per variant"), cls="dark")

def ivl(lo, hi, p, hot):
    X = lambda v: 20 + v * 1100
    return (f'<svg viewBox="0 0 1160 110" aria-hidden="true"><line x1="20" y1="60" x2="1120" y2="60" class="ln-dim"/>'
            + "".join(f'<line x1="{X(t)}" y1="48" x2="{X(t)}" y2="72" class="ln-dim"/><text x="{X(t)}" y="106" text-anchor="middle" class="t-faint">{t:.1f}</text>' for t in (0, .5, 1))
            + f'<rect x="{X(lo)}" y="36" width="{X(hi) - X(lo)}" height="48" rx="24" class="{"f-coral" if hot else "bx-mid"}" opacity="{1 if hot else .9}"/>'
            + f'<circle cx="{X(p)}" cy="60" r="16" class="f-ink"/>'
            + f'<text x="{X(lo)}" y="24" class="t-mut xs" text-anchor="middle">{lo:.2f}</text><text x="{X(hi)}" y="24" class="t-mut xs" text-anchor="middle">{hi:.2f}</text></svg>')
inner = ('<div class="ivl">'
         f'<div class="r"><div><b>Your pair, 3/3</b><span>Wilson 95% interval</span></div>{ivl(0.44, 1.0, 1.0, False)}</div>'
         f'<div class="r"><div><b>The room, 21/30</b><span>Wilson 95% interval</span></div>{ivl(0.52, 0.83, 0.7, True)}</div>'
         '</div><p class="lead sm">Compare lean and bloated only where the room\'s intervals separate. And <b>0.7³ = 0.34</b>: a 70% agent passes three in a row a third of the time.</p>')
add("Lab 2 · pool the room",
    "This is why the board exists. Three out of three sounds perfect, but with three runs the true pass rate could be as low as 0.44. Thirty runs across the room narrow it to roughly 0.52 to 0.83 for a 70 percent agent. The rule for the debrief: only call lean against bloated if the pooled intervals do not overlap. The numbers on this slide are arithmetic, the Wilson interval the kit computes, not a measurement.",
    slide("Lab 2 · the concept", "Pool the room to narrow the interval", inner, 2, 1))

do_slide(2, "Run one task three times per variant", "both laptops",
         "\n".join([P("ROLE=a ./lab2.sh --yes", "laptop a: lean x 3"),
                    P("ROLE=b ./lab2.sh --yes", "laptop b: bloated x 3"),
                    O("── round 1/3: lean"),
                    O("..."),
                    O("| Variant | Passes/k | pass@k | pass^k | 95% CI    |"),
                    O("| lean    | 3/3      | yes    | yes    | 0.44-1.0  |"),
                    O("Paste to the board: ./export-results.sh --lab lab2 --latest"),
                    P("./export-results.sh --lab lab2 --latest"),
                    "",
                    C("offline, or out of usage: the pooled shape"),
                    P("./lab2.sh --sample")]),
         "l2", 15,
         [card("Paste to the board", "Both laptops, three lines each."),
          card("Runs outlast the box?", "Leave them going over the break. Paste when they finish.", quiet=True)],
         "--yes skips the question because everyone saw the plan in lab 1. Rounds interleave, so an interrupted lab still has balanced data. Three Sonnet sessions per laptop take roughly 6 to 15 minutes; they may run into the break, and that is by design. While they wait, pairs can open results/lab1/*/summary.md and compare turns. If the Wi-Fi or a plan gives out, ./lab2.sh --sample prints the pooled shape from the synthetic set so the discussion still works; say clearly that it is synthetic.",
         "Lab 2 · do this", dark=True)

debrief(2, "Read the spread before the average",
        ["For the same task and setup, how far apart were turns and cost?",
         "Did any pair get 3/3 on one variant and 0/3 on the other?",
         "Do the pooled intervals for lean and bloated overlap? Then lab 1's verdict was noise."],
        board_card("On the board, lab 2 panel", "A dot per run",
                   ["Each pair's runs as dots, the single-run pass rate, and <b>pass@k</b> and <b>pass^k</b> per variant."]),
        "Start with the dots, before any averages: point at one pair's row where identical runs went differently. Then read pass@k and pass^k from the panel. The usual finding is a big gap between them, which is exactly the argument for k of at least three in their own evals. If runs are still coming in, do the debrief on what is there and look at the panel again when you return from the break. Keep it to eight minutes.",
        "Lab 2 · debrief")

brk(15, "10:40", "Leave lab 2 running. <b>Lab 3 calls no model</b>, so late runs can finish while you work.", "b1", 2,
    "Before people leave, check the board: which pairs have not posted lab 2? Their runs can finish over the break, and they paste when they are back. Use the break to rescue any laptop that failed in lab 0 or hit a usage limit: move that pair to LITE=1 or to one laptop. Press T to run the break timer on the projector.",
    "Break", sub="Not posted lab 2 yet? Paste when your runs finish. A laptop in trouble? Tell the facilitator now.")

# ── Lab 3 ──
beat(3, "Lab 3 · break the grader", "Break the grader",
     "Write a wrong solution that a weak checker passes, then harden the checker until only the right one passes.",
     [("clock", "Time box", '35 min<small>10:40 to 11:15</small>', "tb"),
      ("gauge", "Model sessions", "None. Maven only, 5 to 10 s per check.", ""),
      ("term", "While you work", "Lab 2 runs can finish in another terminal", "")],
     "Say it out loud: this lab calls no model. It sits here on purpose, so lab 2 runs that are still going can finish in another terminal while pairs work. Glance at the lab 2 panel on the board now and mention any late arrivals. The task is export-currency-column: a sixth CSV column, currency, after gross, upper case, EUR by default.",
     "Lab 3 · break the grader")

inner = ('<div class="two-col"><table class="mtx"><thead><tr><th>Implementation</th><th>Weak checker</th></tr></thead><tbody>'
         '<tr><td>reference<small>the correct sixth column</small></td><td class="ok">PASS</td></tr>'
         '<tr><td>cheat-1-header-only<small>header gains the column, rows do not</small></td><td class="bad">PASS<small>false pass</small></td></tr>'
         '<tr><td>cheat-2-hardcoded-eur<small>every row says EUR</small></td><td class="bad">PASS<small>false pass</small></td></tr></tbody></table>'
         '<div class="m7-side"><p class="lead sm">The weak checker compiles the code and runs <b>one test</b>: does the header mention currency?</p>'
         '<p class="lead sm">Every pass rate built on it would be fiction.</p></div></div>')
add("Lab 3 · a weak checker",
    "Show what the weak checker does: it compiles the code and runs one test, which checks that the header mentions currency. Both shipped cheats pass it. One adds the header and leaves the rows alone, the other writes EUR on every row whatever the invoice says. Any pass rate or cost per accepted task computed with this checker would be wrong. The checker is part of the eval, and it needs tests of its own.",
    slide("Lab 3 · the problem", "A weak checker passes wrong work", inner, 3, 2))

inner = ('<div class="hard">'
         f'<div class="h weak">{icon("doc")}<div><h3>Run the repo\'s own tests</h3><p><code>RUN_OWN_TESTS=1</code>, <code>TEST_FILTER=</code>. Stops today\'s cheats, but an agent can edit those tests.</p></div><span class="lvl">cheap</span></div>'
         f'<div class="h">{icon("check")}<div><h3>Hidden JUnit tests</h3><p>Concrete rows: a CZK invoice, a lower-case code, no currency, a comma and a newline in a name.</p></div><span class="lvl">better</span></div>'
         f'<div class="h">{icon("dice")}<div><h3>A property check</h3><p>Many invoices from a fixed <code>Random</code> seed, read back with <code>CsvReader</code>, invariants on every row.</p></div><span class="lvl">strong</span></div>'
         '</div>')
add("Lab 3 · harden it",
    "Three ways to harden it, from cheap to strong. Turning on the repo's own tests fails both cheats today, but only because the cheats left the old five-column assertions alone; in a real eval the agent edits those tests, and a cheat that updates them to match itself passes. Hidden tests with concrete rows are better. A property check with a fixed seed is strongest, and the seed keeps failures reproducible. Remind them of the goal: under the column called mine, only the reference passes.",
    slide("Lab 3 · the fix", "Harden the checker, cheapest first", inner, 3, 2, note="Goal: your checker passes the reference and fails everything else"))

do_slide(3, "Cheat, harden, swap, check", "partner A cheats · partner B hardens",
         "\n".join([P("./lab3.sh", "creates lab3-work/repo and lab3-work/checker"),
                    C("A: make CsvExport wrong in a new way, in"),
                    C("   lab3-work/repo/src/main/java/com/example/invoicing/"),
                    C("B: harden lab3-work/checker/ (checker.conf, tests/*.java)"),
                    P("./lab3.sh check", "weak and mine x 4 implementations"),
                    O("| Implementation        | weak | mine |"),
                    O("| yours                 | PASS | fail |"),
                    O("| reference             | PASS | PASS |"),
                    O("| cheat-1-header-only   | PASS | fail |"),
                    O("| cheat-2-hardcoded-eur | PASS | fail |"),
                    C("swap roles and check again; for the debrief:"),
                    P("./lab3.sh answer")]),
         "l3", 22,
         [card("Paste to the board", "Nothing. Keep <code>results/lab3/&lt;ts&gt;/matrix.md</code> for the debrief."),
          card("Stuck?", "<code>./lab3.sh reset</code> starts again. <code>lab3/README.md</code> has ideas.", quiet=True)],
         "Suggested split: five minutes reading lab3/weak/ and writing down what a wrong implementation could get away with, ten minutes of partner A cheating while partner B hardens, then swap. Every check runs Maven offline in five to ten seconds and writes results/lab3/<timestamp>/matrix.md; each cell also prints a short reason. Watch for checkers that fail the reference: that is the most common mistake and the best debrief material. Tell them not to open lab3/answer-key/ before the debrief.",
         "Lab 3 · do this", termcls="sm")

debrief(3, "Did your checker ever fail the right answer?",
        ["A checker that fails the reference rejects a correct agent. Did yours?",
         "Which of your tests would the agent see if they lived in the repo?",
         "What does a false pass cost your team? A false fail?"],
        board_card("On the projector", "<code>./lab3.sh answer</code>",
                   ["Adds the answer key: the own suite, hidden acceptance tests and a <b>property check over 300 seeded invoices</b>."], link=False),
        "Run ./lab3.sh answer on the projector and compare the answer-key column with a couple of pairs' columns. Ask who wrote a checker that failed the reference at some point; a checker that is too strict pushes the pass rate down as surely as a weak one inflates it. Point out the design of the real eval: hidden tests live in eval/hidden/ and are copied in only for grading, and the checker restores pom.xml, mvnw and .mvn/ and requires at least as many own tests as the untouched repo has. Ask which cheats that stops.",
        "Lab 3 · debrief", dark=True)

# ── Lab 4 ──
beat(4, "Lab 4 · read the traces", "Read the traces",
     "Find the turns in your own lab 1 and 2 sessions where the agent repeated work, and decide whether each one was waste.",
     [("clock", "Time box", '25 min<small>11:15 to 11:40</small>', "tb"),
      ("gauge", "Model sessions", "None. It reads the transcripts you already have.", ""),
      ("trace", "Input", "Your stream-json transcripts, or two synthetic ones", "")],
     "The score from labs 1 and 2 tells them what happened; the transcript tells them why. Every run saved its full stream-json transcript, so this lab costs nothing. Pairs without transcripts, because their runs failed or they ran LITE, use the two synthetic sample traces.",
     "Lab 4 · read the traces")

tr = [("t3", "tool", "Read Report.java", "", ""), ("t6", "tool", "Read Report.java", "re-read", "w"),
      ("t7", "plan", "So the plan: look at Report...", "restated plan", "w"), ("t8", "tool", "Bash mvn -q test", "error", "bad"),
      ("t9", "tool", "Bash mvn -q test", "blind retry", "w"), ("t10", "tool", "Grep src", "repeat", "w")]
rws = "".join(
    f'<div class="rw {w if w == "w" else ""}"><span class="no">{n}</span><span class="ty">{t}</span><span>{d}</span>'
    + (f'<span class="tag">{f}</span>' if w == "w" else f'<span class="res {"bad" if w == "bad" else ""}">{f}</span>') + "</div>"
    for n, t, d, f, w in tr)
inner = ('<div class="m7-tr2"><div class="v-win term m7-trace"><div class="tbar"><i class="r"></i><i class="y"></i><i class="g"></i>'
         f'<span>synthetic sample trace · bloated · 17 calls</span></div><div class="wbody">{rws}</div></div>'
         '<div class="m7-call"><span class="k">In this sample</span><div class="big">27%</div>'
         '<p>of the estimated cost went to <b>five flagged turns</b>. A flag marks a candidate; you decide if it is waste.</p></div></div>')
add("Lab 4 · four flags",
    "The trace report flags four patterns: a re-read of an unchanged file, a repeated identical tool call, a blind retry after a failure with the same arguments, and a restated plan. Each flag carries the tokens it added to the context and an estimated cost. This example is the synthetic bloated trace from the kit: five flags, about 27 percent of the session's estimated cost. Stress that a flag is a candidate. A re-read after an edit, or a retry after fixing the command, is sensible work.",
    slide("Lab 4 · the concept", "Four patterns earn a flag", inner, 4, 3), cls="dark")

do_slide(4, "Run the trace report on your own sessions", "trace report",
         "\n".join([P("./lab4.sh", "your lab 1 and lab 2 transcripts"),
                    O("Lab 4 · trace report over 5 transcript(s); no model calls."),
                    O("| Flag          | Count | Tokens | Cost (est) | Share |"),
                    O("| re-read       | 2     | 2.2k   | $0.0337    | 11.3% |"),
                    O("| blind retry   | 1     | 30     | $0.0176    | 5.9%  |"),
                    O("Saved: results/lab4/&lt;ts&gt;/trace-report.md"),
                    "",
                    C("no transcripts of your own, or offline:"),
                    P("./lab4.sh --sample"),
                    C("any stream-json transcript:"),
                    P("./trace-report.sh FILE...")]),
         "l4", 13,
         [card("Then read", "Open a flagged <code>transcript.jsonl</code> and read the turn before each flag."),
          card("Bring to the debrief", "One flag, and the CLAUDE.md line that would prevent it.", quiet=True)],
         "lab4.sh finds every transcript.jsonl under results/lab1 and results/lab2 and writes a Markdown report with a turn table per session. The turn table is the useful part: context size, output tokens and the tool call per turn, with flags marked. Ask pairs to compare one lean and one bloated session side by side. Nothing goes to the board. If a pair has no transcripts, lab4.sh falls back to the synthetic ones by itself and says so.",
         "Lab 4 · do this")

debrief(4, "Which flags were real waste?",
        ["Pick one flag. Real waste, or a sensible check?",
         "Did the bloated sessions carry more flags than the lean ones?",
         "Which one line in a CLAUDE.md or prompt would remove it, and how would you test that change?"],
        board_card("Close the loop", "The next eval run",
                   ["A fix to a CLAUDE.md is a new variant. Labs 1 and 2 are the harness to <b>test it</b>."], link=False),
        "Take two or three flags from the room and let the pair argue whether each one was waste. The strong answer to the third question is a variant: write the CLAUDE.md change, then run lab 1 and lab 2 again with it and compare. That links traces back to evals, which is the spine of talk 07: the score tells you what, the trace tells you why. Keep it to seven minutes and send them to the break.",
        "Lab 4 · debrief", dark=True)

brk(10, "11:50", "Keep your laptops awake. After the break, <b>laptop b starts one command</b> before anything else.", "b2", 4,
    "Short break. While people are out, check the board for lab 1 and lab 2 lines that are still missing and nudge those pairs when they return. Remind yourself of the lab 5 trick: laptop b starts lab 6's Haiku runs in the background at the start of lab 5, so lab 6 fits its 25 minutes.",
    "Break 2", sub="Laptop b: <code>ROLE=b ./lab6.sh --yes</code> is the first command after the break. It runs lab 6 in the background while you score commit messages.")

# ── Lab 5 ──
beat(5, "Lab 5 · judge model", "A model as the judge",
     "Score eight commit messages by hand, run a judge on the same rubric, and measure how far it agrees with you.",
     [("clock", "Time box", '30 min<small>11:50 to 12:20</small>', "tb"),
      ("gauge", "Model calls", "8 judge calls on laptop a, one turn, no tools", ""),
      ("route", "Laptop b", "Starts lab 6's Haiku runs in the background", "")],
     "Some output has no test: nobody can assert that a commit message is good, yet agents write them all day. The usual answer is a judge model with a written rubric. Before anyone trusts one, they should measure how well it agrees with people. Start laptop b's lab 6 command first, then explain.",
     "Lab 5 · judge model")

inner = rail([("Rubric", "accuracy, why, scope, format, overall; 1 to 5"),
              ("Hand scores", "blind: <code>authors.json</code> stays closed"),
              ("Judge", "one <code>claude -p</code> call per message"),
              ("Compare", "exact, within one, Spearman, bias")],
             ["check", "people", "judge", "sheet"])
add("Lab 5 · score first",
    "Four steps. The rubric in lab5/rubric.md has four criteria plus a holistic overall score, each from 1 to 5, and the judge gets exactly that text. Pairs score all eight messages by hand first, without opening authors.json, because knowing who wrote a message changes how people score it. Then the judge scores each message in a separate call with no tools, so it never compares messages. The comparison reports exact agreement, agreement within one point, Spearman rank correlation and the judge's bias.",
    slide("Lab 5 · the method", "Score by hand first, then run the judge", inner, 5, 4, note="The judge gets exactly the rubric text you scored with · one call per message, so it never compares them"))

inner = ('<div class="jd"><div class="v-panel"><span class="kk">Self-preference</span><h3>Judges favour their own family</h3>'
         '<p>Panickssery et al., 2024. <code>lab5.sh</code> splits judge minus you by author: model-written against human-written.</p></div>'
         '<div class="v-panel"><span class="kk">Eight samples cannot show</span><ul>'
         '<li>Agreement or bias, statistically: Spearman 0.7 on 8 spans about -0.01 to 0.94.</li>'
         '<li>Anything about other messages: the board adds raters, not samples.</li>'
         '<li>Real human text, unless <code>authors.json</code> says the stand-ins were replaced.</li></ul></div></div>')
add("Lab 5 · self-preference",
    "Self-preference is the tendency of a model to rate text from its own family higher than people do. The kit splits the gap, judge minus you, by author. Then be honest about the numbers: eight samples, four per group, cannot establish agreement or self-preference. A Spearman of 0.7 on eight samples has a 95 percent interval of roughly minus 0.01 to 0.94. Pooling ten pairs adds raters, not samples. And check authors.json: unless you replaced the four stand-in human messages before the day, all eight were written by Claude, and the self-preference check compares Claude with Claude. Say which case applies today.",
    slide("Lab 5 · the caveat", "Self-preference, and the limits of eight samples", inner, 5, 4))

do_slide(5, "Score, judge, compare", "laptop b first, then laptop a",
         "\n".join([C("laptop b, first: lab 6's Haiku runs, in the background"),
                    P("ROLE=b ./lab6.sh --yes"),
                    "",
                    C("laptop a: read lab5/HANDOUT.md and lab5/rubric.md,"),
                    C("fill lab5/my-scores.csv together, then"),
                    P("./lab5.sh"),
                    O("- Exact agreement: 3/8; within one point: 8/8"),
                    O("- Spearman rank correlation: 0.73"),
                    O("- Mean bias (judge - you): +0.12 points"),
                    P("./export-results.sh --lab lab5 --latest"),
                    C("offline: ./lab5.sh --sample · Haiku judge: LITE=1 ./lab5.sh")]),
         "l5", 16,
         [card("Paste to the board", "Laptop a: 8 judge runs and 8 score lines."),
          card("Do not open", "<code>lab5/authors.json</code> until the judge has run.", quiet=True)],
         "The order matters. Laptop b starts ROLE=b ./lab6.sh --yes first: six Haiku sessions that run in the background for 10 to 25 minutes and are ready when lab 6 starts. Pairs with Ollama who want the local model can start ROLE=b LOCAL_MODEL=qwen3-coder ./lab6.sh --local --yes instead; warn them it is slow. Then both partners score the eight messages together on laptop a, whole numbers 1 to 5 in every cell. Twelve minutes of scoring, three for the judge, the rest reading the agreement. The output on the slide is from the synthetic sample set. If the network is down, ./lab5.sh --sample uses synthetic judge scores against their real hand scores.",
         "Lab 5 · do this", termcls="sm")

debrief(5, "How far does the judge agree with you?",
        ["Where did you and the judge differ by two points or more? Who was right?",
         "Did the judge catch the claim in s2 that the diff does not support?",
         "Is the judge kinder to model-written messages than you are?"],
        board_card("On the board, lab 5 panel", "Judge against the room",
                   ["Each sample's judge score against every pair's score, and the <b>self-preference gap</b>."]),
        "Read the scatter first: where the room's scores spread widely, people disagree with each other, and the judge's agreement with any one pair means less. Then the self-preference gap, with the caveat from two slides back. Sample s2 is polished but claims a round-trip test that is not in the diff: ask who caught it, the judge or the pairs. The practical rule to leave with: before a judge gates anything, score 50 to 100 outputs by hand, from several people.",
        "Lab 5 · debrief", dark=True)

# ── Lab 6 ──
beat(6, "Lab 6 · route by the numbers", "Route by the numbers",
     "Compare Haiku and Sonnet on the same three tasks, and pick by cost per accepted task.",
     [("clock", "Time box", '25 min<small>12:20 to 12:45</small>', "tb"),
      ("gauge", "Model sessions", "6 Haiku on b, already running; about 2 Sonnet on a", ""),
      ("loop", "Reuse", "4 Sonnet runs reused from labs 1-2", "")],
     "Laptop b's Haiku runs started at the beginning of lab 5 and should be done or nearly done. Laptop a reuses its lean Sonnet runs from labs 1 and 2 on the same tasks and tops up about two more. That keeps this lab inside a Pro window. The routing material from the old talk 07 lives here now: three slides while the last runs finish.",
     "Lab 6 · route by the numbers")

inner = ('<div class="v-acc"><div role="img" aria-label="Illustrative suite of ten runs. Model A: $0.10 per run, 3 of 10 accepted, $0.33 per accepted task. Model B: $0.25 per run, 9 of 10 accepted, $0.28 per accepted task.">'
         '<div class="legend"><b>Same suite, 10 runs</b><span><i class="A"></i>Model A</span><span><i class="B"></i>Model B</span></div>'
         '<div class="m"><div class="lab">Cost per run<small>headline</small></div><div class="br"><i class="A" style="width:32%"></i><b>$0.10</b></div><div class="br"><i class="B" style="width:80%"></i><b>$0.25</b></div></div>'
         '<div class="m"><div class="lab">Accepted runs, out of 10</div><div class="br"><i class="A" style="width:24%"></i><b>3</b></div><div class="br"><i class="B" style="width:72%"></i><b>9</b></div></div>'
         '<div class="m"><div class="lab">Cost per accepted task<small class="hot">B is cheaper</small></div><div class="br"><i class="A" style="width:80%"></i><b>$0.33</b></div><div class="br"><i class="B" style="width:68%"></i><b>$0.28</b></div></div></div>'
         '<div class="call"><span class="k">Divide total spend by</span><div class="big o">passes</div><p>A cheap run that fails still costs you the run, and a retry or a review.</p></div></div>')
add("Lab 6 · cost per accepted task",
    "These are talk 07's invented numbers, there to show the arithmetic. Model B costs two and a half times as much per run and is still cheaper per accepted task, because nine of its ten runs pass. The lab measures the same thing on real runs: total spend of a model divided by the runs that passed the hidden tests. Mention the other cost the number leaves out: someone has to notice and handle each failure.",
    slide("Lab 6 · the metric", "Divide by the runs that passed", inner, 6, 5, note="Illustrative numbers from talk 07 · total cost ÷ accepted runs"))

do_slide(6, "Run Sonnet next to your Haiku runs", "laptop a · laptop b",
         "\n".join([C("laptop b: the Haiku runs from lab 5 should be done"),
                    C("laptop a: Sonnet, reusing your lean runs from labs 1-2"),
                    P("ROLE=a ./lab6.sh --yes"),
                    O("  sonnet (claude-sonnet-5) (reusing 4 from labs 1-2)"),
                    O("| Model  | Accepted | Cost per run | Cost per ACCEPTED task |"),
                    P("./export-results.sh --lab lab6 --latest", "both laptops"),
                    "",
                    C("optional, if your plan includes Opus (+6 sessions):"),
                    P("OPUS=1 ROLE=a ./lab6.sh --yes"),
                    C("offline: the pooled shape from the synthetic set"),
                    P("./lab6.sh --sample")]),
         "l6", 12,
         [card("Paste to the board", "Both laptops. The board compares the models."),
          card("Local model", "Started on laptop b in lab 5 with <code>--local</code>. Its cost exports as 0.0.", quiet=True)],
         "Laptop a runs about two Sonnet top-ups, four to ten minutes, while you talk through the next three slides. Each laptop's own summary only shows its own model; the comparison happens on the board, so both laptops must paste. OPUS=1 goes on laptop a's command, not a second run, and only if their plan includes Opus. If laptop b's Haiku runs failed or never started, run ./lab6.sh --sample on the projector for the shape and use whatever the board has.",
         "Lab 6 · do this", dark=True)

axis = ['<svg class="axis" viewBox="0 0 1080 560" role="img" aria-label="Illustrative placement of three models on three axes: A is cheapest, C is smartest and has the finest taste, B sits in the middle.">']
for k, (lab_, pos) in enumerate([("cheaper", {"C": .1, "B": .5, "A": .9}), ("smarter", {"A": .12, "B": .55, "C": .9}), ("finer taste", {"A": .15, "B": .42, "C": .88})]):
    y = 90 + k * 170
    axis.append(f'<text x="0" y="{y - 40}" class="t-cap">{lab_}</text><line x1="0" y1="{y}" x2="1040" y2="{y}" class="ln-dim"/><path d="M1030 {y - 12} L1056 {y} L1030 {y + 12}" class="ln-dim"/>')
    for m, p in pos.items():
        cx = 30 + p * 980
        hot = m == "B"
        axis.append(f'<circle cx="{cx:.0f}" cy="{y}" r="34" class="{"f-coral" if hot else "f-ink"}"/><text x="{cx:.0f}" y="{y + 11}" text-anchor="middle" class="{"t-on" if hot else "t-paper"}">{m}</text>')
axis.append("</svg>")
inner = ('<div class="rt">' + "".join(axis) +
         '<div class="m7-side"><p class="lead"><b>A</b> cheap and fast, for bulk mechanical work.</p>'
         '<p class="lead"><b>B</b> the workhorse.</p><p class="lead"><b>C</b> for hard problems nobody will supervise, or where taste is the bottleneck.</p></div></div>')
add("Lab 6 · no model wins",
    "Models trade off cost, intelligence and taste. Cheap, fast models suit bulk mechanical work; smarter models suit hard problems you will not supervise; the highest-taste models earn their price where UI or copy quality is the bottleneck. The placement is illustrative. Your eval numbers decide where real models sit, and the lab you are running now measures one axis of it, cost per accepted task, on three tasks.",
    slide("Lab 6 · routing", "No model wins on cost, intelligence and taste at once", inner, 6, 5, note="Illustrative placement · your eval numbers decide the real positions"))

inner = ('<div class="hn">'
         '<div class="v-panel"><span class="kk">Cursor · IDE harness</span><div class="big">Auto</div><p>Picks a model per request. Cursor Router on Teams and Enterprise: Cost, Balance or Intelligence.</p></div>'
         '<div class="v-panel"><span class="kk">OpenRouter · one key</span><div class="big">400+</div><p>Models, no markup on tokens, 5.5% card top-up fee. Fallback is on: pin hosts with <code>provider.only</code>.</p></div>'
         '<div class="v-panel"><span class="kk">Pi · minimal harness</span><div class="big">&lt;1,000</div><p>Tokens of prompt and tools. MIT, 15+ providers. Claude needs an API key or extra usage.</p></div></div>')
add("Lab 6 · other harnesses",
    "Three other ways to route, checked in September 2026. Cursor's Auto picks a model per request and bills at the routed model's list price; on Teams and Enterprise the relaunched version is Cursor Router, with Cost, Balance and Intelligence modes. OpenRouter gives one key and one bill over 400-plus models, 457 entries with variants in its public list this month; token prices pass through with no markup, card top-ups carry a 5.5 percent fee with a 0.80 dollar minimum, and fallback is on by default, so a request can land on a host you did not expect. Pi is Mario Zechner's minimal terminal harness, now developed at Earendil under MIT; using Claude through it means an API key or extra-usage billing, so check Anthropic's current rules on subscriptions and third-party tools first.",
    slide("Lab 6 · routing", "Other harnesses route for you", inner, 6, 5, note="Sources: cursor.com, openrouter.ai docs, pi.dev · checked September 2026"), cls="dark")

inner = ('<div class="ow"><div class="m7-facts">'
         '<div><span class="kk">Frontier gap</span><p>NIST\'s CAISI rated <b>GLM-5.2</b> (June, MIT) about level with OpenAI\'s GPT-5.2 of December 2025.</p></div>'
         '<div><span class="kk">On a laptop</span><p><b>Gemma 4 12B</b> fits 16 GB. <b>Qwen 3.6 35B-A3B</b> needs about 23 GB at 4-bit.</p></div>'
         '<div><span class="kk">With Claude Code</span><p>Ollama works, uses no plan, and Anthropic does not support it.</p></div></div>'
         '<div class="m7-when"><div class="col loc"><span class="kk">Go local for</span><h3>Control</h3><p>Private or air-gapped code, marginal cost near zero.</p></div>'
         '<div class="col host"><span class="kk">Stay hosted for</span><h3>Capability</h3><p>Frontier quality, fast turnaround, no hardware.</p></div></div></div>')
add("Lab 6 · open weights and local",
    "Frame it carefully: the gap is closing, and it is still a gap. NIST's CAISI rated GLM-5.2, a roughly 750-billion-parameter mixture of experts released in June under MIT, about level with OpenAI's GPT-5.2 of December 2025, so roughly six months behind. GLM-5.3 moved to a custom licence, so read licences before standardising. On laptops, Gemma 4 12B fits in 16 GB with ollama run gemma4:12b, and Qwen 3.6's 35B-A3B needs about 23 GB at 4-bit, so plan for 32 GB. Claude Code can talk to Ollama's Anthropic-compatible API; Anthropic does not support routing Claude Code to non-Claude models, and while that gateway credential is set the subscription is not used. Local makes sense for control; hosted wins on capability.",
    slide("Lab 6 · routing", "Open weights trail the frontier by about six months", inner, 6, 5, note="Sources: nist.gov CAISI, blog.google, Qwen model cards, docs.ollama.com · checked September 2026"))

debrief(6, "Which model gets which task?",
        ["Which model was cheapest per run, and which per accepted task?",
         "On which task did Haiku hold up, and where did it fall over?",
         "Would you route by task type? How would you check that rule next month?"],
        board_card("On the board, lab 6 panel", "Cost per accepted task",
                   ["Runs, pass rate, cost per run and per accepted task for each model, with a <b>headline</b> naming the cheapest."]),
        "Read the panel's headline first: it names the model that was cheapest per run and the one that was cheapest per accepted task, and whether they differ. Then go per task: the usual pattern is that the cheap model holds up on the mechanical fix and falls over on the task that needs judgement, which is the argument for routing by task type. The answer to how to check the rule next month is the take-home: the same suite, run again. If anyone ran Opus or a local model, ask them for one sentence on it; local cost shows as zero because the kit does not price local tokens.",
        "Lab 6 · debrief", dark=True)

# ── Lab 7 ──
beat(7, "Lab 7 · take it home", "Take it home",
     "Leave with three solved tasks from your own repo and a plan to turn them into an eval this week.",
     [("clock", "Time box", '15 min<small>12:45 to 13:00</small>', "tb"),
      ("gauge", "Model sessions", "None today. CI later needs an API key.", ""),
      ("doc", "Kit", "<code>take-home/GUIDE.md</code> and <code>template/eval/</code>", "")],
     "The invoice app was practice. Their own code is where the numbers mean something. This last block leaves each pair with three candidate tasks picked from their own git history, and the guide covers the rest in about an afternoon.",
     "Lab 7 · take it home")

inner = rail([("Pick three", "a bug fix, a feature, a refactor"),
              ("Write YAML", "quoted <code>base_ref</code>, the issue as prompt"),
              ("Hide tests", "<code>hidden/&lt;task&gt;/Hidden*Test.java</code>"),
              ("Check both ways", "fails on base, passes on fix"),
              ("Run k ≥ 3", "compare cost per accepted task")],
             ["git", "doc", "lock", "shield", "sheet"])
add("Lab 7 · five steps",
    "Walk the five steps in the guide. Pick three small, finished pieces of work with tests: a bug fix, a small feature and a refactor, each under an hour for a person. Write each as task YAML with the base commit quoted, because YAML can read a numeric-looking hash as a number. Turn the tests the fix added into hidden tests. Check the checker both ways, as in lab 3: it must fail on the base and pass on the fix, and ideally fail one plausible wrong solution. Then run each task at least three times and compare variants by cost per accepted task.",
    slide("Lab 7 · the recipe", "Five steps to an eval on your repo", inner, 7, 6))

do_slide(7, "Pick three tasks before you leave", "in your own repository",
         "\n".join([C("fixes that came with a test"),
                    P("git log --oneline -- '*Test.java' | head -20"),
                    C("note two commits per task: base (the parent) and fix"),
                    "",
                    C("later, from the lab folder:"),
                    P("cp -R take-home/template/eval /path/to/your-repo/"),
                    P("git worktree add /tmp/base &lt;base_ref&gt;"),
                    P("eval/checkers/maven-hidden-tests --repo /tmp/base \\"),
                    "    --task example-bugfix",
                    O("  must FAIL on the base, and PASS on the fix")]),
         "l7", 6,
         [card("Paste to the board", "Nothing. Write down three tasks and their commits."),
          card("CI", "<code>take-home/ci/</code> has a GitHub Actions job and a shell script.", quiet=True)],
         "Six minutes: each pair opens one of their own repositories and finds three candidate tasks with git log, noting the base and the fix commit for each. If their laptop does not have a work repository, they can do it from memory of last month's tickets. The worktree and checker commands are what they will run later, following section 4 of the guide. The checker runs Maven offline, so they prefetch once with ./mvnw dependency:go-offline in their repo.",
         "Lab 7 · do this")

debrief(7, "Name your first task",
        ["Each pair: one task, its base commit, and what the hidden test will check.",
         "What will you measure first: a CLAUDE.md change, a model switch, or a new skill?"],
        board_card("In CI", "About 9 sessions",
                   ["Three tasks at k = 3 on Sonnet. CI has no subscription login, so it needs <b>ANTHROPIC_API_KEY</b>, billed per token."], link=False),
        "Go round the room fast, one sentence per pair; this is also the commitment device. Push for small tasks with a clear test. For CI, be clear that it needs an API key billed per token, not a subscription; three tasks at k equals three on Sonnet is roughly nine sessions at a few tens of cents each, and MAX_BUDGET_USD caps every session. Then move to the recap.",
        "Lab 7 · debrief", dark=True)

# ── close ──
rc = [("Lab 1", "Commit the guess before the data."),
      ("Lab 2", "One run is an anecdote. Pool runs, check pass^k."),
      ("Lab 3", "Test the checker: pass the reference, fail plausible wrong work."),
      ("Lab 4", "The score says what failed; the trace says why."),
      ("Lab 5", "Check a judge against people before it gates anything."),
      ("Lab 6", "Route by cost per accepted task."),
      ("Lab 7", "Three real tasks, k ≥ 3, this week.")]
inner = ('<div class="rc">' + "".join(f'<div><span class="kk">{k}</span><p>{v}</p></div>' for k, v in rc) +
         '<div class="defs"><span class="kk">Terms</span><p><b>pass@k</b> any run passed</p><p><b>pass^k</b> every run passed</p>'
         '<p><b>per accepted</b> spend ÷ passes</p><p><b>self-pref.</b> judge favours own family</p></div></div>')
add("Recap",
    "One page to photograph. Read the seven lines, one per lab, and point at the terms card: these are the four definitions on the handout. Tell them the handout in workshops/evals/HANDOUT.md carries the commands and the definitions, and the board stays open, so they can compare their own repo's numbers with the room's later.",
    slide("Close · recap", "One page to keep", inner, None, 7))

inner = ('<div class="v-refs cols2 n7">'
         f'<a href="{BOARD}" target="_blank" rel="noopener"><span class="lt">The room board</span><span class="ld">claude.ai artifact · stays open</span><span class="la" aria-hidden="true">'+icon("arrow")+'</span></a>'
         '<a href="workshops/evals/HANDOUT.md" target="_blank" rel="noopener"><span class="lt">Participant handout</span><span class="ld">workshops/evals/HANDOUT.md</span><span class="la" aria-hidden="true">'+icon("arrow")+'</span></a>'
         '<a href="workshops/evals/lab/take-home/GUIDE.md" target="_blank" rel="noopener"><span class="lt">Take-home guide</span><span class="ld">lab/take-home/GUIDE.md</span><span class="la" aria-hidden="true">'+icon("arrow")+'</span></a>'
         '<a href="measuring-what-works.html" target="_blank" rel="noopener"><span class="lt">Talk 07, the concepts</span><span class="ld">measuring-what-works.html</span><span class="la" aria-hidden="true">'+icon("arrow")+'</span></a>'
         '</div><p class="lead sm">Before you go: tell us <b>one thing to cut</b> and <b>one thing to keep</b>. Your transcripts stay in <code>results/</code> on your laptop.</p>')
add("Thank you",
    "Thank the room. Ask for the two pieces of feedback on the slide, one thing to cut and one to keep, on a sticky note or in the chat. Remind them that nothing ran against their own code or settings, and that results/ in the lab folder holds every transcript if they want to keep them. Leave the board open; export it with Copy all rows as JSON for your own records before you clear it.",
    slide("Close · links", "Thank you. The board stays open.", inner, None, 7), cls="dark")

# ════════════════════════════ ASSEMBLE ════════════════════════════
secs = []
for i, s in enumerate(SLIDES, 1):
    cls = f'slide {s["cls"]} v2 m7 ws {s["extra"]}'.strip()
    body = s["body"]
    secs.append(f'<section class="{cls}" id="slide-{i}" data-label="{esc(s["label"])}" '
                f'data-speaker-notes="{esc(s["notes"])}">\n{body}</section>\n')

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Evals, Hands On · workshop deck</title>
<link rel="icon" href="data:,">

{BASE_HEAD}{WS_CSS}
</head>
<body>
<!--
  Evals, Hands On: the slide layer for the half-day evals workshop
  (workshops/evals/). Ten pairs, labs 0 to 7 on the Java lab kit in
  workshops/evals/lab/, results pooled on the live room board. Facilitator
  run sheet: workshops/evals/FACILITATOR.md; participant sheet:
  workshops/evals/HANDOUT.md. Companion to talk 07 (measuring-what-works.html).
  Runs on the Ember deck-stage component: arrows, Space, Home/End, #N deep
  links; N notes, P presenter window, F fullscreen, T starts or pauses the
  time box on a "Do this" or break slide, Shift+T resets it.
  Status: work in progress until the dry run on a Pro account.
-->
<deck-stage width="1920" height="1080" no-rail>

{"".join(secs)}
</deck-stage>

{TAIL}{TIMER_JS}
</body>
</html>
"""
OUT.write_text(page, encoding="utf-8")
print(f"wrote {OUT} with {len(SLIDES)} slides")
