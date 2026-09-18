#!/usr/bin/env python3
"""Bake a bottom fade into a screenshot so it dissolves into a page background.

    fade_bottom.py shot.jpg out.jpg --bg '#13161e' [--depth 30]

Why bake it instead of doing it in CSS: a gradient overlay or a ::after
pseudo-element is exactly what email clients strip, so the fade would look
right in a browser preview and be gone for the reader. Compositing it into
the pixels produces an ordinary JPEG that needs nothing from the client.

The fade only blends against the solid colour you pass as --bg. If the page
background changes, re-run this from the unfaded original — keep those.

Depth is a percentage of image height. The 30% default suits a screenshot
whose lower third is empty chrome. Drop to ~15% when the thing the reader is
meant to look at sits near the bottom of the frame, or the fade erases it.

Requires ImageMagick (`magick`).
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"error: {' '.join(cmd[:2])} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("source", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument(
        "--bg",
        required=True,
        help="page background to fade into, as #rrggbb (the email card colour)",
    )
    ap.add_argument(
        "--depth",
        type=float,
        default=30.0,
        help="fade height as %% of the image (default 30; use ~15 if the subject is near the bottom)",
    )
    ap.add_argument("--quality", type=int, default=88)
    args = ap.parse_args()

    if shutil.which("magick") is None:
        sys.exit("error: ImageMagick not found — install it (brew install imagemagick)")
    if not args.source.is_file():
        sys.exit(f"error: no such file: {args.source}")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", args.bg):
        sys.exit(f"error: --bg must be #rrggbb, got {args.bg!r}")
    if not 0 < args.depth <= 100:
        sys.exit(f"error: --depth must be between 0 and 100, got {args.depth}")

    width, height = run(
        ["magick", "identify", "-format", "%w %h", str(args.source)]
    ).split()
    width, height = int(width), int(height)
    fade = max(1, round(height * args.depth / 100))

    # Same RGB at both stops, varying only alpha: interpolating to a bare
    # "none" blends through transparent black and muddies the midpoint.
    gradient = f"gradient:{args.bg}00-{args.bg}ff"

    run([
        "magick", str(args.source),
        "(", "-size", f"{width}x{fade}", gradient, ")",
        "-geometry", f"+0+{height - fade}", "-composite",
        "-quality", str(args.quality), str(args.output),
    ])

    kb = args.output.stat().st_size / 1024
    print(f"{args.output} · {width}x{height} · fade {fade}px ({args.depth:g}%) · {kb:.0f} KB")
    print("remember: drop the img border and square its bottom corners, or it draws a line across the fade")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
