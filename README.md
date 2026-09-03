# DramaEverAfter

The cross-platform vertical drama database. This repo is the single source of truth: the data, the generator, and the published site all live here.

## Layout
- **/data/** — the database. Ten CSVs (titles, people, platforms, availability, credits, tropes, match_queue, snapshots, harvest_queue, popular_actors). Schema documented in Craft doc "3. Data Schema" plus v2 deltas in doc "7. Technical Architecture".
- **/generator/** — build.py reads /data and writes the generated site to the repo root. Run: `cd generator && python3 build.py`
- **Repo root** — the generated site (actors/, titles/, tropes/, where-to-watch/, apps/, index.html, 404.html, sitemap.xml, style.css, robots.txt, platforms.html). Netlify publishes the repo root. Never edit these by hand; the generator overwrites them on every build (style.css included: its source is the CSS block inside build.py). Only data/ and generator/ are hand-editable.
- **Hand-maintained root files the build never touches**: `_redirects`, `_headers`, `favicon.svg`, `apple-touch-icon.png`, `share.png` (the default social preview card; replace it with a designed one any time, same filename and 1200x630).

## Update runbook (for Claude sessions)
1. PULL this repo's current state from GitHub (raw files, public repo)
2. SCRAPE platform catalogs via web fetch (per-platform adapters in the dramaeverafter-pipeline skill)
3. MERGE into /data CSVs: exact platform+title matches update last_checked and view_count; new titles enter as needs_check; fuzzy matches go to match_queue.csv, never auto-merged
4. GENERATE: run build.py
5. HANDOFF: give Cyan the changed files plus a change report

## Update workflow (for Cyan)
Sessions with the repo attached commit and push to main directly; push is publish (Netlify auto-deploys in about 15 seconds). The older route still works: drag the files Claude hands over into the matching folders on github.com and commit.

## Rules
- Slugs never change once published (URLs are permanent)
- Trope/platform combo pages publish only at 5+ verified titles
- One canonical page per title; alt titles live in the alt_titles column, never as separate pages
