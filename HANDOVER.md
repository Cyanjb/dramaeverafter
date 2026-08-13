# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)**
2. **7. DEA GAPS (what needs filling, ranked)** — new, the three worklists
3. **7. DEA TASKS (what needs Cyan)** — my to-do list, not your work queue

Then read, in the repo: `references/adapters.md` **sections 18–23**.

## NOTHING IS UNPUSHED. Check before you believe otherwise.

`main` and `origin/main` are both at the same commit, working tree clean, everything
live.

The last handover claimed "23 commits unpushed" and it was **stale** — the previous
session pushed after writing the note. A session then nearly re-did applied work on
the strength of it. **Run `git rev-parse HEAD origin/main` before trusting any
unpushed count.**

    3,586 titles · 2,212 actors · 4,621 credits · 3,370 availability · 9,620 pages
    642 of 3,370 title-platform pairs COMPLETE (19%) under the FIVE-point bar
    2 platforms clear the 50-complete breadth bar: ReelShort 467, My Drama 136
    match_queue: 77 pending of 205

Deploy is automatic and proven: new pages went 404 to 200 in about 12 seconds, and
the live pages were checked for CONTENT, not just status.

## THE QUALITY BAR CHANGED — 19% IS NOT COMPARABLE TO THE OLD 26%

Cyan restated it on 13 Aug with **five** points, where the recorded rule had four:

    a title · a caption WE wrote · at least the leads · a link to the platform · 1+ trope

`generator/completeness.py` enforces all five. Two were added:

- **at least one trope**, because an entry with no trope is invisible to every trope
  page and every combo page, which is how this audience browses.
- **the caption must be ours**. The old check measured LENGTH only, so a scraper
  truncation counted as a description — the metric was certifying entries that break
  the caption rule. It now rejects the two documented truncation shapes (exactly 300
  characters, exactly 300 bytes). That is a floor, not a guarantee: verbatim copy of
  an untruncated synopsis still passes, so provenance is enforced at WRITE time.

Cyan's reason for the caption rule, confirmed 13 Aug: **copyright** (and a close
paraphrase can still be derivative, which is why the rule says "from scratch" and
not "reworded"), plus **duplicate content** — if our synopsis matches ReelShort's,
Google has no reason to rank our page over theirs.

## THE DRIVE BATCH IS FINISHED: 92 done, 1 no_data, 0 todo of 93

And it was closed by **parsing**, not transcribing. Hand-reading is what made it take
four sessions. Two new scripts:

    generator/parse_imdb_person_pdf.py   filmography -> staged credits
    generator/parse_imdb_title_pdf.py    title page -> cast grid AND platform

**Both were controlled against three hand-transcribed pages before being trusted:**
Griffin Blazi 38/38 exact, Kasey Esser 55/55 exact, Armand Procacci 46 of 47, and
**zero false positives across 141 credits**. Use them for the next batch. They read a
Downloads PDF; Drive is not required. pypdf is already installed.

The control caught three bugs that wrote **wrong** data rather than none — read the
docstrings before changing either parser.

## WHAT ONLY CYAN CAN DO, highest value first

1. **SAVE MORE IMDb PERSON PAGES.** `ACTORS-FILMOGRAPHY.md` ranks **2,100 unread
   actors by REACH**, with the IMDb link pre-filled wherever we hold an nm id. Top of
   the list: Jesse Morales 2.1B views, Samantha Drews 1.7B, Autumn Noel 1.4B. Save as
   `<Name> - IMDb.pdf` to Downloads — the parser takes the name from the filename.
   Measured: across the 28 actors read so far, IMDb credits them on 810 titles and we
   hold 476 (59%, up from 37%). The gap is titles that do not exist, not cast.
2. **The PineDrama 73** — one page to check, not 73. 64 of 73 have an identical
   episode count to their twin, 8 blank on one side, and exactly ONE disagrees
   (*Big Bad Husband, Please Wake Up*, 55 vs 104).
3. **14 people.csv rows are two people fused** by a full-width comma. About 28 real
   people held as 14 identities, with credits attached to the fusion.
4. **77 pending match_queue rows**, including the Sophia Soto lead (named only on a
   TikTok post as Study Buddy cast — not applied, a caption is not evidence).
5. **16 fan-list titles we don't hold**, from an IMDb user list with 15,500 visits —
   a *chosen* import queue, still needing platform evidence.

## THE THREE WORKLISTS (regenerated, never hand-edited)

    py generator/make_gap_report.py

    ACTORS-PHOTOS.md       2,013 credited actors with no photo
    ACTORS-FILMOGRAPHY.md  2,100 actors whose IMDb page has never been read
    TITLES-INCOMPLETE.md   2,684 failing the 5-point bar, 835 ONE FIELD SHORT

Ranked by reach. **`view_count` is a display string** (`'218.1M'`) and `int()` on it
silently yields zero — 2,340 of 2,374 populated rows are non-numeric. Use the
`views()` helper; do not write a second one.

## YOU CAN SEARCH THE WEB YOURSELF — USE IT FOR PLATFORM HUNTING

Cyan had to google a platform on 13 Aug that the session could have looked up itself.
Don't repeat that. The Browser pane tools drive a real browser.

- **Google bot-blocks it** with an "unusual traffic" check. Do NOT try to solve it —
  CAPTCHAs are off-limits. **DuckDuckGo works**, including `site:` queries.
- The query that worked, and it is a ROUTE rather than a one-off:

      site:dramaboxdb.com "<exact title>"

  For `I Became Mrs Grayson by Bragging` that returned DramaBox's own database page in
  one hit — giving the **platform, a direct_link, and the episode count (59)** where
  the IMDb page had named only production houses. A plain title search had returned
  only a Dailymotion re-upload, so the `site:` restriction is what made it work.
- **Take the link and the episode count. NEVER take the synopsis** — it is the
  platform's text and the caption rule forbids copying or rewording it.
- Worth running at: the 16 fan-list titles we don't hold, and any title whose IMDb
  page names only production houses.

## READY TO PICK UP

- **1,918 of 4,603 credits have a blank `character_name`**, and staged filmographies
  can fill 19 right now. The applier skips them because it treats an existing credit
  as "already complete" before looking at the empty field. Character names are one of
  the two stated edges over VerticalVault.
- **CandyJar: 96 titles, ZERO tropes** — and unlike My Drama this is NOT a parser gap.
  A series page was probed: no `genre`, no `keywords`, nothing. It needs another
  route (IMDb keywords the obvious candidate).
- **0 thin trope pages**, down from 44; the 5+ rule is now enforced for plain trope
  pages too. 43 withdrawn URLs will 404 for Google until it re-crawls.

## TRAPS ADDED THIS SESSION

- **A converter's output is not the transcription.** `_filmography_batch.json` and
  `_cast_batch.json` are built FROM the per-actor files and were both stale, so 17 of
  28 actors had never reached an applier while the other 11 were already applied.
  Regenerate from the per-file JSONs and dry-run before believing either direction.
- **`harvest_mydrama_descriptions.fetch()` returns `(html, error)`** and swallows the
  exception. Called unchecked it yields a TUPLE, every parse fails silently, and the
  run reports 0 recovered — indistinguishable from the platform publishing nothing.
- **Matching a vocabulary by exact slug cannot see a near miss.** The My Drama harvest
  produced `vampires` beside our existing `vampire` (642 titles). `build.py`'s
  canonicalisation folds CASE and SPACING onto one slug and CANNOT fold two different
  slugs. Flag near-slugs; do NOT auto-merge — `mate`/`mates` differ in this genre.
- **A platform's `genre[]` mixes content with UI labels.** My Drama's carries
  `trending` (22 titles) and `male lead`. `trending` cleared the 5+ bar and would have
  published a page nothing on the site can ever keep true.
- **Sec 5's My Drama field list is incomplete** and is now wrong in a checkable way
  twice. It names no genre field; the ld+json TVSeries node carries `genre[]` and
  `keywords`, in the same node the description pass read and walked past. Also
  `"seriesData"` is GONE — they restructured. **Prefer the page over the field list.**
- **IMDb appends the billing variant to the character** — "Kane Hudson (as Jesse
  Morales)". Eight credits went live with it before it was caught.
- **A commit message is not evidence that a write happened.** Commit `349201992` says
  "it gains a platform"; that title's availability was empty until 13 Aug.
- **Blank-line blocking is the wrong model for a PDF credit list.** Two credits render
  with no blank between them, and a first-type/last-year reading fuses them — it gave
  one title the episode count of the one below it.
- **Never round-trip a UTF-8 file through `Get-Content` + `Set-Content`.** The default
  read encoding is cp1252, so every em-dash comes back as mojibake and then gets
  written back as "valid" UTF-8. This corrupted HANDOVER.md itself on 13 Aug. Edit
  files with a real editor/writer, not PowerShell string replacement.

## STANDING RULES ADDED THIS SESSION

- **Production houses are not a platform** (Cyan, 13 Aug). If the production-company
  field names only production companies, LEAVE THE TITLE OUT until its platform is
  found. This is a wait, not a rejection: `I Became Mrs Grayson by Bragging` was held
  back on this rule, then landed the same day once the platform was found by search.
- **A name variant is settled by the nm id, not by resemblance** — and the id is often
  already on disk. Where no nm exists, the second route is the same series under two
  title names on two sites. Merge INTO the existing person_id; those slugs are
  published URLs. Two merges landed this way: jesse-morales 23 to 30 credits,
  robert-watkins 1 to 12.

## HOW CYAN WORKS

Don't ask her to approve routine decisions like slugs — pick sensible ones and tell
her. Do ask when something is one-way or a brand judgement. **Do the checks you
suggest, when you suggest them** — don't hand her a list you could have resolved, and
don't hand her a lookup you could have run yourself. Tell her before running anything
that rewrites thousands of files, including build.py. If you can't verify something,
say so plainly rather than guessing. Generated output that looks correct is not
evidence that it works — click the thing, measure the thing, request the URL.

**Captions and synopses are written from scratch. Never reword a platform's or IMDb's.**
