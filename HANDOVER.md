# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)**
2. **7. DEA TASKS (what needs Cyan)** — my to-do list, not your work queue
3. **7. DEA POPULAR ACTORS (Reddit fan panels)**

Then read, in the repo: `references/adapters.md` **sections 18–23**.

## FIRST: 23 COMMITS ARE UNPUSHED

`main` is at `14f1e67e7`. The working tree is **CLEAN** — nothing is at risk. But the
last thing that reached the live site was `e2751dcb2`, and **23 commits sit locally**.

Almost all of them are staged transcription (no page impact). The exceptions that
DO change pages are already committed and just need pushing. Ask Cyan before pushing;
she has been happy to, but each push is a live deploy.

Deploy is proven and automatic: a push on 12 Aug went live in ~20 seconds.

    3,416 titles · 2,125 actors · 4,186 credits · 9,220 pages · 15 platforms
    855 of 3,199 title-platform pairs complete (27%)
    titles.csv has an imdb_id column, 314 filled
    people.csv aka_names populated on 44
    match_queue: 43 still pending

## THE DRIVE BATCH — 67 of 93 FILES, 1,051 CREDITS STAGED, NONE APPLIED

Ledger: `generator/staging/drive_2026-08-09_ledger.json`.
Run `_reconcile.py` to rebuild status from the staged files (they are ground truth).

**Remaining: 25 files — 18 filmographies, 5 title pages, 2 misc.**

Everything transcribed since 12 Aug is staged only. The two appliers and their
converters are proven and in the repo:

    _to_filmography_batch.py  ->  apply_imdb_filmography.py
    _to_cast_batch.py         ->  apply_imdb_pdf_cast.py --json

## THE FINDING THAT MATTERS MOST

Cyan asked whether we hold all of Armand Procacci's titles. **We hold 14 of 47.**

Measured across all 28 actors whose IMDb pages she has supplied:

    810 IMDb credits · we hold 303 · 37% · 483 titles missing

**A comprehensive actor page is a TITLE-IMPORT problem, not a cast problem.** The
filmography PDFs already give us the full credit list; the titles those credits point
at do not exist.

- **165** of the 483 can get a platform from the already-parsed company catalogues.
  Cyan APPROVED importing these. `generator/build_filmography_import_2026_08_13.py`
  builds the queue and has NOT been run.
- The other **318** need one saved IMDb page each.

### I was wrong about the 318, and it matters
I told Cyan those had "no platform available". That was a statement about what is
parsed on disk, NOT about the world. **Every IMDb title page names the platform in
its production-company field.** She disproved it in one move by handing over
`Reelshort - You've Been Replaced, First Love (TV Mini Series 2026) - IMDb.pdf`,
where the filename AND the production-company field both said ReelShort.

So the 318 are a queue, not a wall.

## HOW TO READ A SAVED IMDb PDF — the indentation is the data

This was solved on 13 Aug and it changes the yield completely.

1. **`pypdf` link annotations** carry the cast `nm` ids. IMDb's links have
   `?ref_=tt_cst_t_N`, giving billing ORDER and the nm id for every slot.
2. **`extract_text(extraction_mode='layout')`** preserves IMDb's TWO-COLUMN cast
   grid: each row is `left actor | right actor` then `left character | right character`.
3. **NEVER STRIP WHITESPACE.** A lone character is only assignable by its INDENT.
   Stripping it took one title from 18 pairs down to 3.

Works on a Downloads PDF. **Drive is NOT required** — I told Cyan otherwise and
withdrew it. `py -m pip install pypdf` works.

The PDF Tools MCP cannot RENDER pages here (missing native canvas binding), so
visual inspection is not a fallback. The annotation route is the fallback.

## TRAPS ADDED THIS SESSION

- IMDb's **Upcoming/Previous pagination controls land INSIDE credit rows** on person
  pages, splitting a title, character, year or episode count from its own line — and
  can drop an UNRELATED credit into the gap. **Ten of fourteen** pages were hit.
  Every safe repair depended on another field independently confirming the orphan.
- **`aka_names` is not reliably "where the typos live".** Commit `930d17eab` filed 20
  variants as typos on 18 July; at least one, `Lukas Charles Stafford`, is a real
  billing name used in IMDb's own bio. Check before trusting that classification.
- **`aka_names` has no consistent separator** — 37 single, 5 pipe, 2 semicolon.

## WHAT CYAN RULED THIS SESSION

- Blend the Popular Actors rail with reach, not fans alone (done, live)
- Fix the truncated synopsis only, not the 7 upstream rewrites (done)
- Import the **165** titles that can have a platform (NOT yet run)
- "Do the checks when you suggest them" — act, don't park

## STILL FOR CYAN

1. **Save IMDb pages for the missing filmography titles** — now the highest-value
   thing only she can do. Platform prefix in the filename, Downloads is fine.
2. **The PineDrama 73.** Evidence is gathered: 64 of 73 have an IDENTICAL episode
   count to their twin, 8 blank on one side, **one** disagrees (*Big Bad Husband,
   Please Wake Up*, 55 vs 104). She checks ONE page, not 73.
3. **14 people.csv rows are two people fused into one** by a full-width comma
   (`Wang Yeonheum，Baek Seoryeo`). ~28 real people held as 14 identities.
4. **~2,084 truncated synopses**, counted as complete by `completeness.py`. Proven
   ours only for the 300-BYTE cases; the 687 GoodShort 300-CHAR ones need one fetch.
5. 43 pending match_queue rows.

## HOW CYAN WORKS

Don't ask her to approve routine decisions like slugs — pick sensible ones and tell
her. Do ask when something is one-way or a brand judgement. **Do the checks you
suggest, when you suggest them** — don't hand her a list you could have resolved.
Tell her before running anything that rewrites thousands of files, including
build.py. If you can't verify something, say so plainly rather than guessing.
Generated output that looks correct is not evidence that it works — click the thing,
measure the thing, request the URL.

**Captions and synopses are written from scratch. Never reword a platform's or IMDb's.**
