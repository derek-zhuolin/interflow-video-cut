#!/usr/bin/env python3
"""Lint the reference card HTML for hand-edit breakage.

Catches the failure mode that slipped through cdff892: an opening tag whose
closing '>' got dropped while editing a data-anim value across line breaks.
Without the '>', the HTML parser swallows the following body text / child
element into the tag's attribute list and the card content silently vanishes
at render.

Usage:  python3 scripts/lint-cards.py [root]
Exit 0 = clean, 1 = broken tags found.
"""
import sys
import re
import glob
import os

# Line that opens a tag and ends on a quoted attribute with no '>' yet.
OPEN_TAG_UNCLOSED = re.compile(r'<[a-zA-Z][^>]*"\s*$')
# Next line is just another attribute -> legit multi-line tag, not broken.
ATTR_CONTINUATION = re.compile(r'^\s*[a-zA-Z-]+\s*=')


def find_broken(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    broken = []
    for i, ln in enumerate(lines):
        if not (OPEN_TAG_UNCLOSED.search(ln) and "<" in ln
                and ">" not in ln.split("<")[-1]):
            continue
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        nxt = lines[j] if j < len(lines) else ""
        if not ATTR_CONTINUATION.match(nxt):  # next line is text/child => never closed
            broken.append((i + 1, ln.strip()[:70], nxt.strip()[:50]))
    return broken


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(__file__))
    pattern = os.path.join(root, "references", "**", "*.html")
    total = 0
    for f in sorted(glob.glob(pattern, recursive=True)):
        for line, tag, nxt in find_broken(f):
            total += 1
            rel = os.path.relpath(f, root)
            print(f"BROKEN {rel}:{line}")
            print(f"   unclosed: {tag}")
            print(f"   next:     {nxt}")
    if total:
        print(f"\n{total} unclosed opening tag(s) — add the missing '>'.")
        return 1
    print("OK: no unclosed opening tags in references/**/*.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
