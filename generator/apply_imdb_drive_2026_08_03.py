"""Write the Drive-batch cast, IMDb links and book credit into the CSVs.

Follows the same safety rules as apply_imdb_pdf_cast.py: exact name match reuses the
person, near-match goes to match_queue UNCREDITED, new people are needs_check,
character names are fill-blank-only.

TWO THINGS THIS ONE ADDS, both because the Drive PDFs carry IMDb's link list:

1. IMDb LINKS. An nm id here is IMDb tying a named person to a title we already hold,
   which is the standard this project set for a socials link on 1 August. It is added
   only when the person has no imdb.com link already, and never overwrites.

2. A BOOK CREDIT, fill-blank-only, never overwriting a value Cyan supplied.

Nothing is marked lead: IMDb's cast order is not billing order.
"""
import csv, io, os, re, sys, difflib, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
SOURCE = "imdb_drive_2026-08-03"

spec = importlib.util.spec_from_file_location("drive", os.path.join(HERE, "imdb_drive_batch_2026_08_03.py"))
drive = importlib.util.module_from_spec(spec); spec.loader.exec_module(drive)

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def loose(s): return re.sub(r"[^a-z0-9]", "", s.lower())
def norm(s):
    s = s.lower().replace("’", "'").replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "", s)
def term_of(p):
    raw = open(p, "rb").read(); c = raw.count(b"\r\n")
    return "\r\n" if c > raw.count(b"\n") - c else "\n"
def load(n): return list(csv.DictReader(open(os.path.join(DATA, n), newline="", encoding="utf-8")))
def save(n, fields, recs):
    p = os.path.join(DATA, n); buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator=term_of(p))
    w.writeheader(); w.writerows(recs)
    open(p, "w", newline="", encoding="utf-8").write(buf.getvalue())

titles, people, credits, queue = load("titles.csv"), load("people.csv"), load("credits.csv"), load("match_queue.csv")
by_norm, ambiguous = {}, set()
for t in titles:
    k = norm(t["primary_title"])
    if k in by_norm: ambiguous.add(k)
    by_norm[k] = t
by_name = {p["name"].strip().lower(): p for p in people}
by_loose = {}
for p in people: by_loose.setdefault(loose(p["name"]), p)
cred_idx = {(c["title_id"], c["person_id"]): c for c in credits}
queued = {(q["candidate_a"], q["candidate_b"]) for q in queue}
existing_ids = {p["person_id"] for p in people}

new_credits, new_people, to_queue, filled_chars, linked, booked = [], [], [], [], [], []
matched = created = 0

for title_name, (tt, cast) in drive.CAST.items():
    k = norm(title_name)
    if k in ambiguous:
        print(f"AMBIGUOUS, skipped: {title_name}"); continue
    t = by_norm.get(k)
    if not t:
        print(f"NOT IN titles.csv, skipped: {title_name}"); continue
    tid = t["title_id"]
    for actor, character, nm in cast:
        key = actor.strip().lower()
        person = by_name.get(key)
        if person is None:
            near = by_loose.get(loose(actor))
            if near is None:
                close = difflib.get_close_matches(loose(actor), by_loose.keys(), n=1, cutoff=0.90)
                if close: near = by_loose[close[0]]
            if near is None:
                aw = actor.split()
                if len(aw) >= 2:
                    a_key = (aw[0].lower(), aw[-1].lower())
                    for cand in people + new_people:
                        cw = cand["name"].split()
                        if len(cw) >= 2 and (cw[0].lower(), cw[-1].lower()) == a_key:
                            near = cand; break
            if near is not None and near["name"].strip().lower() != key:
                pair = (near["person_id"], slug(actor))
                if pair not in queued:
                    queued.add(pair)
                    to_queue.append({"candidate_a": near["person_id"], "candidate_b": slug(actor),
                                     "evidence": f"IMDb {tt} ('{title_name}') credits '{actor}' ({nm}); "
                                                 f"people.csv has '{near['name']}'. Not merged pending a "
                                                 f"ruling. Source: {SOURCE}.",
                                     "status": "pending"})
                ex = cred_idx.get((tid, near["person_id"]))
                if ex is not None and not (ex.get("character_name") or "").strip() and character:
                    ex["character_name"] = character
                    filled_chars.append(f"{t['primary_title']}: {near['name']} -> {character}")
                continue
            pid = slug(actor)
            if pid in existing_ids: continue
            existing_ids.add(pid)
            person = {"person_id": pid, "slug": pid, "name": actor, "aka_names": "", "role_type": "actor",
                      "socials": f"https://www.imdb.com/name/{nm}/", "bio_short": "", "photo_ref": "",
                      "data_confidence": "needs_check", "source": SOURCE}
            new_people.append(person); by_name[key] = person
            by_loose.setdefault(loose(actor), person); created += 1
            linked.append(f"{actor} -> {nm} (new person)")
        else:
            matched += 1
            # IMDb itself ties this nm to a title we hold, which is the evidence bar
            # the 1 August socials pass set. Add only if absent; never overwrite.
            if "imdb.com" not in person["socials"]:
                person["socials"] = (f"https://www.imdb.com/name/{nm}/"
                                     + ("; " + person["socials"] if person["socials"].strip() else ""))
                linked.append(f"{person['name']} -> {nm}")

        ex = cred_idx.get((tid, person["person_id"]))
        if ex is not None:
            if character and not (ex.get("character_name") or "").strip():
                ex["character_name"] = character
                filled_chars.append(f"{t['primary_title']}: {person['name']} -> {character}")
            continue
        rec = {"title_id": tid, "person_id": person["person_id"], "role": "actor",
               "character_name": character}
        cred_idx[(tid, person["person_id"])] = rec
        new_credits.append(rec)

for title_name, author in drive.BOOK.items():
    t = by_norm.get(norm(title_name))
    if t and not (t.get("book") or "").strip():
        t["book"] = author
        booked.append(f"{t['primary_title']} -> {author}")

print(f"new credits: {len(new_credits)}  (people matched {matched}, created {created})")
print(f"IMDb links added: {len(linked)}")
for l in linked: print("   ", l)
print(f"character names filled: {len(filled_chars)}")
print(f"book credits filled: {len(booked)}  {booked}")
print(f"queued uncredited: {len(to_queue)}")

if "--dry-run" in sys.argv:
    for c in new_credits: print("   +", c["title_id"], c["person_id"], c["character_name"])
    print("(dry run, nothing written)"); raise SystemExit

if new_people or linked: save("people.csv", list(people[0].keys()), people + new_people)
if new_credits or filled_chars: save("credits.csv", list(credits[0].keys()), credits + new_credits)
if to_queue: save("match_queue.csv", list(queue[0].keys()), queue + to_queue)
if booked: save("titles.csv", list(titles[0].keys()), titles)
print(f"\nwrote {len(new_credits)} credits, {len(new_people)} people, {len(linked)} IMDb links, "
      f"{len(booked)} book credits, {len(to_queue)} queued")
