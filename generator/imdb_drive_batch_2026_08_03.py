"""Cast, IMDb ids and a book credit from Cyan's Google Drive IMDb PDFs, 3 August 2026.

Folder: "Dramaeverafter", drive.google.com/drive/folders/1ndq_ecYP2GvBKKngurYY-rqZ5TuXfFgu
36 files. This module holds what has been transcribed from them so far.

WHY THESE ARE BETTER THAN THE Downloads BATCH: the Drive copies extract with the IMDb
link list intact, so every cast row carries its nm id and every page its tt id. The
Downloads batch gave names only. Record the id with the credit - the 1 August pass threw
seven nm ids away on refusal and the searches had to be redone.

CAST rows are (actor, character, nm_id) exactly as IMDb printed them, in its cast order.
That order is NOT billing order - see apply_imdb_batch_2026_08_03.py - so nothing is lead.

CROSS-CHECK THAT PASSED: Olivia Rose Williams resolves to nm17198698 on both the
Fight Dirty and Life Is Not a Game pages independently.
"""

# title in titles.csv -> (imdb tt id, [(actor, character, nm id), ...])
CAST = {
    "Fight Dirty": ("tt41152236", [
        ("Olivia Rose Williams", "Kenzie Goodman", "nm17198698"),
        ("Carter Malone Harvey", "Clay Barton",    "nm16309879"),
        ("Cameron Somers",       "Tristan",        "nm11156502"),
        ("Haulston Mann",        "Patrick",        "nm5498943"),
        ("Marcus Mannis",        "Viper",          "nm13982321"),
        ("Jade Spurr",           "Ashley",         "nm10754557"),
        ("Isabella Garcia",      "Lacey",          "nm18373125"),
    ]),
    "Life Is Not a Game": ("tt40288266", [
        ("Halle Fletcher",       "Charlotte", "nm12690249"),
        ("Noah Andre",           "TJ",        "nm15813938"),
        ("Emma Reinagel",        "Tracy",     "nm11328568"),
        ("Nate Memba",           "Cory",      "nm13804506"),
        ("Olivia Rose Williams", "Sadie",     "nm17198698"),
    ]),
    "The Perfect Spiral": ("tt39774985", [
        ("Victoria Andrunik", "Alex Thompson", "nm8409836"),
        ("Jared Staub",       "Knox Carter",   "nm15994251"),
        ("Travis Long",       "Wes Carter",    "nm12751516"),
        ("Jeff Lawless",      "Drew",          "nm10703946"),
        ("Ben L. Cohen",      "Andy",          "nm16328827"),
        ("Brianne Buishas",   "Bar Attendee",  "nm12033767"),
        ("Brande Renzoni",    "Delilah",       "nm18206013"),
    ]),
}

# titles.csv `book` field. Stores the AUTHOR where IMDb names one, per the existing
# convention (a bare "yes" only when we know it is an adaptation but not by whom).
# Life Is Not a Game's IMDb storyline opens "Based on the novel by Kara Verbeek".
# This is the first hard evidence for the open question of whether CandyJar's catalogue
# is wholesale Inkitt/Galatea book adaptations - it is ONE title, not the other 89.
BOOK = {
    "Life Is Not a Game": "Kara Verbeek",
}
