# Data conventions (read me before merging)

- Slugs are permanent identifiers. Never change an existing slug.
- Slug style matches ReelShort URL slugs: apostrophes become hyphens.
  Correct: dominated-by-my-dad-s-boss / Wrong: dominated-by-my-dads-boss
  When slugifying a new title, check for an existing near-match (compare with all hyphens removed) before creating a new row.
- ReelTalk episodes, The Next ReelStar, and other unscripted/interview content are excluded from titles.csv.
- View counts in availability.csv update freely; all other non-blank fields are fill-blank-only.
- Add a snapshots.csv row per title per harvest date.
- One page per show, dubs included (Cyan, 24 Sep 2026). A platform's dub listing
  ("[ENG DUB] X", "(Dubbed) X", "[Dubbed Version] X") belongs on X's page as a second
  availability row with `version` = `english-dub`; `version` is blank for the original.
  Run `generator/merge_dubs.py --apply` after adding dub listings; check_site warns if
  one is left on its own page. A dub with no original on file keeps its page, marked
  english-dub. Any title with an english-dub row is found by Browse's Dubbed filter.
- `origin` (titles.csv) is a label and a Browse filter, never a folder: english
  (the default when unknown), chinese, korean. Every show lives at /titles/<slug>.html.
- credits.csv `role` = `dub_voice` for a dub's voice cast, billed by the platform but
  not on screen; the title page says "English dub voice" and lists them last.
