# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

lines = s.splitlines()
out = []
cur = None
for ln in lines:
    m = re.match(r"^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜", ln)
    if m:
        cur = (m.group(2), m.group(3))
        out.append(ln); continue
    m2 = re.match(r"^\[[\d.]+s-[\d.]+s\](，.*)$", ln)
    if m2 and cur:
        out.append(f"[{cur[0]}s-{cur[1]}s]{m2.group(1)}")
        continue
    # 裸名收纳（跳过锁定/映射/字幕行）
    if ln.startswith("【") and ("】：" in ln or "参考图映射" in ln):
        out.append(ln); continue
    if ln.startswith("（字幕"):
        out.append(ln); continue
    for name in ("沈幼怡", "陈诚", "手机", "玻璃杯", "行李箱", "双肩书包", "黑拖鞋"):
        ln = re.sub(r"(?<!【)" + name + r"(?!】)", "【" + name + "】", ln)
    out.append(ln)

s = "\n".join(out).replace("【【", "【").replace("】】", "】")
open(f, "w", encoding="utf-8").write(s)
print("dialogue windows aligned; bare names wrapped")
