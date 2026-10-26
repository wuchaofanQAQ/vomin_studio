# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''            m = LOCK_RE2.match(line) or LOCK_RE.match(line)
            if m:
                name, table, row = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()'''
new = '''            m2 = LOCK_RE2.match(line)
            m = LOCK_RE.match(line)
            if m2:
                name, table, row = m2.group(2).strip(), m2.group(3).strip(), m2.group(4).strip()
            elif m:
                name, table, row = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            if m2 or m:'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("LOCK_RE2 分组已修正")
