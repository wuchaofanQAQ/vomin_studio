# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''            rate = cn_len(d["text"]) / max(d["end"] - d["start"], 1e-6)
            if rate > 5.35:'''
new = '''            rate = cn_len(d["text"]) / max(d["end"] - d["start"], 1e-6)
            # OS 旁白不按对白语速卡（旁白可压在动作上，节奏另算）
            if rate > 5.35 and "OS" not in sp:'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("OS rate exempt")
