# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
t = open(p, encoding="utf-8").read()

old = '''_TIMELINE_RE = re.compile(r"\\s*(\\d+):(\\d+)\\s*[-–—~]\\s*(\\d+):(\\d+)")'''
new = '''_TIMELINE_RE = re.compile(r"\\s*(\\d+):(\\d+)\\s*[-–—~]\\s*(\\d+):(\\d+)")
_TIMELINE_S_RE = re.compile(r"\\s*\\[?\\s*([\\d.]+)s?\\s*[-–—~]\\s*([\\d.]+)s\\s*\\]?")'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''    m = _TIMELINE_RE.match(shot.get("timeline") or "")
    if m:
        span = (int(m[3]) * 60 + int(m[4])) - (int(m[1]) * 60 + int(m[2]))
        if span > 0:
            return min(span, MAX_SHOT_SECONDS)
    return default'''
new2 = '''    tl = shot.get("timeline") or ""
    m = _TIMELINE_RE.match(tl)
    if m:
        span = (int(m[3]) * 60 + int(m[4])) - (int(m[1]) * 60 + int(m[2]))
        if span > 0:
            return min(span, MAX_SHOT_SECONDS)
    m = _TIMELINE_S_RE.match(tl)
    if m:
        span = float(m[2]) - float(m[1])
        if span > 0:
            return min(span, MAX_SHOT_SECONDS)
    return default'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("timeline parsing extended to [0s-30s]")
