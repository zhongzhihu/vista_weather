# Vista Weather — Landing Page (Astro)

Static landing page for **Vista Weather**, built with [Astro](https://astro.build).
Ships as pure HTML/CSS with effectively zero client-side JavaScript — perfect for SEO and fast loads.

---

## Quick start

```bash
# 1. Install dependencies (one-time)
npm install

# 2. Run the dev server
npm run dev
```

Open the URL it prints (typically `http://localhost:4321`).

To produce the production build:

```bash
npm run build      # writes static HTML/CSS/JS into ./dist
npm run preview    # serves ./dist locally to test
```

The `dist/` folder is what you deploy.

---

## Deploying

Drop `dist/` on any static host. The easiest options:

- **Netlify** — drag-and-drop `dist/` at [app.netlify.com/drop](https://app.netlify.com/drop), or connect your Git repo
- **Vercel** — `vercel deploy` from this folder, or connect your Git repo
- **Cloudflare Pages** — connect your Git repo, build command `npm run build`, output dir `dist`
- **GitHub Pages** — push `dist/` to a `gh-pages` branch

All three free tiers are more than enough for a launch page.

---

## Project structure

```
astro/
├── public/              static assets served as-is (favicon, /robots.txt, /og.png)
├── src/
│   ├── components/      reusable pieces: Phone, Nav, StoreBadge, etc.
│   ├── data/
│   │   └── cities.ts    the cities + photo URLs + forecast data
│   ├── layouts/
│   │   └── Layout.astro the <head> + global wrapper
│   ├── pages/
│   │   └── index.astro  the landing page itself
│   └── styles/
│       └── global.css   tokens, type, base styles
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

---

## Editing tips

- **Headline / copy** → `src/pages/index.astro`
- **City photos** → `src/data/cities.ts` (currently hot-linked from Unsplash; for production
  you'll want to host them yourself — drop the images in `public/cities/` and update the
  `photo` field to `/cities/sf.jpg`, etc.)
- **Colors / fonts** → CSS custom properties at the top of `src/styles/global.css`
- **Add a new page** (e.g. `/privacy`) → create `src/pages/privacy.astro`

---

## SEO checklist (already in place)

- ✅ Semantic HTML, content rendered server-side
- ✅ `<title>` and `<meta name="description">`
- ✅ Open Graph (`og:title`, `og:description`, `og:image`) for link previews
- ✅ Twitter Card meta
- ✅ `<link rel="canonical">`
- ⏳ Replace placeholder `og:image` in `public/og.png` with a real preview render
- ⏳ Add real domain to `site:` in `astro.config.mjs`
- ⏳ Add `public/robots.txt` and `public/sitemap.xml` (Astro can auto-generate the sitemap
  with `@astrojs/sitemap` integration when ready)

---

## Adding the waitlist backend

The form currently has no backend. Easy options:

- **Formspree** — replace the `<form>`'s `action` with your Formspree endpoint, done
- **Netlify Forms** — add `data-netlify="true"` to the `<form>` and Netlify handles the rest
- **Resend / Mailchimp / ConvertKit** — hook up via their JS embed

---

Built in Astro 4 · No tracking · No analytics by default
