[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/cendelobening/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/cendelobening/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

# The World — 18 November 2026, in one image

A newspaper front page that sums up Wednesday 18 November 2026's world
news in a single 1024×1024 image. `entry.png` is drawn entirely by a
pure-stdlib Python generator (custom 5×7 bitmap font, hand-rolled PNG
encoder — no Pillow, no image libraries), and `main.py` validates the
image and copies it to the output directory. The image is generated
by `gen.py` — regenerate it any time with `python3 gen.py entry.png`.

## Design (v2)

A bold broadsheet redesign: a black masthead with cream type and gold
rules over a red EXTRA date band, a dark-red radar lead panel for the
Iran–US strikes (concentric scope rings, a gold sweep, drone and
missile art, and story chips), and a dense grid of four framed panels
with flag, bridge and temple art, closed by a Gaza aid strip and a
ruled footer.

## The six stories

1. **Trump lands in Manila** — the US president arrives in the Philippines
   for Quad talks ahead of his China visit and the APEC summit in Shenzhen.
2. **Crimea Bridge hit again** — Ukraine strikes the bridge for a second
   consecutive day as Russia keeps pounding Kyiv's bridges.
3. **Iran–US strikes escalate** — Iran attacks a US military radar system in
   Bahrain with drones; the US carries out precision strikes on an IRGC
   missile launch site on Iran's Qeshm Island in the Strait of Hormuz.
4. **Canada, China extend deals** — trade deals extended as Xi meets PM
   Mark Carney ahead of the APEC summit.
5. **Israel power shift** — President Herzog asks ex-army chief Gadi
   Eisenkot to try to form Israel's next government, bypassing Netanyahu;
   Britain sanctions Israeli settlement firms.
6. **Aid call for flooded Gaza** — Australia, Canada, Italy and the UK
   jointly call on Israel to let aid reach flooded Gaza.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` checks `entry.png` (PNG signature, 1024×1024, at most 1 MiB,
valid chunk CRCs, decodes to exactly 1024 RGB scanlines) and copies it
byte-for-byte to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`),
mode 0644. The run is deterministic: every invocation writes identical
bytes.
