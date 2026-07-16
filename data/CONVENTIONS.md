# Data conventions (read me before merging)

- Slugs are permanent identifiers. Never change an existing slug.
- Slug style matches ReelShort URL slugs: apostrophes become hyphens.
  Correct: dominated-by-my-dad-s-boss / Wrong: dominated-by-my-dads-boss
  When slugifying a new title, check for an existing near-match (compare with all hyphens removed) before creating a new row.
- ReelTalk episodes, The Next ReelStar, and other unscripted/interview content are excluded from titles.csv.
- View counts in availability.csv update freely; all other non-blank fields are fill-blank-only.
- Add a snapshots.csv row per title per harvest date.
