# Spec: `vertical-drama`

A production skill for vertical micro-drama, built for Seedance (via Higgsfield), Runway, and Craft.
English throughout. No code yet: this document is the thing to argue with before anything gets built.

---

## 1. What it is

One skill that takes a story from whatever state it arrives in to a set of paste-ready generation
prompts, keeping every stage machine-checkable so a change upstream reports what it broke downstream.

It has a three-way front door and a single shared spine. The front door is the only branching part.

```
        ROUTE A                  ROUTE B                  ROUTE C
   existing story           premise only            existing outline
   (novel, script,          (one line,              (theirs or yours,
    treatment, text)         nothing else)           any format)
        |                        |                        |
     extract                  generate                  parse
        |                        |                        |
        +------------------------+------------------------+
                                 |
                          series.json
                     (must pass --stage skeleton)
                                 |
                  ROUTE C stops here with a diagnosis
                  unless the user says continue
                                 |
   1 SERIES SKELETON  ->  sign-off gate (3 named decisions)
   2 EPISODE BREAKDOWN
   3 CAST           -> hands off to banana-pro-director-20
   4 WORLD          -> hands off to banana-pro-director-20
   5 SCRIPT
   6 SHOT PLAN
   7 PROMPT PACK    -> emits per engine
   8 GENERATE + QC  -> credit-watch, Higgsfield/Runway MCP, failure log
```

## 2. Boundaries

Written first, on purpose, and enforced by gates where possible.

**It does:** series structure, payoff cadence, per-episode breakdown, character and location asset
registers, timed script with a beat flow, shot plan quantised to what the engine can generate in one
call, and the emission of prompts for a named engine.

**It does not:**

- Write face-lock, outfit or character-sheet image prompts. That is `banana-pro-director-20`. This
  skill writes the character brief and calls it.
- Invent engine syntax from memory. It reads `engine-params.json` and the Seedance / Kling / Veo
  reference files owned by `video-prompt-director`.
- Edit or assemble footage. That is `ai-footage-recut`.
- Write captions, hooks or channel copy. That is `hook-generator` and `cy-ai-content-writing`.
- Decide emotional direction from scratch for a prestige piece. If the project wants Emotion Cards
  and a 10-point arc, it routes to `ai-director`. Most micro-drama does not need that layer, and
  saying so is part of the spec.
- Write a synopsis containing quoted dialogue. A quotation mark in an episode synopsis means the
  model has started writing the script two stages early. Gated.

## 3. Why a new skill and not an extension

`production-bible-builder` covers this shape for prestige work: one film, one arc, one emotional
spine, eight stages, a Craft folder. Vertical micro-drama is a different problem in four ways that
each break one of its assumptions.

| Assumption in `production-bible-builder` | Micro-drama reality |
|---|---|
| One emotional arc across the piece | 60 to 80 arcs, one per episode, plus a series arc, plus a payoff cadence measured in episodes |
| Shot list built once | 2000+ cuts. It has to be generated in batches and re-validated after every script edit |
| Landscape framing assumed | 9:16 locked, with platform UI eating the top 12% and bottom 20% |
| Consistency handled by pasting cards into prompts | Consistency across 60 episodes is the entire problem, and paste-forward does not survive it |

Trying to bolt episode count onto the bible builder produces a worse version of both. It stays; this
sits beside it.

## 4. Architecture

**Five JSON artifacts, one CLI, Craft as the human mirror.**

The JSON is the authority. Craft holds what a person reads and comments on. The skill writes both and
the sync direction is one way (JSON to Craft) except at the sign-off gate, where the user's edits in
Craft are read back and re-validated.

```
drama/
  series.json      params, premise, adaptation notes, cast roster, location roster,
                   prop roster, payoff beats, per-episode breakdown
  cast.json        one entry per character: identity, tier, arc, anchor descriptors,
                   reference image paths, voice spec
  world.json       locations with consistency anchors and lighting states;
                   narrative props with scale and state variants
  script.json      one file per episode batch. Scenes, beat flow, timing
  shots.json       one file per episode batch. Segments, cuts, frame prompts
  pack/E01/        emitted prompts and reference manifest per segment
  .gates.jsonl     gate failure log (shot stage only, see 11)
```

Five artifacts and not five skills, unlike shuohao. A micro-drama is one production with one set of
thresholds and one style lock; splitting it into five installable skills would mean five copies of
the params block and five chances for them to disagree. The internal separation stays because the
passes and the gate sets are genuinely separate.

## 5. Stage 0: the three-way intake

The only branching stage. All three routes end at the same place: a `series.json` that passes
`validate --stage skeleton`.

### The routing question

Asked once, first message, one block, never re-asked in the session:

> What have you got?
> **A.** A story already written (novel, short story, script, treatment, a finished text).
> **B.** A premise. One line, or a title and a trope, or a vibe.
> **C.** An outline that already exists, and you want it checked before you build on it.

Plus, in the same block and regardless of route, the four parameters that have no safe default:

1. **Episode count and episode length.** No default (see 10 for the numbers to offer).
2. **Genre and primary trope.** Determines the payoff type. Guessing this wrong wastes the whole
   pass, so it is asked, not inferred.
3. **Platform target.** ReelShort / DramaBox / ShortMax / other. Sets thresholds, not style.
4. **Engine.** Seedance 2.5 via Higgsfield, or Runway. Sets the segment ceiling and the resolution
   ceiling, which change the shot plan.

Anything the opening message already answered is not asked again.

### Route A: existing story

The adaptation route. Closest to what shuohao's `novel-outline` does, and the reason to read it.

1. **Locate the input.** A file path is used directly. Pasted text is written to a `.txt` first,
   because the verbatim-evidence gate (G-S8) needs the source on disk to compare against.
2. **Chunk if long.** Split by chapter heading, falling back to character count. Report the chunk
   count and, if the input exceeds the cap, say so explicitly rather than truncating quietly.
3. **Summarise per chunk** into structured material: plotlines (organised by line, not by chapter,
   because the line is the adaptation unit), characters with every alias seen in that chunk, payoff
   material with verbatim evidence, locations that actually host action.
4. **Cut, merge, order.** Cut to one main line plus at most one subplot, each cut carrying a reason.
   Merge functionally duplicate characters. Tier the survivors. Collect locations. Order the payoffs.
   Collect narrative props last, because a prop is defined by which payoff it carries, so props
   cannot be identified before the payoffs are placed.
5. **Evidence.** Every decision under `adaptation.keep` carries a verbatim fragment from the source.
   Never translated, never trimmed, never two fragments merged. This is the countermeasure to
   adapting from the title rather than the text, and it is the gate that makes Route A trustworthy.

### Route B: premise only

The generation route. The risk here is the opposite of Route A: nothing constrains the output, so
three attempts sound like one attempt.

1. **Expand the premise into three distinct series shapes**, not three versions of one. Distinct
   means the protagonist's want differs, not the setting. Each shape gets: logline, the lie the
   protagonist believes, the payoff engine (what mechanism generates a payoff every two to three
   episodes for 60 episodes), and the ending.
2. **The user picks one.** One question, not a menu of twelve.
3. **Ground the payoff cadence against real data.** If `--dea <path>` is supplied, resolve the chosen
   tropes against `data/tropes.csv` and report the title count for each. A combination with a high
   count is proven demand and a crowded field; a combination with no titles at all is either a gap or
   a reason nobody makes it. Report it as a flag, never as an error. See 12.
4. **Build the skeleton** through the same steps 4 and 5 as Route A, minus evidence (there is no
   source text, so `adaptation.keep` is empty and the evidence gate reports as skipped rather than
   passing).

### Route C: existing outline, health check

The checkup route, and the one most likely to be used by somebody who is not Cyan.

1. **Parse whatever arrives** into `series.json`. Missing fields are marked `null` with a `missing`
   note rather than invented. Asking the user to fill twelve blanks before they get any diagnosis
   defeats the point.
2. **Run the gates only.** No generation, no rewriting, no suggestions mixed into the output.
3. **Render the diagnosis.** Failed gates do not block the render. The failures are the product.
4. **Stop.** The route ends here by design. If the user says continue, the outline enters Stage 1 as
   if it had come from Route A, and the sign-off gate still applies.

The honest framing to keep in the skill: a passing checkup means the outline is structurally sound,
not that the show is good. The gates catch cadence vacuums, unemployed characters, unreachable
payoffs and missing hooks. They cannot tell you whether anyone will watch it.

### The convergence contract

Whatever the route, Stage 0 hands Stage 1 a `series.json` with `params`, `adaptation`, `characters`,
`locations`, `beats` populated and `episodes` empty, passing `validate --stage skeleton`. Everything
after this point is identical across the three routes, and nothing downstream is allowed to ask which
route the project came from. If a downstream stage needs to know, that is a fact that belonged in
`series.json`.

## 6. Stages 1 to 8

### Stage 1: Series skeleton, then a hard stop

Two rounds, the way shuohao does it, because the cost asymmetry is extreme: a wrong skeleton costs
one pass, a wrong skeleton discovered after 70 episode breakdowns costs everything.

**Round 1, fast.** Fill the four skeleton blocks, pass `--stage skeleton`, stop.

**Sign-off gate.** Put three named decisions in front of the user and wait:

1. Which storyline was cut, and what that makes the ending.
2. Which characters were merged, and who is in the lead group.
3. Which episode the first major payoff lands in, and which one the finale payoff lands in.

Not "does this look right". Three specific things, each answerable with a yes or a correction.

**Round 2, detailed.** Absorb corrections, pass `--stage beats`, proceed.

### Stage 2: Episode breakdown

Batches of 10 episodes, parallel where the environment supports it. Each batch receives the signed-off
skeleton, its own episode range, and the payoffs landing inside that range. Each episode produces:

- `synopsis` in narrative voice, no quoted dialogue
- `hook`: the question that makes someone tap the next episode
- `cliff`: the thread left hanging
- `characterIds`, `locationIds`, `propIds`
- `blockingPlan` where three or more characters appear (mandatory in 9:16, see 9)
- `warnings` for known generation hazards present in the synopsis

Ten per batch and not sixty, because the back half of a long single generation degrades: the cadence
flattens, the hooks start repeating, and characters drift. Batches align against the skeleton, never
against the previous batch's prose.

### Stage 3: Cast

Seeded from `series.json`. The roster, the tiers and the arcs are already decided and are carried by
script, not re-reasoned. This stage fills only what this layer decides: aliases, anchor descriptors,
the visual brief, the voice spec.

**Anchor descriptors** are the load-bearing five: hair, one signature garment, one distinctive prop or
asymmetry, build, and a demeanour word. They are what every downstream prompt repeats. Five is the
number `video-prompt-director` already uses; keep it rather than inventing a second convention.

Then hand off to `banana-pro-director-20` for face lock and outfit references, one character at a
time, resumable by file existence. This skill does not restate face-lock rules.

### Stage 4: World

Locations and narrative props, seeded from `series.json`.

Per location: design intent (what the space is for dramatically, not its floor plan), three to five
consistency anchors that are checkable in a generated frame, and the lighting states this location
actually appears in across its episodes. An anchor is a patched awning or a broken seventh plank. "An
aged atmosphere" is an adjective, not an anchor, and cannot be used to QC a frame.

Per prop: dramatic function (which payoff it carries), scale band, and state variants. A prop that
cannot be given a function is set dressing and belongs to a location's anchors instead.

Variants over new locations. Generating a new environment is cheap; keeping a sixtieth one consistent
is not. A location that appears once either gets cut or gets declared a variant of an existing one
with the delta written down.

### Stage 5: Script

Batches of 3 episodes. Seeded from `series.json` with target seconds, hook, cliff and claimed payoffs
already filled.

**Dialogue is structured data, never prose.** Each line is its own entry with a speaker, the line, and
a delivery note. Each action is its own beat. This is not a style preference; it is the foundation of
every deterministic check in the stage, and it is what lets the line book feed TTS directly.

Craft rules that carry into the writing and are worth stating because they are specific to generated
video, not to screenwriting in general:

- **Common actions only.** The performance is rendered by a video model, which can only play what it
  has seen a great many times. Boarding a boat, sitting, handing something over, nodding, turning
  back, gripping something, standing up: safe. Blocking an object with a pole, an eyelash tremor, a
  half-inch retreat, a metaphorical image: rewrite or cut. Dramatic information comes from the
  combination and timing of ordinary actions, not from the delicacy of the action itself.
- **The hook is the first beat, and it moves.** Not a label, not a static insert. A concrete image
  with subject motion in the opening beat. Static detail (the white-knuckled grip, the shape in the
  pocket) is the second landing, not the first.
- **Change one beat, read three.** After any edit, read the beat before and after and check three
  things: where each character physically is, what is in their hands, and who is present. Spatial
  state lives in your head while writing and does not while editing.
- **Change the picture, change the sound.** An action edit propagates to the shot description, the
  soundscape line and the frame prompt. All three, or the generated clip plays the sound of an event
  that is no longer in the scene.

### Stage 6: Shot plan

Batches matching the script's batches. Two levels:

- **Segment** = one generation call. Never crosses a scene. Duration ceiling comes from
  `engine-params.json`, not from this document.
- **Cut** = a hard cut inside a segment. 2 to 5 seconds, aimed at 3. Each cut claims a contiguous run
  of script beats.

**Claiming is the mechanism that makes the whole pipeline re-checkable.** Each cut declares
`beats: [from, to]` against a scene. Every beat must be claimed by exactly one cut, in order, with no
gap and no overlap. When the script changes, re-running validate names the cuts that no longer line
up. Without claiming, a script edit silently orphans a shot plan and nobody finds out until the
footage comes back wrong.

Per cut: seconds, shot size, camera move from the engine's vocabulary, on-screen characters, on-screen
props, and a frame prompt for the keyframe image.

### Stage 7: Prompt pack

Emission. This stage makes no creative decisions; everything it writes is derived from Stage 6.

Per segment it emits a folder containing:

- The video prompt for the target engine, in that engine's grammar
- The keyframe image prompt per cut
- A reference manifest: which character sheets, location plates and prop plates to attach, in order,
  with each one's role stated
- A voice manifest: which lines, in which order, with each speaker's voice spec

**Derived strings are reconciled verbatim.** Where the engine's grammar includes cut timestamps or an
alignment instruction, those are computed from the cut durations and the validator compares the
computed string against what is in the artifact, character for character. Change a duration, forget
the prompt, and the gate catches it. This is the single most valuable trick in the shuohao repo and it
transplants directly.

### Stage 8: Generate, QC, ledger

1. **Cost pre-flight** via `credit-watch` before anything is submitted, including the opt-in question
   about whether this project gets logged.
2. **First segment only, by default.** Generate the opening segment's full set and show it. Style,
   asset consistency and shot-reverse framing get confirmed on three to five frames, not on the
   thirty to forty in a full episode.
3. **QC each returned clip** against the locked style string, the character anchors, the location
   anchors, the frame size requested, and face count. A break means regenerate, not fix in the edit.
4. **Log failures** with the write-back protocol already in `video-prompt-director`: log what was
   asked for, what went wrong, what fixed it, and never log a failure with no known fix.
5. **Reconcile spend** afterwards, because failed generations often still charge.

Footage then leaves this skill and goes to `ai-footage-recut`.

## 7. Artifact schemas

Field-level detail belongs in `references/schema.md` at build time. The shape:

```jsonc
// series.json
{
  "source": "...",                  // title
  "route": "A|B|C",                 // recorded, never branched on downstream
  "params": {
    "episodes": 60,
    "secondsPerEpisode": 90,
    "genre": "...",
    "tropes": ["contract-marriage", "reborn"],
    "platform": "reelshort",
    "engine": "seedance-2.5",
    "aspect": "9:16",
    "styleFormula": "...",          // one string, repeated verbatim in every frame prompt
    "thresholds": { }               // overrides only; see 10
  },
  "adaptation": { "core": "", "keep": [{"what":"","why":"","evidence":""}],
                  "cut": [], "merge": [], "cutNote": "", "mergeNote": "", "risks": [] },
  "characters": [{ "id": "C01", "name": "", "role": "", "tier": "lead|support|functional",
                   "arc": "", "from": [] }],
  "locations": [{ "id": "S01", "name": "", "primary": true, "variantOf": null, "reusePlan": "" }],
  "props":     [{ "id": "P01", "name": "", "function": "", "beatIds": [] }],
  "beats":     [{ "id": "B01", "type": "", "weight": "major|minor", "episode": 3,
                  "setup": "", "payoff": "" }],
  "episodes":  [{ "ep": 1, "synopsis": "", "hook": "", "cliff": "",
                  "characterIds": [], "locationIds": [], "propIds": [],
                  "blockingPlan": "", "warnings": [] }]
}
```

`cast.json`, `world.json`, `script.json` and `shots.json` follow the same discipline: ids are stable
and referenced, never names; every field either has a gate or has a reason in the schema doc for why
it does not.

**Id discipline.** Data stores ids, interfaces show names. `C01` in the artifact; "Sheng Wen" in the
Craft page and in the rendered report. This is what makes a rename a one-line edit instead of a
search and replace across five files.

## 8. The gates

Twenty-seven, grouped by stage. Each has a stable id, a label, a boolean, and a detail string. Each
gets a breach case in the selftest.

**Series (`--stage skeleton` and `--stage beats`)**

| id | Checks |
|---|---|
| `series/episode-count` | `episodes.length == params.episodes` |
| `series/tier-caps` | lead 1 to 5, support <= 10, functional <= 10 (overridable) |
| `series/location-cap` | primary locations <= derived cap (see 10) |
| `series/prop-cap` | narrative props <= 8; skipped explicitly if `props` absent |
| `series/beat-gap` | gap between payoffs <= 3 episodes, no vacuum at head or tail |
| `series/major-early` | at least one major payoff, and the first one is not the final episode |
| `series/ep1-hook` | episode 1 has a hook |
| `series/ep-fields` | every episode has synopsis, hook and cliff |
| `series/narrative-voice` | no quotation marks in synopsis, hook or cliff (boundary gate) |
| `series/blocking-plan` | any episode with >= 3 characters carries a blocking plan |
| `series/hazard-flag` | hazard keywords in a synopsis (rain, physical contact, crowd, hand close-up) appear in that episode's `warnings` |
| `series/refs` | every referenced id exists; no character, location or prop goes unused; no payoff lands outside the episode range |
| `series/evidence` | every `adaptation.keep` entry with an `evidence` field matches the source file verbatim. Route B: skipped explicitly |

**Cast**

| id | Checks |
|---|---|
| `cast/roster-match` | every `series.characters` id has a cast entry and no extras |
| `cast/anchors` | exactly five anchor descriptors per character |
| `cast/no-names` | no character name, author name or work title inside any image prompt |
| `cast/distinct` | pairwise word overlap between any two characters' image prompts below the measured threshold; failure names the pair |

**World**

| id | Checks |
|---|---|
| `world/anchors` | 3 to 5 consistency anchors per location |
| `world/lighting` | at least one lighting state per location, each with a full prompt |
| `world/empty-plate` | location plate prompts specify no people, and the negative prompt excludes people |
| `world/prop-function` | every prop has a dramatic function and a scale band, and the scale phrase appears in its prompt |
| `world/variant-refs` | `variantOf` points at a real location and carries a delta |

**Script**

| id | Checks |
|---|---|
| `script/duration` | per-episode estimate within target +/- 15% |
| `script/line-length` | no single line exceeds the one-breath ceiling |
| `script/speaker` | every speaker is in that scene's cast or marked VO |
| `script/has-action` | every scene has at least one action beat |
| `script/action-prose` | no quoted dialogue inside an action beat |
| `script/hook-beat` | the hook's concrete image lands inside the first N beats of the episode |
| `script/cliff-beat` | the final beat of every episode is the cliff |
| `script/claims-payoff` | every payoff the skeleton assigns to an episode has beats delivering it |
| `script/refs` | characters reconcile to `cast.json`, locations, lighting states and props to `world.json` |

**Shots**

| id | Checks |
|---|---|
| `shots/coverage` | every script beat claimed exactly once, in order, contiguous |
| `shots/segment-cap` | segment total within the engine's per-generation ceiling |
| `shots/cut-length` | every cut within the min/max band |
| `shots/dialogue-fit` | the dialogue seconds a cut claims fit inside that cut's duration |
| `shots/ep-duration` | episode total within the script target +/- 15% |
| `shots/onscreen-count` | at most two faces in a 9:16 cut unless a blocking note explains (see 9) |
| `shots/vertical-safe` | every frame prompt carries the vertical framing phrase and states subject placement |
| `shots/segment-id` | segment ids are `E01-01` format and sequential |
| `shots/size-phrase` | the shot size phrase appears in that cut's frame prompt |
| `shots/camera-vocab` | camera move is in the engine's vocabulary |
| `shots/style-phrase` | the locked style string appears verbatim in every frame prompt |
| `shots/no-names` | no character names in any image prompt |
| `shots/refs` | scenes, characters and props reconcile to `script.json` |

**Prompt pack**

| id | Checks |
|---|---|
| `pack/derived-verbatim` | every derived timestamp or alignment string matches the value recomputed from cut durations |
| `pack/dialogue-verbatim` | every claimed line appears in the prompt character for character |
| `pack/engine-limits` | prompt length, reference count and aspect ratio all inside the engine's declared limits |
| `pack/anchor-repeat` | every shot containing a locked character repeats at least two anchor descriptors |
| `pack/audio-direction` | every shot carries a sound line and a music line, or an explicit no-music line |
| `pack/refs-complete` | every reference named in the manifest exists on disk, or is listed as not yet generated |

**Skipped is printed, never implied.** A gate whose input was not supplied prints "skipped: no
`cast.json` given". It never prints a tick. Silently passing and lying are one step apart.

## 9. What makes it vertical

The rules in this section are the reason this is not a landscape pipeline with a different aspect
ratio in the footer.

**Safe areas.** The platform UI covers roughly the top 12% and the bottom 20% of the frame. A face
centred vertically sits under a caption bar. Frame prompts state subject placement in the upper-middle
band, and `shots/vertical-safe` checks that the placement is stated at all.

**Two faces is the practical ceiling per cut.** A three-shot in 9:16 is either three small faces or a
cropped composition. `shots/onscreen-count` gates at two with a note required above it, which is
stricter than the landscape convention of three for exactly this reason. This is also why
`series/blocking-plan` is mandatory earlier: a three-character episode has to be planned as coverage,
not as a wide.

**The first three seconds are load-bearing.** Not a style note. Vertical platforms autoplay into a
feed, so the opening cut carries subject motion or the episode is scrolled past before the premise
lands. `script/hook-beat` gates the position; whether the beat actually moves is writing discipline
the gate cannot judge, and the skill says so rather than pretending otherwise.

**The cliff is the retention mechanism.** `script/cliff-beat` gates that the last beat is the cliff,
because an episode that resolves cleanly has no reason for anyone to tap again.

**Cadence, not arc.** A feature has one arc. A 60-episode vertical has a payoff every two to three
episodes, and the thing that kills a series is a vacuum in the middle third. `series/beat-gap` is the
gate that matters most in this whole spec.

## 10. Params, thresholds and their provenance

Every default carries the sentence explaining where it came from. A number without a provenance
sentence cannot be revised by anyone except the person who wrote it.

| Param | Default | Provenance |
|---|---|---|
| `episodes` | none, always asked | Measured from `data/titles.csv` in this repo: 3217 titles carry an episode count, median 62, mean 63.2, and 2713 of them (84%) sit between 40 and 89. Offer 60 to 80 as the normal band and 30 to 50 as the short band |
| `secondsPerEpisode` | none, always asked | Platform-dependent. Ask |
| `maxLeads` | 5 | Carried from shuohao. Revise against real productions |
| `maxSupport` / `maxFunctional` | 10 / 10 | Same. Their own note: tighten both for short runs, since the defaults were set for 60+ episodes |
| `maxPrimaryLocations` | `4 + ceil(episodes / 10)`, clamped 5 to 15 | Derived, not constant. 60 episodes gives 10. The cap protects consistency asset maintenance, not a set budget, because generating a location is cheap and keeping the sixtieth one on-model is not |
| `maxProps` | 8 | Same order of magnitude as the lead count. A prop that cannot be given a dramatic function is set dressing |
| `maxBeatGap` | 3 episodes | The retention lever. Platform-specific, so it belongs in `thresholds` |
| `charsPerSecond` | to be measured | shuohao uses 4.5 for Mandarin. English is a different rate and the number has to be measured against a real read before it is trusted. Until then, mark it a working assumption in the output |
| `actionSeconds` | 2.5 per beat | Carried. Measure and revise |
| `tolerance` | 15% | Carried. It is an estimate, not a stopwatch, and the tolerance exists to say so |
| `minCutSeconds` / `maxCutSeconds` | 2 / 5 | Attention rhythm, not an engine limit |
| `maxOnScreen` | 2 | Vertical-specific, see 9 |
| `maxSegmentSeconds` | read from `engine-params.json` | Engine limit. Never hardcoded here, because this is the number that moved between Seedance 2.0 and 2.5 and caused the patch note currently sitting at the top of `video-prompt-director` |

Everything in `params.thresholds` overrides. Nobody edits code to change a platform's limits.

## 11. Gate logging

`validate` and `checkup` append per-gate results to `.gates.jsonl` in the working directory.
`stats` summarises: which gate fires most (that rule's wording in the skill is what needs fixing),
which gate has never fired (either a dead gate or a rule the model has internalised), and what the
failure details actually look like.

**Ship this on the shot stage only.** shuohao ships it on one skill out of five and writes down why:
if nobody opens it after months of real use, the feature was wrong, and propagating it would copy the
mistake. Same discipline here. Revisit after one real series.

## 12. The DramaEverAfter connection

Optional flag, `--dea <path to the repo>`. When supplied:

- Trope ids in `params.tropes` resolve against `data/tropes.csv`, and an unrecognised trope is an
  error, since the taxonomy already exists and inventing a parallel one splits it.
- The title count for each trope is reported. As of this writing the top of the distribution runs
  toxic love 1658, sweet 1628, reborn 1555, cute kids 1171, misunderstanding 1074, billionaire 1037,
  contract marriage 1032. That is demand data and crowding data at the same time.
- A trope combination with no titles in the database is flagged, not blocked. It is either a genuine
  gap or a combination nobody makes for a reason, and the skill is not in a position to tell which.
- `params.episodes` outside the observed band is flagged with the actual distribution rather than a
  rule of thumb.

No other skill in the stack has ground truth like this available to it. 3789 catalogued titles from
the exact platforms this skill produces for is a real asset, and wiring it in costs one CSV read.

## 13. CLI surface

Deterministic, zero dependency, standard library only, so the skill stays copyable.

```
vertical-drama.mjs

  intake <route> [...]                route-specific scaffolding for stage 0
  chunk <source.txt> <workdir>        split a long source (route A)
  validate <file> [--stage s] [refs]  gates; prints violations and exits 1
  checkup <file> [refs]               gates only, never blocks, renders the diagnosis
  seed <upstream.json> [--eps 1-10]   deterministic carry-forward to the next stage
  timing <script.json>                per-episode duration estimate
  pack <shots.json> --script s.json   emit the prompt pack per segment
  render <file> [--md|--html]         human-readable output
  craft-sync <file>                   push the human mirror to Craft
  stats                               summarise .gates.jsonl (shot stage)
  slug <name>                         safe filename
```

Reconciliation flags, all optional, all printing "skipped" when absent: `--series`, `--cast`,
`--world`, `--script`, `--dea`, `--engine`.

## 14. Engine layer

The skill knows the grammar of a shot plan. It does not know Seedance's syntax by heart.

- **Engine limits** come from the shared `engine-params.json` proposed in the gap report (edit E2):
  per-generation ceiling, prompt length ceiling, reference asset caps, supported aspect ratios,
  camera vocabulary, each with a source and a verification date.
- **Prompt grammar** comes from `video-prompt-director`'s reference files. For a multi-character
  vertical drama with drift risk, that means the Locked tier: frame map, per-character subject lock,
  cross-frame rules, performance block. Micro-drama is exactly the case the Locked tier was built for.
- **Higgsfield specifics** worth carrying: Seedance 2.5 there exposes 480p and 720p only, which is a
  real constraint on a 60-episode deliverable and should be surfaced at Stage 0 rather than
  discovered at Stage 8.
- **Runway** enters through `generate_multishot_video` and the image and upscale tools. Its multishot
  structure maps onto segments and cuts differently from Seedance; the pack stage emits per engine and
  the two emitters are separate code paths, not one with flags.
- **Character and location images** are generated through `banana-pro-director-20` and the Higgsfield
  image tools. Not this skill's grammar.

## 15. Craft integration

Craft is the human mirror, not the store.

- `craft-sync` writes one project folder: Series Bible, Cast, World, Scripts (one page per batch),
  Shot Plan, Production Notes.
- The sync is one way, JSON to Craft, with one exception: at the Stage 1 sign-off gate, edits made in
  the Craft page are read back, parsed into `series.json`, and re-validated. Everywhere else, editing
  the Craft page and expecting the pipeline to notice is a trap, and the skill says so on the page.
- Tasks and deadlines route to `craft-task-manager`. This skill does not manage tasks.

## 16. Selftest

Non-negotiable, and the reason any of the above is worth building.

`scripts/selftest.mjs` calls no model, costs no quota, runs in about a second, and covers every
deterministic path: chunking, seeding, timing arithmetic, the derived-string computation, and every
one of the twenty-seven gates with at least one breach case proving the gate actually catches.

The bundled example is this skill's own, never borrowed: one short original premise taken through all
eight stages at a miniature scale, six episodes of ninety seconds, four characters, three locations,
two props. It doubles as the quality benchmark and the test fixture. Breaking it breaks the test.

## 17. Build order

Each phase ends with a working, testable thing. Nothing is built ahead of the phase that needs it.

| Phase | Build | Done when |
|---|---|---|
| 1 | `series.json` schema, the 13 series gates, `validate --stage`, `checkup`, selftest | Route C works end to end. The health check is shippable on its own |
| 2 | Route A and Route B intake, `chunk`, evidence gate, the sign-off gate | A real story reaches a signed-off skeleton |
| 3 | Episode breakdown, batching, `render --md` | A full 60-episode breakdown passes the gates |
| 4 | `cast.json` and `world.json`, their gates, `seed`, the banana-pro handoff | Assets are registered and reference images exist |
| 5 | `script.json`, timing, the 9 script gates | Three episodes of script pass duration and structure |
| 6 | `shots.json`, claiming, the 13 shot gates, `.gates.jsonl` and `stats` | A shot plan survives a script edit and names what broke |
| 7 | `pack`, the derived-verbatim reconciliation, per-engine emitters | A segment folder pastes straight into Higgsfield |
| 8 | credit-watch wiring, QC loop, failure log | One episode generated, QC'd, and reconciled against spend |

Phase 1 alone is a useful product. If the build stops there, the health check still earns its keep.

## 18. Open questions

Three of these change the shape of the build. The rest change defaults.

**Shape-changing:**

1. **Dialogue language.** English only, or does this need to produce Mandarin or other dialogue for
   platform delivery? If non-English, the language and role split (human fields follow a `lang`
   parameter, machine fields always English, TTS specs always English) has to be designed in from
   phase 1, not retrofitted. `charsPerSecond` also becomes per-language.
2. **Primary engine for the first series.** Seedance 2.5 via Higgsfield at 720p maximum, or Runway?
   The segment ceiling and the resolution ceiling both change the shot plan, and the two pack
   emitters are separate code paths. Pick one to build first.
3. **Voice and TTS in scope?** If yes, the script stage grows a line book with per-character voice
   specs and the pack stage grows a voice manifest, both of which are already sketched above. If no,
   cut them and the script stage gets simpler.

**Default-changing:**

4. Episode count and length for the first real production. The DEA distribution says 60 to 80
   episodes is normal, but your first one might deliberately not be.
5. Is the DEA repo available on disk at run time, or does the skill need a snapshot of `tropes.csv`
   copied into `references/`?
6. Does `craft-sync` run automatically at the end of every stage, or only when asked?
