# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 场景统一：客厅图已包含阳台
s = s.replace("陈诚公寓玄关客厅（傍晚）", "陈诚公寓客厅")
s = s.replace("【陈诚公寓阳台】：{场景库：陈诚公寓阳台}\n", "")
s = s.replace("陈诚公寓阳台", "陈诚公寓客厅")

# 2) 段落锁定去重（场景行去重、映射按锁定顺序重建）
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    lines = [l for l in lock.splitlines() if l.strip()]
    # 去重场景行
    seen, out = set(), []
    has_scene = False
    for l in lines:
        if "{场景库：" in l:
            if has_scene:
                continue
            has_scene = True
        out.append(l)
    lock = "\n".join(out) + "\n\n"
    # 重建映射
    names = re.findall(r"【([^】]+)】：\{场景库", lock) + \
            re.findall(r"【([^】]+)】：\{角色库", lock) + \
            re.findall(r"【([^】]+)】：\{道具库", lock)
    add_scene = ""
    if "【陈诚公寓玄关】" in rest and "【陈诚公寓玄关】：" not in lock:
        lock = lock.rstrip("\n") + "\n【陈诚公寓玄关】：{场景库：陈诚公寓玄关}\n\n"
        names = re.findall(r"【([^】]+)】：\{场景库", lock) + \
                re.findall(r"【([^】]+)】：\{角色库", lock) + \
                re.findall(r"【([^】]+)】：\{道具库", lock)
    mapping = "【参考图映射】" + "；".join(f"图{n+1}=【{nm}】" for n, nm in enumerate(names))
    lock = re.sub(r"【参考图映射】[^\n]+", mapping, lock, count=1)
    res += [head, lock + rest]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("scenes unified; maps rebuilt")
