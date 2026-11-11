// Muhammad Amad portfolio — filters, mobile nav, forms (no backend yet)
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('.menu-btn');
  const links = document.querySelector('.nav-links');
  if (btn && links) btn.addEventListener('click', () => links.classList.toggle('open'));

  // Work filters
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.addEventListener('click', () => {
      document.querySelectorAll('.filter-btn').forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      const f = b.dataset.filter;
      document.querySelectorAll('[data-cat]').forEach(card => {
        card.style.display = (f === 'all' || card.dataset.cat.includes(f)) ? '' : 'none';
      });
    });
  });

  // Contact / registration forms — front-end validation + success state.
  // No email is sent yet: wire Formspree/Resend in README when Amad confirms his email.
  document.querySelectorAll('form[data-demo-form]').forEach(form => {
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const ok = form.parentElement.querySelector('.form-ok');
      if (ok) ok.style.display = 'block';
      form.reset();
      form.querySelector('button[type=submit]').textContent = 'Sent — thank you';
    });
  });

  // Footer year
  document.querySelectorAll('[data-year]').forEach(el => el.textContent = new Date().getFullYear());

  // ---- AnimMaster-style motion pack (original code, vanilla JS) ----
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(pointer: fine)').matches;

  // 1) Split-word hero: each word rises + rotates in, staggered.
  const heroH1 = document.querySelector('.hero h1');
  if (heroH1 && !reduced) {
    heroH1.classList.add('split');
    let wordIndex = 0;
    heroH1.querySelectorAll('.hl > span').forEach((line, li) => {
      const nodes = Array.from(line.childNodes);
      line.textContent = '';
      nodes.forEach(node => {
        const wrapWord = text => {
          const w = document.createElement('span');
          w.className = 'w';
          const wi = document.createElement('span');
          wi.className = 'wi';
          wi.textContent = text;
          wi.style.animationDelay = (li * 140 + wordIndex * 55) + 'ms';
          w.appendChild(wi);
          line.appendChild(w);
          line.appendChild(document.createTextNode(' '));
          wordIndex++;
        };
        if (node.nodeType === 3) {
          node.textContent.split(/\s+/).filter(Boolean).forEach(wrapWord);
        } else {
          // element (em / .outline): split its text the same way, keeping the tag
          const tag = node.tagName.toLowerCase();
          const cls = node.className ? ' class="' + node.className + '"' : '';
          node.textContent.split(/\s+/).filter(Boolean).forEach(t => {
            const w = document.createElement('span');
            w.className = 'w';
            const wi = document.createElement('span');
            wi.className = 'wi';
            wi.innerHTML = '<' + tag + cls + '>' + t + '</' + tag + '>';
            wi.style.animationDelay = (li * 140 + wordIndex * 55) + 'ms';
            w.appendChild(wi);
            line.appendChild(w);
            line.appendChild(document.createTextNode(' '));
            wordIndex++;
          });
        }
      });
    });
  }

  // 2) Magnetic buttons — CTAs drift toward the cursor, snap back on leave.
  if (finePointer && !reduced) {
    document.querySelectorAll('.hero-ctas .btn, .nav-cta, .btn-lime').forEach(btn => {
      btn.classList.add('magnetic');
      btn.addEventListener('mousemove', e => {
        const r = btn.getBoundingClientRect();
        const x = (e.clientX - r.left - r.width / 2) * 0.25;
        const y = (e.clientY - r.top - r.height / 2) * 0.35;
        btn.style.transform = 'translate(' + x.toFixed(1) + 'px,' + (y - 2).toFixed(1) + 'px)';
      });
      btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
    });
  }

  // 3) Cursor glow — soft lime light follows the mouse (dark sections).
  if (finePointer && !reduced) {
    const glow = document.createElement('div');
    glow.id = 'cursor-glow';
    document.body.appendChild(glow);
    let gx = -600, gy = -600, tx = gx, ty = gy, shown = false;
    document.addEventListener('mousemove', e => {
      tx = e.clientX - 260; ty = e.clientY - 260;
      if (!shown) { glow.style.opacity = '1'; shown = true; }
    });
    (function loop() {
      gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
      glow.style.transform = 'translate(' + gx.toFixed(1) + 'px,' + gy.toFixed(1) + 'px)';
      requestAnimationFrame(loop);
    })();
  }

  // 4) 3D tilt — work cards + hero portrait lean toward the cursor.
  if (finePointer && !reduced) {
    document.querySelectorAll('.work-card, .portrait-card, .svc').forEach(card => {
      card.classList.add('tilt');
      const maxTilt = card.classList.contains('svc') ? 4 : 7;
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transition = 'transform .15s ease-out';
        card.style.transform = 'perspective(900px) rotateY(' + (px * maxTilt).toFixed(2) + 'deg) rotateX(' + (-py * maxTilt).toFixed(2) + 'deg) translateY(-4px)';
      });
      card.addEventListener('mouseleave', () => {
        card.style.transition = 'transform .6s cubic-bezier(.2,.7,.2,1)';
        card.style.transform = '';
        setTimeout(() => { card.style.transition = ''; }, 650);
      });
    });
  }

  // 5) Clip-path image reveal — work covers wipe open on scroll.
  // NOTE: observe the CARD, not the cover — a fully-clipped element never
  // intersects (its painted area is empty), so the observer must watch the
  // unclipped parent and open the child cover.
  if (!reduced) {
    const covers = document.querySelectorAll('.work-card .cover');
    covers.forEach(c => { c.style.clipPath = 'inset(0 0 100% 0)'; });
    const cio = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          const cov = en.target.querySelector('.cover');
          if (cov) cov.style.clipPath = 'inset(0 0 0% 0)';
          cio.unobserve(en.target);
        }
      });
    }, { threshold: 0.2 });
    document.querySelectorAll('.work-card').forEach(card => cio.observe(card));
  }

  // 6) Hero parallax — headline column + portrait frame drift apart subtly.
  if (finePointer && !reduced) {
    const hero = document.querySelector('.hero');
    const leftCol = hero && hero.querySelector('.hero-grid > div:first-child');
    const frame = hero && hero.querySelector('.photo-frame');
    if (hero && (leftCol || frame)) {
      let mx = 0, my = 0, cx = 0, cy = 0;
      hero.addEventListener('mousemove', e => {
        const r = hero.getBoundingClientRect();
        mx = (e.clientX - r.left) / r.width - 0.5;
        my = (e.clientY - r.top) / r.height - 0.5;
      });
      hero.addEventListener('mouseleave', () => { mx = 0; my = 0; });
      (function ploop() {
        cx += (mx - cx) * 0.06; cy += (my - cy) * 0.06;
        if (leftCol) leftCol.style.transform = 'translate(' + (cx * -10).toFixed(1) + 'px,' + (cy * -8).toFixed(1) + 'px)';
        if (frame) frame.style.transform = 'translate(' + (cx * 14).toFixed(1) + 'px,' + (cy * 10).toFixed(1) + 'px)';
        requestAnimationFrame(ploop);
      })();
    }
  }

  // ---- Services cards + premium footer pack ----
  // 7) Scroll progress bar (lime line at the very top).
  if (!reduced) {
    const bar = document.createElement('div');
    bar.id = 'scroll-progress';
    document.body.appendChild(bar);
    const updateBar = () => {
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
    };
    document.addEventListener('scroll', updateBar, { passive: true });
    updateBar();
  }

  // Header gains a shadow once the page scrolls (premium sticky header).
  (function () {
    const header = document.querySelector('header.site');
    if (!header) return;
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 12);
    document.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  })();

  // 8) Cursor ring — lime ring trailing the mouse, grows over links/buttons.
  if (finePointer && !reduced) {
    const ring = document.createElement('div');
    ring.id = 'cursor-ring';
    document.body.appendChild(ring);
    let rx = -100, ry = -100, tx2 = rx, ty2 = ry, shown2 = false;
    document.addEventListener('mousemove', e => {
      tx2 = e.clientX; ty2 = e.clientY;
      if (!shown2) { ring.style.opacity = '1'; shown2 = true; }
    });
    document.querySelectorAll('a, button, .svc, .work-card').forEach(el => {
      el.addEventListener('mouseenter', () => ring.classList.add('grow'));
      el.addEventListener('mouseleave', () => ring.classList.remove('grow'));
    });
    (function rloop() {
      rx += (tx2 - rx) * 0.18; ry += (ty2 - ry) * 0.18;
      const half = ring.classList.contains('grow') ? 32 : 19;
      ring.style.transform = 'translate(' + (rx - half).toFixed(1) + 'px,' + (ry - half).toFixed(1) + 'px)';
      requestAnimationFrame(rloop);
    })();
  }

  // 9) Services spotlight — the lime glow inside a card follows the cursor.
  if (finePointer && !reduced) {
    document.querySelectorAll('.svc').forEach(card => {
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  // 10) Brands slider — auto-scrolls, drag it to scrub, pauses while held.
  (function () {
    const strip = document.querySelector('.brand-marquee span');
    if (!strip || reduced) return;
    const half = () => strip.scrollWidth / 2;
    let x = 0, dragging = false, startX = 0, startOffset = 0;
    const parent = strip.closest('.brand-strip');
    function tick() {
      if (!dragging) {
        x -= 0.6;
        if (x <= -half()) x += half();
        strip.style.transform = 'translateX(' + x.toFixed(1) + 'px)';
      }
      requestAnimationFrame(tick);
    }
    parent.addEventListener('pointerdown', e => {
      dragging = true; startX = e.clientX; startOffset = x;
      parent.classList.add('dragging');
    });
    window.addEventListener('pointermove', e => {
      if (!dragging) return;
      x = startOffset + (e.clientX - startX);
      strip.style.transform = 'translateX(' + x.toFixed(1) + 'px)';
    });
    window.addEventListener('pointerup', () => {
      if (!dragging) return;
      dragging = false;
      parent.classList.remove('dragging');
      // wrap back into the seamless range
      while (x <= -half()) x += half();
      while (x > 0) x -= half();
    });
    requestAnimationFrame(tick);
  })();

  // 11) Back to top — smooth scroll (footer link).
  document.querySelectorAll('.to-top').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' });
    });
  });

  // 12) Canvas crowd (Skiper-inspired, original code) — lime particles drift
  // across the hero and gather gently toward the cursor.
  (function () {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas || reduced) return;
    const ctx = canvas.getContext('2d');
    let W = 0, H = 0, mx = -9999, my = -9999;
    const N = 70, pts = [];
    function size() {
      const r = canvas.parentElement.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = r.width; H = r.height;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size();
    window.addEventListener('resize', size);
    for (let i = 0; i < N; i++) {
      pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35, r: Math.random() * 1.8 + .8 });
    }
    canvas.parentElement.addEventListener('mousemove', e => {
      const r = canvas.getBoundingClientRect();
      mx = e.clientX - r.left; my = e.clientY - r.top;
    });
    canvas.parentElement.addEventListener('mouseleave', () => { mx = -9999; my = -9999; });
    (function draw() {
      ctx.clearRect(0, 0, W, H);
      for (const p of pts) {
        const dx = mx - p.x, dy = my - p.y, d = Math.hypot(dx, dy);
        if (d < 160 && d > 0.01) { p.vx += (dx / d) * .012; p.vy += (dy / d) * .012; }
        p.vx *= .985; p.vy *= .985;
        if (Math.abs(p.vx) < .05) p.vx += (Math.random() - .5) * .02;
        if (Math.abs(p.vy) < .05) p.vy += (Math.random() - .5) * .02;
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
        if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(183,254,93,.55)'; ctx.fill();
      }
      for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) {
        const a = pts[i], b = pts[j], d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < 110) {
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = 'rgba(183,254,93,' + (0.14 * (1 - d / 110)).toFixed(3) + ')';
          ctx.lineWidth = 1; ctx.stroke();
        }
      }
      requestAnimationFrame(draw);
    })();
  })();

  // Scroll reveal — cards and sections fade up as they enter view.
  // The .reveal class is added here (not in the HTML), so no-JS never hides content.
  const revealEls = document.querySelectorAll('.work-card,.svc,.step,.course,.timeline>div,.card,details.faq,.tool-panel,.result,.sec-head,.manifesto,.swatch');
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  revealEls.forEach((el, i) => {
    el.classList.add('reveal');
    el.style.transitionDelay = ((i % 4) * 70) + 'ms';
    io.observe(el);
  });
});
