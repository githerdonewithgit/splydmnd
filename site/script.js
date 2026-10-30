(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Stage-light texture that stands in for photos until real images are added
  function paint(canvas, hue, seed) {
    var r = canvas.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = Math.round(r.width * dpr), h = Math.round(r.height * dpr);
    canvas.width = w; canvas.height = h;
    var c = canvas.getContext('2d');
    c.fillStyle = 'hsl(' + hue + ',30%,7%)'; c.fillRect(0, 0, w, h);
    var s = seed || 1;
    function rnd() { s = (s * 9301 + 49297) % 233280; return s / 233280; }
    c.globalCompositeOperation = 'lighter';
    for (var i = 0; i < 4; i++) {
      var x = rnd() * w, y = rnd() * h * 0.7, rad = (0.35 + rnd() * 0.5) * Math.max(w, h);
      var hh = hue + (rnd() - 0.5) * 60;
      var g = c.createRadialGradient(x, y, 0, x, y, rad);
      g.addColorStop(0, 'hsla(' + hh + ',85%,58%,0.42)');
      g.addColorStop(1, 'hsla(' + hh + ',85%,40%,0)');
      c.fillStyle = g; c.fillRect(0, 0, w, h);
    }
    for (var b = 0; b < 3; b++) {
      var bx = rnd() * w;
      var grad = c.createLinearGradient(bx, 0, bx + w * 0.2, h);
      grad.addColorStop(0, 'hsla(' + hue + ',70%,75%,0.18)');
      grad.addColorStop(1, 'hsla(' + hue + ',70%,75%,0)');
      c.fillStyle = grad;
      c.beginPath(); c.moveTo(bx, 0); c.lineTo(bx + w * 0.04, 0); c.lineTo(bx + w * 0.35, h); c.lineTo(bx + w * 0.05, h); c.closePath(); c.fill();
    }
    c.globalCompositeOperation = 'source-over';
    var img = c.getImageData(0, 0, w, h), d = img.data;
    for (var p = 0; p < d.length; p += 4) { var n = (rnd() - 0.5) * 22; d[p] += n; d[p + 1] += n; d[p + 2] += n; }
    c.putImageData(img, 0, 0);
  }
  function paintAll() {
    document.querySelectorAll('canvas[data-hue]').forEach(function (cv) { paint(cv, +cv.dataset.hue, +cv.dataset.seed); });
  }
  paintAll();
  var rt;
  window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(paintAll, 200); });

  // Mobile menu
  var menuBtn = document.getElementById('menu-btn');
  var menu = document.getElementById('mobile-menu');
  if (menuBtn && menu) {
    var setOpen = function (open) {
      menu.hidden = !open;
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('menu-open', open);
    };
    menuBtn.addEventListener('click', function () { setOpen(menu.hidden); });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) { setOpen(false); menuBtn.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 900 && !menu.hidden) setOpen(false); });
  }

  // Roster filter
  var tabs = document.querySelectorAll('.tab');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
      t.setAttribute('aria-pressed', 'true');
      var f = t.dataset.filter;
      document.querySelectorAll('.card[data-type]').forEach(function (card) {
        card.hidden = !(f === 'all' || card.dataset.type === f);
      });
      paintAll();
    });
  });

  // Hero slider
  var slides = document.querySelectorAll('.slide');
  if (slides.length) {
    var dots = document.querySelectorAll('.dot');
    var counter = document.getElementById('counter');
    var current = 0, timer = null;
    var show = function (i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === current); });
      dots.forEach(function (d, k) {
        d.classList.toggle('is-active', k === current);
        if (k === current) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
      });
      if (counter) counter.textContent = '0' + (current + 1) + ' / 0' + slides.length;
    };
    var stop = function () { if (timer) clearInterval(timer); timer = null; };
    var start = function () { if (reduce) return; stop(); timer = setInterval(function () { show(current + 1); }, 6000); };
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); start(); }); });
    var hero = document.querySelector('.hero');
    hero.addEventListener('mouseenter', stop); hero.addEventListener('mouseleave', start);
    hero.addEventListener('focusin', stop); hero.addEventListener('focusout', start);
    start();
  }

  // Booking form
  var form = document.getElementById('inquiry-form');
  if (form) {
    var status = document.getElementById('f-status');
    var out = document.getElementById('f-out');
    var artistSel = document.getElementById('f-artist');
    var typeSel = document.getElementById('f-type');
    var prefill = function () {
      var slug = (location.hash || '').replace('#', '');
      if (!slug || !artistSel) return;
      var opt = artistSel.querySelector('option[value="' + slug + '"]');
      if (!opt) return;
      artistSel.value = slug;
      typeSel.value = opt.dataset.type === 'artist' ? 'Artist booking' : 'DJ booking';
    };
    prefill();
    window.addEventListener('hashchange', prefill);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = form.elements.name.value.trim();
      if (!name) { status.textContent = 'Add your name so we know who to reply to.'; form.elements.name.focus(); return; }
      var artist = artistSel.options[artistSel.selectedIndex].text;
      var text = ['Inquiry for SPLY/DMND', 'Name: ' + name, 'Company/venue: ' + (form.elements.org.value.trim() || '-'),
        'Looking for: ' + typeSel.value, 'Artist: ' + artist, 'Date: ' + (form.elements.date.value || 'Flexible'), '',
        form.elements.msg.value.trim()].join('\n');
      out.value = text;
      var fallback = function () { out.hidden = false; out.focus(); out.select(); status.textContent = 'Select all and copy the text below into an email.'; };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { out.hidden = true; status.textContent = 'Copied. Paste it into an email to hello@splydmnd.com.'; }, fallback);
      } else { fallback(); }
    });
  }
})();
