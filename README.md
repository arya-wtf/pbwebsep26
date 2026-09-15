# arya.wtf

Personal site. Astro (static) → Cloudflare Workers static assets.

## Run

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # → dist/
npm run deploy     # astro build && wrangler deploy  (needs `wrangler login` once)
```

Point `arya.wtf` at the Worker in the Cloudflare dashboard (Workers → arya-wtf → Settings → Domains & Routes).

## Write an entry

Add `src/content/log/<slug>.md`. The eight fields live in frontmatter; the body is the argument. `draft: true` builds the page
(so you can preview it) but marks it `noindex`, keeps it out of the RSS feed and out of the ItemList. Filename = URL.

```yaml
---
title: …
summary: …            # one sentence; used on the index, the home page and RSS
date: 2026-09-22
revised: 2026-10-01   # optional
verdict: automate | assist | leave
source: Client · logistics
draft: false
fields:
  work: …
  before: …           # the figure before — no number, no entry
  verdict: …
  refused: …          # what you refused to automate — none named, entry unfinished
  result: …
  uncomfortable: …
  tools: …
---
```

## Where things are

- `src/lib/site.ts` — the identity string, nav, shared JSON-LD (`Person`, `Organization`, `WebSite`). Change the descriptor here and it changes everywhere.
- `src/lib/work.ts` — the work list (temporary; revise freely).
- `src/styles/global.css` — the whole design system as tokens. No literal colours in components.
- `public/img/` — hero + five plates (WebP), OG image. Regenerate with the prompts in `IMAGES.md`.
- `public/llms.txt`, `public/robots.txt`, `public/_headers` — machine-facing files. Sitemap is generated at `/sitemap-index.xml`.

## SEO / GEO / AIO checklist (what the build already does)

- One `h1` per page; headings phrased as the question the page answers.
- Canonical, OG, description, `theme-color` on every page.
- JSON-LD `@graph` on every page with a stable `Person @id`; `ProfilePage`, `Article`, `Service` + `Offer` (IDR), `FAQPage`, `CollectionPage` + `ItemList` per page type.
- `dateModified` on anything that changes; RSS at `/log/rss.xml`; `llms.txt`; sitemap.
- Zero client-side JavaScript. Fonts self-hosted. Images sized, lazy below the fold, with real alt text.
