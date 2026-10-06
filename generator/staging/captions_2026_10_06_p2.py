# -*- coding: utf-8 -*-
"""Caption batch 6 Oct 2026, part 2, titles imported 6 Oct (DramaBox 28 Sep data and Cyan's Reddit finds). STAGED FOR CYAN'S REVIEW, not approved.

32 titles, 30 written, 2 skipped. Every caption is written from the platform page the
title links to (availability.csv direct_link): 31 DramaBox books (the banked
synopsis is the platform's own text; dramaboxdb.com refuses direct fetches) and
one AnyReel book (no-escape-from-the-vampire). Each FACTS entry is that source text.

SKIPPED, no story in the source, needs Cyan or a better source:
  i-went-to-the-mafia-boss-for-a-baby: DramaBox publishes a one line teaser and nothing else ("I saved a cartel king who tricked me into marriage. What he doesn't know is, I have secrets too."). No names, no story, and the baby in the title is not in the source.
  i-m-the-rule: DramaBox publishes a generic marketing blurb with no names and no plot (a nameless mafia Emperor navigating betrayal, love and loyalty while hiding his identity).
"""

CAPTIONS = {
    # 247.6M  The Longlost Heiress's Return
    'the-longlost-heiress-s-return':
        "Her mother built an empire just to find her.\nZoe Park lost her daughter Nova in an accident, and she never stopped searching. To find her daughter, Zoe built the biggest conglomerate on the planet and promised a fortune to anyone who could bring Nova home. At last word comes in. Nova has been found at a medical lab. But when Zoe walks in, she sees a pack of opportunists stripping her girl of every last scrap of dignity. Zoe swears they'll pay for it, and they have no idea whose daughter they've been stepping on.",
    # 126.4M  Shifter Academy: Taming Three Wild Mates
    'shifter-academy-taming-three-wild-mates':
        "One human girl. Three alphas. And it's mating season.\nIvy is human, and all she wants is to finish school. Her scholarship sends her to Shifter Academy, a campus packed with apex predators, right in the middle of mating season. And there's a catch nobody told her about. Ronan, Leon and Talon, the three most powerful shifters at the academy, all turn out to have the same fated mate. It's her. Three alphas are bound to her, and she can only choose one. Her heart has already decided, and it was love at first slap.",
    # 103.9M  Trails of Hope: His Journey Back Home
    'trails-of-hope-his-journey-back-home':
        "A car accident cost him his parents. Twenty years later he's coming home.\nTwenty years ago a car accident cut Theo Levy off from his mom and dad, and he never found his way back to them. The chairman of Boyd Group adopted him, and the man Theo is today is the one that chairman raised. Now he's finally back in the town where he was born, and he's made a vow to track down the parents he lost. The only thing he has to go on is a pendant, and twenty missing years he wants back.",
    # 90.8M  He Broke the Heart That Saved Him
    'he-broke-the-heart-that-saved-him':
        "She saved his life, then left without telling him about the baby.\nWhen Vance was dying, Mia gave up everything she had to save him. She had no idea he was the greatest heir in Cloud City. To give him back the future that was waiting for him, she walked away for good, and she never told him she was pregnant. Years later a tragedy involving their child brings them face to face again. But Vance believes the cruel lies he's been told about Mia and turns on her, and in the end it costs their little boy his life. Mia has lived with the grief of losing her son ever since. When Vance finally learns the truth, the regret he's left carrying is more than he can bear.",
    # 78.6M  Sex Education By My Best Friend
    'sex-education-by-my-best-friend':
        "One rule between best friends. No kissing.\nEmma is in college, and after a party leaves her humiliated, her confidence is in pieces. So she goes to Chase. They've been friends since they were kids, he's a charming playboy, and she asks him to help her believe in herself again. They agree on one simple rule, no kissing. But the closer they get, the more real feelings start to grow. Then the rule gets broken. Now Emma has to choose between the guy she used to chase and the one who was right in front of her the whole time.",
    # 60.1M  Fated to My Neighbor Boss
    'fated-to-my-neighbor-boss':
        "Her stepsister stole one of her twins and the man she loves.\nSherry spends one night with Ethan and ends up having twins. Her cruel stepsister Katrina takes one of the babies, a little boy, passes him off as her own son, and ends up engaged to Ethan. Six years later Sherry comes back as Siren, a famous perfumer. She tears apart every lie Katrina has told, gets her stolen son back, and finds herself falling for Ethan. But six years of her boy's life went to the woman who took him.",
    # 53.0M  It's Too Late to Apologize
    'it-s-too-late-to-apologize':
        "Her husband blamed her. Her daughter wanted a different mom.\nZoey's husband has always believed she trapped him into their marriage. Her own daughter wishes someone else were her mother. Then comes one last betrayal, and Zoey is done. She signs the divorce papers and vanishes. Sooner or later her husband and daughter will understand that she isn't coming back. What will they do then?",
    # 49.7M  Mafia's Captive Bride
    'mafia-s-captive-bride':
        "She saved the mafia boss. He made her his wife.\nElena is at her mother's grave when she saves a man's life. That man is Sebastian, a mafia boss, and the way he repays her is by forcing her to marry him. Elena is trapped, but she won't give in. She fights back, and little by little she's the one doing the taming. As one crisis after another comes at them, she ends up falling in love with the man who took her freedom.",
    # 44.4M  Masked Magnate: The Dominant Son-in-Law
    'masked-magnate-the-dominant-son-in-law':
        "His wife's family calls him useless. He's the CEO.\nChris Bell has just been reunited with his real father, and with that comes the CEO job at Apex Group's Olgow branch. Then at the birthday party for his wife's father, he isn't even allowed a seat at the family table. To them he's the live in son in law, good for nothing. His wife gets looked down on right beside him. Another man is trying to take her from him, developers want to tear their home down by force, and worst of all, a rich man viciously attacks his daughter. Everyone at that table thinks he's nobody, and they have no idea who they're dealing with.",
    # 40.8M  Return of His Majesty
    'return-of-his-majesty':
        "He left a villager and came back an emperor. Nobody knows.\nWhen Leo Lowe left home, he gave his fiancee Tina Leed his word. If he ever became emperor, he'd come back for her and make her his empress. Years go by, and he does it. He founds a brand new dynasty and takes the throne. So he heads back to the village to keep that promise, dressed like any other villager. What he never expected was to be stopped at the gate of his own hometown and made to pay just to get in, by people who have no idea they're shaking down their emperor.",
    # 37.5M  Love's Detour to Destiny
    'love-s-detour-to-destiny':
        "Their third anniversary. Her husband in bed with someone else.\nMia Cole and Joe Holt are three years into their marriage, and on their anniversary she walks in on Joe in bed with Sue Cole. She asks for a divorce. Then she takes back her place as MY Corp's founder, and she beats Sue. Along the way the misunderstandings between Mia and Joe get cleared up, and they stick together through the good and the bad and end up happy. She nearly walked away from the man she was meant to be with.",
    # 34.0M  Love at Midnight
    'love-at-midnight':
        "She signed the divorce papers. Then she met Dereck.\nStella has signed her divorce agreement, and she's determined to leave her past behind for good. Then at a bar she meets Dereck, handsome and impossible to read, and he steps in at just the right moment to get her out of trouble. From there things between them start to heat up. She wanted a clean break, and instead she's falling for a man she barely knows.",
    # 30.6M  Alpha King's Silent Cinderella
    'alpha-king-s-silent-cinderella':
        "She lost her voice saving the Alpha King.\nTwenty years ago a girl saved Evan's life, and it cost her the ability to speak. Now Evan, the Alpha King, finds Claudia again. She can't say a word, and she's being mistreated. Fate keeps pulling them together while lies keep pushing between them, and Evan has to choose between his power, the vows he's made, and the girl he truly loves. She gave up her voice for him once. Now it's his turn to give something up.",
    # 26.6M  This Letter To You Is My Last
    'this-letter-to-you-is-my-last':
        "She's dying, and she's planned every detail of her goodbye.\nAda has a terminal illness, and she spends the time she has left setting up a farewell, every piece of it worked out in advance. Her husband Frank has hated her and humiliated her for a long time. Through the goodbye Ada leaves him, he finally learns the truth that was kept from him. By then it's too late. She's gone for good, and all Frank has left is regret that never ends.",
    # 24.3M  The Unwanted Wife Strikes Back
    'the-unwanted-wife-strikes-back':
        "He was cheating on her. He was stealing her designs too.\nShe's a housewife married to a big name in fashion. Then she finds out he's been unfaithful, and on top of that he's been taking her designs. So she divorces him, then goes after him with everything she has, out to take back the empire she quietly helped him build. To expose his lies she'll have to go to war with his mistress, who never stops scheming, and his sister, who's cold as ice. And she'll have to join forces with Cyrus Voss, the biggest rival her husband has. He built his name on her work, and now she wants all of it back.",
    # 20.9M  Reborn To Love Alpha King
    'reborn-to-love-alpha-king':
        "Betrayed, then reborn. Now she's going back to the Alpha King.\nChelsea Wharton was betrayed, and then she was reborn. This time she's set on finding her way back to the man she once loved. Her relatives are cruel and want her inheritance for themselves, so she has to outsmart them at every turn. She's fighting two battles at once, protecting the man she loves and protecting what's rightfully hers, and this time she means to change how her story ends.",
    # 19.2M  The Rejected Alpha Queen Comes Back
    'the-rejected-alpha-queen-comes-back':
        "She came home a wolfless nobody. She's the Alpha Queen.\nLucia is the Alpha Queen, but when she goes back to her home pack she arrives as an ordinary commoner with no wolf, hoping to be with her mate Frederick again. Instead she finds out he's betrayed her. He rejects her, and she's tortured. That's when she shows them who she really is and what she can do. With Neo, her true mate, she brings down Frederick's cruel rule, puts things right, and brings the whole pack together with herself at its head. Frederick threw away a queen, and now he has to answer to her.",
    # 17.3M  Roommate Benefits: The Governor's Son
    'roommate-benefits-the-governor-s-son':
        "She hid that she's an heiress for a man who betrayed her.\nMegan kept quiet about being an heiress because she was in love, and she gave her boyfriend everything. He betrayed her anyway. After they split she ends up sharing a home with Cole Warner, the governor's son, sexy, rebellious and a total bad boy. At first they can't stop fighting. Then the fighting turns into an attraction neither of them can get away from. She hid who she was for the wrong man, and the right one is the last guy she'd have picked.",
    # 15.3M  Bullies and Me
    'bullies-and-me':
        "New school, first day, and she's already at war with the Hayes brothers.\nChloe transfers to Blackstone Academy, and on her very first day she stands up to the Hayes brothers, the privileged elite of the school. After that she's marked as untouchable, and she can't get away from them. They become sworn enemies. But after one round of bullying after another, Archer starts to fall for her. Could Chloe ever feel the same about one of the boys who made her life miserable?",
    # 14.1M  Too Late, My Ex-Campus King
    'too-late-my-ex-campus-king':
        "One look at his computer and she was done.\nAria opens up Chase's computer by accident, and what she finds there are dozens of intimate photos of her boyfriend with Serena, his first love. That's the last straw. The same day she says yes to her family's plan for her to leave L.A., move to New York and run HMS Group. Chase has no idea what's going on in her head. He keeps up his murky friendship with Serena, crossing line after line and telling himself none of it means anything. By the time he figures it out, it'll be too late.",
    # 12.5M  My Secret Agent Husband 2
    'my-secret-agent-husband-2':
        "They survived the first time. Now the wedding is in danger again.\nLucas and Wyatt made it through everything that came at them the first time around, and they're finally starting a new chapter together. Lucas is doing great as CEO of CryptoLink. Wyatt, his secret agent husband, is juggling one undercover mission after another. Just as things start to feel steady, old dangers come back and new betrayals come to light. They've waited so long for their wedding, and once again it might not happen.",
    # 9.5M  How to Conquer the Celibate Lawyer
    'how-to-conquer-the-celibate-lawyer':
        "She's working at a strip club to get her mother out of prison.\nSonja's mother is locked up for something she didn't do, and to save her Sonja takes a job at a strip club. Then she spends one night with Bruce Cross, a powerful lawyer, and finds out she's pregnant with twins. The celibate lawyer has a family to protect now, and he'll stand up to anyone who tries to shame her.",
    # 8.5M  Married My CEO Ex In My 40s
    'married-my-ceo-ex-in-my-40s':
        "Her high school reunion. Her first love. A son who might be his.\nMary Larson is in her 40s and works hard as a housekeeper. At her high school reunion she runs into James Hastings. He was her first love, he's a rich man, and he's never stopped regretting that they split up. As the old feelings come back, Mary can't stop doubting herself, and her past still weighs on her. And she's keeping a secret that could change both their lives. James might be her son's father.",
    # 7.9M  Love You To Death
    'love-you-to-death':
        'Her perfect new boyfriend has a dark side.\nBrooke is a senior and a cheerleader, and her life looks perfect. She wants out of it. So when Nate transfers in as the new quarterback, she falls for him hard and fast, and things get hot and heavy. For a while everything is perfect. Then Brooke finds out how dark Nate can really get, and the boy she ran to may be the most dangerous thing in her life.',
    # 6.7M  The Sorority Hazed The Wrong Girl
    'the-sorority-hazed-the-wrong-girl':
        "They hazed the new girl for getting close to the campus king. She's his sister.\nLaci Richmond is a billionaire heiress and an equestrian champion, and she's starting fresh at Salem University. Then someone spots her with Edward, the campus king, and the rumors spread fast. Everyone decides she's his mistress. His girlfriend Victoria is the Queen Bee, and she's eaten up with jealousy, so she and her sorority sisters set out to make Laci's rush weekend hell. What none of them know is that Laci is Edward's sister. They picked the wrong girl.",
    # 5.9M  Playing It Real
    'playing-it-real':
        "She kissed a stranger to get rid of her ex. Now he wants something back.\nHer ex cheated on her, and to shake him off she kisses a handsome stranger. That stranger is no ordinary guy. He's the richest bachelor in town. Now he expects a favor back. So they agree to a contract marriage. It should be simple. The problem is she's falling for him a little more every day, and she can't stop it.",
    # 4.4M  My Ex's Brother Teaches Me to Puck
    'my-ex-s-brother-teaches-me-to-puck':
        "Her ex dumped her with an insult. His brother offered lessons.\nLily is a med student, and her boyfriend dumps her by calling her the girl nobody on campus would ever want to sleep with. So she teams up with his brother, Mason Clark, to learn how to be sexy. The lessons bring them closer, in their hearts and physically too, and Lily realizes Mason was the right one all along. Then her ex finds out she's moved on, and the rivalry between the two brothers blows up. Can the brothers fix what's broken between them so Lily and Mason can be together, or will her ex rip them apart?",
    # 3.2M  Love Me When I Am Gone
    'love-me-when-i-am-gone':
        "She married him in her twin sister's place. Three years, then she's gone.\nRosie needs money for her father's medical bills, so when her twin sister runs off, Rosie marries Mason in her place on a three year contract marriage. She gives him everything, and just as he finally starts to care for her, his first love comes back and Rosie's world falls apart. She puts up with being ignored and hurt, and the moment the three years end, she leaves and never looks back. When Mason finally learns the truth he's full of regret, but Rosie is already gone.",
    # 2.0M  Heartbreak High: Revenge on My First Love
    'heartbreak-high-revenge-on-my-first-love':
        "They humiliated his sister at prom, sure she was the other woman.\nBrody is the school's golden boy, and he's just put a promise ring on his girlfriend Alexis's finger. He can't wait to introduce her to Becca, his older sister, at prom. But Alexis gets it wrong and decides Becca is Brody's mistress, and she and her friends humiliate Becca viciously in the middle of the ballroom. Then Brody tells the truth about who Becca is, and Becca stands up and demands justice. Prom turns into a day of reckoning, and every bully, everyone who helped them and everyone who stood by and watched is going to pay.",
    # 0  No Escape from the Vampire
    'no-escape-from-the-vampire':
        "Her father gave her to the Vampire Emperor as a peace offering.\nSelina is the heiress of a legendary clan of vampire hunters. At the banquet for her 18th birthday, her own father hands her over to Lucien, the cold and bloodthirsty Vampire Emperor, to keep the peace. Selina would sooner die than give in to him. At their wedding she bites his lip until it bleeds, to show him where she stands. At midnight she climbs out of the castle window and runs. When desire takes hold of him, she goes for his heart with a dagger. But Lucien has made up his mind to tame her. He locks her inside his ancient castle, rips the deadly siren to shreds on her behalf, defies his entire vampire clan, and won't let her go even when she hurts him. A blood bond has tied these two sworn enemies together, and every time she tries to escape, her own body pulls her back toward him. Danger is moving in the shadows of the castle, and a love that began as possession could end in betrayal or in total surrender.",
}

FACTS = {
    'the-longlost-heiress-s-return':
        "Nova Park is lost due to an accident, and her mother Zoe Park, determined to find her, establishes the world’s largest conglomerate and offers a huge reward. Finally, she receives news of her daughter at a medical laboratory. However, when she arrives, she witnesses her daughter's dignity being crushed by opportunists. Determined, Zoe vows to teach them a harsh lesson.",
    'shifter-academy-taming-three-wild-mates':
        "What could possibly go wrong when a human girl spends mating season at a school full of apex predators? Everything. Ivy only wanted to finish her education. Instead, her scholarship to Shifter Academy comes with a catch: she's the fated mate of not one, not two, but three of the strongest shifters on campus: Ronan, Leon and Talon. Three alphas. One impossible choice. Her heart has chosen. It's love at first slap.",
    'trails-of-hope-his-journey-back-home':
        'Theo Levy lost contact with his parents 20 years ago due to a car accident. Fortunately, he was adopted by the chairman of Boyd Group, who raised him into the man he is today. Now that he has finally returned to his hometown, he swears to find his biological parents with the pendant he has.',
    'he-broke-the-heart-that-saved-him':
        "Mia sacrifices everything for her dying lover Vance, never knowing he is Cloud City's greatest heir. To return the future to him, Mia walks away resolutely without telling him she's pregnant. Years later, their child's tragic fate crosses their paths again. Yet vicious lies turn him against her, driving their boy to his death. Since then, Mia has lived in the pain of losing her son, while Vance, upon discovering the truth, will be left to bear the crushing weight of regret.",
    'sex-education-by-my-best-friend':
        'After a humiliating party, college student Emma turns to her childhood friend Chase, a charming playboy, to help rebuild her confidence. They agree to a simple rule, no kissing, but as they grow closer, feelings begin to develop. When the rule is broken, Emma must choose between the crush she once chased and the love that has been in front of her all along.',
    'fated-to-my-neighbor-boss':
        'After a one-night stand with Ethan, Sherry gives birth to twins. Katrina, her wicked stepsister, steals one of the babies, pretends to be his mother, and becomes Ethan’s fiancee. Six years later, Sherry returns as a famous perfumer Siren, exposes Katrina’s lies, reunites with her stolen child, and falls in love with Ethan.',
    'it-s-too-late-to-apologize':
        "Her husband accused her of trapping him. Her daughter wished for a different mom. Now she's gone. After one last betrayal, Zoey signs the divorce papers and disappears.What will they do when they realize she's never coming back?",
    'mafia-s-captive-bride':
        "Mafia boss Sebastian forces Elena into a marriage after she saves his life at her mother's grave. Elena, trapped by Sebastian, fights back, tames him, and falls in love amidst crises.",
    'masked-magnate-the-dominant-son-in-law':
        "After being reunited with his biological father, Chris Bell assumes the CEO position at the Olgow branch of Apex Group. However, at his father-in-law's birthday party, he faces rejection from the family table, labeled as a useless live-in son-in-law. His challenges escalate as his wife faces disdain alongside him, a suitor tries to take her away, developers attempt to forcibly demolish their home, and his daughter falls victim to a brutal attack by a wealthy man.",
    'return-of-his-majesty':
        'Before leaving his hometown, Leo Lowe makes a promise to his fiancée, Tina Leed, that once he becomes emperor, he will return to make her his empress. Years later, he successfully establishes a new dynasty and becomes the emperor of it, so he returns to the village disguised as an ordinary villager to fulfill his promise, not expecting to be forced to pay just to get through the entrance.',
    'love-s-detour-to-destiny':
        'Mia Cole has been married to Joe Holt for three years when she catches him in bed with Sue Cole on the day of their third wedding anniversary. After seeking a divorce, Mia reclaims her title as the founder of MY Corp and overcomes Sue, resolving the misunderstandings between herself and Joe. Having gone through thick and thin together, they finally end up as a happy couple.',
    'love-at-midnight':
        'After signing the divorce agreement, Stella determined to break free from the past. However, she met Dereck at a bar, a handsome and mysterious man whose appearance injected new sparks into the story. Dereck timely helped Stella out of trouble, and the relationship between the two began to heat up.',
    'alpha-king-s-silent-cinderella':
        'Saved by a girl who lost her voice for him, Alpha King Evan reunites with Claudia 20 years later—now mute and abused. Bound by fate and lies, he must choose between power, vows, and true love.',
    'this-letter-to-you-is-my-last':
        'Ada, diagnosed with a terminal illness, spends the final moments of her life orchestrating a carefully planned farewell. Through it, her husband Frank—who had long despised and humiliated her—finally uncovers the truth that had been hidden from him, only to lose her forever in a sea of endless regret.',
    'the-unwanted-wife-strikes-back':
        "When a housewife discovers her fashion mogul husband is cheating, and stealing her designs, she files for divorce and wages a scorched-earth revenge campaign to reclaim the empire she secretly helped build. But exposing his lies means going to war with his scheming mistress, his icy sister - and allying herself with Cyrus Voss, her husband's biggest rival.",
    'reborn-to-love-alpha-king':
        'Betrayed and reborn, Chelsea Wharton strives to return to her former love and battles wits with malicious relatives who covet her inheritance, changing her fate amidst the dual crises of protecting her love and her legacy.',
    'the-rejected-alpha-queen-comes-back':
        "Lucia, the Alpha Queen, returns to her home pack as a wolfless commoner to reunite with her mate, Frederick, only to discover his betrayal. Rejected and tortured, she reveals her true identity and power. With her true mate, Neo, she overthrows Frederick's tyranny, restores justice, and unites the pack under her rule. Love and vengeance intertwine in this tale of redemption and strength.",
    'roommate-benefits-the-governor-s-son':
        "Megan hid her heiress identity for love, only to be betrayed by the boyfriend she gave everything to. After their breakup, she unexpectedly ends up living under the same roof as Cole Warner—the governor's sexy, rebellious badboy son. What starts as constant clashes soon turns into an irresistible attraction neither of them can escape.",
    'bullies-and-me':
        'On the first day Chloe transfers to Blackstone Academy, she confronts the Hayes brothers—the privileged nobles here. She is labeled "untouchable" and is stuck with the bullying brothers. They become each other\'s biggest enemies. However, after a series of bullying incidents, Archer develops romantic feelings for Chloe. Will she return those feelings?',
    'too-late-my-ex-campus-king':
        "Aria accidentally opens her boyfriend Chase's computer – and what she finds shatters her world: dozens of intimate photos of Chase and his first love, Serena. The discovery becomes the final straw. That very day, Aria agrees to her family's plan – to leave L.A. for New York and take over HMS Group. Unaware of what's brewing in her heart, Chase continues his ambiguous friendship with Serena, blurring every line while convincing himself it's harmless...",
    'my-secret-agent-husband-2':
        "After surviving the chaos of their first adventure, Lucas and his secret agent husband, Wyatt, finally settle into a new chapter of their lives. Lucas is thriving as CryptoLink's CEO, while Wyatt juggles his undercover missions. But just when they think they’ve found stability, old threats resurface, new betrayals unfold, and their long-awaited wedding is once again in jeopardy.",
    'how-to-conquer-the-celibate-lawyer':
        'To save her wrongfully imprisoned mother, Sonja works at a strip club—until a one-night stand with powerful lawyer Bruce Cross leaves her pregnant with twins, and he becomes the man who fiercely protects her from anyone who dares to shame her.',
    'married-my-ceo-ex-in-my-40s':
        "Mary Larson, a hardworking housekeeper in her 40s, attends her high school reunion, where she reconnects with James Hastings, her wealthy first love who has never stopped regretting their separation. As old feelings resurface, Mary struggles with self-doubt, the weight of her past, and the secret that her son might be James's child.",
    'love-you-to-death':
        'Rebelling against her perfect life, high school senior cheerleader Brooke falls into a hot and heavy romance with transfer student and new QB Nate. Everything seems perfect. Until she discovers that Nate has a very dark side.',
    'the-sorority-hazed-the-wrong-girl':
        "Equestrian champion and billionaire heiress Laci Richmond arrives at prestigious Salem University ready for a new beginning. But when she's seen with campus king Edward, rumors explode—she’s instantly labeled his mistress. His girlfriend, the ruthless Queen Bee Victoria, is burning with jealousy. Together with her sorority sisters, she vows to make rush weekend a nightmare for Laci. There's just one problem… Laci is Edward's sister.",
    'playing-it-real':
        "To ditch my cheating ex, I kissed a handsome stranger. Turns out, he's not just anyone, but the richest bachelor in town! And now he wants something in return. So we're engaged in a contract marriage. What could possibly go wrong? The only thing is I'm slowly, uncontrollably, falling in love with him.",
    'my-ex-s-brother-teaches-me-to-puck':
        'When med student Lily gets dumped for being "the most unfuckable girl on campus," she teams up with her ex’s brother, Mason Clark, to learn the art of "sex appeal." However, as their lessons draw them closer emotionally as well as physically, Lily realizes Mason was the one all along. But when her ex discovers she’s moved on, the rivalry between the brothers explodes. Will the brothers be able to mend their bond and Lily be with Mason? Or will her ex tear them apart?',
    'love-me-when-i-am-gone':
        "To pay her father's medical bills, Rosie marries Mason in place of her runaway twin sister for a three-year contract. Just as her devotion finally wins his affection, his first love returns, shattering her world. Enduring neglect and heartbreak, Rosie leaves him without looking back the moment the three years are up. By the time Mason learns the truth and regrets his actions, she is already gone.",
    'heartbreak-high-revenge-on-my-first-love':
        "Golden-boy Brody gives his girlfriend, Alexis, a promise ring, excited for her to finally meet his older sister, Becca, at the prom. But when Alexis mistakes Becca for Brody's mistress, she and her clique brutally humiliate her in the ballroom. After Brody reveals the truth, Becca rises to demand justice, turning the prom into a reckoning where every bully, accomplice, and bystander must pay.",
    'no-escape-from-the-vampire':
        "On her 18th birthday banquet, Selina, the heiress of a legendary vampire hunter clan, is offered as a peace offering by her own father to Lucien, the cold, bloodthirsty Vampire Emperor. She would rather die than submit. She bites his lip to draw blood and draw a line between them at their wedding, climbs out the castle window at midnight in a desperate escape, and even drives a dagger toward his heart when he is consumed by desire. But Lucien is determined to tame this thorny rose. He imprisons her in his ancient castle, tears apart the deadly siren for her, stands his entire vampire clan, and refuses to let go even when she wounds him. The blood bond ties the fates of these two mortal enemies inextricably together. The more she tries to run, the more her body betrays her, pulling her irresistibly toward him. Dark currents swirl beneath the castle's stone walls, and deadly dangers lurk in the shadows. Will this forbidden love born of possession end in bitter betrayal or all-consuming surrender?",
}

SOURCES = {
    'the-longlost-heiress-s-return': ('platform', 'https://www.dramaboxdb.com/movie/41000113988/the-longlost-heiress-s-return'),
    'shifter-academy-taming-three-wild-mates': ('platform', 'https://www.dramaboxdb.com/movie/42000021919/shifter-academy-taming-three-wild-mates'),
    'trails-of-hope-his-journey-back-home': ('platform', 'https://www.dramaboxdb.com/movie/41000103670/trails-of-hope-his-journey-back-home'),
    'he-broke-the-heart-that-saved-him': ('platform', 'https://www.dramaboxdb.com/movie/42000023802/he-broke-the-heart-that-saved-him'),
    'sex-education-by-my-best-friend': ('platform', 'https://www.dramaboxdb.com/movie/42000009489/sex-education-by-my-best-friend'),
    'fated-to-my-neighbor-boss': ('platform', 'https://www.dramaboxdb.com/movie/41000113604/fated-to-my-neighbor-boss'),
    'it-s-too-late-to-apologize': ('platform', 'https://www.dramaboxdb.com/movie/42000001099/it-s-too-late-to-apologize'),
    'mafia-s-captive-bride': ('platform', 'https://www.dramaboxdb.com/movie/41000116575/mafia-s-captive-bride'),
    'masked-magnate-the-dominant-son-in-law': ('platform', 'https://www.dramaboxdb.com/movie/41000104224/masked-magnate-the-dominant-son-in-law'),
    'return-of-his-majesty': ('platform', 'https://www.dramaboxdb.com/movie/41000111652/return-of-his-majesty-dubbed'),
    'love-s-detour-to-destiny': ('platform', 'https://www.dramaboxdb.com/movie/41000104494/love-s-detour-to-destiny'),
    'love-at-midnight': ('platform', 'https://www.dramaboxdb.com/movie/41000106806/love-at-midnight'),
    'alpha-king-s-silent-cinderella': ('platform', 'https://www.dramaboxdb.com/movie/42000002456/alpha-king-s-silent-cinderella'),
    'this-letter-to-you-is-my-last': ('platform', 'https://www.dramaboxdb.com/movie/42000007571/this-letter-to-you-is-my-last'),
    'the-unwanted-wife-strikes-back': ('platform', 'https://www.dramaboxdb.com/movie/41000123150/the-unwanted-wife-strikes-back'),
    'reborn-to-love-alpha-king': ('platform', 'https://www.dramaboxdb.com/movie/42000007126/reborn-to-love-alpha-king'),
    'the-rejected-alpha-queen-comes-back': ('platform', 'https://www.dramaboxdb.com/movie/41000117514/the-rejected-alpha-queen-comes-back'),
    'roommate-benefits-the-governor-s-son': ('platform', 'https://www.dramaboxdb.com/movie/42000012856/roommate-benefits-the-governor-s-son'),
    'bullies-and-me': ('platform', 'https://www.dramaboxdb.com/movie/42000014119/bullies-and-me'),
    'too-late-my-ex-campus-king': ('platform', 'https://www.dramaboxdb.com/movie/42000005743/too-late-my-ex-campus-king'),
    'my-secret-agent-husband-2': ('platform', 'https://www.dramaboxdb.com/movie/41000112200/my-secret-agent-husband-2'),
    'how-to-conquer-the-celibate-lawyer': ('platform', 'https://www.dramaboxdb.com/movie/42000004163/how-to-conquer-the-celibate-lawyer'),
    'married-my-ceo-ex-in-my-40s': ('platform', 'https://www.dramaboxdb.com/movie/41000114449/married-my-ceo-ex-in-my-40s'),
    'love-you-to-death': ('platform', 'https://www.dramaboxdb.com/movie/42000000481/love-you-to-death'),
    'the-sorority-hazed-the-wrong-girl': ('platform', 'https://www.dramaboxdb.com/movie/42000009318/the-sorority-hazed-the-wrong-girl'),
    'playing-it-real': ('platform', 'https://www.dramaboxdb.com/movie/41000118506/playing-it-real'),
    'my-ex-s-brother-teaches-me-to-puck': ('platform', 'https://www.dramaboxdb.com/movie/42000024002/my-ex-s-brother-teaches-me-to-puck'),
    'love-me-when-i-am-gone': ('platform', 'https://www.dramaboxdb.com/movie/42000020710/love-me-when-i-am-gone'),
    'heartbreak-high-revenge-on-my-first-love': ('platform', 'https://www.dramaboxdb.com/movie/42000019210/heartbreak-high-revenge-on-my-first-love'),
    'no-escape-from-the-vampire': ('platform', 'https://www.anyreel.app/movie/no-escape-from-the-vampire-5708'),
}
