# Popular Actors — IMDb lookup list

Source: Reddit fan panels, 9 Aug 2026. All 38 confirmed present in people.csv.

**What each job produces.** An IMDb PDF gives us CREDITS (filmography) — it does not give us photos.
Photos are hotlinked from the platform CDNs (all 109 on file come from ReelShort's
`v-mps.crazymaplestudios.com`), which is Claude's job and needs network access the
sandbox does not currently have. So: you fetch IMDb, Claude fetches faces. They are separate passes.

Save each page as PDF into the Drive folder, same as the 7 Aug batch. Claude applies them
with `generator/apply_imdb_filmography.py`.

---

## Priority 1 — fans know them, the database does not (8)

Zero credits on file. Highest value: fans named them unprompted, so the titles exist and we are missing them.

| # | Actor | Credits | Panel |
|---|---|---|---|
| 1 | Adam Heath | 0 | B-D-E |
| 2 | Andrew Rogers | 0 | Swoon |
| 3 | Ben Schreen | 0 | Meets the Parents |
| 4 | Brando White | 0 | Smokin |
| 5 | Claude George Jr. | 0 | The Eyes Have It |
| 6 | Joshua Dunkin | 0 | Smokin |
| 7 | Nick Milone | 0 | The Eyes Have It |
| 8 | Triston Pons | 0 | Smokin |

## Priority 2 — in the rail, but thin (25)

These already render in the Popular Actors rail. More credits makes each page worth landing on.

| # | Actor | Credits | Panel |
|---|---|---|---|
| 1 | Armand Procacci | 12 | first-name grid |
| 2 | Jackson Tiller | 10 | first-name grid |
| 3 | Jarred Harper | 10 | first-name grid |
| 4 | Sully Christian | 6 | first-name grid |
| 5 | Ben Taylor | 4 | Charming |
| 6 | Carson Polish | 4 | The Eyes Have It |
| 7 | Jacob Tittl | 4 | Chisled |
| 8 | Pierre Longer | 4 | Swoon |
| 9 | Tate Doppler | 4 | Charming |
| 10 | Alex Pychtin | 3 | B-D-E |
| 11 | Connor Tuohy | 3 | Chisled |
| 12 | Grant Lowell Garcia | 3 | The Eyes Have It |
| 13 | Jude Gabrielson | 3 | Smokin |
| 14 | Zane Haney | 3 | Meets the Parents |
| 15 | JT Garcia | 2 | first-name grid |
| 16 | Jesse Katz | 2 | Charming |
| 17 | Marcus Brodie | 2 | B-D-E |
| 18 | Andrew Britton Patterson | 1 | Chisled |
| 19 | Drake Clowes | 1 | first-name grid |
| 20 | Evan Camacho | 1 | Charming |
| 21 | Levi Peterson | 1 | first-name grid |
| 22 | Michael Joseph Nelson | 1 | Meets the Parents |
| 23 | Myles Clohessy | 1 | first-name grid |
| 24 | Ryan Larson | 1 | Swoon |
| 25 | Ryley Schroeder | 1 | Chisled |

## Already have a photo (5) — no photo pass needed

| Actor | Credits |
|---|---|
| Kasey Esser | 17 |
| Aaron Oberst | 8 |
| Neven Tomic | 5 |
| Robbie Silverman | 3 |
| Sam Gousheh | 1 |

---

**Totals.** 38 fan-picked actors · 30 in the rail · 
5 with a photo, 33 without.

Generated from `data/popular_actors.csv`.