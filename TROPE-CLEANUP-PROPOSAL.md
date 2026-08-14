# Trope vocabulary cleanup - PROPOSAL, awaiting Cyan's rulings

Written 14 Aug 2026. **Nothing in here has been executed.** Every number below was
measured against `data/titles.csv` and `data/tropes.csv` as they stand, read-only.

Raised by Cyan: "I see you have SM as a trope, what is that? 261 tropes is a lot.
I also notice you have some stuff tagged Secret Billionaire but not Billionaire?"
All three turned out to share one root cause.

## The diagnosis in one paragraph

Trope tags were taken from each platform's own vocabulary and never reconciled with
each other or with ours. Three consequences: GoodShort tags at 35 tropes per title
where every other source averages 3.3, which floods the vocabulary with labels that
carry no information; the same concept is stored under several spellings, splitting
one idea across two published pages; and platform content labels we never chose
(`sm`, `gay`) are live as public trope pages.

Measured vocabulary sizes, which disagree with each other and are the answer to
"261 is a lot":

| Measure | Count |
|---|---|
| Rows in `tropes.csv` | 224 |
| Distinct tropes actually used on titles | 300 |
| Trope pages built | 203 |
| Used on titles but absent from `tropes.csv` | 117 |
| In `tropes.csv` but used on zero titles | 41 |
| Rows whose `title_count` is wrong | 170 of 224 |

`title_count` is badly stale: CEO declares 103, actual usage is 1,827.

---

## DECISION 1 - the three content-label pages that are live now

`/tropes/sm.html`, `/tropes/bl.html` and `/tropes/gay.html` all return 200 on the
live site. The SM page renders as:

    <title>Best Sm Vertical Dramas (2026) | DramaEverAfter</title>
    <h1>Sm</h1>

In Chinese short-drama and webnovel tagging **SM means sadomasochism**. It sits
beside `bl` (boys love) and `gay` in the same GoodShort vocabulary, which is what
makes the reading confident.

| Tag | Titles | Sources | Evidence it is not real tagging |
|---|---|---|---|
| `sm` | 212 | GoodShort only | 118 of the 212 also carry `cute kids` |
| `gay` | 190 | GoodShort only | 188 also carry `bl` |
| `bl` | 356 | GoodShort 346, **Vigloo 10** | the GoodShort 346 also carry `strong female lead` on 322 |

**A frequency cut will NOT catch these.** They sit at 12%, 10% and 19% of the
GoodShort catalogue, below every threshold in Decision 2. They need explicit
handling.

**PROPOSED, and the `bl` line is the one worth your eye:**

1. `sm` - delete the tag from all 212 titles, delete the page. It is an adult
   content classification you never chose to publish and the data contradicts it.
2. `gay` - delete the tag from all 190 titles, delete the page. Same basis. Note
   this is not a decision about LGBT titles on the site, it is a decision about a
   label applied by a scraper to titles it does not describe.
3. `bl` - **drop the 346 GoodShort assignments, KEEP the 10 Vigloo ones.** The
   Vigloo rows look genuine: `An Omega Among Alphas`, `Sweet Trap for My Omega`,
   `Uncle Doesn't Know`, `The Reversed Life of the Young Master`, tagged cleanly as
   `bl;romance` or `bl;animation` rather than buried in 35 others. The page keeps
   10 titles, which clears the 5+ publish bar honestly. Rename the display to
   **"BL"** or **"boys love"** so it stops rendering as "Bl".

Deleted pages are published URLs, so each needs a 301 in `_redirects` rather than a
bare 404.

---

## DECISION 2 - GoodShort's tag density

1,820 GoodShort titles average **35.1 tropes each**. Every other source averages
**3.3**. Their commonest tags cover almost the whole catalogue:

    counterattack       1781  (98% of GoodShort titles)
    regret              1738  (95%)
    CEO                 1723  (95%)
    revenge             1697  (93%)
    strong female lead  1682  (92%)

A tag on 98% of a catalogue carries no information. It is also self-contradictory:
456 titles carry both `werewolf` and `vampire`, 188 carry both `bl` and `gay`.

**Correction to my first read, recorded so it is not repeated:** this is NOT the
browse vocabulary dumped wholesale onto every title. All 1,820 tag sets are
distinct and pairwise Jaccard similarity is 0.43. GoodShort really does tag per
title, just far too loosely to use as-is.

**Dropping GoodShort tags entirely is too destructive** and is not proposed:
all 1,820 titles fall to zero tropes, failing point 5 of the completeness bar, and
**88 published trope pages** fall below the 5+ publish bar.

**PROPOSED: a source-scoped frequency cut.** Drop a tag from GoodShort titles only
where it covers a large share of GoodShort's own catalogue. Other platforms keep
the same tag untouched, so `CEO` survives as a real trope on its genuine titles.

| Threshold | Tags cut | Avg tropes left per title | Published pages lost |
|---|---|---|---|
| >= 80% | 16 | 20.9 | measured on request |
| **>= 50% (recommended)** | **27** | **14.0** | **15** |
| >= 40% | 33 | 11.4 | 18 |
| >= 25% | 49 | 6.1 | 26 |

No titles are left with zero tropes at any threshold down to 40%.

**Recommendation: 50%.** It removes the pure noise while costing 15 pages. If you
want GoodShort to look like every other source (6.1 tropes per title, close to the
3.3 average) that is the 25% row, at 26 pages. I would not go below 25%.

---

## DECISION 3 - 41 concepts stored under more than one spelling

This is the direct answer to the Secret Billionaire question. Only 2 titles carry
`secret billionaire` and neither also carries `billionaire`, because nothing
reconciles tags between platforms. The same fracture runs through the vocabulary,
and **every one of these is a mechanical spelling difference, not a semantic
judgement** - hyphen versus space, or case:

    'underdog rise'=1615      vs  'underdog-rise'=50
    'contract marriage'=1021  vs  'contract-marriage'=11
    'love after marriage'=839 vs  'love-after-marriage'=3
    'love triangle'=833       vs  'love-triangle'=4
    'hate love'=739           vs  'hate-love'=11
    'forbidden love'=677      vs  'forbidden-love'=4
    'second chance'=671       vs  'second-chance'=43
    'dark romance'=660        vs  'dark-romance'=10
    'flash marriage'=638      vs  'flash-marriage'=24
    'one night stand'=550     vs  'one-night-stand'=22
    'time travel'=393         vs  'time-travel'=7
    'office romance'=381      vs  'office-romance'=2
    'substitute bride'=314    vs  'substitute-bride'=3
    'age gap'=293             vs  'age-gap'=20
    'miracle doctor'=252      vs  'miracle-doctor'=1
    'enemies to lovers'=154   vs  'enemies-to-lovers'=27
    'hidden-identity'=147     vs  'hidden identity'=56
    'superpower'=116          vs  'super-power'=9
    'CEO'=1727                vs  'ceo'=100
    ... 22 more, full list reproducible from the audit

**PROPOSED:** merge each pair into the higher-count spelling, 301 the losing URL.
37 of the 41 have a published page on BOTH sides today, so 37 redirects.

**This is not the near-slug rule you set.** That rule exists because `mate` and
`mates` are genuinely different in this genre. These pairs are the same words with
different punctuation. I am asking for blanket approval on the mechanical pairs
only. Anything semantic stays held, including `childhood-sweethearts` vs
`childhood sweethearts`, which belongs with your pending singular/plural ruling on
childhood sweetheart/s, contract lover/s and athlete/s.

---

## DECISION 4 - genres filed as tropes

`titles.csv` already has a `genres` column and these are almost absent from it:

| Value | Titles as trope | Already in genres column | Has a trope page |
|---|---|---|---|
| `anime` | 311 | 0 | yes |
| `romance` | 117 | 8 | yes |
| `fantasy` | 87 | 2 | yes |
| `thriller` | 64 | 0 | yes |
| `animation` | 46 | 0 | yes |
| `drama` | 24 | 0 | yes |
| `comedy` | 17 | 0 | yes |
| `sci-fi` | 10 | 0 | yes |
| `horror` | 3 | 0 | no |

Same shape as the My Drama `trending` problem already on the traps list.

**PROPOSED:** move these into `genres` and retire the trope pages with redirects.

**One flag before executing:** all 311 `anime` assignments are GoodShort, and
GoodShort's catalogue is live-action vertical drama. Those 311 are probably wrong
rather than misfiled, in which case `anime` should be deleted rather than moved. I
want to check a sample against the actual titles before touching it, and I have not.

---

## DECISION 5 - housekeeping, no ruling needed

These are corrections with no judgement in them. Say the word and they run with the
rest:

- Regenerate `title_count` on all 224 rows. 170 are wrong today.
- Reconcile the vocabulary: add the 117 tropes used on titles but missing from
  `tropes.csv`, remove or retire the 41 declared with zero usage.
- Fix the `.title()` render trap for acronyms so `CEO` stops rendering as "Ceo"
  (100 titles), `female ceo` as "Female Ceo" (600) and `bl` as "Bl". This was
  already logged as latent in the traps list. It is live.

---

## Order of execution, once ruled

1. Decision 1 (live content labels) - smallest change, highest urgency.
2. Decision 5 housekeeping and Decision 3 merges - mechanical, low risk.
3. Decision 2 threshold cut - largest data change.
4. Decision 4 genres, after the `anime` sample check.
5. Regenerate `_redirects`, rebuild, re-run `completeness.py` and report the new
   number. Expect the headline completeness figure to MOVE, because point 5 of the
   bar is "at least one trope" and this changes which titles have one.

Nothing above runs until Cyan rules. The live site is unaffected either way until
the next deploy.
