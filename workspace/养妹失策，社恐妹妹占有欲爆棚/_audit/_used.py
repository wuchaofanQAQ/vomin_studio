p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        lock_set = set(names)
        used = set()'''
new = '''        lock_set = set(names)
        used = set()
        for nm in BODY_ASSET_RE.findall(s["style"] + s["space"] + s["final"] + s["live"]):
            if nm in lock_set:
                used.add(nm)'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("used scan widened")
