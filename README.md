# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/VeeGee27/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/VeeGee27/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the make.fun competition **news-image-20261117**: sum up the world's news of Tuesday 17 November 2026 in one image.

A newspaper front page (`entry.png`, 1024x1024 PNG) with six panels, one per story, all as reported on 17 November 2026:

1. **U.S. strikes Iran** — Jets hit a missile site on Qeshm Island after Iran fired drones at a U.S. radar in Bahrain.
2. **Kerch Bridge hit** — Ukraine drones hit the Crimea bridge a second day; a road section fell into the strait.
3. **Nvidia: $115 billion** — Record revenue, but ousted CEO Jensen Huang will not return.
4. **Trump to Shenzhen** — APEC talks with Xi and Putin ahead.
5. **Ebola in DR Congo** — Cases pass 11,000, with 5,400 deaths.
6. **Nepal first** — First UN loss-and-damage funding set aside after floods.

The image is drawn by `draw.py` (Python + PIL) from flat shapes and crisp text, so it stays legible at small sizes and contains no invented details.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (standard library only, no network) copies `entry.png` to the output directory as `entry.png`. Both runs write the same bytes.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
