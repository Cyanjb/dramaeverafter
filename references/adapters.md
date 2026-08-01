# DramaEverAfter source adapters
Last verified: 2026-07-17. Sites change; verify structure on first fetch each session.

## 1. ReelShort actor/actress tag pages
- URL: `https://www.reelshort.com/tags/movie-actors/{slug}-movies-{id}` (or movie-actresses)
- Reachable from bash with a desktop User-Agent (contrary to older skill note).
- Data: embedded `__NEXT_DATA__` JSON at `props.pageProps.tagBooks`.
  - `books[]`: book_title, read_count (views), chapter_count (episodes), special_desc (synopsis), book_id
  - `total_items`, `page`, `page_size` (10). Pagination: append `/2`, `/3`... (NOT ?page=)
  - Map book_id to slug via hrefs: `/movie/{slug}-{24-hex-id}`
- Feeds: people, titles, availability, credits (role=actor), snapshots.

## 2. ReelShort movie detail pages
- URL: `https://www.reelshort.com/movie/{slug}-{id}`
- `__NEXT_DATA__` contains a book object (hunt for dict with book_title + read_count).
- chapter_count often absent on detail pages; leave episode_count blank rather than 0.
- 404 = delisted title. Do not add; log for review.

## 3. ReelShort fandom blog (WordPress, open REST API) — richest source
- Base: `https://www.reelshort.com/fandom/wp-json/wp/v2/posts`
- Params: `?categories={id}&per_page=100&page={n}&_fields=id,title,link,content`
- Categories (2026-07-17): 3 = Movie Cast List (1,543), 1 = General Topic (1,130),
  4 = Top Movie Stories (343), 5 = Movie Streaming Guide (52).
- Cast extraction patterns (use ONLY these; prose "played by" captures junk):
  - h2/h3 headings: `Actor Name as Character Name`
  - Inline: `Character Name (Actor: Actor Name)` / `(Actress: ...)`
  - Validate actor names: 2-4 capitalized words, reject pronoun/article starts.
- Drama identity: most-frequent `/movie/{slug}-{id}` link in the article, never the headline text.
- Bios: sentences containing the actor's full name plus a career keyword
  (actor, known for, starred, born, based, trained...). Skip character-description sentences.
- Socials: NOT present in fandom articles as of 2026-07-17. Needs another source.
- Streaming guides mention platforms rhetorically ("Is X on Netflix?"); a mention is NOT
  availability. Only "official full episodes on YouTube" claims are worth a review flag.

## 4. Blocked or rejected sources (tested 2026-07-17)
- Reddit: 403 from bash (old. and www.). Reachable via Claude's web search/fetch tools only.
- fandom.com wikis: 403 from bash; ReelShort runs its own fandom section anyway (see 3).
- IMDb: bot-blocked from bash AND from the fetch tool (403 as of 2026-08-01 - the fetch route
  used to work, it no longer does). Only web SEARCH reaches it. That is still enough: search
  results surface imdb.com/title/ttXXX/characters/nmXXX/ URLs, which are IMDb asserting that a
  named person played a named role - the strongest cheap evidence available for a credit.
- Dailymotion: reachable, public API at api.dailymotion.com, but content is pirated
  re-uploads with junk metadata. NEVER link or ingest. Off-brand for a where-to-watch site.
- TikTok: serves stub pages to bash. /discover/ pages surface via web search and can
  reveal actor handles for the socials column; manual/per-actor only.

## Screenshot intake (Reddit/Facebook identification threads)
- Cyan drops a screenshot; read title guesses and actor names from the thread text.
- Anything ambiguous goes to match_queue.csv with the screenshot description as evidence.
- Never auto-merge a fan identification; needs_check until Cyan confirms.

## Merge policy reminders (see data/CONVENTIONS.md)
- Match key: platform_id + title_as_listed (case-insensitive). Slug near-match check:
  compare with all hyphens removed before creating any new title row.
- Fill blanks only; never overwrite non-blank fields without logging a conflict.
- Near-identical actor names (blog typos are common): hold the rarer spelling out of
  people.csv, log to match_queue. Slugs are permanent; a wrong actor page is worse
  than a one-run delay.

## 5. My Drama (Holywater) — full catalog adapter (added 2026-07-17)
- Sitemap: `https://my-drama.com/sitemap.xml` -> ~187 `/series/{slug}-{uuid}` URLs. Reachable from bash with desktop UA.
- Data: Next.js streamed payload (`self.__next_f.push` chunks; join, unicode-unescape).
  `"seriesData":{...}` block has: name, slug, description, totalEpisodes, cast (camelCase keys), likes, rating, langs, coverUrl.
- Cast display names: regex `"name":"X","url":"https://my-drama.com/actors/{key}"` pairs in the same payload (from embedded structured data). Actor pages exist at /actors/{key} — unharvested; likely bios/photos for a future run.
- No view counts (likes + rating instead) -> no snapshots rows; view_count left blank.
- My Drama is originals-only: same title text as another platform almost certainly means a DIFFERENT production. Never auto-merge cross-platform title matches; match_queue them.
- ~50 of 173 credited actors overlap the ReelShort roster (US-based Holywater productions); the rest are largely Ukrainian cast (Kyiv productions).

## 6. Platform reachability probe (2026-07-17, from bash, desktop UA)
- OPEN: netshort.com (200, server-rendered /drama/ links + /all-episodes), goodshort.com (200, hydration JSON), vigloo.com (200, sitemaps at /sitemaps/index.xml incl. sitemap-content-en-*.xml), my-drama.com (200 + sitemap).
- BLOCKED: dramabox.com (403 bash; homepage only via fetch tool, /browse and dramaboxdb.com bot-walled), shortmax.com (503), playlet.com (503), anyreel.com (503), stardusttv.com (403), kalostv.com (200 but 3KB JS stub).
- Next adapter candidates in order: vigloo (sitemap = easy), netshort (server-rendered), goodshort (hydration parse).

## 7. CandyJar (Inkitt/Galatea) — full catalog adapter (added 2026-07-17)
- Homepage `https://www.candyjar.com` (bash OK, desktop UA) embeds the FULL catalog in Next.js
  `self.__next_f.push` chunks: 90 unique series (261 rail appearances — dedupe by id).
  Fields per series: id, title, coverUrl, summary. NO episodeCount in rails.
- Sitemaps: robots at candyjar.com (non-www) -> /en/sitemap.xml lists /series/{kebab-title}-{id}.
- Episode counts: fetch each series page, count distinct `"episodeNumber":N` in the payload.
- NO cast data on CandyJar's own site (confirmed; reviews note "actor search limitations"). CORRECTION 2026-07-24:
  cast data DOES exist off-platform for high-profile CandyJar titles via entertainment press (Yahoo, Primetimer,
  celebethnicity-style bio sites) covering viral actors — e.g. Nick Skonberg's full cast on Loving My Brother's
  Best Friend was sourced this way. All 90 CandyJar titles still have zero credits as of this date; this is a
  real, sizeable gap (not "no data exists", just "not on the platform itself") worth a dedicated press-sourced
  cast pass, prioritized by which titles/actors went viral rather than working the full 90 blind.
- Galatea originals (book adaptations): same-name matches on other platforms are DIFFERENT productions; match_queue them.

## 8. Big-platform status (checked 2026-07-17)
- DramaBox: comprehensively bot-walled. Main site, /browse, dramaboxdb.com, and all three official
  mirrors (dramaboxapp.com, dramaboxen.com, dramaboxtv.com) return 403 from bash; fetch tool also
  blocked on everything except the bare homepage. No bulk route. Per-title data only via web
  search snippets. Revisit occasionally; walls change.
- DramaWave: PARTIALLY CORRECTED 2026-08-01. dramawave.com/.tv/.app are indeed dead, but
  `mydramawave.com` is live (HTTP 200, robots.txt allows all) and there IS an API host at
  `api.mydramawave.com`. Found via the app's YouTube channel, @dramawaveapp.
  BUT: mydramawave.com is a client-rendered SPA - /sitemap.xml returns the same HTML shell as
  the homepage, and the page contains zero occurrences of "actor", "cast" or "episode". The
  main JS bundle (static-v1.mydramawave.com/frontend_static/assets/index-*.js, ~229KB) names
  the API host but its drama endpoints are code-split into lazily-loaded chunks; the only
  paths recoverable from the main bundle are novel-section ones (/novel-search, /novel/my-list).
  So an adapter is POSSIBLE but needs endpoint discovery (watch network traffic in a browser),
  which was not done.
  PRIORITY: LOW for now. We hold exactly 1 DramaWave title, and the catalogue is 30K+ mostly
  translated Chinese content — low fit for the English-actor-centric DB. This becomes
  interesting if/when the /chinese/ section is populated (see sec 11), not before.
- Shortical (a.k.a. "Shorticles"): app-only, no web catalog; small operator (Short Entertainment LTD),
  rough user reviews. Low priority.
- GoodShort: OPEN from bash. Server-rendered: /channel/ x8 (browse rails), /drama/ title pages,
  /tag/ x231 on homepage (includes actor-style tags — same shape as ReelShort). No /sitemap.xml (404).
  Enumerate via channels + tags. STRONGEST next adapter among the "big" apps.
- DramaReels (Jan 2026 #1 by downloads): dramareels.app serves 200 (76KB) — unexplored, probe next run.

## 9. GoodShort (Singapore New Reading Tech) — full catalog adapter (added 2026-07-17)
- No sitemap (404). Enumerate via `https://www.goodshort.com/dramas/playlets?page=1..187`
  -> ~1853 unique `/drama/{slug}-{numericid}` URLs. Reachable from bash, desktop UA.
- Per drama page: TVSeries JSON-LD block has name, description, numberOfEpisodes, genre, dateCreated (year).
  Views: HTML `Views</p><p ...>375.2K</p>` (already K/M format -> snapshots directly).
  Tropes: `/tag/{trope}-playlets-videos` hrefs on the page. Admit a tag to trope vocab only when it
  appears on >=3 titles (filters junk); recompute tropes.csv title_count after.
- NO cast/actor data on drama pages. Titles + availability + tropes + views only.
- Translated novel adaptations -> same-name matches usually DIFFERENT productions; new collisions go to
  match_queue (9 held this run). Per 2026-07-18 policy: compare, don't blanket-hold.
- Result 2026-07-17: 1828 new titles, 1828 availability rows, 1816 snapshots, 97 new tropes, 9 held.

## 9. NetShort — full-catalog adapter (added 2026-07-24)
- Domain: netshort.com (NO www — www 301s via Cloudflare; bash OK with desktop UA).
- Sitemap index: /sitemap_netshortcom.xml -> site_play_1.xml .. site_play_17.xml (15K URLs each,
  17th partial; 18+ empty). ~244.5K entries total, refreshed daily.
- Video sitemap format: each <url> has <loc> (/episode/{kebab-title}-{19-digit-id}),
  <video:title>, <video:description>, <video:thumbnail_loc>. Title+synopsis+cover come FREE
  from the sitemap — no per-page fetching needed for catalog matching.
- EP-collapse rule: entries are per-episode for some series ("Title - EP N"); strip
  /\s*[-–]\s*EP\s*\d+\s*$/i to collapse to series level. 244.5K entries -> ~69.9K unique series.
- Per-title detail: episode page embeds JSON-LD (script#json-ld) with @type TVSeries:
  name, description, genre[], numberOfEpisodes, image, canonical /full-episodes/ URL.
- NO cast data anywhere on web (confirmed — "cast" hits were the word "Outcast").
- NO view counts on web. Popularity signal = homepage trending rails (~54 curated titles).
- robots.txt: Crawl-delay 1; python-requests/Scrapy/wget UAs banned — always use browser UA.
- Strategy (ruled 2026-07-24): NEVER bulk-import the 69.9K tail. (1) cross-match sitemap vs
  existing titles for availability rows; (2) import new titles ONLY from homepage trending rails.
- 2026-07-24 run: 167 existing titles matched, 126 already had rows, 41 new availability rows added.

## 10. Actor popularity methodology — correction (2026-07-24)
- WRONG signal: ranking actors by credit COUNT already in our own DB — this just measures how much we've
  already scraped, not real-world popularity, and misses actors we haven't found yet by definition.
- BETTER signal: entertainment press coverage ("breakout star", "first superstar", viral/TikTok-fancam
  coverage, awards like Vertical Drama Fan Love Awards, Rolling Stone/Yahoo/People "hottest leading men"
  round-ups). Search queries like `"<platform>" hottest leading men vertical drama` or `vertical drama
  breakout star` surface these round-up articles, which name 5-10 actors at once with cross-links.
- Real finding this run: Nick Skonberg (called industry's "first superstar" by Yahoo, viral Oct 2025) was
  completely absent from people.csv despite his title already being in titles.csv with zero credits.
  Joseph Purcell (Dominic Purcell's son, notable enough for press coverage) had only 1 credit on file.
  Neither would have surfaced from a DB-credit-count-based priority list.
- NO Reddit access confirmed 2026-07-24: no MCP connector registered, and reddit.com is unreachable via
  both web_search (site:reddit.com returns near-zero real results) and web_fetch (robots.txt blocks it,
  same wall as IMDb direct fetches). Fan opinion mining route instead: entertainment press round-ups >
  fan-bio aggregator sites (famousbirthdays, celebethnicity-style) > IMDb "known for" > TikTok/YouTube
  captions surfaced via web_search (not direct platform access).

## 11. Origin categories — Western vs Chinese (decided 2026-07-26)
- RULE: every title carries an `origin` field (17th column in titles.csv). Values so far:
  `english` (default) and `chinese`. Any harvest that adds a title MUST set it. Blank is
  treated as `english` by the generator, so never rely on blank for a non-English title.
  NOTE: this value was renamed western -> english on 2026-07-28. build.py's ROOT_ORIGIN is
  "english"; this doc said "western" until 2026-08-01. It is routing/display only, never a
  slug, so the rename moved zero URLs.
- WHY: Western vertical drama (ReelShort/CandyJar/GoodShort/MyDrama/Vigloo/PineDrama, English
  language) and Chinese duanju (Douyin/Kuaishou native, Chinese language, 60-107 eps) are
  different products for different audiences. Mixing them dilutes the site.
- URL ARCHITECTURE (deliberate, do not "tidy" this):
    english -> /titles/{slug}.html, /where-to-watch/{slug}.html      (ROOT, unchanged)
    chinese -> /chinese/titles/{slug}.html, /chinese/where-to-watch/{slug}.html
  English stays at the root because ~9,076 URLs are already indexed. Prefixing English with
  /english/ would 404 every one of them and destroy the accumulated SEO. Never do this.
- Root sections (homepage, /tropes/, trope x platform pages, platform compare, the homepage
  "Titles" stat) are WESTERN ONLY. Non-Western origins are browsed from their own section
  index at /{origin}/index.html, which is auto-generated and linked from the homepage only
  when that origin actually has titles.
- ACTORS STAY GLOBAL at /actors/{slug}.html across all origins — one page per performer, so
  anyone working in both categories has a single complete filmography. Do not split actors.
- Trope pages are Western-derived. `trope_chip()` renders a trope as an inert span instead of
  a link when no trope page exists, so Chinese-only tropes can never emit a 404. If Chinese
  trope browsing is wanted later, generate /chinese/tropes/ rather than polluting the root.
- Verified at implementation: with 0 Chinese titles the refactor is a byte-for-byte no-op
  (9,076 pages, zero output files changed). A synthetic Chinese row was used to confirm
  routing, relative depth (../../ to root assets), and canonicals, then removed.
- SCALE WARNING: Chinese duanju is 20-50x the size of the Western catalogue (NetShort's
  sitemap alone = 69,913 unique series, mostly Chinese). Same discipline as section 9: this
  category needs a curated boundary, never a bulk import.

## 12. Vigloo — cast adapter (documented 2026-08-01, method recovered)

- 369 people carry `source=vigloo_2026-07-20` but this file had NO Vigloo section, so the
  method was undocumented. Recovered and recorded here.
- WHERE THE CAST IS: content pages ship a schema.org TVSeries block inside
  `<script type="application/ld+json">`, and that block carries an `actor` array:
      "actor":[{"@type":"Person","name":"Jung Jaebin"},{"@type":"Person","name":"Na Raon"}]
- TRAP: a summarising fetch tool reports "no cast anywhere on this page" for these URLs,
  because converting the page to text discards the JSON-LD. Read the RAW html. This cost a
  wrong conclusion once already ("Vigloo publishes no cast") before the raw fetch was tried.
- Names are already display-formatted; no camelCase expansion needed (unlike My Drama sec 5).
- URL shape: `https://www.vigloo.com/en/content/{8-digit-id}`, same for covered and uncovered
  titles, so the shape tells you nothing about whether cast exists.
- THE REMAINING GAP IS NOT RECOVERABLE FROM VIGLOO. Checked all 64 uncovered titles on
  2026-08-01: 0 yielded a cast. They are in one of two states:
    * no `actor` array in the JSON-LD at all (e.g. 15000926 My Four Billionaire Stepsisters)
    * an `actor` array holding a literal placeholder, `{"@type":"Person","name":"-"}`
      (e.g. 15001058 My Ex Sold Everything for Nothing)
  Guard against that "-" placeholder; a naive parser will happily create a person named "-".
- Titles that DO carry cast skew Korean-licensed (Timeleap Joseon etc.), which is likely why
  coverage stalled at 129/193 rather than the harvest being incomplete.
- Script: `generator/harvest_vigloo_cast.py`. Safe to re-run; it only touches titles with no
  credits, and will pick up newly-added Vigloo titles that do publish a cast.

## 13. Cast-data availability by platform (checked 2026-08-01)

Cast is the scarcest field in the DB: 2,269 of 3,407 titles have none. Status per platform,
so nobody re-tests these:
- ReelShort  93% covered - fandom blog cast lists (sec 3) is the richest source in the project
- My Drama   75% - `cast` array in the Next.js payload (sec 5), camelCase tokens
- Vigloo     67% - JSON-LD `actor` array (sec 12); the rest publish none, confirmed exhaustively
- CandyJar   46% - NOT on candyjar.com; sourced per-title from IMDb (sec 7 + the 2026-08-01 pass)
- PineDrama   1% - no cast on pinedrama.com (confirmed 2026-08-01)
- NetShort    0% - no cast anywhere on web (confirmed 2026-07-24 and again 2026-08-01)
- GoodShort   0% - no cast on drama pages (confirmed 2026-07-17 and again 2026-08-01).
                   1,820 titles, by far the largest single gap in the database.
- DramaBox      - bot-walled entirely (sec 8)

For the platforms at 0%, the only route is per-title off-platform sourcing (IMDb search, or
entertainment press for viral titles). There is no bulk option. Do not re-probe the platform
sites hoping for a different answer.
