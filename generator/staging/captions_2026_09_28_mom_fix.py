# -*- coding: utf-8 -*-
"""Correction for mom-love-me-again, 28 Sep 2026.

The 27 Sep caption was written from the WRONG ReelShort book. Two books share
this title and slug: 66827538 (Alzheimer's family drama, 11.3M) is the one the
page links to; 66ded2c8 (framed, reborn, revenge, 10.0M) is held in match_queue.
load_facts() keys by slug, so the second book's synopsis overwrote the first and
the caption described the held show. This caption is written from 66827538:
https://www.reelshort.com/movie/mom-love-me-again-66827538f9a66355f9032622
The source is mostly a marketing blurb; the one story line (mother diagnosed,
forgets her family, daughter tries to reconnect) is all this uses.

The reborn caption is kept in captions_2026_09_27_new69.py for the held book,
if Cyan rules the two different and it gets its own page.
"""

CAPTIONS = {
    'mom-love-me-again':
        "Her mother has Alzheimer's. She's forgetting her own family.\nA mother is diagnosed with Alzheimer's, and little by little she loses her memory of the people she loves most. Her daughter is left trying to reach her, fighting to rebuild the bond between them while the illness keeps pulling her mother further away.",
}

FACTS = {
    'mom-love-me-again':
        '"Mom, Love Me Again” is about heartwarming eunion. A mother, diagnosed with Alzheimer’s, forgets her family. Her daughter struggles to reconnect and rebuild their bond. Think “The Notebook” meets “Still Alice”. Get ready for emotional drama, poignant moments, and a powerful celebration of unconditional love! You can’t ignore the wonder of this amazing tear-jerking.',
}
