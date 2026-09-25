# -*- coding: utf-8 -*-
"""Rewrite batch r0, 25 Sep 2026: the top 25 by reach still showing platform
text or no caption at all (19 live copies, 6 blank). All rank inside the top 300,
so this batch is UNAPPROVED until Cyan reviews it.

Facts: every title fetched live from its ReelShort page on 25 Sep (full
special_desc, not the truncated stub on disk), banked in
staging/facts_r0_2026-09-25.json and repeated in FACTS below.
"""

CAPTIONS = {

    # You've Been Replaced, First Love
    # FACTS: To Jason, Tessa was only a disposable practice run for the girl he actually wanted. After 
    # FACTS: the blood on the sheets became a public trophy and her dignity a ghost, young Tessa finall
    # FACTS: y stops trying to mend the shards. She is done with her first love. She is leaving him beh
    # FACTS: ind for a future that doesn't taste like salt and shame. But at the edge of the wreckage s
    # FACTS: tands the one person who shouldn’t be there: another boy with no intention of letting her 
    # FACTS: go alone.
    'you-ve-been-replaced-first-love':
        "She was only ever his practice run.\nTessa gave her first love everything she had, and to Jason she was never more than a rehearsal for the girl he really wanted. When he brags about their first night to everyone, she's left humiliated. So Tessa stops trying to glue the pieces back together. She's finished with him and walking toward a future where she doesn't have to feel ashamed. But she isn't walking alone. Another boy is standing right there, and he has no plans to let her go.",

    # The Heiress Blacklisted Her Husband
    # FACTS: Giselle, the Duke's daughter and rightful heiress of the Von Howard's family, married Patr
    # FACTS: ick Hilton three years ago after he saved her life. She secretly helped his company go pub
    # FACTS: lic, but constant harassment from Patrick’s mother and relentless taunts from Becky leave 
    # FACTS: Giselle, now pregnant, feeling hopeless. She decides to divorce Patrick. Despite everythin
    # FACTS: g, Patrick’s heart belongs only to Giselle. After the divorce, he realizes how much he nee
    # FACTS: ds her and begins a long journey to win her back.
    'the-heiress-blacklisted-her-husband':
        "She secretly built his success. His family still treated her like dirt.\nThree years ago Patrick Hilton saved Giselle's life, and she married him. She's the Duke's daughter and the true heiress of the Von Howard family, and she's the one who quietly helped take his company public. At home it's his mother picking on her day after day and Becky mocking her at every turn, until Giselle, pregnant and out of hope, asks for a divorce. Patrick never stopped loving her. It's only once she's gone that he understands how much he needs her, and winning her back is going to be a long road.",

    # Fiancée's Betrayal, Dante's Inferno
    # FACTS: In Fiancée's Betrayal Dante's Inferno movie, Dante Bosch returns home after 3 years in the
    # FACTS:  Marine Raiders on a top secret mission, only to discover not only is his fiancée Lilith p
    # FACTS: regnant with his brother Virgil's baby, but Virgil has also spent all his money. To add in
    # FACTS: sult to injury, his parents take Virgil's side. After suffering betrayals and humiliations
    # FACTS: , Dante exposes Virgil's lies with a video at his wedding.
    'fiancee-s-betrayal-dante-s-inferno':
        "Three years away on a secret mission. He comes home to find it all gone.\nDante Bosch spent three years with the Marine Raiders on an operation he couldn't talk about. When he gets home, his fiancee Lilith is carrying his brother Virgil's baby, and Virgil has burned through every cent Dante had. His own parents take Virgil's side. Dante swallows one humiliation after another, and then he picks his moment. Virgil's wedding day is when the video plays, and everyone finally sees what his brother really is.",

    # Rejecting My Five Female Mates
    # FACTS: Orphaned Caine spent ten years protecting his foster father Alpha's five daughters, believ
    # FACTS: ing they were his destined mates. However, the arrival of Seth, a manipulative rogue wolf,
    # FACTS:  shatters his world. Blinded by Seth's deceit, the five sisters turn against Caine, relent
    # FACTS: lessly humiliating him and stripping away his honor and sacred armor to appease the rogue.
    # FACTS:  Pushed to the brink of despair by the family he once loved, Caine faces a turning point a
    # FACTS: t his Ascension Ceremony. Will the powerful warrior continue to endure their cruel betraya
    # FACTS: l, or will he sever their fated bonds to claim a greater destiny?
    'rejecting-my-five-female-mates':
        "He guarded them for ten years. They chose a rogue over him.\nCaine grew up an orphan in the house of his foster father, the Alpha, and spent a decade protecting the Alpha's five daughters because he believed they were his fated mates. Then Seth turns up. He's a rogue wolf and a liar, and one by one the sisters believe him and turn on Caine. They humiliate him to keep Seth happy, strip him of his honor and take his sacred armor. Caine is at his lowest when his Ascension Ceremony comes around. Does he keep taking it, or does he cut the bond and go after a far bigger destiny?",

    # Faking It with My Ex's Best Friend
    # FACTS: Clara fakes amnesia to test her boyfriend—only to catch him cheating and watch him toss he
    # FACTS: r aside for his best friend, Ethan. Big mistake. For the ultimate payback, Clara starts fa
    # FACTS: ke-dating Ethan to drive her ex insane with jealousy. But what happens when Ethan’s fake k
    # FACTS: isses start to feel dangerously real?
    'faking-it-with-my-ex-s-best-friend':
        "She faked amnesia to test her boyfriend. He failed.\nClara pretends she's lost her memory to see how her boyfriend really feels about her, and what she learns is that he's cheating and more than ready to be rid of her. So Clara turns it around. She starts fake dating his best friend Ethan, and the whole point is to make her ex lose his mind with jealousy. The trouble is that Ethan's kisses are only supposed to be for show, and they're starting to feel like anything but.",

    # Pregnant by the Billionaire
    # FACTS: Mia Harper, down on her luck, marries wealthy CEO Carter Prescott as part of a deal. Their
    # FACTS:  fake marriage soon blossoms into real romance, but their love is tested when Carter's rut
    # FACTS: hless ex, Lily, stops at nothing to win him back. The drama intensifies when Mia discovers
    # FACTS:  she's pregnant with Carter's baby and uncovers the shocking truth that Lily is her long-l
    # FACTS: ost stepsister...
    'pregnant-by-the-billionaire':
        "It started as a deal. It didn't stay one.\nMia Harper is out of luck and out of options when she agrees to marry Carter Prescott, a wealthy CEO, as part of an arrangement. What starts out as a fake marriage turns into the real thing. Then Carter's ex Lily comes back, and she'll do whatever it takes to have him again. Mia learns she's carrying Carter's child, and right behind that comes the real shock. Lily is her long lost stepsister.",

    # Her Billionaire Father Spoils Her Rotten
    # FACTS: In Her Billionaire Father Spoils Her Rotten movie, Genius hacker Abby was the Governor's a
    # FACTS: doptive daughter, enduring years of abuse to help him seize power. Yet, right before her 1
    # FACTS: 8th birthday, her adoptive father sells her to a lecherous businessman for $5 million. In 
    # FACTS: despair, she uses DNA matching to find her biological father—America's top tycoon, Dominic
    # FACTS:  Mancini. Back in the lap of luxury, Abby not only inherits trillions but also has three e
    # FACTS: lite adopted brothers, each a titan in his own right, to protect her. At her grand coming-
    # FACTS: of-age ceremony, Abby makes a magnificent return as the sole heir, publicly unmasking her 
    # FACTS: adoptive family's cruelty and making those who once bullied her pay dearly. Reborn from th
    # FACTS: e ashes, she will begin her brilliant life at the pinnacle of power.
    'her-billionaire-father-spoils-her-rotten':
        "Sold for five million dollars by the man who raised her.\nAbby is a genius hacker, and for years she put up with the Governor's abuse while she helped her adoptive father climb to power. Just before she turns eighteen, he sells her to a sleazy businessman for five million dollars. Desperate, Abby runs a DNA match and finds her real father, Dominic Mancini, the richest tycoon in America. Overnight she's the sole heir to trillions, with three powerful adopted brothers standing guard over her. At her coming of age ceremony she walks in as the Mancini heir, exposes everything her adoptive family did to her, and makes every one of her bullies pay. Reborn from the worst of it, she's only just getting started.",

    # Keeping the Cowboy's Baby
    # FACTS: She came to town for a fresh start. Instead, Penelope Harris got pregnant by her ex’s powe
    # FACTS: rful older brother, Knox Grant– the rugged cowboy who owns the ranch where she works. Now 
    # FACTS: Penelope is caught between the man who would burn the world down for her and her ex, who w
    # FACTS: ants to see her burn.
    'keeping-the-cowboy-s-baby':
        "She came for a fresh start. She got pregnant by her ex's brother.\nPenelope Harris moves to town to start over and takes a job on a ranch. The ranch belongs to Knox Grant, a rugged cowboy with a lot of power, who also happens to be her ex's older brother. Then Penelope ends up pregnant with Knox's baby. Now she's stuck between two brothers. Knox would tear the world apart to keep her safe. Her ex would like nothing better than to watch her go down in flames.",

    # Hating and Loving My Adopted Brother
    # FACTS: In Hating and Loving My Adopted Brother movie, after Abigail's parents both die in an acci
    # FACTS: dent, she gets adopted by her dad's friend. She transfers to a new high school and clashes
    # FACTS:  with Chris, who acts like a total selfish prick — only to discover that he's her new adop
    # FACTS: ted brother! Living under the same roof, she falls for him... but does he like her back?
    'hating-and-loving-my-adopted-brother':
        "The boy she can't stand is now her brother.\nAbigail loses both her parents in an accident, and her dad's friend takes her in. At her new high school she runs straight into Chris, who acts like a selfish jerk and seems to care about nobody but himself. Then she finds out he's the son of the family that adopted her, which makes him her new brother. Now they live under one roof, and somewhere between the fights Abigail starts falling for him. But does he feel the same way?",

    # The Hockey Captain That Hates Me
    # FACTS: In The Hockey Captain That Hates Me movie, plus-size figure skater Skylar Carter hates the
    # FACTS:  arrogant hockey team captain, Mason Reed, with good reason. When Skylar’s prank against t
    # FACTS: he team leaves Mason injured, she’s forced to be his assistant or risk losing her own spor
    # FACTS: ts future. Forced together, their rivalry turns into undeniable chemistry. But after the s
    # FACTS: chool announces only one program will survive to next season, Skylar and Mason may be fall
    # FACTS: ing for the one person whose victory could destroy their dreams.
    'the-hockey-captain-that-hates-me':
        "Her prank got him hurt. Now she has to be his assistant.\nSkylar Carter is a plus size figure skater, and she has every reason to hate Mason Reed, the arrogant captain of the hockey team. Her prank on the team goes wrong and leaves Mason injured, and the price is that she works as his assistant or puts her own skating future at risk. Stuck together, their rivalry turns into chemistry neither of them can ignore. Then the school says only one of the two programs will survive next season. Skylar and Mason could be falling for the one person whose win wrecks everything they've worked for.",

    # After Divorce, My Ex-Wife Became a Billionaire
    # FACTS: In After Divorce My Ex-Wife Became a Billionaire movie, Claire, secretly the heir to a vas
    # FACTS: t fortune, hides her true identity to marry Milo out of love. Living in Los Angeles, she q
    # FACTS: uietly uses her wealth and influence to smooth out the obstacles on Milo's path to buildin
    # FACTS: g his startup. Just as Milo is on the brink of success, Claire discovers he's been unfaith
    # FACTS: ful. Confronted, Milo admits he's fallen out of love, speaks harshly to her, dismisses all
    # FACTS:  she's done for him, and pressures her into a divorce. Heartbroken and deeply disappointed
    # FACTS: , Claire decides to reclaim her position as a billionaire heiress. She withdraws all her s
    # FACTS: upport, and lets Milo face the consequences of his actions, making him regret everything h
    # FACTS: e's done.
    'after-divorce-my-ex-wife-became-a-billionaire':
        "She hid a fortune to marry for love. He cheated anyway.\nClaire is secretly the heiress to an enormous fortune, and she keeps it quiet so she can marry Milo because she loves him. In Los Angeles she uses her money and connections behind the scenes to clear the way for his startup. Just as it's about to take off, she finds out he's cheating. When she confronts him, Milo tells her he doesn't love her anymore, throws everything she's done for him back in her face and pushes her into a divorce. Heartbroken, Claire takes back her place as a billionaire heiress. She pulls every bit of her support and lets Milo find out what his success was really built on. Now he regrets all of it.",

    # Freeze! Runaway Groom
    # FACTS: In Freeze! Runaway Groom movie, to pay for her father's medical bills, Ivy is forced to ma
    # FACTS: rry Byron, a wealthy heir, instead of her stepsister. But on their wedding day, Byron does
    # FACTS: n't show up, leaving Ivy humiliated in front of all their family and friends. After they f
    # FACTS: inally marry, they set three rules—agreeing they won't fall in love with each other. Event
    # FACTS: ually, Byron tells Ivy that the agreement is ridiculous because he's already fallen in lov
    # FACTS: e with her. He asks her if she loves him back. So, will Ivy reciprocate his feelings?
    'freeze-runaway-groom':
        "She married him to pay her father's bills. He didn't show up to the wedding.\nIvy's father needs medical care she can't pay for, so she's pushed into marrying Byron, a wealthy heir who was meant for her stepsister. On the wedding day Byron never shows, and Ivy is left standing there humiliated in front of everyone they know. When they do finally marry, they agree on three rules, and one of them is that nobody falls in love. It's Byron who breaks it. He tells Ivy the whole deal is ridiculous because he already loves her, and he wants to know if she loves him too. Will she say yes?",

    # The Virgin Camp Counselor
    # FACTS: When Chloe's first day of camp, her nemesis Morgan reveals that she's a virgin to all of t
    # FACTS: he other counselors, and the guys at camp compete to see who takes Chloe's V-Card. But whe
    # FACTS: n she's saved by bad boy counselor Asher, she meets the first person who gets her to let h
    # FACTS: er guard down. Can Chloe and Asher's relationship a summer of crazy campers, wild bonfires
    # FACTS: , and a hoard of counselors who want to tear their relationship apart?
    'the-virgin-camp-counselor':
        "Her first day at camp, and her secret is everyone's business.\nOn Chloe's first day as a camp counselor, her nemesis Morgan tells the rest of the staff that Chloe is a virgin. The guys turn it into a contest over who gets to be her first. Then bad boy counselor Asher steps in to save her, and he's the first person she's ever let her guard down around. Can what they have make it through a summer of wild campers, bonfires and a whole camp full of counselors trying to pull them apart?",

    # Her Double, His Trouble
    # FACTS: Identical twins Erin and Elise were torn apart as kids. 20 years later, gently Elise is be
    # FACTS: trayed by the two people she trusted most — her husband and best friend — then tortured an
    # FACTS: d left for dead. Grief-stricken and furious, badass CEO Erin steps into her dead sister’s 
    # FACTS: life to exact revenge. Their faces may be carbon copies, but Erin is no one one to mess wi
    # FACTS: th as she systematically and pyschologically pits her sister’s husband and best friend aga
    # FACTS: inst each other in a cat and mouse game to destroy the murderers.
    'her-double-his-trouble':
        "Her twin was murdered. She's taking her place.\nErin and Elise are identical twins who were split up as children. Twenty years later, sweet Elise is betrayed by her husband and her best friend, the people she trusted more than anyone, and they torture her and leave her for dead. Erin is a CEO and nobody's pushover. Wild with grief and rage, she takes over Elise's life to make them pay. She looks exactly like Elise, and she uses that to turn the husband and the best friend against each other, one mind game at a time, in a game of cat and mouse built to destroy the two people who killed her sister.",

    # My Alpha Boss Gave Me Triplets
    # FACTS: In My Alpha Boss Gave Me Triplets movie, Evie, a talented but vulnerable human designer, b
    # FACTS: ecomes bound to Leopold, the ruthless Alpha of the Stonehearth Pack, leaving her pregnant 
    # FACTS: with his rare triplets. To protect her, Leopold forces her to move in with him, presenting
    # FACTS:  their relationship as purely transactional while privately struggling with uncontrollable
    # FACTS:  mate-bond instincts that cause him to share Evie's pain and emotions. As Evie is drawn in
    # FACTS: to Leopold’s corporate and pack world, Darleen, a powerful she-wolf from another pack dete
    # FACTS: rmined to claim Leopold, escalates from professional threats to phsyical ones. Evie's estr
    # FACTS: anged family piles on by attempting to kidnap her. Will Leopold be able to prioritize his 
    # FACTS: mate over everything, and save her from the whirlwind he brought her into?
    'my-alpha-boss-gave-me-triplets':
        "A human designer, an Alpha, and three rare babies on the way.\nEvie is a gifted designer, but she's human and she's vulnerable, and she ends up bound to Leopold. He's the Alpha of the Stonehearth Pack, and he's ruthless. Now she's pregnant with his triplets, which almost never happens. Leopold moves her into his home to keep her safe and tells everyone it's strictly business. In private the mate bond is getting the better of him, to the point where he feels her pain and every emotion she has. As Evie gets pulled into his company and his pack, Darleen, a strong she wolf from a different pack who wants Leopold for herself, goes from threatening Evie's work to threatening her life. Then Evie's estranged family try to kidnap her. Can Leopold put his mate first and get her out of the storm he dragged her into?",

    # Swimming My Way Back to You
    # FACTS: In Swimming My Way Back to You movie, Hazel has been in love with Marcus for eight years a
    # FACTS: nd spent three of them as his secret lover. Just when she thought she had finally won his 
    # FACTS: heart, she overhears Marcus confessing that the only person he’s ever truly loved is his f
    # FACTS: irst love, Zoe. Heartbroken, Hazel decides it’s time to break things off with him—only to 
    # FACTS: find out she’s pregnant...
    'swimming-my-way-back-to-you':
        "Eight years loving him. Three of them in secret.\nHazel has loved Marcus for eight years, and for three of those she's been the girlfriend nobody was allowed to know about. Just when she thinks she's finally won him over, she hears him admit that the only woman he's ever really loved is Zoe, his first love. Hazel is devastated and decides it's over. Then she finds out she's carrying his baby, and walking away just got a lot harder.",

    # All the Wrong Reasons
    # FACTS: In All the Wrong Reasons episode 5, Andrea must handle a sex column or lose her job. She h
    # FACTS: ad no idea about sex as she was inexperienced at it. Andrea sets out to have sex. In the p
    # FACTS: rocess, she met Justin, an old-time friend. Justin volunteers to help Andrea with her sex 
    # FACTS: column. What starts as a simple research turns into a steamy romance.
    'all-the-wrong-reasons':
        "Write the sex column or lose the job.\nAndrea has to take on the sex column at work or she's out of a job. The problem is she has almost no experience to write from. So Andrea goes looking for some, and along the way she runs into Justin, a friend from way back. He offers to help with her research. It's meant to be purely for the column, but it doesn't stay that way, and it turns into a steamy romance.",

    # The Gourmet CEO Turns out to Be My Baby's Dad
    # FACTS: Betrayed by her family, Skylar is forced into a compromising situation with a sleazy-looki
    # FACTS: ng director in exchange for her grandmother's medical bills. However, she unexpectedly has
    # FACTS:  a one-night stand with Maxwell, CEO of Klein Group, instead, leading to an unplanned preg
    # FACTS: nancy. Sent abroad, Skyhlar returns six years later with her son and opens a restaurant. F
    # FACTS: ate eventually brings her and Maxwell back... Will he recognize Skylar as the unforgettabl
    # FACTS: e woman from that fateful night?
    'the-gourmet-ceo-turns-out-to-be-my-baby-s-dad':
        "Her family set her up with a sleazy director. She ended up with a CEO instead.\nSkylar's own family betray her, pushing her into a night with a sleazy looking director so her grandmother's medical bills get paid. Instead she ends up spending the night with Maxwell, the CEO of Klein Group, and she gets pregnant. She's sent abroad, and six years later she comes back with her son and starts her own restaurant. Fate keeps steering Maxwell back to her. Will he realize she's the woman he never forgot from that one night?",

    # Don't Mess with a Prep School Princess
    # FACTS: Sierra Lane thought she was getting her life back when she was finally released from juvie
    # FACTS:  after taking the fall for her boyfriend, Jake. Instead, she’s met with a shocking truth: 
    # FACTS: she’s the long-lost Lancaster Heiress, heir to one of the biggest fortunes in the country.
    # FACTS:  Armed with a new identity and eager to reclaim her place at Hawthorne Prep, Sierra return
    # FACTS: s to school, ready to share the news. But instead of a warm welcome, she finds that Jake h
    # FACTS: as moved on with her ex-best friend, Fallon. Even worse, Fallon has already been telling e
    # FACTS: veryone that she and the heiress are best friends, making Sierra’s arrival a direct threat
    # FACTS:  to Fallon's reign as queen bee of the school. As Sierra battles relentless gossip, sabota
    # FACTS: ge, and an entire school that wants her sent back to juvie, she’ll have to prove she’s exa
    # FACTS: ctly who she says she is before Fallon destroys her reputation for good.
    'don-t-mess-with-a-prep-school-princess':
        "She took the fall for her boyfriend. She came out an heiress.\nSierra Lane served time in juvie for something her boyfriend Jake did, and on the day she gets out she learns the truth. She's the Lancaster family's missing heiress, and one of the largest fortunes in the country is hers. She heads back to Hawthorne Prep ready to tell everyone, and finds Jake has moved on with her former best friend Fallon. Fallon has also been going around telling the whole school she's best friends with the missing heiress, so Sierra showing up threatens everything Fallon has as queen bee. Now Sierra is up against gossip, sabotage and a whole school that would love to see her locked up again, and she has to prove who she really is before Fallon ruins her name for good.",

    # The CEO's Wife is A Badass
    # FACTS: In The CEO's Wife is A Badass movie, Cora, a modest artist and the wife of billionaire Bra
    # FACTS: ndon Pearson, finds herself managing his gallery while he's away on business. However, her
    # FACTS:  role as the CEO's wife is unexpectedly eclipsed by her college classmate Ashley, leaving 
    # FACTS: Cora scorned by her colleagues. Can Cora reclaim her place and prove her worth?
    'the-ceo-s-wife-is-a-badass':
        "The billionaire's wife, pushed aside in his own gallery.\nCora is a quiet artist married to billionaire Brandon Pearson, and while he's out of town for work she's left in charge of his gallery. Then Ashley, a classmate from her college days, turns up and takes the spotlight, and Cora's place as the CEO's wife suddenly counts for nothing. The staff turn their noses up at her. Can Cora take her place back and show them all what she's worth?",

    # Finding Master Right
    # FACTS: Kate's always fantasized about a sexy man who will dominate her in the bedroom, but findin
    # FACTS: g one is way easier said than done. Until Catacombs' notorious Master, Banner Jennings, of
    # FACTS: fers to help her find the perfect Dom. But once he finds her sexual match, will he be will
    # FACTS: ing to let her go?
    'finding-master-right':
        "She wants a man who takes control. Finding one is the hard part.\nKate has always dreamed of a gorgeous man who takes charge of her in the bedroom, but actually finding him turns out to be a lot harder than dreaming about him. Then Banner Jennings, the notorious Master at Catacombs, offers to help her find the right Dom. The catch comes once he's found her perfect match. Will Banner really be able to let her go?",

    # Audrey in Full Bloom
    # FACTS: In Audrey in Full Bloom movie, Harvard MBA Audrey Lorenzo Bloom is on her way to shatter b
    # FACTS: arriers as powerful conglomerate BloomCo’s first female and non-white CEO. She’s been prep
    # FACTS: aring for years, even using an alias as a Latina cleaning lady to learn the inner workings
    # FACTS:  of the company. Now on the eve of the banquet introducing her, Audrey discovers her fianc
    # FACTS: é thinks she’s an illegal alien and plans to defraud and deport her, the senior executives
    # FACTS:  are plotting a coup to put her white cousin in charge, and her bitterest enemy since chil
    # FACTS: dhood, Ryder Marlow, might not be her enemy after all…
    'audrey-in-full-bloom':
        "Years undercover as a cleaner. One night before she takes the top job.\nAudrey Lorenzo Bloom has a Harvard MBA and is about to become the first woman and the first person of color to be CEO of BloomCo, a powerful conglomerate. She's spent years getting ready, even working there under a fake name as a Latina cleaning lady so she'd know how the company really runs. The night before she's due to be presented at a big banquet, it all comes at once. Her fiance thinks she's undocumented and is planning to cheat her and have her deported. Top executives are scheming to push her aside and hand the job to her white cousin. And Ryder Marlow, her worst enemy since they were kids, might not be the enemy she always thought.",

    # The Queen Bee Strikes Back
    # FACTS: Bella, heir to the wealthy Walton family, is tired of being surrounded by calculating rich
    # FACTS:  kids. She falls for Marc, a plus-size guy who seems to love her for who she is, hiding he
    # FACTS: r identity and even helping him get recruited to Harvard’s football team. But betrayal hit
    # FACTS: s hard, Bella discovers Marc has been cheating on her with her classmate - and bully - Jes
    # FACTS: sie, who constantly mocks Bella’s body. Even worse, Marc has stolen her identity, claiming
    # FACTS:  he is the Walton heir to win clout and rise to the top of Western High’s social scene. Be
    # FACTS: lla dumps him, has a stunning glow-up, and embraces her curves. When they mock her college
    # FACTS:  future… could Bella’s next move leave them speechless?
    'the-queen-bee-strikes-back':
        "She hid her money to be loved for herself. He stole her name.\nBella is the heir to the Walton family's fortune and sick of rich kids who only want something from her. She meets Marc, a plus size guy, and falls for him because he seems to like her for exactly who she is. She keeps her background a secret and even helps get him recruited to the Harvard football team. Then she finds out he's been cheating on her with Jessie, her classmate and her bully, who picks on Bella's body every chance she gets. On top of that, Marc has taken her identity and is telling everyone he's the Walton heir so he can climb to the top at Western High. Bella leaves him, goes through a stunning glow up and learns to love her curves. They're laughing about her college plans now. Her next move might shut them up for good.",

    # I Hired a Billionaire Manny
    # FACTS: 5 years ago, Sienna and Damian had an one night stand. Now, she's back with their daughter
    # FACTS:  Poppy as the CEO of a huge production company in LA. To reconnect with them, Damian hides
    # FACTS:  his billionaire identity and becomes Poppy's manny. Will they stand against the world and
    # FACTS:  build a new life as a family?
    'i-hired-a-billionaire-manny':
        "Five years after their one night, she's back with his daughter.\nFive years ago Sienna and Damian spent one night together. Now she's back in LA, running a huge production company as its CEO, and she's brought their daughter Poppy with her. Damian wants back into their lives, so he hides the fact that he's a billionaire and takes a job as Poppy's manny. Can the three of them take on the world and become a real family?",

    # Mancini’s Forbidden Bride
    # FACTS: Pregnant. Widowed. Dragged into the Mancini mafia. Ava never expected her late husband to 
    # FACTS: be the hidden heir—nor to crave his ruthless brother. Ice-cold don Luca vows to shield her
    # FACTS: , but every touch ignites a forbidden fire. Rival gangs close in, her birth family plots b
    # FACTS: etrayal, and the dynasty teeters on war. How long before Luca shatters every rule to claim
    # FACTS:  the woman worth killing for?
    'mancini-s-forbidden-bride':
        "Pregnant, widowed, and pulled into the mafia.\nAva had no idea her late husband was the secret heir to the Mancini family, and she never expected to want his ruthless brother. Luca is an ice cold don who swears he'll protect her, and every time he touches her it's a fire neither of them is allowed. Rival gangs are closing in, her own birth family is planning to betray her, and the whole dynasty is on the edge of war. How long can Luca keep to the rules before he breaks every one of them to have the woman worth killing for?",

}

FACTS = {
    'you-ve-been-replaced-first-love': "To Jason, Tessa was only a disposable practice run for the girl he actually wanted. After the blood on the sheets became a public trophy and her dignity a ghost, young Tessa finally stops trying to mend the shards. She is done with her first love. She is leaving him behind for a future that doesn't taste like salt and shame. But at the edge of the wreckage stands the one person who shouldn’t be there: another boy with no intention of letting her go alone.",
    'the-heiress-blacklisted-her-husband': "Giselle, the Duke's daughter and rightful heiress of the Von Howard's family, married Patrick Hilton three years ago after he saved her life. She secretly helped his company go public, but constant harassment from Patrick’s mother and relentless taunts from Becky leave Giselle, now pregnant, feeling hopeless. She decides to divorce Patrick. Despite everything, Patrick’s heart belongs only to Giselle. After the divorce, he realizes how much he needs her and begins a long journey to win her back.",
    'fiancee-s-betrayal-dante-s-inferno': "In Fiancée's Betrayal Dante's Inferno movie, Dante Bosch returns home after 3 years in the Marine Raiders on a top secret mission, only to discover not only is his fiancée Lilith pregnant with his brother Virgil's baby, but Virgil has also spent all his money. To add insult to injury, his parents take Virgil's side. After suffering betrayals and humiliations, Dante exposes Virgil's lies with a video at his wedding.",
    'rejecting-my-five-female-mates': "Orphaned Caine spent ten years protecting his foster father Alpha's five daughters, believing they were his destined mates. However, the arrival of Seth, a manipulative rogue wolf, shatters his world. Blinded by Seth's deceit, the five sisters turn against Caine, relentlessly humiliating him and stripping away his honor and sacred armor to appease the rogue. Pushed to the brink of despair by the family he once loved, Caine faces a turning point at his Ascension Ceremony. Will the powerful warrior continue to endure their cruel betrayal, or will he sever their fated bonds to claim a greater destiny?",
    'faking-it-with-my-ex-s-best-friend': 'Clara fakes amnesia to test her boyfriend—only to catch him cheating and watch him toss her aside for his best friend, Ethan. Big mistake. For the ultimate payback, Clara starts fake-dating Ethan to drive her ex insane with jealousy. But what happens when Ethan’s fake kisses start to feel dangerously real?',
    'pregnant-by-the-billionaire': "Mia Harper, down on her luck, marries wealthy CEO Carter Prescott as part of a deal. Their fake marriage soon blossoms into real romance, but their love is tested when Carter's ruthless ex, Lily, stops at nothing to win him back. The drama intensifies when Mia discovers she's pregnant with Carter's baby and uncovers the shocking truth that Lily is her long-lost stepsister...",
    'her-billionaire-father-spoils-her-rotten': "In Her Billionaire Father Spoils Her Rotten movie, Genius hacker Abby was the Governor's adoptive daughter, enduring years of abuse to help him seize power. Yet, right before her 18th birthday, her adoptive father sells her to a lecherous businessman for $5 million. In despair, she uses DNA matching to find her biological father—America's top tycoon, Dominic Mancini. Back in the lap of luxury, Abby not only inherits trillions but also has three elite adopted brothers, each a titan in his own right, to protect her. At her grand coming-of-age ceremony, Abby makes a magnificent return as the sole heir, publicly unmasking her adoptive family's cruelty and making those who once bullied her pay dearly. Reborn from the ashes, she will begin her brilliant life at the pinnacle of power.",
    'keeping-the-cowboy-s-baby': 'She came to town for a fresh start. Instead, Penelope Harris got pregnant by her ex’s powerful older brother, Knox Grant– the rugged cowboy who owns the ranch where she works. Now Penelope is caught between the man who would burn the world down for her and her ex, who wants to see her burn.',
    'hating-and-loving-my-adopted-brother': "In Hating and Loving My Adopted Brother movie, after Abigail's parents both die in an accident, she gets adopted by her dad's friend. She transfers to a new high school and clashes with Chris, who acts like a total selfish prick — only to discover that he's her new adopted brother! Living under the same roof, she falls for him... but does he like her back?",
    'the-hockey-captain-that-hates-me': 'In The Hockey Captain That Hates Me movie, plus-size figure skater Skylar Carter hates the arrogant hockey team captain, Mason Reed, with good reason. When Skylar’s prank against the team leaves Mason injured, she’s forced to be his assistant or risk losing her own sports future. Forced together, their rivalry turns into undeniable chemistry. But after the school announces only one program will survive to next season, Skylar and Mason may be falling for the one person whose victory could destroy their dreams.',
    'after-divorce-my-ex-wife-became-a-billionaire': "In After Divorce My Ex-Wife Became a Billionaire movie, Claire, secretly the heir to a vast fortune, hides her true identity to marry Milo out of love. Living in Los Angeles, she quietly uses her wealth and influence to smooth out the obstacles on Milo's path to building his startup. Just as Milo is on the brink of success, Claire discovers he's been unfaithful. Confronted, Milo admits he's fallen out of love, speaks harshly to her, dismisses all she's done for him, and pressures her into a divorce. Heartbroken and deeply disappointed, Claire decides to reclaim her position as a billionaire heiress. She withdraws all her support, and lets Milo face the consequences of his actions, making him regret everything he's done.",
    'freeze-runaway-groom': "In Freeze! Runaway Groom movie, to pay for her father's medical bills, Ivy is forced to marry Byron, a wealthy heir, instead of her stepsister. But on their wedding day, Byron doesn't show up, leaving Ivy humiliated in front of all their family and friends. After they finally marry, they set three rules—agreeing they won't fall in love with each other. Eventually, Byron tells Ivy that the agreement is ridiculous because he's already fallen in love with her. He asks her if she loves him back. So, will Ivy reciprocate his feelings?",
    'the-virgin-camp-counselor': "When Chloe's first day of camp, her nemesis Morgan reveals that she's a virgin to all of the other counselors, and the guys at camp compete to see who takes Chloe's V-Card. But when she's saved by bad boy counselor Asher, she meets the first person who gets her to let her guard down. Can Chloe and Asher's relationship a summer of crazy campers, wild bonfires, and a hoard of counselors who want to tear their relationship apart?",
    'her-double-his-trouble': 'Identical twins Erin and Elise were torn apart as kids. 20 years later, gently Elise is betrayed by the two people she trusted most — her husband and best friend — then tortured and left for dead. Grief-stricken and furious, badass CEO Erin steps into her dead sister’s life to exact revenge. Their faces may be carbon copies, but Erin is no one one to mess with as she systematically and pyschologically pits her sister’s husband and best friend against each other in a cat and mouse game to destroy the murderers.',
    'my-alpha-boss-gave-me-triplets': "In My Alpha Boss Gave Me Triplets movie, Evie, a talented but vulnerable human designer, becomes bound to Leopold, the ruthless Alpha of the Stonehearth Pack, leaving her pregnant with his rare triplets. To protect her, Leopold forces her to move in with him, presenting their relationship as purely transactional while privately struggling with uncontrollable mate-bond instincts that cause him to share Evie's pain and emotions. As Evie is drawn into Leopold’s corporate and pack world, Darleen, a powerful she-wolf from another pack determined to claim Leopold, escalates from professional threats to phsyical ones. Evie's estranged family piles on by attempting to kidnap her. Will Leopold be able to prioritize his mate over everything, and save her from the whirlwind he brought her into?",
    'swimming-my-way-back-to-you': 'In Swimming My Way Back to You movie, Hazel has been in love with Marcus for eight years and spent three of them as his secret lover. Just when she thought she had finally won his heart, she overhears Marcus confessing that the only person he’s ever truly loved is his first love, Zoe. Heartbroken, Hazel decides it’s time to break things off with him—only to find out she’s pregnant...',
    'all-the-wrong-reasons': 'In All the Wrong Reasons episode 5, Andrea must handle a sex column or lose her job. She had no idea about sex as she was inexperienced at it. Andrea sets out to have sex. In the process, she met Justin, an old-time friend. Justin volunteers to help Andrea with her sex column. What starts as a simple research turns into a steamy romance.',
    'the-gourmet-ceo-turns-out-to-be-my-baby-s-dad': "Betrayed by her family, Skylar is forced into a compromising situation with a sleazy-looking director in exchange for her grandmother's medical bills. However, she unexpectedly has a one-night stand with Maxwell, CEO of Klein Group, instead, leading to an unplanned pregnancy. Sent abroad, Skyhlar returns six years later with her son and opens a restaurant. Fate eventually brings her and Maxwell back... Will he recognize Skylar as the unforgettable woman from that fateful night?",
    'don-t-mess-with-a-prep-school-princess': "Sierra Lane thought she was getting her life back when she was finally released from juvie after taking the fall for her boyfriend, Jake. Instead, she’s met with a shocking truth: she’s the long-lost Lancaster Heiress, heir to one of the biggest fortunes in the country. Armed with a new identity and eager to reclaim her place at Hawthorne Prep, Sierra returns to school, ready to share the news. But instead of a warm welcome, she finds that Jake has moved on with her ex-best friend, Fallon. Even worse, Fallon has already been telling everyone that she and the heiress are best friends, making Sierra’s arrival a direct threat to Fallon's reign as queen bee of the school. As Sierra battles relentless gossip, sabotage, and an entire school that wants her sent back to juvie, she’ll have to prove she’s exactly who she says she is before Fallon destroys her reputation for good.",
    'the-ceo-s-wife-is-a-badass': "In The CEO's Wife is A Badass movie, Cora, a modest artist and the wife of billionaire Brandon Pearson, finds herself managing his gallery while he's away on business. However, her role as the CEO's wife is unexpectedly eclipsed by her college classmate Ashley, leaving Cora scorned by her colleagues. Can Cora reclaim her place and prove her worth?",
    'finding-master-right': "Kate's always fantasized about a sexy man who will dominate her in the bedroom, but finding one is way easier said than done. Until Catacombs' notorious Master, Banner Jennings, offers to help her find the perfect Dom. But once he finds her sexual match, will he be willing to let her go?",
    'audrey-in-full-bloom': 'In Audrey in Full Bloom movie, Harvard MBA Audrey Lorenzo Bloom is on her way to shatter barriers as powerful conglomerate BloomCo’s first female and non-white CEO. She’s been preparing for years, even using an alias as a Latina cleaning lady to learn the inner workings of the company. Now on the eve of the banquet introducing her, Audrey discovers her fiancé thinks she’s an illegal alien and plans to defraud and deport her, the senior executives are plotting a coup to put her white cousin in charge, and her bitterest enemy since childhood, Ryder Marlow, might not be her enemy after all…',
    'the-queen-bee-strikes-back': 'Bella, heir to the wealthy Walton family, is tired of being surrounded by calculating rich kids. She falls for Marc, a plus-size guy who seems to love her for who she is, hiding her identity and even helping him get recruited to Harvard’s football team. But betrayal hits hard, Bella discovers Marc has been cheating on her with her classmate - and bully - Jessie, who constantly mocks Bella’s body. Even worse, Marc has stolen her identity, claiming he is the Walton heir to win clout and rise to the top of Western High’s social scene. Bella dumps him, has a stunning glow-up, and embraces her curves. When they mock her college future… could Bella’s next move leave them speechless?',
    'i-hired-a-billionaire-manny': "5 years ago, Sienna and Damian had an one night stand. Now, she's back with their daughter Poppy as the CEO of a huge production company in LA. To reconnect with them, Damian hides his billionaire identity and becomes Poppy's manny. Will they stand against the world and build a new life as a family?",
    'mancini-s-forbidden-bride': 'Pregnant. Widowed. Dragged into the Mancini mafia. Ava never expected her late husband to be the hidden heir—nor to crave his ruthless brother. Ice-cold don Luca vows to shield her, but every touch ignites a forbidden fire. Rival gangs close in, her birth family plots betrayal, and the dynasty teeters on war. How long before Luca shatters every rule to claim the woman worth killing for?',
}

SOURCES = {
    'you-ve-been-replaced-first-love': ('platform', 'https://www.reelshort.com/movie/you-ve-been-replaced-first-love-6a469b12d3f5c65f7f095b8a'),
    'the-heiress-blacklisted-her-husband': ('platform', 'https://www.reelshort.com/movie/the-heiress-blacklisted-her-husband-677db481a3cc638b8f0d8a59'),
    'fiancee-s-betrayal-dante-s-inferno': ('platform', 'https://www.reelshort.com/movie/fiancee-s-betrayal-dante-s-inferno-6a2b076bbe129b998d0fa894'),
    'rejecting-my-five-female-mates': ('platform', 'https://www.reelshort.com/movie/rejecting-my-five-female-mates-6a99555185913218590748f3'),
    'faking-it-with-my-ex-s-best-friend': ('platform', 'https://www.reelshort.com/movie/faking-it-with-my-ex-s-best-friend-6a4bde37cdb434b20e085b0a'),
    'pregnant-by-the-billionaire': ('platform', 'https://www.reelshort.com/movie/pregnant-by-the-billionaire-669ff9a361704e7f8e045c5f'),
    'her-billionaire-father-spoils-her-rotten': ('platform', 'https://www.reelshort.com/movie/her-billionaire-father-spoils-her-rotten-6a3d9547091cd749a8093d65'),
    'keeping-the-cowboy-s-baby': ('platform', 'https://www.reelshort.com/movie/keeping-the-cowboy-s-baby-6a580b359cc3a55a2b08ad6d'),
    'hating-and-loving-my-adopted-brother': ('platform', 'https://www.reelshort.com/movie/hating-and-loving-my-adopted-brother-69c0a262b5d57818100485ef'),
    'the-hockey-captain-that-hates-me': ('platform', 'https://www.reelshort.com/movie/the-hockey-captain-that-hates-me-6a18b1c2bbfcc4fcd30a20b9'),
    'after-divorce-my-ex-wife-became-a-billionaire': ('platform', 'https://www.reelshort.com/movie/after-divorce-my-ex-wife-became-a-billionaire-67cb8fb6ec57377a7408e9bb'),
    'freeze-runaway-groom': ('platform', 'https://www.reelshort.com/movie/freeze-runaway-groom-67f790db472487b6b00b8e24'),
    'the-virgin-camp-counselor': ('platform', 'https://www.reelshort.com/movie/the-virgin-camp-counselor-67b821fdd25ca3629404c514'),
    'her-double-his-trouble': ('platform', 'https://www.reelshort.com/movie/her-double-his-trouble-689e222a75034b7ff90fd71b'),
    'my-alpha-boss-gave-me-triplets': ('platform', 'https://www.reelshort.com/movie/my-alpha-boss-gave-me-triplets-6a18943221fde96a100f8ed8'),
    'swimming-my-way-back-to-you': ('platform', 'https://www.reelshort.com/movie/swimming-my-way-back-to-you-67f06f8c388bcdbbae08b10a'),
    'all-the-wrong-reasons': ('platform', 'https://www.reelshort.com/movie/all-the-wrong-reasons-666baef14c30f415f501bd3b'),
    'the-gourmet-ceo-turns-out-to-be-my-baby-s-dad': ('platform', 'https://www.reelshort.com/movie/the-gourmet-ceo-turns-out-to-be-my-baby-s-dad-67887e2258dceeba8200f5b7'),
    'don-t-mess-with-a-prep-school-princess': ('platform', 'https://www.reelshort.com/movie/don-t-mess-with-a-prep-school-princess-68a77fac1967059c3c0457d2'),
    'the-ceo-s-wife-is-a-badass': ('platform', 'https://www.reelshort.com/movie/the-ceo-s-wife-is-a-badass-67380d9c3f2f3cd986037939'),
    'finding-master-right': ('platform', 'https://www.reelshort.com/movie/finding-master-right-689412a977c582c95a06a0be'),
    'audrey-in-full-bloom': ('platform', 'https://www.reelshort.com/movie/audrey-in-full-bloom-67d8a6ea787657f63a0faf83'),
    'the-queen-bee-strikes-back': ('platform', 'https://www.reelshort.com/movie/the-queen-bee-strikes-back-689bfcef5bd68625550ec33b'),
    'i-hired-a-billionaire-manny': ('platform', 'https://www.reelshort.com/movie/i-hired-a-billionaire-manny-67218268a00a63dd47062dab'),
    'mancini-s-forbidden-bride': ('platform', 'https://www.reelshort.com/movie/mancini-s-forbidden-bride-6883565dc255ace14a072541'),
}
