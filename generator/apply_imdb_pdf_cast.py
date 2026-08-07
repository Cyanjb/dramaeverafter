"""Apply cast from a manually-saved IMDb PDF.

Cyan navigates to the IMDb page herself and saves it, which removes the single
biggest weakness of the search-based route: ambiguity. A search for "Broken" or
"My Girl" can land on the wrong production; a page she opened cannot.

The PDF also carries the FULL top-cast list with character names, where search
snippets typically surface only three or four names and no characters.

Same safety rules as every other pass: exact match reuses the person, near-match
goes to match_queue uncredited, new people are needs_check, character names are
fill-blank-only (never overwrite an existing value).
"""
import csv, io, os, re, sys, difflib, time

DATA = os.environ["DEA_DATA"]
SOURCE = "imdb_pdf_" + time.strftime("%Y-%m-%d")

# title in titles.csv -> [(actor, character), ...]  exactly as printed on the IMDb page
CAST = {
    "Cursed Temptation": [
        ("Francisco DeCun", "Damian"),
        ("Megan Suzanne Beattie", "Laura"),
        ("Logan Hunt", "Cerulean"),
        ("Kellen Shaffer", "Glen"),
        ("Paulina Rezende", "Melody"),
        ("Xander Bailey", "Lucifer"),
    ],
    "The Perfect Spiral": [
        ("Victoria Andrunik", "Alex Thompson"),
        ("Jared Staub", "Knox Carter"),
        ("Travis Long", "Wes Carter"),
        ("Jeff Lawless", "Drew"),
        ("Ben L. Cohen", "Andy"),
        ("Brianne Buishas", "Bar Attendee"),
        ("Brande Renzoni", "Delilah"),
    ],
    "His Bride by Bet": [
        ("Meg Bush", "Ellie Evans"),
        ("Noah Fearnley", "Mark Donahil"),
        ("Billy Walker", "Jeremy"),
        ("Victor Negrete", "Mark's Bodyguard"),
        ("Rachel Ashley Johnson", "Wedding Guest"),
        ("Evan Faunce", "Felix"),
        ("Christopher T. Young", "Mark's Bodyguard"),
        ("Michael Mac McMillian", "Mark's Bodyguard"),
    ],
    "Mic Drop Diva": [
        ("Cayla Brady", "Ivy Lancaster"),
        ("Christopher Quartuccio", "Blake Whitmore"),
        ("Christine Oswald", "Vanessa Reed"),
        ("Jacob Kaufman", "Tyler Carter"),
        ("Kobe Markworth", "Baxter"),
        ("Amanda Deljou", "Selina"),
        ("Kruz Valero", "Nurse Sarah"),
        ("Bailee Hebbler", "Jane"),
        ("Ethan Keller", "Zane"),
    ],
    "Kissed by Claw and Fang": [
        ("Hannah Lowery", "Ivy Stone"),
        ("Evan Adams", "Sebastian Moonflame"),
        ("Ben Armstrong", "Zane Vale"),
        ("Céline Planata", "Skyler Hill"),
        ("George Spielvogel III", "Edward"),
        ("Martina Monti", "Mia"),
        ("Jutta Charbonnier", "Kelly"),
        ("Joaquin Rodriguez", "Brady Wilson"),
        ("Scott Travis", "Elder Rufus"),
        ("David Moskowitz", "Dr. White"),
    ],
    "It Was Always You": [
        ("Shay Dinneen", "Liam Green"),
        ("Erin Orcutt", "Chloe Green"),
        ("Ryan Larson", "Alexander Miller"),
        ("Nilo Benicio", "Fred Miller"),
        ("B Hale", "Zoey Miller"),
        ("Eliot", "Mr. Bennett"),
        ("Sj Mendelson", "Dorothy Green"),
        ("Shannon Echols", "Maternity Doctor"),
    ],
    "Hate to Love You": [
        ("Krystal Pohaku", "Cheerleader #2"),
        ("Hannah Lowery", "Kennedy Clarke"),
        ("Blake Manning", "Shay Coleman"),
        ("Carter Moczan", "Gabe Clarke"),
        ("Keiva Bradley", "Casey"),
        ("Daniela Leon", "Becca Lee"),
        ("Kimberly Crabb", "Aby Martinez"),
        ("Chaz Lack", "Carruthers"),
        ("Jonah Walker", "Parker Stanson"),
        ("Cailynn Knabenshue", "Mina"),
    ],
    "Sex Education with My Enemy Stepbrother": [
        ("Hannah Lowery", "Tessa Morgan"),
        ("Blake Manning", "Connor Vaughn"),
        ("Sam Drake", "Brad Dawson"),
        ("Sierra Kazil", "Kelly Carmichael"),
        ("Sarah Halstead", "Linda Morgan"),
        ("Ryan Barrier", "Jonathan Vaughn"),
        ("Katherine Morshedian", "Penny Walsh"),
        ("Maëva Karen Jolard", "Rebecca Olsen"),
        ("Jazmine Drucilla Jackson", "Self - Student A"),
        ("Desteny Tolbert", "Nerd Girl A"),
        ("Sorcha Chow", "Student B"),
        ("Peter McNamara", "Physical Therapist"),
    ],
    "Craving My Brother's Best Friend": [
        ("Cayla Brady", "Alison"),
        ("Evan Adams", "Brett Harrison"),
        ("James C. Burns", "Coach Brenner"),
        ("Corinne DeCost", "Megan"),
        ("AnnMarie Giaquinto", "Cheerleading Coach"),
        ("Emma Dusenbury", "Rita"),
        ("Victoria Saitz", "Madison"),
        ("Wesley Dean", "Jason"),
        ("Smeet Doshi", "Alex"),
        ("Deontay Wilson", "Security Guard"),
    ],
    "Claimed by My Ex's Alpha Brother": [
        ("Savannah Coffee", "Ella Wilson"),
        ("Blake Lewis", "Liam Gravens"),
        ("Shane Dorriz", "Noah Gravens"),
        ("Nadia Wilemski", "Ava Reynolds"),
        ("María José De La Cruz", "Jade Edge"),
        ("Frankie Stofan", "Kat"),
        ("Jaida Henley", "Rachel"),
        ("Jones Titera", "Young Ella"),
        ("Raphaella Dreyer", "Elder Witch"),
        ("Kennedy Remery-Pearson", "Young Bully"),
        ("Alex Kravitz", "Pack Dignitary"),
    ],
    "The Glow-Up Game": [
        ("Joseph Purcell", "Daniel Jackson"),
        ("Kirsten Kendall", "Lexi Fox"),
        ("Nikki Hru", "Camille Lannister"),
        ("Charlie Wood", "Josh"),
        ("Mary Foster", "Reece"),
        ("Dilara Foscht", "Stylist Gertrude"),
        ("Joseph Wright", "Angry Diner at a fancy restaurant"),
    ],
    "Falling For My Bodyguard": [
        ("Kyra Wisely", "Harmoni"),
        ("Joseph Purcell", "William"),
        ("Sophie Steele", "Emily"),
        ("Noah Andre", "Jesse"),
        ("Rib Hillis", "James"),
        ("Mark Chinnery", "Butler"),
    ],
    "Breathe": [
        ("Savannah Coffee", "Sadie White"),
        ("Blake Lewis", "Jax Stone"),
        ("Mitchell Hawes", "Jack"),
        ("Luchy Salvador García", "Self - Teenage Student C"),
        ("Blade Ladson", "Star Halloway"),
        ("Sophia Marie", "Teenage Fan"),
        ("Meredith Riley Stewart", "Marissa Stone"),
        ("Marval A. Rex", "Kane"),
        ("Bree Long", "Jessica White"),
        ("Grace Ella", "Pauline"),
        ("Rachel Ashley Johnson", "Colleague"),
    ],
    "Bound by Honor": [
        ("Savannah Coffee", "Aria"),
        ("Rhett Wellington", "Luca"),
        ("Savanna Blau", "Gianna"),
        ("LX Xander", "Enzo"),
        ("Anna Lumley", "Grace"),
        ("Jozé Nicolini", "Raffaele"),
        ("Kelton White", "Frankie"),
        ("Ashley North", "Jenny"),
        ("Robyn Stephenson", "Layla"),
        ("Ronald Quigley", "Rocco"),
        ("Jonah Walker", "MAN#1"),
        ("Vivian Dao", "Doctor"),
        ("Ryan Knapper", "Mafia 1"),
        ("David Eugene Sweat", "Priest"),
        ("Serena Jordan", "Bully"),
        ("Arturo Vega", "MAN#2"),
        ("Shervin Gholian", "Self - Mafia Man"),
        ("Alfonso Illan Sutton", "Enzo"),
    ],
    "Fight Dirty": [
        ("Olivia Rose Williams", "Kenzie Goodman"),
        ("Carter Malone Harvey", "Clay Barton"),
        ("Cameron Somers", "Tristan"),
        ("Haulston Mann", "Patrick"),
        ("Marcus Mannis", "Viper"),
        ("Jade Spurr", "Ashley"),
        ("Isabella Garcia", "Lacey"),
    ],
    "Life Is Not a Game": [
        ("Halle Fletcher", "Charlotte"),
        ("Noah Andre", "TJ"),
        ("Emma Reinagel", "Tracy"),
        ("Nate Memba", "Cory"),
    ],
}

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def loose(s): return re.sub(r"[^a-z0-9]", "", s.lower())
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
by_title = {t["primary_title"]: t for t in titles}
by_name = {p["name"].strip().lower(): p for p in people}
by_loose = {}
for p in people: by_loose.setdefault(loose(p["name"]), p)
cred_idx = {(c["title_id"], c["person_id"]): c for c in credits}
queued = {(q["candidate_a"], q["candidate_b"]) for q in queue}
existing_ids = {p["person_id"] for p in people}

new_credits, new_people, to_queue, filled_chars = [], [], [], []
matched = created = 0

for title_name, cast in CAST.items():
    t = by_title.get(title_name)
    if not t:
        print(f"NOT IN titles.csv, skipped: {title_name}"); continue
    tid = t["title_id"]
    for order, (actor, character) in enumerate(cast):
        key = actor.strip().lower()
        person = by_name.get(key)
        if person is None:
            near = by_loose.get(loose(actor))
            if near is None:
                close = difflib.get_close_matches(loose(actor), by_loose.keys(), n=1, cutoff=0.90)
                if close: near = by_loose[close[0]]
            if near is None:
                # A middle name defeats character-similarity entirely: "Megan Suzanne Beattie"
                # vs "Megan Beattie" scores below any sane cutoff, yet is obviously one person.
                # Match on first + last word instead.
                aw = actor.split()
                if len(aw) >= 2:
                    a_key = (aw[0].lower(), aw[-1].lower())
                    for cand in people + new_people:
                        cw = cand["name"].split()
                        if len(cw) >= 2 and (cw[0].lower(), cw[-1].lower()) == a_key:
                            near = cand
                            break
            if near is not None and near["name"].strip().lower() != key:
                pair = (near["person_id"], slug(actor))
                if pair not in queued:
                    queued.add(pair)
                    to_queue.append({"candidate_a": near["person_id"], "candidate_b": slug(actor),
                                     "evidence": f"IMDb page for '{title_name}' credits '{actor}'; people.csv has "
                                                 f"'{near['name']}'. Same role, so almost certainly one person, but "
                                                 f"names differ. Not merged pending a ruling.",
                                     "status": "pending"})
                # The existing person is the one already credited, so still fill their character.
                ex = cred_idx.get((tid, near["person_id"]))
                if ex is not None and not (ex.get("character_name") or "").strip() and character:
                    ex["character_name"] = character
                    filled_chars.append(f"{near['name']} -> {character}")
                continue
            pid = slug(actor)
            if pid in existing_ids: continue
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
            # Already credited: only fill a blank character name, never overwrite.
            if character and not (ex.get("character_name") or "").strip():
                ex["character_name"] = character
                filled_chars.append(f"{person['name']} -> {character}")
            continue
        rec = {"title_id": tid, "person_id": person["person_id"],
               "role": "lead" if order < 2 else "actor", "character_name": character}
        cred_idx[(tid, person["person_id"])] = rec
        new_credits.append(rec)

print(f"new credits: {len(new_credits)} | people matched {matched} | created {created}")
print(f"character names filled on EXISTING credits: {len(filled_chars)}")
for f in filled_chars: print("   ", f)
print(f"near-duplicates queued: {len(to_queue)}")
for q in to_queue: print("   ", q["evidence"][:120])

if "--dry-run" in sys.argv:
    for c in new_credits: print("   +", c["person_id"], "as", c["character_name"])
    print("(dry run, nothing written)"); raise SystemExit

if new_people: save("people.csv", list(people[0].keys()), people + new_people)
if new_credits or filled_chars: save("credits.csv", list(credits[0].keys()), credits + new_credits)
if to_queue: save("match_queue.csv", list(queue[0].keys()), queue + to_queue)
print(f"\nwrote {len(new_credits)} credits, {len(new_people)} people, {len(to_queue)} queued, "
      f"{len(filled_chars)} character names filled")
