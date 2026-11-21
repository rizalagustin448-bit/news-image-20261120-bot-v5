#!/usr/bin/env python3
"""News image v5 entrypoint: copy the drawn front page to the output dir.

Standard library only. The image (entry.png) ships in this repository; the
program just places the same bytes at $MAKEFUN_OUTPUT_DIR/entry.png so both
runs write identical output.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    # Fail loudly instead of shipping a truncated copy.
    if dst.stat().st_size != src.stat().st_size:
        raise SystemExit("entry.png copy size mismatch")


if __name__ == "__main__":
    main()
