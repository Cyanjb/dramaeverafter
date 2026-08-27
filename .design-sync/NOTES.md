# design-sync notes — DramaEverAfter

- **Review gate (Cyan's rule, kept for future syncs): nothing uploads until she has reviewed the local `.review.html` and signed off.** First sync: she approved on 27 Aug 2026 and all 40 components shipped that day. Treat every re-sync the same — build, verify, serve the review page, wait for her yes.
- This repo is a static Python-generated site, not a JS design system. The `design-system/` package was authored for the sync: thin React wrappers emitting the site's exact class names; `scripts/build-styles.mjs` re-copies the root `style.css` into `dist/styles.css` on every build so the CSS can never go stale. The site stylesheet is the source of truth — never restyle components inside the package.
- Build: `cd design-system && npm run build` (tsc + style copy), then the converter with `--entry ./design-system/dist/index.js`.
- Fonts (Fraunces, Atkinson Hyperlegible) load via a Google Fonts remote `@import` prepended in `dist/styles.css` — `[FONT_REMOTE]` on validate is expected, not a gap.
- Poster images: previews deliberately use the blush `poster--empty` fallback (a designed state on the site) instead of remote CDN poster URLs — deterministic renders, no external fetches.
- **Site quirk found during preview grading**: `.actor-tile`/`.person-row` name + sub are inline spans with no whitespace between them; they only look stacked on the live site because narrow tiles force a line wrap. Short names (e.g. "Meg Bush" + "21 titles") likely run together on the live site. The DS components set `display:block` on `.name`/`.sub` inline to make the intended stacking explicit — surfaced to Cyan 25 Aug 2026.

- **Contrast fixes applied 27 Aug 2026 (site + kit, Cyan-approved)**: `--tert` #8A7A70 → #7D6C64 (4.69:1 on paper); chip counts, trope-index counts, and watch disclosure moved from `--ph` to `--tert`; `.fav-btn` got a 44px touch target via `::after{inset:-6px}`. `--ph` is now placeholder-only — keep informational text off it.

## Known render warns
- (none recorded yet)

## Re-sync risks
- `design-system/` exists solely for this sync; if the site's markup patterns change (build.py templates), the wrappers must be updated by hand — nothing diffs site HTML against the components.
- Preview content (titles, actor names, counts) is real site data frozen in August 2026; it will drift from the live database but that's cosmetic.
