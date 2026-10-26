# -*- coding: utf-8 -*-
import pathlib
files = [str(p) for p in pathlib.Path("skills").rglob("*.md")] + ["CLAUDE.md"]
total = 0
for f in files:
    t = open(f, encoding="utf-8").read()
    n = t.count("novel-to-script")
    if n:
        t = t.replace("novel-to-script", "novel-to-drama")
        open(f, "w", encoding="utf-8").write(t)
        print(f"{f}: {n}")
        total += n
print("total:", total)
