/* ═══════════════════════════════════════════════════════════════════════
   Ivory · deck.js — the shared deck runtime. Load it after deck-stage.js:

     <script src="ivory_design_system/deck-stage.js"></script>
     <script src="ivory_design_system/deck.js"></script>

   It needs no other script and no chrome markup in the deck. It:
   - numbers the slides: every empty .snum gets its two-digit slide number
     (hand-written values win) and, if the deck does not set --deck-total,
     it is set to the number of slides (so the header reads "07 / 30");
   - restarts a slide's <video> from 0 whenever that slide becomes active;
   - adds the presenter aids (top-level window only, not when embedded):
     Notes / Present / Fullscreen buttons (shown on mouse move) and the notes
     panel, unless the page already has .pui-controls / .pui-notes;
     N toggles the notes panel, P opens the presenter window (current slide,
     next slide, notes, elapsed timer, clock), F toggles fullscreen.
     The presenter window copies the deck's <head> stylesheets, so styles.css
     styles it; this file injects no CSS.
   Screenshot hooks (query string): ?chrome opens the notes panel and shows the
   buttons; ?pw renders the presenter window in the page instead of a pop-up.
   No dependencies, no build step. Do not fork per deck.
   ═══════════════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  function two(n){ return (n < 10 ? '0' : '') + n; }

  function init(){
    var ds = document.querySelector('deck-stage');
    if (!ds) return;
    function slides(){ return Array.prototype.slice.call(ds.querySelectorAll(':scope > section')); }

    /* ── slide numbers and total ─────────────────────────────────────── */
    var all = slides();
    all.forEach(function(s, i){
      var n = s.querySelector('.slide-head .snum') || s.querySelector('.snum');
      if (n && !n.textContent.trim()) n.textContent = two(i + 1);
    });
    if (!getComputedStyle(document.documentElement).getPropertyValue('--deck-total').trim()) {
      /* a <style> in <head> (not an inline style) so the presenter window copies it */
      var st = document.createElement('style');
      st.setAttribute('data-ivory', 'deck-total');
      st.textContent = ':root{--deck-total:"' + two(all.length) + '"}';
      document.head.appendChild(st);
    }

    /* ── restart embedded explainer videos when their slide becomes active ── */
    ds.addEventListener('slidechange', function(e){
      var v = e.detail.slide && e.detail.slide.querySelector('video');
      if (v) { v.currentTime = 0; var p = v.play(); if (p && p.catch) p.catch(function(){}); }
    });

    /* ── presenter aids: notes overlay (N), fullscreen (F), presenter window (P) ── */
    if (window.self !== window.top) return; /* skip when embedded by a host/viewer */

    var controls = document.querySelector('.pui-controls');
    if (!controls) {
      controls = document.createElement('div');
      controls.className = 'pui-controls';
      controls.innerHTML =
        '<button type="button" data-pui="notes">Notes<kbd>N</kbd></button>' +
        '<button type="button" data-pui="present">Present<kbd>P</kbd></button>' +
        '<button type="button" data-pui="fullscreen">Fullscreen<kbd>F</kbd></button>';
      document.body.appendChild(controls);
    }
    var notesEl = document.querySelector('.pui-notes');
    if (!notesEl) {
      notesEl = document.createElement('div');
      notesEl.className = 'pui-notes';
      notesEl.setAttribute('role', 'note');
      notesEl.setAttribute('aria-live', 'polite');
      notesEl.innerHTML = '<div class="pui-nhead"></div><div class="pui-nbody"></div>';
      document.body.appendChild(notesEl);
    }
    var nHead = notesEl.querySelector('.pui-nhead');
    var nBody = notesEl.querySelector('.pui-nbody');
    var current = Math.max(0, slides().findIndex(function(s){ return s.hasAttribute('data-deck-active'); })), presenter = null, mouseT = null;
    var q = new URLSearchParams(location.search);

    function noteOf(s){ return s.getAttribute('data-speaker-notes') || 'No notes for this slide.'; }
    function labelOf(s){ return s.getAttribute('data-label') || ''; }

    document.addEventListener('mousemove', function(){
      document.body.classList.add('pui-mouse');
      clearTimeout(mouseT);
      mouseT = setTimeout(function(){ document.body.classList.remove('pui-mouse'); }, 1800);
    });

    function syncNotes(){
      var all = slides(), s = all[current];
      if (!s) return;
      nHead.textContent = 'Notes · ' + labelOf(s) + ' · ' + (current + 1) + ' / ' + all.length;
      nBody.textContent = noteOf(s);
    }
    function toggleNotes(){ notesEl.classList.toggle('open'); if (notesEl.classList.contains('open')) syncNotes(); }

    function toggleFullscreen(){
      if (document.fullscreenElement) { document.exitFullscreen(); }
      else { document.documentElement.requestFullscreen().catch(function(){}); }
    }
    var railWasOff = false;
    document.addEventListener('fullscreenchange', function(){
      if (document.fullscreenElement) {
        railWasOff = ds.hasAttribute('no-rail');
        ds.setAttribute('no-rail', '');
      } else if (!railWasOff) {
        ds.removeAttribute('no-rail');
      }
    });

    /* ?pw: a full-page iframe stands in for the pop-up (screenshots, tests) */
    function inPageWindow(){
      var f = document.createElement('iframe');
      f.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;border:0;z-index:100';
      document.body.appendChild(f);
      return f.contentWindow;
    }

    function openPresenter(){
      if (presenter && !presenter.closed) { presenter.focus(); return; }
      presenter = q.has('pw') ? inPageWindow() : window.open('', 'deck-presenter', 'width=1200,height=760');
      if (!presenter) {
        nHead.textContent = 'Presenter window';
        nBody.textContent = 'The browser blocked the pop-up — allow pop-ups for this page and press P again.';
        notesEl.classList.add('open');
        return;
      }
      var pd = presenter.document;
      pd.open();
      pd.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Presenter — ' + document.title.replace(/</g,'&lt;') + '</title><base href="' + document.baseURI + '"></head><body></body></html>');
      pd.close();
      /* carry the deck's stylesheets over: styles.css styles both the slide clones and the .pw-* UI */
      document.head.querySelectorAll('link[rel="stylesheet"], link[rel="preconnect"], style').forEach(function(el){
        var c = pd.importNode(el, true);
        if (el.tagName === 'LINK' && el.href) c.setAttribute('href', el.href);
        pd.head.appendChild(c);
      });
      pd.body.innerHTML =
        '<div class="pw">' +
          '<div class="pw-bar">' +
            '<span class="cnt"></span><span class="lbl"></span>' +
            '<span class="tmr" title="click to reset">elapsed <b class="el">00:00</b></span>' +
            '<span>clock <b class="ck"></b></span>' +
            '<button data-nav="-1">‹ prev</button><button data-nav="1">next ›</button>' +
          '</div>' +
          '<div class="pw-main">' +
            '<div class="pw-col"><div class="pw-cap">Current</div><div class="pw-box" id="pwCur"><div class="pw-canvas"></div></div></div>' +
            '<div class="pw-col right"><div class="pw-cap">Next</div><div class="pw-box" id="pwNext" style="aspect-ratio:16/9;min-height:120px"><div class="pw-canvas"></div></div>' +
            '<div class="pw-cap" style="margin-top:6px">Notes</div><div class="pw-notes"></div></div>' +
          '</div>' +
        '</div>';

      var t0 = Date.now();
      function tick(){
        if (presenter.closed) return;
        var el = Math.floor((Date.now() - t0) / 1000);
        pd.querySelector('.el').textContent = two(Math.floor(el / 60)) + ':' + two(el % 60);
        var d = new Date();
        pd.querySelector('.ck').textContent = two(d.getHours()) + ':' + two(d.getMinutes());
        presenter.setTimeout(tick, 1000);
      }
      tick();
      pd.querySelector('.tmr').addEventListener('click', function(){ t0 = Date.now(); });

      function fit(boxId){
        var box = pd.getElementById(boxId), cv = box.querySelector('.pw-canvas');
        var k = Math.min(box.clientWidth / 1920, box.clientHeight / 1080);
        cv.style.transform = 'scale(' + k + ')';
        cv.style.left = ((box.clientWidth - 1920 * k) / 2) + 'px';
        cv.style.top = ((box.clientHeight - 1080 * k) / 2) + 'px';
      }
      function fill(boxId, slide){
        var cv = pd.getElementById(boxId).querySelector('.pw-canvas');
        cv.textContent = '';
        if (slide) {
          var c = pd.importNode(slide, true);
          c.setAttribute('data-deck-active', '');
          cv.appendChild(c);
        }
        fit(boxId);
      }
      presenter.__update = function(i){
        var all = slides(), s = all[i];
        if (!s) return;
        var next = i + 1;
        while (next < all.length && all[next].hasAttribute('data-deck-skip')) next++;
        fill('pwCur', s);
        fill('pwNext', all[next] || null);
        pd.querySelector('.cnt').textContent = (i + 1) + ' / ' + all.length;
        pd.querySelector('.lbl').textContent = labelOf(s) + (all[next] ? '   →   next: ' + labelOf(all[next]) : '   ·   last slide');
        pd.querySelector('.pw-notes').textContent = noteOf(s);
      };
      presenter.addEventListener('resize', function(){ fit('pwCur'); fit('pwNext'); });
      pd.addEventListener('keydown', function(e){
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') { e.preventDefault(); ds.next(); }
        else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); ds.prev(); }
        else if (e.key === 'Home') { ds.goTo(0); }
        else if (e.key === 'End') { ds.goTo(slides().length - 1); }
      });
      pd.querySelectorAll('[data-nav]').forEach(function(b){
        b.addEventListener('click', function(){ this.dataset.nav === '1' ? ds.next() : ds.prev(); });
      });
      presenter.__update(current);
    }

    ds.addEventListener('slidechange', function(e){
      current = e.detail.index;
      if (notesEl.classList.contains('open')) syncNotes();
      if (presenter && !presenter.closed && presenter.__update) presenter.__update(current);
    });

    document.addEventListener('keydown', function(e){
      var t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var k = e.key.toLowerCase();
      if (k === 'n') { toggleNotes(); }
      else if (k === 'f') { toggleFullscreen(); }
      else if (k === 'p') { openPresenter(); }
    });
    controls.querySelector('[data-pui="notes"]').addEventListener('click', toggleNotes);
    controls.querySelector('[data-pui="fullscreen"]').addEventListener('click', toggleFullscreen);
    controls.querySelector('[data-pui="present"]').addEventListener('click', openPresenter);

    /* screenshot hooks */
    if (q.has('chrome')) setTimeout(function(){
      controls.style.transition = 'none'; /* no fade, so the capture is deterministic */
      document.body.classList.add('pui-mouse'); clearTimeout(mouseT); toggleNotes();
    }, 400);
    if (q.has('pw')) setTimeout(openPresenter, 400);
  }

  /* normally loaded at the end of <body>, after deck-stage.js; tolerate <head> too */
  if (document.querySelector('deck-stage')) init();
  else document.addEventListener('DOMContentLoaded', init);
})();
