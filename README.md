# Muhammad Amad — Personal Portfolio

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
