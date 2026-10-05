## ReelShort weekly scrape, 2026-10-05

| | |
|---|---|
| Requests | 1757 |
| Books seen | 2764 |
| Known titles refreshed | 945 |
| View counts that moved | 611 |
| Snapshot rows written | 987 |
| New titles created | 42 |
| Held for a ruling (match_queue) | 1 |
| Credits added | 15 |
| New people (actor pages) created / close names held for a ruling | 0 / 0 |
| Episode counts / posters / links / years filled | 2 / 0 / 0 / 1 |
| Delisted (404, not deleted) | 7 |
| Catalogue only (genre sweep or sitemap, under 10M views), not imported | 1680 |
| Excluded as unscripted (ReelTalk and kin) | 84 |
| Skipped: no title or slug / URL unconfirmed | 0 / 2 |
| ReelShort rows still older than 45 days | 7 |
| Rulings applied from the wanted file / lines still unmatched | 0 / 17 |
| Tropes from ReelShort's tag pages (vocabulary only) / tag names unknown | 148 / 294 |
| Umbrella tropes added | high fantasy 80 |
| Linked on Cyan's confirmed_same rulings | 0 |
| Platform page says AI-generated, labelled ai=yes | 21 |
| Scrape errors | 56 |

Routes: detail {"delisted": 7, "failed": 14, "ok": 439, "targets": 460}, fandom {"hrefs": 41, "posts": 100, "status": 200}, genres {"books": 2110, "failed": 0, "pages": 267, "pages_listed": 7}, home {"books": 129, "hrefs": 0, "status": 200}, tags {"books": 614, "failed": 1, "pages": 987, "pages_listed": 939}, wanted {"file": "reelshort_wanted.txt", "held": 142, "resolved": 0, "searched": 41, "unresolved": 41, "urls": 30}

### New titles (needs_check): each one needs a caption

These are live with no synopsis of ours. Platform text is never copied (Cyan, 14 Aug). The synopsis each page published is banked in the staging JSON as the fact source; `caption_pipeline.py next` picks them up by reach and the /dea-captions skill writes them for Cyan's review.

- Dirty Games (`dirty-games`) 11.1M via detail, home
- Fighting the Fire (`fighting-the-fire`) 2.8M via genres, home
- Banging Lanie (`banging-lanie`) 2.3M via genres, home
- Secrets and Soulmates (`secrets-and-soulmates`) 17.9M via detail, fandom
- Charmed to Meet You, Too (`charmed-to-meet-you-too`) 11.8M via detail, fandom
- On the Day of the Broken Engagement, I Married a Half-Blood Dragon (`on-the-day-of-the-broken-engagement-i-married-a-half-blood-dragon`) 12.2M via genres
- When The Black Out Comes (`when-the-black-out-comes`) 7.8M via fandom, genres
- The Wife He Gave Away (`the-wife-he-gave-away`) 12.2M via genres
- Trash Boy's Super Watch (`trash-boy-s-super-watch`) 7.0M via genres, home
- Divorced, She Reclaimed Her Empire (`divorced-she-reclaimed-her-empire`) 8.3M via genres, home
- The Godfather’s Hidden Wife (`the-godfather-s-hidden-wife`) 2.0M via genres, home
- Mated to My Sworn Enemy (`mated-to-my-sworn-enemy`) 5.5M via detail, home
- The Don's Fatal Tenderness (`the-don-s-fatal-tenderness`) 828.5K via detail, home
- Prep School Pop Star! (`prep-school-pop-star`) 2.3M via genres, home
- The School for Bad Boys: Bully in the Closet (`the-school-for-bad-boys-bully-in-the-closet`) 469.7K via tags
- God of Wrath (`god-of-wrath`) 477.3K via tags
- The School for Bad Boys: S*x Lessons (`the-school-for-bad-boys-s-x-lessons`) 472.1K via genres, tags
- Rejected Luna is His Fated Mate (`rejected-luna-is-his-fated-mate`) 13.4M via detail, home
- My Twins Picked a Billionaire Dad (`my-twins-picked-a-billionaire-dad`) 1.4M via detail, home
- Swapped Bride: Awakening of the True Princess (`swapped-bride-awakening-of-the-true-princess`) 6.8M via genres, home
- CLAIMED BY MY ALPHA STEPBROTHER (`claimed-by-my-alpha-stepbrother`) 3.9M via genres, home
- His Defective Robot Boyfriend (`his-defective-robot-boyfriend`) 812.1K via detail, home
- The Swap Game: Claimed by His Uncle (`the-swap-game-claimed-by-his-uncle`) 1.3M via detail, home
- The Big Wife's Revenge: From Model to Queen (`the-big-wife-s-revenge-from-model-to-queen`) 4.5M via genres, home
- The Odyssey: A Warrior King's Homecoming (`the-odyssey-a-warrior-king-s-homecoming`) 841.4K via detail, home
- Don't Wake the Dead Man (`don-t-wake-the-dead-man`) 3.0M via detail, home
- Hunted by the Alpha (`hunted-by-the-alpha`) 2.9M via detail, home
- The School for Bad Boys (`the-school-for-bad-boys`) 2.3M via genres, tags
- The Alpha's Forbidden Bunny (`the-alpha-s-forbidden-bunny`) 1.1M via detail, home
- Second Chance at Life (`second-chance-at-life`) 1.0M via genres, home
- Forward, Without Him (`forward-without-him`) 12.8M via detail, home
- The Alpha Who Let His Luna Die (`the-alpha-who-let-his-luna-die`) 1.3M via detail, home
- The Alpha's Secret Pup (`the-alpha-s-secret-pup`) 855.9K via detail, home
- Wrong Door Right Girl (`wrong-door-right-girl`) 730.3K via detail, home
- Forced to Bear the Dragon’s Heir (`forced-to-bear-the-dragon-s-heir`) 1.1M via detail, home
- The CEO's Genius Baby (`the-ceo-s-genius-baby`) 1.0M via detail, home
- The Girl He Lost in the Flames (`the-girl-he-lost-in-the-flames`) 2.1M via detail, home
- After His Number Disappeared (`after-his-number-disappeared`) 1.1M via detail, home
- Saved My Life, No More Love (`saved-my-life-no-more-love`) 1.4M via detail, home
- I'll Never See You Again (`i-ll-never-see-you-again`) 4.2M via detail, home
- Dear Brother, Your Regret Came Too Late (`dear-brother-your-regret-came-too-late`) 2.7M via genres, home
- The Boss Forces My Heart. (`the-boss-forces-my-heart`) 7.7M via detail, home

### Held for Cyan's ruling

- 'Space Cowboy's Royal Escort' vs existing `space-cowboy-s-royal-escort`: same slug

### Delisted on ReelShort (404), left in place

- `mafia-boss-owns-my-body` https://www.reelshort.com/movie/mafia-boss-owns-my-body-6923c6289c16eb72620ef564
- `the-heat-after-the-ac-died` https://www.reelshort.com/movie/the-heat-after-the-ac-died-6a4358c4abdd23a03d0d6563
- `uncle-i-don-t-want-you-anymore` https://www.reelshort.com/movie/uncle-i-don-t-want-you-anymore-6a63772875b2eafae30ae376
- `the-new-ceo-turns-out-to-be-my-gynecologist` https://www.reelshort.com/movie/the-new-ceo-turns-out-to-be-my-gynecologist-6a7aceebbdf01d86f40cb0e2
- `my-two-dangerous-roommates-crave-me` https://www.reelshort.com/movie/my-two-dangerous-roommates-crave-me-6a6c022bedfbef3f380fbfb9
- `the-summer-the-ac-broke` https://www.reelshort.com/movie/the-summer-the-ac-broke-6a44c5b8c3d931368c03b98b
- `our-camp-night-went-wrong` https://www.reelshort.com/movie/our-camp-night-went-wrong-6a7dd5b4b2c257cfb60da399

### Wanted-file lines that matched no held title (still waiting)

- Seducing the God of Olympus
- The Dragon Lord's Regret
- Light and Roses: Tears of a Vampire
- I Rejected My Alpha After 12 Years
- Billionaire Luna: Taming My Alpha Mate
- Alpha at My Wedding
- The Summer the Sea Broke
- Sugar Daddy: Sweet Pursuit
- Unconditionally Loved by the Billionaire
- The Mongrel Husband Bought for $5,000
- Taming the Lion
- The Mafia Boss Has a Gun
- Darling Don't Run
- Legally Bound
- Unexpected
- Married to a Billionaire Nurse
- Two Snakes, One Mate

### ReelShort tag names not in our vocabulary (Cyan decides; count of books)

- drama (312)
- Romance (146)
- Secret Reveal (140)
- Contemporary (122)
- Romantic (121)
- Drama (107)
- Modern (105)
- Self-growth (91)
- Feel-Good (85)
- Fantasy (73)
- Emotional (71)
- Secret (69)
- USA (60)
- Sabotaging (59)
- Fated Lovers (58)
- Hooking-up (57)
- Animation (55)
- Competition (45)
- Mansion (39)
- Love-Hate (36)
- Villa (35)
- China (35)
- Looking-for-Love (34)
- Protective Husband (32)
- Heartfelt (32)
- Super Warrior (31)
- Morals & Ethics (30)
- Breakup (28)
- Engagement Breakup (27)
- Bittersweet (27)
- Supernatural (27)
- Banquet (26)
- Genius Babies (26)
- Charming (25)
- Damsel (24)
- survival (24)
- Conspiracy (24)
- Hospital (22)
- Survival (22)
- Exciting (21)

### Labelled AI this run: ReelShort's own page says AI-generated

- `after-his-number-disappeared`
- `don-t-wake-the-dead-man`
- `forced-to-bear-the-dragon-s-heir`
- `forward-without-him`
- `his-defective-robot-boyfriend`
- `hunted-by-the-alpha`
- `i-ll-never-see-you-again`
- `mated-to-my-sworn-enemy`
- `my-twins-picked-a-billionaire-dad`
- `rejected-luna-is-his-fated-mate`
- `saved-my-life-no-more-love`
- `the-alpha-s-forbidden-bunny`
- `the-alpha-s-secret-pup`
- `the-alpha-who-let-his-luna-die`
- `the-boss-forces-my-heart`
- `the-ceo-s-genius-baby`
- `the-don-s-fatal-tenderness`
- `the-girl-he-lost-in-the-flames`
- `the-odyssey-a-warrior-king-s-homecoming`
- `the-swap-game-claimed-by-his-uncle`
- `wrong-door-right-girl`

261 ReelShort tag listing pages discovered (add to reelshort_tags.txt to sweep them).

### Credits added (exact name, one person)

- His Daughter Chose Me: Marc Hermann
- The Legend in Disguise: Marc Hermann
- The School for Bad Boys: Bully in the Closet: Declan Clifford
- The School for Bad Boys: Bully in the Closet: Cayman Cardiff
- The School for Bad Boys: Bully in the Closet: Autumn Noel
- The School for Bad Boys: Bully in the Closet: Greg Duffy
- The School for Bad Boys: Bully in the Closet: Ben Ubinas
- God of Wrath: Savannah Coffee
- God of Wrath: Nate Flores
- The School for Bad Boys: S*x Lessons: Tate Doppler
- The School for Bad Boys: S*x Lessons: Autumn Noel
- The School for Bad Boys: Autumn Noel
- The School for Bad Boys: Declan Clifford
- The School for Bad Boys: Greg Duffy
- The School for Bad Boys: Ben Ubinas

### Errors

- {"page": 1, "route": "tags", "status": 404, "url": "https://www.reelshort.com/tags/movie-actresses/nicole-provonsil-movies-676d210a4582b53a1408183e"}
- {"query": "Seducing the God of Olympus", "route": "wanted", "status": "search: 2 exact of 12 results"}
- {"query": "The Dragon Lord's Regret", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Light and Roses: Tears of a Vampire", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "I Rejected My Alpha After 12 Years", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Billionaire Luna: Taming My Alpha Mate", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Alpha at My Wedding", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "The Summer the Sea Broke", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Honey Trapped, My Fiance's Billionaire Rival", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Miss CEO's Baby Daddy", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "The Merchant of Death", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Carrying His Triplets", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Becoming His Wife", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "American Sniper", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "The Last Round", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Step Aside, I'm the King", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Djinn", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Runaway Single Mom", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Safe in His Arms", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Abandoned by the Dragon King", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Bound by Beauty", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Sugar Daddy: Sweet Pursuit", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Unconditionally Loved by the Billionaire", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "The Mongrel Husband Bought for $5,000", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Taming the Lion", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Waking Up Pregnant", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "The Mafia Boss Has a Gun", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Darling Don't Run", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Legally Bound", "route": "wanted", "status": "search: 0 exact of 12 results"}
- {"query": "Unexpected", "route": "wanted", "status": "search: 0 exact of 12 results"}
