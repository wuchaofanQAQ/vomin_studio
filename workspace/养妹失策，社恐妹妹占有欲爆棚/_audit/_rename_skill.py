# -*- coding: utf-8 -*-
import os, pathlib
roots = ["skills", "."]
files = []
for root in ["skills"]:
    for p in pathlib.Path(root).rglob("*.md"):
        files.append(str(p))
files.append("CLAUDE.md")
total = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    n = t.count("script-to-prompt-30")
    if n:
        t = t.replace("script-to-prompt-30", "drama-segment-generation")
        open(f, "w", encoding="utf-8").write(t)
        print(f"{f}: {n}")
        total += n
print("total replaced:", total)
