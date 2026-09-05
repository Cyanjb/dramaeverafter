# DramaEverAfter — handover for the next session

Paste this as your first message. Written 3 Sep 2026, 02:40 UTC, at the end of
the session that built the weekly scrape. Nothing from that session lives only
in chat: every ruling is in `generator/staging/reelshort_wanted.txt`, every
scrape record in `generator/staging/reelshort_<date>.json`, the design in
README.md and `references/adapters.md` sec 27, and the code comments say why.

---

We're continuing work on DramaEverAfter. Read README.md ("The weekly update
runs itself"), `references/adapters.md` section 27, and the header of
`generator/staging/reelshort_wanted.txt`. Then `git fetch` and run
`git rev-list --left-right --count origin/main...HEAD` before trusting any
state claim below.

## STATE: pushed, clean, live. main = a3098913 plus whatever run 5 commits.

## GOOGLE DEMOTION, 1 SEP (diagnosed 5 Sep) — THE RECOVERY IS THE PRIORITY

Search traffic died overnight 31 Aug -> 1 Sep: 58 clicks/1,939 impressions on
31 Aug, 0 clicks/44 impressions on 1 Sep. Diagnosis (GSC exports + live
probes, 5 Sep): ALGORITHMIC site-level quality demotion. Manual actions:
none. Security: n/a. Crawl: healthy throughout. Indexed count: stable
through 28 Aug, but the top page (eng-dub-apocalypse-romance-system, 76
clicks in Aug) has since been EJECTED from the index ("Crawled - currently
not indexed"). Brand queries still rank; content queries return nothing.
Likely trigger: scaled-content profile (646 verbatim platform synopses,
~2,000 castless/synopsis-less title pages, 1,600 one-credit actor stubs,
+167 new thin pages that week). Expect weeks-to-months recovery, tied to
content quality, not tricks.

RECOVERY STATE (5 Sep):
- Batch four captions (129, into the 35M reach tier) WRITTEN, all gates
  passed, staged UNAPPROVED in generator/staging/captions_2026_09_02_b4.py.
  Cyan is reviewing on the artifact page. Apply + build + push when she
  finishes. Then keep batching: 646 scraped synopses is the number to zero.
- Extensionless-to-.html 301 rules are IN _redirects but DORMANT, verified
  5 Sep: Netlify's Pretty URLs post-processing answers /titles/foo itself,
  so non-forced rules never fire (and forced 301! would LOOP - never use
  it). The fix is Cyan's toggle: Netlify site settings > Build & deploy >
  Post processing > disable Pretty URLs. The moment it is off, the rules
  take over and extensionless 301s to canonical. Until then canonical tags
  carry the load, as before.
- Sitemap: Google last read it 2 Aug; "Temporary processing error" on
  inspections. Cyan is resubmitting in GSC.
- AWAITING CYAN'S RULING (proposed, not applied): (a) noindex thin pages
  (~2,051 titles with no synopsis AND no cast; ~1,233 actor pages with <=1
  credit and no bio); (b) gate: new scraped titles ship noindexed until
  captioned. Do not implement either without her yes.
- Do NOT mass-"Request indexing"; it does nothing for a demotion.

## STANDING RULE: EMAIL (Cyan, 2 Sep)

Claude can send email via the Gmail connector as cyan@dramaeverafter.com
(default send-as alias on aiandcyan@gmail.com). NEVER send an email until
Cyan has seen the exact final text and explicitly said to send it. Feedback
on a draft, "yes", "sounds good", or tone notes are NOT a send instruction.
This was violated once (2 Sep, ReelShort outreach sent early); do not repeat.

THE WEEKLY SCRAPE EXISTS AND RUNS ITSELF. `.github/workflows/weekly-scrape.yml`
runs every Sunday 12:00 UTC (14:00 Johannesburg) on a GitHub runner (the cloud
sandbox cannot reach any platform; GitHub can), straight to main, push is
publish. Cyan chose ReelShort first, direct to main, Sunday afternoon. Three
pieces: `generator/scrape_reelshort.py` (routes: actor tag pages, genre tag
pages, homepage rails, fandom blog, the wanted list, title pages),
`generator/merge_scrape.py` (the database rules, enforced not remembered),
and the workflow. The run summary on the Actions page is the change report.

RUNS ON 3 SEP: run 3 (full, 1,139 requests) refreshed 666 ReelShort rows and
created 102 titles; run 4 (genre sweep + wanted list) refreshed 665, created
65, applied Cyan's AI rulings (A Zombie Girl's Journey Home is ai=yes). Run 5
was dispatched at 02:40 UTC with routes genres,wanted,detail to apply the hot
list rulings, the high fantasy umbrella, the tag-to-trope mapping and the four
"same" links. CHECK ITS SUMMARY FIRST: Actions > Weekly scrape > latest run.
The "still waiting" list there is dictation slips for Cyan to correct.

    3,680 titles (was 3,513) · ReelShort rows checked today 666 of 677
    snapshots now carry dates (audit H2 closed) · New and trending rail keys
    on first-seen · AI titles show by default, hide toggle in the Browse
    results head

## CYAN'S RULINGS TONIGHT (all recorded in the wanted file or data)

- "We definitely are going to have to start using AI-generated titles."
  About 80 AI titles named, ~20 human. `ai=yes|no` lines in the wanted file;
  the merge applies them. The ai column stays hand-set; the file is the hand.
- AI titles NOT hidden by default; a visible hide button. Done: Browse
  results head, beside sort.
- "Same" on the four weekly-scrape match_queue rows (status set; the merge
  links them to ReelShort on run 5).
- Djinn is the correct title (dictated "Gin, as in DJ").
- HIGH FANTASY is a trope, umbrella over werewolf, dragon, elf, mermaid,
  magic (185 titles). In tropes.csv and UMBRELLAS in merge_scrape.py.
- ReelShort's LGBTQ+ tag = our bl. TAG_ALIASES in merge_scrape.py.
- "New releases" renamed "New and trending" (releases land daily).
- New titles need captions: the platform synopsis is banked in the staging
  JSON, caption_pipeline.load_facts() reads it, so `next` ranks them by
  reach. The dea-captions skill writes them for her review. 167 new titles
  since 3 Sep have no caption.
- Trope names ReelShort uses that are NOT in our vocabulary, HER DECISION:
  music, high society, royalty, toxic romance, country, new adult, strong
  heroine, bully romance, regret, zero to hero, reverse harem, action, fated
  lovers, upgrade from ex, superhero, academy/school (she asked; we have
  campus 410 and college romance 12). Run 5's summary lists ReelShort tag
  names with counts.
- "When we finish we also need to clean up the trope tabs" (her words,
  3 Sep). The GoodShort trope soup from the 24 Aug handover is still open.

## OPEN QUESTIONS SHE RAISED, NOT YET ANSWERED

- Which ReelShort number is views? Their pages show collect (bookmark),
  likes, and a flame count. Our view_count is ReelShort's `read_count`
  field from its page data (plays), the same field the July scrape used, so
  rankings are consistent with July. The Great and Powerful Genie came in
  at 254.8M and leads the new titles; it should be in Most Watched. She
  says its tropes are high fantasy and superhero (superhero not in vocab).
- Waking Up Pregnant vs Spoiled by the Daddy CEO During Pregnancy: poster
  says one, page says the other. In the wanted file; check what search
  returns.
- The Alpha and His Nanny Luna and Blitzed by My Rival's Obsession: she
  thinks AI. The scraper now records when a title page says "AI-generated";
  the summary lists those without a ruling.

## TRAPS ADDED 3 SEP (append to Craft READ FIRST)

- GitHub refuses to dispatch a workflow that is not on the default branch
  (404). Test on main or not at all.
- A second workflow run on the same day used to OVERWRITE that day's
  staging JSON (run 4 replaced run 3's 753-book record). Fixed: the scraper
  merges into an existing same-day file. Verify on the next same-day run.
- The homepage rails carry books with no /movie/ href; the fandom REST
  JSON escapes slashes; actor tag pages list ReelTalk episodes with real
  view counts. All handled; see adapters.md sec 27.
- The sandbox cannot curl the live site (000 on every host). Verify via
  the GitHub commit and ask Cyan to look.
- A dictated title that never resolves is a mishearing, not a missing
  show: the wanted file's "still waiting" list is where to look.

## NEXT, IN ORDER

1. Read run 5's summary; fix any "still waiting" spellings with Cyan.
2. Captions for the 167 new titles, top by reach first (dea-captions).
3. Her trope vocabulary decisions above, then the trope cleanup.
4. GoodShort and NetShort scrapers, same staging shape (adapters sec 27).
5. The year capture: check "years filled" in a summary; if zero, the field
   names in year_hint() are wrong for ReelShort's page data.
