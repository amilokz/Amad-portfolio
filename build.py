#!/usr/bin/env python3
"""Build Muhammad Amad's portfolio as plain static HTML (no build step).
Run: python3 build.py   -> writes index.html, about.html, work.html, ...
Deploy: push the whole folder to Vercel / any static host. No secrets in repo.
Content rule (from the brief): never invent testimonials, metrics, awards,
prices, dates or credentials. Anything unconfirmed is labelled as such.
"""
import os
from pathlib import Path

ROOT = Path(__file__).parent
LINKEDIN = "https://www.linkedin.com/in/muhammad-amad7/"
AKCLNT = "https://akclnt.com"

NAV = [
    ("Work", "work.html"), ("About", "about.html"), ("Academy", "academy.html"),
    ("Tools", "tools/index.html"), ("Insights", "insights.html"), ("Contact", "contact.html"),
]

def header(active=""):
    links = "".join(
        f'<a href="{href}" data-text="{label}" class="{"active" if label.lower() == active else ""}">{label}</a>'
        for label, href in NAV)
    return f"""<header class="site"><nav class="nav">
<a class="wordmark" href="index.html">Muhammad <span>Amad</span></a>
<button class="menu-btn" aria-label="Menu">☰</button>
<div class="nav-links">{links}</div>
<a class="btn btn-lime nav-cta" href="contact.html">Let’s Talk →</a>
</nav></header>"""

def footer():
    # Built by AKCLNT badge sits in the MIDDLE column of the footer, on every page.
    return f"""<footer class="site"><div class="wrap">
<div class="foot-grid">
<div><h4>Muhammad Amad</h4>
<p style="color:#b9c4d0">Graphic designer &amp; creative lead — brand identity, visual communication, and design education.</p>
<p style="color:#8fa0b3;font-size:14px">Based in Peshawar, Pakistan — working with clients in Pakistan and abroad.</p>
<a href="{LINKEDIN}">LinkedIn ↗</a>
<a href="cv.html">Download / view CV</a></div>
<div class="foot-mid"><h4>Built with care</h4>
<a class="akclnt-badge" href="{AKCLNT}" target="_blank" rel="noopener"><span class="dot"></span>Built by&nbsp;<b>AKCLNT</b>&nbsp;<small>akclnt.com</small></a>
<p style="color:#8fa0b3;font-size:13px;margin-top:12px">Design &amp; development by AKCLNT.</p></div>
<div><h4>Explore</h4>
<a href="work.html">Work</a><a href="about.html">About</a><a href="academy.html">Academy</a>
<a href="insights.html">Insights</a><a href="contact.html">Contact</a>
<a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></div>
</div>
<a class="foot-word" href="contact.html">MUHAMMAD AMAD</a>
<div class="foot-bottom"><span>© <span data-year>2026</span> Muhammad Amad. All rights reserved.</span>
<span>Graphic Designer &amp; Creative Lead</span>
<a href="#" class="to-top">↑ Back to top</a></div>
</div></footer>
<script src="assets/js/main.js"></script>"""

PERSON_JSONLD = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"Person","name":"Muhammad Amad","jobTitle":"Graphic Designer & Creative Lead","description":"Graphic designer and creative lead focused on brand identity, visual communication, and design education.","address":{"@type":"PostalAddress","addressLocality":"Peshawar","addressCountry":"PK"},"alumniOf":[{"@type":"EducationalOrganization","name":"University of Agriculture Peshawar"},{"@type":"EducationalOrganization","name":"Saylani Welfare"}],"worksFor":{"@type":"Organization","name":"Markhor Group of Companies"},"knowsAbout":["Brand Identity","Graphic Design","Packaging Design","Campaign Design","Creative Direction","Design Education"],"sameAs":["https://www.linkedin.com/in/muhammad-amad7/"]}</script>"""

def page(title, desc, active, body, dark_body=False, extra_head=""):
    cls = ' class="dark"' if dark_body else ""
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Muhammad Amad</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title} — Muhammad Amad">
<meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<meta property="og:image" content="https://amad-portfolio-psi.vercel.app/assets/img/og-image.png">
<meta name="twitter:card" content="summary_large_image">
{PERSON_JSONLD}{extra_head}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%23111820'/><text x='50' y='68' font-size='52' text-anchor='middle' fill='%23b7fe5d' font-family='Arial' font-weight='bold'>M</text></svg>">
</head><body{cls}>{header(active)}{body}{footer()}</body></html>"""

def subpage(title, desc, active, body):
    """Same as page() but for /work/* — asset paths go one level up."""
    html = page(title, desc, active, body)
    return (html.replace('href="index.html"', 'href="../index.html"')
                .replace('href="work.html"', 'href="../work.html"')
                .replace('href="about.html"', 'href="../about.html"')
                .replace('href="academy.html"', 'href="../academy.html"')
                .replace('href="insights.html"', 'href="../insights.html"')
                .replace('href="contact.html"', 'href="../contact.html"')
                .replace('href="cv.html"', 'href="../cv.html"')
                .replace('href="privacy.html"', 'href="../privacy.html"')
                .replace('href="terms.html"', 'href="../terms.html"')
                .replace('href="tools/index.html"', 'href="../tools/index.html"')
                .replace('href="assets/', 'href="../assets/')
                .replace('src="assets/', 'src="../assets/'))

def toolpage(title, desc, active, body, extra_head=""):
    """Pages under /tools/ — same header/footer, paths one level up.
    The nav 'Tools' link points at the tools index itself."""
    html = page(title, desc, active, body, extra_head=extra_head)
    return (html.replace('href="index.html"', 'href="../index.html"')
                .replace('href="work.html"', 'href="../work.html"')
                .replace('href="about.html"', 'href="../about.html"')
                .replace('href="academy.html"', 'href="../academy.html"')
                .replace('href="insights.html"', 'href="../insights.html"')
                .replace('href="contact.html"', 'href="../contact.html"')
                .replace('href="cv.html"', 'href="../cv.html"')
                .replace('href="privacy.html"', 'href="../privacy.html"')
                .replace('href="terms.html"', 'href="../terms.html"')
                .replace('href="tools/index.html"', 'href="index.html"')
                .replace('href="assets/', 'href="../assets/')
                .replace('src="assets/', 'src="../assets/'))

PROJECTS = [
    ("markhor-cola", "Markhor Cola", "Brand Identity · Packaging", "Brand work, logo, label and packaging.", "cover-cola", "Brand Identity,Packaging"),
    ("markhor-king", "Markhor King", "Packaging · Brand Identity", "Label design, packaging and retail display.", "cover-king", "Packaging,Brand Identity"),
    ("markhor-energy-drink", "Markhor Energy Drink", "Campaigns & Advertising", "Campaigns, sponsorship creative and social content.", "cover-energy", "Campaigns"),
    ("markhor-ginseng", "Markhor Ginseng", "Packaging · Brand Identity", "Label, packaging and supporting brand visuals.", "cover-ginseng", "Packaging,Brand Identity"),
]

def work_card(slug, name, cat, desc, cover, cats):
    return f"""<a class="work-card" href="work/{slug}.html" data-cat="{cats}">
<div class="cover {cover}"><span class="tag">Case study</span>
<div class="can"><b>{name}</b><i>Markhor Group</i></div></div>
<div class="work-body"><h3>{name}</h3><p>{desc}</p>
<div class="meta-row"><span class="pill">{cat}</span><span class="pill">View case study →</span></div></div></a>"""

def write(rel, html):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8")
    print("wrote", rel)

# ---------------------------------------------------------------- HOME
# Hero portrait: drop Amad's real photo at assets/img/portrait.jpg and rebuild —
# it replaces the MA monogram automatically. Until then the monogram shows.
_HAS_PORTRAIT = (ROOT / "assets" / "img" / "portrait.jpg").exists()
portrait_inner = ('<img class="portrait-img" src="assets/img/portrait.jpg" alt="Muhammad Amad — portrait">' if _HAS_PORTRAIT else '<div class="monogram">MA</div>')
portrait_note = ('Photograph: Muhammad Amad.' if _HAS_PORTRAIT else 'Professional portrait to be supplied by Amad — this monogram is a design placeholder, not a photograph.')
# About page portrait (same photo when present; note says where it came from)
about_portrait_inner = ('<img class="portrait-img" src="assets/img/portrait.jpg" alt="Muhammad Amad — portrait" style="width:100%;height:220px;object-fit:cover;border-radius:14px">' if _HAS_PORTRAIT else '<div class="monogram">MA</div>')
about_portrait_note = ('Portrait: Muhammad Amad — LinkedIn profile photo for now; a professional portrait will replace it once he supplies one.' if _HAS_PORTRAIT else 'Professional portrait to be supplied by Amad.')
home = f"""
<section class="hero"><canvas id="hero-canvas"></canvas><div class="wrap hero-grid"><div>
<span class="eyebrow anim-in">Graphic Designer &amp; Creative Lead</span>
<h1><span class="hl"><span>Designing <em>identities.</em></span></span><span class="hl"><span>Building <span class="outline">ideas.</span></span></span><span class="hl"><span>Empowering <em>creatives.</em></span></span></h1>
<p class="hero-sub anim-in" style="animation-delay:.45s">I’m Muhammad Amad, a graphic designer and creative lead focused on brand identity, visual communication, and design education.</p>
<p class="roll-line anim-in" style="animation-delay:.5s"><span class="roll-label">Designing</span> <span class="roll-words"><span class="roll-track"><span>Brand Identities</span><span>Packaging</span><span>Campaign Design</span><span>Creative Direction</span><span>Design Education</span><span>Brand Identities</span></span></span></p>
<div class="hero-ctas anim-in" style="animation-delay:.55s"><a class="btn btn-lime" href="work.html">Explore My Work →</a>
<a class="btn btn-ghost" href="contact.html">Let’s Connect</a></div>
<div class="hero-meta anim-in" style="animation-delay:.7s"><span class="pill">Senior Graphic Designer — Markhor Group</span>
<span class="pill">Graphics Lead — TechKhwa (Remote)</span>
<span class="pill">Peshawar, Pakistan</span>
<span class="pill">BS Information Technology</span></div>
</div>
<div class="portrait-card"><div class="photo-frame">{portrait_inner}<span class="photo-chip chip-a"><i>●</i>Senior Designer — Markhor</span><span class="photo-chip chip-b"><i>●</i>Graphics Lead — TechKhwa</span></div>
<div><div class="role">Muhammad Amad</div><p>Brand identity · Packaging · Campaigns · Creative direction · Design education</p></div>
<p class="portrait-note">{portrait_note}</p></div>
</div></section>
<div class="marquee"><span>Brand Identity ✦ Packaging ✦ Campaign Design ✦ Creative Direction ✦ Design Education ✦ Brand Identity ✦ Packaging ✦ Campaign Design ✦ Creative Direction ✦ Design Education ✦</span></div>
<section class="brand-strip"><div class="wrap"><span class="eyebrow">Brands shaped</span></div><div class="brand-marquee"><span>Markhor Cola ✦ <b>Markhor King</b> ✦ Markhor Energy Drink ✦ <b>Markhor Ginseng</b> ✦ TechKhwa ✦ <b>Markhor Group</b> ✦ Markhor Cola ✦ <b>Markhor King</b> ✦ Markhor Energy Drink ✦ <b>Markhor Ginseng</b> ✦ TechKhwa ✦ <b>Markhor Group</b> ✦</span></div></section>
<section class="light"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Selected Work</span><h2>Work that <em>speaks</em> on the shelf.</h2></div>
<a class="btn btn-navy" href="work.html">All Work →</a></div>
<div class="work-grid">{''.join(work_card(*p) for p in PROJECTS)}</div>
<p style="color:var(--muted);font-size:14px;margin-top:18px">Projects from the brief — Amad has already given permission to publish them. Final artwork and process images will be added once he supplies them; the coloured covers here are design placeholders, not the final artwork.</p>
</div></section>
<section class="white"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">What I Do</span><h2>From idea to <em>identity.</em></h2></div></div>
<div class="svc-grid">
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg></span><span class="num">01</span></div><h3>Brand Identity</h3><p>Logos, visual systems and guidelines that make a brand recognisable at a glance.</p></div>
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg></span><span class="num">02</span></div><h3>Graphic Design</h3><p>Clear, confident visuals for print, social and everyday brand touchpoints.</p></div>
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16.5 9.4L7.55 4.24"/><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.29 7 12 12 20.71 7"/><line x1="12" y1="22" x2="12" y2="12"/></svg></span><span class="num">03</span></div><h3>Packaging</h3><p>Labels and packs designed to stand out on a real shelf — and read clearly in hand.</p></div>
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/></svg></span><span class="num">04</span></div><h3>Campaign Design</h3><p>Campaign visuals and sponsorship creative that carry one idea across every format.</p></div>
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg></span><span class="num">05</span></div><h3>Creative Direction</h3><p>Direction across a project — concept, exploration, final artwork and rollout.</p></div>
<div class="svc"><div class="svc-top"><span class="svc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span><span class="num">06</span></div><h3>Design Education</h3><p>Teaching graphic design — practical workflow, honest critique and real project habits.</p></div>
</div></div></section>
<section class="white"><div class="wrap" style="max-width:920px">
<p class="manifesto reveal">A brand is <em>remembered</em> when every touchpoint tells the same story.</p>
<p class="lead" style="margin-top:18px">Logo, pack, feed, shelf — one idea, carried everywhere. That is the work.</p>
</div></section>
<section class="darksec"><div class="wrap two"><div>
<span class="eyebrow">About</span><h2 style="font-size:clamp(32px,4vw,48px);margin-top:10px">A designer who teaches what he <em style="color:var(--lime);font-style:normal">practices.</em></h2>
<p class="lead">I work on brand identity and packaging by day, and I teach design so the next designer starts further ahead than I did.</p>
<p style="color:#b9c4d0">Senior Graphic Designer at Markhor Group of Companies, and Graphics Lead at TechKhwa (remote). BS Information Technology, University of Agriculture Peshawar, 2021–2025.</p>
<a class="btn btn-lime" href="about.html">More About Me →</a></div>
<div class="timeline">
<div><span class="when">Now</span><h3>Senior Graphic Designer — Markhor Group of Companies</h3><p>Peshawar. Brand and packaging work across Markhor brands.</p></div>
<div><span class="when">Now</span><h3>Graphics Lead — TechKhwa (Remote)</h3><p>Leading graphics work and design education.</p></div>
<div><span class="when">2021 – 2025</span><h3>BS Information Technology</h3><p>University of Agriculture Peshawar.</p></div>
<div><span class="when">Training</span><h3>Graphic Design &amp; UI/UX Design</h3><p>SMIT Peshawar.</p></div>
<div><span class="when">2022 – 2023</span><h3>Diploma in Graphic Design</h3><p>Saylani Welfare — Grade A.</p></div>
</div></div></section>
<section class="light"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Process</span><h2>From concept <em>to reality.</em></h2></div></div>
<div class="steps">
<div class="step"><b>01</b><h3>Sketch</h3><p>Understand the brief, the audience and the shelf — then sketch fast and wide.</p></div>
<div class="step"><b>02</b><h3>Explore</h3><p>Test directions, type and colour. Keep what survives honest critique.</p></div>
<div class="step"><b>03</b><h3>Design</h3><p>Refine the chosen direction into final artwork, ready for print and screen.</p></div>
<div class="step"><b>04</b><h3>Deliver</h3><p>Hand over clean files, guidelines and the real-world result — no surprises.</p></div>
</div></div></section>
<section class="white"><div class="wrap two"><div>
<span class="eyebrow">Academy</span><h2 style="font-size:clamp(32px,4vw,48px);margin-top:10px">Learn design the <em style="color:var(--lime-dark);font-style:normal">practical</em> way.</h2>
<p class="lead">Courses are being prepared — catalogue, curriculum and registration will be published once Amad confirms course names, dates and fees. No payment is taken at launch.</p>
<a class="btn btn-navy" href="academy.html">See the Academy →</a></div>
<div class="card"><h3>Join the interest list</h3><p style="color:var(--muted)">Tell me which topic interests you and I’ll let you know when enrolment opens.</p>
<p><span class="pill">Brand Identity</span> <span class="pill">Packaging</span> <span class="pill">Design Workflow</span></p>
<a class="btn btn-lime" href="academy.html#register">Register Interest →</a></div></div></section>
<section class="light"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Free Tools</span><h2>Free tools for <em>designers &amp; brands.</em></h2></div>
<a class="btn btn-navy" href="tools/index.html">All Free Tools →</a></div>
<p class="lead" style="max-width:640px">Three free tools I built for the people I work with — small businesses, packaging buyers and design students. They run entirely in your browser: no sign-up, nothing uploaded.</p>
<div class="svc-grid" style="margin-top:28px">
<div class="svc"><span class="num">Free · No sign-up</span><h3>Logo &amp; Brand Identity Cost Estimator</h3><p>What does a logo or a full brand identity cost in Pakistan? Pick your deliverables and get an indicative PKR range from published 2026 market guides.</p><p><a href="tools/design-cost-estimator.html">Use the estimator →</a></p></div>
<div class="svc"><span class="num">Free · No sign-up</span><h3>Drinks Label Size Finder</h3><p>Pick your bottle or can — cola, energy drink, water, wine — and get the exact label size, wrap width and print-ready artwork size in mm and inches.</p><p><a href="tools/label-size-finder.html">Find your label size →</a></p></div>
<div class="svc"><span class="num">Free · No sign-up</span><h3>Print Preflight Checker</h3><p>About to send artwork to print? Check bleed, resolution, safe margin, colour mode, fonts and file format — and fix what fails before you pay for a reprint.</p><p><a href="tools/print-preflight-checker.html">Check your artwork →</a></p></div>
</div></div></section>
<section class="white"><div class="wrap" style="max-width:820px">
<div class="sec-head"><div><span class="eyebrow">FAQ</span><h2>Questions, <em>answered.</em></h2></div></div>
<details class="faq"><summary>What services does Muhammad Amad offer?</summary><p>Brand identity, graphic design, packaging, campaign design, creative direction, and design education — for businesses in Pakistan and abroad.</p></details>
<details class="faq"><summary>Where is Muhammad Amad based?</summary><p>In Peshawar, Pakistan. He works as Senior Graphic Designer at Markhor Group of Companies and as Graphics Lead at TechKhwa (remote).</p></details>
<details class="faq"><summary>Are the free tools really free?</summary><p>Yes. The cost estimator, label size finder and preflight checker all run entirely in your browser. No sign-up, no account, and nothing you enter is uploaded or stored.</p></details>
<details class="faq"><summary>How do I get an exact price for my project?</summary><p>Use the free cost estimator for an indicative PKR market range, then send an inquiry through the contact page — every project gets an exact written quote.</p></details>
</div></section>
<section class="darksec"><div class="wrap" style="text-align:center">
<span class="eyebrow" style="justify-content:center">Contact</span>
<h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Have a brand to build?<br>Let’s <em style="color:var(--lime);font-style:normal">talk.</em></h2>
<p class="lead" style="max-width:560px;margin:0 auto 28px">Branding, packaging, a campaign — or a question about learning design. Send an inquiry and I’ll get back to you.</p>
<a class="btn btn-lime" href="contact.html">Start a Project →</a>
<a class="btn btn-ghost" href="https://www.linkedin.com/in/muhammad-amad7/" target="_blank" rel="noopener">LinkedIn ↗</a>
</div></section>
"""
HOME_SCHEMA = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"Muhammad Amad","url":"https://amad-portfolio-psi.vercel.app/","author":{"@type":"Person","name":"Muhammad Amad"}}</script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What services does Muhammad Amad offer?","acceptedAnswer":{"@type":"Answer","text":"Brand identity, graphic design, packaging, campaign design, creative direction, and design education — for businesses in Pakistan and abroad."}},{"@type":"Question","name":"Where is Muhammad Amad based?","acceptedAnswer":{"@type":"Answer","text":"In Peshawar, Pakistan. He works as Senior Graphic Designer at Markhor Group of Companies and as Graphics Lead at TechKhwa (remote)."}},{"@type":"Question","name":"Are the free tools really free?","acceptedAnswer":{"@type":"Answer","text":"Yes. The cost estimator, label size finder and preflight checker all run entirely in your browser. No sign-up, no account, and nothing you enter is uploaded or stored."}},{"@type":"Question","name":"How do I get an exact price for my project?","acceptedAnswer":{"@type":"Answer","text":"Use the free cost estimator for an indicative PKR market range, then send an inquiry through the contact page — every project gets an exact written quote."}}]}</script>"""
write("index.html", page("Muhammad Amad — Graphic Designer & Creative Lead",
    "Muhammad Amad is a graphic designer and creative lead focused on brand identity, visual communication, and design education.", "home", home, dark_body=True, extra_head=HOME_SCHEMA))

# ---------------------------------------------------------------- ABOUT
about = f"""
<section class="light"><div class="wrap two"><div>
<span class="eyebrow">About</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Design is how an idea becomes <em style="color:var(--lime-dark);font-style:normal">real.</em></h2>
<p class="lead">I’m Muhammad Amad — a graphic designer and creative lead working on brand identity, packaging and campaigns, and teaching design alongside the work.</p>
<p>I entered design through hands-on practice and formal training, and grew into leadership and teaching roles. My work is practical: a brand has to survive on a real shelf, in a real feed, and in a real brief — not just in a portfolio mockup.</p>
<p>As a teacher, I focus on workflow over shortcuts: how to approach a brand project, how to move from sketch to final design, and how to use AI as part of a designer’s process — not as a replacement for judgement.</p>
<div class="note"><b>About this page:</b> every fact here follows Amad’s brief, which Amad has confirmed is correct. His portrait, CV PDF and final project artwork are placeholders until he supplies them — permission to publish the work is already given.</div>
</div><div>
<div class="portrait-card" style="min-height:320px"><div>{about_portrait_inner}<div class="role" style="margin-top:14px">Muhammad Amad</div><p>Graphic Designer &amp; Creative Lead</p></div>
<p class="portrait-note">{about_portrait_note}</p></div>
<div class="card" style="margin-top:20px"><h3>Tools I use</h3><p style="color:var(--muted)">Adobe Photoshop · Adobe Illustrator</p>
<h3 style="margin-top:20px">Capabilities</h3><p style="color:var(--muted)">Brand identity · Graphic design · Packaging · Campaign visuals · Creative direction · Teaching &amp; mentoring</p></div>
</div></div></section>
<section class="white"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Experience &amp; Education</span><h2>My <em>journey</em> so far.</h2></div></div>
<div class="timeline">
<div><span class="when">Current</span><h3>Senior Graphic Designer — Markhor Group of Companies</h3><p>Brand and packaging design.</p></div>
<div><span class="when">Current</span><h3>Graphics Lead — TechKhwa (Remote)</h3><p>Graphics leadership and design education.</p></div>
<div><span class="when">Experience</span><h3>Graphic Design — approximately 4 years</h3><p>As stated in the brief, confirmed by Amad.</p></div>
<div><span class="when">2021 – 2025</span><h3>BS Information Technology — University of Agriculture Peshawar</h3><p>Undergraduate degree, 2021–2025.</p></div>
<div><span class="when">Training</span><h3>Graphic Design and UI/UX Design — SMIT Peshawar</h3><p>Training / certificates — exact certificate names to be supplied by Amad.</p></div>
<div><span class="when">2022 – 2023</span><h3>Diploma in Graphic Design — Saylani Welfare</h3><p>Jan 2022 – Dec 2023 · Grade A.</p></div>
</div></div></section>
<section class="white"><div class="wrap"><div class="sec-head"><div><span class="eyebrow">Brand Palette</span><h2>The colours this <em>site</em> is built on.</h2></div></div>
<p class="lead" style="max-width:640px">The palette comes from the brief's own design tokens — the same dark, navy and lime that run through this website.</p>
<div class="palette-grid">
<div class="swatch reveal"><i style="background:#111820"></i><div><b>Studio Dark</b><small>#111820 — backgrounds, hero</small></div></div>
<div class="swatch reveal"><i style="background:#142B4D"></i><div><b>Deep Navy</b><small>#142B4D — cards, depth</small></div></div>
<div class="swatch reveal"><i style="background:#B7FE5D"></i><div><b>Signal Lime</b><small>#B7FE5D — accents, calls to action</small></div></div>
<div class="swatch reveal"><i style="background:#F5F6F3;border-bottom:1px solid var(--border)"></i><div><b>Paper Light</b><small>#F5F6F3 — light sections</small></div></div>
</div></div></section>
<section class="light"><div class="wrap" style="text-align:center">
<h2>Want to work together?</h2><p class="lead">See the work, then send an inquiry.</p>
<a class="btn btn-navy" href="work.html">View Work →</a> <a class="btn btn-lime" href="contact.html">Contact Me →</a>
</div></section>
"""
write("about.html", page("About — Muhammad Amad",
    "About Muhammad Amad: graphic designer and creative lead — Senior Graphic Designer at Markhor Group, Graphics Lead at TechKhwa, BS IT 2021–2025.", "about", about))

# ---------------------------------------------------------------- WORK
work = """
<section class="light"><div class="wrap">
<span class="eyebrow">Portfolio</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Selected <em style="color:var(--lime-dark);font-style:normal">work.</em></h2>
<p class="lead" style="max-width:640px">Brand identity, packaging and campaign work. Each case study shows what was done and what is still to be confirmed — no invented results.</p>
<div class="filters" style="margin-top:28px">
<button class="filter-btn active" data-filter="all">All</button>
<button class="filter-btn" data-filter="Brand Identity">Brand Identity</button>
<button class="filter-btn" data-filter="Packaging">Packaging</button>
<button class="filter-btn" data-filter="Campaigns">Campaigns &amp; Advertising</button>
</div>
<div class="work-grid">""" + ''.join(work_card(*p) for p in PROJECTS) + """</div>
<div class="note" style="margin-top:28px"><b>Permission confirmed:</b> Amad has already given permission to publish these projects (confirmed by Komil). The coloured covers on this page are design placeholders — final artwork and process images will replace them once Amad supplies them.</div>
</div></section>
"""
write("work.html", page("Work — Muhammad Amad",
    "Selected work by Muhammad Amad: Markhor Cola, Markhor King, Markhor Energy Drink and Markhor Ginseng — brand identity, packaging and campaigns.", "work", work))

# ---------------------------------------------------------------- CASE STUDIES
CASES = {
 "markhor-cola": ("Markhor Cola", "Brand Identity · Packaging", "cover-cola",
   "Brand work, logo, label and packaging for Markhor Cola.",
   "The brand work for Markhor Cola — identity, logo and label/packaging, with production or market imagery if approved for publication."),
 "markhor-king": ("Markhor King", "Packaging · Brand Identity", "cover-king",
   "Label design, packaging and retail display for Markhor King.",
   "Label design and packaging for Markhor King, including process work and physical retail implementation where permission allows."),
 "markhor-energy-drink": ("Markhor Energy Drink", "Campaigns & Advertising", "cover-energy",
   "Campaigns, sponsorship creative and social content for Markhor Energy Drink.",
   "Campaigns and sponsorship creative for Markhor Energy Drink, with promotional visuals and social content."),
 "markhor-ginseng": ("Markhor Ginseng", "Packaging · Brand Identity", "cover-ginseng",
   "Label, packaging and supporting brand visuals for Markhor Ginseng.",
   "Label and packaging for Markhor Ginseng, with supporting brand visuals."),
}
for slug, (name, cat, cover, desc, overview) in CASES.items():
    others = [p for p in PROJECTS if p[0] != slug]
    nxt = others[0]
    body = f"""
<section class="case-hero"><div class="wrap">
<span class="eyebrow">{cat}</span><h1 style="margin-top:12px">{name}</h1>
<p class="hero-sub">{desc}</p>
<div class="hero-meta"><span class="pill">Client / Brand: Markhor Group</span><span class="pill">Role: Graphic Designer</span><span class="pill">Year: to be confirmed</span></div>
</div></section>
<section class="light"><div class="wrap case-grid"><div>
<div class="cover {cover}" style="border-radius:22px;height:320px"><div class="can"><b>{name}</b><i>Markhor Group</i></div></div>
<p style="color:var(--muted);font-size:14px;margin-top:10px">Placeholder cover — final artwork to be supplied by Amad.</p>
<h2 style="margin-top:32px">Overview</h2><p>{overview}</p>
<h2>Challenge</h2><p>To be written with Amad: the design or communication problem, described accurately — no invented problem statement will be published here.</p>
<h2>Approach</h2><p>To be written with Amad: research, references, concept and design direction, where shareable.</p>
<h2>Process</h2><p>Sketches, iterations, exploration and final artwork will be added once Amad supplies the approved material.</p>
<h2>Final work</h2><p>High-resolution visuals, details, mockups and real-world photographs will be added once approved. Mockups will be labelled as mockups; real photographs as real photographs.</p>
<h2>Outcome</h2><p>No outcome or metric is claimed for this project. Verified implementation or results will be added only if Amad supplies evidence and approves the wording.</p>
<div class="note"><b>Credits &amp; permission:</b> permission to publish this project is already given by Amad. His exact contribution and collaborators will be listed once the final artwork is supplied. Work is not presented as sole authorship where it was collaborative.</div>
</div><div class="card"><h3>Project details</h3><div class="kv">
<div><b>Project</b>{name}</div><div><b>Category</b>{cat}</div>
<div><b>Client / Brand</b>Markhor Group</div><div><b>Role</b>Graphic Designer</div>
<div><b>Year</b>To be confirmed</div><div><b>Status</b>Case study in preparation</div>
</div><p style="margin-top:20px"><a class="btn btn-navy" href="../contact.html">Discuss a Similar Project →</a></p>
<p><a href="../work.html">← Back to all work</a></p></div></div></div></section>
<section class="white"><div class="wrap"><h2>Next project</h2>
<div class="work-grid">{work_card(*nxt).replace('href="work/', 'href="../work/')}</div></div></section>
"""
    write(f"work/{slug}.html", subpage(f"{name} — Muhammad Amad",
        f"{name}: {desc}", "work", body))

# ---------------------------------------------------------------- ACADEMY
academy = """
<section class="light"><div class="wrap">
<span class="eyebrow">Academy</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Learn design the <em style="color:var(--lime-dark);font-style:normal">practical</em> way.</h2>
<p class="lead" style="max-width:680px">I teach graphic design the way I practise it — real briefs, real workflow, honest critique. Courses are being prepared now.</p>
<div class="note" style="margin-top:20px"><b>Launch model:</b> course catalogue + registration of interest only. No full LMS, no online payments, no automated certificates at launch. Course names, dates, fees, format and curriculum will be published only once Amad confirms them.</div>
</div></section>
<section class="white"><div class="wrap">
<div class="sec-head"><div><span class="eyebrow">Proposed Topics</span><h2>What I’ll <em>teach.</em></h2></div></div>
<div class="course-grid">
<div class="course"><span class="status">Coming soon — interest open</span><h3>Brand Identity Foundations</h3><p>How to approach a brand identity project — from brief and research to a usable visual system.</p><p><b>Level:</b> to be confirmed · <b>Format:</b> to be confirmed</p></div>
<div class="course"><span class="status">Coming soon — interest open</span><h3>Packaging Design in Practice</h3><p>What makes packaging work on a real shelf — label hierarchy, print thinking and real-world checks.</p><p><b>Level:</b> to be confirmed · <b>Format:</b> to be confirmed</p></div>
<div class="course"><span class="status">Coming soon — interest open</span><h3>Design Workflow &amp; AI Tools</h3><p>From sketch to final design: a practical creative workflow, including how to use AI as part of a designer’s process.</p><p><b>Level:</b> to be confirmed · <b>Format:</b> to be confirmed</p></div>
</div>
<p style="color:var(--muted);font-size:14px;margin-top:16px">These are proposed topics from the brief’s article ideas — not confirmed course titles, dates or prices.</p>
</div></section>
<section class="light" id="register"><div class="wrap two"><div>
<h2>Register your interest</h2><p class="lead">Leave your details and I’ll let you know when enrolment opens — no payment, no commitment.</p>
<p style="color:var(--muted)">Student work and testimonials will only be shown with the student’s permission.</p></div>
<div class="card"><form data-demo-form>
<label>Name <input required name="name" placeholder="Your full name"></label>
<label>Email <input required type="email" name="email" placeholder="you@example.com"></label>
<label>Course interest <select name="course"><option>Brand Identity Foundations</option><option>Packaging Design in Practice</option><option>Design Workflow &amp; AI Tools</option><option>Not sure yet — keep me updated</option></select></label>
<label>Experience level <select name="level"><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select></label>
<label><span><input type="checkbox" required style="width:auto"> I agree to be contacted about this course. (Privacy policy)</span></label>
<button class="btn btn-lime" type="submit">Register Interest →</button>
</form><div class="form-ok"><b>Thank you.</b> Your interest has been noted on this page. Email delivery will be connected once Amad confirms his professional email address.</div></div>
</div></section>
"""
write("academy.html", page("Academy — Muhammad Amad",
    "Learn graphic design with Muhammad Amad: brand identity, packaging and practical design workflow. Courses coming soon — register your interest.", "academy", academy))

# ---------------------------------------------------------------- INSIGHTS
insights = """
<section class="light"><div class="wrap">
<span class="eyebrow">Insights</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Notes on design, <em style="color:var(--lime-dark);font-style:normal">honestly.</em></h2>
<p class="lead" style="max-width:640px">No articles are published yet. The topics below are planned — each will be published as a full, useful article, not a placeholder post.</p>
<div class="course-grid" style="margin-top:32px">
<div class="course"><span class="status">Writing soon</span><h3>How I approach a brand identity project</h3><p>Brand Identity · Planned article</p></div>
<div class="course"><span class="status">Writing soon</span><h3>From sketch to final design: a practical creative workflow</h3><p>Creative Process · Planned article</p></div>
<div class="course"><span class="status">Writing soon</span><h3>How I use AI as part of a designer’s process</h3><p>AI in Design · Planned article</p></div>
<div class="course"><span class="status">Writing soon</span><h3>Lessons from teaching graphic design</h3><p>Teaching · Planned article</p></div>
<div class="course"><span class="status">Writing soon</span><h3>What makes packaging design work on a real shelf?</h3><p>Packaging · Planned article</p></div>
<div class="course"><span class="status">Writing soon</span><h3>Behind the scenes of a selected case study</h3><p>Creative Process · Planned article</p></div>
</div></div></section>
"""
write("insights.html", page("Insights — Muhammad Amad",
    "Design notes by Muhammad Amad on brand identity, packaging, creative process and teaching. Articles coming soon.", "insights", insights))

# ---------------------------------------------------------------- CONTACT
contact = """
<section class="light"><div class="wrap two"><div>
<span class="eyebrow">Contact</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Let’s build something <em style="color:var(--lime-dark);font-style:normal">worth looking at.</em></h2>
<p class="lead">Branding, packaging, a campaign, a collaboration — or a question about learning design. Tell me a little about it and I’ll reply.</p>
<div class="card"><h3>Other ways to reach me</h3>
<p><b>LinkedIn</b><br><a href="https://www.linkedin.com/in/muhammad-amad7/" target="_blank" rel="noopener">linkedin.com/in/muhammad-amad7/ ↗</a></p>
<p style="color:var(--muted)">Professional email and WhatsApp will be listed here only once Amad confirms the exact public contact details. Behance, Instagram and Pinterest will be added only once he confirms those accounts.</p></div>
</div><div class="card"><form data-demo-form>
<label>Name * <input required name="name" placeholder="Your full name"></label>
<label>Email * <input required type="email" name="email" placeholder="you@example.com"></label>
<label>Company / brand <input name="company" placeholder="Optional"></label>
<label>Inquiry type * <select required name="type"><option>Branding</option><option>Graphic Design</option><option>Packaging</option><option>Campaign</option><option>Collaboration</option><option>Employment</option><option>Speaking</option><option>Other</option></select></label>
<label>Budget range (optional) <select name="budget"><option>Prefer not to say</option><option>Under $500</option><option>$500 – $1,500</option><option>$1,500 – $5,000</option><option>$5,000+</option></select></label>
<label>Timeline (optional) <input name="timeline" placeholder="e.g. Within 4 weeks"></label>
<label>Project details * <textarea required name="details" rows="5" placeholder="What do you need, and what does success look like?"></textarea></label>
<label><span><input type="checkbox" required style="width:auto"> I agree to my details being used to reply to this inquiry. See the <a href="privacy.html">privacy policy</a>.</span></label>
<button class="btn btn-lime" type="submit">Send Inquiry →</button>
</form><div class="form-ok"><b>Thank you — your message has been noted on this page.</b><br>Email delivery is not connected yet: it will send to Amad’s confirmed professional email once he supplies it (see README). For now, please also reach out on LinkedIn.</div></div>
</div></section>
"""
write("contact.html", page("Contact — Muhammad Amad",
    "Contact Muhammad Amad for branding, packaging, campaign design, collaboration or speaking inquiries.", "contact", contact))

# ---------------------------------------------------------------- CV
cv = """
<section class="light"><div class="wrap"><div class="cv-head">
<div><span class="eyebrow">CV / Resume</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Muhammad Amad</h2>
<p class="lead">Graphic Designer &amp; Creative Lead — brand identity, visual communication, and design education.</p></div>
<div class="no-print"><button class="btn btn-navy" onclick="window.print()">Print / Save as PDF ↓</button></div>
</div>
<div class="note" style="margin-top:20px"><b>Note:</b> this web CV follows the brief. Amad’s latest CV PDF will replace the print option once he supplies it — the button above saves this page as a PDF in the meantime.</div>
<div class="two" style="margin-top:32px"><div>
<h2>Experience</h2><div class="timeline">
<div><span class="when">Current</span><h3>Senior Graphic Designer — Markhor Group of Companies</h3><p>Brand and packaging design.</p></div>
<div><span class="when">Current</span><h3>Graphics Lead — TechKhwa (Remote)</h3><p>Graphics leadership and design education.</p></div>
<div><span class="when">Experience</span><h3>Graphic Design — approximately 4 years</h3><p>As stated in the brief, confirmed by Amad.</p></div>
</div>
<h2 style="margin-top:32px">Selected Work</h2>
<p>Markhor Cola · Markhor King · Markhor Energy Drink · Markhor Ginseng — see <a href="work.html">Work</a> for case studies.</p>
</div><div>
<h2>Education</h2><div class="timeline">
<div><span class="when">2021 – 2025</span><h3>BS Information Technology</h3><p>University of Agriculture Peshawar.</p></div>
<div><span class="when">Training</span><h3>Graphic Design &amp; UI/UX Design</h3><p>SMIT Peshawar — exact certificate names to be supplied by Amad.</p></div>
<div><span class="when">2022 – 2023</span><h3>Diploma in Graphic Design</h3><p>Saylani Welfare, Jan 2022 – Dec 2023 · Grade A.</p></div>
</div>
<h2 style="margin-top:32px">Skills &amp; Tools</h2>
<p>Brand identity · Graphic design · Packaging · Campaign visuals · Creative direction · Teaching &amp; mentoring</p>
<p>Adobe Photoshop · Adobe Illustrator</p>
<h2 style="margin-top:32px">Contact</h2>
<p><a href="https://www.linkedin.com/in/muhammad-amad7/" target="_blank" rel="noopener">LinkedIn — muhammad-amad7 ↗</a><br>Professional email — to be confirmed by Amad.</p>
<p style="color:var(--muted);font-size:14px">* Role wording, experience length and certificate names subject to Amad’s confirmation.</p>
</div></div></div></section>
"""
write("cv.html", page("CV — Muhammad Amad",
    "CV of Muhammad Amad: Senior Graphic Designer at Markhor Group, Graphics Lead at TechKhwa, BS IT 2021–2025.", "cv", cv))

# ---------------------------------------------------------------- LEGAL + 404
privacy = """
<section class="light"><div class="wrap" style="max-width:820px">
<span class="eyebrow">Legal</span><h2 style="margin-top:10px">Privacy Policy</h2>
<p>This website collects only what you submit through its forms: your name, email, and the details of your inquiry or course registration. That information is used only to reply to you and to manage your inquiry or registration.</p>
<p>Form submissions are not yet connected to an email provider — until Amad confirms his professional email and a delivery provider, submissions are only shown as a confirmation on this page and are not sent or stored. Once delivery is connected, this policy will be updated with the provider’s name and retention details.</p>
<p>No analytics, advertising trackers or newsletter signups run on this site at launch. No personal data is sold or shared. To ask for your submitted details to be removed, contact Amad via LinkedIn.</p>
<p><a href="contact.html">← Back to Contact</a></p></div></section>
"""
write("privacy.html", page("Privacy Policy — Muhammad Amad", "Privacy policy for muhammadamad — what the contact and registration forms collect and why.", "contact", privacy))

terms = """
<section class="light"><div class="wrap" style="max-width:820px">
<span class="eyebrow">Legal</span><h2 style="margin-top:10px">Terms</h2>
<p>Content on this site — including project names, case-study text and course information — belongs to Muhammad Amad unless otherwise credited. Do not reuse project artwork without permission.</p>
<p>Course information on the Academy page is provisional: course names, dates, fees and refund terms will be published only once confirmed. No payment is taken through this site at launch, and no place on a course is guaranteed by registering interest.</p>
<p>Project inquiries sent through the contact form are requests, not bookings. Any work, timeline or fee is agreed separately with Amad.</p>
<p><a href="contact.html">← Back to Contact</a></p></div></section>
"""
write("terms.html", page("Terms — Muhammad Amad", "Terms for Muhammad Amad’s website, courses and inquiries.", "contact", terms))

notfound = """
<section class="darksec"><div class="wrap" style="text-align:center;padding:60px 0">
<span class="eyebrow" style="justify-content:center">404</span>
<h2 style="font-size:clamp(40px,6vw,72px);margin-top:10px">This page went <em style="color:var(--lime);font-style:normal">off-brief.</em></h2>
<p class="lead">The page you’re looking for doesn’t exist — or it moved.</p>
<a class="btn btn-lime" href="index.html">Back Home →</a> <a class="btn btn-ghost" href="work.html">View Work</a>
</div></section>
"""
write("404.html", page("Page Not Found — Muhammad Amad", "The page you’re looking for doesn’t exist.", "home", notfound, dark_body=True))

# ---------------------------------------------------------------- STATIC FILES
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://amad-portfolio-psi.vercel.app/sitemap.xml\n", encoding="utf-8")
(ROOT / "sitemap.xml").write_text("""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
""" + "".join(f"  <url><loc>https://amad-portfolio-psi.vercel.app/{p}</loc></url>\n" for p in
["", "about.html", "work.html", "academy.html", "insights.html", "contact.html", "cv.html", "privacy.html", "terms.html",
 "tools/index.html", "tools/design-cost-estimator.html", "tools/label-size-finder.html", "tools/print-preflight-checker.html"]) + "</urlset>\n", encoding="utf-8")

(ROOT / "README.md").write_text("""# Muhammad Amad — Personal Portfolio

Agenz-inspired portfolio for Muhammad Amad (graphic designer & creative lead),
built from his 25-page brief (v1.0, 8 Nov 2026). Static site — no build step, no backend.

## Design
- **Agenz layout:** dark hero, huge display type, lime accents, marquee strip, big rounded
  work cards, services grid, process steps, big dark footer.
- **Colours (brief tokens):** dark `#111820`, navy `#142B4D`, lime accent `#B7FE5D`,
  light `#F5F6F3`, body `#26313D`, muted `#687482`.
- **Fonts:** Space Grotesk (display) + Inter (body), Google Fonts.
- **Footer:** the small **Built by AKCLNT** badge sits in the **middle column** of the
  footer on every page, linking to https://akclnt.com.

## Pages
`index` (hero, selected work, services, about preview, process, academy preview, contact CTA),
`about`, `work` (filterable: Brand Identity / Packaging / Campaigns),
`work/markhor-cola`, `work/markhor-king`, `work/markhor-energy-drink`, `work/markhor-ginseng`,
`academy` (interest registration only — no LMS/payments), `insights` (planned topics only),
`contact` (inquiry form), `cv` (web CV + print-to-PDF), `privacy`, `terms`, `404`.

## Motion (added 2026-11-10)
- Hero: headline words rise + rotate in one by one (staggered), drifting lime glow,
  scrolling marquee, floating portrait card with role chips.
- AnimMaster-style pack: magnetic buttons, cursor glow (desktop mouse only),
  3D tilt on work cards + portrait, nav-link roll, clip-path cover reveal,
  hero parallax, scroll-reveal everywhere. All vanilla CSS/JS, no dependency;
  `prefers-reduced-motion` disables it. NOTE: animmasterlib.dev is a PAID pack
  ($4.99 PRO / $8 Premium) — its code was NOT copied; these are original
  implementations of the same effect families. If the pack is ever bought, its
  real components can be integrated instead.
- Hero portrait slot: drop Amad's photo at `assets/img/portrait.jpg` and rebuild —
  build.py emits the real `<img>` when the file exists, otherwise the MA monogram.
- Services/footer pack (2026-11-10): What I Do cards get a mouse-spotlight glow,
  shine sweep and 3D tilt; scroll progress bar (lime, top); cursor ring on desktop;
  brands strip is a real slider (auto-scroll + drag to scrub); premium footer with
  link underline sweeps, hover-fill giant wordmark (links to Contact), AKCLNT badge
  shine, and a Back to top link. Footer badge stays in the middle column, one per page.
- Service icons + header (2026-11-10): each What I Do card has its own SVG icon
  (layers/pen/box/megaphone/compass/book); header gains a shadow once scrolled.
- Skiper-inspired pack (2026-11-10): Skiper UI is skiper-ui.com (NOT skipperui.com,
  which does not resolve) — React/Tailwind library, 106 components, 37 free, 69
  Premium ($129 one-time). Its code was NOT copied; original vanilla versions of
  the same families: hero canvas crowd (particles drift + follow the cursor),
  rolling-words hero line (Designing — Brand Identities/Packaging/...), rotating
  gradient border on service-card hover, scroll-with-blur section headings.
  VERIFICATION NOTE: plain headless --screenshot catches the ~1.2s hero entrance
  mid-flight (frozen half-risen words) — that is a screenshot-timing artifact, NOT
  a site bug. Verified via CDP after 7 real seconds: word transform is identity,
  hero-sub opacity 1, all 6 words + full headline present.

## Run locally / deploy
```bash
python3 build.py        # regenerate all HTML from build.py
python3 -m http.server 8000   # then open http://localhost:8000
```
Push the whole folder to the (empty) repo and deploy on Vercel as a static site —
this is the first live home (GitHub + Vercel). No custom domain yet: once everything
is done, shift it to Amad's own domain, then update `sitemap.xml` / `robots.txt`
with the live URL.

## What is NOT invented (per the brief)
No testimonials, metrics, awards, prices, dates or credentials were invented.
The brief governs all facts on the site — Amad confirmed the brief is correct
(Komil, 2026-11-10). Permission to publish the Markhor projects is already given.
- Placeholders kept for now: portrait photos, CV PDF, role/certificate confirmation.
- LinkedIn was also read (2026-11-10, after Komil signed in): it lists "Senior Designer"
  and a Saylani Diploma in Graphic Design (Jan 2022–Dec 2023, Grade A). Per Komil the
  brief wins for roles/experience wording; the Saylani diploma was ADDED to the site on
  his word (2026-11-10) — Home, About and CV. Tools are Photoshop and
  Illustrator only, per Komil's word — no InDesign, Figma or CapCut listed.
- Markhor project covers are CSS placeholders, not final artwork; final artwork and
  process images will replace them once Amad supplies them.
- No email / WhatsApp / Behance / Instagram / Pinterest is published — none was
  confirmed in the brief. Forms show a success state on-page only.

## Still needed from Amad (before launch)
1. Professional portrait (2–5 photos), short + full bio approval, latest CV PDF.
2. Role/certificate confirmation — placeholders kept for now (brief wording used).
   Personal palette vs TechKhwa colours — decision still open.
3. Final + process images for the Markhor projects (permission already given).
4. Course names, format, dates, fees, refund terms — or keep Academy as interest-only.
5. Professional email (to wire the contact + registration forms — Formspree/Resend),
   WhatsApp number if public, and confirmed social URLs.
6. Custom domain later — after the Vercel launch; then update sitemap.xml / robots.txt.
7. Approve the headline: “Designing identities. Building ideas. Empowering creatives.”

## SEO (done 2026-11-10)
- Person schema (JSON-LD) on every page; WebSite + FAQPage schema on the home page;
  WebApplication + FAQPage schema on each tool page.
- Unique title + meta description on every page; Open Graph image
  `assets/img/og-image.png` (1200×630, drawn, no photo); `robots.txt` + `sitemap.xml`
  (live domain `https://amad-portfolio-psi.vercel.app` since 2026-11-10;
  update again when Amad's custom domain connects).
- FAQ section on the home page; internal links: home → tools, tools → work/contact/academy.
- After the Vercel deploy: verify the live site in Google Search Console, submit the
  sitemap, and request indexing for the home page + the 3 tool pages.
- Honest note: a new site ranks on guides + tools together, not on a bare tool page —
  that is why every tool page carries a full guide (method, formula, example table, FAQ).

## Free tools (done 2026-11-10) — untapped angles only
Competition was checked first (2026-11-10). REJECTED as already taken by dedicated
sites — do not build these: generic label-size calculator (labelsize.com, boxnovo,
converterslab, label.com.pk), print bleed calculator (llion.net, printruler.com,
cityprintexpress.com), sticker-sheet layout calculator (printreadykit.com,
madegooddesigns.com), box dieline generator (dielinemaker.com, vorexpackaging.com),
freelance hourly-rate calculator Pakistan (ratekaropk.site, broi.store).
Built instead — the soft spots:
1. `tools/design-cost-estimator.html` — Logo & Brand Identity Cost Estimator, Pakistan
   (PKR). Interactive; guides exist but no interactive PKR estimator. Ranges grounded
   in published 2026 guides (GoDesign, PrimeMedia, LogicRacks, ICM) — shown on the page.
   Labelled "indicative market range, not a quote" with a CTA for Amad's exact quote.
2. `tools/label-size-finder.html` — Drinks Label Size Finder. Not a generic calculator:
   presets for drinks bottles/cans (250 ml slim can, 330 ml can, 500 ml bottle, 1 L,
   750 ml wine, 350 ml glass cola) + wrap/front modes + bleed + artwork size.
3. `tools/print-preflight-checker.html` — checks bleed, DPI, safe margin, colour mode,
   fonts and file format with pass/check/fix verdicts. No dedicated interactive tool found.
All three run 100% client-side (`assets/js/tools.js`, syntax-checked with node).
No sign-up, nothing uploaded. Each tool page has guide content + FAQ, per the SEO note above.

## Motion (added 2026-11-10 — hero felt static, marquee did not move, cards had no life)
- Hero: headline lines rise out of a mask one after another; eyebrow, sub, CTAs and
  pills fade up in sequence; slow lime glow drifts behind the headline.
- Marquee: now actually scrolls (26s loop; text duplicated for a seamless wrap).
- Scroll reveal: work cards, services, steps, courses, timeline, FAQ and tool panels
  fade up via IntersectionObserver in `assets/js/main.js` (class added by JS only,
  so no-JS never hides content). `prefers-reduced-motion` disables all motion.
- Cards: hover lift + lime border; work-cover artwork zooms slightly on hover.
- Hero portrait slot: the portrait card is a photo frame. Drop Amad's real photo at
  `assets/img/portrait.jpg` and rebuild — it replaces the MA monogram automatically
  (build.py checks for the file). Until then the monogram + floating role chips show.

## Editing content
Edit `build.py` (content + page templates) and re-run it — or edit the generated
`.html` files directly. Shared styles: `assets/css/style.css`. Shared behaviour:
`assets/js/main.js` (mobile nav, work filters, demo forms, scroll reveal).
Tool logic: `assets/js/tools.js` (estimator, label finder, preflight checker).
""", encoding="utf-8")
print("wrote robots.txt, sitemap.xml, README.md")
print("DONE")

# ---------------------------------------------------------------- FREE TOOLS
# Competition check (2026-11-10): generic label-size, bleed and sticker-sheet
# calculators are TAKEN by dedicated sites (labelsize.com, boxnovo, llion.net,
# printruler.com, printreadykit.com, dielinemaker.com, vorexpackaging.com).
# These three are the soft spots: a PKR design-cost estimator (guides exist,
# no interactive estimator), a drinks-preset label finder (not a generic
# calculator), and an interactive print preflight checker (no dedicated tool).

TOOLS_SCHEMA = lambda name, desc: f"""<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebApplication","name":"{name}","applicationCategory":"DesignApplication","operatingSystem":"Any","offers":{{"@type":"Offer","price":"0","priceCurrency":"PKR"}},"description":"{desc}"}}</script>"""

tools_index = """
<section class="light"><div class="wrap">
<span class="eyebrow">Free Tools</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Free tools for <em style="color:var(--lime-dark);font-style:normal">designers &amp; brands.</em></h2>
<p class="lead" style="max-width:680px">Three free tools from Muhammad Amad — a Peshawar-based graphic designer who makes brand identities and packaging every day. They run entirely in your browser: no sign-up, no account, nothing uploaded.</p>
<div class="course-grid" style="margin-top:32px">
<div class="course"><span class="status">Free · No sign-up</span><h3>Logo &amp; Brand Identity Cost Estimator</h3><p>What does a logo or a full brand identity cost in Pakistan? Indicative 2026 PKR ranges for freelancers and agencies.</p><p><a class="btn btn-navy" href="design-cost-estimator.html">Open Tool →</a></p></div>
<div class="course"><span class="status">Free · No sign-up</span><h3>Drinks Label Size Finder</h3><p>Pick your bottle or can — cola, energy drink, water, wine — and get the exact label and artwork size in mm and inches.</p><p><a class="btn btn-navy" href="label-size-finder.html">Open Tool →</a></p></div>
<div class="course"><span class="status">Free · No sign-up</span><h3>Print Preflight Checker</h3><p>Check bleed, resolution, safe margin, colour mode, fonts and file format before you send artwork to print.</p><p><a class="btn btn-navy" href="print-preflight-checker.html">Open Tool →</a></p></div>
</div>
<p style="color:var(--muted);margin-top:28px">Built by a working designer, for the jobs that come up every week: pricing a logo, sizing a drinks label, and catching a print mistake before it costs a reprint. Need the work done, not just the tool? <a href="../contact.html">Contact Muhammad Amad →</a></p>
</div></section>
"""
write("tools/index.html", toolpage("Free Design Tools — Muhammad Amad",
    "Free design tools by Muhammad Amad: logo & brand identity cost estimator Pakistan (PKR), drinks label size finder, and print preflight checker. No sign-up.",
    "tools", tools_index))

# --- Tool 1: cost estimator ---
EST_FAQ = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Is this Muhammad Amad's price?","acceptedAnswer":{"@type":"Answer","text":"No. This tool shows indicative 2026 market ranges from published Pakistan pricing guides. Your exact price comes as a written quote after a short brief — send an inquiry through the contact page."}},{"@type":"Question","name":"Why do logo prices vary so much in Pakistan?","acceptedAnswer":{"@type":"Answer","text":"Scope, concepts, revisions, deadline and who designs it. A freelancer logo with source files is typically PKR 10,000–60,000; an agency logo starts around PKR 40,000–80,000 and a full identity goes past PKR 300,000."}},{"@type":"Question","name":"What does a full brand identity include?","acceptedAnswer":{"@type":"Answer","text":"Usually a logo, colour system, typography, business card and stationery, social templates and brand guidelines — the full kit a business needs to look consistent everywhere."}}]}</script>"""
estimator = """
<section class="light"><div class="wrap">
<span class="eyebrow">Free Tool · No sign-up</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Logo &amp; Brand Identity Cost Estimator — <em style="color:var(--lime-dark);font-style:normal">Pakistan (PKR)</em></h2>
<p class="lead" style="max-width:680px">How much does a logo or a full brand identity cost in Pakistan? Pick what you need and who should design it — the estimator shows an indicative 2026 PKR market range. It is a guide, not a quote.</p>
<div class="tool-grid" style="margin-top:32px"><div class="tool-panel">
<h3>Your project</h3><form onsubmit="return false">
<label>What do you need?
<div class="chips" style="margin-top:8px">
<label class="chip"><input type="radio" name="est-service" value="logo" checked style="width:auto"> Logo only</label>
<label class="chip"><input type="radio" name="est-service" value="identity" style="width:auto"> Full brand identity</label>
</div></label>
<label>Who should design it?
<div class="chips" style="margin-top:8px">
<label class="chip"><input type="radio" name="est-who" value="freelancer" checked style="width:auto"> Freelancer</label>
<label class="chip"><input type="radio" name="est-who" value="agency" style="width:auto"> Agency / studio</label>
</div></label>
<div class="field-row">
<label>Logo concepts <select id="est-concepts"><option>2</option><option selected>3</option><option>5</option></select></label>
<label>Rush delivery? <select id="est-rush"><option value="">No — standard</option><option value="1">Yes — rush (+25%)</option></select></label>
</div>
<p style="font-size:13px;color:var(--muted)">Rush delivery adds 25% to the top of the range.</p>
</form></div>
<div class="result" id="est-result"><span class="eyebrow">Indicative market range</span>
<div class="big" id="est-range">PKR —</div>
<p class="fine" id="est-note"></p>
<p style="margin-top:20px"><a class="btn btn-lime" href="../contact.html">Get My Exact Quote →</a></p>
<p class="fine">Not a quote from Amad. Every project gets an exact written quote after a short brief.</p></div>
</div></div></section>
<section class="white"><div class="wrap" style="max-width:820px">
<h2>What the ranges are based on</h2>
<p>These are indicative 2026 ranges from published Pakistan pricing guides — not a survey, and not Amad’s price list. Final quotes always depend on scope, revisions and deadline.</p>
<table class="guide-table"><tr><th>Service</th><th>Freelancer (PKR)</th><th>Agency / studio (PKR)</th><th>Source</th></tr>
<tr><td>Logo only</td><td>10,000 – 60,000</td><td>40,000 – 150,000</td><td>GoDesign 2026 guide; LogicRacks Starter PKR 40,000; ICM logo PKR 80,360</td></tr>
<tr><td>Full brand identity</td><td>40,000 – 200,000</td><td>96,000 – 400,000</td><td>PrimeMedia 2026 guide; LogicRacks Pro PKR 96,000</td></tr></table>
<h2>Why prices vary</h2>
<p><b>Concepts:</b> two concepts cost less than five. <b>Revisions:</b> more rounds, more time. <b>Scope:</b> a logo alone is one deliverable; a full identity adds a colour system, typography, stationery, social templates and guidelines. <b>Deadline:</b> rush work costs more. <b>Who designs it:</b> a freelancer’s overhead is lower than a studio’s — but a studio brings a team and a process.</p>
<h2>Frequently asked questions</h2>
<details class="faq"><summary>Is this Muhammad Amad’s price?</summary><p>No. This tool shows indicative 2026 market ranges from published Pakistan pricing guides. Your exact price comes as a written quote after a short brief — send an inquiry through the contact page.</p></details>
<details class="faq"><summary>Why do logo prices vary so much in Pakistan?</summary><p>Scope, concepts, revisions, deadline and who designs it. A freelancer logo with source files is typically PKR 10,000–60,000; an agency logo starts around PKR 40,000–80,000 and a full identity goes past PKR 300,000.</p></details>
<details class="faq"><summary>What does a full brand identity include?</summary><p>Usually a logo, colour system, typography, business card and stationery, social templates and brand guidelines — the full kit a business needs to look consistent everywhere.</p></details>
<p><a href="index.html">← All free tools</a> · <a href="../contact.html">Get an exact quote →</a></p>
</div></section>
<script src="assets/js/tools.js"></script>
"""
write("tools/design-cost-estimator.html", toolpage("Logo & Brand Identity Cost Estimator Pakistan (PKR) — Free",
    "How much does a logo or brand identity cost in Pakistan? Free estimator with indicative 2026 PKR ranges for freelancers and agencies. No sign-up.",
    "tools", estimator, extra_head=TOOLS_SCHEMA("Logo & Brand Identity Cost Estimator Pakistan", "Free estimator: indicative 2026 PKR ranges for logo and brand identity design in Pakistan.") + EST_FAQ))

# --- Tool 2: drinks label size finder ---
LABEL_FAQ = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"How do I measure a bottle for a label?","acceptedAnswer":{"@type":"Answer","text":"Measure the straight section only — from where the shoulder starts to flatten to where the base begins to taper. Measure the diameter across the widest straight part, or wrap a strip of paper around it, mark where it meets, and measure it flat. Never measure the shoulder or the base curves: a flat label will not sit there."}},{"@type":"Question","name":"What is the label size formula?","acceptedAnswer":{"@type":"Answer","text":"Circumference = diameter × π (3.1416). A full wrap label is the circumference minus a small gap (3 mm), or plus an overlap for the seam. A front label is usually about 45% of the circumference. Add bleed — usually 3 mm on every side — to get the artwork size."}},{"@type":"Question","name":"Do I need bleed on a label?","acceptedAnswer":{"@type":"Answer","text":"Yes — 3 mm on every side is the standard. The artwork must extend past the cut line so the cutter's small drift never leaves a white edge."}}]}</script>"""
label_finder = """
<section class="light"><div class="wrap">
<span class="eyebrow">Free Tool · No sign-up</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Drinks Label Size <em style="color:var(--lime-dark);font-style:normal">Finder</em></h2>
<p class="lead" style="max-width:680px">What size label fits your bottle or can? Pick your drink below — cola, energy drink, water, wine — or type your own measurements. You get the label size and the print-ready artwork size in millimetres and inches.</p>
<div class="tool-grid" style="margin-top:32px"><div class="tool-panel">
<h3>Your container</h3>
<p style="font-size:14px;color:var(--muted)">Pick a drink — or type your own size. Presets are typical starting points; always measure your actual container.</p>
<div class="chips">
<button class="chip lb-preset active" data-preset="slim250">250 ml slim can</button>
<button class="chip lb-preset" data-preset="can330">330 ml can</button>
<button class="chip lb-preset" data-preset="bottle500">500 ml bottle</button>
<button class="chip lb-preset" data-preset="bottle1000">1 litre bottle</button>
<button class="chip lb-preset" data-preset="wine750">750 ml wine</button>
<button class="chip lb-preset" data-preset="cola350">350 ml glass cola</button>
</div>
<div class="field-row3">
<label>Diameter (mm) <input id="lb-dia" type="number" value="52" min="20" max="300"></label>
<label>Label height (mm) <input id="lb-height" type="number" value="120" min="10" max="400"></label>
<label>Bleed / edge (mm) <input id="lb-bleed" type="number" value="3" min="0" max="10"></label>
</div>
<label style="margin-top:14px">Label type
<div class="chips" style="margin-top:8px">
<label class="chip"><input type="radio" name="lb-mode" value="wrap" checked style="width:auto"> Full wrap (3 mm gap)</label>
<label class="chip"><input type="radio" name="lb-mode" value="overlap" style="width:auto"> Full wrap (overlap seam)</label>
<label class="chip"><input type="radio" name="lb-mode" value="front" style="width:auto"> Front label only</label>
</div></label>
</div>
<div class="result" id="lb-result"><span class="eyebrow">Your label size</span>
<table>
<tr><td>Circumference</td><td id="lb-circ">—</td></tr>
<tr><td>Label width</td><td id="lb-width">—</td></tr>
<tr><td>Label height</td><td id="lb-height-out">—</td></tr>
<tr><td>Artwork size (with bleed)</td><td id="lb-art">—</td></tr>
<tr><td>Label size in inches</td><td id="lb-inch">—</td></tr>
</table>
<p class="fine" id="lb-formula"></p>
<p style="margin-top:20px"><a class="btn btn-lime" href="../contact.html">Need This Label Designed? →</a></p></div>
</div></div></section>
<section class="white"><div class="wrap" style="max-width:820px">
<h2>How the size is worked out</h2>
<p>For a round bottle or can, the label width comes from the circumference — and the circumference comes from the diameter: <b>Circumference = Diameter × π (3.1416)</b>. A full wrap is the circumference minus a 3&nbsp;mm gap so the ends never collide, or plus a 6&nbsp;mm overlap if the seam should overlap itself. A front label is usually about 45% of the circumference. The label height is the usable straight height you measured. Add bleed to both sides of each dimension: a label with 3&nbsp;mm bleed needs 6&nbsp;mm extra in each direction for the artwork file.</p>
<h2>How to measure a bottle or jar</h2>
<p>Measure the straight section only — from where the shoulder starts to flatten to where the base begins to taper. Measure the diameter across the widest straight part, or wrap a strip of paper around the container, mark where it meets, and measure it flat. Never measure the shoulder or the base curves: a flat label will not sit there. A small gap (about 3&nbsp;mm) hides small measuring and application errors.</p>
<h2>Common drinks containers</h2>
<table class="guide-table"><tr><th>Container</th><th>Diameter</th><th>Typical label height</th><th>Full wrap width</th></tr>
<tr><td>250 ml slim can (energy drink)</td><td>52 mm</td><td>120 mm</td><td>160 mm</td></tr>
<tr><td>330 ml standard can</td><td>66 mm</td><td>100 mm</td><td>204 mm</td></tr>
<tr><td>500 ml water / cold-drink bottle</td><td>65 mm</td><td>110 mm</td><td>201 mm</td></tr>
<tr><td>1 litre bottle</td><td>85 mm</td><td>150 mm</td><td>264 mm</td></tr>
<tr><td>750 ml wine bottle (front label)</td><td>75 mm</td><td>100 mm</td><td>106 mm (front)</td></tr></table>
<p style="color:var(--muted);font-size:14px">Typical starting points only — containers vary between manufacturers, so always measure the actual bottle or can before printing.</p>
<h2>Frequently asked questions</h2>
<details class="faq"><summary>How do I measure a bottle for a label?</summary><p>Measure the straight section only — from where the shoulder starts to flatten to where the base begins to taper. Measure the diameter across the widest straight part, or wrap a strip of paper around it, mark where it meets, and measure it flat. Never measure the shoulder or the base curves: a flat label will not sit there.</p></details>
<details class="faq"><summary>What is the label size formula?</summary><p>Circumference = diameter × π (3.1416). A full wrap label is the circumference minus a small gap (3 mm), or plus an overlap for the seam. A front label is usually about 45% of the circumference. Add bleed — usually 3 mm on every side — to get the artwork size.</p></details>
<details class="faq"><summary>Do I need bleed on a label?</summary><p>Yes — 3 mm on every side is the standard. The artwork must extend past the cut line so the cutter’s small drift never leaves a white edge.</p></details>
<p><a href="index.html">← All free tools</a> · <a href="../work.html">See Amad’s label work →</a></p>
</div></section>
<script src="assets/js/tools.js"></script>
"""
write("tools/label-size-finder.html", toolpage("Drinks Label Size Finder — Bottle & Can Label Calculator (Free)",
    "What size label fits your bottle or can? Free finder for cola, energy drink, water and wine bottles: label size and print-ready artwork size in mm and inches.",
    "tools", label_finder, extra_head=TOOLS_SCHEMA("Drinks Label Size Finder", "Free label size finder for drinks bottles and cans: wrap and front label sizes with bleed, in mm and inches.") + LABEL_FAQ))

# --- Tool 3: print preflight checker ---
PRE_FAQ = """<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"What is print bleed?","acceptedAnswer":{"@type":"Answer","text":"Bleed is artwork extended past the trim line — usually 3 mm on every side — so the cutter's small drift never leaves a white edge. Without bleed, a tiny cutting shift shows as an unprinted sliver."}},{"@type":"Question","name":"What resolution do I need for print?","acceptedAnswer":{"@type":"Answer","text":"300 DPI at the finished size for anything held in the hand — business cards, flyers, labels, packaging. Large-format work viewed from a distance can use less."}},{"@type":"Question","name":"Should my print file be CMYK or RGB?","acceptedAnswer":{"@type":"Answer","text":"CMYK. RGB is a screen colour mode; printers print in CMYK, and converting at the last minute shifts colours. Design in CMYK from the start for print work."}}]}</script>"""
preflight = """
<section class="light"><div class="wrap">
<span class="eyebrow">Free Tool · No sign-up</span><h2 style="font-size:clamp(34px,5vw,56px);margin-top:10px">Print Preflight <em style="color:var(--lime-dark);font-style:normal">Checker</em></h2>
<p class="lead" style="max-width:680px">About to send artwork to print? Check bleed, resolution, safe margin, colour mode, fonts and file format first — and fix what fails before you pay for a reprint.</p>
<div class="tool-grid" style="margin-top:32px"><div class="tool-panel">
<h3>Your artwork</h3>
<div class="field-row3">
<label>Bleed / edge (mm) <input id="pf-bleed" type="number" value="3" min="0" max="10" step="0.5"></label>
<label>Resolution (DPI) <input id="pf-dpi" type="number" value="300" min="72" max="1200" step="1"></label>
<label>Safe margin (mm) <input id="pf-safe" type="number" value="5" min="0" max="20" step="0.5"></label>
</div>
<div class="field-row3" style="margin-top:14px">
<label>Colour mode <select id="pf-color"><option value="cmyk">CMYK</option><option value="rgb">RGB</option></select></label>
<label>Fonts <select id="pf-fonts"><option value="outlined">Outlined / converted to curves</option><option value="embedded">Embedded in the PDF</option><option value="missing">Not embedded</option></select></label>
<label>File format <select id="pf-format"><option value="pdfx">PDF/X (print-ready)</option><option value="pdf">Plain PDF</option><option value="image">JPG / PNG</option></select></label>
</div>
<p style="font-size:13px;color:var(--muted);margin-top:14px">Standards used: bleed 3 mm, resolution 300 DPI, safe margin 3 mm, CMYK, fonts outlined, PDF/X. Your printer’s spec sheet always wins over this checker.</p>
</div>
<div class="result"><span class="eyebrow">Preflight result</span>
<div class="big" id="pf-score">—</div>
<div id="pf-list" style="margin-top:8px"></div>
<p style="margin-top:20px"><a class="btn btn-lime" href="../contact.html">Get Print-Ready Design →</a></p>
<p class="fine">This checker does arithmetic on the numbers you enter. It does not open or inspect your file — always ask your printer for a proof before a big run.</p></div>
</div></div></section>
<section class="white"><div class="wrap" style="max-width:820px">
<h2>What each check means</h2>
<table class="guide-table"><tr><th>Check</th><th>Standard</th><th>Why it matters</th></tr>
<tr><td>Bleed</td><td>3 mm per edge</td><td>Cutting drifts by about a millimetre. Without bleed, that drift shows as a white edge.</td></tr>
<tr><td>Resolution</td><td>300 DPI at finished size</td><td>Below 150 DPI, print looks blurry. 150–299 DPI is a risk for anything held in the hand.</td></tr>
<tr><td>Safe margin</td><td>3 mm inside the trim</td><td>Text closer than 3 mm to the edge can get clipped — and looks cramped even on a good cut.</td></tr>
<tr><td>Colour mode</td><td>CMYK</td><td>Printers print CMYK. RGB files get converted late, and colours shift.</td></tr>
<tr><td>Fonts</td><td>Outlined or embedded</td><td>If the printer’s computer lacks your font, it substitutes another one and your layout breaks.</td></tr>
<tr><td>File format</td><td>PDF/X</td><td>The print-ready standard: text stays sharp and print settings travel with the file.</td></tr></table>
<h2>Frequently asked questions</h2>
<details class="faq"><summary>What is print bleed?</summary><p>Bleed is artwork extended past the trim line — usually 3 mm on every side — so the cutter’s small drift never leaves a white edge. Without bleed, a tiny cutting shift shows as an unprinted sliver.</p></details>
<details class="faq"><summary>What resolution do I need for print?</summary><p>300 DPI at the finished size for anything held in the hand — business cards, flyers, labels, packaging. Large-format work viewed from a distance can use less.</p></details>
<details class="faq"><summary>Should my print file be CMYK or RGB?</summary><p>CMYK. RGB is a screen colour mode; printers print in CMYK, and converting at the last minute shifts colours. Design in CMYK from the start for print work.</p></details>
<p><a href="index.html">← All free tools</a> · <a href="../academy.html">Learn design with Amad →</a></p>
</div></section>
<script src="assets/js/tools.js"></script>
"""
write("tools/print-preflight-checker.html", toolpage("Print Preflight Checker — Bleed, DPI, CMYK & Fonts (Free)",
    "Free print preflight checker: check bleed, resolution, safe margin, colour mode, fonts and file format before sending artwork to print. No sign-up.",
    "tools", preflight, extra_head=TOOLS_SCHEMA("Print Preflight Checker", "Free preflight checker for print artwork: bleed, DPI, safe margin, CMYK, fonts and file format.") + PRE_FAQ))
