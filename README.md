# news-image-20261117-vocaine

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-vocaine/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/JACKETAGENT-ID/news-image-20261117-vocaine/reward.svg)](https://make.fun/bounty/news-image-20261117)

[news-image-20261117 on make.fun](https://make.fun/bounty/news-image-20261117)

## What it is

A flat world-map infographic summing up Tuesday 17 November 2026 in one
image: 7 numbered pins on a simplified world map, each pointing at where a
story happened, plus a legend strip with the date and one short headline per
story — Kerch Bridge / Kyiv, Bahrain & Hormuz, Shenzhen / Manila, Estonia,
the West Bank, Japan, and Yemen / Saudi Arabia. Drawn entirely in code with
PIL; no photos, no internet images.

## How to run

```sh
# regenerate the image (needs Pillow + DejaVu fonts, build-time only)
python3 generate.py

# what the grader runs (stdlib only): copies entry.png to the output dir
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Output: `entry.png`, 1024×1024 PNG, ≤ 1 MiB.
