# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
lines = open(f, encoding="utf-8").read().split("\n")
out, cur = [], None
for ln in lines:
    m = re.match(r"^【镜头\d+｜\[([\d.]+)s-([\d.]+)s\]｜", ln)
    if m:
        cur = (m.group(1), m.group(2))
        out.append(ln); continue
    m2 = re.match(r"^\[[\d.]+s-[\d.]+s\](.*)$", ln)
    if m2 and cur:
        out.append(f"[{cur[0]}s-{cur[1]}s]{m2.group(1)}")
        continue
    # 正文裸名（只处理非锁定/非字幕行）
    if not (ln.startswith("【") and ("】：{" in ln or "参考图映射" in ln)) and not ln.startswith("（字幕"):
        ln = re.sub(r"(?<!【)手机(?!】)", "【手机】", ln)
    out.append(ln)
s = "\n".join(out).replace("【【", "【").replace("】】", "】")
s = re.sub(r"\{资产库：【([^】]+)】\}", r"{资产库：\1}", s)
open(f, "w", encoding="utf-8").write(s)
print("台词窗口已对齐镜头；裸名已处理")
