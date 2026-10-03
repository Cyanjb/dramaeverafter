#!/usr/bin/env python3
"""Replace GoodShort's tag soup with GoodShort's own per-show labels.

    python3 generator/goodshort_tropes.py fetch            read each live GoodShort page's labels (resumable)
    python3 generator/goodshort_tropes.py apply            dry run: what the tropes would become
    python3 generator/goodshort_tropes.py apply --apply
    python3 generator/goodshort_tropes.py apply-reviewed <folder> [--apply]
        the reading pass (25 Sep 2026): result_*.json files, title_id -> tropes,
        from reviewers who read each show's title and synopsis against its tags.
        This is what was applied; the keyword `apply` is the fallback and the
        evidence helper (ADDABLE, SYNONYMS) the reviewers were given as hints.

Born 24 Sep 2026. GoodShort titles averaged 17 tropes each (every other app 1-6):
the July scrape took GoodShort's search-tag cloud, and the 14 Aug frequency cut
only halved it (TROPE-CLEANUP-PROPOSAL.md, decision 2). Wrong tropes leaked onto
browse pages - blood-and-bones sat on /tropes/vampire with no vampire in it.
GoodShort's show page carries a separate, short "labels" list (usually 2-5) that
is the platform describing that show: A Dazzling Beauty is "True Love, Revenge".
Those labels, matched to our trope vocabulary, replace the soup.

Only GoodShort-sourced titles are touched, and only when the page gave labels.
Labels with no trope in our vocabulary are skipped, never invented as tropes.
The record, generator/staging/goodshort_labels.json, keeps every page's labels.
"""
import csv, io, json, os, re, sys, time, urllib.request
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RECORD = os.path.join(HERE, "staging", "goodshort_labels.json")
ORIGIN = os.path.join(HERE, "staging", "goodshort_origin.json")
# GoodShort's own synopses, read as trope evidence only. Kept OUT of the repo (the
# repo is public and platform text must not be republished): a temp file by default.
INTRO_CACHE = os.environ.get("GOODSHORT_INTRO_CACHE",
                             os.path.join(os.environ.get("TEMP", "/tmp"), "goodshort_intros.json"))


def load(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r), list(r.fieldnames)


def save(n, fields, recs):
    p = os.path.join(DATA, n)
    raw = open(p, "rb").read()
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") - raw.count(b"\r\n") else "\n"
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=nl)
    w.writeheader(); w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())


def page_facts(url):
    """(labels, intro) from the book's own record. Most GoodShort books carry no
    labels at all (measured 25 Sep 2026: ~80%), so the introduction is read too,
    as EVIDENCE for which tropes the show really has. It is never stored in the
    repo: only the trope names it supports are (platform text stays off GitHub)."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    s = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    bid = re.search(r"-(\d{8,})/?$", url).group(1)
    i = s.find(f'"bookId":"{bid}"')
    if i < 0:
        return None, ""
    rec = s[i:i + 6000]
    m = re.search(r'"labels":\[([^\]]*)\]', rec)
    intro = re.search(r'"introduction":"((?:[^"\\]|\\.)*)"', rec)
    return (re.findall(r'"([^"]+)"', m.group(1)) if m else []), (intro.group(1) if intro else "")


# Keyword evidence per trope. A trope is kept only when GoodShort labelled the
# show with it, or the show's own title or introduction supports it. A trope with
# no entry here needs its own name in the text. Tuned 25 Sep 2026 on the 45
# commonest GoodShort tropes; deliberately tight, since loose evidence is how
# the soup would come straight back ("sweet", "young", "mutual love",
# "dynamic duo" and "group favorite" have no entry and so rarely survive).
SYNONYMS = {
    "toxic love": r"toxic|obsess|possessive|abus",
    "reborn": r"reborn|rebirth|second life|another chance at life|given a second chance|back to the day|regress|woke up \w* ?(years|back)",
    "rebirth": r"reborn|rebirth|second life",
    "cute kids": r"\b(son|daughter|kid|kids|child|children|twins|triplets|toddler|little (boy|girl))\b",
    "little cupids": r"matchmak|(son|daughter|kid|twins|triplets)\b.{0,80}\b(set up|find|daddy|mommy|father|mother)\b",
    "misunderstanding": r"misunderst",
    "misidentification": r"mistak(en|es) (for|as|her|him)|mistaken identity|wrong (man|woman|person|bride|groom|room)",
    "contract marriage": r"contract", "flash marriage": r"flash marri|married on the spot|marr(y|ies|ied) a (complete )?stranger",
    "love after marriage": r"(flash|contract|arranged|forced|sham|fake|convenient) marri|marr(y|ies|ied) a (complete )?stranger",
    "cinderella": r"cinderella|poor girl|\bmaid\b|servant|orphan|penniless",
    "billionaire": r"billionair|trillionair|tycoon|richest", "ceo": r"\bceo\b|chairman|tycoon|president of",
    "love triangle": r"love triangle|torn between|between (her|his) (ex|fianc)",
    "hate love": r"\bhate|hatred|enem(y|ies)|rival", "hate": r"\bhate|hatred",
    "enemies to lovers": r"enem(y|ies)|rival|\bhate",
    "redemption": r"redempt|atone|make amends|win (her|him) back|regret",
    "pregnancy": r"pregnan|expecting|with child|baby bump", "secret baby": r"pregnan|secret (baby|child|son|daughter)|hid(den|ing)? (her|his) (child|son|daughter|twins)",
    "cheating": r"cheat|affair|mistress|slept with", "affair": r"affair|mistress",
    "vampire": r"vampir", "werewolf": r"werewol|\bwolf\b|wolves|lycan|\bpack\b", "alpha": r"\balpha", "luna": r"\bluna\b",
    "second chance": r"second chance|years later|reunit|win (her|him) back|ex-(husband|wife|boyfriend|girlfriend)",
    "forbidden love": r"forbidden|taboo|step-?(brother|sister|father|son)|best friend's (dad|father|brother)",
    "dark romance": r"dark romance|obsess|captive|kidnap|possessive",
    "royal": r"royal|prince|princess|\bking\b|\bqueen\b|emperor|empress|palace|throne",
    "one night stand": r"one[- ]night|drunken night|night with a stranger",
    "heir": r"\bheir\b|heiress|inherit", "heiress": r"heiress",
    "campus": r"campus|college|universit|high school|\bschool\b",
    "crush to love": r"\bcrush", "puppy love": r"puppy love|childhood sweetheart|first love",
    "time travel": r"time travel|travel(l)?ed (back|through time)|transmigrat|back in time|another era",
    "transmigration": r"transmigrat",
    "memory loss": r"amnesi|memory|memories|forg(e|o)t",
    "office romance": r"office|secretary|assistant|\bboss\b|colleague",
    "substitute bride": r"substitute|in (her|his) (sister's )?place|stand[- ]in bride|instead of (her|his) sister",
    "stand in": r"stand[- ]in|substitute|replacement|in (her|his) place|pretend(s|ed)? to be",
    "family reunion": r"reunit|long-lost|lost (daughter|son)|biological|real (daughter|parents|family)|switched at birth",
    "system": r"\bsystem\b", "apocalypse": r"apocalyp|zombie|end of the world", "zombie": r"zombie",
    "housewife": r"housewife|stay-at-home|homemaker",
    "god of war": r"god of war|war god|warlord|\bgeneral\b",
    "age gap": r"years (older|younger)|age gap|\buncle\b|father's (friend|best friend)|much older",
    "business": r"business|company|corporat|empire",
    "mafia": r"mafia|mob boss|gangster|cartel", "revenge": r"reveng|aveng|payback|make them pay",
    "hidden identity": r"hidden identity|secret identity|disguis|true identity|conceal", "secret identity": r"hidden identity|secret identity|disguis|true identity|conceal",
    "divorce": r"divorc", "betrayal": r"betray",
    "martial arts": r"martial|kung fu", "cultivation": r"cultivat|immortal", "dragon": r"dragon",
    "bodyguard": r"bodyguard", "doctor": r"doctor|surgeon|physician|healer|medic",
    "underdog rise": r"underdog|looked down|humiliat|mocked|despised|nobody",
    "counterattack": r"fight back|strikes? back|turn(s|ed)? the tables|counterattack|take back",
}


# Tropes whose keywords are unambiguous enough to ADD when the text names them,
# even if the July tags missed them (a zombie apocalypse show tagged without
# "apocalypse"). Everything else is only ever kept, never added, on evidence.
ADDABLE = ["apocalypse", "zombie", "vampire", "werewolf", "system", "time travel", "transmigration", "ceo",
           "billionaire", "mafia", "revenge", "divorce", "pregnancy", "one night stand", "contract marriage",
           "flash marriage", "secret identity"]
# GoodShort label -> our vocabulary, where the names differ (the 15 Aug cleanup
# folded hidden identity into secret identity).
LABEL_ALIAS = {"hiddenidentity": "secret identity", "familystory": "family bonds"}


def evidenced(trope, text):
    t = trope.lower()
    rx = SYNONYMS.get(t) or r"\b" + r"\s*".join(re.escape(w) for w in re.split(r"[\s-]+", t)) + r"s?\b"
    return re.search(rx, text, re.I) is not None


def fetch():
    origin = json.load(open(ORIGIN, encoding="utf-8")) if os.path.exists(ORIGIN) else {}
    rec = json.load(open(RECORD, encoding="utf-8")) if os.path.exists(RECORD) else {}
    avail, _ = load("availability.csv")
    titles, _ = load("titles.csv")
    live = {t["title_id"] for t in titles if (t.get("status") or "").lower() != "delisted"}
    todo = {}
    for a in avail:
        link = (a.get("direct_link") or "").strip()
        if a["platform_id"] != "goodshort" or not link or a["title_id"] in rec or a["title_id"] not in live:
            continue
        if a["title_id"] not in todo or not (a.get("version") or ""):
            todo[a["title_id"]] = link
    cache = json.load(open(INTRO_CACHE, encoding="utf-8")) if os.path.exists(INTRO_CACHE) else {}
    todo = {k: v for k, v in todo.items() if k not in cache or k not in rec}
    print(f"{len(rec)} recorded, {len(todo)} to fetch; introductions cached outside the repo at {INTRO_CACHE}")
    for n, (tid, link) in enumerate(sorted(todo.items()), 1):
        try:
            lab, intro = page_facts(link)
        except Exception as e:
            lab, intro = f"ERROR {type(e).__name__}", ""
        rec[tid] = {"url": link, "labels": lab, "fetched": time.strftime("%Y-%m-%d")}
        cache[tid] = intro
        if n % 50 == 0 or n == len(todo):
            json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True, ensure_ascii=False)
            json.dump(cache, open(INTRO_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
            print(f"  {n}/{len(todo)}", flush=True)
        time.sleep(1.0)
    json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True, ensure_ascii=False)
    json.dump(cache, open(INTRO_CACHE, "w", encoding="utf-8"), ensure_ascii=False)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def apply(write):
    rec = json.load(open(RECORD, encoding="utf-8"))
    titles, tf = load("titles.csv")
    vocab_rows, vf = load("tropes.csv")
    vocab = {}
    for v in vocab_rows:
        for k in (v.get("name"), v.get("slug")):
            if k: vocab.setdefault(norm(k), v["name"])
    cache = json.load(open(INTRO_CACHE, encoding="utf-8")) if os.path.exists(INTRO_CACHE) else {}
    unmatched, dropped, kept_n = Counter(), Counter(), Counter()
    before, after, changed, emptied, no_intro = [], [], 0, 0, 0
    for t in titles:
        r = rec.get(t["title_id"])
        if not r or not isinstance(r["labels"], list) or not (t.get("source") or "").startswith("goodshort"):
            continue
        if t["title_id"] not in cache:
            no_intro += 1
            continue   # no evidence read for this one; leave it as it is
        text = (t.get("primary_title") or "") + " " + (t.get("alt_titles") or "") + " " + cache[t["title_id"]]
        old = [x.strip() for x in (t.get("tropes") or "").split(";") if x.strip()]
        labelled = []
        for lab in r["labels"]:
            name = vocab.get(norm(lab)) or vocab.get(norm(LABEL_ALIAS.get(norm(lab), "")))
            if name and name not in labelled: labelled.append(name)
            elif not name: unmatched[lab] += 1
        new = [x for x in old if x in labelled or evidenced(x, text)]
        new += [x for x in labelled if x not in new]
        new += [vocab[norm(x)] for x in ADDABLE if norm(x) in vocab and vocab[norm(x)] not in new
                and evidenced(x, text)]
        for x in old:
            (kept_n if x in new else dropped)[x] += 1
        r["tropes_kept"] = new          # the record says what survived and why it could
        before.append(len(old)); after.append(len(new))
        if not new: emptied += 1
        if new != old:
            t["tropes"] = ";".join(new); changed += 1
    avg = lambda xs: sum(xs) / len(xs) if xs else 0
    print(f"GoodShort titles read: {len(before)}  changed: {changed}  left with no trope: {emptied}  skipped (no introduction read): {no_intro}")
    print(f"tropes per title: {avg(before):.1f} -> {avg(after):.1f}  (max {max(after, default=0)}); "
          f"titles with 15+: {sum(1 for x in before if x >= 15)} -> {sum(1 for x in after if x >= 15)}")
    print("most dropped:", dropped.most_common(12))
    print("most kept:   ", kept_n.most_common(12))
    print("labels with no trope in the vocabulary (skipped):", unmatched.most_common(15))
    if write:
        tcount = Counter()
        for t in titles:
            for x in {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}:
                tcount[x] += 1
        for v in vocab_rows:
            v["title_count"] = str(tcount.get((v.get("name") or "").lower(), 0))
        save("titles.csv", tf, titles); save("tropes.csv", vf, vocab_rows)
        json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True, ensure_ascii=False)
        print("written")
    else:
        print("[dry run] nothing written")


def apply_reviewed(folder, write):
    """Apply a reading pass: result_*.json files mapping title_id -> trope list,
    written by reviewers who read each show's title and synopsis against its
    tags (Cyan, 25 Sep 2026: "the ones that should apply should be there, but if
    it doesn't apply then it shouldn't", e.g. no high fantasy on a modern-day
    billionaire drama). Names outside the vocabulary are rejected, not created."""
    import glob
    rec = json.load(open(RECORD, encoding="utf-8"))
    titles, tf = load("titles.csv")
    vocab_rows, vf = load("tropes.csv")
    vocab = {norm(v["name"]): v["name"] for v in vocab_rows}
    reviewed, bad = {}, Counter()
    for f in sorted(glob.glob(os.path.join(folder, "result_*.json"))):
        for tid, lst in json.load(open(f, encoding="utf-8")).items():
            out = []
            for x in lst:
                name = vocab.get(norm(x))
                if name and name not in out: out.append(name)
                elif not name: bad[x] += 1
            reviewed[tid] = out
    before, after, changed = [], [], 0
    for t in titles:
        if t["title_id"] not in reviewed: continue
        old = [x for x in (t.get("tropes") or "").split(";") if x.strip()]
        new = reviewed[t["title_id"]]
        before.append(len(old)); after.append(len(new))
        rec.setdefault(t["title_id"], {})["tropes_kept"] = new
        if new != old:
            t["tropes"] = ";".join(new); changed += 1
    avg = lambda xs: sum(xs) / len(xs) if xs else 0
    print(f"reviewed: {len(reviewed)}  applied to titles: {len(before)}  changed: {changed}")
    print(f"tropes per title: {avg(before):.1f} -> {avg(after):.1f}  (max {max(after, default=0)}); "
          f"none: {sum(1 for x in after if not x)}; 15+: {sum(1 for x in before if x >= 15)} -> {sum(1 for x in after if x >= 15)}")
    print("rejected names (not in vocabulary):", bad.most_common(10))
    if write:
        tcount = Counter()
        for t in titles:
            for x in {x.strip().lower() for x in (t.get("tropes") or "").split(";") if x.strip()}:
                tcount[x] += 1
        for v in vocab_rows:
            v["title_count"] = str(tcount.get((v.get("name") or "").lower(), 0))
        save("titles.csv", tf, titles); save("tropes.csv", vf, vocab_rows)
        json.dump(rec, open(RECORD, "w", encoding="utf-8"), indent=1, sort_keys=True, ensure_ascii=False)
        print("written")
    else:
        print("[dry run] nothing written")


if __name__ == "__main__":
    if sys.argv[1:2] == ["fetch"]: fetch()
    elif sys.argv[1:2] == ["apply"]: apply("--apply" in sys.argv)
    elif sys.argv[1:2] == ["apply-reviewed"] and len(sys.argv) > 2: apply_reviewed(sys.argv[2], "--apply" in sys.argv)
    else: sys.exit(__doc__)
