# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_coverage.py"
t = open(p, encoding="utf-8").read()
old = '    quotes = [q for q in QUOTE_RE.findall(novel) if len(norm(q)) >= 3]'
new = '    quotes = [q for q in QUOTE_RE.findall(novel) if len(PUNCT.sub("", q)) >= 3]'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("sfx quotes filtered")
