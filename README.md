# news-image-20261121-entry

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/sugiartho/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/sugiartho/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-image front page summing up the world news of Saturday 21 November 2026: Russian missiles landing in Poland after the biggest strike on Ukraine of the war, world markets sliding into correction, the FBI's crime database hacked, COP31 missing its deadline, a pancreatic-cancer pill making tumours undetectable, Mexico capturing "El Chapo Isidro", and BepiColombo entering orbit around Mercury.

Every story was verified against at least two outlets in the 21 November 2026 news cycle (BBC, CNN, AP, ESA, The Guardian, PBS NewsHour, France 24 and others — see NOTES.md). The image is drawn from scratch with PIL (draw.py in this repo — flat vector, DejaVu Sans Bold). No photos, no screenshots, no copied artwork. Nothing in the image predates 13 November 2026.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (stdlib only) copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`. To redraw the image from scratch: `python3 draw.py entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=c31gnmy5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
