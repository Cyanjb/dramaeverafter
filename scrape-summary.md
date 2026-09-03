## ReelShort weekly scrape, 2026-09-03

| | |
|---|---|
| Requests | 287 |
| Books seen | 2324 |
| Known titles refreshed | 733 |
| View counts that moved | 50 |
| Snapshot rows written | 17 |
| New titles created | 16 |
| Held for a ruling (match_queue) | 2 |
| Credits added | 0 |
| Episode counts / posters / links / years filled | 8 / 0 / 0 / 0 |
| Delisted (404, not deleted) | 0 |
| Catalogue only (genre sweep or sitemap, under 10M views), not imported | 1562 |
| Excluded as unscripted (ReelTalk and kin) | 10 |
| Skipped: no title or slug / URL unconfirmed | 1 / 2 |
| ReelShort rows still older than 45 days | 9 |
| Rulings applied from the wanted file / lines still unmatched | 68 / 17 |
| Tropes from ReelShort's tag pages (vocabulary only) / tag names unknown | 68 / 2 |
| Umbrella tropes added | high fantasy 186 |
| Linked on Cyan's confirmed_same rulings | 4 |
| Platform page says AI-generated, no ruling yet | 0 |
| Scrape errors | 41 |

Routes: detail {"delisted": 0, "failed": 6, "ok": 2, "targets": 8}, genres {"books": 1582, "failed": 4, "pages": 233, "pages_listed": 7}, wanted {"file": "reelshort_wanted.txt", "held": 122, "resolved": 15, "searched": 46, "unresolved": 31, "urls": 2}

### New titles (needs_check): each one needs a caption

These are live with no synopsis of ours. Platform text is never copied (Cyan, 14 Aug). The synopsis each page published is banked in the staging JSON as the fact source; `caption_pipeline.py next` picks them up by reach and the /dea-captions skill writes them for Cyan's review.

- Divorced and Desired! My Trio of Elite Suitors (`divorced-and-desired-my-trio-of-elite-suitors`) 19.2M via genres
- Late Bloomer (`late-bloomer`) 2.2M via genres, wanted
- Legally Bound To Love (`legally-bound-to-love`) 15.9M via wanted
- The Rabbit Bride Who Rejected Her Alpha King (`the-rabbit-bride-who-rejected-her-alpha-king`) 2.2M via wanted
- My Two Dangerous Roommates Crave Me (`my-two-dangerous-roommates-crave-me`) 3.3M via wanted
- Daddy We're Done (`daddy-we-re-done`) 4.3M via wanted
- My Fireplace Ships to Dragon Realm (`my-fireplace-ships-to-dragon-realm`) 6.2M via wanted
- Caught! The Ruthless Alpha's Runaway Luna (`caught-the-ruthless-alpha-s-runaway-luna`) 2.7M via wanted
- The Dragon's Return: Reclaiming My Throne (`the-dragon-s-return-reclaiming-my-throne`) 775.3K via wanted
- My Boss Is My Secret Online Dom (`my-boss-is-my-secret-online-dom`) 792.1K via genres, wanted
- CEO's Irresistible Wet Nurse (`ceo-s-irresistible-wet-nurse`) 840.2K via wanted
- Faked My Death, Destroyed The Billionaire (`faked-my-death-destroyed-the-billionaire`) 878.3K via wanted
- 100-Day Contract：Mafia’s Dangerous Desire (`100-day-contract-mafia-s-dangerous-desire`) 2.0M via wanted
- Fake Husband, Hidden King (`fake-husband-hidden-king`) 2.5M via genres, wanted
- Love Has A Deadline (`love-has-a-deadline`) 373.6K via wanted
- He Paid for One Night, Then Wanted Forever (`he-paid-for-one-night-then-wanted-forever`) 1.0M via wanted

### Held for Cyan's ruling

- 'CEO Queen: A Mother’s Revenge' vs existing `ceo-queen-a-mother-s-revenge`: same slug
- 'Luna Reborn: Alpha's Second Chance' vs existing `luna-reborn-alpha-s-second-chance`: same slug

### Rulings applied (Cyan, via the wanted file)

- `a-cinderella-for-wolf-king` ai=yes
- `the-lycan-s-savage-luna` ai=yes
- `breathe` trope +age gap
- `rent-a-mom-for-the-billionaire-twins` trope +age gap
- `love-has-a-deadline` trope +high fantasy
- `pucked-in-the-friend-zone` ai=no
- `keeping-the-cowboy-s-baby` ai=no
- `keeping-the-cowboy-s-baby` trope +cowboy
- `keeping-the-cowboy-s-baby` trope +forbidden love
- `the-alpha-and-his-nanny-luna` trope +werewolf
- `the-alpha-and-his-nanny-luna` trope +luna
- `the-ugly-girl-turned-pretty` ai=yes
- `the-ugly-girl-turned-pretty` trope +playing dumb
- `hate-to-love-you` ai=no
- `make-my-cheating-husband-pay-the-price` ai=yes
- `make-my-cheating-husband-pay-the-price` trope +billionaire
- `100-day-contract-mafia-s-dangerous-desire` ai=yes
- `100-day-contract-mafia-s-dangerous-desire` trope +mafia
- `100-day-contract-mafia-s-dangerous-desire` trope +revenge
- `my-boss-is-my-secret-online-dom` ai=yes
- `my-boss-is-my-secret-online-dom` trope +playing dumb
- `how-to-land-a-movie-star` ai=no
- `how-to-land-a-movie-star` trope +workplace
- `how-to-land-a-movie-star` trope +rom-com
- `the-fake-dating-spell` ai=yes
- `the-fake-dating-spell` trope +young adult
- `the-fake-dating-spell` trope +fake dating
- `my-fireplace-ships-to-dragon-realm` trope +dragon
- `my-fireplace-ships-to-dragon-realm` trope +high fantasy
- `nanny-to-my-hot-bully` ai=no
- `nanny-to-my-hot-bully` trope +young adult
- `the-tutor-trap` ai=no
- `once-upon-a-breakup` ai=no
- `once-upon-a-breakup` trope +young adult
- `the-seduction-game` ai=no
- `the-seduction-game` trope +young adult
- `the-rabbit-bride-who-rejected-her-alpha-king` ai=yes
- `the-rabbit-bride-who-rejected-her-alpha-king` trope +playing dumb
- `offside-with-the-hockey-star` ai=yes
- `offside-with-the-hockey-star` trope +young adult
- `offside-with-the-hockey-star` trope +love triangle
- `my-two-dangerous-roommates-crave-me` ai=yes
- `my-two-dangerous-roommates-crave-me` trope +bl
- `my-two-dangerous-roommates-crave-me` trope +love triangle
- `blitzed-by-my-rival-s-obsession` trope +bl
- `daddy-we-re-done` ai=yes
- `your-husband-is-mine` ai=no
- `your-husband-is-mine` trope +billionaire
- `he-paid-for-one-night-then-wanted-forever` ai=yes
- `he-paid-for-one-night-then-wanted-forever` trope +billionaire
- `the-dragon-s-return-reclaiming-my-throne` trope +dragon
- `the-dragon-s-return-reclaiming-my-throne` trope +high fantasy
- `chained-by-hades-the-underworld-king` trope +high fantasy
- `reborn-to-love-mr-right` ai=no
- `hating-and-loving-my-adopted-brother` ai=no
- `the-virgin-s-bucket-list` ai=no
- `legally-bound-to-love` ai=no
- `faked-my-death-destroyed-the-billionaire` ai=yes
- `faked-my-death-destroyed-the-billionaire` trope +billionaire
- `faked-my-death-destroyed-the-billionaire` trope +revenge
- `caught-the-ruthless-alpha-s-runaway-luna` ai=yes
- `caught-the-ruthless-alpha-s-runaway-luna` trope +werewolf
- `fake-husband-hidden-king` ai=yes
- `fake-husband-hidden-king` trope +billionaire
- `fake-husband-hidden-king` trope +secret identity
- `a-cinderella-for-wolf-king` trope +werewolf
- `a-cinderella-for-wolf-king` trope +fated mates
- `the-alpha-king-sold-me-to-the-war-god` trope +werewolf

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

- drama (201)
- survival (1)

### Linked to ReelShort on Cyan's confirmed_same rulings

- `pregnant-by-the-billionaire` https://www.reelshort.com/movie/pregnant-by-the-billionaire-669ff9a361704e7f8e045c5f
- `the-heiress-blacklisted-her-husband` https://www.reelshort.com/movie/the-heiress-blacklisted-her-husband-677db481a3cc638b8f0d8a59
- `i-m-the-one-in-charge` https://www.reelshort.com/movie/i-m-the-one-in-charge-69ae3bf4fe655b0dec0c3f53
- `sweet-temptation` https://www.reelshort.com/movie/sweet-temptation-6a7d21ead4f206c4400f1499

98 ReelShort tag listing pages discovered (add to reelshort_tags.txt to sweep them).

### Errors

- {"page": 1, "route": "tags", "status": 404, "url": "https://www.reelshort.com/tags/movie-moods/k%C4%B1yamet-movies-676d210d4582b53a14081a1e"}
- {"page": 1, "route": "tags", "status": 404, "url": "https://www.reelshort.com/tags/movie-moods/%E6%AE%AD%E5%B1%8D-movies-676d210d4582b53a14081a0e"}
- {"page": 4, "route": "tags", "status": 404, "url": "https://www.reelshort.com/tags/movie-themes/survival-movies-676d210d4582b53a140819ca"}
- {"page": 1, "route": "tags", "status": 404, "url": "https://www.reelshort.com/tags/movie-moods/cult-movies-676d210d4582b53a140819e1"}
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
