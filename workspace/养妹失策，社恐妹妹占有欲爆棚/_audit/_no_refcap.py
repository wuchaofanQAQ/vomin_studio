# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:40]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\drama-segment-generation\scripts\check_segment_prompt.py", [
('''        if refs > 5:
            errors.append(f"{tag} 参考图 {refs} 张（场景{n_scene}+角色{n_char}）> 5，必须拆段或改用群像资产")
''', ""),
('''        ("参考图 ≤5 张", max_refs <= 5, f"最多 {max_refs} 张"),''',
 '''        ("参考图张数（仅统计，不设上限）", True, f"最多 {max_refs} 张"),'''),
])

rep(r"skills\drama-segment-generation\SKILL.md", [
("参考图超过 5 张必须拆。", "参考图张数不设上限（API 没有这个限制），该用几张用几张。"),
("- **参考图超过 5 张必须拆**：拆段，或把同场多人合并成一个 `M` 群像资产。",
 "- **参考图不设上限**：场景图、角色图、道具图该挂都挂；拆段只看空间变化与动作密度。"),
("| 参考图 | ≤3 张 | 4~5 张 | ≥6 张 |", "| 参考图 | 1~2 张 | 3~4 张 | ≥5 张 |"),
])
print("ref cap removed")
