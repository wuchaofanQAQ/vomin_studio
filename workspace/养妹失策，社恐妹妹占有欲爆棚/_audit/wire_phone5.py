# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 手机已出图：S4/S5 的待出图 → 真锚点
s = s.replace("待出图：【手机】", "【手机】：{道具库：手机}")

# 映射补 图N=【手机】（仅缺的段）
def add_phone(m):
    body = m.group(1)
    if "【手机】" in body:
        return m.group(0)
    items = body.split("；")
    items.append(f"图{len(items)+1}=【手机】")
    return "【参考图映射】" + "；".join(items)
s = re.sub(r"【参考图映射】([^\n]+)", add_phone, s)
open(f, "w", encoding="utf-8").write(s)
print("phone wired in all segments")
