# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = r'_DIALOGUE_LINE_RE = re.compile(r"^\s*([^：:\n]{1,20}?)\s*[：:]\s*(.+?)\s*$")'
new = r'_DIALOGUE_LINE_RE = re.compile(r"^\s*([^：:\n]{1,60}?)\s*[：:]\s*(.+?)\s*$")'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("patched")
