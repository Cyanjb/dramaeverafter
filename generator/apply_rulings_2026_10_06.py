#!/usr/bin/env python3
"""Apply Cyan's first duplicate rulings (6 Oct 2026, from the rulings page).

SAME (link the listing to the page we hold, fill-blank only, DramaBox cast
credited where it names exactly one person we hold, otherwise created as
needs_check like the weekly merge): A Deal With My Billionaire Donor, Cheer
Queen Returns to Slay, Come Back for You, Dark Web of Desire, Crush Alert:
Love Request from My Enemy, Emergency Reckoning: Brother's Fury (DramaBox, 28
Sep scrape record), and CEO Queen: A Mother's Revenge (ReelShort link).

DIFFERENT, Cyan: "one is AI and one is human ... both on DramaBox", and she
gave the AI book of each: Cause You Were Never Mine (42000012972) and
Divorced at the Wedding Day (42000013146). Our pages held the HUMAN cast and
story but linked the AI book. So each page is re-pointed at its human book
(41000110709, 41000116643) and each AI book gets its own page, ai=yes.

Usage: python3 generator/apply_rulings_2026_10_06.py [--apply]
"""
import difflib, json, os, re, sys, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from merge_scrape import load, save

TODAY = "2026-10-06"
SRC = "rulings_2026-10-06"
DB = json.load(open(os.path.join(HERE, "staging", "dramabox_2026-09-28.json"), encoding="utf-8"))
BOOKS = {str(b["book_id"]): b for b in (DB["books"].values() if isinstance(DB["books"], dict) else DB["books"])}
SAME_DB = {"a-deal-with-my-billionaire-donor": "41000122689", "cheer-queen-returns-to-slay": "41000122781",
           "come-back-for-you": "41000110859", "dark-web-of-desire": "41000100700",
           "crush-alert-love-request-from-my-enemy": "42000008972",
           "emergency-reckoning-brother-s-fury": "41000123062"}
SAME_RS = {"ceo-queen-a-mother-s-revenge":
           "https://www.reelshort.com/movie/ceo-queen-a-mother-s-revenge-6825af4b1657d2354b0d8094"}
SPLIT = [("cause-you-were-never-mine", "41000110709", "42000012972", "cause-you-were-never-mine-ai"),
         ("divorced-at-the-wedding-day", "41000116643", "42000013146", "divorced-at-the-wedding-day-ai")]
JUNK = re.compile(r"^(?:Biography\s+)?(?:IMDbPro\s+)?", re.I)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main(apply):
    T, tf = load("titles.csv"); A, af = load("availability.csv"); S, sf = load("snapshots.csv")
    C, cf = load("credits.csv"); P, pf = load("people.csv")
    by = {t["title_id"]: t for t in T}
    names = {}
    for p in P:
        for n in [p["name"]] + re.split(r"[|;]", p.get("aka_names") or ""):
            if n.strip():
                names.setdefault(norm(n), set()).add(p["person_id"])
    pids = {p["person_id"] for p in P}
    held = {(c["title_id"], c["person_id"]) for c in C}
    log = []

    def url(bid):
        b = BOOKS[bid]
        return b.get("url") or "https://www.dramaboxdb.com/movie/%s" % bid

    def fill(t, bid):
        b = BOOKS[bid]
        for col, val in (("episode_count", b.get("episodes")), ("poster_ref", b.get("poster")), ("year", b.get("year"))):
            if val and not t.get(col):
                t[col] = str(val)

    def credit(tid, bid):
        for c in BOOKS[bid].get("cast") or []:
            name = JUNK.sub("", c["name"]).strip()
            ids = names.get(norm(name), set())
            if len(ids) == 1:
                pid = next(iter(ids))
            elif ids:
                continue
            else:
                close = difflib.get_close_matches(norm(name), list(names), n=1, cutoff=0.9)
                if close:
                    log.append("HELD close name %r ~ %s on %s" % (name, sorted(names[close[0]]), tid)); continue
                pid = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower())).strip("-")
                if pid in pids:
                    continue
                P.append({k: "" for k in pf} | {"person_id": pid, "slug": pid, "name": name, "role_type": "actor",
                                                 "data_confidence": "needs_check", "source": "dramabox_cast_%s" % TODAY})
                pids.add(pid); names[norm(name)] = {pid}; log.append("new person %s" % pid)
            if (tid, pid) not in held:
                C.append({k: "" for k in cf} | {"title_id": tid, "person_id": pid, "role": "actor"})
                held.add((tid, pid)); log.append("credit %s -> %s" % (pid, tid))

    def avail_row(tid, platform, link, title, views):
        A.append({k: "" for k in af} | {"title_id": tid, "platform_id": platform, "title_as_listed_on_platform": title,
                                         "direct_link": link, "view_count": views or "", "view_count_date": "2026-09-28" if views else "",
                                         "last_checked": TODAY})
        if views:
            S.append({k: "" for k in sf} | {"title_id": tid, "platform_id": platform, "view_count": views, "date": "2026-09-28"})

    for tid, bid in SAME_DB.items():
        t = by[tid]; b = BOOKS[bid]
        if any(r["title_id"] == tid and bid in (r["direct_link"] or "") for r in A):
            log.append("already linked %s" % tid); continue
        avail_row(tid, "dramabox", url(bid), b.get("title"), b.get("views"))
        fill(t, bid); credit(tid, bid); log.append("linked %s -> DramaBox %s" % (tid, bid))
    for tid, link in SAME_RS.items():
        if not any(r["title_id"] == tid and r["platform_id"] == "reelshort" for r in A):
            avail_row(tid, "reelshort", link, by[tid]["primary_title"], ""); log.append("linked %s -> ReelShort" % tid)

    for tid, human, ai, ai_tid in SPLIT:
        t = by[tid]
        for r in A:
            if r["title_id"] == tid and ai in (r["direct_link"] or ""):
                b = BOOKS[human]
                r["direct_link"] = url(human); r["view_count"] = b.get("views") or ""; r["view_count_date"] = "2026-09-28"
                r["last_checked"] = TODAY
        if t.get("poster_ref") and ai in t["poster_ref"]:
            t["poster_ref"] = BOOKS[human].get("poster") or ""
        t["episode_count"] = str(BOOKS[human].get("episodes") or t["episode_count"])
        if BOOKS[human].get("views"):
            S.append({k: "" for k in sf} | {"title_id": tid, "platform_id": "dramabox", "view_count": BOOKS[human]["views"], "date": "2026-09-28"})
        credit(tid, human)
        if ai_tid not in by:
            b = BOOKS[ai]
            new = {k: "" for k in tf} | {"title_id": ai_tid, "slug": ai_tid, "primary_title": t["primary_title"],
                   "episode_count": str(b.get("episodes") or ""), "poster_ref": b.get("poster") or "", "year": str(b.get("year") or ""),
                   "source_urls": url(ai), "last_verified": TODAY, "data_confidence": "needs_check", "source": SRC,
                   "origin": "english", "ai": "yes", "tropes": t.get("tropes", "")}
            T.append(new); by[ai_tid] = new
            avail_row(ai_tid, "dramabox", url(ai), b.get("title"), b.get("views"))
        log.append("split %s: page -> human %s; AI %s -> %s" % (tid, human, ai, ai_tid))

    print("\n".join(log))
    if apply:
        for n, f, r in (("titles.csv", tf, T), ("availability.csv", af, A), ("snapshots.csv", sf, S),
                        ("credits.csv", cf, C), ("people.csv", pf, P)):
            save(n, f, r)
        print("applied")


if __name__ == "__main__":
    main("--apply" in sys.argv)
