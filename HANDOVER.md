# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)** — the CURRENT STATE block and the
   eight newest traps are from 14 Aug and describe exactly this tree.
2. **7. DEA TASKS (what needs Cyan)** — her to-do list, not your work queue. The
   task list below mirrors it; if they ever disagree, ask her which is current.

Then in the repo: `references/adapters.md` **sections 24–26**, and
`REWRITE-QUEUE.md`.

## STATE: COMMITTED BUT NOT PUSHED. Verify, then ask about push.

`main` is **5 commits ahead of origin/main**, working tree clean. Run
`git rev-parse HEAD origin/main` before trusting that count — it was measured at
handover time, not guaranteed later. The five commits are the complete 13–14 Aug
cleanup plus the AI-search work (`e3d309837` data · `5b2adf9a4` generator ·
`8d691aea1` docs · `5b1e980ab` site rebuild · `ff09f731f` AI search). **Pushing is
Cyan's call** — with Netlify publishing PAUSED by her (credits), a push only backs
the work up to GitHub and deploys nothing, but ask rather than assume.

A disaster save point exists OUTSIDE the repo:
`C:\Users\cyanj\DramaEverAfter-backups\dea-savepoint-2026-08-14.zip` (the
gitignored synopsis quarantine + all data CSVs). Refresh it after any pass that
grows the quarantine or reshapes the CSVs — the quarantine file is the one
irreplaceable thing git never sees. Cyan still needs to copy it off this machine.

    3,513 titles · 2,212 actors · 4,574 credits · 3,297 availability · 9,479 pages
    504 of 3,297 title-platform pairs COMPLETE (15%) — only ReelShort clears 50
    The drop from 19% is the CLEANUP: 2,389 copied synopses came off the site

## WHAT THE FIVE COMMITS CONTAIN, shortest version

**pinedrama.com is not a platform** — it is a fan/affiliate site (its own payload
says `"supplier":"reelshort"`; watch buttons are affiliate redirects). Its 73
same-name "twins" were proven the SAME productions (posters: 16 byte-identical,
72 of 73 same pixel dimensions) and merged into their real titles on Cyan's
ruling — 29 credits moved, 16 blank character names filled — then deleted.
**63 titles remain pinedrama-only** and need re-homing (platform + link + poster;
their posters hotlink v.pinedrama.com). `/apps/pinedrama.html` dies with the last
row. Proof of route: Divorced at the Wedding Day → DramaBox, one search.

**No copied copy.** 2,389 scrape-sourced synopses quarantined into
`generator/staging/_quarantined_synopses.json` (gitignored — it is the FACT
SOURCE for rewrites; never reuse its wording). 60 captions rewritten so far.

**Watch buttons are honest.** Official title link → verified platform homepage →
"Platform being verified". Zero `#AFFILIATE-LINK-PENDING` anywhere.

**AI search plumbing is live in the build.** TVSeries schema with cast-as-character
arrays (characterName is the moat field), episode counts, IMDb sameAs, WatchAction
on official links only (pinedrama excluded); FAQPage answering
where-to-watch / episode-count / who-stars from HELD DATA ONLY; Person schema with
nm-id sameAs; robots.txt enacting Cyan's stance (search crawlers welcomed by name,
training-only crawlers refused by name, `Content-Signal: search=yes, ai-train=no`);
llms.txt with counts derived from data. The rule everywhere: a blank field emits
nothing — fabricated schema is worse than none.

## THE CAPTION VOICE IS SETTLED — DO NOT GUESS IT

Cyan's choice, 14 Aug: **warm + bestie, "fun but without the silly ditz."** Full
spec is a standing rule in READ FIRST. Hard rules: **NO DASHES OF ANY KIND**
(hyphens included — rephrase compounds) and **the punchy line LEADS as a hook**
before a newline (build.py renders it as a subheading). Accurate to the story:
plot only from the fact file or the title; one aside per caption, evaluating the
experience, never adding events; heavy material drops the playfulness.

**THE CORPUS IS THE VOICE, NOT THE SPEC.** Read ten of the 60 approved captions in
`generator/captions_2026_08_14.py` / `_b2.py` before writing any. Then **WRITE
FIVE AND SHOW CYAN BEFORE BATCHING** — mandatory, whoever you are. The spec alone
was not enough for the model that wrote it; assume it is not enough for you. A
rejected example sits beside the approved one in the standing rule so the line is
visible.

## THE COMPLETE TASK LIST — every waiting item, nothing omitted

### Claude's queue, in value order

1. **Captions.** 2,374 quarantined titles are captionless (facts in the quarantine
   file, ranked by reach via the `views()` helper — never `int()`), plus the 646
   suspects in REWRITE-QUEUE.md. Batches of ~45 worked well. Calibrate five first
   (see above). Rewritten captions leave the queue automatically (the hook newline
   marks them ours).
2. **The PineDrama 63** — official platform + link + poster per title via
   domain-restricted search (adapters sec 25).
3. **112 platform rows from the company PDFs** (72 titles have NO platform today,
   outside completeness.py's denominator). Matches on tt;
   `parse_imdb_company_pdf.py` prints per-file numbers. Applier still to write —
   model on apply_dramabox_pass.py.
4. **Two confirmed imports** (`staging/samename_rulings_2026-08-14.json`): Fallen
   for My Best Friend's Dad (reelshort, tt35230395) and Evil Stepmom Survival
   Guide (kalostv, tt36129137 — KalosTV's first real entry, Jake Hobbs in cast).
   Pick sensible slugs and tell her.
5. **App Store fallbacks** for the 23 rows with no verified homepage (dramapops 16,
   shortical 4, shorts/playlet/kalostv 1 each). Cyan approved store links as the
   third tier. Verify the store listing's developer name matches the platform.
6. **Actor pages**: fill the TOP actors' holes first (rail actors) — photos, blank
   character names, unread filmographies. Run all lookups in the browser; never
   hand Cyan one.
7. **878-title import queue** from the six company PDFs — CHOSEN, NOT SWEPT.
8. Low: a guard on raw `.title()` for genres (latent). `_dramabox_cache/` and
   `_quarantined_synopses.json` stay gitignored — never commit them. Refresh the
   save-point zip after data passes.

### Cyan's list (mirrors DEA TASKS in Craft)

- **Push, and deploy when Netlify credits allow** — until then the live site
  still carries everything the cleanup removed.
- **Rule the singular/plural tropes**: childhood sweetheart/s, contract lover/s,
  athlete/s — 30 DramaBox tag assignments held until ruled.
- **Copy the save-point zip off this machine** (Drive is the obvious home).
- **Save IMDb pages** for ACTORS-FILMOGRAPHY.md (2,100 unread, ranked by reach) —
  the standing highest-value Cyan-only item. Rail actors first.
- **The 14 fused people.csv rows** (full-width comma, ~28 people in 14 identities).
- **77 pending match_queue rows**, plus 13 blank/unruled.
- **4 ReelShort AI poster checks** (AI-CHECK.md).
- **Homepage URLs** for shorts / playlet / kalostv / dramapops / shortical if she
  spots them — otherwise the App Store fallback covers those buttons.
- **L.J. Shen adaptations official?** (Scandalous, Vicious) — no author credit
  until verified.
- **The two Drive lookup sheets** (DEA Lookups 1 and 2).
- **My Ex's Best Friends platform** (tt36433156) — confirmed a real separate
  show; no platform found by search; waits under the production-house rule.
- **Parked, hers**: GoodShort's ~1,800 castless (deliberately last), the
  verticaldrama.tv data-swap approach, user ratings (spice level first), whether
  upcoming titles get a homepage rail.

## VERIFIED CLEAN, 14 Aug — do not re-audit without cause

Zero referential orphans across all six table relationships; zero duplicate ids
or rows; all 5,946 content pages' internal links resolve (strip query strings
before os.path.exists — browse.html?trope= hits are scanner artifacts); no `<` in
any data field; `&` in 22 titles is legal HTML5; ld+json parses everywhere
including pages with quotes; every meta date derives from the build.

## HOW CYAN WORKS — read this before working

Run lookups yourself in the browser; never hand her one you could run. Calibrate
voice on a SMALL batch before scaling any writing. Fresh saves of the same IMDb
page differ — read the "1-N of M" header and prefer N==M. Tell her before running
anything that rewrites thousands of files, including build.py. Generated output
that looks correct is not evidence that it works — click the thing, measure the
thing, request the URL.

**Captions and synopses are written from scratch. Never reword a platform's or
IMDb's. And keep them accurate to the story.**
