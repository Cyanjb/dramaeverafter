# -*- coding: utf-8 -*-
"""Caption batch 6 Oct 2026, part 4, titles imported 6 Oct (DramaBox 28 Sep data and Cyan's Reddit finds). STAGED FOR CYAN'S REVIEW, not approved.

31 titles, 29 written, 2 skipped. Every caption is written from the DramaBox book
the title page links to (availability.csv direct_link); each FACTS entry is the
platform's own synopsis as banked by the 28 Sep scrape (DramaBox refuses direct
fetches, so the banked text is the source).

SKIPPED, no story in the source, needs Cyan or a better source:
  fated-to-my-cruel-ceo: the DramaBox synopsis is a two sentence blurb (two orphans, a promise, "a fated reunion filled with love, secrets and echoes of their past") with no plot after the premise and nothing about the CEO in the title.
  ark-on-time: the DramaBox synopsis is a three line tagline (resurrected, she will reclaim love and career, make her enemies suffer) with no names, no setting and no story.
"""

CAPTIONS = {
    # 169.8M  Submitting to My Bestie's Dad
    'submitting-to-my-bestie-s-dad':
        "Her ex leaked her nudes. Her best friend's dad came to her rescue.\nJune's ex put her private photos out there, and the man who stepped in to save her was Killian. He's dark, he's dangerous, and he's her best friend's father. She knows that every time she walks into his private space she's betraying her friend, and she goes anyway. On purpose, she keeps whispering things meant to test how far his famous self control will hold. In his study, right and wrong stop mattering. Now they're playing a risky game of not getting caught, and what started as thanks has turned into obsession. Graduation is close, it's all one slip away from blowing up, and the person she's betraying is her best friend.",
    # 122.8M  Step Back! I'm the Hidden King
    'step-back-i-m-the-hidden-king':
        "She asked him to be her fake husband. He said no, then backed her for $100 billion.\nArthur is flying to New York when he meets Anya, the heiress to Throne Tech. She's being pushed into an arranged marriage, and her way out is a fake marriage, so she asks Arthur. He turns her down. But he raises her investment bid all the way to $100 billion. Later his fiancee Serena dumps him, and it's Anya who stands up for him. Then at a huge gala Arthur shows everyone who he really is, the CEO of Titan Group. He puts his money behind Anya, and they decide to start a new life together. Serena walked out on the Hidden King without ever knowing who he was.",
    # 93.4M  Flash Marriage with My Werewolf Husband
    'flash-marriage-with-my-werewolf-husband':
        "She ran from her stepfather and ended up in a flash marriage with her boss.\nLisa gets away from her abusive stepfather by taking a job at a New York law firm, and before she knows it she's in a flash marriage with the man she works for. She has her job to keep up with, and she has something else on her mind too. A werewolf attacked her once, and she wants to see it answer for what it did. Meanwhile her new husband is getting more and more suspicious of her. She's falling for him at the same time, and she can't work out what to do next. She's hunting a werewolf, and she's married to one.",
    # 82.8M  Forbidden Fling With My Bestie's Dad
    'forbidden-fling-with-my-bestie-s-dad':
        "She caught her fiance cheating on the plane. Then she slept with the bride's dad.\nMia is a grad student flying out to her best friend's wedding somewhere tropical, and on the way she finds out her fiance is cheating on her. She gets drunk and spends the night with Damien, a silver fox billionaire nobody seems to know much about. Then she learns who he is. He's the father of the bride. For the whole wedding weekend, with everything going wrong around them, they have to keep what's between them hidden. Jealous exes turn up, they keep sneaking off together, and someone out for revenge is trying to sabotage the wedding. Her best friend's big day could be ruined before anyone says I do.",
    # 59.2M  If I Never Loved You
    'if-i-never-loved-you':
        "She saved his family and his life. Then she told him she only wanted his money.\nFive years ago Nolan's family was bankrupt and his life was on the line, and Elena saved both. The money came from Victor, a mysterious billionaire, as a 30 billion investment, and the price Elena paid for it was her heart. Then she broke up with Nolan and lied, letting him believe she'd only ever cared about money. Now Nolan is a tycoon, and he's engaged to Sophia. Sophia is the one who schemed to ruin his family in the first place. He's about to marry the woman who brought him down, while the woman who saved him is the one he thinks sold him out.",
    # 51.4M  Your Husband is The Tech King
    'your-husband-is-the-tech-king':
        "Everyone sees a repairman. He's the Tech King.\nTo the people around him he's a modest repairman, but behind the scenes he's the one who keeps a whole tech empire from going under. The truth is he's the Tech King, the man who disappeared. His girlfriend is greedy, and that greed is why she betrays him. So he takes back his power and his pride. Along the way a brilliant CEO sees what he's really worth, stands with him, and becomes the one he loves. His girlfriend traded the Tech King for money and never knew it.",
    # 47.0M  Legally Sexy and Mr. Ice Cold
    'legally-sexy-and-mr-ice-cold':
        "One night with a billionaire left her pregnant. Her sister stole her place.\nSummer Ellis is still in law school when a single night with billionaire Leo Whitney leaves her pregnant. Her sister Angie is toxic, and she takes Summer's identity for herself and gets engaged to Leo. Six years go by. When Summer runs into Leo again she has a five year old daughter, Melody. Summer ends up as Leo's lawyer in a custody case, the truth that's been buried all this time starts coming back up, and so do the feelings. All those years Angie has been living the life that should have been Summer's.",
    # 44.1M  From Mail-Order Bride To Billionaire's Wife
    'from-mail-order-bride-to-billionaire-s-wife':
        "She became a mail order bride. Her farmer husband is a CEO.\nAnjelica's family betrays her and so does her boyfriend, so she signs on as a mail order bride and marries Eric. As far as she can tell he's a struggling farmer out in Montana. In truth he runs the Hawkins Group as its CEO. With Eric looking out for her, Anjelica starts hitting back at everyone who hurt her, one move at a time. The people who threw her away are the ones who are going to pay for it.",
    # 40.2M  Oops, I Lied About Sex with My Stepbrother
    'oops-i-lied-about-sex-with-my-stepbrother':
        "One impulsive lie, and it's about her new stepbrother.\nShe's always been the good girl. Then she tells a lie without thinking, a lie about sleeping with her new stepbrother, and it drags her into a back and forth with the one boy who was always off limits. Now they're stuck living under the same roof, and the secret games they play together make it harder and harder to tell what's pretend and what's real. The more they fight to stay in control, the further they fall, and what they want from each other could wreck them both.",
    # 36.5M  The Unrivaled Overlord
    'the-unrivaled-overlord':
        "He's the Overlord, with a Wolf Army a million strong. Nobody knows.\nTheo Larsen is known as the Overlord, and the Wolf Army he leads numbers a million. He keeps all of it hidden and marries Sarah Welsh, whose family has done very well for itself. Through that marriage he makes sure the Glory Group has a future, and then he rises to the very top. Sarah married the Overlord without knowing it.",
    # 35.7M  If Only You Loved Me More
    'if-only-you-loved-me-more':
        "She gave him her kidney. He married her to punish her.\nFive years ago Alex almost died saving Beth's life. Beth gave him one of her kidneys, and it left her with blood cancer. She went abroad for treatment, and while she was gone his secretary Stella told him two lies. She said Beth had walked out on him, and she said she was the one who gave him the kidney. Alex believed her. He married Beth out of spite and made her life a misery until her cancer came back. Only after he's lost everything does he learn the truth. Beth is the one who saved him, and she's the heiress of the Duncans, the richest family of all. By then the damage he did to her is done.",
    # 32.7M  Kneel Before The Dragon Queen
    'kneel-before-the-dragon-queen':
        "Seven years in hiding. The Dragon Queen comes back as a healer.\nVeya is the Dragon Queen, and she has spent seven years out of sight. When she comes back she's posing as a simple healer, and the man she used to love betrays her and humiliates her. She agrees to a marriage of convenience with Duke Kael Frostwing, a man with real power. Her enemies look at her and see a commoner with nothing behind her. They're wrong. Veya shows them exactly who she is and takes her throne back, and everyone who looked down on her has to kneel.",
    # 30.0M  Through Ashes Their Sorrow Awakens
    'through-ashes-their-sorrow-awakens':
        "Framed by her adopted sister, she does years in prison. Coming home is worse.\nAshley is the Langstons' real daughter, but Lilith, the girl they adopted, frames her, and Ashley spends years behind bars for it. When she's released nothing has changed. Her family still believes every lie Lilith tells, and so does Ethan, her fiance, and they all go on hurting her. Ethan even goes along with a fake wedding to Lilith just to keep her happy. On the day of that wedding Ashley makes it look as if she died in a fire, and she's gone for good. Only then does it hit them. The shock, the panic and the regret all come at once, and the daughter they refused to believe isn't coming back.",
    # 27.9M  The Return of the Unwanted Wife
    'the-return-of-the-unwanted-wife':
        "She bargained her life with a demon for his success. He handed her divorce papers.\nShe made a deal with a demon so the man she loved could rise all the way to the top. The terms were brutal. If he never came to love her back, she'd have to give up her life. Five years into the marriage her last hope that he'd warm to her is gone, because what he gives her is a divorce. The demon comes to take what it's owed. Then fate turns, and another woman gives up her own soul so that hers can be restored. Now she's back, and she has already paid with her life once for a man who never loved her.",
    # 24.9M  The Runaway Heiress
    'the-runaway-heiress':
        "She's about to marry the man she loves. His love was never real.\nVeronica comes from money, she's in love, and she's about to marry her fiance Logan. Then she realizes his feelings for her are fake. The whole thing is an elaborate scheme, and it was all done for the family's gain. Ellie has her own secret plan as well, to use Veronica's position and her fortune as a way of marrying into the family. Veronica was about to walk down the aisle to a man who never loved her.",
    # 21.7M  Boss, Your Executive Secretary has Resigned
    'boss-your-executive-secretary-has-resigned':
        "She gave up her career to be his secretary. Then the ambulance came.\nAnne was the chief jewelry designer, and she loved Jackson so much that she walked away from it all to work for him as his personal secretary and be his lover in secret. Then she sees Jackson and Melissa, his first love, carried out to an ambulance with no clothes on, both of them poisoned by carbon monoxide. Anne handles the whole mess, and after that she resigns and goes back to the career she gave up for him. She put her own work aside for a man who was with someone else, and now she's taking it back.",
    # 20.2M  Married a Secret Millionaire as a Substitute
    'married-a-secret-millionaire-as-a-substitute':
        "She married her sister's groom to pay her mother's bills.\nOlivia Walker is the Walker family's illegitimate daughter, and her mother's medical bills are more than she can cover. So she becomes a substitute bride and marries the man her sister was supposed to marry, a poor ex convict. What she doesn't know is who he really is. He's Andrew Smith, the richest man in Cascadia. She married him for her mother's sake, and from there their life together turns sweet, and dangerous too.",
    # 18.2M  A Dare to Kiss My Bad Boy
    'a-dare-to-kiss-my-bad-boy':
        "She came for her childhood crush. She got the school's bad boy.\nAvery Parker moves to Crestwood, an elite school, because Nathan is there, the boy she's liked since she was a kid. It goes wrong almost right away. One embarrassing accident and the whole campus is gossiping about her, and she keeps clashing with Jaxson Hale, the bad boy everyone at Crestwood has heard about. Between the bullying, the secrets and the rivalries, Avery learns Nathan isn't the boy she'd pictured. And Jax turns out to be loyal when she least expects it, which shakes everything she thought she knew about love, about trust and about giving someone a second chance.",
    # 16.4M  Lion's Dawn
    'lion-s-dawn':
        "She quit school to care for him through a three year coma.\nAfter a car crash Leo spent three years paralyzed and lying in a coma, and Davina left school so she could look after him. Nobody knew Leo was secretly heir to both the Thorne Group and the Brandohr family. At a fundraiser Joseph tries to take Davina, and that's when Leo wakes up. He calls his family, and they put a stop to Joseph. When the wedding comes, Davina's relatives laugh at Leo, until the Earl of Brandohr walks in with Cynthia and nobody says another word. After she spent three years caring for him, Leo proposes to Davina.",
    # 14.8M  Goodbye, My Dad's Best Friend
    'goodbye-my-dad-s-best-friend':
        "She fell for her dad's best friend. He never let her close.\nLena is in love with Elijah, her father's best friend, and for some reason he has always held her at arm's length. Then she finds out she's pregnant with his baby, which neither of them planned. Lena makes up her mind to walk away from him forever. But what's between them is too knotted up to walk away from, and she can't get free. She's carrying his child and trying to say goodbye to a man who would never let her in.",
    # 13.5M  The Hockey Star Can't Stop Missing Me
    'the-hockey-star-can-t-stop-missing-me':
        "She built his career in secret. He dropped her when his ex came back.\nDiana is the coach's daughter, and without anyone knowing it she's the reason her boyfriend Benson keeps rising. Then his ex shows up with a so called daughter, and Benson throws Diana away. He betrays her again and again, in front of everyone, and it pushes her toward Jake, the man who really loves her. With lies and betrayal on every side, Diana has to decide who she wants. Benson threw her away without knowing what she was doing for him.",
    # 11.3M  The Mafia's Forbidden Virgin
    'the-mafia-s-forbidden-virgin':
        "Her own mother tried to sell her. The mafia heir who stopped it is about to be her stepbrother.\nElena's mother tries to sell her virginity, and Kieran, a mafia heir, is the one who gets her out. Then Elena learns her mother is marrying Kieran's father, which makes them stepsiblings. It gets worse when Kieran turns up as her professor, and now she can't get away from him anywhere. He stands up for her when she's bullied, and at home the tension keeps building. What started as hostility between them turns into something dangerous, because he's the one man she's not allowed to want.",
    # 8.8M  Hi, Mr. Capricious
    'hi-mr-capricious':
        "On the day he got engaged, his mother made her end the pregnancy.\nEmma Blake is Aiden Steele's mistress. On the same day Aiden gets engaged to Isabella Rosewood, his mother forces Emma to have an abortion. To the Steele family a mistress isn't good enough to carry one of their children. Emma loses her baby while Aiden is promising himself to another woman.",
    # 8.4M  After Prison, Falling for the Billionaire Single Dad
    'after-prison-falling-for-the-billionaire-single-dad':
        "She thought her child was dead. Her billionaire boss has been raising that child all along.\nGrace spends one night with a CEO, and afterward her stepfather frames her. She goes to prison and is torn away from her child. When she gets out she starts over, working as a cleaner at that same CEO's company. She believes her child is dead, and she has no idea the CEO is quietly raising a child. As they get closer and fall in love, her past starts coming to light, and with it the truth. The child he's been raising is hers, and prison took all those years with her child away from her.",
    # 7.3M  A Heartbeat Away
    'a-heartbeat-away':
        "She left him because he was poor. Now he's a CEO.\nKatie walked out on her boyfriend Shaun without a second thought, because he didn't have money and she looked down on him for it. Years go by, and Shaun is now a young CEO standing right in front of her again. What he wants is for her to see she made the wrong choice. But little by little he starts to understand that the girl he's facing has loved him the whole time. So why did she leave?",
    # 6.7M  The God Level Blacksmith
    'the-god-level-blacksmith':
        "He's fighting for his sister's cure. Then the demons come.\nRonan Vire lives in a kingdom torn apart by war, and in secret he's the Iron Wraith. He's battling his way up the Hero's List because the top spot comes with the best medicine there is, and his little sister needs it to get well. Then he's pulled into the kingdom's war with the demons. With the whole realm about to fall, Ronan takes up his hammer, a weapon that changes shape and carries God level power, and he faces the demons with Princess Seraphina at his side and friends from the Noble Houses fighting with them. He started fighting to save one girl, and now a whole kingdom needs him.",
    # 3.7M  Oops! I Mate With My Forbidden Alpha
    'oops-i-mate-with-my-forbidden-alpha':
        "She's in love with her guardian. Everyone thinks he's family.\nCrystal Spear is about to come of age in a secret world of werewolves. Her pack expects certain things of her, and she's in love with the one person she shouldn't be. Theo is her guardian. Nobody knows much about him, and everyone believes he's related to her. Then the secrets start coming apart and the truth about who they both are comes out. What they feel for each other shakes everything their world is built on, and they'll have to fight all of it to be together.",
    # 2.9M  Hooking A CEO Daddy for Mommy
    'hooking-a-ceo-daddy-for-mommy':
        "He hired a boy to play his son. The boy has his face.\nJulian Morgan is a cold billionaire heir, and he's under pressure to produce an heir of his own. The one woman he's ever wanted disappeared after a single night with him. Then a little boy turns up who looks exactly like him. Julian offers to pay him to pretend to be his son, and the boy agrees on one condition, that his mom never finds out. The secret holds until Julian comes face to face with the boy's mother. She works in his factory, and she's the very woman he's spent all this time looking for.",
    # 1.2M  Stitched Hearts to the Billionaire’s Late Regret
    'stitched-hearts-to-the-billionaires-late-regret':
        "She let him think she was a gold digger. She did it to save him.\nYears ago Ethan was sick, and Ava gave up everything to save him without telling him. She acted like a gold digger so he'd go home and get treated. Five years on, their son Noah dies saving Ethan's grandmother. Ethan's fiancee humiliates Ava, and Ethan still can't see what really happened. So Ava finally tells him all of it. Ethan is full of regret, and it comes far too late. Ava won't forgive him.",
}

FACTS = {
    'submitting-to-my-bestie-s-dad':
        "What's worse than having your nudes leaked by an ex? Falling for the dark, dangerous man who rescued you—who also happens to be your best friend's dad. June knows every step into Killian's sanctuary is a betrayal, yet she deliberately tests his legendary restraint with whispered provocations. In the heat of his study, morality vanishes. As they play a high-stakes game of don't get caught,' gratitude blurs into obsession, threatening to explode before graduation.",
    'step-back-i-m-the-hidden-king':
        "On a New York-bound flight, Arthur meets Throne Tech heiress Anya, who offers a fake marriage to escape an arranged union. Arthur refuses, yet upgrades her investment bid to $100 billion. Later dumped by his fiancée Serena, Arthur is defended by Anya. At a grand gala, Arthur reveals himself as Titan Group's CEO. He funds Anya, and the two choose to build a new life together.",
    'flash-marriage-with-my-werewolf-husband':
        'To escape her abusive stepfather, Lisa takes the offer from a law firm in New York, where she unexpectedly flash-marries her boss. As she juggles work, she wants to bring the werewolf who once attacked her to justice, her boss becomes more and more suspicious… Caught between his mounting suspicion and her undeniable attraction to him, Lisa struggles with her next move.',
    'forbidden-fling-with-my-bestie-s-dad':
        "After catching her fiancé cheating on the flight to her best friend's tropical wedding, grad student Mia drunkenly hooks up with Damien, a mysterious silver-fox billionaire, only to discover he's the bride's father. Forced to hide their forbidden attraction throughout a chaotic wedding weekend, they face jealous exes, secret encounters, and vengeful sabotage that could destroy the ceremony.",
    'if-i-never-loved-you':
        "Five years ago, Elena sacrificed her heart to mysterious billionaire Victor for a 30 billion investment, saving Nolan's bankrupt family and his life, then lied about being money-driven to break up with him. Five years later, Nolan becomes a tycoon, engaged to Sophia, who actually plotted his family's downfall.",
    'your-husband-is-the-tech-king':
        "A humble repairman secretly saves a tech empire—revealed as the vanished Tech King. Betrayed by his girlfriend's greed, he reclaims power and dignity, while a brilliant CEO sees his true worth and becomes his new ally and love.",
    'legally-sexy-and-mr-ice-cold':
        "A one-night stand with billionaire Leo Whitney leaves law student Summer Ellis unexpectedly pregnant. Her toxic sister, Angie, steals Summer's identity and becomes Leo's fiancée. Six years later, Summer crosses paths with Leo again—this time with her five-year-old daughter, Melody. As Summer represents Leo in a custody case, the buried truth resurfaces, and love ignites.",
    'from-mail-order-bride-to-billionaire-s-wife':
        "Betrayed by her family and boyfriend, Anjelica marries as a mail-order bride to Eric, who appears to be a poor Montana farmer but is actually the CEO of the Hawkins Group. Under Eric's protection, she step-by-step counterattacks those who have hurt her.",
    'oops-i-lied-about-sex-with-my-stepbrother':
        "A good girl's impulsive lie pulls her into a dangerous, magnetic push-and-pull with the one boy she was never supposed to want—her new stepbrother. Forced under the same roof, their secret games blur the line between pretending and something forbidden. The harder they try to keep control, the deeper they fall into a desire that could ruin them both.",
    'the-unrivaled-overlord':
        'Theo Larsen, alias the Overlord, commands a Wolf Army of a million strong. Shrouding his identity, he ties the knot with Sarah Welsh, the daughter of the prosperous Welsh family, securing the future of Glory Group before ascending to the pinnacle of his life.',
    'if-only-you-loved-me-more':
        "Five years ago, Alex nearly died saving Beth, who donated her kidney to him, causing her blood cancer. While she sought treatment abroad, Alex's secretary Stella lied that Beth had left him and claimed she was his donor. Betrayed, Alex married Beth out of spite, torturing her until her illness returned. After losing everything, Alex learned Beth was his true savior and the heiress of the wealthiest Duncan family.",
    'kneel-before-the-dragon-queen':
        'After seven years in hiding, Dragon Queen Veya returns disguised as a humble healer, only to be betrayed and humiliated by the man she once loved. When she enters a marriage of convenience with powerful Duke Kael Frostwing, her enemies mistake her for a powerless commoner—until Veya reveals her true identity and reclaims her throne.',
    'through-ashes-their-sorrow-awakens':
        "Ashley, the Langstons' biological daughter, spends years in prison after Lilith, the adopted daughter, frames her. When she gets out, her whole family—including her fiancé Ethan—still believes Lilith's lies and keeps hurting her. To make Lilith happy, Ethan even agrees to a fake wedding with her. On the day of their wedding, Ashley stages her own death in a fire and leaves for good. That's when they're shocked, panicked, and burning with regret.",
    'the-return-of-the-unwanted-wife':
        'I made a deal with the demon for the man I love to reach his peak. The price was harsh: should he never love me in return, I’d have to give up my own life. Yet, after five years of marriage, my hope that his heart might soften towards me shattered completely. Instead of the love I yearned for, I was served divorce papers, a cold reminder of my failure. The demon came to collect its due, but in the twist of fate, a soul sacrificed her own to restore mine. Now that I’m back…',
    'the-runaway-heiress':
        "The story of a rich girl, Veronica, who is about to marry her beloved fiancé, Logan, but Veronica realizes that Logan's love isn't real, but an elaborate scheme for the benefit of the family. Ellie has been secretly planning to take advantage of Veronica's status and wealth to marry into the family.",
    'boss-your-executive-secretary-has-resigned':
        'Anne deeply in love with the Jackson, gives up her position as chief jewelry designer to become his personal secretary and secret lover, until she witnesses the Jackson and his first love Melissa being carried naked into an ambulance after carbon monoxide poisoning. After handling the situation, she decides to resign and return to her career.',
    'married-a-secret-millionaire-as-a-substitute':
        "In order to pay for her mother's medical expenses, Olivia Walker, the illegitimate child of the Walker family, marries a poor ex-convict in place of her sister. She has no idea that this man is, in fact, Andrew Smith, the richest person in Cascadia. Their lives then take a sweet but dangerous turn.",
    'a-dare-to-kiss-my-bad-boy':
        "Avery Parker transfers to elite Crestwood School hoping to reunite with her childhood crush, Nathan. Instead, a humiliating accident makes her the target of campus gossip and brings her into constant conflict with Jaxson Hale, the school's notorious bad boy. As bullying, secrets, and rivalries unravel, Avery discovers Nathan isn't who she imagined, while Jax's unexpected loyalty challenges everything she believes about love, trust, and second chances.",
    'lion-s-dawn':
        'Leo was paralyzed and in a coma for three years after a car accident. Davina dropped out of school to care for him. Leo was secretly the heir to the Thorne Group and Brandohr family. During a fundraiser, Joseph tried to take Davina, but Leo woke up and called his family, who stopped Joseph. At their wedding, Davina’s relatives mocked Leo, but Cynthia and the Earl of Brandohr appeared, silencing everyone. Leo then proposed to Davina.',
    'goodbye-my-dad-s-best-friend':
        'Lena falls in love with Elijah, her dad’s best friend, who has always kept her at a distance for some reason. Accidentally carrying his child, Lena plans to leave him for good but their tangled love traps her.',
    'the-hockey-star-can-t-stop-missing-me':
        'Diana, the coach\'s daughter who secretly powers her boyfriend Benson\'s rise, is discarded when his ex returns with a "daughter". Public betrayals from Benson push Diana toward Jake—the man who truly loves her. Amid lies and betrayal, how will she choose?',
    'the-mafia-s-forbidden-virgin':
        "After being rescued by Kieran, a mafia heir, from her mother's attempt to sell her virginity, Elena discovers her mother is marrying his father. Now step-siblings, their forbidden attraction intensifies when Kieran becomes her professor, forcing constant contact. From defending her against bullies to simmering home tension, hostility turns into dangerous desire.",
    'hi-mr-capricious':
        "On the day of Aiden Steele's engagement to Isabella Rosewood, Emma Blake was forced into abortion by Aiden’s mother. As the mistress, she was deemed unworthy to bear children for the Steele family.",
    'after-prison-falling-for-the-billionaire-single-dad':
        "Framed by her stepfather after a one-night encounter with the CEO, Grace is imprisoned and separated from her child. She rebuilds her life as a cleaner at the CEO's company, unaware that he is secretly raising the child that she thought was dead. As they grow closer and fall in love, the truth behind her past slowly reveals itself – that the child he's raising was hers!",
    'a-heartbeat-away':
        'Katie heartlessly abandoned her boyfriend Shaun because she looked down on his lack of wealth. Years later, Shaun becomes a young CEO and stands before Katie. He wants her to see her mistake in choosing, but he gradually realizes that the girl before him has actually always loved him.',
    'the-god-level-blacksmith':
        "In the shadows of a war-torn kingdom, Ronan Vire, the hidden Iron Wraith, fights for the top of the Hero's List in order to obtain the best medical resources to cure his little sister. However, he is then caught up in the battle between the kingdom and the demons. To save the realm from collapse, Ronan wields his shape-shifting hammer with God-level power and stands up against the demons with Princess Seraphina and allies from the Noble Houses.",
    'oops-i-mate-with-my-forbidden-alpha':
        'Crystal Spear, on the brink of adulthood in a hidden world of werewolves, finds herself torn between the expectations of her pack and the forbidden love she harbors for Theo, her guardian wrapped in mystery and believed to be kin. As secrets unravel and true identities come to light, their love becomes a beacon, challenging the fabric of their world and leading them to fight for a future where they can be together, against all odds.',
    'hooking-a-ceo-daddy-for-mommy':
        'Julian Morgan, a cold billionaire heir, is forced to produce an heir—but the only woman he ever wanted disappeared after a one-night stand. Then a boy appears... with his face. "Be my son. I\'ll pay you." "Deal. But my mom can\'t know." A perfect secret—until Julian meets the boy\'s mother working in his factory... and realizes she\'s the woman he\'s been searching for.',
    'stitched-hearts-to-the-billionaires-late-regret':
        "Years ago, Ava secretly sacrificed everything to save her sick lover, Ethan, and pretended to be a gold digger to force him home for treatment. Five years later, their son Noah died saving Ethan's grandmother. Humiliated by Ethan's fiancée while Ethan remained blind to the truth, Ava finally revealed everything. Ethan deeply regretted his actions, but Ava refused to forgive him.",
}

SOURCES = {
    'submitting-to-my-bestie-s-dad': ('platform', 'https://www.dramaboxdb.com/movie/42000015527/submitting-to-my-bestie-s-dad'),
    'step-back-i-m-the-hidden-king': ('platform', 'https://www.dramaboxdb.com/movie/42000017882/step-back-i-m-the-hidden-king'),
    'flash-marriage-with-my-werewolf-husband': ('platform', 'https://www.dramaboxdb.com/movie/41000101854/flash-marriage-with-my-werewolf-husband'),
    'forbidden-fling-with-my-bestie-s-dad': ('platform', 'https://www.dramaboxdb.com/movie/42000025978/forbidden-fling-with-my-bestie-s-dad'),
    'if-i-never-loved-you': ('platform', 'https://www.dramaboxdb.com/movie/42000004343/if-i-never-loved-you'),
    'your-husband-is-the-tech-king': ('platform', 'https://www.dramaboxdb.com/movie/42000001987/your-husband-is-the-tech-king'),
    'legally-sexy-and-mr-ice-cold': ('platform', 'https://www.dramaboxdb.com/movie/42000001178/legally-sexy-and-mr-ice-cold'),
    'from-mail-order-bride-to-billionaire-s-wife': ('platform', 'https://www.dramaboxdb.com/movie/42000010001/from-mail-order-bride-to-billionaire-s-wife'),
    'oops-i-lied-about-sex-with-my-stepbrother': ('platform', 'https://www.dramaboxdb.com/movie/42000007612/oops-i-lied-about-sex-with-my-stepbrother'),
    'the-unrivaled-overlord': ('platform', 'https://www.dramaboxdb.com/movie/41000102849/the-unrivaled-overlord'),
    'if-only-you-loved-me-more': ('platform', 'https://www.dramaboxdb.com/movie/41000122783/if-only-you-loved-me-more'),
    'kneel-before-the-dragon-queen': ('platform', 'https://www.dramaboxdb.com/movie/42000025240/kneel-before-the-dragon-queen'),
    'through-ashes-their-sorrow-awakens': ('platform', 'https://www.dramaboxdb.com/movie/42000000541/through-ashes-their-sorrow-awakens'),
    'the-return-of-the-unwanted-wife': ('platform', 'https://www.dramaboxdb.com/movie/41000105041/the-return-of-the-unwanted-wife'),
    'the-runaway-heiress': ('platform', 'https://www.dramaboxdb.com/movie/41000110283/the-runaway-heiress'),
    'boss-your-executive-secretary-has-resigned': ('platform', 'https://www.dramaboxdb.com/movie/42000001834/boss-your-executive-secretary-has-resigned'),
    'married-a-secret-millionaire-as-a-substitute': ('platform', 'https://www.dramaboxdb.com/movie/41000100891/married-a-secret-millionaire-as-a-substitute'),
    'a-dare-to-kiss-my-bad-boy': ('platform', 'https://www.dramaboxdb.com/movie/42000022499/a-dare-to-kiss-my-bad-boy'),
    'lion-s-dawn': ('platform', 'https://www.dramaboxdb.com/movie/41000111140/lion-s-dawn'),
    'goodbye-my-dad-s-best-friend': ('platform', 'https://www.dramaboxdb.com/movie/42000007456/goodbye-my-dad-s-best-friend'),
    'the-hockey-star-can-t-stop-missing-me': ('platform', 'https://www.dramaboxdb.com/movie/42000000485/the-hockey-star-can-t-stop-missing-me'),
    'the-mafia-s-forbidden-virgin': ('platform', 'https://www.dramaboxdb.com/movie/41000117875/the-mafia-s-forbidden-virgin'),
    'hi-mr-capricious': ('platform', 'https://www.dramaboxdb.com/movie/41000100743/hi-mr-capricious'),
    'after-prison-falling-for-the-billionaire-single-dad': ('platform', 'https://www.dramaboxdb.com/movie/42000011264/after-prison-falling-for-the-billionaire-single-dad'),
    'a-heartbeat-away': ('platform', 'https://www.dramaboxdb.com/movie/41000122437/a-heartbeat-away'),
    'the-god-level-blacksmith': ('platform', 'https://www.dramaboxdb.com/movie/42000018757'),
    'oops-i-mate-with-my-forbidden-alpha': ('platform', 'https://www.dramaboxdb.com/movie/42000000096/oops-i-mate-with-my-forbidden-alpha'),
    'hooking-a-ceo-daddy-for-mommy': ('platform', 'https://www.dramaboxdb.com/movie/42000021680/hooking-a-ceo-daddy-for-mommy'),
    'stitched-hearts-to-the-billionaires-late-regret': ('platform', 'https://www.dramaboxdb.com/movie/42000021679/stitched-hearts-to-the-billionaire-s-late-regret'),
}
