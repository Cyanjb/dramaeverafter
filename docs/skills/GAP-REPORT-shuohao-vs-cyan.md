# Gap report: shuohao-skills patterns vs. the Cy_AI skill stack

Read on 2026-09-18. Source: `github.com/eternityspring/shuohao-skills` @ main (novel-outline 1.2.0,
novel-characters 1.11.0, novel-art 1.2.0, novel-script 1.2.0, novel-storyboard 1.3.0) against the
42 skills in `~/.claude/skills/synced/`.

## What I ran

```
for f in skills/*/scripts/selftest.mjs; do node "$f"; done
```

All five pass, zero model calls, about one second total:

| Skill | Assertions | Gates covered |
|---|---|---|
| novel-art | 158 | 11 |
| novel-characters | 355 | (structural, no numbered gate set) |
| novel-outline | 249 | 14 |
| novel-script | 154 | 10 |
| novel-storyboard | 254 | 17 |

Every numbered gate has at least one breach case in the selftest. That is the whole argument of the
repo in one line: the rules are code, and there is a test proving each rule actually catches.

---

## The one structural difference

Everything else in this report follows from it.

**shuohao:** each stage produces a JSON artifact. The model writes only that JSON. Markdown and the
HTML review report are rendered from it. A validator reads it and returns pass/fail per named gate,
exits 1 on any failure. The next stage `seed`s from the previous artifact by script, so facts already
decided upstream are never re-reasoned by a model.

**Cy_AI stack:** each stage produces prose. The state of a project lives in chat scrollback and in
Craft documents. Rules live in the SKILL.md as checklists the model reads and is trusted to apply.
Nothing can be re-checked after an edit.

Two of your skills already break that pattern, which is the proof you build this way when the domain
forces you to:

- `ai-footage-recut` has `sheet.json` in integer frames, `cutsheet.py` validating it, and `qc.py`
  sweeping the rendered file. That is the shuohao architecture, arrived at independently, because a
  mid-frame boundary produces a black frame nobody catches by eye.
- `dramaeverafter-pipeline` has eight CSVs, a match queue that never auto-merges, and a generator
  that enforces the 5-title rule. Same shape.

The creative skills have the same failure mode as a mid-frame cut boundary. They just fail quietly,
so nobody built the checker.

---

## Pattern inventory

Twenty-one patterns worth naming. Column three is the honest cost, not a sales pitch.

| # | Pattern | What it buys | Cost |
|---|---|---|---|
| P1 | JSON artifact per stage; MD and HTML rendered from it | One authority per fact; re-render is free | You have to design a schema before you write |
| P2 | Every quality rule is a code gate with a stable `id`, `label`, `ok`, `detail` | Quality stops depending on the model's mood that day | Only textually decidable rules qualify |
| P3 | A breach case per gate in a selftest that calls no model | A skill edit cannot silently kill a rule | Writing the breach case is half the work |
| P4 | `seed <upstream.json>` carries settled facts forward deterministically | The model never re-decides who is important | Needs a stable id scheme (C01/S01/P01/B01) |
| P5 | Optional reconciliation flags (`--outline`, `--art`, `--cast`), and an unsupplied flag makes the gate print "skipped" | Cross-stage drift is caught; a skipped check never pretends to have run | Flag plumbing in every command |
| P6 | Two-round skeleton with a named human sign-off before the expensive stage | A wrong direction costs one skeleton, not 60 episodes | One forced stop in the flow |
| P7 | Stage-scoped validation (`--stage skeleton\|beats\|full`) | The gate set *is* the workflow gate | Deciding which gate belongs to which stage |
| P8 | Batch caps with a stated reason (10 eps outline, 3 eps script) | Prevents the back-half collapse in long generations | More round trips |
| P9 | `checkup` mode: paste an existing artifact, run gates only, render, never block | Turns the validator into a standalone product | Needs a lenient parse path |
| P10 | Resumability by file existence (`card-<slug>.json` exists, skip) | A failed item in a batch of 30 costs one retry | Naming discipline |
| P11 | Thresholds are `params`, some derived, never constants in code | A platform with different limits is a data edit | You must state each default's provenance |
| P12 | Language/role split enforced by the validator (human fields follow `lang`, machine fields always English; a non-builtin UI language must ship a `ui` block or validate errors) | No half-translated reports; TTS and image engines always get English | A dimension to carry through everything |
| P13 | `evidence` must be verbatim source text, never translated, trimmed or merged | Kills "hallucinating from the book title" | Requires the source file on disk at validate time |
| P14 | Pairwise distinctiveness gate: image and voice prompt word overlap >75% names the offending pair | Two similar characters stop coming out as one person | Threshold has to be measured on real samples |
| P15 | Character budgets with measured ceilings and the measurement written down (`voice.prompt` <= 400 chars; samples run 218-245, the rejected prose versions 490-514) | Numbers you can defend and revise | You have to actually measure |
| P16 | Verbatim derivation and reconciliation between structure and prompt (H3 alignment line and cut timestamps derived from cut durations; validate diffs the string character by character) | Change a duration, forget the prompt, the gate catches it | Only works where the derived string is deterministic |
| P17 | Optional mounted gate (`--shots <dir>` opens gate 17), and the mounted library's suggested shot sizes are *not* gated, only flagged | Optional things stay optional; "an optional mount that becomes strict is one nobody mounts" | Two strictness levels to maintain |
| P18 | Gate-failure log (`.gates.jsonl`) plus `stats`: which gate fires most (fix that rule's wording), which never fires (dead gate or internalised rule) | The rules improve from evidence, not vibes | Deliberately shipped on ONE skill only until proven |
| P19 | Self-containment: a skill must be copyable alone, no dependency on any third-party skill; external methodology is internalised into its own `references/` with the source named | Zero broken links | Duplication risk if applied to a federated stack |
| P20 | Every skill states its boundaries, and the boundary is gated (an outline synopsis containing a quotation mark means you are writing a script; validate blocks it) | Skills stop bleeding into each other | Writing the negative space |
| P21 | Sample data is the skill's own, doubles as test fixture and quality benchmark, never borrowed from a sibling | The example proves the skill, and breaking it breaks the test | One worked example per skill to maintain |

### Three rules in their `CLAUDE.md` worth stealing verbatim

1. **Story before storyboard.** Never write shots before the story is locked. Once the image is
   concrete ("a letter on the table, the father's hand holding it down"), every later "change the
   story" pass just re-motivates the same action, and three versions sound like one version.
2. **Each skill's sample data is its own.** A borrowed example is both a broken link and a
   demonstration of somebody else's genre.
3. **Do not propagate the gate log yet.** They ship `.gates.jsonl` on one skill on purpose, and say
   in writing that if nobody opens it in six months the feature was wrong and propagating it would
   copy the mistake five times.

---

## Where your stack sits against each pattern

| Pattern | Present in your stack? | Where |
|---|---|---|
| P1 artifact | Partly | `ai-footage-recut/sheet.json`, DEA CSVs, `screenwriter`'s `screenplay` array. Nowhere in the creative prompt skills |
| P2 code gates | No | Every checklist is prose the model reads |
| P3 selftest | No | Nothing anywhere |
| P4 seed | No | `production-bible-builder` carries stages forward with the instruction "read them first" |
| P5 reconciliation | No | Nothing checks shot 7's prompt against the character card |
| P6 sign-off gate | Soft | "Do not move to Stage 3 until the Story Bible is confirmed", with no named decisions |
| P7 stage scoping | Soft | 8 stages, strict order, no machine representation of "which stage am I in" |
| P8 batch caps | Partly | Sizing tables exist; nothing enforces them |
| P9 checkup | No | Big missed product: "here is my shot list, what is wrong with it" |
| P10 resumability | No | Resuming means re-asking |
| P11 params | No | 3500, 300-420, 9 images, 15s are all hardcoded in prose, and two of them have already drifted |
| P12 language split | No | Not needed yet, will be the moment you produce non-English dialogue |
| P13 verbatim evidence | No | n/a for original work, relevant for adaptation |
| P14 distinctiveness | No | Nothing stops two characters reading identically |
| P15 measured budgets | Partly | `seedance-locked`'s 300-420 words has no provenance sentence |
| P16 verbatim derivation | No | Nothing derives |
| P17 optional mount | No | n/a |
| P18 gate log | Better than theirs, differently | `video-prompt-director` Step 0: a Craft failure log with a write-back protocol and "never log a failure with no known fix". Manual, but the loop is right |
| P19 self-containment | Deliberately not | Your stack is a routed federation. See the note below |
| P20 boundaries | Partly | `ai-director` says "NOT for writing the final prompt". Three skills can still all claim "turn a brief into a sequence of shots" |
| P21 own samples | Partly | `poker-fish-prompts/example-blockers.md`, `commercial-pipeline/references/example-commercial.md` |

### Five things you do that they do not

Worth keeping and worth writing into the new skill.

1. **Failure log with a write-back protocol** (`video-prompt-director` Step 0). Read before writing,
   pre-apply matching fixes silently, offer to add a row after a fix is found, never log a failure
   with no known fix because that is a complaint not a log entry. shuohao has the machine version
   and not the human protocol.
2. **Opt-in consent register** (`credit-watch` Mode 0). Per-project on/off, asked once, written down
   so it is never asked twice. Nothing in shuohao asks permission for anything.
3. **Cost pre-flight.** `~X credits (~$Y / ~RZ) - balance N - N-X after` before generating, and the
   honest table of which platform can actually quote versus which is balance-delta only.
4. **Confidence grading on claims.** `EMPIRICAL`, `UNVERIFIED by Cyan`, "source: Higgsfield catalog
   snapshot 2026-08-07, re-verify if it matters". shuohao names its sources but does not grade them.
5. **The realism layer.** The imperfection budget (three to five named defects, each quantified and
   placed) and the causality rules are genuinely novel. shuohao has nothing like it.

### On self-containment

Do not copy P19 wholesale. Their stack is five sibling skills in one repo; yours is a federation
where `production-bible-builder` routes to `ai-director` routes to `video-prompt-director`. Copying
self-containment means duplicating the emotion library into five places.

Take the weaker, better rule instead: **one authority per fact, dependency allowed, duplication
forbidden.** You are already violating it once, see E3 below.

---

## Specific edits, by skill

Ordered within each skill by value. Effort is a rough half-day unit.

### `video-prompt-director`

**E1. Ship `scripts/check-prompt.mjs` and `scripts/selftest.mjs`.** (effort: 1)
The Standard-tier pre-delivery checklist is nine items and eight of them are decidable from the
prompt text alone: total character count against the engine ceiling, per-shot word count >= 20,
`SFX:` and `Music:` present on every shot, `Total:` footer present with a shot count matching the
shots actually written, no timestamps inside shot bodies, no banned anti-slop word, no age word, no
em dash, no "Pixar". Input is the prompt string, output is `id / label / ok / detail` per gate and
exit 1 on any failure. Add a breach case per gate. This is the cheapest high-value change in the
whole stack because the checklist already exists and is already precise.

**E2. Move engine limits into `references/engine-params.json`.** (effort: 0.5)
`{ "seedance-2.0": { "maxChars": 3500, "maxSeconds": 15, "maxImages": 9, "maxVideoRefs": 3,
"aspect": ["9:16","16:9","3:4","4:3","1:1","21:9"] }, "seedance-2.5": { "maxChars": null,
"maxSeconds": 30, "maxImages": 30, ... }, "kling-3.0": {...}, "veo-3.1": {...} }`, each row carrying
a `source` and `verifiedOn`. SKILL.md then references the file instead of restating the numbers. The
current patch note at the top of the skill ("the Seedance reference files were written against 2.0
and two of those limits have moved") is exactly the symptom this fixes: the numbers are scattered
across SKILL.md, `seedance.md` and `storyboard-to-video-workflow`, so a version bump means chasing
them. Their rule: thresholds are parameters, not scripture.

**E3. Delete the duplicated Emotion Direction Library.** (effort: 0.25)
It exists verbatim twice: `references/emotion-direction.md` and `references/seedance-locked.md`
lines 708 to 790, and a third partial copy in `ai-director` section 1.5. Keep one, point at it from
the other two. Two copies of anything drift; this is 80 lines of prose that will diverge on the next
edit and nobody will notice which is current.

**E4. Gate the Locked tier's eleven blocks.** (effort: 0.5)
The eleven labelled blocks in a fixed order are already a schema written as English. Four gates fall
out of it directly: (a) all eleven labels present, in order, none merged or renamed, (b) every
`@imageN` in the header bullet list appears at least once in the body and vice versa with matching
numbering, (c) the runtime in the title line equals the runtime in the Camera Capture line, (d) for
multi-shot prompts, the per-shot time ranges sum to the total. Those are four of the repair-pass
conditions the skill currently asks the model to notice about its own output.

**E5. Give the Craft failure log a machine mirror.** (effort: 0.5)
Keep Craft as the human surface. Append the same rows to `.generation-failures.jsonl` with
`{engine, asked, failed, fix, date}` and add a `stats` command answering their three questions:
which failure recurs most (that is a rule whose wording needs fixing), which logged fix has never
been needed again (that rule is internalised, consider deleting it), what is recurring with no known
fix (that is the next thing to investigate).

**E6. Put a provenance sentence on the density rule.** (effort: 0.1)
`seedance-locked` says "target prompt length is 300 to 420 words" with no source. Either state what
it was measured against or mark it a working assumption. shuohao writes the measurement next to the
number every time (400 chars because samples run 218-245 and the rejected prose versions 490-514),
which is what makes the number revisable by somebody other than the author.

### `ai-director`

**E7. Give the Emotion Card a schema.** (effort: 1)
`{ "scene": "...", "surface": "...", "true": "...", "intensity": 7, "arcPosition": "build",
"audienceFeel": "..." }` plus the arc as an array. Three gates: every scene has a card; card
intensity sits inside the band its `arcPosition` allows per the section 1.2 table (a 10 in `setup`
is an error, not a style choice); exactly one `turn` per film. This is the highest-value artifact in
your whole stack, because every downstream skill is instructed to trace its choices back to the
Emotion Card and nothing checks the trace.

**E8. Make "no shot without its emotional reason" a claim, not a promise.** (effort: 0.5)
This is shuohao's 认领 (claim) pattern, which is the mechanism behind their strongest gate. Each
shot-list row carries `emotionCardRef`; two gates follow: every card is claimed by at least one shot
(an unclaimed card is a scene with no coverage), every shot claims a card that exists. Hard Rule 1
currently says the same thing and is enforced by hope.

**E9. Move the section 7 worked micro-example into `examples/`** as the machine-readable fixture the
selftest runs against. (effort: 0.25)

### `production-bible-builder`

**E10. Add `bible.json` beside the six Craft documents.** (effort: 1.5)
Craft keeps the prose a human reads. The JSON holds only what a machine needs: `format`, `stage`,
`characters[].{id, name, cardLocked, refImages[]}`, `locations[].{id, lightingLogic, neverAppears[]}`,
`styleFormula` (one string, verbatim), `forbiddenList[]`, `shots[]`. Then `validate --stage
story|characters|settings|elements|shots` is the strict build order, enforced. Right now "don't skip
stages, don't combine stages" is a request.

**E11. Replace the paste-forward handoffs with `seed`.** (effort: 0.5)
Stage 2 currently says "paste both into the Story Bible document once locked". Stage 3 says "paste
the resulting character sheet images/prompts into the Characters document". Those are manual copies,
which is where fields get dropped. `seed <ai-director.json> > bible.json` moves the settled facts by
script and leaves blank exactly what this stage is supposed to decide.

**E12. Name the sign-off decisions.** (effort: 0.25)
shuohao stops after the fast skeleton and puts three specific questions to the user: which storyline
got cut, which characters got merged, which episode the big payoff lands in. "Do not move to Stage 3
until the Story Bible is confirmed" does not tell the user what they are confirming. Name three:
logline, format, where the Turn lands.

**E13. Make "resuming an in-progress project" a read, not a question.** (effort: 0.1)
`bible.json.stage` is the status line the skill currently hopes somebody wrote into Production Notes.

### `cinematic-shotlist-director`

**E14. The SHOT RECORD block is already a schema. Make it JSON with the same field names.** (effort: 1)
Then the six questions under Quality Gate become gates. Two of them are genuinely mechanical and
worth the whole change on their own: (a) every transition names a physical mechanism, where "names a
mechanism" means the field is non-empty and not a member of the banned set `{"seamlessly
transitions", "dissolve to", "cuts to"}` (the skill already says "do not call something a transition
merely because the prompt says seamlessly transitions" and then has no way to catch it), and (b)
`shots[n].endFrame == shots[n+1].startFrame` as string equality, which is shuohao's verbatim
reconciliation trick applied to your edit points. Also: editorial duration inside the band the skill
declares for that shot's type.

**E15. Settle the boundary with two neighbours.** (effort: 0.25)
`cinematic-shotlist-director`, `storyboard-to-video-workflow` and `video-prompt-director` can all
currently claim "turn a brief into a sequence of shots". Write the negative space into each
description the way `ai-director` already does ("NOT for writing the final Seedance/Higgsfield
prompt"). That one line is why `ai-director` routes cleanly and these three do not.

### `storyboard-to-video-workflow`

**E16. Move the sizing table to `references/sizing.json` and gate it.** (effort: 0.5)
Three gates: the announced panel count matches the table for the chosen length and format, the grid
layout matches the panel count, and `seedanceShots <= storyboardPanels`. The skill states that last
rule in prose ("the Seedance shot count is always less than or equal to the storyboard panel count")
and nothing checks it.

**E17. Gate the six-act arc.** (effort: 0.25)
Every act 1 through 6 has at least one panel; the end card exists for `ad` and `walkthrough`, which
the skill already calls mandatory.

**E18. Keep the honesty section and copy the pattern.** (effort: 0)
"What the storyboard sheet actually does in Seedance" (it is a style and character bible, not N
keyframes; each panel is low resolution inside the sheet) is the single best paragraph in your stack.
It is what shuohao calls 边界. Add the equivalent paragraph to `video-prompter`, `commercial-pipeline`
and the new drama skill.

### `screenwriter`

This is the closest analogue to `novel-script` and has the widest gap.

**E19. `scripts/timing.mjs`.** (effort: 1)
`timing-and-cutting.md` is a careful estimation method a human runs by hand, with real numbers in it
(2.5 words per second of dialogue, 1-2s simple action, 3-5s complex action, 5-10s big physical
event, 3-5s minimum for a long pause, 2-3s per reaction shot). shuohao computes the same thing:
dialogue seconds from character count over a configurable rate, action seconds from beat count, gate
at target +/- 15%. You already have the data structure: `build_screenplay.js` consumes a `screenplay`
array of `slug` / `action` / `character` / `dial` / `trans` entries. Point `timing.mjs` at the same
array and you get the whole timing method as code with no new data model.

**E20. Gate the same array.** (effort: 0.5)
Directly portable from `novel-script`: speaker must be in the scene's character list or marked VO;
an `action` entry containing quotation marks is dialogue smuggled into action and breaks both the
timing calculation and any TTS handoff; every scene has at least one action beat. Then the causality
audit tags (⚠ ПРИЧИННОСТЬ / ЦЕННОСТЬ / БИБЛИЯ / ТЕМП) become fields rather than annotations, and
"which scenes are flagged" becomes a query.

**E21. Decide the language question.** (effort: 0.25)
The skill, its description and all five reference files are in Russian while the rest of the stack is
English. If it is a deliberately separate tool for a Russian-language client, say so in the first
line of the description so the router and any future reader can tell. If it is not, it is the only
skill a model cannot compare against its neighbours.

**E22. State or remove the dependency.** (effort: 0.25)
`README.md` tells the user to run `NODE_PATH=/usr/local/lib/node_modules_global/lib/node_modules node
my_scene.js`. That is a machine-specific path and an npm dependency (`docx`). shuohao's rule is
standard library only, zero npm, so the script runs wherever the skill is copied. Either vendor the
generator, or declare the requirement in frontmatter the way they do (`metadata.requires.bins`).

### `poker-fish-prompts`

**E23. This is the best pilot in your stack. Do it first.** (effort: 1)
It has more gate-shaped rules than anything else you own, and they are integer invariants, not
judgment calls: community card count locked to street (flop 3, turn 4, river 5), chip stack must
match the spoken action, hole card count persistence across panels, showdown card count per
character, card visibility rules. `client-feedback-log.md` shows these are the failures actually
happening. Add `scene.json`:

```json
{ "street": "turn",
  "board": ["Ah","Kd","7c","2s"],
  "pot": 480,
  "players": [ { "id": "shark", "stack": 1200, "hole": 2, "action": "raise", "amount": 300 } ] }
```

and a validator: `board.length == streetCardCount[street]`, every player's `hole` is 2 until they
fold, a raise amount exceeds the current bet, stacks reconcile against the pot across panels.
Roughly 120 lines and it removes the class of error the client keeps flagging.

**E24. Ask the stats question of `client-feedback-log.md`.** (effort: 0.1)
It is already the human version of `.gates.jsonl`. Add one line at the top: which rule does the
client flag most often, because that is the rule whose wording in this skill is failing.

### `ai-footage-recut`

**E25. Cheapest complete win in the stack, about 60 lines.** (effort: 0.5)
It already has the architecture. Two pieces missing: `cutsheet.build()` returns a `problems` list of
free-text strings with no stable ids, and there is no selftest. Give each check an id, and write a
breach case per check (durations that do not sum to runtime, a zero-frame shot, a black frame in the
sweep, a crop below the sharpness floor). `qc.py`'s checks are harder to unit test because they need
a file; generate a two-second synthetic clip in the test rather than skipping them.

### `credit-watch`

**E26. Best-designed skill you have. One edit.** (effort: 0.25)
The Runway rate table is prose. Make it `references/rates.json` with a `verifiedOn` per row, so a
price change is a data edit and a stale rate is visible. The skill already does exactly this for the
Higgsfield catalog snapshot ("source: Higgsfield platform catalog snapshot 2026-08-07, re-verify if
it matters, since the surface moves"). Apply that discipline to every number in the file.

### `cy-design-values`

**E27. It is already shuohao-shaped. Add the checker.** (effort: 0.5)
`DESIGN.md` is the artifact, "this file holds no brand values, never restate them here, never invent
a hex" is the one-authority rule stated better than shuohao states it, and Step 0 stops dead if the
file is missing. The only missing piece is the gate: a script that reads `DESIGN.md` and greps the
built CSS for any hex, font family or spacing value not declared in it. Without it, Step 0 protects
the start of a build and nothing protects the end.

### `skill-creator`

**E28. Add the cheap tier below the eval loop.** (effort: 0.25)
Its eval loop is the model-based equivalent of a selftest: accurate, slow, expensive. Add a rule that
any skill shipping a validator must have its `selftest` pass before an eval run is spawned. Free,
instant, and it catches the regressions that evals currently spend tokens rediscovering.

### `no-ai-slop`, `hook-generator`, `cy-ai-content-writing`, `video-prompt-director`, `storyboard-to-video-workflow`, `poker-fish-prompts`

**E29. One ban list, not four.** (effort: 0.5)
There are at least four separate anti-slop word lists in the stack: `no-ai-slop`'s "words to cut",
`video-prompt-director`'s anti-slop list, `storyboard-to-video-workflow`'s inline list, and the
per-format lists inside `video-prompter`. They already disagree (only some carry "elevate", only some
carry "unleash"). Put them in one `banlist.json` with categories (`generic-slop`, `video-prompt-
degrading`, `age-words`, `style-breaking`) and have every skill read it. This is the same argument as
E3: one authority per fact. It is also the enforcement primitive E1 needs.

---

## Do not copy

- **The per-skill HTML report generator.** Each is 1000+ lines of inlined CSS, and it pays off
  because their deliverable is a review document an industry reader opens to decide whether to green-
  light a production. Your review surface is Craft. Take the gate panel idea (pass/fail burned into
  the page at render time, a lesion banner listing failures, never model self-assessment) and skip
  the report.
- **The gate log on everything.** Their own CLAUDE.md says do not propagate it until it has proven
  itself on one skill, and says explicitly that if nobody opens it the feature was wrong and
  propagating would copy the mistake five times. Put it on one skill, the one with the most gates.
- **Chinese-first output and the single-character-word style rule.** Obviously local.
- **Strict self-containment.** See the note above. Your stack is a federation by design.

---

## Priority order

**Tier 1, this week, high ratio.**
E23 poker scene validator (the rules are unambiguous and the failures are live) ·
E25 ai-footage-recut selftest (60 lines, architecture already there) ·
E29 one ban list ·
E2 engine-params.json ·
E3 emotion library dedupe.

**Tier 2, the real leverage.**
E1 prompt checker and selftest for video-prompt-director ·
E4 locked-tier block gates ·
E19 screenwriter timing.mjs ·
E16 sizing gates.

**Tier 3, the architecture.**
E7 and E8 Emotion Card as artifact with claim gates ·
E10 through E13 bible.json and stage validation ·
E14 shot record as JSON.

**Tier 4.** Everything else.

A reasonable test of whether this is worth doing: pick E23, spend a day, then count how many client
revision rounds the next poker batch takes against the last one. If the number does not move, stop
here and keep the prose.
