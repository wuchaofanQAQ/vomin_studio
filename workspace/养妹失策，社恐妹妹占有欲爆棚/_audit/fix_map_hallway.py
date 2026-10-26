# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 正文里的裸「玄关」→ 资产名
out = []
for ln in s.splitlines():
    if ln.startswith("【") and ("】：{" in ln or "参考图映射" in ln):
        out.append(ln); continue
    ln = re.sub(r"(?<!【)玄关(?!】)", "【陈诚公寓玄关】", ln)
    out.append(ln)
s = "\n".join(out).replace("【【", "【").replace("】】", "】")

# 2) 映射按锁定行顺序重建
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    names = re.findall(r"^【([^】]+)】：\{", lock, re.M)
    mapping = "【参考图映射】" + "；".join(f"图{n+1}=【{nm}】" for n, nm in enumerate(names))
    lock = re.sub(r"【参考图映射】[^\n]+", mapping, lock, count=1)
    res += [head, lock + rest]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("map order + 玄关 wording fixed")
