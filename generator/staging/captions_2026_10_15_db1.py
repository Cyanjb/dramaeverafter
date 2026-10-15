# -*- coding: utf-8 -*-
"""DramaBox batch 1 of the 14 Oct 2026 import (PR 55): the 34 highest-play
new DramaBox titles, written 15 Oct 2026 when Cyan said "you can go ahead now".
Facts from the DramaBox book each page LINKS to (staging/dramabox_2026-10-14.json),
not from the slug: doting-snake-lord shares a slug with a different ReelShort book.

NOT WRITTEN, the DramaBox page is a blurb with no names or story:
  shh-we-are-a-secret, maid-for-my-enemy-ceo
"""

BATCH_TAG = "DramaBox batch 1"

CAPTIONS = {
    # FACTS: Sean York is born into a respected family. For the past three years, he has been in a relationship w
    # FACTS: ith Mia Leed. But he gets injured in a car accident and falls into a coma. For his sake, Mia works m
    # FACTS: ultiple jobs to pay for his medical bills. Mia's relatives often mock and tease her. They introduce 
    # FACTS: Mia to the son of a wealthy family. However, as Mia resists, Sean wakes up. To return her favor, Sea
    # FACTS: n reclaims his title with his parents and confronts those who have wronged Mia. (https://www.dramabo
    # FACTS: xdb.com/movie/41000104043/the-dominant-heir-s-triumphant-return)
    'the-dominant-heir-s-triumphant-return':
        'He wakes up from a coma and finds out what she paid for it.\nSean York comes from a respected family, and he has been with Mia Leed for three years when a car crash leaves him in a coma. Mia takes on job after job to cover his hospital bills, while her own relatives laugh at her for it and keep pushing her toward the son of a rich family. She keeps saying no. Then Sean opens his eyes. To repay her, he takes back his place in his family as its heir and sets about making every person who mocked Mia answer for it. The heir is back, and he remembers exactly who stood by him.',
    # FACTS: Love, lies, and mistaken identities! … As Aileen Smith navigated her new life at work, she unexpecte
    # FACTS: dly fell deeply for her boss—THE BILLIONAIRE. But Aileen had been married for a year, although she a
    # FACTS: nd her husband's encounters were so scarce they could barely recall each other's faces. Through a se
    # FACTS: ries of jaw-dropping twists, Aileen was stunned to discover that the captivating CEO was, in fact, h
    # FACTS: er husband... (https://www.dramaboxdb.com/movie/41000105040/chasing-my-rejected-wife)
    'chasing-my-rejected-wife':
        "She's falling for her boss. She's also married to a man she can barely picture.\nAileen Smith has been married for a year, but she and her husband have met so rarely that neither of them could pick the other out of a crowd. Then she starts a new job and falls hard for the man she works for, a billionaire CEO who is everything her marriage is not. What she does not know is that the boss she cannot stop thinking about and the husband she cannot remember are the same man. Wait until she finds out.",
    # FACTS: Emily, a café worker who caught the groom cheating with the bridesmaid, decides to marry James, the 
    # FACTS: paramedic who saved her life, in a flash marriage to complete her dream wedding. However, she doesn'
    # FACTS: t know that James is the former billionaire CEO and the sole heir to a wealthy family. Emily, who ha
    # FACTS: d sworn never to get involved with rich people again, unknowingly falls in love with James, who is p
    # FACTS: retending to be an ordinary paramedic. (https://www.dramaboxdb.com/movie/41000118564/emergency-marri
    # FACTS: age-to-my-secret-billionaire)
    'emergency-marriage-to-my-secret-billionaire':
        'The groom cheated with the bridesmaid. So she married the paramedic.\nEmily works in a café, and she has just caught her groom with the bridesmaid. James is the paramedic who once saved her life, and she flash marries him so she still gets the wedding she always dreamed of. Emily swore off rich people a long time ago. That is a problem, because James is no ordinary paramedic. He used to be a billionaire CEO and he is the only heir to a wealthy family, and he keeps all of it hidden while she falls in love with him. How long can he keep pretending?',
    # FACTS: Lily, a young bakery worker, saves Mafia boss Salvatore with her rare blood, sparking a dangerous co
    # FACTS: nnection. After being sold by her stepmother, she’s rescued by him and thrown into a world of luxury
    # FACTS:  and violence. As they grow closer, they face betrayal, jealousy, and violence from those around the
    # FACTS: m, including his delusional 'fiancée' Bianca. Despite everything, their bond strengthens, culminatin
    # FACTS: g in their marriage and the birth of twins, marking a happy end. (https://www.dramaboxdb.com/movie/4
    # FACTS: 2000000042/bound-by-blood-the-mafia-king-s-sweetheart)
    'bound-by-blood-the-mafia-king-s-sweetheart':
        'Her rare blood saves a mafia boss. Then her stepmother sells her.\nLily works in a bakery, and when her rare blood saves the life of mafia boss Salvatore, they are tied together in a way that is dangerous for both of them. After her stepmother sells her off, it is Salvatore who rescues her, and suddenly she is living a life full of money and danger in equal measure. The closer they get, the more people want them apart. They are betrayed by those around them, and Bianca, who has convinced herself she is his fiancée, is one of the worst of them. Their love is tested at every turn, but they hold on, all the way to a wedding and twins.',
    # FACTS: Aidan Stein, the Eternal Lord Sovereign of the magnificent Eternity Palace, temporarily loses his me
    # FACTS: mory and intelligence due to his 60-year cycle. He lives alone in Vertania until he encounters Jade 
    # FACTS: Yule, who saves his life and becomes his wife. Years later, Jack Foley, an aristocrat of Vertania, d
    # FACTS: evelops an interest in Jade. He sends his men after Aidan, inadvertently triggering the resurgence o
    # FACTS: f his memories and power. (https://www.dramaboxdb.com/movie/41000102960/rising-dawn-the-awakening-of
    # FACTS: -power)
    'rising-dawn-the-awakening-of-power':
        "Every sixty years he forgets who he is.\nAidan Stein is the Eternal Lord Sovereign of Eternity Palace, and once in every sixty year cycle his memory and his mind are taken from him for a while. During one of those spells he ends up living alone in Vertania, until Jade Yule saves his life and marries him. Time passes. Then a Vertania aristocrat named Jack Foley sets his sights on Jade and sends his men after her husband. It is the worst mistake he could make, because the attack is exactly what brings Aidan's memories and his power flooding back.",
    # FACTS: Olivia is dragged by her husband Ryan to a couples-swapping getaway—only to be paired with Jake, the
    # FACTS:  husband of her closest friend Mia. Jake is magnetic, unreadable, relentless—nothing like the dull, 
    # FACTS: clueless husband Mia always described. And he won't stop closing in. As both men begin fighting for 
    # FACTS: Olivia's attention, and Mia's jealousy cracks in her perfect act, Olivia must uncover the real truth
    # FACTS:  behind the partner-swapping party before it's too late. (https://www.dramaboxdb.com/movie/420000281
    # FACTS: 73/love-is-a-dangerous-game)
    'love-is-a-dangerous-game':
        "Her husband takes her to a couples swap. She gets her best friend's husband.\nOlivia's husband Ryan drags her along to a partner swapping getaway, and the man she ends up paired with is Jake, married to her closest friend Mia. Mia always made Jake sound dull and clueless. He is nothing of the kind. He is magnetic, impossible to read, and he does not back off. Soon Ryan and Jake are both fighting for Olivia, and Mia's perfect act starts to slip as her jealousy shows through. Something is going on behind this weekend that nobody has told Olivia, and she needs to work out what it is before it's too late.",
    # FACTS: Gigi, seeking revenge on the insurance CEO who caused her father's death, offers her only $10,000 to
    # FACTS:  mafia boss Vito to buy his life. Amused by her persistence, Vito proposes she become his bride for 
    # FACTS: 90 days instead. Though he protects her, Vito's cynical nature leads him to refuse life-saving cance
    # FACTS: r surgery. Disheartened, Gigi believes she's just a pawn. When Gigi nearly miscarries, Vito realizes
    # FACTS:  his love and chooses to fight for life to protect her and their child. (https://www.dramaboxdb.com/
    # FACTS: movie/41000116865/mafia-s-90-day-bride)
    'mafia-s-90-day-bride':
        "She brings a mafia boss everything she has. He asks for 90 days.\nGigi blames an insurance CEO for her father's death, and she wants him to pay. So she goes to mafia boss Vito with the only money she has, ten thousand dollars, and asks him to take the man's life. Vito is amused by how hard she pushes, and he makes her a different offer: be his bride for 90 days. He keeps her safe. But Vito is so cynical about life that he turns down the cancer surgery that could save his own, and Gigi starts to believe she was only ever a pawn to him. It takes nearly losing their baby for Vito to see that he loves her, and to decide to fight to live for her and their child.",
    # FACTS: After being cast aside by the woman he helped rise to power, Arthur Storm—secret CEO of the powerful
    # FACTS:  Titan Group—is thrust back into the spotlight when a mysterious billionaire proposes marriage, shak
    # FACTS: ing high society to its core. (https://www.dramaboxdb.com/movie/42000004357/watch-out-i-call-the-fin
    # FACTS: al-shots)
    'watch-out-i-call-the-final-shots':
        'She rose because of him. Then she cast him aside.\nArthur Storm helped a woman climb all the way to power, and once she got there she threw him away. What few people know is that Arthur is the secret CEO of the Titan Group. He does not stay out of sight for long. A mysterious billionaire proposes to him, and the news sends shock waves through high society. Now everyone who wrote Arthur off is about to learn who has been calling the shots all along.',
    # FACTS: Ella is tricked by her divorce-seeking husband Arthur into sleeping with a stranger on their wedding
    # FACTS:  night, and later gives birth to twins, with one dumped on a hospital bench by him. Fisher, the stra
    # FACTS: nger and a billionaire, finds him and raises him. Years later, Ella serves as Fisher's physical ther
    # FACTS: apist in his estate, looking for her missing son. As the truth unravels, Ella finds her other son, a
    # FACTS: nd heals both him and Fisher. The family of four is eventually reunited. (https://www.dramaboxdb.com
    # FACTS: /movie/42000024547/my-billionaire-patient-is-my-baby-daddy)
    'my-billionaire-patient-is-my-baby-daddy':
        "Her husband set her up on their wedding night. Years later she is still looking for her son.\nElla's husband Arthur wants a divorce, so on their wedding night he tricks her into bed with a stranger. She has twins, and Arthur leaves one of the babies on a hospital bench. The stranger, Fisher, is a billionaire, and he finds the boy and brings him up himself. Much later, Ella takes a job as Fisher's physical therapist, living on his estate while she keeps looking for the son she lost. When the truth comes out she finds her other boy at last, and helps both him and Fisher heal. Four people who should have been a family all along finally are.",
    # FACTS: Charlotte signed a life-or-death contract to save her sister, agreeing to marry and work for Leo, th
    # FACTS: e arrogant CEO of Carter Group. For three years, Leo has treated her like a doormat—belittling her, 
    # FACTS: trampling her dignity, and taking credit for her success, convinced she’ll never leave. Now, as the 
    # FACTS: contract nears its end, her old flame Harper returns. Will Charlotte leave Leo, reclaim her life, an
    # FACTS: d reignite the spark with Harper? And will Leo realize what he’s lost? (https://www.dramaboxdb.com/m
    # FACTS: ovie/41000120352/doormat-no-more-the-toxic-ex-licks-my-feet)
    'doormat-no-more-the-toxic-ex-licks-my-feet':
        "Three years as his doormat. The contract is almost up.\nCharlotte signed a contract with life or death stakes to save her sister, and the terms were that she marry Leo, the arrogant CEO of Carter Group, and work for him. For three years he has walked all over her. He belittles her, strips her of her dignity and takes the credit for everything she achieves, certain she will never leave. Now the contract is about to run out, and Harper, the man she once loved, is back. Will Charlotte finally walk away from Leo and start again with Harper? And will Leo work out what he had before she's gone?",
    # FACTS: One rule at Blackwood Academy: never touch Damien Blackthorne, the cursed Alpha heir. But when he to
    # FACTS: uches Maya Whitefang — his rival's sister — their mate marks ignite. Now Maya must choose: the clan 
    # FACTS: that owns her, or the dangerous Alpha whose wolf calms only for her. (https://www.dramaboxdb.com/mov
    # FACTS: ie/42000023004/werewolf-academy-craving-the-forbidden-alpha)
    'werewolf-academy-craving-the-forbidden-alpha':
        "There is one rule at Blackwood Academy. Don't touch Damien.\nDamien Blackthorne is the Alpha heir with a curse on him, and everyone at Blackwood Academy knows to keep their hands off. Maya Whitefang is the sister of his rival. Then he touches her, and the mate marks on both of them burn to life. Now Maya has to choose between the clan that thinks it owns her and the dangerous Alpha whose wolf only settles when she is near. Which will she choose?",
    # FACTS: For five years, Finn Carter has silently fulfilled a contract signed with Renee Lane's mother—to hea
    # FACTS: l her daughter's shattered heart. Day by day, he builds a life with a woman who sees him as nothing 
    # FACTS: more than a placeholder for her first love. When Mike Smith's return coincides with the contract's e
    # FACTS: nd, Finn recognizes his cue to exit the stage of Renee's life. (https://www.dramaboxdb.com/movie/410
    # FACTS: 00113674/my-love-out-of-service)
    'my-love-out-of-service':
        "Five years as a stand in. The contract is about to end.\nFinn Carter signed a contract with Renee Lane's mother, and the job was to mend her daughter's broken heart. For five years he has done it without a word of complaint, building a whole life beside a woman who only ever saw him as someone to fill the space left by her first love. Then the contract runs out at the very moment Mike Smith, that first love, comes back. Finn knows his part is over and he is ready to walk away. But will Renee realize what she is losing before he's gone?",
    # FACTS: Aeron gives his Alpha wolf to his beloved mate Serena to fulfill her dream. After she abandons him, 
    # FACTS: he gains secret Lycan power blessed by the Moon Goddess. Years later, the ambitious Serena invades p
    # FACTS: acks for dominance. Aeron must face his former lover, fight dark forces, and protect his new friends
    # FACTS:  while hiding his true mighty identity. (https://www.dramaboxdb.com/movie/42000027406/the-betrayed-w
    # FACTS: olfless-is-the-lycan-king)
    'the-betrayed-wolfless-is-the-lycan-king':
        'He gave his wolf to his mate. She left him anyway.\nAeron gives up his own Alpha wolf so that Serena, the mate he loves, can have the dream she always wanted. She leaves him. Wolfless and alone, he is blessed by the Moon Goddess with a hidden Lycan power. Years later Serena has grown hungry for more and is invading other packs to take control. Aeron has to face the woman he gave everything to, fight off dark forces and keep his new friends safe, all without anyone learning who he really is. The Lycan King is hiding in plain sight.',
    # FACTS: Seven years ago, Luna Sawyer was pregnant when she discovered that her boyfriend, Samuel Payne—who w
    # FACTS: as battling cancer—was secretly the heir to Payne Corp in Reydon. Samuel was offered a deal: if he b
    # FACTS: roke up with Luna, they would pay for his treatment. But deeply in love with her, he rejected the of
    # FACTS: fer, unaware that Luna had overheard the conversation. Determined not to hold Samuel back, Luna sile
    # FACTS: ntly chose to leave—only to be presumed dead in a car accident. (https://www.dramaboxdb.com/movie/41
    # FACTS: 000115707/for-love-and-nothing-less)
    'for-love-and-nothing-less':
        'He turned down the money for her. So she disappeared.\nLuna Sawyer was expecting a baby seven years ago, and her boyfriend Samuel Payne was fighting cancer. Then she learned what Samuel had kept from her: he was the heir to Payne Corp, and he had been offered a deal: leave Luna, and his treatment would be paid for. Samuel loved her too much and said no. Luna overheard all of it, and she refused to hold him back. So she quietly left, and not long after, she was believed to have died in a car crash. But what if she never died at all?',
    # FACTS: Grace is drugged and framed by her jealous best friend Chloe at her boyfriend Ethan’s birthday party
    # FACTS: . Disoriented, she stumbles onto a hotel terrace and has a one-night stand with ruthless mafia don V
    # FACTS: incent. Waking up, Grace is horrified to find this mysterious man is Ethan’s powerful father. She tr
    # FACTS: ies to forget the mistake and stay with Ethan, yet Vincent keeps drawing near. Where will this forbi
    # FACTS: dden bond between Grace and Vincent lead... (https://www.dramaboxdb.com/movie/42000027414/claimed-by
    # FACTS: -my-boyfriend-s-mafia-dad)
    'claimed-by-my-boyfriend-s-mafia-dad':
        "One night with a stranger. He turns out to be her boyfriend's father.\nGrace's boyfriend Ethan is celebrating his birthday when her jealous best friend Chloe drugs her and sets her up. Dazed, Grace wanders out onto a hotel terrace and spends the night with Vincent, a ruthless mafia don. In the morning she is horrified to learn that the man is Ethan's father. She tries to put it behind her and stay with Ethan, but Vincent won't stay away, and he keeps getting closer. Where can a love this forbidden possibly go?",
    # FACTS: After his father dies, Kane is taken in by Eve, a gym owner. Bullied as a janitor, he hides his skil
    # FACTS: ls until gangsters threaten the gym. Kane defeats them but is forced into an underground death match
    # FACTS:  against the world champion—and wins, securing millions. Eve's kidnapped father is already dead. Kan
    # FACTS: e avenges him. Months later, the gym thrives. Kane and Eve find family and purpose together. (https:
    # FACTS: //www.dramaboxdb.com/movie/42000027254/what-if-i-m-one-hell-of-a-fighter)
    'what-if-i-m-one-hell-of-a-fighter':
        "Everyone at the gym thinks he's just the janitor.\nWhen Kane's father dies, Eve, who owns a gym, takes him in. He works there as the janitor, he gets bullied for it, and he never lets anyone see what he can really do. Then gangsters come after the gym, and Kane takes them all down. That lands him in a fight he can't walk away from, a fight to the death underground against the reigning world champion. He wins, and walks away with millions. Eve's father has been kidnapped and is already dead, and Kane makes the people responsible pay. Months later the gym is thriving, and Kane and Eve have found a family and a purpose in each other.",
    # FACTS: Betrayed by her lover Corrin and best friend Ophelia, Amber was stripped of her bloodline and brutal
    # FACTS: ly murdered. Reborn on the day she chose her bonded beast, she refuses the powerful Corrin and inste
    # FACTS: ad bonds with a lowly white dog Aerion, who tried to save her in the past life and later reveals his
    # FACTS:  true form—the legendary Sky Lion. Just as Amber begins her revenge against the betrayers, a darker 
    # FACTS: conspiracy unfolds, revealing the ultimate mastermind pulling the strings. (https://www.dramaboxdb.c
    # FACTS: om/movie/42000024579/my-weak-little-dog-is-a-legendary-sky-lion)
    'my-weak-little-dog-is-a-legendary-sky-lion':
        'Betrayed and murdered. Then reborn on the day she picks her beast.\nHer lover Corrin and her best friend Ophelia betrayed Amber. She lost her bloodline, and then her life, in the most brutal way. Then she wakes up reborn on the day she has to choose the beast she will be bonded to. This time she turns down the powerful Corrin and bonds instead with Aerion, a lowly white dog who once tried to rescue her in the life she lost. Aerion has a secret of his own: his true form is the legendary Sky Lion. Amber starts taking her revenge on the people who betrayed her, but a darker plot is unfolding underneath it, and someone else has been pulling the strings all along.',
    # FACTS: Disguised as an ordinary employee, billionaire founder Ryan Carter lends his Bugatti to arrogant man
    # FACTS: ager Bella. After she and her family steal, mock, and try to fire him, Ryan reveals his identity in 
    # FACTS: the boardroom—and makes them answer for every cruel choice. (https://www.dramaboxdb.com/movie/420000
    # FACTS: 26686/get-out-of-my-bugatti)
    'get-out-of-my-bugatti':
        'She borrowed his Bugatti and thought he was nobody.\nRyan Carter founded the company and is worth billions, but he goes to work disguised as an ordinary employee. He lends his Bugatti to Bella, an arrogant manager, and she and her family repay him by stealing from him, mocking him and doing their best to get him fired. Then comes the boardroom. Ryan drops the act and tells them exactly who he is, and every one of them is made to answer for the way they treated him.',
    # FACTS: Sold by her family to abusive suitors for magical spring water, fox attendant Sylvia — thought unabl
    # FACTS: e to bear children — turns up pregnant with triplets after a night with a stranger who's secretly th
    # FACTS: e Dragon King, Cassius. As he shields her from family, rivals, and jealous coworkers, an attack mean
    # FACTS: t to kill her instead reveals she's the long-lost princess of the Nine-Tailed Wolf Clan. Villains fa
    # FACTS: ll; Cassius claims her as his queen. (https://www.dramaboxdb.com/movie/42000023840/pregnant-with-the
    # FACTS: -dragon-king-s-triplets)
    'pregnant-with-the-dragon-king-s-triplets':
        "They said she couldn't have children. Then she's carrying triplets.\nSylvia is a fox attendant, and her own family sells her off to cruel suitors in exchange for magical spring water. Everyone believes she can't have children, until one night with a stranger leaves her pregnant with triplets. The stranger is Cassius, and he is secretly the Dragon King. He stands between her and her family, rivals and jealous coworkers. Then an attack meant to kill her reveals who she really is. She is the Nine Tailed Wolf Clan's lost princess. The villains fall, and Cassius makes her his queen.",
    # FACTS: Ingrid Voss must finish her summer internship at the country club without anyone finding out that sh
    # FACTS: e's the heiress to the Voss Empire. However, she meets Jordan Temple, the second son of the powerful
    # FACTS:  Temple Holdings. (https://www.dramaboxdb.com/movie/41000120780/serve-me-ball-girl-heiress)
    'serve-me-ball-girl-heiress':
        "One summer at the country club. Nobody can know she's the heiress.\nIngrid Voss has a summer internship to get through at the country club, and the whole point is that nobody there finds out she is the Voss Empire's heiress. Keeping her head down should be simple enough. Then Jordan Temple comes along, second son of the family behind Temple Holdings, and a quiet summer is suddenly the last thing she's going to get.",
    # FACTS: Linda gave up her billionaire legacy for her husband Nick. A ransom call shatters her perfect life: 
    # FACTS: Nick and their daughter have been kidnapped. Rushing to pay the ransom, she's forced to trade her fr
    # FACTS: eedom for Nick's mistress Claire. She endures three years of torture in a drug lab. When Linda final
    # FACTS: ly escapes and returns as the billionaire heiress of the Hastings Group, she's ready to make everyon
    # FACTS: e who betrayed her kneel at her feet. (https://www.dramaboxdb.com/movie/42000026621/your-dumped-hous
    # FACTS: ewife-is-your-boss)
    'your-dumped-housewife-is-your-boss':
        "She paid the ransom with her own freedom.\nLinda walked away from her billionaire family's legacy to marry Nick. Then a ransom call tears her perfect life apart: someone has taken Nick and their daughter. She rushes to pay, and ends up forced to give up her own freedom in exchange for Nick's mistress Claire. Linda spends three years held in a drug lab and tortured. When she finally escapes, she comes back as the Hastings Group's billionaire heiress, and everyone who betrayed her is going to end up on their knees.",
    # FACTS: Frank, a small-town boy, hastily married urbanite Andrew, chosen by his grandmotherly friends, witho
    # FACTS: ut recognizing each other. Andrew disappeared after going abroad for work. A year later, Frank's bos
    # FACTS: s, the wealthy and charming Andrew, pursued him, leading to an affair. The once-playboy Andrew learn
    # FACTS: ed commitment and restraint, while Frank, once betrayed, regained trust and learned to love freely. 
    # FACTS: At the divorce site, Frank discovered his husband and boss were the same person. (https://www.dramab
    # FACTS: oxdb.com/movie/41000110039/desired-by-my-unknown-husband)
    'desired-by-my-unknown-husband':
        "He married a stranger. A year later the stranger is his boss.\nFrank is a small town boy, and he married Andrew, a man from the city, in a hurry because a group of grandmotherly friends picked him out. Neither of them ever really knew who the other was. Andrew went abroad for work and disappeared. A year later Frank's wealthy, charming boss Andrew starts pursuing him, and they begin an affair. Andrew, who used to be a playboy, learns what commitment means. Frank, who has been betrayed before, learns to trust and love freely again. It's only when they meet to sign the divorce papers that Frank discovers his husband and his boss were the same man all along.",
    # FACTS: After a one-night stand, they accidentally reunite at the registry office and get married, pretendin
    # FACTS: g to be poor to each other after marriage. The heroine is constantly at war with the female antagoni
    # FACTS: st to reclaim her mother's company, during which the hero's true identity gradually surfaces, trigge
    # FACTS: ring a series of conflicts and crises. In the process of reclaiming her mother's relics, their relat
    # FACTS: ionship heats up. (https://www.dramaboxdb.com/movie/41000106479/double-contract-love)
    'double-contract-love':
        "A one night stand, then a marriage. Both of them pretending to be broke.\nAfter one night together, they run into each other again by accident at the registry office and end up married. Each one pretends to the other to be poor. She is locked in a running battle with a rival woman to win back her mother's company, and all the while the truth about who her husband really is keeps slipping out, setting off one crisis after another. The harder she fights to get back what her mother left her, the hotter things get between them.",
    # FACTS: Years ago, Layla York, Balton’s Valkyrie, believed Sean Groff had saved her life, and that belief le
    # FACTS: d to their marriage. Over the past three years, she has devoted herself to him and his family, aidin
    # FACTS: g in his ascent to prominence and facilitating his entry into the Onyx Group. She plans to announce 
    # FACTS: his appointment as CEO during the Phoenix Gala. (https://www.dramaboxdb.com/movie/41000103801/ablaze
    # FACTS: -with-vengeance)
    'ablaze-with-vengeance':
        "She built his career on a rescue she believed in.\nLayla York is Balton's Valkyrie, and years ago she believed Sean Groff saved her life. That belief is why she married him. For three years she has given everything to Sean and his family, helping him rise and getting him into the Onyx Group. Now she is about to announce him as CEO at the Phoenix Gala. But what if the man she married never saved her at all?",
    # FACTS: Abandoned on an island by her father King John, Ingrid is summoned back when her stepmother Martha a
    # FACTS: nd stepsister Lilith covet her betrothal to Lucifer, the King of Hell. Scorned as an ignorant shephe
    # FACTS: rdess, she can secretly communicate with all living things and wields great healing power. Lucifer d
    # FACTS: isrupts her revenge: she once hid him, unaware of his identity, then fled. Seeing through her act, h
    # FACTS: e grips her chin and claims her as his own. This time, he won't let her escape. (https://www.dramabo
    # FACTS: xdb.com/movie/42000027417/my-demon-lord-your-shepherd-girl-has-run-away-again)
    'my-demon-lord-your-shepherd-girl-has-run-away-again':
        'Abandoned on an island. Engaged to the King of Hell.\nKing John left his daughter Ingrid behind on an island. He only calls her home because her stepmother Martha and stepsister Lilith want the one thing she has, her engagement to the King of Hell himself, Lucifer. Everyone writes her off as an ignorant shepherd girl. Secretly she can speak with every living thing and has a great gift for healing. She has her revenge planned, but Lucifer gets in the way. Once, without knowing who he was, she hid him and then ran off. Now he sees straight through her act, takes her by the chin and makes it clear she belongs to him. And this time he is not letting her run.',
    # FACTS: Five years ago, Callista Summers rescued Jeremiah Fuller when he was drugged. She then pursued her c
    # FACTS: areer abroad, driven by her initial self-doubt as a housekeeper. Over time, Callista became a renown
    # FACTS: ed designer and a devoted mother to her son, Scotty Fuller. When she learns of Jeremiah’s kidney fai
    # FACTS: lure, she selflessly returns to donate her kidney, saving him once more. However, misunderstandings 
    # FACTS: breed animosity between them. (https://www.dramaboxdb.com/movie/41000102839/a-breath-away-from-forev
    # FACTS: er)
    'a-breath-away-from-forever':
        "She saved him once. Five years later she saves him again.\nFive years ago Callista Summers was a housekeeper, and she rescued Jeremiah Fuller the night he was drugged. Unsure of herself, she left to build a career abroad. Since then she has become a famous designer, and she is raising her son Scotty Fuller with all the love she has. Then she hears that Jeremiah's kidneys are failing, so she comes back and gives him one of hers. But misunderstandings turn them against each other, and saving his life may not be enough to win his heart.",
    # FACTS: Cade Leed raises his sick younger sister, Amy Leed, on his own despite his young age. Though it brea
    # FACTS: ks his heart, Cade has no choice but to put her up for adoption, hoping that a family with resources
    # FACTS:  can provide the treatment she needs. Twenty years later, Cade falls into a coma after an accident, 
    # FACTS: and his fiancée, Rue Kirk, cares for him tirelessly for five years, never giving up hope. (https://w
    # FACTS: ww.dramaboxdb.com/movie/41000104235/awakened-his-absolute-might-unleashed)
    'awakened-his-absolute-might-unleashed':
        'He gave up his little sister so she could live.\nCade Leed is barely more than a kid himself when he takes on raising his sick little sister Amy alone. It breaks his heart, but he puts her up for adoption, hoping a family with money can get her the care she needs. Two decades on, an accident leaves Cade in a coma, and Rue Kirk, the woman he is engaged to, looks after him for five years without ever losing hope. When he wakes, the power he has kept hidden is about to be unleashed.',
    # FACTS: Chloe Ashford spent three years hiding behind an ugly disguise, believing her billionaire husband lo
    # FACTS: ved her soul. But when Ethan Sterling gives her anniversary gown to his first love, Chloe discovers 
    # FACTS: she was only his weapon against his family. She unveils her true beauty, files for divorce, and rise
    # FACTS: s as Vesper—a fashion genius no one can control. Now Ethan wants her back, but Chloe has learned: sh
    # FACTS: e doesn`t need a savior. (https://www.dramaboxdb.com/movie/42000023914/billionaire-s-ugly-ex-wife-is
    # FACTS: -a-goddess)
    'billionaire-s-ugly-ex-wife-is-a-goddess':
        "Three years in disguise. Then he gave her gown to his first love.\nChloe Ashford hid behind an ugly disguise for three years, believing her billionaire husband Ethan Sterling loved her for who she was inside. Then he gives the gown meant for their anniversary to his first love, and Chloe learns the truth: she was never anything more than a weapon he was using against his own family. She drops the disguise, files for divorce, and reinvents herself as Vesper, a brilliant designer who answers to no one. Now Ethan wants her back. Too bad she isn't looking to be saved.",
    # FACTS: Hercules, the son of Zeus and Hera, goes missing as a child and is swapped with the mortal Icaris by
    # FACTS:  an envious follower. Eighteen years later, Hercules travels to Olympus to join the Divine Guards to
    # FACTS:  save his beloved, far outperforming Icaris. Unaware of his true identity, Zeus's family, instigated
    # FACTS:  by Icaris, cruelly suppress and exile him. Once the truth is revealed, Zeus's family desperately be
    # FACTS: gs for forgiveness, while Icaris conspires with Hades for revenge. (https://www.dramaboxdb.com/movie
    # FACTS: /42000023820/the-lost-son-of-zeus-his-return)
    'the-lost-son-of-zeus-his-return':
        "The real son of Zeus, replaced by a mortal.\nZeus and Hera lose their son Hercules when he is only a small child, and a jealous follower puts a mortal boy called Icaris in his place. Eighteen years later Hercules goes to Olympus hoping to win a place in the Divine Guards so he can save the woman he loves, and he outshines Icaris at every turn. Zeus's family have no idea who he really is. Egged on by Icaris, they crush him and send him into exile. When the truth comes out they are begging him to forgive them, while Icaris joins forces with Hades to get his revenge.",
    # FACTS: Reborn before her tragic fate unfolds, Elena gets a second chance at life. In her previous life, she
    # FACTS:  was betrayed by her sister Veronica and fiancé Grayson, framed for infidelity, and pushed into the 
    # FACTS: Dragon Pit to her death. Determined to change her destiny, Elena turns to Nidhogg, the imprisoned Dr
    # FACTS: agon Progenitor, and unexpectedly becomes pregnant with his nine heirs. (https://www.dramaboxdb.com/
    # FACTS: movie/42000016034/doting-snake-lord)
    'doting-snake-lord':
        "Thrown into the Dragon Pit. Then reborn before it happens.\nElena's sister Veronica and her fiancé Grayson betrayed her, framed her for cheating and threw her into the Dragon Pit to die. Then she wakes up reborn, with all of it still ahead of her, and a second chance to live her life differently. Determined to change how her story ends, Elena goes to Nidhogg, the Dragon Progenitor who has been locked away, and to her shock ends up pregnant with his nine heirs. This time it's her enemies who should be afraid.",
    # FACTS: With the help of his grandfather, Dave Quinn marries Tessa Gray, a girl he does not know much about.
    # FACTS:  After marriage, Tessa works in Quinn Corp as a cleaner and makes Dave promise to keep their relatio
    # FACTS: nship a secret from their colleagues. However, some of her colleagues show disdain towards her, espe
    # FACTS: cially Dave’s childhood sweetheart, Lana Harris, who has a crush on him. Out of jealousy, Lana sets 
    # FACTS: Tessa up in an attempt to get rid of her, hoping to ruin her marriage with Dave. (https://www.dramab
    # FACTS: oxdb.com/movie/41000108064/signed-sealed-secretly-married)
    'signed-sealed-secretly-married':
        "Secretly married, and working as a cleaner at his company.\nDave Quinn's grandfather helps arrange his marriage to Tessa Gray, a girl he hardly knows. After the wedding Tessa takes a job as a cleaner at Quinn Corp, and she makes Dave promise their colleagues will never find out they are married. Some of them look down on her anyway, none more than Lana Harris, Dave's childhood sweetheart, who has always had a crush on him. Jealous, Lana sets Tessa up to get her out of the way and break up the marriage. How long can a secret like this stay buried?",
    # FACTS: I spent five grueling years transforming from a mocked fat girl into an upcoming international model
    # FACTS: . My global debut lands at the same hotel as my high school bullies' reunion. Josephine, my tormento
    # FACTS: r, dug up a humiliating old video and tagged me, while classmates bet I'd never show. I replied calm
    # FACTS: ly and vowed to arrive on time—and make them all pay. (https://www.dramaboxdb.com/movie/42000026723/
    # FACTS: don-t-mess-with-the-xxl-girl)
    'don-t-mess-with-the-xxl-girl':
        "Her bullies' reunion. Her international debut. Same hotel.\nShe was the fat girl everyone laughed at, and she has spent five hard years turning herself into a rising international model. Her global debut happens to be at the same hotel where her old high school bullies are holding their reunion. Josephine, the girl who tormented her most, finds an old video that humiliated her, posts it and tags her, while her classmates bet she won't dare show up. She answers calmly and promises she'll be there on time. And she intends to make every one of them pay.",
    # FACTS: Mia Blackridge, the youngest daughter of Blackridge Pack's Alpha, is widely seen as a useless dumb p
    # FACTS: up who can't even shift into wolf form. Secretly, she is the reborn soul of a former Pack Alpha who 
    # FACTS: ruled for 70 years. When the scheming Beta Grady forges a royal Crown Order to execute her father an
    # FACTS: d wipe out the whole pack, Mia steps forward, exposes the fake seal, outplays the enemy forces with 
    # FACTS: her lifelong wisdom, and saves her entire pack from ruin. (https://www.dramaboxdb.com/movie/42000026
    # FACTS: 722/wipe-out-my-pack-a-dumb-pup-turned-the-tables)
    'wipe-out-my-pack-a-dumb-pup-turned-the-tables':
        "The pack's useless pup once led a pack for seventy years.\nMia Blackridge is the youngest daughter of the Blackridge Pack's Alpha, and everyone thinks she's a dumb pup who cannot even turn into her wolf. What nobody knows is that her soul is reborn from an Alpha who once led a pack for seventy years. Then Beta Grady, who has been plotting all along, fakes an order in the Crown's name to have her father executed and the whole pack wiped out. Mia is the one who steps up. She proves the seal is a fake, outthinks the enemy with a lifetime of experience, and saves everyone from ruin.",
    # FACTS: She gave him her heart, only to be used as a pawn to win her cruel stepsister. Shattered, the gifted
    # FACTS:  Keeper Allie walks away—straight into the devotion of an ancient Original who has waited two centur
    # FACTS: ies for her. Watching her reign alongside a far superior man, her ex falls to his knees begging for 
    # FACTS: a second chance. Too late. She destroys her enemies and chooses true love, leaving the boy who broke
    # FACTS:  her choking on regret. (https://www.dramaboxdb.com/movie/42000024553/no-more-blood-for-my-vampire-f
    # FACTS: irst-love)
    'no-more-blood-for-my-vampire-first-love':
        "He used her to win her stepsister.\nAllie gave him her heart, and he used her as a pawn to win over her cruel stepsister. Broken, the gifted Keeper walks away, and straight into the arms of an Original who is centuries old and has spent two hundred years waiting for her. Now her ex has to watch her rule beside a far better man, and he ends up on his knees, pleading for a second chance. It's too late. Allie takes down her enemies, chooses real love, and leaves the boy who broke her heart drowning in regret.",
}

SOURCES = {
    'the-dominant-heir-s-triumphant-return': ('platform', 'https://www.dramaboxdb.com/movie/41000104043/the-dominant-heir-s-triumphant-return'),
    'chasing-my-rejected-wife': ('platform', 'https://www.dramaboxdb.com/movie/41000105040/chasing-my-rejected-wife'),
    'emergency-marriage-to-my-secret-billionaire': ('platform', 'https://www.dramaboxdb.com/movie/41000118564/emergency-marriage-to-my-secret-billionaire'),
    'bound-by-blood-the-mafia-king-s-sweetheart': ('platform', 'https://www.dramaboxdb.com/movie/42000000042/bound-by-blood-the-mafia-king-s-sweetheart'),
    'rising-dawn-the-awakening-of-power': ('platform', 'https://www.dramaboxdb.com/movie/41000102960/rising-dawn-the-awakening-of-power'),
    'love-is-a-dangerous-game': ('platform', 'https://www.dramaboxdb.com/movie/42000028173/love-is-a-dangerous-game'),
    'mafia-s-90-day-bride': ('platform', 'https://www.dramaboxdb.com/movie/41000116865/mafia-s-90-day-bride'),
    'watch-out-i-call-the-final-shots': ('platform', 'https://www.dramaboxdb.com/movie/42000004357/watch-out-i-call-the-final-shots'),
    'my-billionaire-patient-is-my-baby-daddy': ('platform', 'https://www.dramaboxdb.com/movie/42000024547/my-billionaire-patient-is-my-baby-daddy'),
    'doormat-no-more-the-toxic-ex-licks-my-feet': ('platform', 'https://www.dramaboxdb.com/movie/41000120352/doormat-no-more-the-toxic-ex-licks-my-feet'),
    'werewolf-academy-craving-the-forbidden-alpha': ('platform', 'https://www.dramaboxdb.com/movie/42000023004/werewolf-academy-craving-the-forbidden-alpha'),
    'my-love-out-of-service': ('platform', 'https://www.dramaboxdb.com/movie/41000113674/my-love-out-of-service'),
    'the-betrayed-wolfless-is-the-lycan-king': ('platform', 'https://www.dramaboxdb.com/movie/42000027406/the-betrayed-wolfless-is-the-lycan-king'),
    'for-love-and-nothing-less': ('platform', 'https://www.dramaboxdb.com/movie/41000115707/for-love-and-nothing-less'),
    'claimed-by-my-boyfriend-s-mafia-dad': ('platform', 'https://www.dramaboxdb.com/movie/42000027414/claimed-by-my-boyfriend-s-mafia-dad'),
    'what-if-i-m-one-hell-of-a-fighter': ('platform', 'https://www.dramaboxdb.com/movie/42000027254/what-if-i-m-one-hell-of-a-fighter'),
    'my-weak-little-dog-is-a-legendary-sky-lion': ('platform', 'https://www.dramaboxdb.com/movie/42000024579/my-weak-little-dog-is-a-legendary-sky-lion'),
    'get-out-of-my-bugatti': ('platform', 'https://www.dramaboxdb.com/movie/42000026686/get-out-of-my-bugatti'),
    'pregnant-with-the-dragon-king-s-triplets': ('platform', 'https://www.dramaboxdb.com/movie/42000023840/pregnant-with-the-dragon-king-s-triplets'),
    'serve-me-ball-girl-heiress': ('platform', 'https://www.dramaboxdb.com/movie/41000120780/serve-me-ball-girl-heiress'),
    'your-dumped-housewife-is-your-boss': ('platform', 'https://www.dramaboxdb.com/movie/42000026621/your-dumped-housewife-is-your-boss'),
    'desired-by-my-unknown-husband': ('platform', 'https://www.dramaboxdb.com/movie/41000110039/desired-by-my-unknown-husband'),
    'double-contract-love': ('platform', 'https://www.dramaboxdb.com/movie/41000106479/double-contract-love'),
    'ablaze-with-vengeance': ('platform', 'https://www.dramaboxdb.com/movie/41000103801/ablaze-with-vengeance'),
    'my-demon-lord-your-shepherd-girl-has-run-away-again': ('platform', 'https://www.dramaboxdb.com/movie/42000027417/my-demon-lord-your-shepherd-girl-has-run-away-again'),
    'a-breath-away-from-forever': ('platform', 'https://www.dramaboxdb.com/movie/41000102839/a-breath-away-from-forever'),
    'awakened-his-absolute-might-unleashed': ('platform', 'https://www.dramaboxdb.com/movie/41000104235/awakened-his-absolute-might-unleashed'),
    'billionaire-s-ugly-ex-wife-is-a-goddess': ('platform', 'https://www.dramaboxdb.com/movie/42000023914/billionaire-s-ugly-ex-wife-is-a-goddess'),
    'the-lost-son-of-zeus-his-return': ('platform', 'https://www.dramaboxdb.com/movie/42000023820/the-lost-son-of-zeus-his-return'),
    'doting-snake-lord': ('platform', 'https://www.dramaboxdb.com/movie/42000016034/doting-snake-lord'),
    'signed-sealed-secretly-married': ('platform', 'https://www.dramaboxdb.com/movie/41000108064/signed-sealed-secretly-married'),
    'don-t-mess-with-the-xxl-girl': ('platform', 'https://www.dramaboxdb.com/movie/42000026723/don-t-mess-with-the-xxl-girl'),
    'wipe-out-my-pack-a-dumb-pup-turned-the-tables': ('platform', 'https://www.dramaboxdb.com/movie/42000026722/wipe-out-my-pack-a-dumb-pup-turned-the-tables'),
    'no-more-blood-for-my-vampire-first-love': ('platform', 'https://www.dramaboxdb.com/movie/42000024553/no-more-blood-for-my-vampire-first-love'),
}

FACTS = {
    'the-dominant-heir-s-triumphant-return': "Sean York is born into a respected family. For the past three years, he has been in a relationship with Mia Leed. But he gets injured in a car accident and falls into a coma. For his sake, Mia works multiple jobs to pay for his medical bills. Mia's relatives often mock and tease her. They introduce Mia to the son of a wealthy family. However, as Mia resists, Sean wakes up. To return her favor, Sean reclaims his title with his parents and confronts those who have wronged Mia.",
    'chasing-my-rejected-wife': "Love, lies, and mistaken identities! … As Aileen Smith navigated her new life at work, she unexpectedly fell deeply for her boss—THE BILLIONAIRE. But Aileen had been married for a year, although she and her husband's encounters were so scarce they could barely recall each other's faces. Through a series of jaw-dropping twists, Aileen was stunned to discover that the captivating CEO was, in fact, her husband...",
    'emergency-marriage-to-my-secret-billionaire': "Emily, a café worker who caught the groom cheating with the bridesmaid, decides to marry James, the paramedic who saved her life, in a flash marriage to complete her dream wedding. However, she doesn't know that James is the former billionaire CEO and the sole heir to a wealthy family. Emily, who had sworn never to get involved with rich people again, unknowingly falls in love with James, who is pretending to be an ordinary paramedic.",
    'bound-by-blood-the-mafia-king-s-sweetheart': "Lily, a young bakery worker, saves Mafia boss Salvatore with her rare blood, sparking a dangerous connection. After being sold by her stepmother, she’s rescued by him and thrown into a world of luxury and violence. As they grow closer, they face betrayal, jealousy, and violence from those around them, including his delusional 'fiancée' Bianca. Despite everything, their bond strengthens, culminating in their marriage and the birth of twins, marking a happy end.",
    'rising-dawn-the-awakening-of-power': 'Aidan Stein, the Eternal Lord Sovereign of the magnificent Eternity Palace, temporarily loses his memory and intelligence due to his 60-year cycle. He lives alone in Vertania until he encounters Jade Yule, who saves his life and becomes his wife. Years later, Jack Foley, an aristocrat of Vertania, develops an interest in Jade. He sends his men after Aidan, inadvertently triggering the resurgence of his memories and power.',
    'love-is-a-dangerous-game': "Olivia is dragged by her husband Ryan to a couples-swapping getaway—only to be paired with Jake, the husband of her closest friend Mia. Jake is magnetic, unreadable, relentless—nothing like the dull, clueless husband Mia always described. And he won't stop closing in. As both men begin fighting for Olivia's attention, and Mia's jealousy cracks in her perfect act, Olivia must uncover the real truth behind the partner-swapping party before it's too late.",
    'mafia-s-90-day-bride': "Gigi, seeking revenge on the insurance CEO who caused her father's death, offers her only $10,000 to mafia boss Vito to buy his life. Amused by her persistence, Vito proposes she become his bride for 90 days instead. Though he protects her, Vito's cynical nature leads him to refuse life-saving cancer surgery. Disheartened, Gigi believes she's just a pawn. When Gigi nearly miscarries, Vito realizes his love and chooses to fight for life to protect her and their child.",
    'watch-out-i-call-the-final-shots': 'After being cast aside by the woman he helped rise to power, Arthur Storm—secret CEO of the powerful Titan Group—is thrust back into the spotlight when a mysterious billionaire proposes marriage, shaking high society to its core.',
    'my-billionaire-patient-is-my-baby-daddy': "Ella is tricked by her divorce-seeking husband Arthur into sleeping with a stranger on their wedding night, and later gives birth to twins, with one dumped on a hospital bench by him. Fisher, the stranger and a billionaire, finds him and raises him. Years later, Ella serves as Fisher's physical therapist in his estate, looking for her missing son. As the truth unravels, Ella finds her other son, and heals both him and Fisher. The family of four is eventually reunited.",
    'doormat-no-more-the-toxic-ex-licks-my-feet': 'Charlotte signed a life-or-death contract to save her sister, agreeing to marry and work for Leo, the arrogant CEO of Carter Group. For three years, Leo has treated her like a doormat—belittling her, trampling her dignity, and taking credit for her success, convinced she’ll never leave. Now, as the contract nears its end, her old flame Harper returns. Will Charlotte leave Leo, reclaim her life, and reignite the spark with Harper? And will Leo realize what he’s lost?',
    'werewolf-academy-craving-the-forbidden-alpha': "One rule at Blackwood Academy: never touch Damien Blackthorne, the cursed Alpha heir. But when he touches Maya Whitefang — his rival's sister — their mate marks ignite. Now Maya must choose: the clan that owns her, or the dangerous Alpha whose wolf calms only for her.",
    'my-love-out-of-service': "For five years, Finn Carter has silently fulfilled a contract signed with Renee Lane's mother—to heal her daughter's shattered heart. Day by day, he builds a life with a woman who sees him as nothing more than a placeholder for her first love. When Mike Smith's return coincides with the contract's end, Finn recognizes his cue to exit the stage of Renee's life.",
    'the-betrayed-wolfless-is-the-lycan-king': 'Aeron gives his Alpha wolf to his beloved mate Serena to fulfill her dream. After she abandons him, he gains secret Lycan power blessed by the Moon Goddess. Years later, the ambitious Serena invades packs for dominance. Aeron must face his former lover, fight dark forces, and protect his new friends while hiding his true mighty identity.',
    'for-love-and-nothing-less': 'Seven years ago, Luna Sawyer was pregnant when she discovered that her boyfriend, Samuel Payne—who was battling cancer—was secretly the heir to Payne Corp in Reydon. Samuel was offered a deal: if he broke up with Luna, they would pay for his treatment. But deeply in love with her, he rejected the offer, unaware that Luna had overheard the conversation. Determined not to hold Samuel back, Luna silently chose to leave—only to be presumed dead in a car accident.',
    'claimed-by-my-boyfriend-s-mafia-dad': 'Grace is drugged and framed by her jealous best friend Chloe at her boyfriend Ethan’s birthday party. Disoriented, she stumbles onto a hotel terrace and has a one-night stand with ruthless mafia don Vincent. Waking up, Grace is horrified to find this mysterious man is Ethan’s powerful father. She tries to forget the mistake and stay with Ethan, yet Vincent keeps drawing near. Where will this forbidden bond between Grace and Vincent lead...',
    'what-if-i-m-one-hell-of-a-fighter': "After his father dies, Kane is taken in by Eve, a gym owner. Bullied as a janitor, he hides his skills until gangsters threaten the gym. Kane defeats them but is forced into an underground death match against the world champion—and wins, securing millions. Eve's kidnapped father is already dead. Kane avenges him. Months later, the gym thrives. Kane and Eve find family and purpose together.",
    'my-weak-little-dog-is-a-legendary-sky-lion': 'Betrayed by her lover Corrin and best friend Ophelia, Amber was stripped of her bloodline and brutally murdered. Reborn on the day she chose her bonded beast, she refuses the powerful Corrin and instead bonds with a lowly white dog Aerion, who tried to save her in the past life and later reveals his true form—the legendary Sky Lion. Just as Amber begins her revenge against the betrayers, a darker conspiracy unfolds, revealing the ultimate mastermind pulling the strings.',
    'get-out-of-my-bugatti': 'Disguised as an ordinary employee, billionaire founder Ryan Carter lends his Bugatti to arrogant manager Bella. After she and her family steal, mock, and try to fire him, Ryan reveals his identity in the boardroom—and makes them answer for every cruel choice.',
    'pregnant-with-the-dragon-king-s-triplets': "Sold by her family to abusive suitors for magical spring water, fox attendant Sylvia — thought unable to bear children — turns up pregnant with triplets after a night with a stranger who's secretly the Dragon King, Cassius. As he shields her from family, rivals, and jealous coworkers, an attack meant to kill her instead reveals she's the long-lost princess of the Nine-Tailed Wolf Clan. Villains fall; Cassius claims her as his queen.",
    'serve-me-ball-girl-heiress': "Ingrid Voss must finish her summer internship at the country club without anyone finding out that she's the heiress to the Voss Empire. However, she meets Jordan Temple, the second son of the powerful Temple Holdings.",
    'your-dumped-housewife-is-your-boss': "Linda gave up her billionaire legacy for her husband Nick. A ransom call shatters her perfect life: Nick and their daughter have been kidnapped. Rushing to pay the ransom, she's forced to trade her freedom for Nick's mistress Claire. She endures three years of torture in a drug lab. When Linda finally escapes and returns as the billionaire heiress of the Hastings Group, she's ready to make everyone who betrayed her kneel at her feet.",
    'desired-by-my-unknown-husband': "Frank, a small-town boy, hastily married urbanite Andrew, chosen by his grandmotherly friends, without recognizing each other. Andrew disappeared after going abroad for work. A year later, Frank's boss, the wealthy and charming Andrew, pursued him, leading to an affair. The once-playboy Andrew learned commitment and restraint, while Frank, once betrayed, regained trust and learned to love freely. At the divorce site, Frank discovered his husband and boss were the same person.",
    'double-contract-love': "After a one-night stand, they accidentally reunite at the registry office and get married, pretending to be poor to each other after marriage. The heroine is constantly at war with the female antagonist to reclaim her mother's company, during which the hero's true identity gradually surfaces, triggering a series of conflicts and crises. In the process of reclaiming her mother's relics, their relationship heats up.",
    'ablaze-with-vengeance': 'Years ago, Layla York, Balton’s Valkyrie, believed Sean Groff had saved her life, and that belief led to their marriage. Over the past three years, she has devoted herself to him and his family, aiding in his ascent to prominence and facilitating his entry into the Onyx Group. She plans to announce his appointment as CEO during the Phoenix Gala.',
    'my-demon-lord-your-shepherd-girl-has-run-away-again': "Abandoned on an island by her father King John, Ingrid is summoned back when her stepmother Martha and stepsister Lilith covet her betrothal to Lucifer, the King of Hell. Scorned as an ignorant shepherdess, she can secretly communicate with all living things and wields great healing power. Lucifer disrupts her revenge: she once hid him, unaware of his identity, then fled. Seeing through her act, he grips her chin and claims her as his own. This time, he won't let her escape.",
    'a-breath-away-from-forever': 'Five years ago, Callista Summers rescued Jeremiah Fuller when he was drugged. She then pursued her career abroad, driven by her initial self-doubt as a housekeeper. Over time, Callista became a renowned designer and a devoted mother to her son, Scotty Fuller. When she learns of Jeremiah’s kidney failure, she selflessly returns to donate her kidney, saving him once more. However, misunderstandings breed animosity between them.',
    'awakened-his-absolute-might-unleashed': 'Cade Leed raises his sick younger sister, Amy Leed, on his own despite his young age. Though it breaks his heart, Cade has no choice but to put her up for adoption, hoping that a family with resources can provide the treatment she needs. Twenty years later, Cade falls into a coma after an accident, and his fiancée, Rue Kirk, cares for him tirelessly for five years, never giving up hope.',
    'billionaire-s-ugly-ex-wife-is-a-goddess': 'Chloe Ashford spent three years hiding behind an ugly disguise, believing her billionaire husband loved her soul. But when Ethan Sterling gives her anniversary gown to his first love, Chloe discovers she was only his weapon against his family. She unveils her true beauty, files for divorce, and rises as Vesper—a fashion genius no one can control. Now Ethan wants her back, but Chloe has learned: she doesn`t need a savior.',
    'the-lost-son-of-zeus-his-return': "Hercules, the son of Zeus and Hera, goes missing as a child and is swapped with the mortal Icaris by an envious follower. Eighteen years later, Hercules travels to Olympus to join the Divine Guards to save his beloved, far outperforming Icaris. Unaware of his true identity, Zeus's family, instigated by Icaris, cruelly suppress and exile him. Once the truth is revealed, Zeus's family desperately begs for forgiveness, while Icaris conspires with Hades for revenge.",
    'doting-snake-lord': 'Reborn before her tragic fate unfolds, Elena gets a second chance at life. In her previous life, she was betrayed by her sister Veronica and fiancé Grayson, framed for infidelity, and pushed into the Dragon Pit to her death. Determined to change her destiny, Elena turns to Nidhogg, the imprisoned Dragon Progenitor, and unexpectedly becomes pregnant with his nine heirs.',
    'signed-sealed-secretly-married': 'With the help of his grandfather, Dave Quinn marries Tessa Gray, a girl he does not know much about. After marriage, Tessa works in Quinn Corp as a cleaner and makes Dave promise to keep their relationship a secret from their colleagues. However, some of her colleagues show disdain towards her, especially Dave’s childhood sweetheart, Lana Harris, who has a crush on him. Out of jealousy, Lana sets Tessa up in an attempt to get rid of her, hoping to ruin her marriage with Dave.',
    'don-t-mess-with-the-xxl-girl': "I spent five grueling years transforming from a mocked fat girl into an upcoming international model. My global debut lands at the same hotel as my high school bullies' reunion. Josephine, my tormentor, dug up a humiliating old video and tagged me, while classmates bet I'd never show. I replied calmly and vowed to arrive on time—and make them all pay.",
    'wipe-out-my-pack-a-dumb-pup-turned-the-tables': "Mia Blackridge, the youngest daughter of Blackridge Pack's Alpha, is widely seen as a useless dumb pup who can't even shift into wolf form. Secretly, she is the reborn soul of a former Pack Alpha who ruled for 70 years. When the scheming Beta Grady forges a royal Crown Order to execute her father and wipe out the whole pack, Mia steps forward, exposes the fake seal, outplays the enemy forces with her lifelong wisdom, and saves her entire pack from ruin.",
    'no-more-blood-for-my-vampire-first-love': 'She gave him her heart, only to be used as a pawn to win her cruel stepsister. Shattered, the gifted Keeper Allie walks away—straight into the devotion of an ancient Original who has waited two centuries for her. Watching her reign alongside a far superior man, her ex falls to his knees begging for a second chance. Too late. She destroys her enemies and chooses true love, leaving the boy who broke her choking on regret.',
}
