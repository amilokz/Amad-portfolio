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
