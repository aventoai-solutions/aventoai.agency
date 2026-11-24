# Avento AI — aventoai.agency

The company website of Avento AI Solutions (Dubai, UAE). Plain static HTML, no build step:
Vercel serves this folder as it is.

- `index.html` — Home (written by hand)
- `services/`, `work/`, `about/`, `privacy/`, `terms/` — built by `python tools/pages.py`,
  which copies the Home page's header and footer into each page. Edit the page bodies in
  `tools/pages.py`, run it, then commit.
- `assets/` — the design system: layout, motion, cards, diagrams, scroll moments, the hero's
  shader ground and the real tool icons. `assets/site.css` holds the page transitions.
- `images/` — the logo and screenshots of the live projects.

Preview locally:

```
python -m http.server 5173
```

then open http://localhost:5173.
