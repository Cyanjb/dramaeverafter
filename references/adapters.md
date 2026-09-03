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

## 14. Sandbox network policy — a false negative to watch for (2026-08-02)

The 2026-08-02 run could not scrape AT ALL, and the cause was the session
environment, NOT the platforms. Recording it so nobody writes a platform off
on this evidence.

- Symptom from bash: `curl: (56) CONNECT tunnel failed, response 403` for
  reelshort, goodshort, netshort, my-drama, vigloo and candyjar alike.
- Symptom from the fetch tool: HTTP 403 with no body, on every URL tried.
- THE TELL: `https://example.com/` also returned 403. A blanket block. When a
  neutral control host fails, the wall is local — stop testing platforms and
  check the environment before concluding anything about a site.
- Reachable regardless: github.com and the package registries (the policy's
  allowlist). Web SEARCH still worked; only fetching was blocked. Search alone
  returns editorial coverage, never catalog rows, so it cannot feed a delta run.
- Fix is environmental: the Claude Code environment's network policy has to
  allow the platform domains. See
  https://code.claude.com/docs/en/claude-code-on-the-web
- Contrast with sec 4 and sec 8, which record REAL bot walls (IMDb, DramaBox).
  Those were diagnosed in an environment where control hosts worked. A 403 only
  means "the platform blocks us" if unrelated hosts succeed in the same session.
- Section 6's reachability table was NOT re-verified on 2026-08-02 and its
  results still stand from 2026-07-17; nothing here supersedes it.

## 15. The skill's bundled copy of this file is stale (2026-08-02)

`~/.claude/skills/dramaeverafter-pipeline/references/adapters.md` is a much
older, generic version of this document — it stops at Tier 2 sources and lacks
sections 5-13 entirely. Worse, it CONTRADICTS this file: it states platform
sites "are not reachable from bash", while sec 1 here records that they are,
with a desktop User-Agent.

THIS FILE, IN THE REPO, IS THE SOURCE OF TRUTH. Read `references/adapters.md`
from the cloned repo at Stage 2, never the skill's bundled copy. The skill's
copy should be deleted or replaced with a pointer to this one.

## 16. Generator determinism (fixed 2026-08-02)

Not an adapter note, but it affects how you read a Stage 4 diff.

`build.py` used to render the "If you liked this" hint from a Python `set`, so
per-process hash randomisation rewrote that line on ~2,267 of 3,408 title pages
on EVERY build. Any Stage 4 rebuild therefore produced a ~2,300-file diff that
had nothing to do with the data, which made real changes impossible to spot.

Fixed by rendering from `tropes_of()` (deterministic ordered list, already used
by the trope chips on the same page). Verified byte-identical across
PYTHONHASHSEED=random and PYTHONHASHSEED=0.

EXPECTATION NOW: a rebuild with unchanged data produces ZERO changed files. If
you ever see a large diff again with no data change behind it, treat it as a
regression of this bug, not as normal build noise.

## 17. The manual worklists are generated now (2026-08-06)

CAST-WANTED.md and AI-CHECK.md were hand-written, so nothing took a title off
them once it was settled. Both had rotted:

- All four confirmed-AI titles were still in CAST-WANTED.md, two at slots 1 and
  3. AI productions have no human cast, so those were IMDb lookups that could
  never succeed - the worst kind of stale entry, right at the top.
- AI-CHECK.md still queued three decided titles, including Love at Dangerous
  Speeds at slot 1, which its own header names as confirmed NOT AI.

ROOT CAUSE: `titles.csv.ai` had no way to say "checked, not AI". Blank meant
unchecked, so a not-AI ruling had nowhere to live and the title returned to the
queue forever. The column is tri-state now - blank / yes / no - and only `yes`
is truthy in build.py's is_ai(), so `no` renders identically to blank (verified:
setting it changed 0 of 9,010 pages).

Both files are now built by `generator/make_worklists.py` from data/, so a
ruling recorded in the CSVs leaves the queue automatically. Re-run it after any
pass that adds credits or sets ai.

AI-CHECK's platform filter is deliberately just reelshort + my-drama, the two
that publish cast for their own catalogue (93% and 75%, sec 13). Vigloo and
CandyJar are NOT candidates despite partial coverage: sec 12 proved Vigloo's
remaining titles publish no cast at all, and sec 7/13 that CandyJar publishes
none on-platform. Their blanks are already explained, so including them added
~106 posters to check for a signal that was never there. An AI clue requires a
platform that normally lists cast - not merely one we have partial data for.

## 18. My Drama descriptions were DROPPED BY US, not withheld (diagnosed 2026-08-08)

126 of 186 My Drama titles carry no synopsis_short, which made My Drama look like a
platform that publishes thin metadata. It is not. Our parser lost the field.

- All 186 come from ONE run, mydrama_2026-07-17, same last_verified. There is no
  second, worse pass to blame.
- Of the 126 with no description, 125 still have episode_count and 124 have
  poster_ref. Sec 5 records all three as living in the SAME `"seriesData"` block,
  so the parser reached that block and wrote its neighbours.
- Sec 5 also lists `description` as a field the payload carries.

Therefore: re-run the sec 5 adapter and fill synopsis_short fill-blank-only. No
human input needed, and it is worth ~112 COMPLETE entries under the 8 Aug quality
bar, which makes it the cheapest completeness win in the database.

Not executed on 8 Aug because the environment blocked every platform domain; the
sec 14 control-host tell fired (example.com also failed), so nothing here is
evidence about My Drama's site.

GENERALISE THIS. Counting coverage per FIELD hides this whole class of bug, and it
sat unnoticed for three weeks because "cast is the biggest gap" was the only metric
anyone looked at. generator/completeness.py now scores leads + platform + link +
description together. WHEN ONE FIELD IS SHORT ON A PLATFORM WHILE ITS PAYLOAD
SIBLINGS ARE PRESENT, SUSPECT THE PARSER BEFORE THE SOURCE.

## 19. My Drama descriptions — EXECUTED (2026-08-09)

Sec 18 was right. 125 of the 126 blanks refilled from the platform; the 126th has
no direct_link so there was nothing to fetch. My Drama 14% -> 74% complete, site
total 723 -> 835 of 3,199 title-platform pairs, and My Drama became the third
platform to clear the 50-complete breadth bar. Script: `harvest_mydrama_descriptions.py`.

READ THE ld+json, NOT THE seriesData PAYLOAD. The description appears twice on a
series page. Sec 5 documents the streamed Next.js `"seriesData"` block, which is
escaped and needs unescaping — and the obvious `html.encode().decode('unicode_escape')`
reinterprets each UTF-8 byte as latin-1, producing exactly the invisible C1
mojibake already on the traps list. The same text sits in a clean schema.org
ld+json `@graph` as the node with `"@type": "TVSeries"`, which `json.loads` returns
with codepoints intact. Verified: the fetched text for a title we already held was
byte-identical to what was on file.

A CONTROL RE-READ IS WORTH THE EXTRA REQUESTS. Re-reading the 59 titles that
ALREADY had a description is what proved the reader before 125 writes: 51 came
back identical.

BUT DO NOT LET THE CONTROL CONFUSE ITS TWO FAILURE MODES — the first run aborted
on good data because of this. A control mismatch is either OUR READER mangling
characters (a bug, must stop the run) or MY DRAMA HAVING REWRITTEN the copy since
the 17 July scrape (not a bug, says nothing about the blanks). Tell them apart by
WHERE the strings diverge: a reader fault diverges at a punctuation or non-ASCII
character, a rewrite diverges at a word. Only the encoding class should gate a run.

MY DRAMA REWRITES ITS SYNOPSES. 7 of the 59 now carry materially different copy
('Sex therapist' -> 'Psychologist'; Mr. Denver is wholly new text). NOT APPLIED,
because CONVENTIONS.md makes non-blank fields fill-blank-only — they are recorded
in `generator/staging/mydrama_desc_2026-08-09.json` under
`control.changed_upstream_not_applied` for a human ruling. One more, 'Betrayal at
the Altar', is TRUNCATED MID-WORD on our side ('...love and jus'), which is our
bug rather than their rewrite and is the one worth fixing regardless.

## 20. Actor photos — the two ReelShort routes (2026-08-09)

ROUTE 1, actor_info on a movie page. A ReelShort `/movie/` page embeds
`"actor_info": {"actors": [{"actor_name", "actor_pic", "inside_url", "outside_url"}]}`,
where actor_pic is the `v-mps.crazymaplestudios.com/actorIMG/` URL. All 109 photos
already on file come from here. `outside_url` is an IMDb `nm` link and is currently
thrown away — worth harvesting, given the standing rule to record nm ids.

ROUTE 1 IS EXHAUSTED, MEASURED NOT ASSUMED. Across the 80 ReelShort pages
crediting a fan-panel actor, actor_info yielded 46 distinct names and EVERY ONE
already had a photo; 25 of the 80 pages carry no actor_info at all. It is a
curated subset, so a miss there is normal and is not a parse failure.

ROUTE 2, the fandom blog. reelshort.com/fandom is WordPress with an open REST
search at `/fandom/wp-json/wp/v2/search?search=`, and actor profile pieces carry
headshots under `/fandom/wp-content/uploads/YYYY/MM/`. This yielded 6 of the 33
fan-panel actors. Script: `harvest_actor_photos.py`.

THE FANDOM SEARCH IS FUZZY AND WILL HAND YOU THE WRONG PERSON — querying 'Ben
Taylor' returns an article about BEN ARMSTRONG. A hit is only safe when the
ARTICLE SLUG and the IMAGE FILENAME both contain the actor's full name slug. A
name appearing in an article's body is never enough.

REFUSE SHARED PHOTOS. Files like `jarred-harper-and-meg-bush.jpg` pass a naive
substring test but show two people, and a 78px avatar cannot say which face is
which. Accept only filenames whose stem EQUALS the name slug; report the rest.
This is what took the yield from 8 down to 6, correctly.

THE FANDOM HOST SOFT BLOCKS BY RETURNING HTTP 200 WITH AN EMPTY BODY. It is not
an error and not a parse problem — treat an empty body as retryable, pace requests
(~2s, serial), and cache to disk. Recovery took about 20 seconds.

CORRECTION TO SEC 5: MY DRAMA ACTOR PAGES CARRY NO PHOTOS AND NO BIOS. Sec 5's
'likely bios/photos, unharvested' was a guess and it is wrong. `/actors/{key}`
returns a Person node with name, givenName, familyName, jobTitle, url and
performerIn — no `image`, empty description — and all 27 images on the page are
series COVERS. The page is still a good credit source; it is not a photo source.

## 21. build.py wrote cp1252 on Windows and crashed mid-build (2026-08-09)

19 of its 20 `open()` calls omitted `encoding=`, so on Windows they inherited
cp1252 while every previous session ran on a UTF-8 sandbox. The build died on the
first actor bio containing a full-width comma (U+FF0C) — AFTER writing 8,991 files
in the wrong codec. Fixed by making all 19 writes explicit UTF-8.

TWO THINGS TO NOTE. A partial build leaves the tree in a state that looks like a
huge legitimate diff, so revert the generated output before re-running rather than
building on top of it. And the crash is the lucky case: a bio with only Latin-1
characters would have been written as cp1252 SILENTLY, differing from the repo's
UTF-8 and corrupting curly quotes and em dashes without any error at all.

## 22. THE DRIVE LEDGER — how to work a large PDF batch (established 2026-08-09)

READ THIS BEFORE STARTING ANY MULTI-FILE DRIVE BATCH. It exists because a
session listed a 93-file folder, reported the categories back, and that reading
of the folder was mistaken for having PROCESSED the folder. Four files had
actually been read. A listing is metadata; it is not work.

THE RULE: A BATCH OF MORE THAN ABOUT TEN FILES GETS A LEDGER BEFORE ANY FILE IS
TRANSCRIBED. The ledger is the single source of truth for what has been done,
and it lives on disk, never in the chat.

  generator/staging/drive_<date>_ledger.json
    one row per file: {id, title, kind, status, credits?, note?}
    status is todo | done | no_data | blocked
    validate on creation: entry count == folder count, and zero duplicate ids

  generator/staging/drive_<date>/
    ONE SMALL JSON PER TRANSCRIBED PAGE, plus an append-only _progress.log
    and the _stage.py helper that writes both in one step.

WHY PER-FILE OUTPUTS RATHER THAN ONE GROWING DOCUMENT. Appending to a single
staging file makes every write re-read and re-emit the whole document, which
gets more expensive with each entry and crowds out the actual work. Small files
keep each write flat-cost and let a batch be merged and applied in one pass at
the end. The same reasoning applies to the ledger: tick it in bulk at the end of
a pass rather than after every single file.

WHY IT MATTERS BEYOND BOOKKEEPING. A long batch will outlive the session's
context. The ledger is what lets the next pass — or the next session — answer
'what is left' without re-reading anything, and it is what makes an honest
progress number possible instead of an impression of one. Report progress as
'N of TOTAL files', never as a list of categories found.

STATUS no_data IS A RESULT, NOT A FAILURE. A CandyJar platform page carrying no
cast is a finding worth recording once so nobody opens it again.

## 23. THE PLATFORM IS IN THE FILENAME (Cyan, 2026-08-10)

Cyan encodes the PLATFORM in some Drive filenames, and where she does, that is
authoritative. It matters more than it sounds: IMDb never says which app a title
streams on, and platform is the one field that cannot be inferred from a title
page. The filename is often the ONLY source for it.

Forms seen in the 9 Aug batch:

  "Candyjar Drama- Grayson (TV Mini Series 2026) - IMDb.pdf"   -> candyjar
  "Shortmax drama- The Billion Dollar Baby ... - IMDb.pdf"     -> shortmax
  "Watch Study Buddy _ ... on CandyJar.pdf"                    -> candyjar
  "Goodshort Titles from IMDB.pdf"                             -> goodshort
  "Drama Box Titles from IMDB.pdf"                             -> dramabox
  "Shortical titles.pdf" / "Shortmax Titles.pdf"               -> shortical / shortmax
  "DramaPops Titles.pdf" / "Dramawave Title list from IMDB.pdf"-> dramapops / dramawave

NOT a platform: "Gideon - ShortDramaDB.pdf". ShortDramaDB is the SOURCE SITE the
page was saved from; that page's own content says the title streams on CandyJar.
Distinguish where-it-was-saved-from from what-app-it-is-on.

READ FILENAMES AT INVENTORY TIME, NOT JUST FILE CONTENTS. A session working this
batch reported that the ~200-title import queue was inert because platform was
unknowable from IMDb - while the platform-labelled title lists sat unread in the
same folder. The ledger now carries a platform_from_filename field; populate it
when building the ledger, before transcribing anything.

CONSEQUENCE FOR PRIORITY. The per-platform title-list PDFs are worth MORE than the
filmographies, because a filmography yields credits for titles we may not hold,
while a platform list yields exactly the title-to-platform mapping that turns an
unmatched filmography credit into an importable row.

## 24. CandyJar tropes — the data exists, the legend is robots-disallowed (2026-08-13)

CandyJar is the last platform sitting at ZERO tropes, which under the five-point bar
pins it at 0 complete out of 96 despite 66 with cast, 90 with a link and 58 with a
description. Sec 18 says suspect the parser before the source, so the page was
re-probed rather than trusted. The answer is neither one.

CANDYJAR DOES PUBLISH TAGS, AND WE NEVER READ THEM. A series page is a Next.js app
whose streamed `self.__next_f.push([1,"..."])` payload carries the full series
object, and every one of them ends with:

    "castMembers":{"castMemberIds":[55,154]},
    "tags":{"tagIds":[282,274,248,243,170,149,150,168]}

The homepage payload alone carries 275 series objects and references 104 distinct
tag ids. So the trope data is real, per-title, and already reachable.

THE ID-TO-NAME DICTIONARY IS ON NO ALLOWED SURFACE. tagIds are integers and nothing
resolves them. There is no /browse, /genres or /tags route (all 404). The rendered
series page shows the viewer no tags at all — confirmed by reading the live DOM, not
by grepping HTML. No client-side request fetches a tag vocabulary; the only network
calls on a series load are session, tracking and analytics. The one place the legend
could live is /api/, and:

    https://candyjar.com/robots.txt
    User-Agent: *
    Disallow: /api/

SO THIS IS A RULES STOP, NOT A TECHNICAL ONE. `/api/series/1` does return 200 and is
trivially readable, which is exactly why this needs writing down: the block is that
CandyJar disallows it, the same basis on which shortdramadb and verticaldrama.tv were
refused. DO NOT HARVEST IT. A future session that rediscovers the endpoint should
stop here rather than re-deciding.

WHAT IS LEFT. IMDb keywords, which needs a saved page per title, so CandyJar tropes
stay a Cyan-input job and are NOT the cheap unattended win the 13 Aug gap report
called them. Note the tags ARE harvestable in the sense that matters if CandyJar ever
publishes a legend, so re-check robots.txt before assuming this is permanent.

DO NOT DECODE A NEXT.JS PAYLOAD WITH unicode_escape. Same trap as sec 19: reassemble
by `json.loads()` on each pushed string literal and concatenate. The chunks are JSON
string literals, so this is exact; `.encode().decode('unicode_escape')` reinterprets
each UTF-8 byte as latin-1 and produces the invisible C1 mojibake already on the
traps list.

## 25. Platform hunting by restricted web search (2026-08-13)

The 13 Aug handover's DuckDuckGo `site:dramaboxdb.com "<title>"` route generalises,
and the generalisation is the useful part: run the search with the result set
RESTRICTED TO THE PLATFORM DOMAINS THEMSELVES rather than restricted to one platform
at a time. One query per title then names whichever platform holds it, instead of one
query per platform per title.

    domains: reelshort.com dramaboxdb.com dramabox.com my-drama.com candyjar.com
             goodshort.com netshort.com vigloo.com shorttv.live shortical.com

Run against the 16 fan-list titles this returned 4 platforms with a watch link and a
series id in a single pass (staged in
`generator/staging/fanlist_platform_hunt_2026-08-13.json`).

AN UNRESTRICTED SEARCH RETURNS AGGREGATORS, NOT PLATFORMS. Searching the bare title
surfaced shortdramadb.com, dramaglance.com and shortdramacast.com above every actual
platform. Those are the sources this project has already refused on rights grounds,
so an unrestricted search actively steers toward the one answer that must not be
used. The domain restriction is what makes the route safe, not just faster.

GRADE THE EVIDENCE, DO NOT FLATTEN IT. Three distinct strengths came back and they
are not interchangeable:
  - a watch page on the platform's own domain           -> confirmed
  - only the platform's FANDOM BLOG naming the title    -> probable, get a watch URL
  - only a /tag/ or /search? keyword landing page       -> proves nothing, it is a
    keyword echo and will match titles the platform does not carry

TAKE THE LINK, THE SERIES ID AND THE EPISODE COUNT. NEVER THE SYNOPSIS — search
results hand you the platform's marketing copy, which the standing caption rule
forbids copying or rewording.

A FAN LIST'S TYPO READS AS A MISSING TITLE. 'How to Tame a Sliver Fox' was queued for
import while we already held 'How to Tame a Silver Fox'. Exact-letter matching cannot
see a transposition; a difflib pass at cutoff 0.85 catches it and also surfaced
'Fallen for My Best Friend's Dad' against our 'Falling for My Bestie's Dad'. RUN THE
FUZZY PASS BEFORE ANY IMPORT QUEUE IS BELIEVED — creating a duplicate under a
misspelling is the one mistake that pollutes titles.csv permanently.

## 26. AN IMDb COMPANY LIST IS ~30% EPISODES — TAKE THE POSTER LINK (Cyan, 2026-08-13)

Cyan, reading the DramaBox company PDF: "there are some duplicates of the same show
except its episode of the same show". She is right, and it is not a small edge case.
An IMDb company search lists EPISODES as numbered results in their own right, mixed
in with the series:

    DramaBox   614 results  ->  196 episodes (31%)  ->  418 real series
    GoodShort  540 results  ->  116 episodes (21%)  ->  424 real series
    ShortMax   258 results  ->   72 episodes (27%)  ->  186 real series
    DramaWave / DramaPops / Shortical  ->  0 episodes

384 junk titles across three files. And text extraction FUSES the episode label onto
the series name, so they do not even look like episodes once parsed:

    Episode #1.1Forget Me Not: Omega's Return

THE FIX: EVERY RESULT HAS A POSTER LINK, ref_=sr_i_<slot>, EXACTLY ONE PER RESULT,
always pointing at that result's own tt. Pair it with the printed "<slot>. <name>"
line and drop any name matching ^Episode #\d+\.\d+. On DramaBox: 614 slots, 614
distinct poster ids, ZERO collisions. Implemented in parse_imdb_company_pdf.py.

THREE WRONG ROUTES, ALL TRIED FIRST, ALL PLAUSIBLE:
  - every /title/tt annotation -> 616 ids for 614 results, silently mixing in the
    episode links nested under a series result;
  - tt from extract_text() -> ZERO, the ids exist only in link annotations;
  - "a slot with more than one tt is contaminated" -> flags 198 slots, but most are
    just the poster AND the title text linking to the SAME series. It throws away
    good rows and still keeps bad ones. This one looked the most rigorous and was
    the most wrong.

A CORRECTION THIS OVERTURNED. The 9 Aug staged parse holding 413 titles was accused
in-session of having "silently truncated 413 of 611". It had not: there are 418 real
series, it held 413 of them with ZERO episodes wrongly kept. The accusation came from
comparing a raw tt count against the page header without asking what those ids were.
COUNT THE THING THE HEADER IS COUNTING before calling a parse incomplete.

TWO SAVES OF THE SAME PAGE CAN DIFFER, AND THE FILENAME NEVER SAYS WHICH IS FULLER.
'DramaPops Titles.pdf' is 1-50 of 63; 'Dramapops Title list.pdf' is 1-63 of 63.
'DramaWave Titles List From IMDB.pdf' is 198, 'Dramawave Title list from IMDB.pdf'
is 194. READ THE '1-N of M' HEADER AND PREFER N==M — a scroll that stopped early
saves as a perfectly valid PDF.

WHAT THE SIX FILES ARE WORTH, measured against titles.csv on tt (never on the title
string): 112 titles we ALREADY HOLD would gain a platform row, 72 of which have no
platform at all today and are therefore excluded from completeness.py's denominator
entirely. Plus an 878-title import queue. IMDb still gives no watch link, so a gained
platform row starts without a direct_link - see sec 25 for where the link comes from.

## 27. THE WEEKLY SCRAPE RUNS ITSELF NOW (2026-09-03)

The five-stage pipeline was designed weekly (Craft doc 7, sec 3) and had not
run since 24 July, because it only ever existed as a Claude session doing
fetches by hand and the cloud sandbox cannot reach a platform (sec 14).
`.github/workflows/weekly-scrape.yml` runs it unattended on a GitHub runner
every Sunday 12:00 UTC (14:00 Johannesburg), straight to main, push is
publish. Cyan chose ReelShort first, direct to main, Sunday afternoon (3 Sep).

- `generator/scrape_reelshort.py` writes `generator/staging/reelshort_<date>.json`
  (committed: it is the record, and it holds each title's synopsis as a fact
  source for captions). Routes: the 940 actor tag pages in harvest_queue.csv
  (sec 1, paginated), the homepage rails, the newest 100 fandom posts (sec 3),
  and /movie/ detail pages (sec 2) for anything not already refreshed. The
  sitemap route exists but is off: a sitemap is a sweep, and new titles are
  CHOSEN, not swept (Cyan, 8 Aug).
- `generator/merge_scrape.py` applies Stage 3 exactly: exact book-id match
  refreshes view_count, view_count_date, last_checked, last_verified and
  writes a DATED snapshots row; everything else fill-blank-only; a new title
  is created only when seen via tags, home or fandom; same slug, hyphenless
  slug match or same title after the leading article goes to match_queue and
  is never created; a 404 is reported, never deleted; credits only for an
  exact single-person name match; synopsis_short is never written.
- The run summary (counts, new titles, held, delisted, credits) is on the
  workflow run page under Actions. Dispatch by hand with `dry_run` to test a
  change, or `limit` for a quick probe.
- To add a platform: write `scrape_<platform>.py` emitting the same books
  shape, generalise PLATFORM in merge_scrape.py, add a step. GoodShort (sec 9)
  and NetShort trending rails (sec 9, second) are the obvious next two.
- Monthly full re-crawl on rotation and a 45-day staleness report were part
  of the original design; the summary already counts rows older than 45 days.
- Live probe, 3 Sep 2026 (57 requests, dry run): ReelShort publishes NO
  sitemap (four paths, all 404). The homepage __NEXT_DATA__ carries ~128
  books with NO /movie/ hrefs, so a home-only book gets a slug in
  ReelShort's style from its title and the detail route confirms the URL
  (canonical) before the merge may create it. The fandom REST JSON escapes
  slashes ("\/movie\/"), so links are matched on the unescaped text. Actor
  tag pages surface ReelTalk episodes with real view counts; merge_scrape
  excludes them by title (CONVENTIONS.md).
- Cyan, 3 Sep 2026, two standing consequences of the weekly run: (1) NEW
  TITLES NEED CAPTIONS. They land with no synopsis; the platform text is
  banked in the staging JSON and caption_pipeline.load_facts() reads every
  reelshort_*.json, so they are tier C (facts on disk) and `next` ranks
  them by reach. (2) THE NEW RELEASES RAIL KEYS ON FIRST-SEEN. build.py
  leads with titles whose source is a weekly run within 90 days, newest
  first, then the year ordering. The scraper also takes a year from any
  dated field in the book dict or the page's ld+json, fill-blank-only.
- 3 Sep 2026, later: two more routes. WANTED, `generator/staging/
  reelshort_wanted.txt`, one /movie/ URL per line for a title Cyan names;
  fetched every run, created on the next. GENRES, `generator/staging/
  reelshort_tags.txt`: ReelShort's own tag listing pages exist for moods,
  themes, styles and story beats (/tags/movie-moods/..., /tags/story-beats/...,
  /tags/movie-styles/drammatico-movies-... runs 160+ pages), same
  __NEXT_DATA__ tagBooks shape as the actor tags, paginated /2, /3. This is
  the near-whole catalogue with view counts and the only route to a title
  with no human cast (ReelShort's AI animated originals, e.g. A Zombie Girl's
  Journey Home, 6a8d2d531616ebd404056b3e). A genre page asserts no credit.
  merge_scrape.py creates from a sweep only above POPULAR_MIN (10M views;
  the held catalogue's median is 37.8M, 506 of 566 rows above 10M); the rest
  is counted in the summary as catalogue only.
