"""Fill the missing DramaBox direct_link values from DramaBox's OWN genre catalogue.

WHY NOT THE SEARCH ENDPOINT. https://www.dramaboxdb.com/search?keyword=... is
ROBOTS-DISALLOWED ("Disallow: /search?*"), so it is off-limits regardless of whether
it works. It also does not work: the page returns 200 and the response contains the
title string, but that is the QUERY ECHOED BACK inside the page's own JSON
("query":{"keyword":"..."}), not a result. A naive `title.lower() in html.lower()`
check reports True for every title on earth. Do not reinstate it.

WHY THE GENRE PAGES. robots.txt is "Allow: /" with a short disallow list that does
NOT include /genres, and each /genres/<id> page embeds a __NEXT_DATA__ payload whose
book objects carry bookId, bookName and chapterCount. bookId is exactly the id in the
canonical /movie/<bookId>/<slug> URL, so walking the 54 genres builds a
title -> id index offline and costs one request per genre instead of one per title.

SAME-NAME PRODUCTIONS ARE REAL HERE. A search for "Love in the Shadows" also returns
"Beyond Duty's Call: Love in the Shadows", a different bookId. 83 of our own titles
share a name with another row. So this script matches on the FULL normalised title
only, never on containment, and any title that matches two different bookIds is
reported as ambiguous and left alone rather than guessed.

THE HOST SOFT-BLOCKS. Requests in quick succession get ConnectionReset rather than an
HTTP error. Treat it as retryable, pace serially, and cache every page to disk so a
re-run costs nothing.

Writes generator/staging/dramabox_links_<date>.json. Applies NOTHING - the staged
file is reviewed, then applied by apply_dramabox_links.py.

Usage:
    py generator/harvest_dramabox_links.py [--limit N]
"""
import csv, json, os, re, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(HERE, "..", "data")
CACHE = os.path.join(HERE, "staging", "_dramabox_cache")
OUT = os.path.join(HERE, "staging", "dramabox_links_" + time.strftime("%Y-%m-%d") + ".json")
BASE = "https://www.dramaboxdb.com"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"}
PACE = 2.5


def norm(s):
    """Full-string normalisation. Deliberately NOT a containment test."""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def fetch(url, tries=4):
    """Returns html or raises. ConnectionReset is the soft block; back off and retry."""
    delay = 3
    for attempt in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40)
            body = r.read().decode("utf-8", "replace")
            if len(body) < 500:          # empty-body soft block, same family as sec 20
                raise OSError("suspiciously short body")
            return body
        except Exception as e:
            if attempt == tries - 1:
                raise
            print(f"    retry {attempt + 1} after {type(e).__name__}: {str(e)[:60]}")
            time.sleep(delay)
            delay *= 2.5
    raise OSError("unreachable")


def cached(name, url):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if os.path.exists(p):
        return open(p, encoding="utf-8").read()
    html = fetch(url)
    open(p, "w", encoding="utf-8").write(html)
    time.sleep(PACE)
    return html


def books_in(html):
    """Every object carrying a bookId, from the __NEXT_DATA__ payload."""
    m = re.search(r'id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(1))
    except ValueError:
        return []
    found = []

    def walk(o):
        if isinstance(o, dict):
            if "bookId" in o and o.get("bookName"):
                found.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    return found


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    titles = {t["title_id"]: t["primary_title"]
              for t in csv.DictReader(open(os.path.join(DATA, "titles.csv"),
                                           newline="", encoding="utf-8"))}
    av = list(csv.DictReader(open(os.path.join(DATA, "availability.csv"),
                                  newline="", encoding="utf-8")))
    wanted = [r for r in av if r["platform_id"] == "dramabox" and not r["direct_link"].strip()]
    print(f"dramabox rows missing a direct_link: {len(wanted)}")

    # Genre 0 is the UNFILTERED catalogue and is paginated at /genres/0/<pageNo>,
    # 12 books a page. NOTE the pagination is a PATH SEGMENT: ?pageNo=2 and ?page=2
    # are both silently ignored and re-serve page 1, which would make a query-string
    # crawler collect the same 12 books N times and look like it worked.
    first = cached("genre_0_p1.html", f"{BASE}/genres/0/1")
    m = re.search(r'"pages":(\d+)', first)
    total = int(m.group(1)) if m else 1
    if limit:
        total = min(total, limit)
    print(f"catalogue pages to walk: {total} (12 books each)")

    index = {}          # norm(title) -> {bookId: {...}}
    for p in range(1, total + 1):
        try:
            html = cached(f"genre_0_p{p}.html", f"{BASE}/genres/0/{p}")
        except Exception as e:
            print(f"  [{p}/{total}] FAILED {str(e)[:60]}")
            continue
        bs = books_in(html)
        for b in bs:
            k = norm(b.get("bookName"))
            if not k:
                continue
            index.setdefault(k, {})[str(b["bookId"])] = {
                "bookName": b.get("bookName"),
                "chapterCount": b.get("chapterCount"),
            }
        if p % 25 == 0 or p == total:
            print(f"  [{p}/{total}] index now {len(index)} titles")

    resolved, ambiguous, missing = [], [], []
    for r in wanted:
        name = titles.get(r["title_id"], "")
        hits = index.get(norm(name), {})
        if len(hits) == 1:
            bid, meta = next(iter(hits.items()))
            slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", meta["bookName"].lower())).strip("-")
            resolved.append({
                "title_id": r["title_id"],
                "our_title": name,
                "platform_title": meta["bookName"],
                "book_id": bid,
                "direct_link": f"{BASE}/movie/{bid}/{slug}",
                "episode_count": meta.get("chapterCount"),
            })
        elif len(hits) > 1:
            ambiguous.append({"title_id": r["title_id"], "our_title": name,
                              "candidates": hits})
        else:
            missing.append({"title_id": r["title_id"], "our_title": name})

    out = {
        "source": "dramaboxdb.com /genres catalogue, " + time.strftime("%Y-%m-%d"),
        "method": "title -> bookId from the __NEXT_DATA__ payload of each /genres/<id> "
                  "page. Full normalised-title match only. NOT the robots-disallowed "
                  "/search endpoint.",
        "caption_rule": "NO SYNOPSIS TAKEN. direct_link and episode_count only.",
        "catalogue_size": len(index),
        "resolved": resolved,
        "ambiguous_needs_ruling": ambiguous,
        "not_in_catalogue": missing,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"\ncatalogue titles indexed : {len(index)}")
    print(f"RESOLVED                 : {len(resolved)}")
    print(f"ambiguous (two bookIds)  : {len(ambiguous)}")
    print(f"not in catalogue         : {len(missing)}")
    print(f"written {OUT}")


if __name__ == "__main__":
    main()
