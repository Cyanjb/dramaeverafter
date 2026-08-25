# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. **This file is the current truth, dated
24 Aug 2026.** The Craft doc '7. DEA READ FIRST' still shows the 16 Aug state —
the Craft connector was down when this session closed, so it was NOT updated.
Its standing rules and traps remain valid; its CURRENT STATE block is stale.
Update Craft from this file when the connector is back.

Then in the repo: `generator/caption_pipeline.py`'s docstring (it changed a lot
this week), and `references/adapters.md` sections 24–26.

## STATE: pushed, clean, and live.

`main = origin/main = 6d934d704` (plus possibly a handover commit after it),
working tree clean. Run `git rev-list --left-right --count origin/main...HEAD`
before trusting that. Netlify auto-deploys on push, verified again 24 Aug —
push is publish.

    3,513 titles · 215 captions ours (was 126) · top 300: 171 covered
    ALL of these have Cyan's review: 68 hold her line edits verbatim,
    the rest are read-approved. Her rule: READ MEANS DONE.

**What shipped 24 Aug (commit 6d934d704):** batch two (44) and batch three (45)
went from platform text to our captions; the original 60 thin captions from
14 Aug were replaced wholesale, rewritten from freshly fetched platform pages.
The front page is fully rewritten. Live-verified by curl after deploy:
blood-and-bones, country-gal, ceo-s-twins, kidnapped-by-the-devil all serve the
new text.

## THERE IS NOW A SKILL FOR ALL OF THIS

`/dea-captions` — a user-level skill at
`C:\Users\cyanj\.claude\skills\dea-captions\SKILL.md`, created 24 Aug at Cyan's
request. It carries the whole workflow (select, fetch-first, write, check,
readback, shadow audit, her review page, apply, build, push, verify live), the
condensed voice rules, and the environment traps. Invoke it for ANY caption
work rather than re-deriving the process from this file. The calibration
section below stays as the deeper record; the memory dea-caption-voice.md has
the full detail with her quotes. NOTE: the skill file lives OUTSIDE the repo
(user level) because .claude/ is gitignored here — the repo root is the Netlify
publish dir. It is on this machine only; if it matters, it belongs in the same
off-machine backup as the save-point zip.

## THE CALIBRATION THAT COST A WEEK — read this before writing ANY caption

The session memory (dea-caption-voice.md) has the full detail. The four rulings
Cyan spent 20–24 Aug hammering in, each after finding the fault herself:

1. **Restructure, never synonym-swap.** Writing each source sentence as a
   "changed enough" copy is reworded platform text with extra steps. Facts are
   the constraint, structure is free. An occasional verbatim source sentence is
   FINE ("a sentence here and there left the same is fine rather than a
   sentence that makes no sense"). Measure it: difflib word-ratio of body vs
   source; shadowing shows at 0.55+, honest restructures sit 0.15–0.35.
2. **Genre vocabulary is kept verbatim** — flash marriage, contract marriage,
   fated mates, age gap, silver fox, CEO. Enforced in check() (GENRE_TERMS)
   except CEO, which is judgement (her own janitor edit avoids it).
3. **Count caps are REMOVED, permanently.** Her words: "just remove these word
   caps". The floor was making captions cram source clauses in. Length is
   writer's judgement. The suspended checks are documented in validate().
4. **Contractions are the default fan register** — the observed failure was
   under-use, not over-use. Full forms only where a line wants weight.
   Endings must LAND: a but-turn, a question, a tease, or a punch.

**The pipeline gates all still apply**: check → readback (mandatory, catches
what the noun-guard cannot) → apply from an approved file only → build → push.
`audit_captions.py` every 100. The hook/body boundary now counts as a sentence
break in the noun guard (hooks may lack a full stop — hers do).

## THE JOB NEXT: 129 captions to finish the top 300

171 of 300 covered. Next unwritten title sits at 67.4M reach. The fetch-first
routine is proven: `next` emits the batch, fetch every synopsis from the
platform's own page (WebFetch; reelshort.com blocked in Browser pane but fine
via WebFetch), write, check, readback, review page for Cyan, apply, build, push.

**Review pages** (claude.ai artifacts, hers, private): the 89-batch page and the
rewrite-60 page both have per-caption edit boxes with a "Collect my edits"
button that outputs paste-ready blocks. This is the review format that finally
worked — whole batch on one page, editable in place. Rebuild the generators
from scratchpad if needed; they're session-local, the staging files in
generator/staging/ are the record.

## OPEN ITEMS, verified this session

- **GoodShort trope soup — the second half of Cyan's original complaint, not
  started.** Measured 21 Aug: GoodShort titles average 17.4 tropes vs 3.2 for
  every other platform; 1,491 titles carry 15+, all GoodShort. Wrong tropes
  leak onto browse pages (blood-and-bones sits on /tropes/vampire, /luna,
  /devil with none of those in the show). The 14 Aug cleanup halved it and
  stopped; it needs a second, GoodShort-scoped cut to ~3–5 per title. Cyan
  has seen the numbers and said "first the captions" — captions are done, so
  this is next when she says go.
- ~~Mic Drop Diva~~ **RESOLVED 24 Aug: Cyan ruled the live caption stays.**
  The superseded batch-two duplicate is annotated in the approved b2 file with
  a warning never to apply that file with --update-ours.
- **ReelShort 1-episode anomaly, now FOUR titles**: the-senator-s-son,
  shhh-professor-please-don-t-tell, summer-situationship, outplayed. Pattern,
  not page errors. On her list.
- **Scandalous / Vicious carry no author credit** on their ReelShort pages
  (both "ReelShort original production") — evidence for her open L.J. Shen
  question, not an answer. Note ReelShort DOES credit authors where a book
  exists (Gemma James, Cricket Colson — both credits are live in our captions).
- **Save-point zip still needs copying off this machine**:
  `C:\Users\cyanj\DramaEverAfter-backups\dea-savepoint-2026-08-16.zip` — the
  gitignored quarantine file exists nowhere else. Standing reminder to Cyan.
- Older Cyan-only items unchanged: 638 no-trope titles, DramaBox
  singular/plural ruling, 14 fused people.csv rows, IMDb pages for the
  filmography queue, the two Drive lookup sheets.

## TRAPS ADDED THIS WEEK (append to Craft when it's back)

- Another session pushed to main mid-session on 16 Aug and swept up uncommitted
  work. fetch + rev-list before trusting any state claim, and before build/push.
- `caption_pipeline.py next` names output by date+offset: running it twice the
  same day with a matching offset SILENTLY OVERWRITES the earlier batch file.
  Generate to an explicit filename instead.
- This Bash tool mangles backslashes in heredocs (a `\\n` became a real newline
  inside a Python source file; regexes lose escapes). Write scripts to a file
  with the Write tool and run the file. This bit three separate times.
- Editing a caption in only one of generator-script/staging-file loses the edit
  when the other regenerates. One file is the record (staging); retire spent
  generators with a SPENT header immediately.
- Cyan's collect-box resends entries whose stored edit differs from the applied
  text by mechanical fixes. The repeats are not re-assertions of the typos.

## HOW CYAN WORKS (unchanged, plus this week's additions)

Whole batch on one page, editable in place. Read means done. Her wording goes
in verbatim; mechanical typo fixes are applied but LISTED individually for
veto. When she asks "what is causing it", she wants the mechanism named
honestly, not reassurance — and the fix encoded so she never repeats the
correction. Run lookups yourself. Tell her before anything rewrites thousands
of files. Generated output that looks correct is not evidence: curl the live
page.
