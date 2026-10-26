# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''        with open(raw[1:], "r", encoding="utf-8") as f:
            data = _json.load(f)'''
new = '''        with open(raw[1:], "r", encoding="utf-8-sig") as f:
            data = _json.load(f)'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("BOM tolerant read")
