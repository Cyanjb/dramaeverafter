---
name: dea-captions
description: Write, gate and apply DramaEverAfter title captions (the two-line synopsis_short that replaces a copied platform synopsis). Use this skill whenever the work touches DEA captions in any form - writing a caption batch, rewriting copied synopses, filling titles that have no synopsis, applying Cyan's review edits back from the artifact widget, building a review page for her, or deciding whether a title needs her eye. Trigger it even when the request sounds like something else, because it usually is one: "flesh out the thin pages", "the pages Google sees as thin", "do the next batch", "write these up", "her edits are back", "make a fresh widget", "the captions are terrible, take another pass". Also trigger before touching caption_pipeline.py, readback.py, make_review_page.py, CAPTION-TRAINING.md, or any generator/staging/captions_*.py file. Do NOT trigger for platform scraping, trope cleanup, or general DEA site work that never writes a synopsis.
---

# DramaEverAfter captions

A caption is the two-line `synopsis_short` on a title page: a HOOK line, a
newline, then a BODY. It exists because the site once carried 646 platform
synopses copied word for word, and that scaled-content profile is a direct
cause of the 1 Sep 2026 Google collapse. So a caption has two jobs at once:
make a reader press play, and be genuinely ours.

Cyan is the owner and the editor. She is not technical, she writes fast, and
she is training you deliberately: "consider corrections and my updates to text
as training." Her edit rate per batch is the score. Falling means it is working.

## Read before writing anything

`generator/CAPTION-TRAINING.md` is the corpus: every draft-versus-her-version
pair that taught something, grouped into seven lesson classes. Read it in full
before a batch, not a skim. Then read ten captions already live on the site, so
the register is in your ear rather than in your notes.

This file holds the process and the failures that repeat. The corpus holds the
craft.

## The two failures that keep happening

Both of these have been caught by Cyan more than once. They are not knowledge
gaps, they are process gaps, so they get their own section.

### 1. There is no length limit. Stop inventing one.

Word caps were removed on 24 Aug 2026 ("just remove these word caps") and
`validate()` says so plainly: length is the writer's judgement, full stop. On
6 Sep a batch was written to an invisible target anyway and she rejected it:
"these captions are terrible they seem to be cut off."

Understand why this matters more than it sounds. Compression is the upstream
cause of both complaints she made that day:

- **It makes captions read cut off.** Squeezing drops the connective tissue and
  leaves real details sitting as fragments. "He spent two decades under three
  Masters beyond Sacred Rank" means nothing to someone who does not know the
  story. Her fix kept the detail and explained it: "In a twist of fate he is
  taken in by three Masters beyond Sacred Rank who spend two decades training
  him to be the best of the best."
- **It forces copying.** With no room to retell a story you end up rearranging
  the platform's own sentence, which is precisely what the whole project exists
  to avoid.

Her own bodies run roughly 60 to 105 words, and that is a reference point, not
a target either. Write the whole story. If a caption feels long, that is not a
reason to cut it.

### 2. Retell the story. Do not reword the sentence.

The test is not "did I change the words". It is "did I put the source down and
tell someone what happens". A caption that follows the source clause by clause
is a copy wearing a hat, no matter how many synonyms went in.

Two detectors, because they catch different things:

- The **copy detector** compares whole bodies (difflib, fail at 0.6). It catches
  wholesale reuse.
- **`scripts/lift_check.py`** catches what the ratio misses: a single distinctive
  phrase taken verbatim barely moves a whole-body ratio, but it is exactly what
  Google reads as duplicate and what Cyan reads as "you just changed some
  words". Run it and read every hit. Keep names, and keep genre terms the
  audience browses by. Rewrite everything else.

```bash
python3 .claude/skills/dea-captions/scripts/lift_check.py <batch.py> --n 6
```

## The shape

```
HOOK line, one or two beats, plain and concrete
BODY, the whole story, ending on what it costs somebody
```

Hard bans, mechanical, no exceptions: dashes of any kind, exclamation marks,
runs of four or more capitals, curly apostrophes, multi-dot ellipsis. These are
her rules and the gate enforces them. When her own text breaks one, fix the
mechanical part only and tell her you did.

## The rules that produce her voice

The corpus has the pairs; these are the headlines.

- **The ending is one beat and it must land.** Do not stop at the last plot
  fact. Write the consequence. Her clearest correction: a caption ended
  "decides on a divorce", she added "While she comes to realize losing her
  husband may be her greatest regret." Tease the story, never narrate the
  audience: rhetorical questions about the plot survive ("But why?"), direct
  challenges to the reader and commentary about watching ("deeply satisfying")
  get cut.
- **Plain speech beats constructed cleverness.** "Her husband murdered her.
  Then she woke up." The extra word that adds information usually subtracts
  punch.
- **Never invent the HOW when the source gives the THAT.** Her words: "they
  don't just talk you invented that." If the source says the doctor was
  determined to pull her back, do not stage a night of talking.
- **Do not drop the source's biggest beat.** "You left out the most important
  part where she holds them accountable." The spoiler rule protects the turn,
  not the premise; where the title announces the reveal, put it in.
- **Keep the audience's vocabulary.** CEO, flash marriage, contract marriage,
  mate bond, Luna, Alpha, second chance. These are how people browse. The gate
  fails a paraphrased genre term.
- **Contractions carry the register**, except where a line wants weight.
- **Plain subject-verb order.** Twisted syntax is almost always the tell that a
  sentence was rotated to dodge its source rather than rewritten.

## Facts first, and never invent one

A caption is only ever written from the platform's own page. Facts live in
`generator/staging/facts_*.json` with a URL for each, and
`caption_pipeline.load_facts()` reads them. The sandbox can reach
reelshort.com and goodshort.com directly, so fetch rather than guess.

When a source is a marketing blurb, a truncated stub or has no story in it, do
not write the caption. Name the title in the batch header as needing her or a
better source, and move on. Inventing a plot is the one unrecoverable mistake:
everything else is an edit, that is a lie on her site.

## Who approves what

- **Top 300 by reach**: Cyan reviews. Stage the batch UNAPPROVED and build her
  a review page.
- **Below top 300**: her 16 Aug 2026 ruling is that you write and apply without
  her manual check. Record the approval basis in the approved file's header.
- **READ MEANS DONE**: a caption she ticked without editing is approved. Do not
  re-litigate it.
- **Her edits are verbatim, with one exception she granted on 6 Sep 2026:**
  fix obvious spelling and grammar slips, never word choice, and list every
  change back to her. Her phrasing, rhythm and vocabulary are hers even where
  you would have written it differently; "tutns" and a doubled "but" are not.
  Apply edits by surgical string replacement into the existing staging file,
  not by regenerating it: regenerating reorders keys and breaks the FACTS
  comment pairing. Replace the WHOLE literal with `repr(new_value)` rather than
  patching inside it, or an apostrophe you insert will break a single-quoted
  string, and re-parse the file with `ast.parse` before moving on.
- **`apply` will not overwrite an existing caption** unless you pass
  `--update-ours`. That guard is deliberate, so a rewrite of already-live text
  needs the flag or it silently does nothing and reports "skipping N already
  ours".

## The workflow

```bash
# 1. Queue and facts
python3 generator/caption_pipeline.py next 40            # ranked by reach
# fetch missing synopses from the platform page, bank to staging JSON

# 2. Write into generator/staging/captions_<date>_<name>.py
#    FACTS comments above each key; collapse whitespace with ' '.join(text.split())
#    or a newline inside a comment becomes a SyntaxError

# 3. Gate, in this order
python3 generator/caption_pipeline.py check <batch.py>   # rules + genre terms
python3 generator/readback.py <batch.py>                 # caption beside source
python3 .claude/skills/dea-captions/scripts/lift_check.py <batch.py> --n 6

# 4. Her review, when it needs her
python3 generator/make_review_page.py <batch.py> out.html --title "..."
# publish as an artifact; the storage key is per batch so widgets never collide

# 5. Apply
python3 generator/promote_captions.py <batch.py> <approved.py>
python3 generator/caption_pipeline.py apply <approved.py>
python3 generator/build.py && python3 generator/check_site.py
```

## After every review, close the loop

This is the part that makes the next batch better, and it is the part most
likely to be skipped.

1. Diff each of her edits against the draft.
2. Classify against the corpus classes. A pair that fits an existing class
   means the training has not landed. Say so plainly rather than filing it as
   new.
3. A pair that teaches something new gets added to `CAPTION-TRAINING.md` with
   its lesson.
4. Report her edit rate: percentage of captions touched, and percentage of
   words changed within those. The number is the score.

If a rule keeps getting broken across sessions, the fix belongs in this file or
in the gate, not in another apology.
