// Scales each 1920×1080 .slide to its .frame; ?slide=N shows slide N alone at native size.
(function () {
  var frames = Array.prototype.slice.call(document.querySelectorAll('.frame'));
  var solo = parseInt(new URLSearchParams(location.search).get('slide'), 10);
  if (solo >= 1 && solo <= frames.length) {
    document.body.classList.add('solo');
    frames[solo - 1].classList.add('on');
    return;
  }
  function fit() {
    frames.forEach(function (f) { f.style.setProperty('--s', f.clientWidth / 1920); });
  }
  fit();
  window.addEventListener('resize', fit);
})();
