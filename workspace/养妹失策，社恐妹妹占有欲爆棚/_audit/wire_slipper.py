# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

s = s.replace("待出图：【黑拖鞋】", "【黑拖鞋】：{道具库：黑拖鞋}")

# 重建每段映射（按锁定顺序）
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    names = re.findall(r"【([^】]+)】：\{场景库", body) + \
            re.findall(r"【([^】]+)】：\{角色库", body) + \
            re.findall(r"【([^】]+)】：\{道具库", body)
    mapping = "【参考图映射】" + "；".join(f"图{n+1}=【{nm}】" for n, nm in enumerate(names))
    body = re.sub(r"【参考图映射】[^\n]+", mapping, body, count=1)
    res += [head, body]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("slipper wired")
