# -*- coding: utf-8 -*-
import json, re, os
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"

lib = json.load(open(os.path.join(base, "assets_lib.json"), encoding="utf-8"))
kind = {a["name"]: a.get("kind", "") for a in lib}
print("资产表:", kind)

rows = json.load(open(os.path.join(base, "drafts", "ep01m_shots.json"), encoding="utf-8"))
md_parts = []
for r in rows:
    p = r["prompt"]
    a = p.index("【本段资产锁定】")
    b = p.index("【本段现场生成】")
    block = p[a:b]
    names = re.findall(r"^【([^】]+)】：\{资产库：([^}]+)\}", block, re.M)
    pending = re.findall(r"^待出图：【([^】]+)】", block, re.M)
    if not names and "资产库" not in block:
        # 已经转换过或为空，尝试从参考图映射恢复
        m = re.search(r"【参考图映射】([^\n]+)", block)
        if m:
            names = [(n, n) for n in re.findall(r"图\d+=【([^】]+)】", m.group(1))]
    new = "【本段资产锁定】\n"
    n = 1
    for k, label in (("角色", "角色"), ("场景", "场景"), ("道具", "道具"), ("群像", "群像")):
        sel = [nm for nm, _ in names if kind.get(nm) == k]
        if not sel:
            continue
        new += f"{label}：\n"
        for nm in sel:
            if k == "群像":
                new += f"【{nm}】\n"
            else:
                new += f"图{n} =【{nm}】 = {{资产库：{nm}}}\n"
                n += 1
    if pending:
        new += "待出图：\n" + "".join(f"【{x}】\n" for x in pending)
    new += "\n"
    md_parts.append(p[:a] + new + p[b:])
    print(r["shot_id"], "锁定条数:", len(names), "待出图:", pending)

open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), "w", encoding="utf-8").write("\n\n".join(md_parts) + "\n")
print("md 重建完成")
