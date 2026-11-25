[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/capptainjack/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/capptainjack/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# news-image-20261125

Built for make.fun's [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) bounty ($100 in USDC).

One image summing up the world's news of Wednesday 25 November 2026:
a dense broadsheet front page, "THE WORLD TODAY", with 30 verified
stories across 6 continents — 6 hero stories with vector icons, region
and status labels, a numbered list of 24 more stories, a "THE DAY IN
NUMBERS" box, a "WHERE IT HAPPENED" map, and a DATE CHECK footer.

Every story happened, or was first reported, on 25 November 2026.
Claims by one side are labelled CLAIM, never stated as fact. Sources:
Reuters, BBC, AP, Al Jazeera, Xinhua, UEFA, ESA.

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`. The image is a 1024x1024 PNG, drawn
with Python + Pillow by `draw.py` (vector icons and sharp text, no AI
image generation). Two runs of the program write byte-identical files.

Run: `MAKEFUN_OUTPUT_DIR=out node main.ts`

Re-draw the image: `python3 draw.py entry.png`
