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
- The extensionless 301 rule exists in the file for all five page
  families (titles, actors, tropes, where-to-watch, apps). It is
  checked so nobody deletes it, NOT because it works: see the
  known-broken list below. It fires only for paths with no file.

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

- EVERY PAGE IS STILL REACHABLE AT TWO URLs, and switching off
  Netlify Pretty URLs on 10 Sep did NOT fix it. Verified live that
  day: /actors/blake-manning.html returns 200 with no redirect, so
  the toggle did its own job, and /search (no file) 301s correctly,
  so the rules are being read. But /actors/blake-manning still
  returns 200. Netlify serves foo.html at /foo by DEFAULT, which is
  not the Pretty URLs setting and has no toggle, and our rules are
  non-forced, so an existing file beats them every time.
  A forced 301! is the only rule type that wins, and it very likely
  loops for a reason the 5 Sep note got wrong: :slug matches one
  whole path segment, and "blake-manning.html" IS one whole segment,
  so the target re-matches the same rule and goes to .html.html
  forever. That is independent of Pretty URLs. UNTESTED, and the
  cheap test is a forced rule on /apps/ alone (16 pages, one revert).
  If it does loop, _redirects cannot express this and the options are
  a Netlify edge function (skip any path whose last segment has a
  dot) or leaving the canonical tags to do it.
  Cyan's call, 10 Sep: leave it. The canonical tag on every page
  points at the .html form and is the supported way to say so. Google
  is partly ignoring it (the 10 Sep drilldown found 456 extensionless
  duplicates in "Crawled - currently not indexed", and it ranked
  /actors/blake-manning at position 1), so this stays a live suspect
  in the 29 Aug deindexing, just not one we are acting on today.
- scrape_reelshort.py's detail/wanted route parses empty since ~5 Sep
  (movie-page __NEXT_DATA__ changed); tags/genres routes carry the
  weekly run meanwhile.
