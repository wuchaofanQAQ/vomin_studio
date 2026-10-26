# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        masked = BODY_ASSET_RE.sub("§", s["style"] + s["live"] + s["space"] + s["final"]
                                  + "".join(sh["body"] for sh in s["shots"]))'''
new = '''        masked = BODY_ASSET_RE.sub("§", s["style"] + s["live"] + s["space"] + s["final"]
                                  + "".join(sh["body"] for sh in s["shots"]))
        masked = re.sub(r"「[^」]*」", "§", masked)  # 引号内是台词/屏幕文字，不是资产引用'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("quoted text excluded from bare-name check")
