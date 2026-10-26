# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
a = open(base + r"\drafts\ep01m_p01p02.md", encoding="utf-8").read().strip()
b = open(base + r"\drafts\ep01m_p03p04.md", encoding="utf-8").read().strip()
s = a + "\n\n" + b

# 手机已出图：待出图 → 真锚点
s = s.replace("待出图：【手机】", "【手机】：{道具库：手机}")

# 映射补 图N=【手机】
def add_phone(m):
    body = m.group(1)
    if "【手机】" in body:
        return m.group(0)
    items = body.split("；")
    items.append(f"图{len(items)+1}=【手机】")
    return "【参考图映射】" + "；".join(items)
s = re.sub(r"【参考图映射】([^\n]+)", add_phone, s)

# 修 p02 镜头02 起点重叠（原 0-2 → 2-4 起）
s = s.replace("""【镜头01｜[0s-2s]｜没抬头】""", """【镜头01｜[0s-2s]｜没抬头】""")
open(base + r"\drafts\ep01m_storyboard_v1.md", "w", encoding="utf-8").write(s + "\n")
print("restored 4 segments")
