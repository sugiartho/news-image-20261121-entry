#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261121.

Copies the bundled front-page image (entry.png, in this repository) to
the output directory as entry.png. Stdlib only, no network, no clock,
no randomness: every run writes exactly the same bytes.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print("wrote", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
