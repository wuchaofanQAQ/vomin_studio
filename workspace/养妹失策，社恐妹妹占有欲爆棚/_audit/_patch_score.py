# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        refs = len(anchored)
        score = (max(0, n_scene - 1) * 2 + max(0, n_char - 2)
                 + max(0, refs - 3) + (1 if n_fx else 0) + (1 if n_mob else 0))'''
new = '''        refs = len(anchored)                       # 所有带图资产（含道具），用于 ≤5 张限制
        core_refs = n_scene + n_char               # 场景+角色，用于难度评分（道具图不加重）
        score = (max(0, n_scene - 1) * 2 + max(0, n_char - 2)
                 + max(0, core_refs - 3) + (1 if n_fx else 0) + (1 if n_mob else 0))'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("score patched")
