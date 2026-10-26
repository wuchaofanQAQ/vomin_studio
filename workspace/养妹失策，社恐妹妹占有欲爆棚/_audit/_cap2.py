# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace(
"""    errors: list[str] = []
    total = 0.0
    id_map: dict[str, str] = {}     # id -> name""",
"""    errors: list[str] = []
    total = 0.0
    max_refs = 0
    id_map: dict[str, str] = {}     # id -> name""")

t = t.replace(
"""        cap = 30 if score <= 0 else 24 if score <= 2 else 20 if score <= 4 else 15
        if refs > 5:""",
"""        cap = 30 if score <= 0 else 24 if score <= 2 else 20 if score <= 4 else 15
        max_refs = max(max_refs, refs)
        if refs > 5:""")

t = t.replace(
'        ("参考图 ≤5 张", all_true_refs, "ok"),',
'        ("参考图 ≤5 张", max_refs <= 5, f"最多 {max_refs} 张"),')

open(p, "w", encoding="utf-8").write(t)
print("fixed")
