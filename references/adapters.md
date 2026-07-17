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
