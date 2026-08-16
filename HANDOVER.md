# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)** — the top CURRENT STATE block is
   dated 16 August and describes exactly this tree. Everything below it is history.
2. **7. DEA TASKS (what needs Cyan)** — her list, not your work queue.

Then in the repo: `generator/caption_pipeline.py`'s docstring, and
`references/adapters.md` sections 24–26.

## STATE: pushed, clean, and live.

`main = origin/main = 859a24ded`, working tree clean. Run
`git rev-list --left-right --count origin/main...HEAD` before trusting that.

**Netlify auto-deploys on push.** This is a change from older notes that say
publishing is paused and needs Cyan's button. It isn't. A push goes live in about
a minute, verified many times on 15–16 Aug. So *push is publish* — no separate
deploy step, and no unpushed work sitting safe.

Save point outside the repo:
`C:\Users\cyanj\DramaEverAfter-backups\dea-savepoint-2026-08-16.zip`
(21 entries, integrity tested: the data CSVs, all four caption batch files, the
three pipeline scripts, and the gitignored quarantine file). **Cyan still needs to
copy it off this machine** — the quarantine file exists nowhere else.

    3,513 titles · 126 captions written by us (was 60 on 15 Aug)
    All 34 homepage titles now carry a caption we wrote

## THE JOB RIGHT NOW: captions, to the top 300.

**The target is not 3,513.** Measured: top 100 titles carry **49.6%** of all
views, top 300 carry **82.8%**, top 600 carry **98.4%**. Cyan, 16 Aug: *"Let's
complete the 300 manually, the rest you can just do without manual checking."*
So the top 300 get her eye; past that the audit is the only gate.

**Where it stands.** Batch one (45) and the homepage 21 are done, approved and
live. Batch two is `generator/staging/captions_2026_08_16_r45.py`: **15 written,
30 blank, and all 45 synopses already fetched into its FACTS block** — the slow
half is done. Roughly **130 more captions** to reach 300.

## THE PIPELINE — four commands, in this order, every batch

```
py generator/caption_pipeline.py next 45 --offset N   # batch ranked by reach
py generator/caption_pipeline.py check <file>         # every rule
py generator/readback.py <file>                       # MANDATORY, see below
py generator/caption_pipeline.py apply <file>         # writes to data
py generator/build.py                                 # then commit and push
```

**`readback.py` is not optional.** Cyan, 16 Aug: *"The last thing you do before
you move on from a caption is read your result, then read its source, to make sure
the information is accurate."* The automated guard only compares proper nouns; it
cannot tell whether a claim is TRUE. Its first run caught three of mine that had
passed every check: "he **fired** the woman" when the source said *dumps*, "she
**wakes up** looking like someone else" when no overnight change is described, and
"her best friend **long before** he was her first love" inventing an order of
events.

**`py generator/audit_captions.py` every 100 captions.** It measures the corpus
against *itself* — repeated phrases, hook openings, near-duplicate bodies, crutch
constructions — because the failure mode of unsupervised writing is sameness, not
one bad caption. It already found drift in my own work: *turns out to be* ×4,
*she has no idea* ×4, *what he/she does not know* ×4, five hooks opening *He is*.

**Approved is separate from draft.** Only `captions_approved_*.py` is ever
applied. This exists because Cyan's sign-off on the number-one title sat unapplied
for hours, stranded behind unreviewed drafts in the same file.

**SOURCES sits beside FACTS** in every batch: `title_id -> (kind, where)`, kind
being `platform` / `pdf` / `quarantine` / `fansite` / `imdb`. They are not equally
trustworthy and `check` warns on fan-site ones.

## THE CAPTION VOICE — settled, do not re-derive it

Full spec is a standing rule in READ FIRST. The shape is **HOOK newline BODY**.
The hook renders as a subheading. **There is no third line** — the aside was
removed on 15 Aug because it caused more problems than it solved, though
`build.py` still renders one if a third part ever appears.

Hard rules: **no dashes of any kind, hyphens included.** Bodies are **third
person, present tense**, past only for events before the story opens. **Use "but"
to land an ending** — Cyan rewrote four of mine and every one replaced a full stop
with a "but". Heavy material drops the playfulness entirely. Never state the turn;
set up the situation and stop.

**Accuracy outranks everything, including length.** If the substance isn't there,
drop the count. A title with no findable synopsis goes on a list for her — never a
guess.

## TRAPS THAT COST TIME TODAY

**`apply` silently skips captions already ours** unless given `--update-ours`. That
default protects approved work but blocked a correction to the live number-one page
for hours. If a fix won't land, that is why.

**Edits made only in the approved file get eaten.** `promote.py` rebuilds it *from
the draft*, so Cyan's "stay that way" edit was discarded because the draft still
said "stay that simple". Apply her wording to **both** files.

**Almost every stored synopsis is a truncated first sentence**, not a short one. Of
45 titles in batch two, all 45 held less than the platform publishes. This produced
a caption for *Carrying His Triplets* containing no male lead, no pregnancy and no
romance. **Treat thin facts as no facts and go and read the page.**

**The fetch route works on every platform**, not just ReelShort — proven on
my-drama.com, vigloo.com, candyjar.com, dramaboxdb.com and netshort.com.
reelshort.com is blocked in the Browser pane but fine via WebFetch.

**Do not trust a regex over reading the text.** Two of my own measurements were
wrong that way: a `\w+ed` tense test reported 8 of 30 bodies drifting when the real
number was 2, and a page-existence test reported 37 redirects were needed when the
answer was zero.

## WAITING ON CYAN

- **One caption line.** *Cancel the Wedding, Queen Moves On* is live with her
  wording, "takes back control of everything **she gave him**". The source says
  only that she confronts betrayal and is determined to take control. Flagged, not
  changed.
- **Copy the save-point zip off this machine.**
- **638 titles have no trope** — '7. DEA TROPES WANTED', top 60 tickable.
- The older items: the DramaBox singular/plural ruling, the 14 fused people.csv
  rows, IMDb pages for ACTORS-FILMOGRAPHY.md, the two Drive lookup sheets.

## HOW CYAN WORKS

Run lookups yourself; never hand her one you could run. Show a whole batch on one
page, never in dribs — feeding her six at a time was a real failure and she said
so. Read every caption back cold, as someone who knows nothing about the show,
before she sees it. Tell her before anything rewrites thousands of files. And
generated output that looks correct is not evidence that it works: click the thing,
measure the thing, request the URL.
