#!/usr/bin/env python3
"""Weekly DramaBox scrape. Reads the platform, writes ONE dated staging JSON.
It never touches data/. merge_dramabox.py does that, with the database rules.

WHY NOW. DramaBox was bot-walled from July to September (adapters.md sec 8)
and came back readable on 28 Sep 2026 (sec 29): www.dramaboxdb.com answers
200 to a desktop user agent, and its Next.js pages carry the real play count
and the cast. Cyan approved adding it to the Sunday run the same day. It is
where our reach ranking is blindest: every one of our top 100 by reach was
ReelShort.

ROBOTS. dramaboxdb.com/robots.txt is "Allow: /" with a disallow list that
includes /search?* (so the actor search the research pass used is OFF LIMITS
here) and /downloadapp, /content, /uc, /renewal, /product. Every route below is
outside that list. The script reads robots.txt at the start of every run and
refuses any path it disallows, so a tightened robots.txt stops the route rather
than being ignored. There is no sitemap (/sitemap.xml 404, none in robots).

ROUTES, in order (all verified live 28 Sep 2026):
  trending  The chart, /channel/trending, /2, /3, /4 (pageProps.moreData.items,
            18 a page, pageProps.pages says how many). Each item has bookId,
            bookName, introduction, chapterCount, tags, and a viewCount that is a
            small web-only number, NOT the play count. Chart position is kept.
  home      The homepage rails: pageProps.bigList (the banner) and smallData
            (must-sees 1272, trending 1273, hidden gems 1274; six books each).
  channels  /channel/must-sees and /channel/hidden-gems, paginated like the
            chart. Editorial rails: seen here is not "most popular" by itself.
  known     Every DramaBox link we hold in availability.csv. Three URL shapes
            are on file (www.dramaboxdb.com/movie/<id>/<slug>, dramaboxdb.com/
            movie/<id>/<slug>, www.dramabox.com/drama/<id>/<Slug>); the numeric
            bookId is the same in all of them and dramaboxdb.com/movie/<id>
            redirects to the canonical page, so each maps to one book id.
  cast      /name/<performerId> for every performer whose name matches exactly
            one person in people.csv (name or aka_names). The id is only ever
            learned from a title page's performerList (the actor search is
            robots-disallowed), and every id learned is kept in the staging JSON
            so later runs start with it. The page lists the performer's books.
  detail    /movie/<bookId> for every book above: bookInfo has viewCount (the
            real play count), followCount, introduction, chapterCount, tags,
            language, firstShelfTime and performerList (names, ids, photos). A
            404 is recorded as delisted; nothing is deleted by a machine.
            Detail runs twice: once for the chart and rails (which teaches us
            performer ids), then once more for books the cast route found.

DUBS. DramaBox lists an English dub of a Chinese production as
"<Name> (DUBBED)". The book keeps its listed title; `name` is the title with
the marker stripped and `dubbed` is true. The merge files it by `name` with
version=english-dub and origin=chinese (adapters.md sec 11, CONVENTIONS.md).

`slug` in the output is the HOUSE slug (ReelShort's style: lower case, every
run of non-alphanumerics one hyphen, so apostrophes become hyphens) of `name`,
which is the title_id the merge would give a new title. DramaBox's own URL
slug drops apostrophes, so it is kept separately as `db_slug`.

Politeness: serial, one desktop user agent, 1 to 1.5 s between requests, one
retry on a network error or an empty 200 body, TLS verification always on.

Usage:
    python3 generator/scrape_dramabox.py --out generator/staging/dramabox_2026-10-04.json
    python3 generator/scrape_dramabox.py --limit 30     # a quick probe
    python3 generator/scrape_dramabox.py --routes trending,known,detail

Output:
  {"scraped_at", "routes": {route: {...counts}}, "performers": {id: name},
   "books": {book_id: {"book_id", "title", "name", "dubbed", "slug", "db_slug",
      "url", "synopsis", "episodes", "views", "views_raw", "follows", "tags",
      "genres", "cast": [{"id", "name", "photo"}], "actors": [...], "language",
      "first_shelf", "year", "poster", "seen_via": [...], "rank", "status",
      "known_title_id"}},
   "delisted": [...], "errors": [...]}
"""
import argparse, csv, datetime, glob, io, json, os, random, re, sys, time, unicodedata
import urllib.error, urllib.parse, urllib.request
from html import unescape

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
STAGING = os.path.join(HERE, "staging")
BASE = "https://www.dramaboxdb.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
PAUSE = (1.0, 1.5)
NEXT_RE = re.compile(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
# Any DramaBox title URL we hold, on any of its hosts: the bookId is the key.
LINK_RE = re.compile(r"dramabox(?:db|app)?\.com/(?:[a-z]{2}(?:Hans)?/)?(?:movie|drama|video)/(\d{8,})", re.I)
# Half- or full-width brackets: "X (DUBBED)", "X （DUBBED）", "X （DUBBED)" are
# all on the site (28 Sep 2026).
DUB_RE = re.compile(r"\s*[\(\[（【]\s*(dubbed|eng(lish)?\s*dub(bed)?)\s*[\)\]）】]\s*", re.I)
CHANNELS = ("must-sees", "hidden-gems")


# --- fetching -----------------------------------------------------------------

class Fetcher:
    def __init__(self, pause=PAUSE):
        self.pause = pause
        self.requests = 0
        self.robots = None

    def sleep(self):
        time.sleep(random.uniform(*self.pause))

    def allowed(self, url):
        """Google's robots semantics: the longest matching rule wins, '*' is a
        wildcard, '$' anchors. (urllib.robotparser takes the FIRST match, and
        DramaBox's file opens with "Allow: /", which would allow everything.)"""
        if not self.robots:
            return True
        u = urllib.parse.urlsplit(url)
        target = (u.path or "/") + ("?" + u.query if u.query else "")
        best = (-1, True)
        for allow, pat in self.robots:
            rx = "^" + re.escape(pat).replace(r"\*", ".*")
            if rx.endswith(r"\$"):
                rx = rx[:-2] + "$"
            if re.match(rx, target) and (len(pat) > best[0] or (len(pat) == best[0] and allow)):
                best = (len(pat), allow)
        return best[1]

    def get(self, url, check_robots=True):
        """(status, body). 0 = network failure after a retry; -1 = robots says no."""
        if check_robots and not self.allowed(url):
            return -1, ""
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml",
            "Accept-Language": "en-US,en;q=0.9"})
        last = None
        for attempt in (1, 2):
            self.requests += 1
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    body = r.read().decode("utf-8", "replace")
                    status = r.status
                self.sleep()
                if body.strip():
                    return status, body
                last = "empty body"
            except urllib.error.HTTPError as e:
                self.sleep()
                return e.code, ""
            except Exception as e:  # noqa: BLE001
                last = str(e)
            time.sleep(3 * attempt)
        return 0, "error: %s" % last


def robots_rules(body):
    """[(allow, pattern)] for the 'User-agent: *' group."""
    rules, mine = [], False
    for ln in body.splitlines():
        ln = ln.split("#", 1)[0].strip()
        if ":" not in ln:
            continue
        k, v = [x.strip() for x in ln.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            mine = v == "*"
        elif mine and k in ("allow", "disallow") and v:
            rules.append((k == "allow", v))
    return rules


# --- parsing ------------------------------------------------------------------

def clean(s):
    s = unescape(s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(s.split())


def next_data(html):
    m = NEXT_RE.search(html or "")
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def page_props(html):
    d = next_data(html)
    return ((d or {}).get("props") or {}).get("pageProps") if d else None


def views_label(n):
    """Integer -> the K/M/B string the database stores ('267.2M', '875.3K')."""
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


def house_slug(title):
    """The house slug style (CONVENTIONS.md): lower case, every run of
    non-alphanumerics one hyphen, so apostrophes become hyphens."""
    s = unicodedata.normalize("NFKD", title or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def split_dub(title):
    """'Ruling Over All I See (DUBBED) ' -> ('Ruling Over All I See', True)."""
    t = clean(title)
    name = DUB_RE.sub(" ", t).strip()
    return (name, True) if name != t else (t, False)


def book_record(d):
    """A DramaBox book dict (chart item, rail item, actor-page item or bookInfo)
    -> our normalised record. Fields a source lacks are left empty."""
    bid = str(d.get("bookId") or d.get("action") or "")
    if not re.fullmatch(r"\d{8,}", bid):
        return None
    title = clean(d.get("bookName") or d.get("name") or "")
    name, dubbed = split_dub(title)
    tags = []
    for x in (d.get("tags") or []) + (d.get("labels") or []):
        x = clean(x if isinstance(x, str) else "")
        if x and x not in tags:
            tags.append(x)
    genres = [clean(x) for x in (d.get("typeTwoNames") or []) if isinstance(x, str)]
    cast, actors = [], []
    for p in d.get("performerList") or []:
        if isinstance(p, dict) and p.get("performerName"):
            nm = clean(p["performerName"])
            cast.append({"id": str(p.get("performerId") or ""), "name": nm,
                         "photo": p.get("performerAvatar") or ""})
            actors.append(nm)
    shelf = d.get("firstShelfTime") or d.get("shelfTime") or ""
    cover = d.get("cover") or ""
    return {
        "book_id": bid, "title": title, "name": name, "dubbed": dubbed,
        "slug": house_slug(name), "db_slug": "",
        "synopsis": clean(d.get("introduction") or ""),
        "episodes": str(d.get("chapterCount") or ""),
        "tags": tags, "genres": genres, "cast": cast, "actors": actors,
        "language": d.get("language") or "",
        "first_shelf": shelf[:10] if isinstance(shelf, str) else "",
        "year": shelf[:4] if isinstance(shelf, str) and re.match(r"20\d\d", shelf) else "",
        "poster": re.sub(r"@w=\d+&h=\d+$", "", cover) if isinstance(cover, str) else "",
        "follows": d.get("followCount") if isinstance(d.get("followCount"), int) else "",
        # Rails and the chart carry a small web-only viewCount; only a title
        # page's bookInfo carries the play count. Those are set in detail().
        "views": "", "views_raw": "",
    }


# --- the run ------------------------------------------------------------------

class Run:
    def __init__(self, fetch):
        self.fetch = fetch
        self.books = {}
        self.delisted = []
        self.errors = []
        self.routes = {}
        self.performers = {}      # performerId -> name, every one seen on a title page
        self.detailed = set()

    def note(self, rec, via, fresh=True):
        cur = self.books.get(rec["book_id"])
        if cur is None:
            cur = dict(rec, seen_via=[], status=rec.get("status", 200))
            cur["tags"] = list(rec.get("tags") or [])
            self.books[rec["book_id"]] = cur
        else:
            for k, v in rec.items():
                if k in ("seen_via", "tags", "cast", "actors"):
                    continue
                if v in ("", None, [], False):
                    continue
                if fresh and k in ("views", "views_raw", "episodes", "follows", "status", "title",
                                   "name", "slug", "dubbed", "url", "db_slug"):
                    cur[k] = v
                elif not cur.get(k) or (k == "synopsis" and len(v) > len(cur.get(k) or "")):
                    cur[k] = v
            for tg in rec.get("tags") or []:
                if tg not in cur["tags"]:
                    cur["tags"].append(tg)
            if rec.get("cast"):
                cur["cast"], cur["actors"] = rec["cast"], rec["actors"]
        if via and via not in cur["seen_via"]:
            cur["seen_via"].append(via)
        if not cur.get("url"):
            cur["url"] = "%s/movie/%s" % (BASE, cur["book_id"])
        return cur

    def listing(self, route, path, max_pages):
        """A paginated /channel/<x> listing. Returns books seen."""
        seen, pages, failed, total_pages = 0, 0, 0, None
        page = 1
        while page <= max_pages and (total_pages is None or page <= total_pages):
            url = BASE + path + ("" if page == 1 else "/%d" % page)
            status, html = self.fetch.get(url)
            pages += 1
            pp = page_props(html) if status == 200 else None
            if pp is None:
                failed += 1
                self.errors.append({"route": route, "url": url, "status": status if status != 200 else "no __NEXT_DATA__"})
                break
            total_pages = pp.get("pages") if isinstance(pp.get("pages"), int) else total_pages
            items = ((pp.get("moreData") or {}).get("items")) or []
            for i, it in enumerate(items):
                rec = book_record(it)
                if rec is None:
                    continue
                cur = self.note(rec, route)
                if route == "trending" and not cur.get("rank"):
                    cur["rank"] = (page - 1) * 18 + i + 1
                seen += 1
            if not items:
                break
            page += 1
        return {"pages": pages, "pages_listed": total_pages, "books": seen, "failed": failed}

    def trending(self, max_pages):
        self.routes["trending"] = self.listing("trending", "/channel/trending", max_pages)

    def channels(self, max_pages):
        self.routes["channels"] = {c: self.listing("channel:" + c, "/channel/" + c, max_pages) for c in CHANNELS}

    def home(self):
        status, html = self.fetch.get(BASE + "/")
        pp = page_props(html) if status == 200 else None
        info = {"status": status, "books": 0, "rails": {}}
        if pp is None:
            self.errors.append({"route": "home", "url": BASE + "/", "status": status})
        else:
            for it in pp.get("bigList") or []:
                rec = book_record(it)
                if rec:
                    self.note(rec, "home")
                    info["books"] += 1
            for rail in pp.get("smallData") or []:
                info["rails"][str(rail.get("id"))] = len(rail.get("items") or [])
                for it in rail.get("items") or []:
                    rec = book_record(it)
                    if rec:
                        self.note(rec, "home")
                        info["books"] += 1
        self.routes["home"] = info

    def known(self, known):
        for bid, (url, tid) in known.items():
            self.note({"book_id": bid, "title": "", "name": "", "dubbed": False, "slug": "",
                       "url": "%s/movie/%s" % (BASE, bid), "tags": []}, "known")
        self.routes["known"] = {"links_held": len(known)}

    def cast(self, tracked, limit):
        """tracked: {performerId: person name} whose name is one of our people."""
        ok = failed = books = 0
        items = sorted(tracked.items())
        if limit:
            items = items[:limit]
        for pid, nm in items:
            page, pages = 1, 1
            while page <= pages and page <= 5:
                url = "%s/name/%s" % (BASE, pid) + ("" if page == 1 else "/%d" % page)
                status, html = self.fetch.get(url)
                pp = page_props(html) if status == 200 else None
                if pp is None or not isinstance(pp.get("actorData"), list):
                    failed += 1
                    self.errors.append({"route": "cast", "url": url, "status": status})
                    break
                # The page must be the performer we asked for, by name.
                if clean(pp.get("performerName") or "").lower() != nm.lower():
                    failed += 1
                    self.errors.append({"route": "cast", "url": url,
                                        "status": "name mismatch: %s" % pp.get("performerName")})
                    break
                pages = pp.get("pages") if isinstance(pp.get("pages"), int) else 1
                for it in pp["actorData"]:
                    rec = book_record(it)
                    if rec is None:
                        continue
                    cur = self.note(rec, "cast")
                    cur.setdefault("cast_pages", [])
                    if nm not in cur["cast_pages"]:
                        cur["cast_pages"].append(nm)
                    books += 1
                ok += 1
                page += 1
            print("cast %-28s pages %d books so far %d" % (nm[:28], page - 1, len(self.books)))
            sys.stdout.flush()
        self.routes["cast"] = {"performers": len(items), "pages_ok": ok, "failed": failed, "books": books}

    def detail(self, targets, label):
        ok = missing = failed = 0
        for i, (bid, tid) in enumerate(targets):
            url = "%s/movie/%s" % (BASE, bid)
            cur = self.books.get(bid)
            if cur and cur.get("db_slug"):
                url += "/" + cur["db_slug"]
            status, html = self.fetch.get(url)
            self.detailed.add(bid)
            if status == 404:
                missing += 1
                self.delisted.append({"title_id": tid or "", "book_id": bid, "url": url, "status": 404})
                if cur:
                    cur["status"] = 404
            elif status != 200:
                failed += 1
                self.errors.append({"route": label, "url": url, "status": status})
                if cur:
                    cur["status"] = status
            else:
                pp = page_props(html) or {}
                bi = pp.get("bookInfo")
                rec = book_record(bi) if isinstance(bi, dict) else None
                if rec is None or rec["book_id"] != bid:
                    failed += 1
                    self.errors.append({"route": label, "url": url, "status": "no bookInfo"})
                    continue
                vc = bi.get("viewCount")
                if isinstance(vc, (int, float)) and vc > 0:
                    rec["views_raw"] = int(vc)
                    rec["views"] = views_label(vc)
                m = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', html, re.I)
                canon = unescape(m.group(1)) if m else ""
                mm = re.search(r"/movie/%s/([^/?#\"]+)" % bid, canon)
                if mm:
                    rec["db_slug"] = mm.group(1)
                    rec["url"] = "%s/movie/%s/%s" % (BASE, bid, mm.group(1))
                rec["status"] = 200
                for p in rec["cast"]:
                    if p["id"]:
                        self.performers[p["id"]] = p["name"]
                self.note(rec, "detail")
                ok += 1
            print("%s %4d/%d %s %s" % (label, i + 1, len(targets), status, url[-60:]))
            sys.stdout.flush()
        info = {"targets": len(targets), "ok": ok, "delisted": missing, "failed": failed}
        prev = self.routes.get("detail")
        if prev:
            info = {k: info[k] + prev.get(k, 0) for k in info}
        self.routes["detail"] = info


def rows(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def person_index():
    """lower-cased name or aka -> set of person_ids (aka_names is '|' separated,
    sometimes ';')."""
    idx = {}
    for p in rows("people.csv"):
        for nm in [p.get("name", "")] + re.split(r"[|;]", p.get("aka_names") or ""):
            nm = " ".join(nm.split()).lower()
            if nm:
                idx.setdefault(nm, set()).add(p["person_id"])
    return idx


def earlier_performers(out_path):
    """Performer ids learned by earlier runs, so the cast route does not depend
    on this week's chart happening to include a tracked actor's title."""
    got = {}
    for p in sorted(glob.glob(os.path.join(STAGING, "dramabox_20*.json"))):
        if os.path.abspath(p) == os.path.abspath(out_path) or not re.search(r"dramabox_\d{4}-\d\d-\d\d\.json$", p):
            continue
        try:
            got.update(json.load(io.open(p, encoding="utf-8")).get("performers") or {})
        except (ValueError, OSError):
            continue
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--routes", default="trending,home,channels,known,cast,detail",
                    help="comma list from trending,home,channels,known,cast,detail")
    ap.add_argument("--limit", type=int, default=0,
                    help="cap detail fetches and cast pages (probe runs); 0 = no cap")
    ap.add_argument("--chart-pages-max", type=int, default=8)
    ap.add_argument("--channel-pages-max", type=int, default=6)
    ap.add_argument("--pause", type=float, nargs=2, default=list(PAUSE), metavar=("MIN", "MAX"))
    a = ap.parse_args()
    routes = [r.strip() for r in a.routes.split(",") if r.strip()]
    if min(a.pause) < 1.0:
        print("pause below 1 s is not polite to DramaBox; using 1.0", file=sys.stderr)
        a.pause = [max(1.0, x) for x in a.pause]

    fetch = Fetcher(tuple(a.pause))
    run = Run(fetch)
    started = datetime.datetime.now(datetime.timezone.utc)
    out_path = a.out or os.path.join(STAGING, "dramabox_%s.json" % started.date().isoformat())

    rstatus, rbody = fetch.get(BASE + "/robots.txt", check_robots=False)
    if rstatus == 200:
        fetch.robots = robots_rules(rbody)
    run.routes["robots"] = {"status": rstatus}
    if rstatus == 200 and not fetch.allowed(BASE + "/movie/41000121776"):
        print("robots.txt now disallows /movie/; stopping", file=sys.stderr)
        run.errors.append({"route": "robots", "status": "movie pages disallowed"})
        routes = []

    # A second run on the same day merges into the day's file (the ReelShort
    # scraper's lesson of 24 Aug and 3 Sep): earlier books are the base.
    earlier_runs = []
    if os.path.exists(out_path):
        try:
            prev = json.load(io.open(out_path, encoding="utf-8"))
        except ValueError:
            prev = {}
        for bid, b in (prev.get("books") or {}).items():
            b = dict(b)
            vias = b.pop("seen_via", []) or []
            cur = run.note(b, vias[0] if vias else "earlier", fresh=False)
            for v in vias:
                if v not in cur["seen_via"]:
                    cur["seen_via"].append(v)
        run.delisted = list(prev.get("delisted") or [])
        run.performers.update(prev.get("performers") or {})
        earlier_runs = list(prev.get("runs") or [])
        if prev.get("scraped_at"):
            earlier_runs.append({"scraped_at": prev.get("scraped_at"), "requests": prev.get("requests"),
                                 "routes": prev.get("routes")})
        print("preloaded %d books from %s" % (len(run.books), os.path.basename(out_path)))
    run.performers.update({k: v for k, v in earlier_performers(out_path).items() if k not in run.performers})

    known = {}   # book_id -> (url, title_id) for every DramaBox link we hold
    for r in rows("availability.csv"):
        if r["platform_id"] != "dramabox" or not r.get("direct_link"):
            continue
        m = LINK_RE.search(r["direct_link"])
        if m:
            known.setdefault(m.group(1), (r["direct_link"], r["title_id"]))
    people = person_index()

    if "trending" in routes:
        run.trending(a.chart_pages_max)
    if "home" in routes:
        run.home()
    if "channels" in routes:
        run.channels(a.channel_pages_max)
    if "known" in routes:
        run.known(known)

    def detail_pass(label, want):
        targets = [(bid, known.get(bid, ("", ""))[1]) for bid in sorted(run.books)
                   if bid not in run.detailed and want(run.books[bid])]
        # Chart books first, by position, then the links we hold, then the
        # rest: a --limit probe then samples what matters most.
        targets.sort(key=lambda t: (run.books[t[0]].get("rank") or 999, t[0] not in known, t[0]))
        if a.limit:
            targets = targets[:max(0, a.limit - len(run.detailed))]
        run.detail(targets, label)

    if "detail" in routes:
        detail_pass("detail", lambda b: True)
    if "cast" in routes:
        tracked = {pid: nm for pid, nm in run.performers.items()
                   if len(people.get(" ".join(nm.split()).lower(), ())) == 1}
        run.cast(tracked, a.limit)
        if "detail" in routes:
            detail_pass("detail", lambda b: "cast" in b.get("seen_via", []))

    for bid, b in run.books.items():
        b["known_title_id"] = known.get(bid, ("", ""))[1]

    out = {
        "platform": "dramabox",
        "scraped_at": started.isoformat(timespec="seconds"),
        "finished_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "requests": fetch.requests,
        "routes": run.routes,
        "runs": earlier_runs,
        "performers": dict(sorted(run.performers.items())),
        "books": dict(sorted(run.books.items())),
        "delisted": run.delisted,
        "errors": run.errors,
    }
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    io.open(out_path, "w", encoding="utf-8", newline="\n").write(
        json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n")

    fresh = sum(1 for b in run.books.values() if b["known_title_id"] and b.get("views"))
    new = sum(1 for b in run.books.values() if not b["known_title_id"] and b.get("title"))
    print("\nwrote %s" % out_path)
    print("requests %d | books %d | known refreshed %d | unknown books %d | performers %d | delisted %d | errors %d"
          % (fetch.requests, len(run.books), fresh, new, len(run.performers), len(run.delisted), len(run.errors)))
    print("routes:", json.dumps(run.routes))
    return 0 if run.books else 1


if __name__ == "__main__":
    sys.exit(main())
