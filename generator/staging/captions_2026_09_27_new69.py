# -*- coding: utf-8 -*-
"""New titles from the 27 Sep 2026 weekly scrape (reelshort_2026-09-27),
69 titles that landed needs_check with no synopsis of ours.

Written from each title's own ReelShort page, banked by the scrape in
generator/staging/reelshort_2026-09-27.json and read by caption_pipeline.load_facts().

All 69 rank below top 300 by reach, so the 16 Aug 2026 ruling would allow
applying without review. Cyan reviewed last week's new-title batch, so this one
is STAGED UNAPPROVED and goes through her review page before apply.

THIN SOURCES, written short from the setup only, nothing invented:
  mom-love-me-again  (140 chars; also held in match_queue as a same-slug clash)
  bound-by-hatred    (143 chars, premise only, no names)
  fool-no-more-king-returns, one-night-stand, dream-on, my-x-ray-eyes-rule-the-city

draft-dreams: the source is first person and never gives the narrator a gender.
Written as "he" (basketball draft); Cyan to confirm.
"""

CAPTIONS = {

    # 10.5M    We Are Twins, Daddy!
    'we-are-twins-daddy':
        "Her best friend drugged her and sold her. The night she got away changed everything.\nShe's drugged by the friend she trusted most and handed over to a man for money. She manages to escape, runs straight into a stranger who has been drugged too, and they end up spending the night together. The next morning she learns her best friend and her ex fiance were in it together. When she confronts them she gets hurt and trapped in a fire, and only just survives. Months later she gives birth to twins. Then one of her babies is taken from her.",

    # 10.4M    One Night Stand
    'one-night-stand':
        "One night with her boss. Now she's carrying his baby.\nEmily is an office assistant who works hard and wants more out of life than she has. Then she has a passionate one night stand with Richard, her charming boss, and finds out she's pregnant. Nothing about her life is going to go the way she planned.",

    # 10.0M    Mom, Love Me Again
    'mom-love-me-again':
        "She was framed and it cost her life. Now she gets another one.\nSomeone set her up and she died for it, and the man she loved got it wrong about their own daughter. Given a second life, she's going to use it to protect the people she loves and make the ones who hurt her pay.",

    # 14.3M    Revenge-Uniting with My Rival
    'revenge-uniting-with-my-rival':
        "Her husband is cheating and quietly moving their money. So she teams up with his mistress.\nShe put her own career aside for her husband, then learns he's been cheating on her and secretly shifting their shared assets out of reach. She needs proof before she can divorce him, so she helps his mistress see what kind of man he really is and talks her into working together. Two women who should be enemies are now on the same side. But can a partnership like that last, or will jealousy tear it apart?",

    # 14.2M    I'm the Dragon King & Legendary Healer
    'i-m-the-dragon-king-legendary-healer':
        "A beggar with a battered bowl says he can cure what no doctor could.\nThe eldest daughter of one of the most powerful men in finance is gravely ill, and no expert has been able to help her, no matter how big the reward her father offers. His younger daughter walks past the reward notice and stops to drop a few coins for a beggar on the street. That beggar is a legend in disguise, and to repay her kindness he promises to grant her one wish and follows her home. Her father can't believe a beggar is the answer. Then the beggar gets to work.",

    # 6.8M    Mending a broken love
    'mending-a-broken-love':
        "Seven years together, and it still fell apart.\nAfter seven years, misunderstandings and betrayals finally break the couple up. Then she's gone for good, taken by a love that seems perfect, and he finally understands what he had. Now he's determined to make it right and will try anything to win her back.",

    # 10.4M    I'm Really Not an Immortal
    'i-m-really-not-an-immortal':
        "An orphan raised on a mountain comes down knowing more than anyone expects.\nHe's an orphan his teacher rescued and carried up the mountain, and he grew up learning divine skills at his side. His teacher once shouted at him for wasting the precious ingredients meant for a divine medicine, then was stunned when he actually made it work. Now he's come down to see the world. On his very first day he meets a girl and saves her father's life. What none of them realize is that they are the family he lost, and he's far more powerful than he looks.",

    # 14.9M    Love After Rebirth: Spoiled by My Husband's Uncle
    'love-after-rebirth-spoiled-by-my-husband-s-uncle':
        "Her husband killed her. This time she's marrying his uncle.\nIn her last life the man she married betrayed her and killed her. Reborn, she wakes up on the day the two families first meet, and this time she walks away from her fiance and picks his uncle instead, a powerful man nobody can quite read. People whisper that there's something wrong with him. Married life turns out to be full of surprises, not least of them triplets.",

    # 10.0M    Bride of Vengeance
    'bride-of-vengeance':
        "She found out about the cheating the day before the wedding. She kept the wedding anyway.\nTalia Stone is a billionaire's daughter with three powerful brothers, one in the military, one in show business and one in finance. She nearly lost her legs saving her childhood friend Jack Chase in an accident, and even after top doctors saved them she stayed in a wheelchair because her father asked her to, as a way of finding out how Jack really felt. Then, with the wedding one day away, she learns Jack has been sleeping with her friend Rachel. They deny it to her face, so she plays along while planning to humiliate them both at the ceremony. When a man named Aiden Brooks chases down a thief and brings back her purse, she half jokingly asks him to marry her. He says yes. The wedding is about to become a show nobody forgets.",

    # 14.8M    The Bride of the Wolf King
    'the-bride-of-the-wolf-king':
        "Centuries ago the Wolf King lost the woman he loved. He's found her again.\nA struggle over power and desire cost him the one woman he loved most, and the grief was so deep he sealed away his own memory. Hundreds of years later they cross paths again, and everything left unfinished from their past life starts coming back. This time he swears nobody will stand between them, and anyone who tries will die.",

    # 11.5M    Pampered by My Silver Fox Uncle
    'pampered-by-my-silver-fox-uncle':
        'A princess wakes up in the body of a neglected eight year old.\nOn the day she comes of age, Princess Lia Torres of the Phoen Dynasty finds her soul pulled into the modern world and into the body of a little girl. That girl never got any love, because an imposter daughter took it all, and she died from the neglect. Furious at what was done to her, Lia takes over her life, along with a father everyone else looks down on.',

    # 12.5M    My Rise To Power After She Left
    'my-rise-to-power-after-she-left':
        "His wife took everything. Then he inherited powers nobody knew existed.\nLennox Hayes is betrayed by his wife Yvonne and left with nothing, and then he suddenly inherits ancient powers that change the course of his life. Amelia Langford, heiress to Grimwood's powerful Langford family, tells him they were engaged long ago. Now he has to find his way through a dangerous new world of cultivation and plotting, from the streets of Riverain all the way up to Grimwood's elite, and show that a man who was broken can still come out on top.",

    # 11.4M    Divorced, Devoted & Dominating
    'divorced-devoted-dominating':
        "She was made to wait on her husband's mistress. Then she took her patents back.\nJocelyn walked away from a career in tech to be a wife, and her husband betrayed her and forced her to serve his mistress. So she divorces him, reclaims her patents and sinks his company overnight. Then she has a flash marriage with Steven, the man who used to be her rival, goes back to tech and climbs higher than she ever did before. Her ex is left with nothing.",

    # 13.5M    Her Turn to Fall
    'her-turn-to-fall':
        "He made her a business queen. She betrayed him.\nMiles gave his whole life to turning Wendy into a queen of business, and in the end she betrayed him and he was killed. Wendy was sure she could have had the perfect life with charming Jack instead. When Miles gets a second chance he drops Wendy and goes after someone else. But Wendy is reborn too, certain her success never had anything to do with Miles. This time around Miles doesn't revolve around her, he has someone new, and charming Jack is a scumbag after all. Now it's her turn to fall.",

    # 11.4M    Hey Mommy! Time for a New Daddy!
    'hey-mommy-time-for-a-new-daddy':
        'Five years old again, with one job: protect her mom.\nTalia is reborn as a five year old, and all she cares about is keeping her mother safe. Her charm and her hidden talents win over powerful elders and quiet everyone who doubted her. With a tycoon for a father, a stepfather who is even richer, and a future billionaire husband waiting down the line, she grows up the darling of the whole family. The littlest one in the house ends up shining brightest.',

    # 12.3M    My Fiancé, My Bodyguard
    'my-fiance-my-bodyguard':
        "He wanted peace. A routine security check blew his cover.\nFinn is a soldier hardened by war who just wants a quiet life, until a routine security check reveals who he really is and drags him back into action. He's engaged to Josephine, daughter of the Sinclair family, and he quickly sees she's surrounded by danger. He uses everything he knows to keep her safe and gets pulled into a much bigger conspiracy. One threat after another, he outthinks them all and turns the tables.",

    # 13.4M    Fool No More, King Returns
    'fool-no-more-king-returns':
        'Three years in a daze. He woke up immortal.\nHolden Stone comes out of a three year daze with immortal powers. He can heal like a god and he knows martial arts, and he takes the city by storm. With it comes supreme power, friends who stay loyal, and romance.',

    # 14.1M    X-Ray Eyes, Billionaire Rise
    'x-ray-eyes-billionaire-rise':
        "Hit by the campus queen, he gets up with X ray vision.\nLincoln Cross is a broke student until Audrey Sterling, the campus queen, hits him, and he comes away with astonishing X ray vision. Suddenly gang heiress Vera Blackwood, the gorgeous sisters Blair Leighton and Amber Collins, and elegant Audrey herself are all falling for him, and every one of them can see he's worth a fortune. Based on a hit web novel.",

    # 10.1M    The Immortal's Return
    'the-immortal-s-return':
        'An unbeatable Grandmaster comes down to the mortal world.\nArthur is a Grandmaster no one can defeat, and he steps down into the world of mortals. He and his childhood sweetheart fall hard for each other, while a martial arts goddess and a wealthy heiress fall for him too. Pulled into the brutal fight for control of Meridian, he crushes every rival in his way on the road to the throne at the very top.',

    # 11.8M    Draft Dreams
    'draft-dreams':
        "Relatives who stole his mom's medical money. A basketball and nothing else.\nGrowing up on Drywell's rough streets, he takes every insult from relatives who look down on him, even after they steal the money meant for his mother's treatment. Basketball is the only weapon he has, and every bruise on his hands is proof he won't quit. When a real shot at changing their lives finally comes, it's about much more than a game. It's his chance to show everyone who wrote them off that something grown in the cracks can still push through and reach the light.",

    # 11.3M    Destroy My Silver Wolf Bloodline？I'll Marry a Top Alpha Then
    'destroy-my-silver-wolf-bloodline-i-ll-marry-a-top-alpha-then':
        'Six years of devotion, and on the eve of the wedding his deputy shaved off her silver hair.\nNatalie is heir to the Warwick silver wolf bloodline, with the power to call down moonlight and protect her pack. She gives six years to Alpha Liam, and the night before their wedding his deputy Zoe cuts off her sacred silver hair and drugs her to drain her strength. Liam knows all of it and lets it happen. In her despair Natalie wakes the true mate bond she buried long ago, and it calls Nicholas, the most powerful Alpha of them all, who has been waiting for her for years. He brings the full weight of his clan down on the traitors and helps her get her strength and pride back. She leaves Liam behind, marries Nicholas, and goes from humiliated fiancee to Luna of the Lycan Clan.',

    # 2.0M    I'll Steal You Back
    'i-ll-steal-you-back':
        "She left him to save him. He came back a billionaire.\nEmily's boyfriend Daniel is sick, so she marries wealthy James for the money to save him and tells Daniel she left because she was greedy. Three years later Daniel is back and he's a billionaire. He sets out to get close to her, works on James until she ends up as Daniel's personal assistant, and pulls her into an affair driven by lust that wrecks everything it touches.",

    # 12.7M    The True Alpha Princess
    'the-true-alpha-princess':
        "The real Alpha Princess walks into school. Someone is already pretending to be her.\nVivian is the true Alpha Princess, but when her newly awakened wolf powers get out of hand she hides who she is and switches schools. On her very first day she meets a girl who is using her identity. The fake princess leans on privileges she doesn't have to bully Vivian and even tries to take her fiance Seth. Vivian finally unmasks her in front of everyone, and the impostor gets exactly what's coming to her.",

    # 11.8M    Don’t Mess with My Lethal Fiancée
    'dont-mess-with-my-lethal-fiancee':
        "He doesn't recognize her. She's his fiancee and the woman from that night.\nScarlett is on the run when she spends one night with Landon, a wealthy heir, and then vanishes. Later her mentor asks her to come back as his grandson's fiancee and turn him into an heir worth the name. She never imagined the grandson would be Landon. He has no idea his new fiancee is the mysterious woman he can't forget, and because he hates his grandmother's arrangement he treats Scarlett like an enemy. Living together under a false identity, they keep pushing each other away and keep getting pulled back.",

    # 14.0M    The Simp Claps Back
    'the-simp-claps-back':
        "He made her queen of Wall Street. She pushed him off a roof at their wedding.\nLeo built Maisie into a Wall Street queen, and at their wedding she and Brad pushed him off a roof. When he opens his eyes he's reborn back in college. This time he swears he's living for himself and he's done being Maisie's simp. He even finds someone new, the young heiress of the Hale family. Maisie is about to find out what she threw away.",

    # 13.3M    My S Rank Beast Mate
    'my-s-rank-beast-mate':
        "Her sister stole the husband from her last life. She took the lion nobody wanted.\nShe's reborn on the day she chooses her beast mate, just after her jealous sister Lyra grabs Voss, the B rank snake she married in her past life. Lyra frames her and gets her exiled into the deadly wilds, where she saves a wounded white lion no clan would take in. Everyone mocks him as rankless trash until she gives birth to two S rank lion cubs. The priest discovers the S rank blood hidden in him and names her the reborn Sacred Daughter. Lyra's dream of being a saint falls apart when her own cubs turn out to be weak snakes, and still she screams that her glory was stolen. After everything Lyra has done, who's going to pay?",

    # 11.6M    The Alpha Rejected Me, But the Dragon King Claimed Me
    'the-alpha-rejected-me-but-the-dragon-king-claimed-me':
        "Rejected at her own wedding. Fifteen years later she comes back an Empress.\nOn her wedding day Selene is framed. The Alpha King rejects her, she loses her crest, and her own mother sends her into exile. Everyone believes the cursed girl with silver eyes is gone for good. Fifteen years later she returns as Empress of the Sacred Dominion, ruling from a throne of dragon bone over the richest crystal mines on the continent. Then her adopted son brings home a girl whose mother is the woman who took Selene's life from her, and Selene has no intention of forgiving. Her old enemies close in and the lies they buried start coming out, and one by one the people who betrayed her learn that the girl they broke is now a queen they should be afraid of.",

    # 14.4M    He Pulled a Prank on Me and Lost Everything
    'he-pulled-a-prank-on-me-and-lost-everything':
        "He tied her to the goalpost to impress another girl.\nEleanor Vance's childhood best friend Leo ties her to the school goalpost as a joke, all to show off for another girl. She transfers to a high school in California and starts again. While she heals, does brilliantly in class and falls for someone new, Leo sinks deeper into regret. But some betrayals can't be taken back.",

    # 7.8M    The Mafia Boss My Husband Betrayed
    'the-mafia-boss-my-husband-betrayed':
        "Her husband's mafia boss is hiding in her house. Her husband is on video call.\nEmma is home alone with a crying baby and a painful blocked milk duct after her husband leaves on a job for the mafia. Then Dante Vella, the boss her husband works for, breaks in wounded, hiding from the men trying to kill him. To keep the baby quiet she has to let him help ease her pain, and his steady hands and how close he is stir feelings she shouldn't have. When her husband video calls, Dante stays just out of frame and his hand drifts lower. Her husband talks about hunting Dante down for the bounty, and Emma realizes the real danger isn't outside the door anymore.",

    # 8.2M    The Boy the QB Used in Bed
    'the-boy-the-qb-used-in-bed':
        "Six months as the quarterback's secret. Then the hockey captain held his hand in public.\nAsher has been seeing QB Chase in secret for six months, while in public Chase plays the perfect boyfriend to Asher's sister Daisy. Then a naked photo of Asher spreads across campus, one Daisy took from Chase's phone, and Chase tells Asher to keep quiet and goes on using him. Hockey captain Finn opens Instagram in front of everyone and asks Asher out, on the condition that he follows him first. The next day Finn walks the hallway holding Asher's hand for the whole school to see. Daisy pretends to have a nut allergy attack and blames Asher, and Asher pushes her face first into a fountain. Chase loses his game and melts down at Daisy on the sideline. Finn wins his, looks into the camera and makes it clear he's done letting Asher carry things alone.",

    # 12.6M    You Betrayed the Wrong Alpha Queen
    'you-betrayed-the-wrong-alpha-queen':
        "She gave up her wolf to be with him. He made her his slave.\nRavena Mooncrest is secretly the Wolf Queen, and she has her wolf sealed away so she can run off with her fated mate, Alpha Draven Nightfang. Then Draven sees the birthmark on their son, decides it means she cheated on him, and makes Ravena and the boy his slaves. It takes their son's life being in danger before Draven has any chance of learning the truth. But by then, will it be too late?",

    # 10.7M    The Mob Boss Demands Her Perfect Genes
    'the-mob-boss-demands-her-perfect-genes':
        "He wants her eggs for his heir. She wants nothing to do with him.\nChristine is an elite doctor, and mafia boss Damon has his eye on her because her eggs are the best there are and he wants an heir. She can't stand him, because his mob is the reason her mother took her own life. She rushes into a wedding to get away from him, but Damon storms the ceremony and carries her off. Locked in his penthouse, he comes for her every night and she fights back twice as hard. Slowly she sees what's under the ice, and when someone drugs her Damon burns everything down to get her back. His twisted, obsessive devotion is what finally breaks through, and Christine lets the grudge go.",

    # 11.6M    A Birthmark Exposed My Husband’s Secret
    'a-birthmark-exposed-my-husband-s-secret':
        "One tiny birthmark and she wants a divorce.\nVivienne and Adrian are about to adopt a sweet little girl when Vivienne spots a birthmark the size of a pea on the child's hand. She refuses to sign on the spot and asks for a divorce. Adrian gets down on his knees, his family calls her cruel, barren and heartless, and even the little girl begs her to stay. Nobody can understand why she would end a loving marriage over a mark that small, and she won't tell them. Not until she stands up at a live press conference with three reports in her hand does the truth start coming out.",

    # 11.0M    My Husband Gifted Me His Rival
    'my-husband-gifted-me-his-rival':
        "Every time he cheated, he gave her another man to make up for it.\nFor three years Elena lived in a marriage where each of her husband's affairs ended the same way, with him handing her a new man as compensation. When his pregnant mistress demands a wedding, Damian expects another fake divorce followed by Elena coming back like she always does. This time she takes the young man he picked for her, signs the papers and leaves for good. By the time Damian learns the truth about the betrayal that ended their marriage, she's already at another altar, and she doesn't look back.",

    # 4.5M    Abyssal Throne：The Godslayer
    'abyssal-throne-the-godslayer':
        "Betrayed by the woman he loved and cast out. He came back a Demon Lord.\nKaelen is a fallen noble, betrayed by his beloved and driven out by humanity, and in the lightless depths of the abyss he awakens the bloodline of the Abyssal Demon Lord. With a cursed serpent woman at his side, he swears to tear down the false gods and share the sun among every race. In this world light belongs to the powerful. Human nobles drain their own people's blood to fuel the gods' blessing and crush anyone who objects, while demons and beast tribes are kept from the sun and hunted. When the magic altar falls, the barrier holding the beast tribes breaks, tens of thousands of starving warriors pour into human lands, and war swallows humans, demons, beasts and gods alike. Kaelen has to unite his enemies and break the gods' hold on the light.",

    # 13.2M    Tide of Forbidden Touch
    'tide-of-forbidden-touch':
        'Her honeymoon surf lesson came from her father in law.\nEmma is on her honeymoon in Hawaii when her new husband Jack sets up surf lessons for her with his father Victor. Jack drives the motorboat out in front while Victor shares a board with Emma, holding her tight from behind. Out in the rough waves his secret desire keeps building until neither of them can stop it, and Emma and Victor begin a forbidden affair.',

    # 7.9M    Big Molly The Billionaire's Only Cure
    'big-molly-the-billionaire-s-only-cure':
        "The billionaire heir can't eat. Then he tries her hot dog.\nMolly Hart runs a food truck called Big Molly's Hot Dogs with her adoptive parents. People make jokes about the name and about Molly herself, and she just makes it part of the brand. Adrian Blackwood, the heir to his family's empire, hasn't been able to eat in days, and no doctor, private chef or nutritionist his money can hire has been able to help. Then Charles brings one of Molly's hot dogs back to the estate, and for the first time in days Adrian actually wants a bite. He starts getting better right away. Once he finds out it came from Molly Hart's food truck, he goes looking for her. What starts with food, money and a very strange arrangement turns into real love, and neither of them can let go.",

    # 10.2M    Shh, Don't Let Him Find Out
    'shh-don-t-let-him-find-out':
        "The mafia godfather who saved her is her father in law.\nLena has been secretly married to Isaac for a year and believes it was for love. She has no idea she's just a pawn he's using to satisfy a family rule and qualify for his inheritance. Then Isaac's debts hand her over to loan sharks. One stormy night, drugged and fighting for her life, she escapes and is rescued by Jack Kane, the most feared mafia godfather on the West Coast and the CEO of an empire worth billions. The man watching her with obsessive hunger is her husband's father.",

    # 405.9K    Her Dream of Marrying Rich Turned Deadly
    'her-dream-of-marrying-rich-turned-deadly':
        "She wanted to marry into the family. She destroyed the kidney that could save its patriarch.\nDr Miles Hill is flying a kidney to the Zeller family, the transplant that is the patriarch's only hope, when Jane and her mother sabotage the delivery and the organ is ruined. Without it the head of the Zeller family has no chance of surviving. Jane had dreamed of marrying into their money, and her plan blows up in her face, taking every hope of wealth and status with it overnight.",

    # 699.8K    American Magician: The Last Encore
    'american-magician-the-last-encore':
        "The janitor at her failing theater might be the missing King of Magic.\nSilas was the greatest magician in the world, a masked vigilante known as the King of Magic, until an assassin's bullet meant for him killed his mentor. He vowed to disappear and watch over his mentor's daughter Lyra. Now he's hiding as the janitor at her struggling theater, quietly guarding her and her little girl. Then her cruel ex and her greedy uncle, along with a stream of elite magicians, come to take everything she has, forcing her into magic duels where losing means death. One by one Silas steps out of the shadows, and people start to whisper.",

    # 618.5K    The Sun God’s Beloved
    'the-sun-god-s-beloved':
        "Her mother made her seduce a god for gold. She ran at dawn carrying his child.\nKallydia is head priestess of the Temple of Philotia, and her own mother uses her, pushing her to seduce the Sun God Helios for gold coins. An enchanted incense leads to a night with him, and she slips away at dawn leaving only a silver armband with her name on it. Helios had come to care for her, but a misunderstanding convinces him she's a social climber who plays with men, and in his anger he cuts her off. Then Kallydia finds out she's pregnant. On her own, she protects the faint golden light inside her through public humiliation and her family's cruelty. When the God of War and the Goddess of Wisdom arrive, they reveal that the gentle maidservant they remember and the woman Helios called bad are the same person. By the time Helios gets to her, she has been tortured and thrown into a pit of snakes, and with her last breath she begs the gods to protect her child.",

    # 7.9M    You Ignored My Birthday So I Erased Myself From The Family
    'you-ignored-my-birthday-so-i-erased-myself-from-the-family':
        "Everyone in the family gets a birthday except her.\nHer brother Ethan's birthday means a steakhouse booked a month in advance. Her sister Chloe's means Six Flags and a string of photos on Mom's Instagram. Hers is July 19th, in the middle of summer, and nobody ever remembers it. On her eighteenth she gets up early, does her makeup and waits on the couch. Mom walks past on her way to take Chloe to dance, and Dad heads out with Ethan to play ball. She texts the family group chat that she's eighteen today and nobody answers. They come home that night with food for Ethan and Chloe, without a cake, a candle or a single song, and nobody notices anything is missing. But she's eighteen now, and she gets to decide where she goes next.",

    # 3.2M    Becoming the Heirless Dragon King's Fated Mate
    'becoming-the-heirless-dragon-king-s-fated-mate':
        "Sold to a violent old man, she ran into a cave and found a dragon.\nLaura is sold off to a brutal old man and escapes into a cave, where she forms a bond with Kyle, a silver dragon duke, and ends up carrying his heir. They marry for the baby's sake and then fall in love for real. Through rival schemes and attempts on her life, Laura discovers she's a gifted runemaster, gives birth to twins, founds an academy and takes her place beside Kyle as his equal.",

    # 1.5M    I Signed My Divorce Papers on the Operating Table
    'i-signed-my-divorce-papers-on-the-operating-table':
        "She was dying in childbirth. Her husband was outside another woman's delivery room.\nA hard labor nearly kills her, and while it's happening her husband is waiting outside the delivery room of his subordinate's widow. So she signs the divorce papers and walks out without a second thought. Now he's the one left with regret, and everyone around him has walked away.",

    # 9.9M    Dragonblood Alpha
    'dragonblood-alpha':
        "Abandoned as a baby for having no wolf. Raised by legends, he woke a dragon.\nKyle was left behind as an infant because he had no wolf spirit, and three Legendary Beasts raised him in the Beast Forest. Eighteen years later he's a fierce fighter, and the power of a dragon has woken inside him. Looking for his parents, he rescues Freya, Princess of the Silvermoon Pack, and follows her to Crimson Flame City, where he learns that Elina, a disgraced slave abused by the two faced Alpha Alaric, is his real mother. They've only just found each other when the Thunderclaw Pack invades. Alaric and his cowardly heir Kent surrender and hand Freya over to save themselves, but Kyle stands his ground and uses his dragon and wolf blood to crush the invaders. Behind it all the Thunderclaw Pack has joined the Liches, an undead race set on ending the world. Against the Lich King and his endless ghouls, with Freya's holy light and every werewolf in the world behind him, Kyle becomes a giant silver wolf and wins. His father, the ancient dragon Vodar, wakes from his long sleep, and Kyle takes his place as Alpha of the Crimson Flame Pack with Freya at his side.",

    # 643.3K    My X-Ray Eyes Rule the City
    'my-x-ray-eyes-rule-the-city':
        "He tries to save his fiancee. She thinks he's a creep.\nLeo Banks has a special physique and X ray eyes. When he leaves his sect and runs into his fiancee, he tries to save her and she takes him for a creep. Now he has to prove himself by taking over the city, and he plans to enjoy every carefree minute of it.",

    # 548.9K    Agent Badboy
    'agent-badboy':
        "An FBI agent goes undercover as the dead mafia boss who shares his face.\nTop FBI agent Buddy is the double of Barton, the late head of the Logut mafia family, so he takes Barton's place to expose the family's arms smuggling. Inside he survives Luca's grabs for power and questions from Barton's stepmother Susanna, and the crescent birthmark he shares with Barton keeps him from being found out. He falls for Barton's wife Elise, wins over the bodyguard Haruko and takes control of the San Francisco docks. With the evidence in hand he and FBI Deputy Director Helena plan the final raid, but FBI Director Burke is the mafia's deepest mole. Burke and the Raine family spring a trap and Helena is shot. Buddy kills Burke and Carlos in the fight, and as he dies Burke reveals that Buddy and Barton are twins, stolen as babies and raised to be the mafia's man inside the FBI. Caught between two bloodlines, Buddy stands with Elise, Susanna and Haruko, while Helena, thought dead, moves her fingers.",

    # 4.9M    GODFORGED: TEN SCRAPS OF IRON
    'godforged-ten-scraps-of-iron':
        "They stole his masterpiece and paid him ten scraps of rusted iron.\nPyrrhos works the hammer at Hermon's Forge, and they call him Emberless because the forge fire means nothing to him, and a real smith is supposed to feel it. For a thousand nights he has made the runeblades that bring down dragons and hydras all over the continent. On Assessment Day the guild crowns his senior brother Deryk for a masterpiece called Firstlight, a sword Pyrrhos designed and spent three years on before his name was scraped off the plans. When he asks for his wages and quits, his master dumps ten rusted scraps on the anvil. Then a thread of pure gold flame rises by itself from the dying furnace behind him. With those scraps, a girl with her family's broken sword, a back room rented from a landlord and a wartime order nobody else will take, he builds a forge from nothing and starts exposing the guild's fake runes one blade at a time. That gold fire is no accident. It answers to a bloodline that goes back to Hephaestus himself, and to a father who chose to die in his burning workshop instead of handing over the Godslayer plans. Delphi already has a name ready for him, but he'd rather earn one.",

    # 8.9M    The Alpha's Broken Mate
    'the-alpha-s-broken-mate':
        "She went to prison for her sister. Her mate held her sister while she lost their baby.\nHer whole family made her take the fall for her adopted sister, and her Alpha told her seven years would fly by. While she sat in prison and lost the baby she was carrying, her mate was holding her sister and telling her he loved her. When she got out she cut their soul bond herself and left for the war zone. Later, full of regret, he grabbed hold of her boots and cried out for his Luna. With her hand on her very pregnant belly, she told him she was sorry, but the baby was his older brother's.",

    # 10.4M    The Dragon Queen's Gambit
    'the-dragon-queen-s-gambit':
        "Her consort and her maid swapped her newborn for their son. She waited twenty years.\nDragon Queen Evelyn finds out that her consort Cyril and her handmaid Cecilia, serpent shifters both, switched her newborn daughter for their own son. In secret she raises her daughter Ann to become queen of an empire in the north. After twenty years of quiet endurance she gives up the throne and goes into exile. Then Ann marries the fake prince and the trap closes: the truth comes out, the family's fortune collapses, and the Millennium Dragon Aurelius arrives as Ann's real father. The traitors lose everything, and Evelyn gets her family back.",

    # 2.8M    Tenth Wedding, New Groom
    'tenth-wedding-new-groom':
        "Jilted at her tenth wedding, and replaced by a police dog.\nBrigid Hayes is abandoned at her tenth wedding, and her fiance insults her by swapping her out for a police dog. On the spot she marries Marco Romano, a powerful billionaire. Her toxic ex and his scheming assistant have no idea who she's married now, and they attack her and frame her. Marco hits back fast, digs up their corruption and leaves them ruined in public and in court. As the people who tormented her fall apart, Brigid finds out Marco's devotion comes from a past they share.",

    # 2.5M    The Unbreakables: Super Son Returns
    'the-unbreakables-super-son-returns':
        "Taken at seven. Raised by the villain who kidnapped him.\nKit disappears at seven during a robot attack and grows up as Ash, raised by the kidnapper Voltage. Years later Ash slips into his own family's tryouts, where he's framed by Spark, Voltage's son and the boy he calls brother. His birthmark almost shows, Aura's instincts close in on the truth, and his father doesn't trust him, until Spark burns the mark off. When Voltage claims Ash in public the family goes to war. Ash proves whose blood he carries and helps them get out, and at the crater his memory comes back and he takes back the name Kit Unbreakable. What Spark did to him is still waiting to be settled.",

    # 767.2K    After My Three Alpha Childhood Sweethearts Abandoned Me, They Regretted It
    'after-my-three-alpha-childhood-sweethearts-abandoned-me-they-regretted-it':
        'Her three Alpha childhood sweethearts tortured her over a lie.\nEileen is an orphan who saved the headmaster of Hatton Academy and was adopted, and she grew up alongside three Alphas who were her childhood sweethearts. Then Chloe frames her with forged notes, and the three of them refuse to believe her. They hurt her with hockey pucks, drag her behind a horse and hang her from a flagpole. Something in her dies, and she chooses Bruno, a fallen Alpha, instead. When the truth comes out they are crushed by regret and give up their Alpha blood to save her. She never looks back. She bonds with Bruno and marries him.',

    # 1.5M    Marked by the Wolf King, I Return With My Fierce Cub
    'marked-by-the-wolf-king-i-return-with-my-fierce-cub':
        "One full moon night with the Wolf King. She left carrying his heir.\nUnder a full moon the Werewolf King Cain loses control and sleeps with a human girl named Jenny. She leaves without knowing she's carrying his heir. She fights to keep the pregnancy safe while her father ignores her, her stepmother is cruel to her and her greedy little brother makes things worse, and her son Sammy, half wolf and half human, is born early. To pay the huge hospital bills she works odd jobs by day and sells drinks in nightclubs at night, humiliated at every turn. Then, at her lowest, she meets Cain again. Together they grow through power struggles and family plots, protecting a love that crosses the line between their kinds.",

    # 3.1M    Five Years of Secret Love, He Married My Best Friend
    'five-years-of-secret-love-he-married-my-best-friend':
        "Five years as his secret. Now he's marrying her best friend.\nFor five years Harper has been in a secret relationship with Alpha Connor, waiting for him to go public and stand with her under the Moon Goddess at the wolf clan's sacred moon vow. But she finds out he's about to take that vow with Maddie, who has been her best friend for over a decade. Connor says it's only practical. Maddie's father is gravely ill, and registering as her mate gets him the pack medical benefits he needs. He begs Harper to understand, while playing the perfect fiance in Maddie's home. All the holidays he said he was working, he was with Maddie. Together they push Harper into being Maddie's maid of honor, using small town gossip to keep her quiet. On the day of the vow, Harrison of the Blackstone Pack, Connor's biggest rival in business, crashes the ceremony and exposes him. To protect her family from the rumors, Harper announces in front of everyone that Harrison is her boyfriend, and he slips straight into the role of fake boyfriend. Connor is wrecked with regret and becomes obsessed with getting her back, and Maddie finally admits she has always resented living in Harper's shadow. Harper turns her back on both of them and walks into a new life.",

    # 1.2M    The Nether King's Bride
    'the-nether-king-s-bride':
        "Chosen by prophecy to bear Hades a child, or die.\nTyphon was sealed beneath Mount Etna after he attacked Olympus, and every six hundred years the seal weakens. With the Age of Gods ending, Hades no longer has the power to hold it. The Prophecy Stone says only a divine heir, born to Hades and a mortal woman with witch blood and eyes of two different colors, can make the seal last forever. In the mortal world Saintess Layra is blamed for the volcano's disasters and almost burned alive, until Hades saves her and takes her to the Underworld. The Stone has chosen her as his bride, and she must have his child or die. Bound by the Serpent Soul Pact she fights it at first, but his care and protection slowly bring her round. Minthe, who loves Hades, torments her out of jealousy, and Nyx, Goddess of Night, locks her up and claims she carries a God Devouring Curse. Heartbroken, Layra tries to escape through the Well of Reincarnation, and Hades stops her and tells her he loves her. She falls pregnant, and he grows weaker and starts avoiding her. Then Alector, the high priest who raised her, lures her back to the mortal world and takes her, because he has found out about her witch blood and has plans of his own.",

    # 2.2M    Run, Mommy! Daddy Is Coming!
    'run-mommy-daddy-is-coming':
        'Five years after one night with a CEO, their son finds his father.\nFive years ago actress Lily and CEO Liam had a one night stand, and since coming home she has raised their son Leo on her own. Then Leo happens to recognize his real father, and a DNA test proves it. Lily and Liam sign a contract for a secret marriage. While she fights her way through show business, dealing with rumors, rivals, the attention of movie star Mason and the hostility of actress Lucy, Liam quietly clears her troubles away and starts falling for her. With their clever little boy playing matchmaker, the fake couple starts to feel something real.',

    # 2.1M    Five Winters With Her, Five Fridge Magnets for Me
    'five-winters-with-her-five-fridge-magnets-for-me':
        'He spent five winters in Japan with his first love. He brought her fridge magnets.\nMaya cancels the condo she decorated by herself and leaves her fiance Ryan. For five winters he went to Japan with Hannah, his first love, and bought her custom jewelry, while all Maya ever got was a fridge magnet. She moves to a new city and starts over, ignoring his late apologies and the list of 47 promises he broke. He signs the papers ending it and sends her things back, with one last magnet he picked out himself. Maya keeps it, buys herself her favorite flowers, closes her eyes, and stops waiting.',

    # 7.7M    The Cartel’s Contract Bride
    'the-cartel-s-contract-bride':
        "Sold on her wedding day to pay her fiance's gambling debts.\nEmma is a kindergarten teacher, and on her wedding day her fiance Kyle, buried in gambling debts, sells her to Santiago, the man in charge of a border gang. She's forced into a one year contract marriage and made nanny to his niece Sofia, who stopped speaking after losing her family. As Emma learns to survive in his dangerous world she helps the little girl heal, and she and Santiago slowly fall for each other through one crisis after another. His rival Valentina, his ambitious brother Nacho and his deadly enemy Emilio all come for them, and Emma stops being fragile, learns to shoot to protect herself, and fights beside Santiago to bring their enemies down. Together they break the contract and build a real family.",

    # 1.6M    Eight Heirs for the Dragon King
    'eight-heirs-for-the-dragon-king':
        "He rejected her for her sister. His older brother didn't make that mistake.\nIn their past life Lora's younger sister Selena gave birth to a dragon egg, so William publicly rejects Lora and picks Selena. They have both been reborn, and William blames Lora for never giving him a pureblood dragon heir. His older brother Asher is the one who saves her and treasures her. Together they fight off the schemes of the royal court, and Lora is carrying the pureblood heir William always wanted. It's Asher's.",

    # 444.7K    Bound by Hatred
    'bound-by-hatred':
        "She wants out of the mafia. They marry her to a killer.\nShe's a rebellious mafia daughter who wants nothing more than to be free of that life. Then she's forced to marry a mafia killer who is possessive to the extreme, and he's the one thing standing between her and her freedom.",

    # 479.8K    Dream On
    'dream-on':
        "Hollywood's biggest star wants her as his fake girlfriend. He's also her ex.\nLexington Hall is the biggest movie star around, and when he asks Stevie to be his fake girlfriend it ought to be her Hollywood dream coming true. Except he's the ex who broke her heart. Is this the dream, or her worst nightmare?",

    # 11.6M    Married Off To The Cursed Alpha Daddy
    'married-off-to-the-cursed-alpha-daddy':
        "Married off to a broke, cursed Alpha. He's not what they think.\nMeara's stepmother and half sister are cruel to her, and they hand her over in marriage to Damian, a poor Alpha under a curse and a single father to his disabled daughter Sierra. With no wolf and stuck up in the mountains, Meara struggles just to get by, especially with Violet, a woman in the pack who wants Damian for herself. As Violet schemes to destroy her, Meara fights to protect her new family and get her wolf back. But nobody has Damian right. He's no weak, cursed Alpha. Her fated mate is the Supreme Alpha himself.",

    # 650.2K    At the Mercy of My Vampire Ex
    'at-the-mercy-of-my-vampire-ex':
        "She pushed him into the rain so he'd hate her enough to live.\nThree years ago she shoved her husband out into the rain, making him hate her so he would survive. Three years later she runs into the Underground Blood City to escape, and finds out the man who rules it is him. The husband she supposedly killed is now a vampire godfather. He keeps her at his side, punishes her with his hatred and binds her with a blood oath, until he learns the truth. She didn't betray him at all. Leaving was the only way to keep him alive.",

    # 938.7K    The Dragon King's Slave Mate
    'the-dragon-king-s-slave-mate':
        "His touch marked her as his mate. He hid it behind a slave collar.\nSaria is an abused village girl when Dragon King Alarik takes her, and his touch sets off a Mark that has never happened before, binding them as mates. Alarik hides the bond under a slave collar. With Xander suspicious and Celeste scheming, Saria survives a slave hunt and learns she can bend dragon fire. Then Alarik tells her about his death curse. He has one month to live. When Xander exposes the Mark and attacks, Saria turns blue fire on him and destroys him. Their first kiss seals the bond, but Celeste offers to keep quiet, and she hasn't named her price.",

    # 1.5M    The Husband She Took for Granted
    'the-husband-she-took-for-granted':
        'He gave up science for their baby. She had an abortion for her business partner.\nA brilliant scientist walks away from his career to stay home with their baby, then learns his wife ended a pregnancy so she could save her business partner. He finally files for divorce and goes back to his work. Now his wife, who took him for granted all along, regrets every bit of it.',

    # 16.8M    The Triplets' Final Regret
    'the-triplets-final-regret':
        "She'd have become human for them. They kept choosing the maid's daughter.\nElisa is half human, half vampire, and she believes the Lockhart triplets are the only people she can really trust. She wants to become human for them and spend forever with one of them. Then Amber, the maid's daughter, shows up. Over and over Elisa is left behind, humiliated and robbed of her dignity, all for Amber. Finally she lets go and accepts what she is. She leaves day school, moves to night school and becomes a vampire. So when she walks in wearing her night school uniform, in the arms of a powerful vampire heir, why are the triplets who tossed her aside suddenly on their knees begging her to forgive them?",

    # 1.1M    LadyAid: From Dumped Pauper to Tycoon
    'ladyaid-from-dumped-pauper-to-tycoon':
        "Dumped for being broke. Then he got a system that makes him rich for helping women.\nCole Preston's greedy girlfriend dumps him, and then he awakens the LadyAid System, which makes him enormously rich every time he helps a woman. He climbs from nowhere to hidden billionaire, builds a huge empire and gets tangled up with a string of powerful women. When his ex starts a smear campaign against him, his allies expose her lies and she ends up arrested. With his enemies beaten, Cole stands at the very top of wealth and power.",

    # 988.7K    The Last Daughter of House Vale
    'the-last-daughter-of-house-vale':
        "Scarred with poisoned silver by the man she came to marry.\nSeraphina is House Vale's hidden pureblood heir, and she comes back to honor an arranged marriage. Her fiance Damian and his vicious foster sister humiliate her in public and scar her with poisoned silver. What they don't know is that Damian's family owes its whole empire to Seraphina's mother, who arrives and crushes them. Seraphina scars the wicked woman right back, then locks them both into an eternal blood oath that means they'll make each other suffer forever, until there's nothing left of them but ash.",
}
