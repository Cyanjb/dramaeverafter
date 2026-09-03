# DramaEverAfter

The cross-platform vertical drama database. This repo is the single source of truth: the data, the generator, and the published site all live here.

## Layout
- **/data/** — the database. Ten CSVs (titles, people, platforms, availability, credits, tropes, match_queue, snapshots, harvest_queue, popular_actors). Schema documented in Craft doc "3. Data Schema" plus v2 deltas in doc "7. Technical Architecture".
- **/generator/** — build.py reads /data and writes the generated site to the repo root. Run: `cd generator && python3 build.py`
- **/generator/staging/** — dated records of every scrape and import. A staging file is a record, not a queue.
- **/.github/workflows/** — the unattended jobs. `weekly-scrape.yml` is the database refresh; `fetch-synopses.yml` banks platform synopses for the caption pipeline.
- **Repo root** — the generated site (actors/, titles/, tropes/, where-to-watch/, apps/, index.html, 404.html, sitemap.xml, style.css, robots.txt, platforms.html). Netlify publishes the repo root. Never edit these by hand; the generator overwrites them on every build (style.css included: its source is the CSS block inside build.py). Only data/ and generator/ are hand-editable.
- **Hand-maintained root files the build never touches**: `_redirects`, `_headers`, `favicon.svg`, `apple-touch-icon.png`, `share.png` (the default social preview card; replace it with a designed one any time, same filename and 1200x630).

## The weekly update runs itself
Every Sunday at 12:00 UTC (14:00 Johannesburg) the `Weekly scrape` workflow runs on a GitHub runner, because the cloud Claude sandbox cannot reach any platform and GitHub's runners can:
1. SCRAPE: `generator/scrape_reelshort.py` reads ReelShort (actor tag pages, homepage rails, the fandom blog, title pages) into `generator/staging/reelshort_<date>.json`
2. MERGE: `generator/merge_scrape.py` applies the database rules: exact matches refresh view counts, dates and snapshots; new titles enter as needs_check only when ReelShort is featuring them or an actor we track is in them; near-matches go to match_queue.csv for Cyan, never auto-merged; delisted titles are reported, never deleted
3. GENERATE: `build.py`
4. PUSH to main. Push is publish: Netlify deploys in about 20 seconds
5. The change report (refreshed, new, held, delisted, credits) is on the run page under Actions

Two things the run cannot do by itself, and Cyan wants remembered (3 Sep 2026):
- **New titles need captions.** They go live as needs_check with no synopsis, because platform text is never copied. The synopsis each page published is banked in the staging JSON and `caption_pipeline.py` reads it as the fact source, so `next` picks the new titles up by reach. Write them with the dea-captions skill and put them through Cyan's review.
- **New releases update from the scrape.** The homepage rail leads with titles first seen by a weekly run in the last 90 days (the `source` column carries the run date), newest first, then falls back to the year ordering.

To get a specific title in, add its ReelShort URL to `generator/staging/reelshort_wanted.txt`; the next run creates it. The same file carries Cyan's AI rulings (`<url or slug> ai=yes`), which the merge writes into the ai column; that column is set by hand only and this file is the hand. ReelShort's genre tag pages are swept too (`generator/staging/reelshort_tags.txt`), and a title seen only there is created above 10M views, otherwise counted and left.

Run it by hand from Actions any time (`dry_run` to test without committing, `limit` for a quick probe). Other platforms are added by writing a `scrape_<platform>.py` that emits the same staging shape; see `references/adapters.md` section 27.

## Update runbook (for Claude sessions, ad hoc work)
1. PULL this repo's current state from GitHub
2. SCRAPE what the weekly job does not cover (other platforms, screenshot intake) per `references/adapters.md`, in a session that can reach the platform
3. MERGE into /data CSVs under the same rules as merge_scrape.py: exact matches update last_checked and view_count; new titles enter as needs_check; fuzzy matches go to match_queue.csv, never auto-merged
4. GENERATE: run build.py
5. Commit and push to main; verify the live URL with curl

## Rules
- Slugs never change once published (URLs are permanent)
- Trope/platform combo pages publish only at 5+ verified titles
- One canonical page per title; alt titles live in the alt_titles column, never as separate pages
- New titles are chosen, not swept: newest, most popular, or credited to an actor we track
- match_queue rulings are Cyan's; nothing merges without one
