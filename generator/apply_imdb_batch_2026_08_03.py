"""Apply the 2026-08-03 IMDb PDF batch to the CSVs.

Source data lives in imdb_pdf_batch_2026_08_03.py, which holds the cast exactly as
IMDb printed it: 11 actor filmographies and 5 title cast lists. This script is the
writer; that one is the record.

Same safety rules as apply_imdb_pdf_cast.py, which this follows deliberately:
exact name match reuses the person, near-match goes to match_queue UNCREDITED,
new people are needs_check, character names are fill-blank-only and never overwrite.

TWO RULES SPECIFIC TO THIS BATCH:

1. NOTHING IN THIS BATCH IS MARKED "lead". apply_imdb_pdf_cast.py treats the first two
   names on a cast page as leads, and that assumption does not survive these pages: on
   "Found A Homeless Genius to Save My Company" IMDb's top-cast order puts Audrey and
   "Reporter #1" first and the protagonist Ethan Dalton third. A character literally
   named Reporter #1 is not a lead, so the order is not billing order and cannot be
   read as one. A filmography says even less, carrying no ordering at all. Every credit
   here is role="actor"; upgrade one to lead only from something that actually says so.

2. TITLES MATCH ON A NORMALISED KEY, because IMDb and our CSV disagree on case and
   punctuation ("Emily in Her Glow-up Era after Ex's Out" vs "...Glow-Up Era After...").
   A normalised key that maps to more than one title is skipped rather than guessed.

Titles IMDb credits point at that are NOT in titles.csv are skipped and listed. Do not
bulk-add them: IMDb does not state which app a title is on, which is what blocked
"The Cost of Touch". Non-vertical work in the filmographies (Reed's Point, Dhar Mann,
music videos, a video game) is skipped by the same mechanism, since we hold no such titles.
"""
import csv, io, os, re, sys, difflib, time, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.environ.get("DEA_DATA") or os.path.join(os.path.dirname(HERE), "data")
SOURCE = "imdb_pdf_2026-08-03"

spec = importlib.util.spec_from_file_location(
    "batch", os.path.join(HERE, "imdb_pdf_batch_2026_08_03.py"))
batch = importlib.util.module_from_spec(spec)
sys.stdout = io.StringIO()          # the record module prints its own audit on import
spec.loader.exec_module(batch)
sys.stdout = sys.__stdout__

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

# IMDb spelling -> the people.csv spelling, only where the identity is evidenced.
# Artem Plonder's own IMDb page bills a 2022 credit "as Artyom Plyonder" and 12 of his
# titles match our credits exactly, so this is IMDb's own assertion, not a name guess.
OURS = batch.OURS

# One work list, so both directions go through identical checks.
# (title_name, actor, character, billed, provenance)  billed=True only from a cast page.
work = []
for actor, rows in batch.ACTORS.items():
    for title_name, character in rows:
        work.append((title_name, OURS.get(actor, actor), character, None, f"{actor} filmography"))
for title_name, rows in batch.TITLES.items():
    for order, (actor, character) in enumerate(rows):
        work.append((title_name, OURS.get(actor, actor), character, order, f"{title_name} cast page"))

new_credits, new_people, to_queue, filled_chars, skipped = [], [], [], [], []
matched = created = 0
seen = set()

for title_name, actor, character, billed, prov in work:
    k = norm(title_name)
    if k in ambiguous:
        skipped.append((title_name, actor, "ambiguous title key")); continue
    t = by_norm.get(k)
    if not t:
        skipped.append((title_name, actor, "not in titles.csv")); continue
    tid = t["title_id"]
    if (tid, loose(actor)) in seen: continue      # same person reached twice, two routes
    seen.add((tid, loose(actor)))

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
                                 "evidence": f"IMDb page for '{title_name}' credits '{actor}'; people.csv has "
                                             f"'{near['name']}'. Not merged pending a ruling. "
                                             f"Source: {SOURCE}, {prov}.",
                                 "status": "pending"})
            ex = cred_idx.get((tid, near["person_id"]))
            if ex is not None and not (ex.get("character_name") or "").strip() and character:
                ex["character_name"] = character
                filled_chars.append(f"{t['primary_title']}: {near['name']} -> {character}")
            continue
        pid = slug(actor)
        if pid in existing_ids:
            skipped.append((title_name, actor, "slug collision")); continue
        existing_ids.add(pid)
        person = {"person_id": pid, "slug": pid, "name": actor, "aka_names": "", "role_type": "actor",
                  "socials": "", "bio_short": "", "photo_ref": "",
                  "data_confidence": "needs_check", "source": SOURCE}
        new_people.append(person); by_name[key] = person
        by_loose.setdefault(loose(actor), person); created += 1
    else:
        matched += 1

    ex = cred_idx.get((tid, person["person_id"]))
    if ex is not None:
        if character and not (ex.get("character_name") or "").strip():
            ex["character_name"] = character
            filled_chars.append(f"{t['primary_title']}: {person['name']} -> {character}")
        continue
    rec = {"title_id": tid, "person_id": person["person_id"],
           "role": "actor", "character_name": character}
    cred_idx[(tid, person["person_id"])] = rec
    new_credits.append(rec)

print(f"new credits: {len(new_credits)}  (people matched {matched}, created {created})")
print(f"character names filled on existing credits: {len(filled_chars)}")
print(f"near-duplicates queued uncredited: {len(to_queue)}")
for q in to_queue: print("   ", q["evidence"][:140])
print(f"skipped: {len(skipped)}  ({len({s[0] for s in skipped})} distinct titles not in titles.csv)")

if "--dry-run" in sys.argv:
    for c in new_credits[:200]:
        print("   +", c["title_id"], c["person_id"], c["role"], c["character_name"])
    print("(dry run, nothing written)"); raise SystemExit

if new_people: save("people.csv", list(people[0].keys()), people + new_people)
if new_credits or filled_chars: save("credits.csv", list(credits[0].keys()), credits + new_credits)
if to_queue: save("match_queue.csv", list(queue[0].keys()), queue + to_queue)
print(f"\nwrote {len(new_credits)} credits, {len(new_people)} people, "
      f"{len(to_queue)} queued, {len(filled_chars)} character names filled")
