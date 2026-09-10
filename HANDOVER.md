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

## COVERAGE EXPORT READ 10 SEP: THE 10K IS REAL, AND THE DEMOTION HAS A NAME

Cyan asked why GSC says she has 10K pages. She does. Her Coverage export
(data ends 4 Sep) says Google knows 11,188 URLs: 896 indexed, 10,292 not.
The repo publishes 9,941 html pages (3,753 titles x2 with where-to-watch,
2,213 actors, 199 tropes, 16 apps, the root pages); 4,892 carry noindex
since 5 Sep; 5,048 are in the sitemap. The ~1,250 extra URLs are the
extensionless twins (Pretty URLs is STILL ON, verified live 10 Sep:
/titles/brides-in-smoke answers 200 with a canonical) plus redirected
old URLs. `python3 generator/gsc_coverage.py <export folder>` prints the
two sides next to each other; run it on every Coverage export.

The not-indexed reasons: 864 alternative-canonical (the twins, harmless),
8 redirects, 7,664 discovered-not-indexed (mostly the thin pages, which
are now noindexed and out of the sitemap, so they fade slowly), 1,756
crawled-not-indexed (Google's page-by-page quality verdict; this is the
bucket that matters and shrinks as captions replace platform text).

THE INDEX EJECTION IS DATED: 28 -> 29 Aug, indexed 1,941 -> 896. That is
three days before the 1 Sep click cliff and a week BEFORE our noindex
shipped. Google threw out 1,045 pages on its own; the clicks followed.

THE UPDATE: Google's August 2026 Spam Update rolled out 18-21 Aug
(finished 21 Aug 04:51 ET), aimed at scaled content abuse, programmatic
pages and thin affiliates. Our impressions peaked 21 Aug, the decay
started the day the rollout finished, the ejection came 29 Aug. That is
the profile of a site caught by it, and the diagnosis below (scaled
content: verbatim platform synopses, castless pages, one-credit actors)
is exactly what it targets. Recovery in the published case studies: a
few months AFTER significant changes, and only by fixing, never by
waiting for the next update. So: captions and cast, week after week,
and no tricks. Do not expect the 8 Sep data to show anything yet.

Also verified 10 Sep: weekly scrape run 6 fired on schedule Sunday 6 Sep
and succeeded (first unattended run; ReelShort is current, 809 titles
verified this month, 2,767 still July-dated because GoodShort and the
rest have no scraper yet). The site has NO analytics of any kind; GSC is
the only visitor count and it lags 2-3 days. 818 of the 1,896 indexable
title pages still have no caption (they have cast, so they escaped the
thin rule).

SHIPPED 10 SEP, Cyan's go: GoatCounter on every page (build.py
GOATCOUNTER = "dramaeverafter"; the account must exist at
dramaeverafter.goatcounter.com with that code, or change the constant
and rebuild), and audit H3 closed: /data, /generator, /references,
/design-system and every root .md are forced 404! in _redirects. Both
have check_site.py twins. Cyan turned Pretty URLs OFF the same day; the
extensionless 301 rules fire from the next production deploy.

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

THE APOCALYPSE WAVE SHIPPED 5 Sep (Cyan: trending, bring them in, make
them look good): 29 new ReelShort titles from the survival-movies theme
tag via the wanted file (tropes=apocalypse), 68 captions written and
applied for the whole cluster under her 16 Aug below-top-300 ruling,
/tropes/apocalypse.html live with 69 titles, the eng-dub Apocalypse
Romance System pages (top Google earners, wrongly noindexed on
platform-views grounds) captioned and back in the sitemap. Live
verified. love-in-my-hands has no findable synopsis, waits for Cyan.
CORRECTED 6 Sep: THAT TRAP WAS A MISREADING. Probed live today, the
movie-page __NEXT_DATA__ is intact and books_in() parses it fine
(Fated to My Forbidden Alpha: 219.1M views, 61 episodes, cast, all
present). What had actually changed was the SANDBOX: it can now reach
reelshort.com and goodshort.com directly, where on 3 Sep it got 000 on
every host. The 5 Sep hand-enrichment was working around a network
block, not a parser bug. One REAL bug was found and fixed today: the
movie page calls the episode count "total" while tag pages still say
chapter_count, so every detail fetch was silently banking episodes="".
love-in-my-hands DOES have a synopsis on its page; it never needed
Cyan, it needed a reachable network.

RECOVERY STATE (5 Sep):
- BATCH FOUR IS DONE AND LIVE (6 Sep). Cyan reviewed all 129: 55 came
  back rewritten and were applied VERBATIM, the other 74 ticked (READ
  MEANS DONE). Approved file:
  generator/staging/captions_approved_2026_09_02_b4.py. Her edit rate is
  11.8% of words in the edited ones, ~5% across the batch and falling;
  what she actually changes is written up in CAPTION-TRAINING.md, and the
  short version is she LENGTHENS more than she trims, puts back the names
  I generalise, and talks to the reader with open endings and questions.
  Two things to keep: a two-dot ellipsis in her text was mechanically
  fixed and flagged (her own hard-ban list), and her "Mr Nice Guy" exposed
  a real gate false positive now fixed by the IDIOMS tuple in
  caption_pipeline.py - add to that tuple, never loosen the name rule.
- WIDGET BATCH OPEN, awaiting her (6 Sep): 15 drafts staged UNAPPROVED in
  generator/staging/captions_2026_09_06_widget.py, on the artifact page
  https://claude.ai/code/artifact/544403b2-b379-40aa-9b88-f5be67694fc3 .
  These are the 12 flesh-out titles ABOVE the top-300 floor plus the AI
  titles and front-page titles with no caption, so they need her eye.
  Generated with generator/make_review_page.py, which is the durable
  review-page generator and encodes her workflow. THREE could not be
  drafted and need her or a better source: first-daughter-forbidden-duty
  (no platform link on the row), when-the-wolf-fell-in-love (platform text
  is truncated boilerplate), the-mafias-stolen-bride-twin-switch
  (marketing blurb, no story).
- Extensionless-to-.html 301 rules are IN _redirects but DORMANT, verified
  5 Sep: Netlify's Pretty URLs post-processing answers /titles/foo itself,
  so non-forced rules never fire (and forced 301! would LOOP - never use
  it). The fix is Cyan's toggle: Netlify site settings > Build & deploy >
  Post processing > disable Pretty URLs. The moment it is off, the rules
  take over and extensionless 301s to canonical. Until then canonical tags
  carry the load, as before.
- Sitemap: Google last read it 2 Aug; "Temporary processing error" on
  inspections. Cyan is resubmitting in GSC.
- RULED AND APPLIED 5 Sep, Cyan: "hide the thin pages unless they are
  popular, new or a main actor" plus "if the thin page is popular, new, or
  a main actor then I need to flesh it out." Shipped: 1,888 thin title
  pages + their where-to-watch twins + 1,178 thin actor pages carry
  noindex and left sitemap.xml (9,825 -> 4,871 URLs). Carve-outs: top-600
  views (8.7M floor), first seen by a weekly scrape within 90 days, or a
  lead credit. Logic lives in build.py's NOINDEX block; the kept-but-thin
  survivors are FLESHOUT-QUEUE.md (163 titles, 55 lead actors), generated
  by generator/make_fleshout_queue.py, criteria kept in sync BY HAND. The
  earlier "gate new titles noindexed until captioned" proposal is DEAD:
  her carve-out keeps new titles visible; they surface on the flesh-out
  list and the caption queue instead. A noindexed page un-hides itself on
  the next build once it gains a synopsis or cast.
- Do NOT mass-"Request indexing"; it does nothing for a demotion.

## FLESH-OUT BATCH SHIPPED 6 Sep: 160 THIN PAGES -> 13

Cyan, 6 Sep: "can we do fixes while I finish the captions?" So, without
needing a ruling from her:

- 187 platform synopses fetched live for every title on FLESHOUT-QUEUE.md
  (the thin pages her carve-outs keep visible to Google), 187 of 187, no
  misses, banked in generator/staging/facts_fleshout_2026-09-06.json with
  a URL each. Possible only because the sandbox can reach the platforms
  again.
- 174 captions written and APPLIED under her 16 Aug below-top-300 ruling
  (top-300 floor is 39.4M views; 12 of the 187 sit above it and are hers
  to see, not written yet). Gates: check 174/174, readback read, copy
  detector top ratio 0.598 against source, mean 0.132.
- FLESHOUT-QUEUE.md: 160 thin titles -> 13. Those pages now carry real
  content instead of being offered to Google empty.
- NOT written, on purpose: 'dirty-work' (its platform text is a marketing
  blurb with no story, and inventing one is the thing the rules forbid).
- FLAGGED FOR CYAN: 'he-paid-for-one-night-then-wanted-forever' and
  'my-boss-is-my-secret-online-dom' carry BYTE-IDENTICAL platform
  synopses. One show, two ReelShort listings. Merge or alias is her call;
  both kept as separate rows for now because that is what ReelShort
  publishes. This is exactly the alt_titles case the GSC work found.

## THE VERDICT DATE IS 29 AUG, NOT 1 SEP (10 Sep coverage export)

The coverage chart adds the piece the performance data could not show.
Indexed pages HALVED on 29 August, 1,941 -> 896, with not-indexed jumping
8,594 -> 10,292 the same day. Clicks then ran normally for three more
days (2,084 / 2,036 / 1,939 impressions on 29, 30, 31 Aug) before the
1 Sep cliff.

So the sequence is: Google removed about a thousand pages from the index
on 29 Aug, and the traffic consequence surfaced three days later. The
decision date is 29 August. Anything looking for a cause should look at
what the site looked like THEN, not at 1 September.

COVERAGE LAGS FURTHER THAN PERFORMANCE. This export is dated 10 Sep and
its chart still ends 4 Sep, six days behind, where the performance export
ran two to three days behind. So neither export type has yet covered a
single day after the 5 Sep recovery work. Do not read any of these
numbers as the fix failing.

ISSUE COUNTS MOVED, 5 Sep -> 10 Sep, and this IS after the fix:
  Crawled - currently not indexed      83 -> 1,756   (+1,673)
  Discovered - currently not indexed   8,093 -> 7,664 (-429)
  Alternative page w/ proper canonical 411 -> 864     (+453)
The +1,673 is consistent with Google crawling the pages that got noindex
on 5 Sep and filing them accordingly, and the canonical rise is
consistent with the where-to-watch twins resolving. CONSISTENT IS NOT
CONFIRMED: the same movement would also appear if Google had crawled
1,673 pages and judged them not worth indexing on its own. The two
readings are told apart by WHICH URLs are in that bucket, so the next
useful export is the Coverage DRILLDOWN for "Crawled - currently not
indexed". Ask Cyan for it rather than guessing.

## THE REAL SHAPE OF THE COLLAPSE (6 Sep exports, data ends 4 Sep)

CORRECTS the earlier "traffic died overnight" reading. The 28-day chart
shows three phases, not one event:

  8-18 Aug   0 to 13 clicks a day. The site was barely in search.
  19 Aug     JUMPS to 71 clicks / 1,894 impressions, peaks 21 Aug at
             102 clicks / 3,515 impressions. Nothing was deployed on
             18-19 Aug: this is Google's own indexing of the 14-16 Aug
             work (AI-search schema, llms.txt, trope cleanup, the first
             captions) plus the usual new-content trial boost.
  20-31 Aug  STEADY DECAY, 102 down to 58 clicks (-43%), impressions
             -45%. Twelve straight days of Google losing confidence.
  1 Sep      Cliff. 0 clicks, and impressions 1,939 -> 44 -> 21 -> 7 -> 4.

That impression collapse is not a ranking demotion, it is removal from
content results: only brand queries still serve. Nothing shipped between
27 Aug and 2 Sep, so the cliff is entirely Google-side. Read together,
the site was given a trial in mid-August, was measured over twelve days,
and failed it. That is exactly what a scaled-content profile does, and it
is why the thin-page noindex plus real captions is the right answer
rather than a trick.

TIMING: the recovery work shipped 5 Sep and GSC lags 2-3 days, so this
export CANNOT show it. Earliest signal is ~8 Sep, and the honest
expectation stays weeks to months. Do not read 1-4 Sep zeros as the fix
failing.

## WHY THE TOP PAGE WON, AND THE THREE PLAYS (6 Sep)

Cyan asked why /titles/eng-dub-apocalypse-romance-system.html did so well
(76 clicks, 13.57% CTR at position 7.5, five times the site average) and
whether we can repeat it. Answered from the GSC exports, not from theory:

IT WON A SEARCH FOR A SHOW WE DID NOT LIST. Its clicked queries are
"romance system made me the king of the apocalypse full / full movie /
free" - a SEPARATE GoodShort listing (id 31001702445, 29 eps, mercenary
Ethan and Emily the SSS rank zombie) that was in no row of our database.
Google had the demand, our page was the closest text, the clicks landed by
accident. ADDED 6 Sep as its own title with a written caption; it is NOT
merged with the Oliver Burton show, different lead, separate listing.

THE THREE PLAYS, in value order:
1. UNSERVED DEMAND. 361 queries, 4,257 impressions, 123 clicks are for
   subjects in no title or actor row. Each is a title to add or an alt
   name to record. alt_titles is filled on 8 of 3,752 rows: that column
   is the lever, because the same show carries a different name on every
   app and every relisting.
2. INTENT DECIDES CTR, NOT RANK. Watch intent ("full", "free", "watch",
   "online") converts at 14.2%. Cast intent converts at 1.5% across 3,324
   impressions, actor-age intent at 461 impressions for 2 clicks. We rank
   for cast and age questions and cannot answer them: 61% of titles hold
   no cast, 68% of actors no bio. Serve those or stop chasing them.
3. CHARACTER NAMES ARE SEARCHED, ACTOR NAMES ARE NOT. "elijah baran
   actor" and "elijah baran genie actor": 421 impressions, 14 clicks, and
   Elijah Baran is a ROLE played by Eric Guilmette (whose page is already
   our top AI-Overviews earner). We hold the fact inside his bio text
   where nothing can search it. A character index is Cyan's design call:
   do NOT stuff role names into aka_names, that column means the actor's
   other names and would render a lie on the page.

generator/gsc_opportunities.py makes this repeatable. Point it at a GSC
Queries.csv export folder; it prints UNSERVED, BLIND SPOTS (top-10
position, 15+ impressions, zero clicks) and the INTENT table. It only
prints: every fix is a human ruling about what is really the same show.

## THE dea-captions SKILL EXISTS NOW (6 Sep, Cyan: "we need a skill for this")

.claude/skills/dea-captions/SKILL.md, in the repo so it is version
controlled and any session working here gets it. It exists because the
caption rules were spread across CAPTION-TRAINING.md, comments inside
caption_pipeline.py and this handover, and had to be REMEMBERED - which is
how the 6 Sep length regression happened. The skill holds the process and
the failures that repeat; CAPTION-TRAINING.md still holds the craft, and
the skill says to read it in full before every batch.

It also bundles scripts/lift_check.py, a NEW gate that closes a real hole.
The copy detector compares whole bodies and fails at 0.6, so a caption can
score 0.13 and still carry "three Masters beyond Sacred Rank" lifted word
for word - one phrase barely moves a whole-body ratio. lift_check reports
every 5+ word run shared with the source. Run it on every batch and read
each hit: keep names and genre terms, rewrite the rest. It immediately
found four real lifts in captions that had already passed every other
gate, including an 8-word run.

## SITE-CHECKS EXISTS (6 Sep, Cyan asked for a checklist)

SITE-CHECKS.md is the plain-words list of what must always work (search,
rails, pins, tropes, sitemap/noindex, redirects) and check_site.py is the
same list as code: it runs in the weekly workflow between build and push,
and a FAIL stops the publish. THE TWO ARE TWINS - a new must-keep-working
behavior gets a line in both, in the same commit. Run it locally after any
build: python3 generator/check_site.py.

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
- 6 Sep: New and trending sits directly under Most watched on the homepage
  and now RANKS BY GROWTH, not first-seen date: views gained per day between
  the two most recent snapshots times the daily percentage gain (both, so
  neither giants nor 100K-doublers own the rail). data/pinned.csv is Cyan's
  hand: a title_id with rail=trending leads the rail regardless of score
  (first pin: a-zombie-girl-s-journey-home, her call). Remove the row to
  unpin. Also 6 Sep: every search on the site forgives apostrophes, accents,
  punctuation and word order ("girls" finds "Girl's"); norm_search() in
  build.py and its JS twin SEARCH_NORM_JS must stay identical.
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
- The sandbox CAN now reach the live site, reelshort.com and
  goodshort.com (verified 6 Sep 2026; it could not on 3 Sep). Live
  verification and synopsis fetching both work from here again. Netlify's
  edge can serve a stale copy for a minute or two after a push, so check
  the deploy permalink before believing "still old".
- A dictated title that never resolves is a mishearing, not a missing
  show: the wanted file's "still waiting" list is where to look.

## NEXT, IN ORDER

1. Read run 5's summary; fix any "still waiting" spellings with Cyan.
2. Captions for the 167 new titles, top by reach first (dea-captions).
3. Her trope vocabulary decisions above, then the trope cleanup.
4. GoodShort and NetShort scrapers, same staging shape (adapters sec 27).
5. The year capture: check "years filled" in a summary; if zero, the field
   names in year_hint() are wrong for ReelShort's page data.
