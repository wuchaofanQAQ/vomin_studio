# -*- coding: utf-8 -*-
import re, shutil, os
files = [r"skills\drama-segment-generation\SKILL.md",
         r"skills\drama-segment-generation\references\project-adaptation.md"]
IDNAME = {"S01": "陈诚公寓走廊", "S02": "陈诚公寓玄关", "R01": "沈幼怡",
          "R02": "陈诚", "P01": "行李箱", "P02": "双肩书包"}

def tm(m):
    a = int(m.group(1)) * 60 + float(m.group(2))
    b = int(m.group(3)) * 60 + float(m.group(4))
    return f"[{a:g}s-{b:g}s]"

for f in files:
    shutil.copy(f, f + ".bak")
    t = open(f, encoding="utf-8").read()
    # 1) 时间窗
    t = re.sub(r"(\d{2}):(\d{2}(?:\.\d)?)-(\d{2}):(\d{2}(?:\.\d)?)", tm, t)
    # 2) 锁定条目 【R01｜名：{表：名}】 → 【名】：{表：名}
    t = re.sub(r"【([A-Z]\d{2})｜([^：】]+?)：(\{[^}]+\})】", r"【\2】：\3", t)
    # 3) 正文编号 → 【名】
    t = re.sub(r"([SRP])(\d{2})(?=[\u4e00-\u9fff])", lambda m: "【" + IDNAME.get(m.group(1) + m.group(2), m.group(0)) + "】", t)
    # 4) 参考图映射 图N=S01名 → 图N=【名】
    t = re.sub(r"图(\d+)=([A-Z]\d{2})", lambda m: f"图{m.group(1)}=【{IDNAME.get(m.group(2), m.group(2))}】", t)
    open(f, "w", encoding="utf-8").write(t)
    print("normalized", f)
