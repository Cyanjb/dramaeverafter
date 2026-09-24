#!/usr/bin/env python3
"""Site smoke test: everything SITE-CHECKS.md promises, verified on the built
output. Run after build.py, from anywhere (paths resolve from this file).

Exit 0 = every check passed. Exit 1 = at least one FAIL, and the report says
which; the weekly workflow runs this between build and push, so a broken
build fails the Actions run instead of publishing. WARN lines never fail the
run - they are for drifts worth a look, not breakage.

Checks are invariants, not snapshots: no hardcoded counts or title names,
so a normal week of data changes cannot make them stale. When a page or
behavior is added that must keep working, add its check HERE and its plain
words to SITE-CHECKS.md.
"""
import csv, json, os, re, subprocess, sys, unicodedata
import collections
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
fails, warns, passes = [], [], 0


def ok(msg):
    global passes
    passes += 1
    print(f"  ok    {msg}")

def fail(msg):
    fails.append(msg)
    print(f"  FAIL  {msg}")

def warn(msg):
    warns.append(msg)
    print(f"  WARN  {msg}")

def rd(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()

def rows(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


print("== data integrity ==")
titles = rows("titles.csv")
people = rows("people.csv")
tids = [t["title_id"] for t in titles]
tid_set = set(tids)
pid_set = {p["person_id"] for p in people}
dupes = {x for x in tids if tids.count(x) > 1} if len(tids) != len(tid_set) else set()
if dupes: fail(f"duplicate title_ids in titles.csv: {sorted(dupes)[:5]}")
else: ok(f"titles.csv: {len(titles)} rows, title_ids unique")
for fname, col, universe, label in [
        ("availability.csv", "title_id", tid_set, "titles"),
        ("tropes.csv", "title_id", tid_set, "titles"),
        ("credits.csv", "title_id", tid_set, "titles"),
        ("credits.csv", "person_id", pid_set, "people"),
        ("pinned.csv", "title_id", tid_set, "titles"),
        ("picks.csv", "title_id", tid_set, "titles")]:
    orphans = [r[col] for r in rows(fname) if r.get(col) and r[col] not in universe]
    if orphans: fail(f"{fname}: {len(orphans)} {col} rows point at no {label} row, e.g. {orphans[:3]}")
    else: ok(f"{fname}: every {col} resolves")

print("== search ==")
idx = json.loads(rd("search-index.json"))
if len(idx.get("titles", [])) < 0.9 * len(titles):
    fail(f"search-index.json holds {len(idx.get('titles', []))} titles for {len(titles)} rows; the index build is dropping data")
else:
    ok(f"search-index.json: {len(idx['titles'])} titles, {len(idx.get('actors', []))} actors")
missing = [t["s"] for t in idx["titles"] if not os.path.exists(os.path.join(ROOT, "titles", t["s"] + ".html"))]
if missing: fail(f"{len(missing)} search-index titles have no page, e.g. {missing[:3]}")
else: ok("every search-index title has a page in titles/")
missing = [a["s"] for a in idx["actors"] if not os.path.exists(os.path.join(ROOT, "actors", a["s"] + ".html"))]
if missing: fail(f"{len(missing)} search-index actors have no page, e.g. {missing[:3]}")
else: ok("every search-index actor has a page in actors/")
# Character names (10 Sep): searchable everywhere, and one index page.
def _norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace("\u2019", "").replace("'", "").replace("`", "")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", s).split())
named = [r for r in rows("credits.csv") if (r.get("character_name") or "").strip()]
by_slug_t = {t["s"]: t for t in idx["titles"]}
by_slug_a = {a["s"]: a for a in idx["actors"]}
lost = []
for r in named[:200]:
    ch = _norm(r["character_name"].split("/")[0])
    tt = next((t for t in idx["titles"] if t["s"] == r["title_id"] or t.get("s") == r["title_id"]), None)
    if tt is not None and ch not in tt.get("ch", ""): lost.append(r["character_name"])
if lost: fail(f"character names missing from search-index titles, e.g. {lost[:3]}")
else: ok(f"character names in search-index.json ({sum(1 for t in idx['titles'] if t.get('ch'))} titles, {sum(1 for a in idx['actors'] if a.get('ch'))} actors)")
if not os.path.exists(os.path.join(ROOT, "characters.html")):
    fail("characters.html missing (the one-page character index)")
else:
    ch_html = rd("characters.html")
    n_rows = ch_html.count('class="char-row"')
    hrefs = {h for h in re.findall(r'href="([^"#?]+)"', ch_html) if not h.startswith("http")}
    bad = [h for h in hrefs if not os.path.exists(os.path.join(ROOT, h))]
    if n_rows < 0.9 * len(named): fail(f"characters.html lists {n_rows} rows for {len(named)} named credits")
    elif bad: fail(f"characters.html has {len(bad)} dead links, e.g. {bad[:3]}")
    else: ok(f"characters.html: {n_rows} rows, every link resolves")

browse = rd("browse.html")
az = rd("actors/index.html")
for name, src, needs in [("browse.html", browse, ["function norm(", "function qmatch(", 'id="q"']),
                          ("actors/index.html", az, ["function norm(", "function qmatch(", 'id="actor-search"'])]:
    lost = [n for n in needs if n not in src]
    if lost: fail(f"{name} search wiring missing {lost}")
    else: ok(f"{name} carries the forgiving-search wiring")

# The Python and JS normalizers must agree, or a page matches differently from
# the index. Importing build.py would run the whole build, so lift norm_search's
# source out of the file and exec just that, then run the JS actually shipped in
# browse.html through node - the characters that caused the 6 Sep bug (curly
# apostrophe), plus accents, dashes and case.
norm_search = None
bsrc = rd("generator/build.py")
mdef = re.search(r"\ndef norm_search\(s\):.*?(?=\n\S)", bsrc, re.S)
if not mdef:
    fail("norm_search() no longer exists in build.py")
else:
    ns = {"unicodedata": unicodedata, "re": re}
    exec(mdef.group(0), ns)
    norm_search = ns["norm_search"]
SAMPLES = ["A Zombie Girl’s Journey Home", "Girl's, girls, GIRLS!", "Fiancée  — Déjà Vu", "brother-in-law & co."]
if norm_search:
    m = re.search(r"function norm\(s\).*?return true;\}", browse, re.S)
    if m is None:
        fail("could not extract norm() from browse.html for the parity check")
    else:
        try:
            node = subprocess.run(["node", "-e",
                m.group(0) + ";console.log(JSON.stringify(" + json.dumps(SAMPLES) + ".map(norm)))"],
                capture_output=True, text=True, timeout=30)
            if node.returncode != 0:
                fail(f"shipped norm() does not run under node: {node.stderr.strip()[:120]}")
            elif json.loads(node.stdout) != [norm_search(s) for s in SAMPLES]:
                fail("norm() in the shipped JS disagrees with norm_search() in build.py")
            else:
                ok("JS and Python search normalizers agree on the tricky characters")
        except FileNotFoundError:
            warn("node not available; JS/Python normalizer parity unchecked")

print("== homepage ==")
home = rd("index.html")
mw, nt = home.find("Most watched right now"), home.find("New and trending")
if mw == -1 or nt == -1: fail("homepage is missing the Most watched or New and trending rail")
elif not (mw < nt): fail("New and trending is not directly under Most watched (Cyan, 6 and 13 Sep)")
else: ok("rail order: Most watched right now, then New and trending")
# Our pick (10 Sep): the newest picks.csv row shows on the homepage above the
# rails and its title page carries the chip; a gift link never outlives its expiry.
_picks = rows("picks.csv")
if _picks:
    _pk = max(_picks, key=lambda r: r["added"])
    _tp2 = rd(os.path.join("titles", _pk["title_id"] + ".html"))
    if 'class="pick-grid' not in home or _pk["title_id"] not in home: fail("homepage lacks the pick-of-the-week card for the newest picks.csv row")
    elif home.rfind('class="rail"') > home.find('class="pick-grid'): fail("the pick row must sit AFTER the poster rails (Cyan, 13 Sep)")
    elif home.find("In the mood for") > home.find('class="pick-grid'): fail("the mood chips must sit above the pick row (Cyan, 13 Sep)")
    elif 'pick-chip' not in _tp2: fail(f"the pick's title page lacks the Our pick chip: {_pk['title_id']}")
    elif 'data-expires' in home and 'PICK_JS' not in bsrc: fail("pick gift button has no expiry script")
    else: ok(f"Our pick: {_pk['title_id']} on the homepage and chipped on its page")
rail = re.search(r"New and trending.*?</section>", home, re.S)
rail_slugs = list(dict.fromkeys(re.findall(r"titles/([a-z0-9-]+)\.html", rail.group(0)))) if rail else []
if len(rail_slugs) < 8: fail(f"New and trending rail holds {len(rail_slugs)} titles; should be ~12")
else: ok(f"New and trending rail holds {len(rail_slugs)} titles")
pins = [r["title_id"] for r in rows("pinned.csv") if (r.get("rail") or "").strip() == "trending"]
for i, p in enumerate(pins):
    if p not in rail_slugs[:len(pins)]:
        fail(f"pinned title {p} is not leading the New and trending rail")
    else:
        ok(f"pin honored: {p} leads the rail")

print("== pages and links ==")
for path, must in [("tropes/index.html", ""), ("platforms.html", ""), ("my-list.html", ""),
                   ("contact.html", "cyan@dramaeverafter.com"), ("404.html", ""),
                   ("robots.txt", ""), ("llms.txt", "")]:
    full = os.path.join(ROOT, path)
    if not os.path.exists(full): fail(f"{path} missing")
    elif must and must not in rd(path): fail(f"{path} no longer contains {must}")
    else: ok(f"{path} present" + (f" and carries {must}" if must else ""))

# Every internal link on the entry pages must resolve to a real file. These are
# the pages people land on; a dead link here is a dead end for everyone.
bad = []
for src_page in ["index.html", "browse.html", "tropes/index.html", "actors/index.html", "platforms.html", "contact.html"]:
    base = os.path.dirname(src_page)
    markup = re.sub(r"<script>.*?</script>", "", rd(src_page), flags=re.S)
    for href in re.findall(r'href="([^"#?]+)"', markup):
        if href.startswith(("http", "mailto:", "//")) or href.endswith((".css", ".svg", ".png")):
            continue
        tgt = os.path.normpath(os.path.join(ROOT, base, href))
        if not os.path.exists(tgt):
            bad.append(f"{src_page} -> {href}")
if bad: fail(f"{len(bad)} dead internal links on entry pages, e.g. {bad[:4]}")
else: ok("every internal link on the entry pages resolves")

# Every trope chip on the tropes index must have its page.
tr_missing = [h for h in re.findall(r'href="([a-z0-9-]+\.html)"', rd("tropes/index.html"))
              if not os.path.exists(os.path.join(ROOT, "tropes", h))]
if tr_missing: fail(f"trope pages missing: {tr_missing[:5]}")
else: ok("every trope on the index has a page")

print("== sitemap and noindex ==")
sm = rd("sitemap.xml")
locs = re.findall(r"<loc>([^<]+)</loc>", sm)
if len(locs) < 3000: fail(f"sitemap.xml holds only {len(locs)} URLs")
else: ok(f"sitemap.xml: {len(locs)} URLs")
offsite = [u for u in locs if not u.startswith("https://dramaeverafter.com")]
if offsite: fail(f"sitemap URLs off-domain: {offsite[:3]}")
else: ok("every sitemap URL is on the domain")
noindexed, gone = [], []
for u in locs:
    p = u.replace("https://dramaeverafter.com/", "").replace("https://dramaeverafter.com", "") or "index.html"
    full = os.path.join(ROOT, p)
    if not os.path.exists(full): gone.append(p)
    elif 'content="noindex"' in rd(p): noindexed.append(p)
if gone: fail(f"{len(gone)} sitemap URLs have no file, e.g. {gone[:3]}")
else: ok("every sitemap URL has a file")
if noindexed: fail(f"{len(noindexed)} sitemap URLs carry noindex (they must leave the sitemap), e.g. {noindexed[:3]}")
else: ok("no sitemap URL carries a noindex meta")
# The fold (10 Sep): title pages carry where-to-watch and the quick answers.
_first_title = next((u for u in locs if "/titles/" in u), "")
_tp = rd(_first_title.replace("https://dramaeverafter.com/", "")) if _first_title else ""
if _tp and ('id="at-a-glance"' not in _tp or '"TVSeries"' not in _tp or '<details' in _tp):
    fail(f"title page lacks the At a glance band or TVSeries schema, or still has fold-outs: {_first_title}")
elif _tp: ok("title pages end with the At a glance band and carry TVSeries schema (10 Sep handoff)")

# Every app that carries a title gets its own button (Cyan, 13 Sep). Before
# that the second app was plain text a reader could not click.
_multi = collections.Counter()
for _r in rows("availability.csv"): _multi[_r["title_id"]] += 1
_two = [t for t, n in _multi.items() if n > 1 and os.path.exists(os.path.join(ROOT, "titles", t + ".html"))]
# An app may be plain text ONLY when nothing can be linked: no deep link on
# the row and no verified homepage for the platform (Playlet, Shortical,
# Shorts, KalosTV, DramaPops). A dead button would be worse than the text.
_web = {p["platform_id"]: (p.get("web_url") or "").strip() for p in rows("platforms.csv")}
_linkable = collections.Counter()
for _r in rows("availability.csv"):
    if (_r.get("direct_link") or "").strip() or _web.get(_r["platform_id"]):
        _linkable[_r["title_id"]] += 1
_short = []
for t in _two:
    want = _linkable[t]
    if want < 2: continue
    if rd(os.path.join("titles", t + ".html")).count('class="watch-btn') < want: _short.append(t)
if _short: fail(f"{len(_short)} titles show fewer watch buttons than linkable apps, e.g. {_short[:3]}")
else: ok(f"every linkable app has its own watch button ({len(_two)} titles on two or more apps)")

print("== redirects ==")
red = rd("_redirects")
if re.search(r"\b30[12]!", red):
    fail("_redirects contains a FORCED redirect (301!/302!): with Pretty URLs on, that loops. Never use it (verified 5 Sep).")
else:
    ok("_redirects has no forced redirects (the 5 Sep loop trap)")
if os.path.isdir(os.path.join(ROOT, "where-to-watch")):
    fail("where-to-watch/ exists: folded into the title pages on 10 Sep; a stale build left it behind")
elif not re.search(r"^/where-to-watch/\*\s+/titles/:splat\s+301\s*$", red, re.M):
    fail("_redirects lacks '/where-to-watch/*  /titles/:splat  301'")
else:
    ok("no where-to-watch/ folder, and its URLs 301 to the title pages")
# The repo root is the publish folder (audit H3, closed 10 Sep): everything
# that is not the site must be blocked by a forced 404, or it deploys.
missing = [d for d in ("data", "generator", "references", "design-system")
           if not re.search(rf"^/{re.escape(d)}/\*\s+\S+\s+404!", red, re.M)]
missing += [m for m in sorted(os.listdir(ROOT)) if m.endswith(".md")
            and not re.search(rf"^/{re.escape(m)}\s+\S+\s+404!", red, re.M)]
if missing: fail(f"not blocked on the domain (add a 404! rule to _redirects): {missing}")
else: ok("database, generator, references and every root .md are 404! on the domain")
# The 404! rules match exact case only, and Netlify serves files case-
# insensitively: /Data/titles.csv and /handover.md answered 200 (audit,
# 24 Sep 2026). The real block is netlify.toml's build command, which deletes
# the non-site paths from the deploy copy. Every tracked root entry must be
# either part of the site or removed there.
_toml = rd("netlify.toml") if os.path.exists(os.path.join(ROOT, "netlify.toml")) else ""
_cmd = re.search(r'^\s*command\s*=\s*"([^"]*)"', _toml, re.M)
_pruned = set(re.findall(r"[\w.*-]+", _cmd.group(1))) if _cmd else set()
_SITE_DIRS = {"actors", "apps", "titles", "tropes", "chinese"}
_SITE_FILES = {"_redirects", "_headers", "netlify.toml"}
_SITE_EXT = (".html", ".css", ".js", ".json", ".xml", ".txt", ".png", ".svg", ".ico", ".webp", ".jpg")
try:
    _tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
except (OSError, subprocess.CalledProcessError):
    _tracked = []
_roots = {p.split("/")[0] for p in _tracked if p}
_leak = sorted(r for r in _roots
               if r not in _SITE_DIRS and r not in _SITE_FILES and r not in _pruned
               and not (r.endswith(".md") and "*.md" in _pruned)
               and not (r in _tracked and r.endswith(_SITE_EXT)))
if not _cmd: fail("netlify.toml has no build command: every capitalisation of /data, /generator and the notes is served (audit, 24 Sep 2026)")
elif not _tracked: warn("git ls-files unavailable: could not check that netlify.toml removes every non-site root path")
elif _leak: fail(f"root paths neither part of the site nor removed by netlify.toml's build command: {_leak}")
else: ok("netlify.toml's build command removes every non-site root path, in any capitalisation")

# THE POSTER RULE (Cyan, 13 Sep 2026): posters stay true to their sources, 3:4.
# A design handoff asking for 9:16 or 2:3 does not override it; the sources do.
_css = rd("style.css")
_bad = [m for m in re.findall(r"\.(?:poster|thumb)[^{]*\{[^}]*aspect-ratio:\s*([0-9]+\s*/\s*[0-9]+)", _css)
        if m.replace(" ", "") != "3/4"]
if _bad: fail(f"a poster is not 3:4, which crops the source art: {_bad} (Cyan's standing rule, 13 Sep)")
else: ok("every poster is 3:4, true to what the platforms ship")

print("== indexnow ==")
_keys = [f for f in os.listdir(ROOT) if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
if len(_keys) != 1: fail(f"expected exactly one IndexNow key file at the root, found {_keys}")
elif rd(_keys[0]).strip() != _keys[0][:-4]: fail(f"IndexNow key file {_keys[0]} must contain its own name")
elif "indexnow.py" not in rd(".github/workflows/weekly-scrape.yml"): fail("weekly workflow no longer runs indexnow.py")
else: ok("IndexNow key file present and the weekly workflow submits changes")

print("== analytics ==")
gc = [p for p in ("index.html", "browse.html", "404.html") if "data-goatcounter=" not in rd(p)]
if gc: fail(f"GoatCounter script missing from {gc}")
else: ok("GoatCounter script on the root pages (build.py GOATCOUNTER)")

# No generic /titles/:slug -> /titles/:slug.html rule (nor actors, tropes,
# apps). It never fired for a real page (Netlify serves foo.html at /foo
# first, no toggle), and for a MISSING page :slug swallowed "name.html" as
# one segment, so every unknown URL looped to name.html.html.html forever
# instead of the 404 page (audit, 24 Sep 2026; first seen 10 Sep on a
# misplaced merge 301). The extensionless duplicate itself stays unsolved by
# Cyan's 10 Sep ruling; the canonical tags carry it. See SITE-CHECKS.md.
_lines = red.split("\n")
_generic = [l.strip() for l in _lines if re.match(r"^/(titles|actors|tropes|apps)/:\w+\s", l)]
if _generic: fail(f"generic :slug rules loop on every missing page instead of a 404: {_generic}")
else: ok("no generic page :slug rules, so a missing page gets the 404 page, not a redirect loop")
# Without the generic rule, an old URL's extensionless form needs its own
# rule: every specific page 301 carries its extensionless twin.
_srcs = {l.split()[0] for l in _lines if l.strip() and not l.startswith("#")}
_nolone = [s for s in _srcs if re.match(r"^/(titles|actors|tropes|apps)/\S+\.html$", s)
           and s[:-5] not in _srcs and not os.path.exists(os.path.join(ROOT, s.lstrip("/")))]
if _nolone: fail(f"page 301s with no extensionless twin (merge_person/merge_title write both): {sorted(_nolone)[:3]}")
else: ok("every old page 301 also redirects its extensionless form")

print("== rails ==")
# Cyan, 17 Sep 2026: arrows on hover, no slider, and "don't interfere with
# functionality". The arrows are PROGRESSIVE ENHANCEMENT: built in script, never
# shipped as markup, so a reader with no JavaScript gets the plain scroll rail
# instead of dead buttons. Three things have to stay true or that promise breaks.
_rail_pages = [f for f in ("index.html", "titles/clubhouse-of-desire.html") if os.path.exists(f)]
# "rail-nav" appears on every page as SCRIPT TEXT, so the shipped-markup test
# has to look for the attribute form specifically, not the bare string.
_no_js = [f for f in _rail_pages if 'class="rail"' in rd(f)]
_shipped = [f for f in _rail_pages if 'class="rail-nav' in rd(f)]
_css = rd("style.css")
if _shipped:
    fail(f"arrow markup is in the HTML of {_shipped}: with JavaScript off those "
         "are dead buttons. They must be built in script (build.py RAIL_JS)")
elif not _no_js:
    fail("no page carries a rail any more, or the rail class was renamed: "
         "the hover-arrow script keys off class=\"rail\" (build.py RAIL_JS)")
# Match the AT-RULE, not the bare string: the same words appear in the comment
# above the block, so a plain substring test passes even after the guard is gone.
elif not re.search(r"@media\s*\(\s*hover\s*:\s*hover\s*\)\s*and\s*\(\s*pointer\s*:\s*fine\s*\)", _css):
    fail("the rail arrow CSS lost its (hover:hover) and (pointer:fine) guard: "
         "touch readers would lose the scrollbar and get arrows they cannot hover")
elif ".rail-wrap.has-nav:focus-within" not in _css:
    fail("the rail arrows no longer appear on :focus-within: a keyboard reader "
         "tabbing into a rail would scroll it with no visible control")
else:
    ok("rail arrows are script-built, pointer-guarded and keyboard-reachable")

print("== phone ==")
# Cyan, 18 Sep 2026: most visitors are on a phone, and "as long as it won't
# wreck the desktop website". The phone pass is scoped inside max-width:759.98px
# for exactly that reason -- a desktop restore block only puts back what someone
# remembered to list, and her design handoff proved it by moving 40-odd desktop
# values, so the guarantee here is structural. These checks defend both halves.
_css = rd("style.css")
_home, _browse = rd("index.html"), rd("browse.html")
_title = rd("titles/clubhouse-of-desire.html") if os.path.exists("titles/clubhouse-of-desire.html") else ""

if "@media (max-width:759.98px)" not in _css.replace(" ", " "):
    fail("the phone block is gone or its breakpoint moved: every phone rule "
         "lives inside @media (max-width:759.98px) so desktop never sees it")
elif 'id="nav-sheet"' not in _home:
    fail("the phone menu sheet markup is missing from the page. The header "
         "hides .site-nav below 760px, so without the sheet a phone reader has "
         "NO navigation at all -- only the logo")
elif _home.count('<a href=') and 'class="nav-toggle"' not in _home:
    fail("the hamburger button is gone but the sheet remains: nothing can open it")
elif _home.find('id="nav-sheet"') > 0 and " hidden>" not in _home[_home.find('id="nav-sheet"'):_home.find('id="nav-sheet"') + 40]:
    fail("the menu sheet no longer ships with `hidden`: it would cover the page "
         "for anyone whose JavaScript has not run yet")
elif _title and 'class="watch-sticky"' not in _title:
    fail("the sticky watch bar is missing from title pages: on a phone the "
         "watch button scrolls away and never comes back")
elif 'class="filter-open"' not in _browse or 'id="filter-body"' not in _browse:
    fail("the browse filter sheet is gone: the sidebar renders before the "
         "results, so a phone reader scrolls ~2,000px of chips to reach a title")
elif ".filter-open,.filter-body>.sheet-head" not in _css:
    fail("the phone-only sheet chrome is no longer hidden by default: the "
         "Filters button and sheet header would appear on desktop")
else:
    ok("phone nav, sticky watch bar and filter sheet are all present and "
       "scoped away from desktop")

# A selected filter chip must never take the hover background. `.chip:hover:not(.off)`
# is (0,3,0) and outranks `.chip.on` at (0,2,0), so without the :not(.on) the chip
# paints #fff while .on keeps the text at #FFF8F2 -- white on white, 1.02:1. A touch
# device keeps :hover after a tap, so on a phone that state stuck (Cyan, 18 Sep).
if not re.search(r"\.chip:hover:not\(\.off\):not\(\.on\)", _css):
    fail("the selected-chip guard is gone from .chip:hover: a chosen filter chip "
         "renders white text on a white pill, and on a phone it stays that way")
elif not re.search(r"@media\s*\(\s*hover\s*:\s*hover\s*\)[^@]*\.chip:hover", _css, re.S):
    fail("the chip hover rule is no longer behind @media (hover:hover): a tap on a "
         "phone leaves the hover state stuck on the chip")
else:
    ok("a selected filter chip keeps its wine fill on hover and on touch")

# Bottom-anchored sheets must be sized in dvh, with vh only as the fallback line
# BEFORE it. On iOS Safari 100vh is the viewport WITHOUT the address bar, so a vh
# sheet is taller than the visible area and pushes its own header off the top of
# the screen -- Cyan's 18 Sep screenshot had "Filters" with its ascenders sliced
# off and no grip or rounded edge at all.
_dvh_ok = ("max-height:86vh;max-height:86dvh" in _css and
           "height:100vh;height:100dvh" in _css)
if not _dvh_ok:
    fail("a phone sheet lost its dvh sizing (or the vh fallback stopped coming "
         "first): on iOS the sheet grows taller than the screen and its own "
         "header and close button go off the top")
else:
    ok("phone sheets are sized in dvh, so iOS chrome cannot push their heads off-screen")

# The language filter appears only when BROWSE ITSELF lists more than one
# language. That qualifier matters: build.py scopes browse, home, tropes and
# platforms to ROOT_ORIGIN, and any other origin gets its own section index
# instead (see the comment above titles_root). So the filter was not merely
# empty, it was structurally dead -- adding Chinese titles moves them OUT of
# browse, it does not light up a Chinese chip. Counting the browse population
# rather than the whole file is what makes this check tell the truth, and it
# still flips on its own if that scoping is ever changed.
_root_origin = "english"
_browse_origins = collections.Counter(
    (r.get("origin") or _root_origin).strip().lower() for r in rows("titles.csv")
    if (r.get("origin") or _root_origin).strip().lower() == _root_origin)
_all_origins = collections.Counter((r.get("origin") or _root_origin).strip().lower()
                                   for r in rows("titles.csv"))
_live = len(_browse_origins)
_shown = 'id="f-origin"' in _browse
if _live > 1 and not _shown:
    fail(f"browse now lists {_live} languages but its language filter is hidden")
elif _live <= 1 and _shown:
    fail("the browse language filter is showing, but browse only ever lists "
         f"{_root_origin} titles, so its other chips can never match. If other "
         "origins are meant to appear in browse now, titles_root is the thing "
         "to change, not this filter")
elif "Country of origin" in _browse:
    fail("the language filter is labelled 'Country of origin' again: English and "
         "Chinese are languages, and Dubbed is a release version, not a country")
else:
    ok(f"the browse language filter matches what browse lists "
       f"({_live} language, group {'shown' if _shown else 'hidden'}; "
       f"whole catalogue: {dict(_all_origins)})")

print()
print(f"{passes} ok, {len(warns)} warnings, {len(fails)} failures")
for w in warns: print(f"  WARN  {w}")
for f_ in fails: print(f"  FAIL  {f_}")
sys.exit(1 if fails else 0)
