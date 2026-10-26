# -*- coding: utf-8 -*-
import re

# 1) 引号/字幕里的【】还原
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
s = re.sub(r"「([^」]*)」", lambda m: "「" + m.group(1).replace("【", "").replace("】", "") + "」", s)
s = re.sub(r"（字幕·【([^】]+)】）", r"（字幕·\1）", s)

# 2) 每段补齐待出图
props = ["手机", "黑拖鞋", "玻璃杯"]
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    for p_ in props:
        if f"【{p_}】" in rest and f"待出图：【{p_}】" not in lock:
            lock = lock.rstrip("\n") + f"\n待出图：【{p_}】\n\n"
    out += [head, lock + rest]
s = out[0] + "".join("## " + h + "\n" + b for h, b in zip(out[1::2], out[2::2]))
open(f, "w", encoding="utf-8").write(s)

# 3) 校验器：可见性只查 角色/群像
cp = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(cp, encoding="utf-8").read()
old = '''            subj = found[0]
            for nm in dict.fromkeys(found):'''
new = '''            subj = found[0]
            tbl = {e["name"]: e["table"] for e in s["lock"]}
            for nm in dict.fromkeys(found):
                if tbl.get(nm) not in ("角色库", "群像", "待出图"):
                    if tbl.get(nm) != "角色库":
                        continue'''
assert t.count(old) == 1
t = t.replace(old, new)
# 去掉多余的内层 if
t = t.replace('''                if tbl.get(nm) not in ("角色库", "群像", "待出图"):
                    if tbl.get(nm) != "角色库":
                        continue''', '''                if tbl.get(nm) != "角色库":
                    continue''')
open(cp, "w", encoding="utf-8").write(t)
print("checker: 可见性只看角色")
