# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

anchor = """        # ---- 时间轴 ----"""
insert = """        # ---- 复杂度与参考图预算（30 秒是上限，不是固定值） ----
        def _count(prefix):
            return sum(1 for aid in seen_ids if re.fullmatch(prefix + r"\\d{2}", aid))

        n_scene, n_char = _count("S"), _count("R")
        n_fx, n_mob = _count("FX"), _count("M")
        refs = n_scene + n_char
        score = (max(0, n_scene - 1) * 2 + max(0, n_char - 2)
                 + max(0, refs - 3) + (1 if n_fx else 0) + (1 if n_mob else 0))
        cap = 30 if score <= 0 else 24 if score <= 2 else 20 if score <= 4 else 15
        if refs > 5:
            errors.append(f"{tag} 参考图 {refs} 张（场景{n_scene}+角色{n_char}）> 5，必须拆段或改用群像资产")
        if dur > cap + 0.01:
            errors.append(f"{tag} 段长 {fmt(dur)} > 复杂度上限 {cap}s（场景{n_scene}/角色{n_char}/参考图{refs}/特效{n_fx}/群像{n_mob}），请拆段或缩短")

        # ---- 时间轴 ----"""
assert t.count(anchor) == 1
t = t.replace(anchor, insert)

t = t.replace('("每段 6~30 秒", all(6 <= (s["end"] - s["start"]) <= 30.01 for s in doc), "ok"),',
              '("每段 6~30 秒（30 为上限）", all(6 <= (s["end"] - s["start"]) <= 30.01 for s in doc), "ok"),\n        ("参考图 ≤5 张", all_true_refs, "ok"),')
open(p, "w", encoding="utf-8").write(t)
print("patched; now add refs summary")
