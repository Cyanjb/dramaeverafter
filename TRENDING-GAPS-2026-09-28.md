# Trending and popularity gaps, 28 September 2026

Three research passes run in parallel on 28 Sep: each platform's own charts (16 platforms, 372 chart titles), Reddit and social discussion from roughly the last 60 days (119 titles, 66 actors), and actor popularity (72 actors). Everything was checked against `data/`. Raw results: `generator/staging/trending_research_2026-09-28.json`. **Nothing was written to `data/`.**

## Headline

- **708 distinct titles surfaced; 271 are already in the database, 437 are missing** (9 of them near-matches that need a ruling).
- **Our view-based ranking only sees ReelShort.** All of our top 100 by reach are ReelShort, because it is the only platform we record views for. DramaBox's trending chart alone has 12 titles above 50M views that we do not carry, led by *Watch Out, I'm The Lady Boss* (267.2M, verified on its page).
- **DramaBox is no longer bot-walled** (contradicts `references/adapters.md` sec 8). Its pages carry view count, follows, synopsis, episode count and cast with photos. It can join the weekly scrape.
- **Western live-action stars are well covered; their non-ReelShort work is not.** 75 of 113 actors named are in the database, but their recent DramaBox, Shorts, NetShort, CandyJar and Vigloo titles are largely missing.
- **Chinese live-action stars are the biggest actor gap**: Chen Si, Zhao Xixi, Yao Guanyu, Wang Yilei, Yu Yin, Liu Xiyu and more, none in the database, most-posted-about actors on r/CShortDramas.
- **The most-discussed titles online are mostly AI-generated** (DramaWave, NetShort, PineDrama, iDrama). Sentiment is split: the top anti-AI post has 315 upvotes, and a 144-comment thread calls out AI dramas using real celebrity likenesses.

## What can be added safely

| Group | Titles | Source quality |
|---|---|---|
| Missing, with the platform's own page (URL, usually synopsis, episodes, often views and cast) | 229 | Good: same standard as the weekly scrape, lands as needs_check |
| Missing, named only in Reddit/social or an actor's filmography, no platform page yet | 208 | Discovery only: needs the platform page found before a row is created |

The 229 by platform: NetShort 47, MoboReels 35, GoodShort 31, DramaBox 29, Vigloo 22, ShortMax 15, FlickReels 14, FlexTV 13, StardustTV 10, DreameShort 6, PineDrama 5, My Drama 2. MoboReels, FlexTV, StardustTV and Sereal+ are platforms we do not list yet. StardustTV marks many titles as AI.

## Top 60 missing titles, by strength of signal

Signal combines platform views, independent mentions, and links to popular actors. Views are as shown by each platform and are not comparable across platforms.

| Title | Platform | Views | Mentions | Popular actors |
|---|---|---|---|---|
| Watch Out, I'm The Lady Boss | dramabox | 267.2M |  |  |
| Revenge Marriage Sweet Love | dramabox | 189.2M |  | Jarred Harper |
| Fake Dating My Rich Nemesis | dramabox | 141.7M |  | Ben Armstrong, Meg Bush |
| Faking Forever With My Frenemy | dramawave |  | 9 |  |
| One Fateful Night with My Boss | dramabox | 115.8M |  |  |
| Nights with My CEO | reelshort |  | 8 |  |
| Reveal, Rise and Reign (DUBBED) | dramabox | 106.2M |  |  |
| Escaping the R18 Mafia Bosses Together | netshort |  | 7 |  |
| Think Again! I'm the Hidden Boss Mom | dramabox | 91.7M |  |  |
| Royal Blood & Mafia Knight | pinedrama |  | 6 |  |
| The Drunk Wolf | dramawave |  | 6 |  |
| Ruling Over All I See (DUBBED) | dramabox | 83.7M |  |  |
| Rebel in Devil's Shackle | dramabox | 82.0M |  |  |
| Crown of Hidden Scales | dramawave |  | 5 |  |
| Office Enemies | shorts |  | 1 | Noah Fearnley, Rebecca Stoughton, Sarah Moliski |
| Love Me All You Like | dramabox | 69.3M |  |  |
| Waking Up Married To My Crush! | dramabox | 68.4M |  |  |
| No Escape as the Dragon King's Mate | dramabox | 56.9M |  |  |
| 100% Compatibility | unknown |  | 4 |  |
| Light in Winter | flickreels |  | 4 |  |
| Mating Season Luna Trials | dramawave |  | 4 |  |
| The Raven's Bride | dramawave |  | 4 |  |
| 30 Day Love Bet | unknown |  | 4 |  |
| The Dragon Prince's Knight Is a Girl | unknown |  | 4 |  |
| Step by Step | super punchy / tiktok |  |  | Haley Lohrli, Nicole Mattox, Seth Edeen |
| Almost Lover | dramabox |  |  | Nicole Mattox, Ryan Watson Henderson, Travis DesLaurier |
| Tied to My Dangerous Mafia Husband | dramabox | 53.1M |  |  |
| Forever Was a Lie | dramabox | 43.0M |  |  |
| I'm Nothing but a Mortal (DUBBED) | dramabox | 42.7M |  |  |
| The Wedding Day Divorce (DUBBED) | dramabox | 41.6M |  |  |
| No Romance | unknown |  | 3 |  |
| The Elf Prince Is My Baby Daddy | dramawave |  | 3 |  |
| They Gave the Doomed Duke the Wrong Bride | unknown |  | 3 |  |
| Mommy, You Forgot Me and Daddy | unknown |  | 3 |  |
| Reborn to Escape My Mafia Stepbrother | storyreel |  | 3 |  |
| Craving the Wrong Brother | unknown |  | 3 |  |
| I Can Hear My Cold Husband's Dirty Thoughts | toonshort |  | 3 |  |
| Their Hidden Princess | unknown |  | 3 |  |
| Reincarnated in a Brothel of Death | unknown |  | 3 |  |
| My CEO and His Cleaning Fiancée | idrama |  | 3 |  |
| Mr. Reid, You've Got the Wrong Wife | unknown |  | 3 |  |
| Climbing Into My Sister's Fiancé's Bed | dramawave |  | 3 |  |
| Hotel Noir: Kiss Me to Survive | vigloo |  | 3 |  |
| Oops! I Married My Enemy | shorts |  |  | Ashley Michelle Grant, Noah Fearnley |
| Falling in Love by a Mistaken Vow | netshort |  |  | Mariah Moss, Sam Myerson |
| Love Always Finds Its Way | stardust / dramawave |  |  | Brooke Moltrum, Nick Ritacco |
| Falling For A Superstar | alta |  |  | Ashley Michelle Grant, Jackson Tiller |
| Hate Notes | candyjar |  |  | Blake Manning, Hannah Lowery |
| Back to the 80s | dramabox | 30.3M |  |  |
| My Alien Life | moboreels |  | 2 |  |
| Guess Who They Miss Now | dramabox | 25.9M |  |  |
| Taming the Wolf King | unknown |  | 2 |  |
| After My Divorce I Became the Godfather's XXL Wife | shortmax |  | 2 |  |
| Too Late for My Shifters' Regret | storyreel |  | 2 |  |
| A Rhapsody for the Crown Prince | unknown |  | 2 |  |
| Daddy Teach Me | unknown |  | 2 |  |
| Lethal Love | unknown |  | 2 |  |
| Haunted by A Hot Jealous Ghost | unknown |  | 2 |  |
| Kissing Me Harder Stepbrother | unknown |  | 2 |  |
| Oops, You Bullied the Alpha Queen | unknown |  | 2 |  |

## Actors

**Missing entirely:** James Franco (*Love, Lies & Frank*, Shortical, Sept 2026), Nico Tortorella (*Salt Kiss*), Elliott Eason, Issa Rae, Jesse Tyler Ferguson, Scarlet Sterling Shields, Brittney Jefferson, and the Chinese stars Chen Si, Zhao Xixi, Yao Guanyu, Wang Yilei, Yu Yin, Liu Xiyu, Ma Xiaoyu, Shen Haonan, Guo Yuxin, Zhang Chi, Wang Kaimu, Cao Tiankai and others.

**In the database but thin against a clearly bigger filmography:** Chase Mattson (6 credits, 2.5M TikTok), Mariah Moss (4), Erin Orcutt (8), Sophia Delucchi (4), Ben Armstrong (5), Nic Westaway (2), Jeff Violette (3), Joel Erdmann (1), Gabriel Jayne (2), Dominique Rose (1), Travis DesLaurier (6), Noah Fearnley (19 against 50+ he reports).

**Top 20 by popularity signal:**

| Actor | Database | Signal |
|---|---|---|
| Noah Fearnley | IN_DB noah-fearnley (19 credits) | Wikipedia page; FX "Love Story" (Michael Bergin) + film "Mercy" 2026; 2 wins at 2026 Vertical Drama Love Fan Awards (Male Vertical Legend, B |
| Joseph Purcell | IN_DB joseph-purcell (10 credits) | Profiled by Variety and The Hollywood Reporter in 2026, Wikipedia page, Us Weekly, Mandy; son of Dominic Purcell; CandyJar regular |
| Chase Mattson | IN_DB chase-mattson (6 credits) | "In the Palm of His Hand" 251.3M ReelShort views (Hot); fandom says 80M in first weeks; Verties 2026 Spark award winner (with Maria Barseghi |
| Cameron Porras | IN_DB cameron-porras (14 credits) | Us Weekly "hottest leading men" 2026; fandom nickname "stinkies"; Fangirlish feature Jun 2026; Reddit favourites; fan subthread on why no Ca |
| Kasey Esser | IN_DB kasey-esser (31 credits) | Rolling Stone "breakout star", Cosmopolitan; 35+ verticals / 400M+ views (own site); top of the Aug 2026 Reddit fan panels; TikTok @kaseyess |
| Nicole Mattox | IN_DB nicole-mattox (14 credits) | Verties 2026 Queen (winner); VDLFA 2026 headline winner ("the big ones") and Lead Actress nominee; ReelShort actor page 2.03B views over 11  |
| Cayman Cardiff | IN_DB cayman-cardiff (23 credits) | Verties 2026 King (winner); VDLFA 2026 Lead Actor nominee; Reddit favourites; TikTok @caymancardiff 94,800 followers |
| Eric Guilmette | IN_DB eric-guilmette (20 credits) | VDLFA 2026 Lead Actor nominee; Us Weekly hottest leading men; Fanficable pick; 30+ vertical leads; "#TeamEric" fans sponsor an award; TikTok |
| Evan Adams | IN_DB evan-adams (26 credits) | Us Weekly hottest leading men; own fan subreddit r/EvanAdams; most-hearted in r/ReelShortsNoAI favourites; Hollywood Reporter cites him as t |
| Seth Edeen | IN_DB seth-edeen (30 credits) | ReelShort actor page 3.37B views over 21 dramas (largest in our sample); VDLFA 2026 nominee (lead comedy, couple x2); TikTok @sethedeen 344, |
| Jesse Morales | IN_DB jesse-morales (23 credits) | ReelShort actor page 3.12B views over 24 dramas; VDLFA 2026 Lead Actor + On-Screen Couple nominee (How to Tame a Silver Fox 634M); Us Weekly |
| Sam Myerson | IN_DB sam-myerson (11 credits) | VDLFA 2026 Lead Actor Comedy nominee; attended VDLFA ceremony; Reddit favourites; TikTok @sammyerson 432,100 followers |
| Meg Bush | IN_DB meg-bush (22 credits) | ReelShort 1.57B views over 12 dramas; repeatedly named in Reddit favourites; TikTok @megbush_ 317,700 followers |
| Samantha Drews | IN_DB samantha-drews (20 credits) | ReelShort 2.60B views over 20 dramas; VDLFA Kick-Ass Heroine nominee (My Sister Is the Warlord Queen 638M); TikTok @samanthadrews_ 210,000 f |
| Haley Lohrli | IN_DB haley-lohrli (23 credits) | ReelShort 1.87B views over 16 dramas; VDLFA Kick-Ass Heroine nominee; TikTok @haleylohrli 185,000 followers |
| Tess Dinerstein | IN_DB tess-dinerstein (8 credits) | VDLFA 2026 Lead Actress + On-Screen Couple nominee; ReelShort 1.28B views over 6 dramas |
| Cayla Brady | IN_DB cayla-brady (13 credits) | VDLFA 2026 Lead Actress nominee + couple nominee; Reddit "absolute POWERHOUSE"; Verties Spark nominee |
| Mariah Moss | IN_DB mariah-moss (4 credits) | VDLFA 2026 Lead Actress nominee (Queen of the Court); attended ceremony; TikTok @mariah_moss 153,500 followers |
| Rhett Wellington | IN_DB rhett-wellington (14 credits) | VDLFA 2026 headline winner ("the big ones"); named "#1 actor" in Reddit favourites thread; TikTok @rhettwellington 9,376 followers |
| Erin Orcutt | IN_DB erin-orcutt (8 credits) | VDLFA 2026 headline winner ("the big ones"); DramaBox 8 titles incl. Can't Get Enough of You (2.33M follows, Feb 2026) |

## Database problems found along the way

- `the-hockey-star-s-ramoree` is a misspelled stub (*The Hockey Star's Remorse*), no platform link, from the 24 Jul IMDb lists.
- Actors missing a credit on titles we hold: Nicole Mattox on *Christmas With a Country Bad Boy*; Declan Clifford on *Unwanted True Mate*, *His Sweet Bella* and *Hero Should Never Stay Low*.
- *The Great and Powerful Genie* (526M, our #9 by reach) has no cast on file.

## Access notes

- Reddit: readable through headless Chromium (the proxy CA had to be added to the browser's NSS store). `.json` endpoints and old.reddit are blocked. r/reelshort is banned; r/Vertical_Dramas is the active hub, r/CShortDramas for Chinese live-action, r/ReelShortsNoAI for live-action only.
- DramaWave: connection reset; still no web catalogue. ShortMax encrypts its page data (no views). NetShort and GoodShort show no cast on the web. Vigloo has a public API with view counts and cast.
- IMDb popularity, Instagram and paywalled trade press (Variety, THR) could not be read.
