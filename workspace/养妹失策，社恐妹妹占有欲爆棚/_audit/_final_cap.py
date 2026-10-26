p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        if line.startswith("【本段终态】"):
            cur["in_lock"] = False
            cur["sections"].add("final")'''
new = '''        if line.startswith("【本段终态】"):
            cur["in_lock"] = False
            cur["sections"].add("final")
            cur["final"] = line'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("final captured")
