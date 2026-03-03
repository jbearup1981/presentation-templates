/* Nexus Benefit Solutions — Presentation Navigation & Scaling */

let cur = 0;
const slides = document.querySelectorAll('.slide');
const total = slides.length;

function go(n) {
  if (n < 0 || n >= total) return;
  slides[cur].classList.remove('active');
  cur = n;
  slides[cur].classList.add('active');
  document.getElementById('counter').textContent = (cur + 1) + ' / ' + total;
  document.getElementById('prevBtn').disabled = cur === 0;
  document.getElementById('nextBtn').disabled = cur === total - 1;
}

function nav(d) { go(cur + d); }

document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nav(1); }
  if (e.key === 'ArrowLeft') nav(-1);
  if (e.key === 'Home') go(0);
  if (e.key === 'End') go(total - 1);
  if (e.key === 'f' || e.key === 'F') toggleFullscreen();
});

function toggleFullscreen() {
  if (!document.fullscreenElement) document.documentElement.requestFullscreen();
  else document.exitFullscreen();
}

// Touch support
let tx = 0;
document.addEventListener('touchstart', function(e) { tx = e.changedTouches[0].screenX; });
document.addEventListener('touchend', function(e) {
  var d = e.changedTouches[0].screenX - tx;
  if (Math.abs(d) > 50) nav(d < 0 ? 1 : -1);
});

// Scale
function rescale() {
  const sw = window.innerWidth / 960;
  const sh = window.innerHeight / 540;
  var s = Math.min(sw, sh, 2) * 0.88;
  document.documentElement.style.setProperty('--scale', s);
}
window.addEventListener('resize', rescale);
rescale();

// Responsive mode
if (new URLSearchParams(window.location.search).get('mode') === 'responsive') {
  document.body.classList.add('responsive-mode');
}

// Button listeners (addEventListener for artifact sandbox compatibility)
document.getElementById('prevBtn').addEventListener('click', function() { nav(-1); });
document.getElementById('nextBtn').addEventListener('click', function() { nav(1); });
var fsBtn = document.getElementById('fullscreenBtn');
if (fsBtn) fsBtn.addEventListener('click', function() { toggleFullscreen(); });

// Init
go(0);
