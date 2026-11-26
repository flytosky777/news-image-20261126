[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/flytosky777/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/flytosky777/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

# The World in One Day — Thursday 26 November 2026

A newspaper front page summing up 26 November 2026's world news in one
1024×1024 image, built for the make.fun `news-image-20261126` bounty.

## Stories

1. **US hits China, EU and Brazil with new tariffs** (headline) — the Trump
   administration proposes 20% on Chinese goods and levies on 14 trading
   partners under Section 301; Brazil is singled out for extra duties.
   Sources: AP, Reuters.
2. **Tanker fire kills 31 on Cairo ring road** — a fuel truck overturns and
   explodes on the Ring Road in Giza; 27 vehicles charred, 21 hurt.
   Sources: AP, Reuters.
3. **Judges urge dropping Netanyahu bribery case** — Jerusalem District Court
   says a conviction in Case 4000 is unlikely; Case 2000 to be reconsidered.
   Sources: CNN, Globes.
4. **Ukraine hits five Russian jets at airfield** — three MiG-31s and two
   Su-34s damaged at Savasleyka, 300 km east of Moscow. Source: BBC.
5. **Two Libyan officers die after drone strike** — wounded in Ukraine's
   attack on a Russian warship at Benghazi; the Libyan army vows revenge.
   Source: AP.
6. **Pakistan's first astronaut reaches Tiangong** — Shenzhou-24 docks;
   Zeeshan Ali is the first foreign visitor to China's station.
   Sources: Reuters, China Manned Space Agency.

Photos are illustrative, from Wikimedia Commons. The page is drawn by
`build_frontpage.py` (Python + Pillow); `main.ts` copies the finished
`entry.png` to `/output/entry.png`, byte-identical on every run.

## Reproduce

```sh
python3 build_frontpage.py   # writes entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
