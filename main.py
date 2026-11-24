"""Entry program for the make.fun bounty "Sum up 24 November's world news in one image".

The front page is drawn once by build_image.py and kept as image.png
beside this file. This program only copies that image into the output
directory the harness names, so two runs write byte-identical files.
"""

import os
import shutil
import sys
from pathlib import Path


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    here = Path(__file__).resolve().parent
    source = here / "image.png"
    if not source.is_file():
        print(f"missing image: {source}", file=sys.stderr)
        return 1
    target = Path(out_dir) / "entry.png"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
