---
name: dea-captions
description: Write, review, and ship DramaEverAfter captions end to end - batch selection by reach, fetch-first facts, Cyan's calibrated voice, the check/readback gates, her one-page review artifact, and the apply/build/push ship. Trigger on "write captions", "next caption batch", "caption the top 300", "continue the captions", "DEA captions", or any request to write or fix synopses/captions for dramaeverafter.com. Do NOT trigger for database scraping or site structure work (use dramaeverafter-pipeline) or general DEA strategy questions.
---

# DramaEverAfter captions

**THE GOAL IS AUTONOMY.** Cyan, 24 Aug 2026: "I need you to get to the point
where you can write these captions on your own so consider corrections and my
updates to text as training." Cyan, 2 Sep 2026: "I need to get to a point
where I can trust you to do the captions on your own."

**WRITE TO HER EXEMPLARS, NOT TO THE RULEBOOK** (settled 2 Sep 2026 after
measuring her batch-two edits word by word). The model for every caption is
the "Write like these" block at the end of `generator/CAPTION-TRAINING.md`:
her final wording, verbatim. Read it before writing. Match its register:
plain, warm, present tense, short sentences, contractions where they fall
naturally, one landing line. The rules further down are for the CHECKER; a
writer following forty rules produces exactly the stiff, over-written prose
she keeps deflating ("the two of them" became "they" three times in one
batch). If a sentence sounds clever, make it plainer.

**THE METRIC IS WORDS CHANGED, NOT CAPTIONS TOUCHED.** She edits by instinct,
so "touched or not" can never reach 10% and reported failure for a month
while the real number was already close. After every review report two
numbers: the share of words she changed across the batch (batch two: 11%,
target under 10%), and her minutes on the page. Then diff her edits, classify
them against the lesson classes, and add a lesson only when the same pattern
shows in TWO separate edits.

Repo: `C:\Users\cyanj\DramaEverAfter`. The deep sources, in order: this file for
the workflow, `generator/CAPTION-TRAINING.md` for her training pairs,
`generator/caption_pipeline.py`'s docstring and comments for the
enforced rules and their history, the auto-memory `dea-caption-voice.md` for the
full voice calibration with Cyan's quotes, and HANDOVER.md for current state.
The canon corpus is whatever is live in `data/titles.csv` (captions contain a
newline; platform text does not) — read ten before writing any.

## The shape

Every caption is `HOOK\nBODY` stored in `synopsis_short`. The hook renders as a
subheading. No third line. Hooks may skip the terminal full stop (hers do).

## The workflow, every batch

1. **Select by reach.** `py generator/caption_pipeline.py next 45 --offset N`
   emits a ranked batch. TRAP: the filename is date+offset — running it twice
   the same day silently overwrites the earlier file. Generate to an explicit
   filename if in doubt. The goal is the top 300 by views, not all 3,513.
2. **Fetch every fact source fresh.** Stored synopses are almost always
   truncated first sentences. Read each title's OWN platform page (WebFetch;
   reelshort.com is blocked in the Browser pane but fine via WebFetch; the
   route works on goodshort, my-drama, vigloo, candyjar, dramaboxdb, netshort).
   FROM A CLOUD SESSION, which cannot reach any platform, run the
   `fetch-synopses` GitHub Actions workflow instead (Actions tab, or the
   GitHub MCP `actions_run_trigger` with the branch as ref); it commits
   `generator/staging/facts_<date>.json` to the branch, one entry per title
   with text, route, url and episode count. Store the text in the batch's
   FACTS dict with episode counts, and record SOURCES as
   `tid -> ('platform', url)`. A title with no findable synopsis goes on a
   list for Cyan — NEVER a guess.
3. **Write** to the exemplars (see the top of this file). Close the source
   before writing. Then read each draft once as her: anything she would
   deflate, deflate first.
4. **Gate:** `py generator/caption_pipeline.py check <file>` must pass 100%.
   It also prints WARN lines for her known deflation patterns; a caption with
   two or more warnings is over-written and gets rewritten plainer before she
   sees it.
5. **Read back, mandatory:** `py generator/readback.py <file>` — read each
   caption cold against its source. The noun guard cannot tell whether a claim
   is TRUE; this step is what catches "he fired her" when the source says
   "dumps her". Expect to find several; that is the step working.
6. **Drift audit:** repeated 4-word phrases across the batch (nothing 3+), hook
   openings, crutch phrases. The shadow metric (difflib word-ratio of body vs
   source) is now a COPY DETECTOR ONLY: 0.6 and above means the source was
   copied and the caption is rewritten. Below that, resemblance is not a
   fault. Plain blurb register is what she wants, and forcing distance from
   the source is where the syntax knots came from ("the woman's grandson is
   how she meets Austin"). `py generator/audit_captions.py` every 100 applied.
7. **Review page for Cyan:** ONE artifact page, whole batch, ranked by reach,
   each entry showing hook+body as it will render, the source one tap away, an
   edit box (textarea prefilled, saved to localStorage, "Collect my edits"
   button emitting `[tid]\ntext` blocks), a read tick. Page generators from a
   past session live in that session's scratchpad; rebuild freely — the
   staging file is the record, the page is a view. Whole batch on one page,
   never in dribs. HER RULE: READ MEANS DONE — a reviewed, unedited caption is
   approved.
8. **Apply her edits verbatim.** Fix only mechanical typos and LIST each fix
   individually for veto. Apply to the staging file (the single record); mark
   any generator script SPENT immediately so it cannot regenerate over her
   wording. Genuinely garbled lines: flag, propose minimal fix, never guess
   silently.
9. **Ship:** copy the staging file to `captions_approved_*.py` with a header
   recording the approval basis (only approved files are ever applied), then
   `apply` (add `--update-ours` ONLY when replacing our own live captions —
   without it those are silently skipped; with it, check no earlier-approved
   caption gets clobbered), then `py generator/build.py` (~9,456 pages; nothing
   may be reading the output tree on Windows or the build dies mid-unlink),
   commit, push. **Push is publish** (Netlify auto-deploys in ~1 min). Then
   VERIFY LIVE: curl 3–4 changed pages on dramaeverafter.com and grep for the
   new hooks. Generated output that looks correct is not evidence.

## The voice (full detail with quotes: memory `dea-caption-voice.md`)

Warm + bestie, fun but never ditzy. Third person, present tense; past only for
events before the story opens. The site speaks as "us", never "I".

- **Facts are the constraint.** Tell the story plainly in your own words and
  your own order; do not copy the source, and do not contort a sentence to
  get away from it either. An occasional genuinely good source sentence kept
  verbatim is FINE. Never invent events, names, motives, or "how" when the
  source only gives "that": "bodies behind him" for "murderous" and "the work
  is factory work" for "a job" were both cut by her.
- **Plain beats clever.** Her most frequent edit. "They" not "the two of
  them"; "talk" not "a conversation"; "that whole family" not "the Evans of
  this world"; "just around the corner" not "almost on top of her". The extra
  word that adds information usually subtracts punch.
- **Her landing lines**: "Wait until they find out." / "Little does she know
  that…" / "But why?" / a plain "But…" turn. Tease the story, never narrate
  the audience ("deeply satisfying" and "Which would you choose?" were cut).
- **Genre vocabulary verbatim**: flash marriage, contract marriage, fated
  mates, age gap, silver fox, second chance, CEO. check() enforces most; CEO
  is judgement but the default is keep.
- **Contractions are the default fan register**; full forms only where a line
  wants weight or the material is heavy.
- **Endings must land**: a "but" turn, a question, a tease ("Wait until they
  find out."), or a punch ("Whatever it takes."). Never trail off on
  description. The spoiler rule means don't REVEAL the turn — it never meant
  don't have an ending.
- **No count caps.** Removed permanently by Cyan 24 Aug. Length is judgement.
- Hard bans: dashes of any kind (rephrase compounds), exclamation marks,
  4+ letter caps runs (write "Navy lieutenant", not the acronym), analytical
  verdicts ("done properly", "is the whole appeal"), "love me some".
- Heavy material (grief, trafficking, dying children) drops the playfulness.
- Ellipsis: single … character only (three dots read as sentence marks).
- Straight apostrophes throughout, never curly.

## Working with Cyan

Her wording beats every rule and every protected hook. When she asks what is
causing a fault, name the mechanism honestly and encode the fix so she never
repeats the correction. Any new session or model writes FIVE and shows her
before batching. Tell her before anything rewrites thousands of files.

## Environment traps

- This machine's Bash tool mangles backslashes in heredocs (real newlines
  appear inside string literals). Write scripts with the Write tool, run the
  file. Set PYTHONIOENCODING=utf-8.
- Another session may push to main mid-session. `git fetch` + rev-list before
  trusting state, before build, and before push.
- Mic Drop Diva: two approved captions exist; Cyan ruled 24 Aug the LIVE one
  stays. Do not "fix" it.

<!-- BACKUP COPY, committed 24 Aug 2026. The LIVE skill Claude Code loads is
C:\Users\cyanj\.claude\skills\dea-captions\SKILL.md (user level, outside the
repo because .claude/ is the gitignored Netlify publish root). If that machine
copy is lost or a new machine is set up, restore it from this file. A session
that edits the live skill should refresh this backup in the same commit. -->
