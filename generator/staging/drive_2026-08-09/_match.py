"""Match staged filmography credits against titles.csv, the same way
apply_imdb_filmography.py will. Reports the import queue rather than creating
anything - IMDb never says which platform a title is on, and platform is the one
field that cannot be guessed.
"""
import csv, glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
DATA = os.path.join(ROOT, "data")
HERE = os.path.dirname(os.path.abspath(__file__))


def rows(n):
    with open(os.path.join(DATA, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def loose(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def bare(s):
    # strip a leading article BEFORE collapsing, per the traps list
    x = re.sub(r"^(the|a|an)\s+", "", (s or "").lower())
    return re.sub(r"[^a-z0-9]", "", x)


titles = rows("titles.csv")
byl = {loose(t["primary_title"]): t for t in titles}
byb = {}
for t in titles:
    byb.setdefault(bare(t["primary_title"]), t)
have = {(c["title_id"], c["person_id"]) for c in rows("credits.csv")}

tot_m = tot_u = tot_new = 0
queue = {}
for p in sorted(glob.glob(os.path.join(HERE, "actor__*.json"))):
    d = json.load(open(p, encoding="utf-8"))
    pid = d.get("person_id")
    m = u = new = 0
    for c in d.get("credits", []):
        t = byl.get(loose(c["title"])) or byb.get(bare(c["title"]))
        if t:
            m += 1
            if (t["title_id"], pid) not in have:
                new += 1
        else:
            u += 1
            queue.setdefault(c["title"], []).append(d["name"])
    tot_m += m; tot_u += u; tot_new += new
    print(f"{d['name'][:26]:28} credits={m+u:>3}  matched={m:>3}  new_credits={new:>3}  unmatched={u:>3}")

print(f"\nTOTAL matched={tot_m}  new credits available={tot_new}  unmatched={tot_u}"
      f"  ({tot_u*100//max(1,tot_m+tot_u)}% miss)")
print(f"distinct titles NOT in titles.csv: {len(queue)}")
multi = {k: v for k, v in queue.items() if len(v) > 1}
print(f"  of those, credited by MORE THAN ONE actor in this batch: {len(multi)}")
for k, v in sorted(multi.items(), key=lambda x: -len(x[1]))[:15]:
    print(f"    {k[:52]:54} {v}")
