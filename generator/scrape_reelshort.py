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
  wanted   generator/staging/reelshort_wanted.txt: /movie/ URLs Cyan names,
           one per line. "A Zombie Girl's Journey Home" (3 Sep 2026) has no
           human cast, so no actor tag page can surface it; a named title is
           the purest form of "chosen, not swept". Fetched every run.
  genres   generator/staging/reelshort_tags.txt: ReelShort's own genre, mood,
           theme, style and story-beat tag pages (/tags/movie-moods/...,
           /tags/story-beats/..., found 3 Sep 2026), same __NEXT_DATA__ shape
           as actor tags, paginated with /2, /3. The drama style tag alone runs
           160+ pages, so this is close to the whole catalogue with view counts,
           and it is how a title with NO human cast (an AI animated original)
           can be found at all. It asserts no credits. merge_scrape.py creates
           from it only above a view threshold: most popular, not swept.
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
import argparse, csv, datetime, io, json, os, re, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request
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


def slugify(title):
    """ReelShort's own slug style, which is also the house style: lower case,
    every run of non-alphanumerics becomes one hyphen ("The Alpha's Daughter"
    -> the-alpha-s-daughter). Used only when a page gave us a book with no
    href; the detail route then fetches that URL to confirm it resolves."""
    s = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def canonical_slug(html, bid):
    """The page's own /movie/ URL for this book id, from canonical or og:url."""
    for pat in (r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"',
                r'<meta[^>]+(?:property|name)="og:url"[^>]+content="([^"]+)"'):
        m = re.search(pat, html, re.I)
        if m:
            mm = MOVIE_RE.search(unescape(m.group(1)))
            if mm and mm.group(2) == bid:
                return mm.group(1)
    return ""


def year_hint(d):
    """A release year from a book dict, if it carries one. The July scrape left
    year blank on 439 of 575 ReelShort titles, and the New releases rail keys
    on year, so any dated field is worth taking: an epoch (seconds or ms) or an
    ISO date under a key that mentions time, date, publish, online or release.
    Returns '' rather than guess."""
    for k, v in d.items():
        kl = k.lower()
        if not any(w in kl for w in ("time", "date", "publish", "online", "release", "year")):
            continue
        if kl in ("year",) and str(v).isdigit() and 2000 <= int(v) <= 2100:
            return str(v)
        if isinstance(v, (int, float)) and v > 0:
            secs = v / 1000.0 if v > 1e11 else v
            if 1.3e9 < secs < 2.2e9:
                return str(datetime.datetime.fromtimestamp(secs, datetime.timezone.utc).year)
        if isinstance(v, str):
            m = re.match(r"\s*(20\d\d)-\d\d-\d\d", v)
            if m:
                return m.group(1)
    return ""


def year_from_ldjson(html):
    for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            continue
        for d in walk(data, []):
            for key in ("datePublished", "dateCreated", "startDate", "uploadDate"):
                v = d.get(key)
                if isinstance(v, str) and re.match(r"20\d\d", v):
                    return v[:4]
    return ""


def bare(s):
    """Leading article off first, then letters and digits only (the matching
    key merge_scrape.py uses; the order matters, see READ FIRST)."""
    s = re.sub(r"^(the|a|an)\s+", "", (s or "").strip().lower())
    return re.sub(r"[^a-z0-9]", "", s)


def parse_wanted_line(raw):
    """'<head> [k=v ...]  # comment' -> (head, {k: v}). Trailing tokens that
    contain '=' are flags; everything before them is the head, which may hold
    spaces (a title as Cyan says it)."""
    line = raw.split("#", 1)[0].strip()
    if not line:
        return "", {}
    toks = line.split()
    flags = {}
    while toks and "=" in toks[-1]:
        k, v = toks.pop().split("=", 1)
        flags[k.strip().lower()] = v.strip()
    return " ".join(toks), flags


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
        year = year_hint(d)
        slug = id_to_slug.get(bid, "")
        if not slug:
            # The homepage rails carry books with no href in the HTML (probe,
            # 3 Sep 2026: 128 books, 0 hrefs). The dict itself may hold the URL.
            m = MOVIE_RE.search(json.dumps(d).replace("\\/", "/"))
            if m and m.group(2) == bid:
                slug = m.group(1)
        yield {
            "book_id": bid,
            "slug": slug,
            "title": clean(title),
            "views_raw": raw if isinstance(raw, (int, float, str)) else "",
            "views": views_of(raw),
            "episodes": str(ep) if ep else "",
            "synopsis": clean(d.get("special_desc") or d.get("specialDesc") or d.get("description") or ""),
            "poster": pic if isinstance(pic, str) else "",
            "actors": actors,
            "year": year,
        }


# --- the run ------------------------------------------------------------------

def tag_title(html):
    """'Zombie Movie List | ReelShort' -> 'zombie'; 'Enemies to Lovers Movie
    Collection | ReelShort' -> 'enemies to lovers'. The tag's own name, in
    English, from the page title; the URL slug may be localised."""
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if not m:
        return ""
    t = clean(m.group(1))
    t = re.sub(r"\s*\|\s*ReelShort.*$", "", t, flags=re.I)
    t = re.sub(r"\s+(Movie|Movies|Drama|Dramas)\s+(List|Collection)s?$", "", t, flags=re.I)
    return t.strip().lower()


AI_SAYS_RE = re.compile(r"AI[- ]generated", re.I)


class Run:
    def __init__(self, fetch):
        self.fetch = fetch
        self.books = {}
        self.delisted = []
        self.errors = []
        self.routes = {}
        self.discovered_tags = set()

    def note(self, book, via, url="", fresh=True):
        """fresh=True: this run read the platform, so views and counts are the
        newest and REPLACE what is held. fresh=False: preloading an earlier run's
        record from the same day, fill only."""
        cur = self.books.get(book["book_id"])
        if cur is None:
            cur = dict(book, seen_via=[], actors=list(book.get("actors") or []), status=book.get("status", 200))
            cur.setdefault("tags", [])
            self.books[book["book_id"]] = cur
        else:
            for k in ("title", "views", "views_raw", "episodes", "synopsis", "poster", "slug", "year"):
                if not book.get(k):
                    continue
                if fresh and k in ("views", "views_raw", "episodes"):
                    cur[k] = book[k]
                elif not cur.get(k) or (k == "synopsis" and len(book[k]) > len(cur.get(k) or "")):
                    cur[k] = book[k]
            for a in book.get("actors") or []:
                if a not in cur["actors"]:
                    cur["actors"].append(a)
        for tg in book.get("tags") or []:
            if tg not in cur.setdefault("tags", []):
                cur["tags"].append(tg)
        if book.get("platform_says_ai"):
            cur["platform_says_ai"] = True
        if via not in cur["seen_via"]:
            cur["seen_via"].append(via)
        if url and not cur.get("url"):
            cur["url"] = url
        if cur.get("slug") and not cur.get("url"):
            cur["url"] = "%s/movie/%s-%s" % (BASE, cur["slug"], cur["book_id"])
        return cur

    # route: tag pages (actor tags credit the actor; genre tags do not)
    def tags(self, queue, max_pages, limit, via="tags"):
        seen_ids, pages, failed = set(), 0, 0
        for i, row in enumerate(queue[:limit] if limit else queue):
            url = re.sub(r"/\d+$", "", row["url"].rstrip("/"))
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
                if page == 1:
                    for t_url in set(re.findall(r'href="(/tags/[a-z-]+/[^"/]+-[0-9a-f]{24})', html)):
                        self.discovered_tags.add(BASE + t_url)
                tag_name = "" if row.get("actor") else tag_title(html)
                found = 0
                for b in books_in(data, id_to_slug):
                    if row.get("actor"):
                        b["actors"] = [row["actor"]] + [a for a in b["actors"] if a != row["actor"]]
                    else:
                        b["actors"] = []   # a genre page asserts no credit; actor_info there is noise
                        if tag_name:
                            b["tags"] = [tag_name]   # ReelShort's own tag for this book
                    self.note(b, via)
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
            print("%s %4d/%d %-32s pages %d books so far %d"
                  % (via, i + 1, len(queue), (row.get("actor") or url.rsplit("/", 1)[-1])[:32], pages, len(self.books)))
            sys.stdout.flush()
        self.routes[via] = {"pages_listed": min(len(queue), limit or len(queue)), "pages": pages,
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

    # route: titles Cyan named, by URL or by name
    def wanted(self, path, held):
        """held: set of bare() forms of every title and alt title we hold.
        A line is `<URL or name or slug> [ai=yes|no] [tropes=a;b]`. A URL is
        fetched. A name we already hold is a ruling only (merge_scrape applies
        the flags). A name we do not hold is resolved through ReelShort's own
        search page, accepted only on an exact title match, then fetched."""
        info = {"file": os.path.basename(path), "urls": 0, "held": 0, "searched": 0,
                "resolved": 0, "unresolved": 0}
        if os.path.exists(path):
            for raw in io.open(path, encoding="utf-8"):
                head, flags = parse_wanted_line(raw)
                if not head:
                    continue
                m = MOVIE_RE.search(head)
                if m:
                    info["urls"] += 1
                    self.note({"book_id": m.group(2), "slug": m.group(1), "title": "", "views": "",
                               "views_raw": "", "episodes": "", "synopsis": "", "poster": "",
                               "actors": [], "year": ""}, "wanted")
                    continue
                name = head.replace("-", " ") if re.fullmatch(r"[a-z0-9-]+", head) else head
                if bare(name) in held:
                    info["held"] += 1
                    continue
                info["searched"] += 1
                found = self.search(name)
                if found:
                    info["resolved"] += 1
                    self.note(found, "wanted")
                else:
                    info["unresolved"] += 1
        self.routes["wanted"] = info

    def search(self, name):
        """ReelShort's /search?keywords= page, __NEXT_DATA__ books, exact title
        match on the bare form only. Anything looser would attach a stranger's
        show to Cyan's name for it."""
        url = "%s/search?keywords=%s" % (BASE, urllib.parse.quote_plus(name))
        status, html = self.fetch.get(url)
        if status != 200:
            self.errors.append({"route": "wanted", "query": name, "status": status})
            return None
        data = next_data(html)
        id_to_slug = hrefs_of(html)
        cands = [b for b in books_in(data, id_to_slug)] if data is not None else []
        exact = [b for b in cands if bare(b["title"]) == bare(name)]
        if len(exact) != 1:
            self.errors.append({"route": "wanted", "query": name,
                                "status": "search: %d exact of %d results" % (len(exact), len(cands))})
            return None
        b = exact[0]
        if not b["slug"]:
            b["slug"] = slugify(b["title"])
            b["slug_guessed"] = True
        return b

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
            # WordPress JSON escapes slashes ("\/movie\/"), so match on the
            # unescaped text (probe, 3 Sep 2026: 100 posts, 0 hrefs before this).
            for bid, slug in hrefs_of(body.replace("\\/", "/")).items():
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
                if not got.get("year"):
                    got["year"] = year_from_ldjson(html)
                if AI_SAYS_RE.search(html):
                    # The page itself says AI-generated (ReelShort's AI animated
                    # originals carry this in their description). Evidence for
                    # Cyan's ruling, never the ruling: merge_scrape reports it.
                    got["platform_says_ai"] = True
                true_slug =canonical_slug(html, bid) or got["slug"] or id_to_slug.get(bid, "")
                cur = self.note(got, "detail", url=url)
                if true_slug:
                    cur["slug"] = true_slug
                    cur["url"] = "%s/movie/%s-%s" % (BASE, true_slug, bid)
                cur["slug_guessed"] = False
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
    ap.add_argument("--routes", default="tags,genres,home,fandom,wanted,detail",
                    help="comma list from tags,genres,home,fandom,wanted,sitemap,detail")
    ap.add_argument("--limit", type=int, default=0, help="cap actor tag pages and detail targets (probe runs)")
    ap.add_argument("--tag-pages-max", type=int, default=8, help="pages per actor tag")
    ap.add_argument("--genre-pages-max", type=int, default=250, help="pages per genre tag")
    ap.add_argument("--pause", type=float, default=PAUSE)
    a = ap.parse_args()
    routes = [r.strip() for r in a.routes.split(",") if r.strip()]

    fetch = Fetcher(a.pause)
    run = Run(fetch)
    started = datetime.datetime.now(datetime.timezone.utc)
    out_path = a.out or os.path.join(STAGING, "reelshort_%s.json" % started.date().isoformat())

    # A SECOND RUN ON THE SAME DAY MERGES INTO THE DAY'S FILE, never overwrites
    # it (the handover trap of 24 Aug, and it bit again on 3 Sep: run 4 replaced
    # run 3's record of 753 books). Earlier books are kept as a base; anything
    # this run reads replaces their counts.
    earlier_runs = []
    if os.path.exists(out_path):
        try:
            prev = json.load(io.open(out_path, encoding="utf-8"))
        except ValueError:
            prev = {}
        for bid, b in (prev.get("books") or {}).items():
            b = dict(b)
            vias = b.pop("seen_via", []) or []
            run.note(b, vias[0] if vias else "earlier", fresh=False)
            for v in vias:
                if v not in run.books[bid]["seen_via"]:
                    run.books[bid]["seen_via"].append(v)
        run.delisted = list(prev.get("delisted") or [])
        earlier_runs = list(prev.get("runs") or [])
        if prev.get("scraped_at") and not any(r.get("scraped_at") == prev["scraped_at"] for r in earlier_runs):
            earlier_runs.append({"scraped_at": prev.get("scraped_at"), "finished_at": prev.get("finished_at"),
                                 "requests": prev.get("requests"), "routes": prev.get("routes")})
        run.discovered_tags.update(prev.get("discovered_tags") or [])
        print("preloaded %d books from %s" % (len(run.books), os.path.basename(out_path)))

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
    if "genres" in routes:
        path = os.path.join(STAGING, "reelshort_tags.txt")
        queue = [{"url": ln.strip(), "actor": ""} for ln in io.open(path, encoding="utf-8")
                 if ln.strip() and not ln.startswith("#")] if os.path.exists(path) else []
        run.tags(queue, a.genre_pages_max, 0, via="genres")
    if "home" in routes:
        run.home()
    if "fandom" in routes:
        run.fandom()
    if "wanted" in routes:
        held = set()
        for t in rows("titles.csv"):
            held.add(bare(t["primary_title"]))
            for alt in re.split(r"[|;]", t.get("alt_titles") or ""):
                if alt.strip():
                    held.add(bare(alt))
        run.wanted(os.path.join(STAGING, "reelshort_wanted.txt"), held)
    if "sitemap" in routes:
        run.sitemap()
    # A book with a title but no href gets a slug in ReelShort's own style; the
    # detail route then has to confirm the URL resolves before the merge may
    # trust it, so those books are always detail targets.
    for bid, b in run.books.items():
        if bid not in known and not b.get("slug") and b.get("title"):
            b["slug"] = slugify(b["title"])
            b["slug_guessed"] = True
            b["url"] = "%s/movie/%s-%s" % (BASE, b["slug"], bid)
    if "detail" in routes:
        targets = []
        for bid, (url, tid) in known.items():
            b = run.books.get(bid)
            if b is None or not b.get("views"):
                targets.append((bid, url, tid))
        # Unknown books: fetch when there is no title yet, when the slug was
        # guessed, or when the rail gave no view count (probe 2, 3 Sep: several
        # homepage books arrived with a title and no read_count; a new title
        # with no views ranks nowhere and its page would show no episodes).
        for bid, b in run.books.items():
            if bid in known or not b.get("slug"):
                continue
            if not b.get("title") or b.get("slug_guessed") or not b.get("views"):
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
        "runs": earlier_runs,
        "discovered_tags": sorted(run.discovered_tags),
        "books": dict(sorted(run.books.items())),
        "delisted": run.delisted,
        "errors": run.errors,
    }
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
