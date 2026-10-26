# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_script.py"
t = open(p, encoding="utf-8").read()
t = t.replace('("OS ≤30（第一人称小说改编，原文描写优先用 OS 保留）", s["os"] <= 30, f"{s[\'os\']}"),',
              '("OS ≤15（克制，情节靠画面，OS 只留关键判断）", s["os"] <= 15, f"{s[\'os\']}"),')
open(p, "w", encoding="utf-8").write(t)

p = r"skills\novel-to-drama\references\script-format.md"
t = open(p, encoding="utf-8").read()
t = t.replace("全剧单集 ≤30 句（第一人称小说改编，原文描写优先用 OS 保留；连续不超 2 句，用 △ 打断；换视角 OS 必须带角色名）",
              "全剧单集 ≤15 句（克制：情节靠画面推进，OS 只留关键判断；连续不超 2 句，用 △ 打断；换视角 OS 必须带角色名）")
open(p, "w", encoding="utf-8").write(t)
print("cap -> 15")
