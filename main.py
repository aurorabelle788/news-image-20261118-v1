#!/usr/bin/env python3
"""news-image-20261118-v1: copy the front-page image to the output dir.

The entry image (entry.png, a JPEG) sits beside this file. The program
copies it byte for byte to MAKEFUN_OUTPUT_DIR/entry.png (or /output when
the variable is unset), after checking the source really is a JPEG, and
then checks the copy matches the source exactly. No network, no drawing
at run time: the image is already drawn and stored in the repository.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(SRC, "rb") as f:
        head = f.read(2)
        f.seek(-2, os.SEEK_END)
        tail = f.read(2)
    if head != b"\xff\xd8":
        sys.exit("entry.png is not a JPEG (missing SOI marker)")
    if tail != b"\xff\xd9":
        sys.exit("entry.png is not a whole JPEG (missing EOI marker)")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    if sha256(SRC) != sha256(OUT):
        sys.exit("copied entry.png does not match the source")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
