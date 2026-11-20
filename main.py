#!/usr/bin/env python3
"""News-image-20261120 entry (Python 3.13, standard library only).

The poster is the finished entry.png beside this file: a 1024x1024
newspaper front page summing up Friday 20 November 2026 — Trump putting
the Iran war decision off to 2027, Cyclone Akvan's landfall in Odisha,
GTA VI outgrossing a Hollywood blockbuster, COP31's last day in Antalya,
and Glenn Phillips' treble in Wellington. This program places those exact
bytes at /output/entry.png, so every run reproduces the same file.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1_048_576


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    src = os.path.join(HERE, "entry.png")
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, "entry.png")
    shutil.copyfile(src, dst)

    # The gate rejects a truncated or corrupt image, so verify the copy
    # before finishing: same size and same sha256 as the poster in the
    # repository, and inside the 1 MiB gate.
    if os.path.getsize(src) != os.path.getsize(dst):
        raise SystemExit(f"entry.png copy failed size check: {dst}")
    if sha256(src) != sha256(dst):
        raise SystemExit(f"entry.png copy failed integrity check: {dst}")
    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB gate")
    # The gate also caps the image at 1024x1024 pixels; read the PNG
    # header (IHDR) directly instead of trusting the file name.
    with open(dst, "rb") as handle:
        header = handle.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SystemExit(f"entry.png is not a PNG: {dst}")
    width = int.from_bytes(header[16:20], "big")
    height = int.from_bytes(header[20:24], "big")
    if width > 1024 or height > 1024:
        raise SystemExit(f"entry.png is {width}x{height}, over 1024x1024")
    print(f"news-image: wrote {dst} ({size} bytes, {width}x{height}, "
          f"sha256 {sha256(dst)[:16]}...)")


if __name__ == "__main__":
    main()
