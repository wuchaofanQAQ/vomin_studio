# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = '''                if cat in ("场景", "角色"):
                    table = "场景库" if cat == "场景" else "角色库"
                    anchor = "{" + table + "：" + name + "}"
                    if anchor not in payload:
                        errors.append(f"{tag} {cat}资产【{aid}｜{name}】缺锚点 {anchor}")'''
new = '''                if cat in ("场景", "角色"):
                    table = "场景库" if cat == "场景" else "角色库"
                    anchor = "{" + table + "：" + name + "}"
                    if anchor not in payload and "待出图" not in payload:
                        errors.append(f"{tag} {cat}资产【{aid}｜{name}】缺锚点 {anchor}")'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''                if cat in ("场景", "角色"):
                    anchored.append((f"{letter}{num}", name.strip()))
                elif cat == "道具" and extra and "{" in extra:'''
new2 = '''                if cat in ("场景", "角色"):
                    if "待出图" not in payload:
                        anchored.append((f"{letter}{num}", name.strip()))
                elif cat == "道具" and extra and "{" in extra:'''
assert t.count(old2) == 1
t = t.replace(old2, new2)

open(p, "w", encoding="utf-8").write(t)
print("checker: 待出图 excluded from map")
