# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
t = open(p, encoding="utf-8").read()
old = '''        span = float(m[2]) - float(m[1])
        if span > 0:
            return min(span, MAX_SHOT_SECONDS)'''
new = '''        span = float(m[2]) - float(m[1])
        if span > 0:
            span = min(span, MAX_SHOT_SECONDS)
            return int(span) if span == int(span) else span'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("duration returns int when whole")
