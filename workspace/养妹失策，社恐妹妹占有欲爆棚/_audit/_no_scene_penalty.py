# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        score = (max(0, n_scene - 1) * 2 + max(0, n_char - 2)
                 + max(0, core_refs - 3) + (1 if n_fx else 0) + (1 if n_mob else 0))'''
new = '''        # 复杂度只看人数/特效/群像：换场景与多参考图不再降上限（参考图本来就该多挂）
        score = max(0, n_char - 2) + (1 if n_fx else 0) + (1 if n_mob else 0)'''
assert t.count(old) == 1
t = t.replace(old, new)
t = t.replace('errors.append(f"{tag} 段长 {fmt(dur)} > 复杂度上限 {cap}s（场景{n_scene}/角色{n_char}/参考图{refs}/特效{n_fx}/群像{n_mob}），请拆段或缩短")',
              'errors.append(f"{tag} 段长 {fmt(dur)} > 复杂度上限 {cap}s（角色{n_char}/特效{n_fx}/群像{n_mob}），请拆段或缩短")')
open(p, "w", encoding="utf-8").write(t)
print("scene/ref penalty removed")
