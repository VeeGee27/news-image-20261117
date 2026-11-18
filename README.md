# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/VeeGee27/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/VeeGee27/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the make.fun competition **news-image-20261117**: sum up the world's news of Tuesday 17 November 2026 in one image.

A newspaper front page (`entry.png`, 1024x1024 PNG) with **33 stories from Tuesday 17 November 2026** — 3 hero stories, 12 mid stories, a world map of where it happened, and 18 more one-line stories, chosen for weight rather than count — all as reported on that day:

**Heroes**
1. **Ukraine hits Kerch Bridge again** — Ukrainian drones hit the bridge for a second day; a road section fell into the strait, cutting a key supply route to Crimea.
2. **US strikes Iran after drone attacks** — US jets hit a missile site on Qeshm Island after Iran fired drones at a US radar in Bahrain — its third attack there in five days.
3. **Trump heads to Asia for APEC talks** — Trump starts in Manila for the ASEAN–US summit, then heads to Shenzhen for APEC talks with China's Xi and Russia's Putin.

**Mid stories**
- **Ebola in DR Congo** — Outbreak passes 11,000 cases and 5,400 deaths.
- **Nvidia: $115 billion** — Record $115B sales, yet ousted CEO Jensen Huang will not return.
- **Nepal first** — First UN loss-and-damage funds set aside after floods.
- **Gaza aid at risk** — UK, Australia, Canada, Italy urge Israel to open crossings.
- **Mongolia president resigns** — President Khürelsükh quits amid a corruption scandal.
- **Japan scrambles jets** — Russian aircraft violate Japanese airspace.
- **Measles status lost** — US, Mexico, Bolivia lose status; 5,400+ US cases.
- **Plane crash kills 19** — Military plane crashes in Siberia; all on board die.
- **Depardieu pleads guilty** — French actor admits assault charge, drops appeal.
- **Houthi advance** — Government troops retreat from the Red Sea coast.
- **France strikes again** — Second nationwide strike over pay and conditions.
- **Kyiv bridges hit** — Russian strikes hit two bridges, disrupting water and power.

**Also on Tuesday 17 November** (18 one-liners in the image): Moldova, the West Bank, the UK, Iran, Gaza, Russia, France, Trump, Cuba, China–Canada, Thailand, Cyclone Alvan in India, Kenya, Pope Leo, Apple, Jensen Huang's Congress testimony, China, and oil prices.

The image is drawn by `draw.py` (Python + PIL) from flat shapes and crisp text, so it stays legible at small sizes and contains no invented details. Contested claims are marked as claims in the image.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (standard library only, no network) copies `entry.png` to the output directory as `entry.png`. Both runs write the same bytes.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
