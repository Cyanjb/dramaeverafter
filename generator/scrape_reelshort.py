#!/usr/bin/env python3
"""Weekly ReelShort scrape. Reads the platform, writes ONE dated staging JSON.
It never touches data/. merge_scrape.py does that, with the database rules.

WHY THIS EXISTS. The pipeline skill always said "weekly delta of ReelShort",
but the scrape only ever lived as a Claude session doing web fetches by hand,
and the cloud sandbox cannot reach any platform at all (adapters.md sec 14).
The last real scrape was 14 to 24 July 2026. GitHub's runners reach ReelShort
fine (the fetch-synopses workflow proved it on 2 Sep), so this script is written
to run unattended there, standard library only, and to survive a site that has
shifted since July: every route is optional, every failure is recorded, and a
run that discovers nothing still refreshes what we hold.

ROUTES, in order:
  tags     The 940 actor tag pages in harvest_queue.csv, paginated (adapters.md
           sec 1). Each page's __NEXT_DATA__ carries up to ten books with
           book_id, book_title, read_count, chapter_count, special_desc, and the
           /movie/{slug}-{id} href. This is the route that built the July
           catalogue, and it refreshes most known titles for free, with the
           actor credit attached.
  home     The homepage: every /movie/ href and every book dict in its
           __NEXT_DATA__ (new releases and trending rails).
  fandom   The newest 100 posts on the ReelShort fandom blog (adapters.md
           sec 3, open WordPress REST). Every /movie/ link in them is a title
           ReelShort is currently writing about. This is the route the 24 July
           weekly harvest used to find its five new titles.
  sitemap  OFF BY DEFAULT. /sitemap.xml and the usual variants, if ReelShort
           publishes one. A sitemap is a sweep, and Cyan's rule (8 Aug) is
           that new titles are CHOSEN, not swept: merge_scrape.py never
           creates a title seen only here. Useful for a catalogue count.
  detail   /movie/ pages (adapters.md sec 2) for every known link not already
           seen on a tag page, and for every newly discovered book id. A 404
           here means delisted: recorded, never deleted by a machine.

Politeness: serial, one desktop user agent, a pause between requests, one retry
on a network error, and an empty 200 body is treated as retryable (the fandom
host soft-blocks that way, adapters.md sec 20).

Usage:
    python3 generator/scrape_reelshort.py --out generator/staging/reelshort_2026-09-06.json
    python3 generator/scrape_reelshort.py --routes home,detail --limit 20   # a quick probe

Output:
  {"scraped_at", "routes": {route: {...counts}}, "books": {book_id: {
      "book_id", "slug", "url", "title", "views", "views_raw", "episodes",
      "synopsis", "poster", "actors": [...], "seen_via": [...], "status"}},
   "delisted": [{"title_id", "url", "status"}], "errors": [...]}
"""
import argparse, csv, datetime, io, json, math, os, re, sys, time
import urllib.error, urllib.request
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
STAGING = os.path.join(HERE, "staging")
BASE = "https://www.reelshort.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
PAUSE = 1.0
MOVIE_RE = re.compile(r"/movie/([a-z0-9]+(?:-[a-z0-9]+)*)-([0-9a-f]{24})\b")
NEXT_RE = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
LOC_RE = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")


# --- fetching -----------------------------------------------------------------

class Fetcher:
    def __init__(self, pause=PAUSE):
        self.pause = pause
        self.requests = 0

    def get(self, url):
        """(status, body). 0 = network failure after a retry."""
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Language": "en-US,en;q=0.9"})
        last = None
        for attempt in (1, 2):
            self.requests += 1
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    body = r.read().decode("utf-8", "replace")
                if body.strip():
                    time.sleep(self.pause)
                    return r.status, body
                last = "empty body"
            except urllib.error.HTTPError as e:
                time.sleep(self.pause)
                return e.code, ""
            except Exception as e:  # noqa: BLE001
                last = str(e)
            time.sleep(3 * attempt)
        return 0, "error: %s" % last


# --- parsing ------------------------------------------------------------------

def clean(s):
    s = unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(s.split())


def walk(obj, out):
    if isinstance(obj, dict):
        out.append(obj)
        for v in obj.values():
            walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, out)
    return out


def next_data(html):
    m = NEXT_RE.search(html)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def views_label(n):
    """Integer -> the K/M/B string the database stores ('218.1M', '875.3K')."""
    try:
        n = float(n)
    except (TypeError, ValueError):
        return ""
    if n >= 1e9:
        return "%.1fB" % (n / 1e9)
    if n >= 1e6:
        return "%.1fM" % (n / 1e6)
    if n >= 1e3:
        return "%.1fK" % (n / 1e3)
    return "%d" % n if n > 0 else ""


def views_of(raw):
    if raw is None or raw == "":
        return ""
    if isinstance(raw, (int, float)):
        return views_label(raw)
    s = str(raw).strip().upper().replace(",", "").replace(" ", "")
    if re.fullmatch(r"\d+(\.\d+)?", s):
        return views_label(float(s))
    if re.fullmatch(r"\d+(\.\d+)?[KMB]", s):
        return s
    return ""


def og_image(html):
    for pat in (r'<meta[^>]+(?:property|name)="og:image"[^>]+content="([^"]+)"',
                r'<meta[^>]+content="([^"]+)"[^>]+(?:property|name)="og:image"'):
        m = re.search(pat, html, re.I)
        if m:
            return unescape(m.group(1))
    return ""


def hrefs_of(html):
    """book_id -> slug for every /movie/ link in a page (HTML or JSON text)."""
    out = {}
    for slug, bid in MOVIE_RE.findall(html):
        out.setdefault(bid, slug)
    return out


def books_in(data, id_to_slug):
    """Every dict that looks like a ReelShort book. Yields normalised records."""
    for d in walk(data, []):
        title = d.get("book_title") or d.get("bookTitle")
        bid = d.get("book_id") or d.get("bookId") or d.get("id")
        if not title or not isinstance(bid, str) or not re.fullmatch(r"[0-9a-f]{24}", bid):
            continue
        raw = d.get("read_count", d.get("readCount", d.get("play_count", d.get("playCount"))))
        ep = d.get("chapter_count") or d.get("chapterCount") or ""
        pic = d.get("book_pic") or d.get("bookPic") or d.get("cover") or d.get("thumb") or ""
        actors = []
        ai = d.get("actor_info") or {}
        if isinstance(ai, dict):
            for a in ai.get("actors") or []:
                if isinstance(a, dict) and a.get("actor_name"):
                    actors.append(clean(a["actor_name"]))
        yield {
            "book_id": bid,
            "slug": id_to_slug.get(bid, ""),
            "title": clean(title),
            "views_raw": raw if isinstance(raw, (int, float, str)) else "",
            "views": views_of(raw),
            "episodes": str(ep) if ep else "",
            "synopsis": clean(d.get("special_desc") or d.get("specialDesc") or d.get("description") or ""),
            "poster": pic if isinstance(pic, str) else "",
            "actors": actors,
        }


# --- the run ------------------------------------------------------------------

class Run:
    def __init__(self, fetch):
        self.fetch = fetch
        self.books = {}
        self.delisted = []
        self.errors = []
        self.routes = {}

    def note(self, book, via, url=""):
        cur = self.books.get(book["book_id"])
        if cur is None:
            cur = dict(book, seen_via=[], actors=list(book["actors"]), status=200)
            self.books[book["book_id"]] = cur
        else:
            for k in ("title", "views", "views_raw", "episodes", "synopsis", "poster", "slug"):
                if book.get(k) and (not cur.get(k) or (k == "synopsis" and len(book[k]) > len(cur[k]))):
                    cur[k] = book[k]
            for a in book["actors"]:
                if a not in cur["actors"]:
                    cur["actors"].append(a)
        if via not in cur["seen_via"]:
            cur["seen_via"].append(via)
        if url and not cur.get("url"):
            cur["url"] = url
        if cur.get("slug") and not cur.get("url"):
            cur["url"] = "%s/movie/%s-%s" % (BASE, cur["slug"], cur["book_id"])
        return cur

    # route: actor tag pages
    def tags(self, queue, max_pages, limit):
        seen_ids, pages, failed = set(), 0, 0
        for i, row in enumerate(queue[:limit] if limit else queue):
            url = row["url"].rstrip("/")
            page = 1
            while page <= max_pages:
                status, html = self.fetch.get(url if page == 1 else "%s/%d" % (url, page))
                pages += 1
                if status != 200:
                    failed += 1
                    self.errors.append({"route": "tags", "url": url, "page": page, "status": status})
                    break
                data = next_data(html)
                if data is None:
                    failed += 1
                    self.errors.append({"route": "tags", "url": url, "page": page, "status": "no __NEXT_DATA__"})
                    break
                id_to_slug = hrefs_of(html)
                found = 0
                for b in books_in(data, id_to_slug):
                    b["actors"] = [row["actor"]] + [a for a in b["actors"] if a != row["actor"]]
                    self.note(b, "tags")
                    seen_ids.add(b["book_id"])
                    found += 1
                total, size = None, 10
                for d in walk(data, []):
                    if "total_items" in d and isinstance(d.get("total_items"), int):
                        total = d["total_items"]
                        size = d.get("page_size") or size
                        break
                if found == 0 or total is None or page * size >= total:
                    break
                page += 1
            print("tags %4d/%d %-32s books so far %d" % (i + 1, len(queue), row["actor"][:32], len(self.books)))
            sys.stdout.flush()
        self.routes["tags"] = {"actors": min(len(queue), limit or len(queue)), "pages": pages,
                               "failed": failed, "books": len(seen_ids)}

    # route: homepage rails
    def home(self):
        status, html = self.fetch.get(BASE + "/")
        info = {"status": status, "hrefs": 0, "books": 0}
        if status == 200:
            id_to_slug = hrefs_of(html)
            info["hrefs"] = len(id_to_slug)
            data = next_data(html)
            if data is not None:
                for b in books_in(data, id_to_slug):
                    self.note(b, "home")
                    info["books"] += 1
            for bid, slug in id_to_slug.items():
                if bid not in self.books:
                    self.note({"book_id": bid, "slug": slug, "title": "", "views": "", "views_raw": "",
                               "episodes": "", "synopsis": "", "poster": "", "actors": []}, "home")
        else:
            self.errors.append({"route": "home", "url": BASE + "/", "status": status})
        self.routes["home"] = info

    # route: fandom blog, newest posts
    def fandom(self, per_page=100):
        url = ("%s/fandom/wp-json/wp/v2/posts?per_page=%d&_fields=id,link,content,date"
               % (BASE, per_page))
        status, body = self.fetch.get(url)
        info = {"status": status, "posts": 0, "hrefs": 0}
        if status == 200:
            try:
                posts = json.loads(body)
            except ValueError:
                posts = []
            info["posts"] = len(posts) if isinstance(posts, list) else 0
            for bid, slug in hrefs_of(body).items():
                info["hrefs"] += 1
                self.note({"book_id": bid, "slug": slug, "title": "", "views": "", "views_raw": "",
                           "episodes": "", "synopsis": "", "poster": "", "actors": []}, "fandom")
        else:
            self.errors.append({"route": "fandom", "url": url, "status": status})
        self.routes["fandom"] = info

    # route: sitemap
    def sitemap(self, max_children=40):
        info = {"tried": [], "children": 0, "hrefs": 0}
        for path in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml", "/sitemaps/sitemap.xml"):
            status, body = self.fetch.get(BASE + path)
            info["tried"].append([path, status])
            if status != 200 or "<urlset" not in body and "<sitemapindex" not in body:
                continue
            queue = [body]
            children = 0
            while queue:
                doc = queue.pop(0)
                for bid, slug in hrefs_of(doc).items():
                    if bid not in self.books:
                        self.note({"book_id": bid, "slug": slug, "title": "", "views": "", "views_raw": "",
                                   "episodes": "", "synopsis": "", "poster": "", "actors": []}, "sitemap")
                        info["hrefs"] += 1
                if "<sitemapindex" in doc:
                    for loc in LOC_RE.findall(doc):
                        if children >= max_children:
                            break
                        children += 1
                        s, child = self.fetch.get(loc)
                        if s == 200:
                            queue.append(child)
            info["children"] = children
            break
        self.routes["sitemap"] = info

    # route: detail pages
    def detail(self, targets):
        """targets: [(book_id, url, title_id_or_None)] not yet carrying data."""
        ok = missing = failed = 0
        for i, (bid, url, tid) in enumerate(targets):
            status, html = self.fetch.get(url)
            if status == 404:
                missing += 1
                self.delisted.append({"title_id": tid or "", "book_id": bid, "url": url, "status": 404})
                if bid in self.books:
                    self.books[bid]["status"] = 404
            elif status != 200:
                failed += 1
                self.errors.append({"route": "detail", "url": url, "status": status})
                if bid in self.books:
                    self.books[bid]["status"] = status
            else:
                data = next_data(html)
                id_to_slug = hrefs_of(html)
                got = None
                if data is not None:
                    for b in books_in(data, id_to_slug):
                        if b["book_id"] == bid or got is None:
                            got = b
                            if b["book_id"] == bid:
                                break
                if got is None or got["book_id"] != bid:
                    failed += 1
                    self.errors.append({"route": "detail", "url": url, "status": "no book object"})
                    continue
                if not got["poster"]:
                    got["poster"] = og_image(html)
                cur = self.note(got, "detail", url=url)
                cur["status"] = 200
                ok += 1
            print("detail %4d/%d %s %s" % (i + 1, len(targets), status, url[-60:]))
            sys.stdout.flush()
        self.routes["detail"] = {"targets": len(targets), "ok": ok, "delisted": missing, "failed": failed}


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--routes", default="tags,home,fandom,detail",
                    help="comma list from tags,home,fandom,sitemap,detail")
    ap.add_argument("--limit", type=int, default=0, help="cap actor tag pages and detail targets (probe runs)")
    ap.add_argument("--tag-pages-max", type=int, default=8)
    ap.add_argument("--pause", type=float, default=PAUSE)
    a = ap.parse_args()
    routes = [r.strip() for r in a.routes.split(",") if r.strip()]

    fetch = Fetcher(a.pause)
    run = Run(fetch)
    started = datetime.datetime.now(datetime.timezone.utc)

    known = {}   # book_id -> (url, title_id) for every ReelShort link we hold
    for r in rows("availability.csv"):
        if r["platform_id"] != "reelshort" or not r["direct_link"]:
            continue
        m = MOVIE_RE.search(r["direct_link"])
        if m:
            known[m.group(2)] = (r["direct_link"], r["title_id"])

    if "tags" in routes:
        queue = [h for h in rows("harvest_queue.csv")
                 if "reelshort.com/tags/" in h["url"] and h["status"] != "dead_404"]
        run.tags(queue, a.tag_pages_max, a.limit)
    if "home" in routes:
        run.home()
    if "fandom" in routes:
        run.fandom()
    if "sitemap" in routes:
        run.sitemap()
    if "detail" in routes:
        targets = []
        for bid, (url, tid) in known.items():
            b = run.books.get(bid)
            if b is None or not b.get("views"):
                targets.append((bid, url, tid))
        for bid, b in run.books.items():
            if bid not in known and not b.get("title"):
                targets.append((bid, b.get("url") or "%s/movie/%s-%s" % (BASE, b["slug"], bid), None))
        if a.limit:
            targets = targets[:a.limit]
        run.detail(targets)

    for bid, b in run.books.items():
        b["known_title_id"] = known.get(bid, ("", ""))[1]

    out = {
        "scraped_at": started.isoformat(timespec="seconds"),
        "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "requests": fetch.requests,
        "routes": run.routes,
        "books": dict(sorted(run.books.items())),
        "delisted": run.delisted,
        "errors": run.errors,
    }
    out_path = a.out or os.path.join(STAGING, "reelshort_%s.json" % started.date().isoformat())
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n")

    new = sum(1 for b in run.books.values() if not b["known_title_id"] and b.get("title"))
    fresh = sum(1 for b in run.books.values() if b["known_title_id"] and b.get("views"))
    print("\nwrote %s" % out_path)
    print("requests %d | books %d | known refreshed %d | new candidates %d | delisted %d | errors %d"
          % (fetch.requests, len(run.books), fresh, new, len(run.delisted), len(run.errors)))
    print("routes:", json.dumps(run.routes))
    return 0 if run.books else 1


if __name__ == "__main__":
    sys.exit(main())
