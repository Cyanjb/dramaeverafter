# DramaEverAfter — handover for the next session

Paste this as your first message.

---

We're continuing work on DramaEverAfter. Read these Craft docs first, in this order:

1. **7. DEA READ FIRST (Current State + Traps)** — the CURRENT STATE block and the
   eight new traps at the end are from 14 Aug and describe exactly this tree.
2. **7. DEA TASKS (what needs Cyan)** — her to-do list, not your work queue.

Then in the repo: `references/adapters.md` **sections 24–26** (all new), and
`REWRITE-QUEUE.md`.

## THE ENTIRE 13–14 AUG CLEANUP IS UNCOMMITTED, ON PURPOSE

Cyan said "we will commit last." The working tree holds ALL of it: the quarantine,
the PineDrama unravel, 73 title deletions, 60 new captions, the hook renderer, the
homepage fallback, seven new generator scripts, adapters sections 24–26. `git status`
will look alarming. It is not drift — it is one session's work awaiting her commit
call. **Committing is the first thing to settle with her.** Netlify publishing is
also PAUSED by her (low credits), so nothing local is live regardless.

    3,513 titles · 2,212 actors · 4,574 credits · 3,297 availability · 9,479 pages
    504 of 3,297 title-platform pairs COMPLETE (15%) — only ReelShort clears 50
    The drop from 19% is the CLEANUP: 2,389 copied synopses came off the site

## WHAT HAPPENED, SHORTEST VERSION

**pinedrama.com is not a platform.** It is a fan/affiliate site: its own payload
says `"supplier":"reelshort"`, its watch buttons are affiliate redirects. We carried
it as a platform since 20 Jul because its links returned 200 — a live link is not a
legitimate link. All 73 of its same-name "twins" were proven the SAME productions
(poster comparison: 16 byte-identical, 72 of 73 same pixel dimensions; same
characters in the synopses) and merged into their real titles on Cyan's ruling.
**63 titles remain attributed to pinedrama only** — each needs its official platform
found (the restricted-domain search route, adapters sec 25, resolves them fast) and
its poster re-sourced, since those 63 posters hotlink `v.pinedrama.com`.
`/apps/pinedrama.html` dies when the last row is re-homed.

**No copied copy, anywhere.** 2,389 scrape-sourced synopses were quarantined into
`generator/staging/_quarantined_synopses.json` (gitignored; it is the FACT SOURCE
for rewrites — never reuse its wording). 60 captions are rewritten so far.

## THE CAPTION VOICE IS SETTLED — DO NOT GUESS IT

Cyan chose it from four sample registers on 14 Aug: **warm + bestie, "fun but
without the silly ditz."** The full spec is a standing rule in READ FIRST. The two
hard rules: **NO DASHES OF ANY KIND** (hyphens included — rephrase compounds), and
**the punchy line LEADS as a hook** on its own first line before a newline;
build.py renders it as a subheading. A first draft in a dry/wry register was
rejected — the spec exists so that never repeats. **Keep captions accurate to the
story**: plot only from the fact file or the title; the one aside per caption
evaluates the experience, never adds events; heavy material drops the playfulness.

**THE CORPUS IS THE VOICE, NOT THE SPEC.** Read ten of the 60 approved captions in
`generator/captions_2026_08_14.py` / `_b2.py` before writing any. Then WRITE FIVE
AND SHOW CYAN BEFORE BATCHING — mandatory, whoever you are. The spec alone was not
enough for the model that wrote it, so assume it is not enough for you.

## THE COMPLETE TASK LIST — every waiting item, nothing omitted

The same list lives as checkboxes in Craft's **DEA TASKS** doc (updated 14 Aug).
If the two ever disagree, ask Cyan which is current rather than picking one.

### Claude's queue, in value order

1. **Commit** (three clean commits: data / code / docs) the moment Cyan says the
   word — currently blocked ONLY on her say-so. Deploy is her button after.
2. **Captions.** 2,374 quarantined titles are captionless (facts in the gitignored
   quarantine file, ranked by reach via the `views()` helper), plus the 646
   suspects in REWRITE-QUEUE.md. Batches of ~45 worked well. Voice spec is a
   standing rule in READ FIRST; rewritten captions drop off the queue
   automatically (the hook newline marks them ours). Keep them ACCURATE TO THE
   STORY.
3. **The PineDrama 63** — official platform + link + poster per title, one
   restricted-domain search each (adapters sec 25). Their posters currently
   hotlink v.pinedrama.com, and `/apps/pinedrama.html` (still in the sitemap)
   dies when the last row is re-homed. One resolved already as proof of route:
   Divorced at the Wedding Day → DramaBox.
4. **112 platform rows from the company PDFs** (72 of those titles have NO
   platform today, so they sit outside completeness.py's denominator). Matches on
   tt; `parse_imdb_company_pdf.py` prints per-file numbers. Applier still to be
   written — model it on apply_dramabox_pass.py.
5. **Two confirmed imports** from `staging/samename_rulings_2026-08-14.json`:
   Fallen for My Best Friend's Dad (reelshort, tt35230395) and Evil Stepmom
   Survival Guide (kalostv, tt36129137 — KalosTV's first real entry, Jake Hobbs
   in cast). Pick sensible slugs and tell her.
6. **App Store fallbacks** for the 23 rows with no verified homepage (dramapops
   16, shortical 4, shorts/playlet/kalostv 1 each). Cyan approved store links as
   the third tier: title link → homepage → store page. Verify the developer name
   on the store listing matches the platform before wiring it.
7. **Actor pages**: fill the TOP actors' holes first (the rail actors), not raw
   reach order — photos, blank character names, unread filmographies. Run all
   lookups in the browser yourself; never hand Cyan one.
8. **878-title import queue** from the six company PDFs — CHOSEN, NOT SWEPT:
   newest / most popular / coming soon only, per the standing rule.
9. Low housekeeping: a guard on raw `.title()` for genres (latent, currently
   harmless). `_dramabox_cache/` (19MB) and `_quarantined_synopses.json` are
   gitignored ON PURPOSE — never commit them.

### Cyan's list (mirrors DEA TASKS in Craft — hers to action, not a session's)

- **Commit + deploy the 14 Aug cleanup** (new, High): until both happen the live
  site still carries everything the cleanup removed.
- **Rule the singular/plural tropes**: childhood sweetheart/s, contract lover/s,
  athlete/s — 30 DramaBox tag assignments held until ruled.
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
- **My Ex's Best Friends platform** (tt36433156) if she spots which app carries
  it — confirmed a real separate show, no platform found by search.
- **Parked, hers**: GoodShort's ~1,800 castless (deliberately last), the
  verticaldrama.tv data-swap approach, user ratings (spice level first), whether
  upcoming titles get a homepage rail.

## VERIFIED CLEAN, 14 Aug — do not re-audit without cause

Referential integrity zero-orphan across all six checks; zero duplicate ids or
rows; all 5,946 content pages' internal links resolve (the 103 "broken"
browse.html?trope= hits were a scanner artifact — strip query strings before
os.path.exists); no `<` anywhere in data; `&` in 22 titles is legal HTML5 and
renders fine; ld+json parses with quotes escaped; every page's meta date now
derives from the build (was hardcoded "July 2026" for a month).

## HOW CYAN WORKS — additions this session

Run lookups yourself in the browser; she should never be handed one you could run.
Calibrate voice on a SMALL batch before scaling any writing. Fresh saves of the
same IMDb page differ — read the "1-N of M" header and prefer N==M. And the
standing rule that paid for itself twice today: generated output that looks correct
is not evidence that it works — click the thing, measure the thing.
