# Reddit audience research, 20 September 2026

Source: the enriched PDF Cyan supplied, "Reddit Vertical-Drama Research -
Enriched Master Dataset", 233 title records compiled from vertical-drama
Reddit threads plus a "Trending AI Mafia Dramas" infographic. The full
structured import is `generator/staging/reddit_research_2026-09-20.json`.

The document says of itself that it is discovery notes, not metadata. This
pass treated it that way: nothing was written into `titles.csv`.

## 1. What it is worth as a data source

| | |
|---|---|
| Records in the document | 233 |
| Already in the database | 90 (39%) |
| Near-matches sent to `match_queue.csv` for a ruling | 16 |
| Held, nothing created | 127 |
| Platform claims that landed on an existing title | 13 |
| Of those, claims that **disagreed** with `availability.csv` | **0** |

That last row is the reason to take the rest seriously. Every platform
attribution in this document that could be checked against the database was
right. It is not proof the other 167 are right, but it is better calibration
than fan lists usually earn.

The 127 held records are not rejects. They are titles no adapter in this repo
has ever reached: 11 on ShortMax, 10 on DramaWave, 3 on FlickReels, 2 on
iDrama, 2 on My Muse, 1 on Vigloo, plus 86 with no platform named at all.
The database's blind spots and this document's contents are close to the same
list.

## 2. What the audience commentary actually supports

Be honest about the sample. Only **80 of the 233 records carry real viewer
commentary**; the rest are bare title mentions. Theme counts run from 2 to 10
titles. This is directional evidence about what readers say they want, not a
measurement.

| Signal | Titles | Representative |
|---|---|---|
| Strong female lead | 10 | Forensic Bride, The Lost Witch Tops Magic Exam, Kiss of the Pirate King |
| Humour / self-aware fun | 8 | Dear Stranger I Love You, Deny Me Dragon King, The New York Godfather |
| Satisfying ending or twist | 6 | Crown of Hidden Scales, The Raven's Bride |
| Attractive male lead | 6 | The Words, No Escape from the Vampire, The Maid Who Ran From the Don |
| Acting / writing praised | 5 | Life Is Not a Game, We Are Never Ever Getting Back Together |
| Chemistry | 4 | Fight Dirty, Kissed by Claw and Fang |
| Production quality | 4 | Kiss of the Pirate King, The God Level Blacksmith |
| AI realism / coherence | 4 | Caught in His Current, Sold to the Warlord Born for the Sky |
| Romance without cruelty | 4 | Light in Winter, Bumped into the Billionaire |
| Rewatch / finished all episodes | 3 | Life Is Not a Game, He Broke the Heart That Saved Him |

Three things in there are worth acting on, because they cut against what the
platforms themselves merchandise:

1. **Chemistry survives bad production, production does not survive bad
   chemistry.** Kissed by Claw and Fang is recommended with its effects called
   "Snapchat bad" in the same sentence. Nobody in this document recommends a
   title for looking expensive alone.
2. **Absence of cruelty is a selling point.** Bumped into the Billionaire is
   praised specifically for having no slapping, no revenge arc and a male lead
   who stays focused on the heroine. Forensic Bride is praised for having no
   dragged-out misunderstanding. Viewers are naming the tropes they are tired
   of, which is a sharper signal than naming the ones they like.
3. **Trope subversion is described as the pleasure, not the exception.** The
   Lost Witch Tops Magic Exam is praised because the heroine knows the
   found-heiress playbook and refuses to run it.

## 3. The AI finding, which is the real story

The document names **57 titles claimed as AI-generated** (32 explicit, 25 that
need verification). Only **5 of those 57 are in the database**, and only one
(`caught-in-his-current`) is flagged `ai=yes`. Across the whole database, 71 of
3,789 titles carry an AI ruling.

So: the audience conversation about AI verticals is now large enough to fill a
third of a 233-title research document, and the database covers it at under
10%. That is the widest gap this research exposes.

What viewers praise in AI titles has also moved. It is no longer "the visuals
are impressive". It is coherence, pacing, consistent character design, and
endings that land: The God Level Blacksmith, One Night Stand with the Empire's
General, Caught in His Current, They Gave the Doomed Duke the Wrong Bride.
One commenter volunteered that repeated outfits matter less in fantasy, which
is why dragons, wolves, vampires and magic dominate the AI list.

Four in-database titles carry an AI claim from this document and a blank `ai`
column. They need Cyan's ruling, not mine, because the `ai` column is set by
hand:

- `my-x-ray-vision-sees-right-through-you`
- `blitzed-by-my-rival-s-obsession`
- `zero-to-alpha-return-of-the-wolf-king`
- `rose-in-chains`

## 4. What was changed in this pass

- `generator/staging/reddit_research_2026-09-20.json` — all 233 records,
  verbatim, with match status, platform claims, AI claims, aliases and
  audience evidence per title. The permanent record.
- `data/match_queue.csv` — 16 near-match rows awaiting a
  confirmed_same / confirmed_different ruling. Five are near-certain
  (article-only differences: The Perfect Spiral, The Best Mistake Ever, The
  Atlantic Bride, Sold to the Warlord, and the infographic's shortened
  "The Billionaire's Unexpected Bride"). Eleven are genuine judgement calls.
- `generator/staging/reelshort_wanted.txt` — 12 ReelShort-attributed titles
  the database does not have. No `ai=` flag on any of them; that column is
  Cyan's hand. Eleven come from the mafia infographic, the weakest source in
  the document, so they are left to resolve through ReelShort's own search:
  real titles get created on the next weekly run, invented ones simply report
  as still waiting. The file verifies them for us.

Nothing was written to `titles.csv`, `availability.csv` or the `ai` column.

## 5. Open decisions for Cyan

1. **The 127 held titles.** Most sit on platforms with no adapter (ShortMax,
   DramaWave, FlickReels, iDrama, My Muse). Writing a DramaWave adapter would
   convert the largest single block, and DramaWave is where Cy's own favourites
   came from. Worth a session; not worth guessing rows into the database.
2. **Audience evidence has nowhere to live.** The schema has no field for why
   viewers liked a title. It is sitting in a staging JSON where the generator
   cannot see it. Options: a new `audience_notes` column on titles, or leave it
   as caption fuel only. The second is cheaper and probably right for now.
3. **The 16 match-queue rulings**, which block those titles from being either
   merged or created.
4. **Six in-database titles have no synopsis and this document supplies real
   fact material for them**: `faking-it-with-the-hockey-captain`,
   `life-is-not-a-game`, `cheer-up-baby`, `fight-dirty`,
   `kiss-of-the-pirate-king`, `i-kissed-a-ceo-and-he-liked-it`. That is caption
   work, through the dea-captions skill and Cyan's review, not a merge.
5. **An AI editorial page.** 57 claimed AI titles and a repeated audience
   appetite for them is a content opportunity the site currently does not serve
   at all. It needs verified titles first, which is decision 1 again.
