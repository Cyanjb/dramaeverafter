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
- IMDb: bot-blocked from bash; works via search/fetch tools. Use for per-actor verification.
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
- NO cast data anywhere on web (confirmed; reviews note "actor search limitations"). Titles/availability only.
- Galatea originals (book adaptations): same-name matches on other platforms are DIFFERENT productions; match_queue them.

## 8. Big-platform status (checked 2026-07-17)
- DramaBox: comprehensively bot-walled. Main site, /browse, dramaboxdb.com, and all three official
  mirrors (dramaboxapp.com, dramaboxen.com, dramaboxtv.com) return 403 from bash; fetch tool also
  blocked on everything except the bare homepage. No bulk route. Per-title data only via web
  search snippets. Revisit occasionally; walls change.
- DramaWave: no functioning web catalog found (dramawave.com/.tv/.app all dead or 503). App-only.
  30K+ titles, mostly translated Chinese content — low fit for the English-actor-centric DB anyway.
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
