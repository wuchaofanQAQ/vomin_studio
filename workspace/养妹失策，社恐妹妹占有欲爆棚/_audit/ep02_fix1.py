# -*- coding: utf-8 -*-
import re

# 1) 校验器：画外声不要求进锁定；总时长可配置
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = '''            for d in sh["dlg"]:
                who = d["who"].replace("画外音", "").strip()'''
new = '''            for d in sh["dlg"]:
                if "画外" in d["who"] or "画外" in d["text"]:
                    continue  # 画外声只有声音，不需要参考图
                who = d["who"].replace("画外音", "").strip()'''
assert t.count(old) == 1
t = t.replace(old, new)

t = t.replace('''    ap.add_argument("--target", type=float, default=SEG_MAX)''',
              '''    ap.add_argument("--target", type=float, default=SEG_MAX)
    ap.add_argument("--total", type=float, default=TOTAL_MAX)''')
t = t.replace('''    if total > TOTAL_MAX + 1e-6:
        errors.append(f"全片总时长 {fmt(total)} > {fmt(TOTAL_MAX)}")''',
              '''    if total > 180 + 1e-6 and total > args_total_holder[0] + 1e-6:
        errors.append(f"全片总时长 {fmt(total)} > {fmt(args_total_holder[0])}")''')
t = t.replace('''def check(segs: list[dict], target: float) -> tuple[list[str], list[str]]:''',
              '''args_total_holder = [TOTAL_MAX]


def check(segs: list[dict], target: float) -> tuple[list[str], list[str]]:''')
t = t.replace('''    errors, notes = check(segs, args.target)''',
              '''    args_total_holder[0] = args.total
    errors, notes = check(segs, args.target)''')
open(p, "w", encoding="utf-8").write(t)
print("checker patched")

# 2) ep02 p01 修正
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep02_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
pairs = [
("十五镜按下列时码依次硬切", "十四镜按下列时码依次硬切"),
("中景是出风口，后景是虚焦的天花板。", "中景是出风口，后景是虚焦的顶面。"),
("42码的黑拖鞋套在她脚上", "42码的【黑拖鞋】套在她脚上"),
("【陈诚】（OS、心里嘀咕说）：「就住一晚，别再给我整出个感冒来。」", "【陈诚】（OS、心里嘀咕说）：「就住一晚，别给我整出感冒来。」"),
("【陈诚】（OS、心疼地说）：「这老货色开一宿十块，够我吃一天。」", "【陈诚】（OS、心疼地说）：「这老货开一宿十块，够我吃一天。」"),
]
for a, b in pairs:
    c = s.count(a)
    print(c, a[:28])
    if c == 1:
        s = s.replace(a, b)
open(f, "w", encoding="utf-8").write(s)
print("ep02 p01 patched")
