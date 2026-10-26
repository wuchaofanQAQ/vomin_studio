# -*- coding: utf-8 -*-
import re
p = r"skills\drama-segment-generation\references\example-segment.md"
t = open(p, encoding="utf-8").read()
t2 = re.sub(r"【对白\s*(\d{2}:\d{2}(?:\.\d)?)\s*-\s*(\d{2}:\d{2}(?:\.\d)?)】", r"\1-\2，", t)
print("replaced:", t.count("【对白"), "->", t2.count("【对白"))
open(p, "w", encoding="utf-8").write(t2)
