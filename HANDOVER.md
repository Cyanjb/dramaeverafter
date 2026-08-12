# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)**
2. **7. DEA TASKS (what needs Cyan)** — my to-do list, not your work queue
3. **7. DEA POPULAR ACTORS (Reddit fan panels)**

Then read, in the repo: `references/adapters.md` **sections 18–23**.

## FIRST: NOTHING IS COMMITTED, AND THE PILE IS NOW BIGGER

`main` and `origin/main` are both at `fa502cc3f`. The working tree carries the
9–10 Aug session's work **and** the 12 Aug session's work, all unreviewed by Cyan.
She was asked on 12 Aug and chose to review before committing. Do not commit
without asking again.

**A restore point exists outside the repo**: `C:\Users\cyanj\dea-restore-2026-08-12\`
holds `tracked-changes.patch`, `untracked.zip` (55 files) and `status.txt`, captured
at the START of the 12 Aug session. It restores the 9–10 Aug state, not the 12 Aug one.

## WHAT THE 12 AUG SESSION DID

**The 543 staged Drive credits are APPLIED.** They sat inert across two sessions.

    credits.csv       3,988 -> 4,184   (+196: 43 filmography, 153 title-page)
    people.csv        2,029 -> 2,125   (+96)
    castless titles   2,196 -> 2,152
    CandyJar castless    39 -> 18
    complete entries    835 -> 855     (26% -> 27% of title-platform pairs)

**CANDYJAR CLEARED THE 50-COMPLETE BREADTH BAR** — fourth platform over it, after
ReelShort, Vigloo and My Drama. Also 36 blank character_names filled and 9
aka/socials fields on people who had none while we held their nm id.

Route: `generator/staging/drive_2026-08-09/_to_filmography_batch.py` and
`_to_cast_batch.py` convert the staged per-file JSON into the shapes the two audited
appliers want. `apply_imdb_pdf_cast.py` gained a `--json` input and ASCII-folded
slugs for NEWLY CREATED people only.

**Betrayal at the Altar's truncated synopsis is fixed** (now ends `justice.`).

### Three things that would have corrupted data if applied raw
- **Mojibake in the transcription**: `CÃ©line Planata`, `Arne KÃ¼bler`, `SÃ©lynne Silver`
  were UTF-8 read as latin-1. people.csv had zero corrupted names before and still does.
- **An accent collision**: repaired `Céline Planata` no longer matches the
  `Celine Planata` on file, so she would have arrived as a SECOND person. The stored
  spelling was used; she was not renamed.
- **The article and casing traps**: `Alpha's Doe` -> our `The Alpha's Doe`;
  `Half of My Heart` -> our `Half Of My Heart`. Raw, these report as "not in
  titles.csv", indistinguishable from genuinely absent.

### Slug decision, made not asked (per Cyan's standing instruction)
New people get ASCII-folded slugs: `Arne Kübler` -> `arne-kubler`, not `arne-k-bler`.
The 12 EXISTING people with the older shape (`ch-na-verony`, `andr-s-de-la-mora`,
`mari-a-camila-rueda`) were deliberately NOT rewritten — they are published URLs.

## THE BIG UNRESOLVED FINDING: ~2,084 TRUNCATED DESCRIPTIONS

Chasing one truncated synopsis turned up a systemic cut. TWO different caps, which
means two different scraper paths:

    cut at exactly 300 CHARACTERS   687 titles   GoodShort 525, vigloo 66, pinedrama 59
    cut at exactly 300 BYTES         27 titles   CandyJar 22, my-drama 2
    300/300, pure ASCII, fits either 1,370       GoodShort 1,138

`completeness.py` scores every one of them as HAVING a description, so the 27%
completeness figure is softer than it looks. The truncation is PROVEN ours only for
the byte-cap case (My Drama serves 303 chars, we stored 300 bytes). The 687
char-capped GoodShort rows need ONE fetch to settle whether GoodShort itself
publishes a 300-char teaser — do not assume either way.

## THE SITE IS REBUILT AND THE TROPE TAGS MOVED

Cyan approved the rebuild once the restore point was in place. 9,124 -> **9,220 pages**
(+96, exactly the new actors). Verified in a real browser, not just in the markup:
`Arne Kübler` renders its umlaut, no page contains U+FFFD, both trope chips resolve 200,
and `celine-planata.html` is a single page with 5 credits while `c-line-planata.html`
404s — the accent collision did not create a duplicate.

**TROPE TAGS NOW SIT UNDER THE SYNOPSIS** on title pages (Cyan, 12 Aug). They used to
sit between the views line and the watch card. Order is now h1 -> views -> watch card
-> "The story" -> trope chips, measured with getBoundingClientRect (story bottom 624,
chips top 646, 22px gap). The chips div is now CONDITIONAL — a title with no tropes
used to emit an empty `<div class="chips">`.

### A BUILD CRASHED MID-RUN ON 12 AUG. READ THIS.
The first attempt died with `PermissionError [WinError 32]` on
`actors/sophia-delucchi.html`: a background process of MINE was reading the tree while
build.py was unlinking it. Windows locks open files; Linux does not. **Never leave a
process reading the output tree while build.py runs.** Worse, the command was piped
through `tail`, so `$?` reported the exit of `tail` and printed `BUILD EXIT=0` over a
crash — the same masking trap as the `| head` one already on the list. **Capture the
exit code before the pipe, or redirect to a file.** The partial tree was healed by
re-running the build twice and confirming identical diff fingerprints.

## TWO DECISIONS ASKED ON 12 AUG AND NOT ANSWERED

1. **8 near-matches queued** in match_queue.csv, all punctuation/article-only and all
   almost certainly one production each:
   `Feelin the Burn`/`Feelin' the Burn` · `I'm a Queen, Not a Mistress`/`...Queen Not a...` ·
   `The CEO and the Country Girl`/`CEO and...` · `Love's U-Turn from a Mistake`/`Love's U-Turn，From a Mistake` ·
   `Mancini's Forbidden Bride` (straight vs curly apostrophe) · `My Cold-Blooded Alpha King`/`My Coldblooded...` ·
   `Billionaire's Baby`/`The Billionaire's Baby` · `Ex-Husband Step Aside: Lady Boss Returns`/`..., Lady Boss...`
2. **Two aka_names appends.** Procacci: we hold `Armund`, IMDb says `Arman`. Tiller:
   we hold `Jakson`, IMDb says `Jack` (billed that way on two titles). Both were left
   alone because fill-blank-only skips non-blank fields. Unrecorded variants are
   exactly what makes a future pass create duplicate people.

## SMALLER FINDINGS FROM 12 AUG

- **Our title contains a full-width comma**: `Love's U-Turn，From a Mistake`. U+FF0C is
  the character class that crashed build.py on 9 Aug.
- **Two people.csv rows hold TWO names each**, joined by a full-width comma:
  `Wang Yeonheum，Baek Seoryeo`, `Oh Hyeon-yeop，Son Chung-yang`, and two more.
  Pre-existing, not from this session.
- **Not imported, correctly**: `Forgive Me Father` and `The Billion Dollar Baby` have
  title-page cast staged but neither title is in titles.csv. Titles are chosen, not swept.
- `Céline Planata` is stored as `Celine Planata`. IMDb has the accent. Not renamed.

## THE 9 AUG DRIVE BATCH — 47 of 93 FILES TRANSCRIBED, ALL 47 NOW APPLIED

Ledger: `generator/staging/drive_2026-08-09_ledger.json`. Run `_reconcile.py` to rebuild
statuses from the staged files (they are ground truth; the ledger has drifted before).
`_progress.log` now carries a 12 Aug entry recording exactly what was applied — the
staged JSON is a RECORD, NOT A QUEUE, so do not re-apply it.

**Remaining: 46 files — 35 filmographies, 9 title pages, 2 misc.**

### THE PLATFORM IS IN THE FILENAME
"Shortmax drama- ...", "Goodshort Titles from IMDB", "Candyjar Drama- ...". IMDb never
says which app a title is on. adapters.md sec 23.

### Platform catalogues already parsed
    dramabox   413 titles  co1028734       dramawave  194  co1124838
    goodshort  190         co1045147       shortmax   186  co1065580
    dramapops   50         co1084498       shortical   24  co1167893

**112 titles we ALREADY HOLD could gain a platform** without importing anything. That is
the cheapest breadth work left and it is still untouched.

### Platform URLs recovered (2 of 7 dead buttons)
    shortical  https://www.shortical.com/   verified 200
    shortmax   https://www.shorttv.live/    verified 200

## HOW CYAN WORKS

Don't ask her to approve routine decisions like slugs — pick sensible ones and tell her.
Do ask when something is one-way or a brand judgement. **Tell her before running anything
that rewrites thousands of files**, including build.py. If you can't verify something, say
so plainly rather than guessing. Generated output that looks correct is not evidence that
it works — click the thing, measure the thing, request the URL.

**Captions and synopses are written from scratch. Never reword a platform's or IMDb's.**
