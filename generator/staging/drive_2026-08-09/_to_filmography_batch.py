"""Convert the per-actor staged files into the ONE dict-of-person_id batch that
apply_imdb_filmography.py expects, without touching that audited script.

Two shape differences have to be bridged:
  - the applier iterates `batch.items()` keyed by person_id; we hold one file each
  - the applier unpacks `for title, character, year in rec["credits"]`, so credits
    must be 3-item lists, not the dicts the transcription wrote

AKA IS NOT PASSED THROUGH VERBATIM. The staged AKA_TO_ADD fields are prose notes
("IMDb alternative name 'Aaron Earl Oberst'."), and handing those to the applier
would write a whole sentence into people.csv's aka_names. The clean variants are
extracted here by hand, and only for people whose aka_names is currently BLANK -
the applier is fill-blank-only, so an actor who already holds a variant would be
silently skipped anyway. Those cases are reported instead, for a human ruling.

SOCIALS follow the people.csv convention observed across all 153 populated rows:
"; "-separated, IMDb name URL first. Five of these actors have no socials at all
while we hold their nm id, which the standing rule says to record.
"""
import json, glob, os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "..", "data"))
OUT = os.path.join(HERE, "_filmography_batch.json")

# Extracted by hand from AKA_TO_ADD / imdb_alternative_name. Names only, "|"-separated
# to match the people.csv convention (nick-ritacco: 'Nicholas Ritacco|Nicky Ritacco').
AKA = {
    "aaron-oberst": "Aaron Earl Oberst",
    "jarred-harper": "Jared Harper|Jarod Harper",
    "nick-puya": "Nicholas Puya",
    "tyler-scherer": "Ty Scherer",
    # armand-procacci and jackson-tiller deliberately absent: both already hold a
    # DIFFERENT variant, so this is an append-to-non-blank judgement, not a fill.
}

# Extra profile links beyond the IMDb URL, from the staged `socials` field.
EXTRA_SOCIALS = {
    "jackson-tiller": ["https://linktr.ee/JacksonTiller__",
                       "https://www.instagram.com/jacksontiller__"],
}


def main():
    people = {p["person_id"]: p for p in csv.DictReader(
        open(os.path.join(DATA, "people.csv"), newline="", encoding="utf-8"))}

    batch, notes = {}, []
    for path in sorted(glob.glob(os.path.join(HERE, "actor__*.json"))):
        d = json.load(open(path, encoding="utf-8"))
        pid = d["person_id"]
        person = people.get(pid)
        if not person:
            notes.append(f"  ! {pid} not in people.csv - applier will skip it")
            continue

        rec = {"credits": [[c["title"], c.get("character") or "", c.get("year")]
                           for c in d["credits"]]}

        aka = AKA.get(pid)
        if aka:
            cur = (person.get("aka_names") or "").strip()
            if cur:
                notes.append(f"  ~ {pid}: aka_names already '{cur}', NOT overwriting")
            else:
                rec["aka"] = aka
        elif d.get("AKA_TO_ADD") or d.get("imdb_alternative_name"):
            cur = (person.get("aka_names") or "").strip()
            notes.append(f"  ? {pid}: IMDb variant known but aka_names holds '{cur}' "
                         f"- needs a ruling, left alone")

        if not (person.get("socials") or "").strip():
            urls = [f"https://www.imdb.com/name/{d['nm']}/"] + EXTRA_SOCIALS.get(pid, [])
            rec["socials"] = "; ".join(urls)

        batch[pid] = rec

    json.dump(batch, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(len(r["credits"]) for r in batch.values())
    print(f"wrote {OUT}")
    print(f"  {len(batch)} people, {n} credits")
    print(f"  aka to fill:     {sum(1 for r in batch.values() if 'aka' in r)}")
    print(f"  socials to fill: {sum(1 for r in batch.values() if 'socials' in r)}")
    if notes:
        print("NOTES:")
        for x in notes:
            print(x)


if __name__ == "__main__":
    main()
