"""IMDb's company page for Candy Jar (US), co1130595, read 3 August 2026.

WHY THIS FILE MATTERS MORE THAN ITS SIZE SUGGESTS. Every other IMDb source this project
uses has the same hole: IMDb does not say which app a title is on, which is what blocked
"The Cost of Touch" and what makes generic titles unusable. A COMPANY page states it by
definition - all 59 of these are CandyJar on IMDb's own say-so. That is platform
attribution from a source that normally cannot give it.

ORDERING WAS VERIFIED, NOT ASSUMED. The PDF interleaves metadata blocks with the numbered
title list, so year and tt id are matched by position. Three independent anchors confirm
the alignment: Fight Dirty -> tt41152236, Life Is Not a Game -> tt40288266 and
The Perfect Spiral -> tt39774985 all match the individual title PDFs read separately.

SYNOPSES ARE DELIBERATELY NOT CARRIED ACROSS. The company page has one for nearly every
title, but that is IMDb's editorial writing; our synopses come from the platforms
themselves. Cyan's call: add the titles blank and fill them from CandyJar's own site later.

ONE REFUSAL IS REVERSED BY THIS PAGE. "Our Dirty Little Secret" was refused on 1 August
because three unrelated IMDb productions share the title and none listed our character
Tulli. It is here at tt37527539 and its synopsis names Tulli, so the right production is
now identified. "Jekyll & Hyde", the other refusal, is NOT on this list, so that one stands.
"""

# (title, year, imdb tt id) in IMDb's popularity order
TITLES = [
    ("Fight Dirty",                        "2026", "tt41152236"),
    ("Grayson",                            "2026", "tt43702965"),
    ("Study Buddy",                        "2026", "tt43652002"),
    ("Falling for My Bodyguard",           "2026", "tt40805648"),
    ("The Ecstasy of Faking It",           "2026", "tt43709556"),
    ("Off Limits and All Mine",            "2026", "tt41617430"),
    ("Enemies",                            "2026", "tt43528025"),
    ("Sumner Comes First",                 "2026", "tt42095419"),
    ("Beneath the Blue Ice",               "2026", "tt43635271"),
    ("Don't Say Te Amo",                   "2026", "tt43665062"),
    ("Spoiled Rotten",                     "2025", "tt37286908"),
    ("Life Is Not a Game",                 "2026", "tt40288266"),
    ("The Glow-Up Game",                   "2025", "tt37692843"),
    ("Just Another Roomie",                "2026", "tt43328813"),
    ("Next Door",                          "2026", "tt42495282"),
    ("The Perfect Spiral",                 "2026", "tt39774985"),
    ("Private Lessons",                    "2025", "tt37898867"),
    ("Rooming with the Devil",             "2026", "tt39375684"),
    ("Loving My Brother's Best Friend",    "2025", "tt37748150"),
    ("The Cheer Scandal",                  "2025", "tt39027984"),
    ("The Bad Boy Wants Me",               "2025", "tt39179792"),
    ("Seeing Scarlett",                    "2026", "tt41742040"),
    ("The Stepford Vampires",              "2026", "tt39956966"),
    ("Chasing Kiarra",                     "2025", "tt37246287"),
    ("Secrets of Vixen",                   "2025", "tt37775860"),
    ("Alpha's Doe",                        "2026", "tt43387956"),
    ("The Fraternity",                     "2026", "tt39311143"),
    ("Beastly Lights",                     "2026", "tt42357339"),
    ("My Sexy Devil",                      "2025", "tt38220958"),
    ("Coming of Age",                      "2025", "tt37755961"),
    ("Luna Graced",                        "2025", "tt38221065"),
    # No metadata block sits against this one on the page, so its year is left unknown
    # rather than carried over from a neighbour.
    ("Broken: Enemies Attract",            "",     "tt43716919"),
    ("Did You Have to Be a Hockey Star?",  "2025", "tt39139863"),
    ("My Silent Treasure",                 "2026", "tt40106019"),
    ("The Arrangement: Parts 3 & 4",       "2025", "tt37245916"),
    ("The All-American Rejects: Superfan", "2026", "tt42946430"),
    ("Billionaire's Baby",                 "2024", "tt32055314"),
    ("His Muse",                           "2026", "tt41389885"),
    ("Victory Formation",                  "2025", "tt37246059"),
    ("The Arrangement: Part 4",            "2025", "tt37618067"),
    ("Taming the Heiress Part 1",          "2025", "tt38221149"),
    ("Hated by My Mate",                   "2026", "tt38347878"),
    ("Conflict of Interest",               "2025", "tt37908349"),
    ("Half of My Heart",                   "2025", "tt37070351"),
    ("Enemies with Benefits",              "2025", "tt38516169"),
    ("The Tutors",                         "",     "tt37521454"),
    ("In Love with Mr. Mafia",             "2026", "tt41743211"),
    ("Boss's Secret Baby",                 "2025", "tt35664732"),
    ("Not All About You",                  "2025", "tt37421444"),
    ("Taming the Heiress Part 2",          "2025", "tt38515978"),
    ("Beautiful Mistake",                  "2023", "tt30142531"),
    ("Exercise Discretion",                "2025", "tt37748257"),
    ("Older Than His Alibi",               "2025", "tt37178880"),
    ("French Kiss",                        "2025", "tt39311179"),
    ("Unfortunate Friends",                "2024", "tt34491679"),
    ("Our Dirty Little Secret",            "2025", "tt37527539"),
    ("New Beginnings",                     "2025", "tt37741708"),
    ("Secrets of Siren",                   "2025", "tt38988990"),
    ("Billionaire Love Start with Lies",   "2025", "tt35702185"),
]
