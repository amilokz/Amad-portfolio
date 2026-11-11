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
    document.querySelectorAll('.work-card, .portrait-card').forEach(card => {
      card.classList.add('tilt');
      card.addEventListener('mousemove', e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transition = 'transform .15s ease-out';
        card.style.transform = 'perspective(900px) rotateY(' + (px * 7).toFixed(2) + 'deg) rotateX(' + (-py * 7).toFixed(2) + 'deg) translateY(-4px)';
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

  // Scroll reveal — cards and sections fade up as they enter view.
  // The .reveal class is added here (not in the HTML), so no-JS never hides content.
  const revealEls = document.querySelectorAll('.work-card,.svc,.step,.course,.timeline>div,.card,details.faq,.tool-panel,.result,.sec-head');
  const io = new IntersectionObserver(entries => {
    entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  revealEls.forEach((el, i) => {
    el.classList.add('reveal');
    el.style.transitionDelay = ((i % 4) * 70) + 'ms';
    io.observe(el);
  });
});
