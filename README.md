# The Day in the World — 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Kegelapan-ai/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Kegelapan-ai/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the [make.fun bounty “Sum up 24 November's world news in one
image”](https://make.fun/bounty/news-image-20261124): one program that writes
one front page summing up Tuesday 24 November 2026.

## The image

`image.png` is a 1024×1024 newspaper front page, drawn with Pillow by
`build_image.py`. Six stories, all checked against live reporting from
24 November 2026:

1. **Ukraine / Libya (lead)** — Kyiv says the sea-drone strike that sank the
   Russian corvette Merkury off Benghazi was self-defence, and confirms a
   second strike on the arms ship Sparta II in the Gulf of Finland.
2. **Markets** — Nvidia reinstates Jensen Huang as chief executive; shares
   jump 31%, the best day since 2003, adding about $950bn in value.
3. **War in Ukraine** — a Russian strike partly destroys a five-storey
   apartment block in Zaporizhzhia: 2 killed, 22 wounded; a Russian drone
   briefly enters Polish airspace again.
4. **Gaza** — Israeli strikes kill at least six Palestinians, including two
   police officers; Hamas security chief Naeem Abu Nahel is among the dead.
5. **Indonesia** — the death toll from the candy-factory fire in Cikande,
   Banten, rises to 26, with eight more workers still missing.
6. **Colombia** — a car bomb outside the governor's office in Villavicencio
   injures more than 20 people; no deaths are reported.

The footer ticker adds the Abu Dhabi talks ending, the Nepal earthquake
(magnitude 5.6), the Pentagon holding back 60 Patriot missiles for Kyiv, and
the World Chess Championship opening in Geneva. Sources: Reuters, AP, CNN,
Kyiv Independent, El Tiempo, Xinhua. Any figure that could not be confirmed
against live reporting was left out.

## Run it

```sh
python3 build_image.py        # redraws image.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` copies the checked image into the output directory, so two runs
write byte-identical files. No network is used. Python 3.13, standard
library plus Pillow for the drawing step only.

## Licence

MIT — see [LICENSE](LICENSE).
