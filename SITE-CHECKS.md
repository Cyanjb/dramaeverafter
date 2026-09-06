# SITE-CHECKS: what must always work on dramaeverafter.com

Two layers, and they are twins. This file is the plain-words promise;
`generator/check_site.py` is the same promise as code, run automatically
after every build in the Sunday workflow (a failure stops the publish and
shows red on the Actions page). When something new must keep working, it
gets a line here AND a check there, in the same commit.

Written 6 Sep 2026, the day search silently failed on "girls" vs "Girl's".

## Checked automatically, every build

**Data integrity**
- No duplicate title_ids in titles.csv.
- Every availability, tropes, credits and pinned row points at a real
  title; every credit points at a real person.

**Search** (broke 6 Sep, fixed same day)
- Every title and actor in search-index.json has a live page.
- Browse and the actors page carry the forgiving search: apostrophes
  (straight or curly), accents, punctuation and word order are all
  ignored, and words can match in any order. "a zombie girls journey
  home" must find "A Zombie Girl's Journey Home".
- The Python normalizer in build.py and the JavaScript one shipped to
  browsers agree character for character (they must stay identical).

**Homepage**
- Rail order: Most watched first, New and trending directly under it
  (Cyan, 6 Sep).
- The trending rail holds ~12 titles, ranked by real view growth from
  the weekly snapshots.
- Every pin in data/pinned.csv leads the rail, in file order.

**Pages and links**
- tropes/index, platforms, my-list, contact, 404, robots.txt and
  llms.txt all exist; contact still carries cyan@dramaeverafter.com.
- Every internal link on the entry pages (home, browse, tropes, actors,
  platforms, contact) resolves to a real file.
- Every trope chip on the tropes index has its page.

**Sitemap and noindex** (the 1 Sep Google demotion recovery)
- Sitemap URLs: on-domain, every one has a file, none carries a noindex
  meta. Thin pages are noindexed AND out of the sitemap, together.

**Redirects**
- _redirects never contains a forced 301!/302! (verified 5 Sep: with
  Netlify Pretty URLs on, a forced rule loops forever).

## Not checkable by script - Cyan's 5-minute click-through

Do this after any big change, on the live site, hard refresh first:

1. Homepage: rails look right, posters load, your pinned title leads
   New and trending.
2. Search "a zombie girls journey home" (no apostrophe, on purpose)
   from the header box: the title comes up.
3. Click a trope chip, a platform tile, an actor: real pages, posters.
4. Star a title, open My List: it is there. Unstar: it is gone.
5. Contact page: the email links open with cyan@dramaeverafter.com.
6. Phone check: browse and a title page on your phone, nothing overflows.

## Known-broken or waiting, so a check would just be red

- Extensionless redirects are DORMANT until Netlify Pretty URLs is
  switched off (Cyan's toggle, see HANDOVER.md).
- scrape_reelshort.py's detail/wanted route parses empty since ~5 Sep
  (movie-page __NEXT_DATA__ changed); tags/genres routes carry the
  weekly run meanwhile.
