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
- Character names are searchable (10 Sep): "elijah baran" finds Djinn
  Under Contract on Browse and Eric Guilmette on the actors page, and
  characters.html lists every named character with working links.

**Homepage**
- Rail order: Most watched right now first, New and trending directly under
  it, then Faces you keep seeing (Cyan, 6 and 13 Sep).
- The trending rail holds ~12 titles, ranked by real view growth from
  the weekly snapshots.
- Every pin in data/pinned.csv leads the rail, in file order.
- Pick of the week (13 Sep): the newest row of data/picks.csv shows as a
  bordered blush card at the BOTTOM of the homepage, after the last
  poster rail and above the footer, its left edge lined up with the
  rails. Its title page carries the chip. One sentence, a fixed plum
  pill label, no gold button. A link with an expiry is dropped by the
  build once it passes and hidden in the browser the minute it does, so
  a dead offer never shows.

**Watch buttons** (13 Sep)
- A title on more than one app shows a button per app, the first gold and
  the rest wine outline. An app appears as plain text only when nothing
  can be linked: no deep link and no verified homepage (Playlet,
  Shortical, Shorts, KalosTV, DramaPops). A dead button is worse.

**Posters** (Cyan's standing rule, 13 Sep)
- Every poster is 3:4, because that is what the platforms ship: ReelShort,
  GoodShort, NetShort, PineDrama and DramaBox all serve 3:4 art. Posters
  stay true to their source and are never cropped to a prettier shape. A
  design handoff asking for 9:16 or 2:3 does not override this.

**Pages and links**
- tropes/index, platforms, my-list, contact, 404, robots.txt and
  llms.txt all exist; contact still carries cyan@dramaeverafter.com.
- Every internal link on the entry pages (home, browse, tropes, actors,
  platforms, contact) resolves to a real file.
- Every trope chip on the tropes index has its page.

**Title pages** (the 10 Sep fold)
- Every title page ends with the always-open "At a glance" band (where
  to watch with the checked date, length, cost, cast) and carries
  TVSeries schema; no fold-outs, no FAQ markup (Cyan's 10 Sep design).
  There is no where-to-watch/ folder; those URLs 301 to the title page.

**Sitemap and noindex** (the 1 Sep Google demotion recovery)
- Sitemap URLs: on-domain, every one has a file, none carries a noindex
  meta. Thin pages are noindexed AND out of the sitemap, together.

**Redirects**
- Every specific old-URL 301 (a merged actor or title) sits BEFORE the
  generic /:slug rules. Placed after, it never fires: :slug swallows
  "name.html" as one segment and the old URL 301s to name.html.html
  without end (found live 10 Sep). merge_person.py and merge_title.py
  insert in the right place.
- _redirects never contains a forced 301!/302! (verified 5 Sep: with
  Netlify Pretty URLs on, a forced rule loops forever).
- /data, /generator, /references, /design-system and every root .md file
  are blocked with a forced 404! (10 Sep: the repo root is the publish
  folder, so anything not blocked deploys to the brand domain).

**IndexNow** (10 Sep)
- Exactly one key file (32 hex characters .txt, containing its own name)
  sits at the site root, and the Sunday workflow runs indexnow.py after
  its push so Bing learns what changed. A failure there never blocks a
  publish.

**Analytics** (10 Sep)
- Every page carries the GoatCounter script; the site code lives in
  build.py as GOATCOUNTER and nowhere else.
- The extensionless 301 rule exists in the file for all four page
  families (titles, actors, tropes, apps; where-to-watch was folded
  into titles on 10 Sep and its URLs 301 there). It is
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

**Rail arrows** (17 Sep)

Cyan asked for arrows that pop up on hover instead of a slider under
each rail, and said not to interfere with functionality. Three things
have to stay true, and check_site fails the build if any of them stops
being true.

- The arrows are built in JavaScript and never appear in the HTML we
  ship. That is the whole reason a reader with JavaScript off is no
  worse off than before: they get the plain scroll rail they always
  had, not two buttons that do nothing. If arrow markup ever shows up
  in a page's source, that promise is broken.
- Everything about them sits behind `(hover:hover) and (pointer:fine)`.
  A phone cannot hover, so a phone gets no arrows and keeps its native
  swipe and its own scrollbar. Lose that guard and touch readers lose
  the scrollbar AND get arrows they can never reveal. Note the words
  also appear in the comment above the CSS, so the check looks for the
  actual @media rule, not the phrase.
- The arrows show on `:focus-within` as well as hover, so tabbing into
  a rail with a keyboard brings them up. Without it a keyboard reader
  scrolls the rail with no visible control.

Two smaller things worth knowing if this ever looks wrong:

- The arrow centres on the POSTER, not the card. A card is artwork plus
  one or two lines of caption, so centring on the card sinks the arrow
  into the text. The script measures the first poster and sets a CSS
  variable, which is why it lands right on all three rail sizes.
- A rail at rest sits at scrollLeft 22, not 0. scroll-snap-align snaps
  to the first card, which starts after the rail's 22px padding. The
  back arrow reads the padding to know it is at the start; a plain
  "is it zero" test left the back arrow live on every rail on the site.

**Phone pass** (18 Sep)

Most visitors are on a phone, and Cyan's condition was plain: build it
properly "as long as it won't wreck the desktop website". So the phone
work is scoped the opposite way round to how her design handoff was
written.

The handoff was phone-first, with desktop restored inside a
`min-width:760px` block. Measured in a real browser, that moved about
forty things on desktop, because a restore block only puts back what
someone remembered to list. It stretched the title-page watch card from
440px to 902px, froze the fluid hero headline, and resized rail posters.

So every phone rule here lives inside `@media (max-width:759.98px)`.
Desktop never sees any of it. That is a structural guarantee, not a
promise to be careful, and it is checked: desktop computed styles were
compared before and after across four pages at 1280, 1024, 800 and 760
and came back with **zero** differences.

The three things that had to be built, because the handoff's CSS
referred to markup the site did not have:

- **Menu sheet.** The header hides the nav below 760px, so without the
  sheet a phone reader has no navigation at all, just the logo. This is
  the one to watch: the sheet markup ships in the HTML with `hidden`,
  not built in script like the rail arrows, precisely because it is
  navigation and has to survive a script that never runs. The hamburger
  is the only part that needs JavaScript.
- **Sticky watch bar** on title pages. The watch button is the point of
  the page and it used to scroll away for good. An IntersectionObserver
  on the real button brings it back, so it never doubles up, and a title
  with no clickable button gets no bar rather than a bar that lies.
- **Browse filter sheet.** The sidebar renders before the results, so a
  phone reader scrolled past roughly 2,000px of filter chips to reach
  the first title. The heading, search and active-filter summary stay in
  the flow; the chips move behind one button. First result now lands at
  508px instead of about 2,600px.

Two details that look odd but are deliberate:

- The title-page hero uses a FLOAT on phones, not flex. The watch card
  is inside `.info-col`, so `.split-hero .watch-card{flex:1 1 100%}` does
  nothing at all: the card is a grandchild, not a flex item. Left as
  flex it is stuck in a 230px column and "Watch on ReelShort" wraps.
- The "No poster" label is indented 32px on phone cards. The favourite
  star is a fixed 32px circle and at 120px card width it lands on top of
  the label. The badge is already the minimum comfortable tap target, so
  the label gives way, not the badge.

**Three phone fixes** (18 Sep, from Cyan using it)

- **Selected filter chips went white.** `.chip:hover:not(.off)` is (0,3,0)
  and outranks `.chip.on` at (0,2,0), so hovering a selected chip painted
  it `#fff` while `.on` kept the text at `#FFF8F2`. White on white, a
  contrast ratio of 1.02:1. This was a long-standing bug on desktop too,
  but there the mouse moves away and it clears; a touch device KEEPS
  `:hover` after a tap, so on a phone the chip stayed unreadable until
  you tapped something else. Fixed by excluding `.on` from the hover
  rule and putting the whole rule behind `@media (hover:hover)`. Note
  this does change one desktop behaviour on purpose: hovering an already
  selected chip now darkens to wine instead of going blank.
- **Tapping a menu link flashed the old page.** The sheet closed on tap,
  which uncovered the page you were already on, and you looked at it for
  the length of the request before the new page painted. Cyan called it
  a quick cut, and it was: two transitions where there should be one.
  The sheet now stays up during navigation and the next page replaces
  it. A same-page link still closes it, because nothing will repaint and
  the sheet would sit over the destination.
- **Contact was 14px next to 20px links.** It was in a `.sheet-foot`
  styled as small print. It is a nav item, so it moved into the nav list.

**Sheets are sized in dvh, not vh** (18 Sep)

Cyan's screenshot showed the filter sheet with the word "Filters" cut
off across the ascenders, no rounded top edge and no grip handle: the
sheet was taller than the screen and had pushed its own head off the
top.

On iOS Safari `100vh` means the viewport WITHOUT the address bar. A
bottom-anchored sheet capped at `86vh` is therefore taller than what the
reader can actually see, and everything above the fold is simply gone,
including the close button. `dvh` is the live viewport and tracks the
browser chrome as it hides and shows.

Both sheets now declare `vh` first and `dvh` second, so an older browser
takes the fallback and everything current takes `dvh`. The order matters
and check_site enforces it.

Worth knowing when testing: headless Chromium has no dynamic address bar,
so `vh` and `dvh` resolve identically there. A desktop browser cannot
reproduce this bug. It has to be checked on a real phone.

**The language filter on browse** (18 Sep)

Cyan: "you have called where the English and Chinese is the country of
origin, and I don't think that's correct... you also have Chinese
blurred out, and I know for a fact we do have some Chinese verticals."

Both halves were right, and the second one uncovered something bigger.

The label was simply wrong. English and Chinese are languages, not
countries, and Dubbed is neither: it is which version of a release you
are watching. It now reads **Language**, with the hint "Original
language, or an English dub" so Dubbed does not look misfiled.

The greyed Chinese chip was not a display fault. Every one of the 3,789
titles carries `origin=english`. There are no Chinese titles in the
database at all, and no `/chinese/` section page has ever been built.

But the filter could not have worked even if there were. build.py scopes
browse, home, tropes and platforms to ROOT_ORIGIN, and any other origin
gets its OWN section index instead (the comment above `titles_root` says
so). Adding Chinese titles moves them out of browse; it does not light up
a Chinese chip. The filter was structurally dead from the day it was
written, not merely waiting on data.

So the group is hidden while browse lists one language, and it returns on
its own if that ever stops being true. check_site counts the browse
population rather than the whole file, which is the only way this check
tells the truth: counting every row would say "two languages, show the
filter" while browse still showed none of them.

One consequence worth remembering: **if Chinese titles are ever added,
they will not appear in Browse.** They get a section index at
`/chinese/index.html`. Whether that is what we want is a design decision
nobody has made yet, and it should be made before the titles arrive
rather than after.

Also: the sheet now carries its own **Clear all**, because the page's own
Reset sits behind the sheet on a phone and cannot be tapped while you are
choosing filters. Both controls run one handler and share one show/hide
rule, so they cannot disagree.
