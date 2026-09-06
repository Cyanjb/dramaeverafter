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
        ("pinned.csv", "title_id", tid_set, "titles")]:
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
mw, nt = home.find("Most watched"), home.find("New and trending")
if mw == -1 or nt == -1: fail("homepage is missing the Most watched or New and trending rail")
elif not (mw < nt): fail("New and trending is not directly under Most watched (Cyan, 6 Sep)")
else: ok("rail order: Most watched, then New and trending")
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

print("== redirects ==")
red = rd("_redirects")
if re.search(r"\b30[12]!", red):
    fail("_redirects contains a FORCED redirect (301!/302!): with Pretty URLs on, that loops. Never use it (verified 5 Sep).")
else:
    ok("_redirects has no forced redirects (the 5 Sep loop trap)")

print()
print(f"{passes} ok, {len(warns)} warnings, {len(fails)} failures")
for w in warns: print(f"  WARN  {w}")
for f_ in fails: print(f"  FAIL  {f_}")
sys.exit(1 if fails else 0)
