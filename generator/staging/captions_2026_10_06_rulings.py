# -*- coding: utf-8 -*-
"""Captions for titles linked or split by Cyan's duplicate rulings, 6 Oct 2026. Ad hoc batch: live on apply, also on the standing review page.

10 titles, 10 written, none skipped. Every caption is written from the book the
title page links to (availability.csv direct_link); each FACTS entry is that
book's platform synopsis as banked by caption_pipeline.load_facts().

Notes for Cyan:
- cause-you-were-never-mine (live action) and cause-you-were-never-mine-ai (AI)
  tell the same story. The live action caption follows Bruce (revenge, Morgan
  Group) and the AI caption follows Jade (why she lied); hooks and endings differ.
- divorced-at-the-wedding-day-ai: its live action twin already has a live caption
  (hook "The engagement lasts exactly one day."). The AI caption opens on the
  mistaken mistress and carries the later beats the twin leaves out: the bloody
  revenge and Sophie's fake pregnancy and betrayal scheme being exposed.
- come-back-for-you: the source is 24 words, so the caption retells only those
  beats (murdered by ex husband Ricky, reborn ten years back, revenge, second
  chance love with Johnny Wonder) and is short on purpose.
- cheer-queen-returns-to-slay: source is one sentence and names nobody, so the
  caption names nobody.
- ceo-queen-a-mother-s-revenge: facts are the ReelShort book the page links to;
  the opening "In CEO Queen A Mother's Revenge movie," is SEO filler and was
  ignored. SOURCES points at that ReelShort book, not the PineDrama link.
- a-deal-with-my-billionaire-donor and dark-web-of-desire: facts are the
  DramaBox books the pages link to; SOURCES points there.
"""

CAPTIONS = {
    # 98.8M  Cause You Were Never Mine
    'cause-you-were-never-mine':
        "He was about to propose. She let him believe she was cheating.\nBruce had a proposal planned for Jade. Then her mother got sick, and Jade didn't want him weighed down with it, so she made it look like she was cheating on him with Dexter. It worked. Bruce was crushed and ended things. He wanted revenge, so with his family behind him he started a business of his own. Five years later he's the CEO of Morgan Group, and the woman he hires is Jade. Now she works for him, and they hurt each other at every turn while still being drawn together. Her lie spared him once. Now it's costing them both.",
    # 78.6M  A Deal With My Billionaire Donor
    'a-deal-with-my-billionaire-donor':
        "She needs a baby. He needs a wife. They put it in writing.\nClaire Miller is diagnosed with premature ovarian failure, and from that moment having a child is all she wants. Her ex's new girlfriend is expecting, and Claire swears she'll be pregnant before that baby arrives. Ethan Reed is a billionaire with a problem of his own. Unless he marries, he loses his inheritance. So they agree on a sperm contract that gets each of them what they need, and it comes with a fake marriage. Then Ethan ends up as her boss, the sparks start flying, and the lines between them begin to blur. This marriage started out as a matter of pride. Can it turn into real love?",
    # 24.8M  Come Back for You
    'come-back-for-you':
        "Her ex husband killed her. Then she woke up ten years earlier.\nShannon was married to Ricky once, and Ricky is the man who murdered her. She doesn't stay dead. She's reborn ten years in the past, and this time she's going after him for what he did. She gets a second chance at love too, with Johnny Wonder. Ricky took her whole life from her, and now he's the one who's going to pay.",
    # 17.0M  Emergency Reckoning: Brother's Fury
    'emergency-reckoning-brother-s-fury':
        "They thought she was a mistress. She's actually the fiance's sister.\nCamilla is engaged to Nolan, and she and her family decide Annie must be a mistress. They insult her and they beat her. What none of them know is that Annie is Nolan's sister, which makes Camilla her future sister in law. Then Nolan shows up. He breaks off the engagement and gets Annie out of there. Camilla loses the man she was going to marry, and her whole family is left wishing they could take it back.",
    # 9.9M  Crush Alert: Love Request from My Enemy
    'crush-alert-love-request-from-my-enemy':
        "The boy she tells everything to online is her rival at school.\nShe's a scholarship girl at an elite school, and the other students bully her. The one person she opens up to is a boy she plays games with online. She has no idea who he really is, but she trusts his voice, and he's the only one she tells her secrets to. That voice belongs to the cocky boy she clashes with at school every day. He knows the truth, and he's struggling to find a way to tell her. And every secret she trusts him with makes it harder to say.",
    # 9.4M  Divorced at the Wedding Day
    'divorced-at-the-wedding-day-ai':
        "She thought she'd caught his mistress. It was his pregnant sister.\nIt's Lorenzo's engagement day, and his fiancee Sophie decides Alessia must be his mistress. Alessia is Lorenzo's sister, and she's pregnant. Sophie and her entire family go after Alessia in front of everyone. Alessia loses her baby, and the family heirloom, a necklace worth five billion dollars, is destroyed. Then the truth comes out, and Lorenzo's revenge for his sister is a bloody one. Sophie's own secrets don't stay buried either. Her pregnancy is fake, and so is the betrayal she was planning. She came to marry into Lorenzo's family. Instead she cost it a child.",
    # 8.0M  Dark Web of Desire
    'dark-web-of-desire':
        "Sold out on the dark web, she lands in a hunting game played by the rich.\nChloe Morgan comes from aristocracy, but that life is behind her. Someone sells her out on the dark web, and inside a hunting game the rich play for sport she runs into the mafia lord Shaun Luther. He drags her down into hell with him, where sweetness and torture come from the same man. When she's finally ready to leave, he locks her up. She tries again and again, and every time he keeps her. Is it love that makes him do it, or hate? Their desire is forbidden and it's more than either of them can handle. They wound each other, and somehow they save each other too.",
    # 6.0M  Cause You Were Never Mine
    'cause-you-were-never-mine-ai':
        "Her mother was sick. She broke his heart rather than tell him.\nJade's mother is in a medical crisis, and her boyfriend Bruce is just about to ask her to marry him. She won't let him get dragged into it. So she pretends to be having an affair with Dexter, and Bruce walks away hurt and sure she betrayed him. Five years go by. Bruce comes back with real power, CEO of Morgan Group now, and he gives Jade a job. He still resents her, and the chemistry between them hasn't gone anywhere either. The road back to love is going to be a painful one.",
    # 5.1M  Cheer Queen Returns to Slay
    'cheer-queen-returns-to-slay':
        "She was a cheer legend once. Now she's seventeen again.\nHer glory days on the squad are long gone. Then she wakes up back in the body she had at seventeen. Her daughter is spending the summer at cheer camp and getting bullied there, so this former Cheer Queen gets herself into the camp. She's there to look after her girl, put the mean girls in their place, and tumble her way back to the top. The girls picking on her daughter are about to find out what a real cheer legend looks like.",
    # 0  CEO Queen: A Mother's Revenge
    'ceo-queen-a-mother-s-revenge':
        "Fifteen years at an orphanage. Nobody knew she ran an empire.\nMary Miller has spent fifteen years living quietly and working at an orphanage. Then a brain hemorrhage puts her in a coma. Grace, the youngest of her adopted daughters, sells her own blood trying to keep her alive, while Rose and William, her other children, show how cruel they really are. When Mary wakes up she says she's the legendary CEO of Phoenix Group, and nobody believes her. People laugh at her, call her a delusional old woman and get violent with her. They have no idea who they're dealing with. Mary's empire is getting ready to hit back at everyone who hurt her family, and Grace, who loved her all along without ever knowing who she really was, is about to be rewarded.",
}

FACTS = {
    'cause-you-were-never-mine':
        "When Jade's mother falls ill, Jade pretends to cheat with Dexter to avoid burdening Bruce, who was planning to propose. Heartbroken, Bruce breaks up with her. To revenge, Bruce starts his own business with the help of his family. Five years later, as CEO of Morgan Group, he hires Jade, thus beginning a love story of mutual torment that would touch hearts.",
    'a-deal-with-my-billionaire-donor':
        'Claire Miller, desperate to have a child after being diagnosed with premature ovarian failure, vows to get pregnant before her ex’s new girlfriend gives birth. Enter Ethan Reed—a billionaire forced to marry or lose his inheritance. They strike a “sperm contract” for mutual benefit, but when Ethan becomes her new boss, sparks ignite and emotions blur. Can a fake marriage born of pride turn into real love?',
    'come-back-for-you':
        'After murdered by her ex-husband Ricky, Shannon reborn 10 years ago to start her revenge for Ricky and second chance love with Johnny Wonder.',
    'emergency-reckoning-brother-s-fury':
        "Annie is mistaken for a mistress and is insulted and beaten by her future sister-in-law, Camilla, and her family. Her brother Nolan arrives, calls off his engagement to Camilla, and rescues Annie, leaving Camilla's family full of regret.",
    'crush-alert-love-request-from-my-enemy':
        "Bullied at her elite school, a scholarship girl shares her secrets only with the mysterious boy she plays online games with. She doesn't know the voice she trusts belongs to her cocky rival at school, who knows the truth and is struggling to tell her.",
    'divorced-at-the-wedding-day-ai':
        'On Lorenzo’s engagement day, his fiancée Sophie mistakes his pregnant sister Alessia for his mistress, publicly abuses her with her entire family, causes her miscarriage, and destroys a five-billion-dollar family heirloom necklace. After the truth is revealed, Lorenzo launches a bloody revenge for his sister, while Sophie’s fake pregnancy and betrayal scheme are exposed.',
    'dark-web-of-desire':
        'Sold out by someone in dark web, Chloe Morgan bumps into mafia lord, Shaun Luther in the riches’ hunting game. Once an aristocracy, Chloe is now dragged into inferno by Shaun, lost in sweetness and tortures. She finally makes up her mind to leave, but Shaun confines her no matter how many times she tries. It’s out of love, or of hatred? Overwhelmed by love and forbidden desire, the two hurt each other but simultaneously save each other.',
    'cause-you-were-never-mine-ai':
        'Jade fakes an affair with Dexter, to shield her boyfriend Bruce from her mother’s medical crisis just as he is about to propose, Heartbroken and betrayed, Bruce leaves. Five years later, he returns as the powerful CEO of Morgan Group and hires Jade. It sparks a roller coaster of deep resentment and undeniable chemistry, leading them through a painful but beautiful journey back to love.',
    'cheer-queen-returns-to-slay':
        "A washed-up cheer legend wakes up in her 17-year-old body and infiltrates her daughter's summer cheer camp — ready to protect her bullied daughter, humiliate mean girls, and flip her way back to glory.",
    'ceo-queen-a-mother-s-revenge':
        'In CEO Queen A Mother’s Revenge movie, after 15 years of living as a humble orphanage worker, Mary Miller\'s peaceful life is shattered when a brain hemorrhage leaves her comatose. While her youngest adopted daughter Grace desperately tries to save her life by selling her own blood, her other children Rose and William reveal their true cruel nature. When Mary finally wakes and claims to be Phoenix Group\'s legendary CEO, she faces brutal mockery and violence. But those who dare abuse the "delusional old woman" are about to learn they\'ve made a terrible mistake—as Mary\'s vast empire prepares to strike back against all who wronged her family, while rewarding the one daughter who loved her without knowing her true identity.',
}

SOURCES = {
    'cause-you-were-never-mine': ('platform', 'https://www.dramaboxdb.com/movie/41000110709/cause-you-were-never-mine'),
    'a-deal-with-my-billionaire-donor': ('platform', 'https://www.dramaboxdb.com/movie/41000122689/a-deal-with-my-billionaire-donor'),
    'come-back-for-you': ('platform', 'https://www.dramaboxdb.com/movie/41000110859/come-back-for-you'),
    'emergency-reckoning-brother-s-fury': ('platform', 'https://www.dramaboxdb.com/movie/41000123062/emergency-reckoning-brother-s-fury'),
    'crush-alert-love-request-from-my-enemy': ('platform', 'https://www.dramaboxdb.com/movie/42000008972/crush-alert-love-request-from-my-enemy'),
    'divorced-at-the-wedding-day-ai': ('platform', 'https://www.dramaboxdb.com/movie/42000013146/divorced-at-the-wedding-day'),
    'dark-web-of-desire': ('platform', 'https://www.dramaboxdb.com/movie/41000100700/dark-web-of-desire'),
    'cause-you-were-never-mine-ai': ('platform', 'https://www.dramaboxdb.com/movie/42000012972/cause-you-were-never-mine'),
    'cheer-queen-returns-to-slay': ('platform', 'https://www.dramaboxdb.com/movie/41000122781/cheer-queen-returns-to-slay'),
    'ceo-queen-a-mother-s-revenge': ('platform', 'https://www.reelshort.com/movie/ceo-queen-a-mother-s-revenge-6825af4b1657d2354b0d8094'),
}
