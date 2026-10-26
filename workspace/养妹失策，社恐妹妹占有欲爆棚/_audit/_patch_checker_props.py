# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

# 1) 道具带图锚点校验
old = '''                if cat in ("场景", "角色"):
                    table = "场景库" if cat == "场景" else "角色库"
                    anchor = "{" + table + "：" + name + "}"
                    if anchor not in payload:
                        errors.append(f"{tag} {cat}资产【{aid}｜{name}】缺锚点 {anchor}")'''
new = '''                if cat in ("场景", "角色"):
                    table = "场景库" if cat == "场景" else "角色库"
                    anchor = "{" + table + "：" + name + "}"
                    if anchor not in payload:
                        errors.append(f"{tag} {cat}资产【{aid}｜{name}】缺锚点 {anchor}")
                elif cat == "道具" and extra and "{" in extra:
                    anchor = "{道具库：" + name + "}"
                    if anchor not in payload:
                        errors.append(f"{tag} 道具【{aid}｜{name}】的锚点应为 {anchor}")'''
assert t.count(old) == 1
t = t.replace(old, new)

# 2) 带图资产改为按锁定顺序包含「带锚点的道具」
old2 = '''        anchored = []
        for cat, payload in s["lock_lines"]:
            if cat not in ("场景", "角色"):
                continue
            for letter, num, name, _ in ENTRY_RE.findall(payload):
                anchored.append((f"{letter}{num}", name.strip()))'''
new2 = '''        anchored = []
        for cat, payload in s["lock_lines"]:
            for letter, num, name, extra in ENTRY_RE.findall(payload):
                if cat in ("场景", "角色"):
                    anchored.append((f"{letter}{num}", name.strip()))
                elif cat == "道具" and extra and "{" in extra:
                    anchored.append((f"{letter}{num}", name.strip()))'''
assert t.count(old2) == 1
t = t.replace(old2, new2)

# 3) 参考图数按带图资产统计
old3 = '''        refs = n_scene + n_char'''
new3 = '''        refs = len(anchored)'''
assert t.count(old3) == 1
t = t.replace(old3, new3)

open(p, "w", encoding="utf-8").write(t)
print("checker patched")
