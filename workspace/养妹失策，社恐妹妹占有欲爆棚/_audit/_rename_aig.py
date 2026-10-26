# -*- coding: utf-8 -*-
import pathlib
files = [str(p) for p in pathlib.Path("skills").rglob("*.md")] + ["CLAUDE.md"]
files += [str(p) for p in pathlib.Path(".").glob("*.py")]
total = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    n = t.count("asset-image-generation")
    if n:
        t = t.replace("asset-image-generation", "drama-asset-generation")
        open(f, "w", encoding="utf-8").write(t)
        print(f"{f}: {n}")
        total += n
print("total:", total)
