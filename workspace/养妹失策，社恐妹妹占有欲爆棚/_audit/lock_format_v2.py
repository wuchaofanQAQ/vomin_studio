# -*- coding: utf-8 -*-
import re

# 1) 校验器：支持新格式「图N =【名】 = {资产库：名}」
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
if "LOCK_RE2" not in t:
    t = t.replace('MAP_RE = re.compile(r"^【参考图映射】(.+)$")',
                  'MAP_RE = re.compile(r"^【参考图映射】(.+)$")\n'
                  'LOCK_RE2 = re.compile(r"^图\\s*(\\d+)\\s*=\\s*【([^】]+)】\\s*=\\s*\\{([^：}]+)[:：]([^}]+)\\}")')
    t = t.replace('''            m = LOCK_RE.match(line)
            if m:''', '''            if line.strip().endswith("："):
                continue  # 类型分组标题（角色：/场景：/道具：）
            m = LOCK_RE2.match(line) or LOCK_RE.match(line)
            if m:''')
open(p, "w", encoding="utf-8").write(t)
print("checker 已支持新锁定格式")

# 2) 分镜：把锁定块改成分组格式
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

segs = re.split(r"(?m)^(## 【第\d+段.*?】)$", s)
out = [segs[0]]
for i in range(1, len(segs), 2):
    head, body = segs[i], segs[i + 1]
    if "【本段资产锁定】" not in body:
        out += [head, body]; continue
    a = body.index("【本段资产锁定】")
    b = body.index("【本段现场生成】")
    lock_txt = body[a:b]
    names = re.findall(r"^【([^】]+)】：\{([^：}]+)[:：]([^}]+)\}", lock_txt, re.M)
    pending = re.findall(r"^待出图：【([^】]+)】", lock_txt, re.M)
    new = "【本段资产锁定】\n"
    n = 1
    for kind, label in (("角色库", "角色"), ("场景库", "场景"), ("道具库", "道具")):
        rows = [(nm, tb, rw) for nm, tb, rw in names if tb == kind]
        if not rows:
            continue
        new += f"{label}：\n"
        for nm, tb, rw in rows:
            new += f"图{n} =【{nm}】 = {{{tb}：{rw}}}\n"
            n += 1
    if pending:
        new += "待出图：\n" + "".join(f"【{x}】\n" for x in pending)
    new += "\n"
    body = body[:a] + new + body[b:]
    out += [head, body]
s = "".join(out)
open(f, "w", encoding="utf-8").write(s)
print("分镜锁定块已改分组格式")
