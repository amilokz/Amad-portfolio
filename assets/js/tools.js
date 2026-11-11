// Free tools for muhammadamad — all client-side, nothing uploaded.
// 1) Logo & Brand Identity Cost Estimator (Pakistan, PKR)
// 2) Drinks Label Size Finder  3) Print Preflight Checker
(function () {
  'use strict';
  const $ = id => document.getElementById(id);
  const fmt = n => 'PKR ' + Math.round(n).toLocaleString('en-PK');

  /* ---------- 1. Cost estimator ----------
     Ranges are indicative 2026 market ranges from published Pakistan guides
     (GoDesign, PrimeMedia, LogicRacks) — shown on the page. NOT a quote. */
  const COST = {
    logo:     { freelancer: [10000, 60000],  agency: [40000, 150000] },
    identity: { freelancer: [40000, 200000], agency: [96000, 400000] }
  };
  function estimate() {
    const svc = document.querySelector('input[name="est-service"]:checked');
    const who = document.querySelector('input[name="est-who"]:checked');
    const concepts = parseInt(($('est-concepts') || {}).value || '3', 10);
    const rush = $('est-rush') && $('est-rush').value === '1';
    const out = $('est-result');
    if (!svc || !who || !out) return;
    const base = COST[svc.value][who.value];
    // More concepts push the estimate toward the top of the range.
    const pos = Math.min(1, Math.max(0, (concepts - 2) / 3)); // 2 concepts=0, 5=1
    const lo = base[0] + (base[1] - base[0]) * pos * 0.35;
    const hi = base[1] * (rush ? 1.25 : 1);
    $('est-range').textContent = fmt(lo) + ' – ' + fmt(hi);
    $('est-note').textContent =
      (svc.value === 'logo' ? 'Logo design' : 'Full brand identity') + ' · ' +
      (who.value === 'freelancer' ? 'Freelancer' : 'Agency / studio') + ' · ' +
      concepts + ' concepts' + (rush ? ' · Rush delivery (+25%)' : '') +
      '. Indicative market range, not a quote — your exact price depends on scope, revisions and deadline.';
  }
  document.querySelectorAll('input[name="est-service"], input[name="est-who"]').forEach(el => el.addEventListener('change', estimate));
  if ($('est-concepts')) $('est-concepts').addEventListener('change', estimate);
  if ($('est-rush')) $('est-rush').addEventListener('change', estimate);
  if ($('est-rush')) $('est-rush').addEventListener('input', estimate);
  if ($('est-result')) estimate();

  /* ---------- 2. Drinks Label Size Finder ---------- */
  const PRESETS = {
    slim250:  { label: '250 ml slim can (energy drink)', dia: 52,  height: 120 },
    can330:   { label: '330 ml standard can',           dia: 66,  height: 100 },
    bottle500:{ label: '500 ml water / cold-drink bottle', dia: 65, height: 110 },
    bottle1000:{label: '1 litre bottle',                 dia: 85,  height: 150 },
    wine750:  { label: '750 ml wine bottle (front label)', dia: 75, height: 100 },
    cola350:  { label: '350 ml glass cola bottle',       dia: 60,  height: 80 }
  };
  function labelCalc() {
    const dia = parseFloat(($('lb-dia') || {}).value);
    const height = parseFloat(($('lb-height') || {}).value);
    const bleed = parseFloat(($('lb-bleed') || {}).value || 3);
    const mode = (document.querySelector('input[name="lb-mode"]:checked') || {}).value || 'wrap';
    const out = $('lb-result');
    if (!dia || !height || !out) return;
    const circ = Math.PI * dia;
    let width;
    if (mode === 'wrap') width = circ - 3;                    // 3 mm gap so ends never collide
    else if (mode === 'overlap') width = circ + 6;            // 6 mm overlap seam
    else width = circ * 0.45;                                 // front label ~45% of circumference
    const r = (n, d) => (Math.round(n * Math.pow(10, d)) / Math.pow(10, d));
    $('lb-circ').textContent = r(circ, 1) + ' mm';
    $('lb-width').textContent = r(width, 1) + ' mm';
    $('lb-height-out').textContent = r(height, 1) + ' mm';
    $('lb-art').textContent = r(width + 2 * bleed, 1) + ' × ' + r(height + 2 * bleed, 1) + ' mm';
    $('lb-inch').textContent = r(width / 25.4, 2) + ' × ' + r(height / 25.4, 2) + ' in';
    $('lb-formula').textContent = 'Circumference = π × ' + dia + ' mm = ' + r(circ, 1) +
      ' mm. ' + (mode === 'wrap' ? 'Wrap width = circumference − 3 mm gap.' :
        mode === 'overlap' ? 'Wrap width = circumference + 6 mm overlap.' :
        'Front label ≈ 45% of circumference.') +
      ' Artwork = label + ' + bleed + ' mm bleed on every side.';
  }
  document.querySelectorAll('.lb-preset').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.lb-preset').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const p = PRESETS[btn.dataset.preset];
      if (p && $('lb-dia') && $('lb-height')) {
        $('lb-dia').value = p.dia; $('lb-height').value = p.height;
      }
      labelCalc();
    });
  });
  ['lb-dia', 'lb-height', 'lb-bleed'].forEach(id => { if ($(id)) $(id).addEventListener('input', labelCalc); });
  document.querySelectorAll('input[name="lb-mode"]').forEach(el => el.addEventListener('change', labelCalc));
  if ($('lb-result')) labelCalc();

  /* ---------- 3. Print Preflight Checker ---------- */
  function preflight() {
    const bleed = parseFloat(($('pf-bleed') || {}).value);
    const dpi = parseFloat(($('pf-dpi') || {}).value);
    const safe = parseFloat(($('pf-safe') || {}).value);
    const color = ($('pf-color') || {}).value;
    const fonts = ($('pf-fonts') || {}).value;
    const format = ($('pf-format') || {}).value;
    const list = $('pf-list'); const score = $('pf-score');
    if (!list || isNaN(bleed)) return;
    const checks = [
      { name: 'Bleed', pass: bleed >= 3, warn: bleed > 0 && bleed < 3,
        ok: 'Bleed is ' + bleed + ' mm — good, the cutter has room to drift.',
        bad: bleed === 0 ? 'No bleed. Any colour reaching the edge will show a white sliver after cutting — extend it ' + 3 + ' mm past the trim.' : 'Bleed is only ' + bleed + ' mm. Most printers ask for 3 mm per edge.' },
      { name: 'Resolution', pass: dpi >= 300, warn: dpi >= 150 && dpi < 300,
        ok: 'Resolution is ' + dpi + ' DPI — sharp in print.',
        bad: dpi < 150 ? 'Resolution is ' + dpi + ' DPI — this will look blurry in print. Rebuild at 300 DPI.' : 'Resolution is ' + dpi + ' DPI — acceptable for large format, risky for anything held in the hand.' },
      { name: 'Safe margin', pass: safe >= 3, warn: safe > 0 && safe < 3,
        ok: 'Text sits ' + safe + ' mm inside the trim — safe from the cutter.',
        bad: 'Text sits only ' + safe + ' mm inside the trim. Keep important text at least 3 mm inside.' },
      { name: 'Colour mode', pass: color === 'cmyk', warn: false,
        ok: 'CMYK — correct for print.',
        bad: 'RGB is a screen colour mode. Convert to CMYK before sending to print, or colours will shift.' },
      { name: 'Fonts', pass: fonts === 'outlined', warn: fonts === 'embedded',
        ok: 'Fonts are outlined — text cannot reflow on the printer’s computer.',
        bad: fonts === 'embedded' ? 'Fonts are embedded, which usually works — outlining them is safer.' : 'Fonts are not embedded or outlined. The printer may substitute a different font.' },
      { name: 'File format', pass: format === 'pdfx', warn: format === 'pdf',
        ok: 'PDF/X — the print-ready standard.',
        bad: format === 'pdf' ? 'Plain PDF usually works — PDF/X is the safer, print-ready choice.' : 'JPG/PNG is fine for a single image, but send print jobs as PDF so text stays sharp.' }
    ];
    let passed = 0;
    list.innerHTML = checks.map(c => {
      const cls = c.pass ? 'pass' : (c.warn ? 'warn' : 'fail');
      const tag = c.pass ? 'PASS' : (c.warn ? 'CHECK' : 'FIX');
      if (c.pass) passed++;
      return '<div class="check"><span class="badge ' + cls + '">' + tag + '</span><div><b>' + c.name + '</b><span>' + (c.pass ? c.ok : c.bad) + '</span></div></div>';
    }).join('');
    score.textContent = passed + ' / ' + checks.length + ' checks passed';
    score.style.color = passed === checks.length ? '#b7fe5d' : (passed >= 4 ? '#ffd166' : '#ff6b6b');
  }
  ['pf-bleed', 'pf-dpi', 'pf-safe', 'pf-color', 'pf-fonts', 'pf-format'].forEach(id => {
    if ($(id)) $(id).addEventListener('input', preflight);
    if ($(id)) $(id).addEventListener('change', preflight);
  });
  if ($('pf-list')) preflight();
})();
