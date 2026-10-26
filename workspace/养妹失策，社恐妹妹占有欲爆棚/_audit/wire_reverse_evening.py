# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

DAY, EVE = "陈诚公寓客厅（反打玄关）", "陈诚公寓客厅（傍晚·反打玄关）"
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    if i >= 5:  # 第3、4段是傍晚
        body = body.replace(DAY, EVE)
        if f"【{EVE}】：" not in body:
            lock_end = body.index("【本段现场生成】")
            body = body[:lock_end].rstrip("\n") + f"\n【{EVE}】：{{场景库：{EVE}}}\n\n" + body[lock_end:]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    names = re.findall(r"^【([^】]+)】：\{", lock, re.M)
    mapping = "【参考图映射】" + "；".join(f"图{n+1}=【{nm}】" for n, nm in enumerate(names))
    lock = re.sub(r"【参考图映射】[^\n]+", mapping, lock, count=1)
    res += [head, lock + rest]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("evening reverse scene wired into p03/p04")
