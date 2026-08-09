# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)** — updated 9 Aug, read it all
2. **7. DEA TASKS (what needs Cyan)** — my to-do list, not your work queue
3. **7. DEA POPULAR ACTORS (Reddit fan panels)** — the 38 fan-picked names

Repo is `github.com/Cyanjb/dramaeverafter` (public). **Check out branch `claude/popular-actors-rail`, not `main`** — last session's work is pushed there and unmerged. Starting from main rebuilds the rail from scratch.

## FIRST THING: are you running locally?

Last session was a cloud session and every domain was blocked. The cause is now known and it is NOT the allowlist: **there are two separate allowlists.** Claude desktop's Browser tools list (which already has my-drama.com, reelshort.com, imdb.com) governs sessions running locally on my machine. A session with a cloud icon and a repo badge in the title bar runs in a remote container governed by the environment's network policy at claude.ai/code — a different screen. I added the domains and started a fresh chat, and it was still blocked. That is the proof.

Run this before anything else:

```
curl -s -o /dev/null -w '%{http_code}' https://example.com/
curl -s -o /dev/null -w '%{http_code}' https://my-drama.com/
```

`example.com` is the control. If it fails, the block is blanket — say so and don't test platforms one by one.

**If the network is open, do these two unattended, in this order:**

1. **My Drama descriptions.** ~126 entries are one field short of complete. Our parser dropped the field; My Drama does publish it. adapters.md sec 18. Fill blank-only. This is the single biggest available win.
2. **CDN photo pass for 33 actors.** `data/popular_actors.csv` lists the fan-picked 38; 33 have no `photo_ref`. Hotlink from the platform CDNs — all 109 photos on file come from `v-mps.crazymaplestudios.com` (ReelShort's). **Not TMDB** — $149 commercial, and this site has affiliate links. `generator/harvest_tmdb.py` does not exist and never did, whatever the archive doc says.

Also worth one request while you have network: `/titles/it-was-always-you.html`. It exists only in the 8 Aug batch, so it loading proves the deploy actually ran. Nobody has ever confirmed this visually.

## What last session did

Built the **Popular Actors rail** — live on `/actors/` above the A–Z bar, 30 tiles, ranked from the fan panels rather than view counts. The ranking lives in `data/popular_actors.csv` so it's data, not build logic. The 8 fan-named actors with zero credits are held out (`in_rail=no`) because a tile reading "0 titles" is a dead end. Rebuild touched only `actors/index.html`, so determinism held.

Corrected three stale facts in Craft: the TMDB photo route (wrong twice over), the apex-vs-www item (closed 8 Aug, still marked open), and what the 23% actually measures.

`POPULAR-ACTORS-LOOKUP.md` in the repo root is my IMDb worklist — 8 priority-1 actors with zero credits, 25 priority-2.

## The quality bar — what it actually means

**A complete entry has 2+ cast, a platform, a watch link, and a description.** Currently **723 of 3,199, 23%**. Measure with `generator/completeness.py`.

**The denominator is title-platform pairs, not titles.** completeness.py iterates availability rows, so a title on two platforms counts twice and titles with no platform are excluded entirely. 3,416 titles → 3,154 with a platform → 3,199 rows. Say "title-platform pairs" when quoting the 23%.

**The gap is almost entirely cast, and mostly GoodShort's.** GoodShort is 1,821 of the 3,199 and only 9 are complete — but 1,820 already have a link and a description. It is a pure cast problem. Fixing GoodShort alone would take the site from 23% to roughly 79%.

**But GoodShort is deliberately LAST.** Every entry costs a full IMDb filmography lookup, making it the most expensive completion on the board. Order: My Drama descriptions → CandyJar's 28 (bounded, ends) → GoodShort. A target that ends is worth more than one that doesn't.

## Decisions already made — implement, don't reopen

- **Captions under every Browse poster** — short line always visible, longer on desktop hover. Not swipe. **Every caption written from scratch**; never reword a platform's synopsis. This is the most important caption rule.
- **Upcoming section on the homepage** — `status=upcoming` is already built and live.
- **Ratings/Goodreads — PARKED**, deliberately. Logged in DEA TASKS with the reasoning. Don't start it.
- **verticalvault.app** killed "actor depth is our moat". **verticaldrama.tv** harvesting is refused permanently (EU Article 4). Targeted gap-fills fine, systematic extraction not.

## Two data facts that will bite you

- `view_count` is a **display string** (`"218.1M"`), not a number. `int()` silently returns 0 and every actor ranks equal. 2,340 of 2,374 populated rows are non-numeric.
- `spice_level` exists as a column and is **blank on all 3,416 titles**. Top-level filter for this audience, unusable today, and no platform publishes it.

## Waiting on me

- Two Google Sheets in the "Drama Ever After" Drive folder: 54 same-or-different rulings, 39 CandyJar cast lookups
- IMDb PDFs for the actors in `POPULAR-ACTORS-LOOKUP.md`
- One PineDrama page compared to its ReelShort twin — settles 73 queued titles
- 4 ReelShort posters checked for the AI badge

## How I work

Don't ask me to approve routine decisions like slugs — pick sensible ones and tell me. Do ask when something is genuinely one-way or a judgement call about the brand. If you can't verify something, say so plainly rather than guessing. Generated output that looks correct is not evidence that it works — click the thing, measure the thing, request the URL.
