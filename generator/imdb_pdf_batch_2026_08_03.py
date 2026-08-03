"""Cast transcribed from Cyan's 16 manually-saved IMDb PDFs, 3 August 2026.

WHY THIS FILE EXISTS: the PDFs were read once, by hand, and the transcription is
the expensive part. Holding it here means a future session re-runs this instead of
re-reading 16 PDFs. The PDFs themselves were in C:\\Users\\cyanj\\Downloads.

11 ACTOR pages (a filmography each) and 5 TITLE pages (a cast each). Names and
character names are EXACTLY as IMDb printed them, including IMDb's own spellings
where they differ from ours - see OURS below, which maps IMDb's spelling to the
people.csv spelling for the one case that has been evidenced.

READ-ONLY. This script writes nothing. It reports what an import WOULD add:
new credits, character names for credits we already hold blank, new people, and
IMDb credits for titles not in titles.csv. Run it from anywhere:

    PYTHONUTF8=1 python generator/imdb_pdf_batch_2026_08_03.py

As of 3 August 2026 it reports 82 new credits (38 of them GoodShort, the platform
that publishes no cast anywhere), 62 character names, 29 new people, and 97
distinct unmatched titles.

BEFORE IMPORTING ANY OF THIS, read the 3 August entry in the Craft doc
"7. Technical Architecture". Two rules from it: the 97 unmatched titles must NOT
be bulk-added, because IMDb does not state which app a title is on; and the
filmographies carry non-vertical work (Reed's Point, Dhar Mann, music videos, a
video game) that must be filtered out, not ingested.
"""
import csv, re, collections, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ACTORS = {
"Artem Plonder": [  # our people.csv spelling: Artem Plyonder
 ("His Next Target: My Heart","James"),("Bloodlust","Victor"),("Sultan's Heart","Serkan Guler"),
 ("A Queen for the Mafia Kings","Liam Blackwood"),("No Escape from the Mafia King's Embrace","Soren Moreti"),
 ("The Maid Who Became His Cinderella","Jeremy"),("Bleeding Blue Bird","Cat"),
 ("The Mafia Beast Won Me in a Gamble","Neil"),("Hired for Pleasure",""),("Brace Face Betty","Vel"),
 ("Too Young to Want Her Professor","Nate Blackwell"),("I Became My CEO's Darkest Secret","Jared Branson"),
 ("My Golden Cage","Geremy"),("Taboo Match","Jack"),("Bride for Lucifer","Lucas Craven Lucifer"),
 ("Act Like You Love Me","Walt"),("Alpha King's Hated Princess","Chad"),
 ("Sold to the Possessive Mafia Boss","Havier"),("The Alpha's Mate Who Cried Wolf","Gamma Kane"),
 ("Love Captive to the Mafia Boss","Harvey")],
"Hannah Lowery": [
 ("My Billionaire Enemies Are Secretly My Family","Ariel Scarlett"),("Revenge Puck","Lucy"),
 ("Hate to Love You","Kennedy Clarke"),("Corrupting My Billionaire Boss's Heart","Lyla Walker"),
 ("Pucked in the Friend Zone","Reese"),("Sex Education with My Enemy Stepbrother","Tessa Morgan"),
 ("Kissed by Claw and Fang","Ivy Stone"),("Good to See You Again, My Billionaire Baby Daddy","Lina Wells"),
 ("Sisterhood of Lies: Pledge for Revenge","June & Ashlyn Wadsworth"),("Too Late to Miss Me","Anna"),
 ("Heiress's Ballet Revenge","Alicia Deville"),("Tell Me Not to Love You","Brie Ellison"),
 ("Pucked by My Brother's Rival","Jenny"),("Mile High on Cloud 9","Nevaeh Brooks"),
 ("Escaping the Mafia, I Married a Homeless Billionaire","Myra"),("The Devil's Bride","Julia Byrd"),
 ("My Online Crush Is My Contract Husband","Gillian"),
 ("Sleeping for 30 Years, My Brothers Kneel for Me","May Grayson"),
 ("Finally See You Carrying Our Baby","Chloe"),("My Mile High Billionaire Obsession","Harper"),
 ("If Loving You Is a Sin Then I'll Go to Hell","Ellie Jones"),("Shotgun Wedding with My Boss","Roxanne Fields"),
 ("Love at the End of Lies","Ava"),("Uncle William, Please Say I Do","Alaina Carter DuPont"),
 ("My Wedding Day Fortune","Rachel Grant"),("Secretly Married to My Billionaire Boss","Leila Myers"),
 ("My Vampire System Omnibus","Kensey"),("The Devil Wears Desire","Jenny"),
 ("Break My Heart Again","Interviewee #1"),("The Return of My Drama Queen","Sadie Fontaine"),
 ("The Rise of Mr. and Mrs. Mafia","Michelle"),("Ms. Swan, Teach Me Love","Female Student #1")],
"Evan Adams": [
 ("Keeping Secrets with the Rowing Captain","Brad"),("Revenge Puck","Blake Ashburn"),
 ("Foul Play with My Brother's Best Friend","Jaden"),("Craving My Brother's Best Friend","Brett Harrison"),
 ("Academy of Lies","Judd"),("The Day My Stepbrother Knows My Dirty Secret","Seth Astor"),
 ("Kissed by Claw and Fang","Sebastian Moonflame"),("Kissing the Wrong Brother","Miles Carson"),
 ("Wild Ride with the Dangerous Kian","Kian Wilder"),("Pucked by My Brother's Rival","Xavier"),
 ("Lap by Lap: Back to You","Justin"),("Accidentally Slept with the Young Mafia Boss","Vincent"),
 ("Hot Gardener's Seduction","Arthur"),("The Bad Boy Who Ruined Me","Zach Lloyd"),
 ("Dear Stranger, I Love You","Brad Sterling"),("The Senator's Son","Zach Walker"),
 ("The Virgin Camp Counselor","Asher"),("Baby Daddy Goals","Max Mendelson"),
 ("Oops, I'm in Love with My Step-Brother","Finn Swanson"),("Summer Situationship","Noah Allen"),
 ("My Vampire System 2","Quinn"),("My Secret with Country Boys","Zach Miller"),("Mated to the Alpha","Alpha")],
"Luke Dodge": [
 ("Teach Me How to Say Goodbye","Colton"),("Taming My Bullies 3","August"),
 ("Taming My Bullies 2","August Langford"),("The Maid and the Ice Prince","Tony"),
 ("Cleaning His Mansion, Catching His Heart","Noah"),("The Day the Champion Racer Lost His Bride","Ryder Kane"),
 ("Miss President, at Your Service","Wayne Davis"),("Their Brother Lost in Space","Timothy Snyder"),
 ("Turn Left to Mr. Right","Nate Barrett"),("Oops! Nerdy Girl Is My Kitten","Julian"),
 ("Tell Me Not to Love You","Teddy"),("Taming My Bullies","August Langford"),
 ("The Tutor Trap","Brady Wilder"),("Don't Miss Me When I'm Gone","Dylon Miller"),
 ("My Boss Is My Secret Sperm Donor","Xavier"),("Straight A Pregnancy","Hunter"),
 ("Second Baby Second Chance","Bobby")],
"Bar Daniel": [
 ("Breaking My Bodyguard","Kinsley"),("Pucking My Brother's Offside Rival","Lilith Thorne"),
 ("Taming My Bullies 3","Hazel"),("Taming My Bullies 2","Hazel"),("When the Moon Hides Her Crown","Lily"),
 ("Scandalous","Young Woman 2"),("Baby Daddy at the Front Desk","Laura"),
 ("Tutoring My Rival Boy","Bianca Brown"),("Frozen Wife, Unfrozen Revenge","Vivian"),
 ("Taming My Bullies","Hazel Jones"),("Straight Until He Kissed Me","Cindy"),
 ("My Ex's Uncle Put Quadruplets in Me","Tina"),("Fake Dating My Rich Nemesis","Daphne Remiah"),
 ("Regret Is the Punishment","Merry Brown"),("When Love Comes Too Late","Dessert Shop Worker")],
"Cameron Porras": [
 ("Nero: Made Men","Nero Caruso"),("I Accidentally Sexted My Enemy","Colton Hayes"),
 ("Taming My Bullies 3","Rowan"),("Taming My Bullies 2","Rowan Calloway"),
 ("Sex Education by My Best Friend","Chase"),("Marked by My Alpha Stepbrother","Caleb Hawthorne"),
 ("Vicious","Baron Vicious Spencer"),("Outplayed","Ethan Cambry Thorne"),
 ("My Boyfriend Gave My Virginity to His Bro","Dylan"),("The Daughter of Zeus","Kairos"),
 ("Frozen Wife, Unfrozen Revenge","Julian Sinclair"),("Taming My Bullies","Rowan Calloway"),
 ("Surrender to My Dominant Doctor","Sebastian Bale"),("The Lost Son Returns as the Duke","Arthur"),
 ("My Stepbrother's Dirty Secret","James Hatton"),("Song of My Mother's Tears","Seth"),
 ("Mafia Boss Becomes My Pet","Nigel"),("The Billion Dollar Baby","Ethan Blake")],
"Meg Bush": [
 ("Pregnant with the Hockey Star's Baby","Katy Moore"),("Echoes of Your Heartbeat","Ella Collins"),
 ("Taming My Bullies 3","Emma"),("Taming My Bullies 2","Emma Parker"),("Reborn for the Crown","Mia"),
 ("His Bride by Bet","Ellie Evans"),("Emily in Her Glow-Up Era After Ex's Out","Emily"),
 ("Scandalous","Edie Van Der Zee"),("My Billionaire Devil","Alicia"),("The One That Got Away","Bella Rupert"),
 ("Breaking News","Summer"),("Time to Cut Off My Shameless Family","Peggy"),
 ("From Zero to Hero: My Super-Vision Husband","Vanessa Shaw"),("The CEO and the Country Girl","Avery"),
 ("The One I Never Forget","Sofia Macaulay"),("Taming My Bullies","Emma Parker"),
 ("Taming the Landlord","Evelyn"),("Fake Dating My Rich Nemesis","Tessa Sinclair"),
 ("Mancini's Forbidden Bride","Ava Jackson"),("Keys to My Heart","Sophie"),
 ("Breaking My Boss: Purity Bet","Emma Davis"),("Bye Mr. Ex, Your Commander Is Calling","Hazel Langston"),
 ("A Girl's Guide to Queen Bee Takedown","Audrey Wintersby Rose"),("Woke Up Married to My Crush","Alice"),
 ("My Cold-Hearted Mafia King","Vivian Green"),("Pretty Baby","Rosy"),
 ("Billionaire CEO's Secret Obsession","Leah"),("Baby Trapped by the Billionaire","Katie Marshall"),
 ("Maid for My Nemesis","Emma Johnson"),("Playing by the Billionaire's Rules","Becky Jacobs"),
 ("Mr. Hill's Adorable Wife","Valerie Patterson"),("The Heiress Strikes Back","Amelia")],
"Sasha Anika": [
 ("Love Tied by Hate","Jolene"),("A Queen for the Mafia Kings","Jasmine Harlow"),
 ("Cousins by Name Lovers in Secret","Emma Middleton"),("The President's Secret Daughter","Liora"),
 ("Make Me Yours","Peyton Pierce"),("The Mafia Beast Won Me in a Gamble","Lauren"),
 ("My Billionaire Boss Claimed Me as His Prize","Ivy Rivers"),
 ("I Became My CEO's Darkest Secret","Iris Little"),("What Was I Made For","Evelyn"),
 ("Taboo Match","Anna"),("Under the Royal Rule","Diana Watson"),("Act Like You Love Me","Gina"),
 ("Spark Me Tenderly","Floris Blossom"),("Sold to the Possessive Mafia Boss","Jane"),
 ("The Shy Beauty and the Billionaire Beast","Ana"),("The Mafia Boss",""),("Victim's Eyes","")],
"Vanessa von Schwarz": [
 ("Falling for the Striker","Sylvie"),("Laws of Attraction","Penny Hartford"),
 ("Forbidden Eyes in the Dark","Clarissa"),("My Secret Affair with Ex's Brother","Clara Murphy"),
 ("The Sorority Hazed the Wrong Girl","Victoria Hart"),("Too Late, My Ex-Campus King","Serena Alden"),
 ("The Christmas Contract: Mafia Stand-In Bride","Eliana"),("Your Husband Is Mine","Vivienne Cross"),
 ("His Love Was A Lie","Tessa Whitmore"),("Imprisoned Phoenix","Siv"),
 ("Cheer Queen Returns to Slay","Lexi"),("Hollywood Heartthrob","Scarlett"),
 ("Married to the Secret Lycan King","Vivian Wilder"),
 ("Breaking the Deal with My Hockey Bad Boy","Melissa Shelton"),("The Scent That Made Him Mine","Cassie"),
 ("The Virgin Stripper and the Hockey Star","Serena"),("Mated to My Savage Alpha","Jennifer"),
 ("In Love with My Taken Boss","Amanda"),("Saving Nora","Angela"),
 ("My Double Life with the Hoffmans","Christine DeLeon"),("My Wedding Day Fortune","Natalie Brown"),
 ("The Quarterback Next Door","Tiffany Ryland"),("Breaking the Darkness","Clara"),
 ("Royal's Successor Is a Maid","Vivian Blackwell"),("Señorita Playing with Fire","Isabella Rosa Morales"),
 ("Love Mission","Amanda Wood"),("Forbidden Love","Indigo")],
"Eric Guilmette": [
 ("Forbidden Eyes in the Dark","Masked Man Leo"),("The All-American Rejects: Superfan","Josh"),
 ("Djinn Under Contract","Elijah Baran"),("My Billionaire Devil","Preston Rothschild"),
 ("CEO's Kansas Sweetheart","Dominic Knight"),("Your Twin Cupids Reporting for Duty","Cassian Hayes"),
 ("My Silent Treasure","Dean Weston"),("Dungeons of Ecstasy","Luke Lucian"),
 ("The Healing Touch","Blade"),("When My Ex Becomes My Gynecologist","Blade"),
 ("I Slept with My Three Werewolf Stepsons","Alexander Blackburn"),
 ("Goodbye After 99 Forgiveness","Marcus"),("Love & Blood","Noah Archer"),
 ("How We Measure Guilt in Bed","Troy"),("CEO's Baby Mama Secretary","Finn Vanderbilt"),
 ("Campus Rivals","Xavier Brooks"),("Boss Please Behave","Mike Wright"),
 ("Married a Billionaire Behind the Mask","Ethan Warnimont Connor"),
 ("Seducing Mr. Sterling: The Ice-Cold Heir","Ethan Sterling"),("The Alpha's Gifted Luna","Allen"),
 ("Stealing My Alpha's Heart","Sebastian"),("What Happens in Vegas","Lucas Worthington"),
 ("I Adopted My Stolen Baby","Michael"),("The Secret She Couldn't Escape","Alex Crow"),
 ("Chosen by Fate, Rejected by the Alpha","Reece The Alpha"),
 ("Treasured by My Alpha Brother","Leonardo Rossi Anthony Bianchi"),
 ("Devil's Triangle","Killian Vanderbilt"),("The Alpha King Is My Second Mate","Xander Kallias"),
 ("The Big Shot Is My Ex-wife","Frederick"),("I'm the Rule","Joseph Brando"),
 ("The Return of the Unwanted Wife","Elijah Cromwell"),("My Gigolo Alpha","Brian Charles"),
 ("You Belong with Me","Henry Lockwood"),("The Unwanted Mate","Keiran"),
 ("Forget Me Not: Omega's Return","Theodore Joseph")],
"Franky Cammarata": [
 ("A Wife for Two Rivals","James Moretti"),("Oops I Married My Daughter's Daddy","Alex Sterling"),
 ("Found My Daddy at the Construction Site","Tristen Bolton"),
 ("Found A Homeless Genius to Save My Company","Ethan Dalton"),
 ("Boss, Your Ex-Con Bride Is Back","Lucien Lowell"),("I Stand Where Love Ends","Cooper Walker"),
 ("The Girl They Left Behind","Nathaniel Benjamin"),("Assemble My Avenging Billionaires","Felix Luxton"),
 ("Dominate Me Please, Mafia King","Finn"),("Cases Closed: The Legal Queen Returns","Ian Fuller"),
 ("Bound by Blood: The Mafia King's Sweetheart","Salvatore Mancini"),
 ("This Time I Choose Mr. Mafia","Adrian Hawthorne"),("Trapped and Redeemed by His Love","Archer"),
 ("She Finds Redemption in His Love","Jackson Carroll"),("Kidnapped by the Mafia","Vicenzo")],
}

TITLES = {
"Found My Daddy at the Construction Site": [
 ("Franky Cammarata","Tristen Bolton"),("Dylan Lee","Dani Duvall"),("Haley Lohrli","Giselle Duvall"),
 ("Jayda Stephens","Jada Mendez"),("Alicia Read","Celeste"),("Cameron Love","Zachary Slater"),
 ("Grace Fouracre","Kimberly Hale"),("Madison McConnachie","Guest"),("Julie Bruns","Diane Duvall"),
 ("Gavin Marck","Lance Clarke"),("Gavin LeClaire","Silas Duvall"),("Carolyn Rogers","Saleswoman"),
 ("Michaela Mackenzie","Employee A"),("Jennifer Belanger","Nova Schulz"),("Duke Murrdodge","Pastor"),
 ("Steven Kammerer","Dr. Voss"),("Joshua John Krenus","Club Manager"),("Aneurin Sheasby","Guest")],
"Found A Homeless Genius to Save My Company": [
 ("SeAnne Simpson","Audrey"),("Wendy Dow","Reporter #1"),("Franky Cammarata","Ethan Dalton"),
 ("Ben Whalen","Richard Harrington"),("Tristan Wilder Hallett","Ethan Dalton (Young)"),
 ("Michelle Levy","Guest 5"),("Claudia Sprague","Guest 1"),("Peter D'Alessio","Manufacturer #1"),
 ("Brian Sheltra","Guest 2"),("Lauren Smith","Sophia Harrington (Adult)")],
"Pucked by My Brother's Rival": [
 ("Hannah Lowery","Jenny"),("Evan Adams","Xavier"),("Katie Rose","Rosalie"),
 ("Eloise Lola Gordon","Lisa"),("Joseph Girard","Samuel Carter"),("Bo Burroughs","Chris"),
 ("Andrew Brown","Harrison")],
"Taming My Bullies": [
 ("Meg Bush","Emma Parker"),("Cameron Porras","Rowan Calloway"),("Bar Daniel","Hazel Jones"),
 ("Travis Owens","Liam Davenport"),("Luke Dodge","August Langford"),("Grant Lowell Garcia","Karl Reed"),
 ("Stacey Marie Keba","Amy"),("Nicholas Amodio","Noah"),("Jennifer Dunn","Julia Parker"),
 ("Céline Planata","Chelsea"),("Francisco DeCun","Mason"),("Elizabeth Stenmoen","Student 1"),
 ("Tigerlily Morales","Vera"),("Thomas Patrick Riley","David"),("Evelyn Case","Student 3"),
 ("McKenzie Morris","Schoolgirl Lockers 2")],
"I Became My CEO's Darkest Secret": [
 ("Artem Plonder","Jared Branson"),("Sasha Anika","Iris Little")],
}

# our people.csv spelling where IMDb differs
OURS = {"Artem Plonder": "Artem Plyonder"}

def norm(s):
    s = s.lower().replace("’","'").replace("&","and")
    return re.sub(r"[^a-z0-9]+", "", s)

titles = list(csv.DictReader(open(os.path.join(REPO,"data/titles.csv"), encoding="utf-8")))
people  = list(csv.DictReader(open(os.path.join(REPO,"data/people.csv"),  encoding="utf-8")))
credits = list(csv.DictReader(open(os.path.join(REPO,"data/credits.csv"), encoding="utf-8")))
avail   = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(REPO,"data/availability.csv"), encoding="utf-8")):
    avail[r["title_id"]].append(r["platform_id"])

t_by_norm = {norm(t["primary_title"]): t for t in titles}
p_by_norm = {norm(p["name"]): p for p in people}
have = {(c["person_id"], c["title_id"]): c for c in credits}

new_credits, new_chars, unknown_titles, new_people = [], [], [], set()
plat_hits = collections.Counter()

def consider(actor_name, title_name, character, origin):
    ours_name = OURS.get(actor_name, actor_name)
    p = p_by_norm.get(norm(ours_name))
    t = t_by_norm.get(norm(title_name))
    if t is None:
        unknown_titles.append((title_name, actor_name, origin)); return
    if p is None:
        new_people.add(actor_name)
        new_credits.append((actor_name, t["primary_title"], character, "|".join(avail[t["title_id"]]), origin))
        plat_hits["|".join(avail[t["title_id"]]) or "(no platform row)"] += 1
        return
    key = (p["person_id"], t["title_id"])
    if key in have:
        if character and not have[key]["character_name"]:
            new_chars.append((ours_name, t["primary_title"], character, origin))
    else:
        new_credits.append((ours_name, t["primary_title"], character, "|".join(avail[t["title_id"]]), origin))
        plat_hits["|".join(avail[t["title_id"]]) or "(no platform row)"] += 1

for actor, rows in ACTORS.items():
    for title_name, character in rows:
        consider(actor, title_name, character, f"{actor} filmography")
for title_name, rows in TITLES.items():
    for actor, character in rows:
        consider(actor, title_name, character, f"{title_name} cast page")

print("=" * 70)
# A person can reach the same title twice: once via their filmography, once via that
# title's cast page. Import must dedupe on (person, title), so report both numbers.
print(f"NEW CREDITS available      : {len({(a, t) for a, t, ch, plat, src in new_credits})} "
      f"({len(new_credits)} rows before deduping person+title)")
print(f"CHARACTER NAMES for existing credits that have none : {len(new_chars)}")
print(f"NEW PEOPLE (not in people.csv)                      : {len(new_people)}")
print(f"IMDb credits for titles we do NOT hold              : {len(unknown_titles)}")
print()
print("New credits by platform of the matched title:")
for k, v in plat_hits.most_common():
    print(f"   {k or '(none)':22s} {v}")
print()
print("--- GOODSHORT new credits (the platform that publishes no cast) ---")
for a, t, ch, plat, src in new_credits:
    if "goodshort" in plat:
        print(f"   {t:52.52s} {a:24.24s} {ch}")
print()
print("--- character names recoverable for credits we already hold ---")
for a, t, ch, src in new_chars[:25]:
    print(f"   {t:48.48s} {a:22.22s} -> {ch}")
print(f"   ... {len(new_chars)} total")
print()
print("--- new people that would be created ---")
print("   " + ", ".join(sorted(new_people)))
print()
print(f"--- IMDb titles not in titles.csv: {len(unknown_titles)} "
      f"({len({norm(u[0]) for u in unknown_titles})} distinct) ---")
for t in sorted({u[0] for u in unknown_titles})[:40]:
    print("   ", t)
