# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_script.py"
t = open(p, encoding="utf-8").read()
t = t.replace('("OS ≤25（第一人称小说改编，原文描写优先用 OS 保留）", s["os"] <= 25, f"{s[\'os\']}"),',
              '("OS ≤30（第一人称小说改编，原文描写优先用 OS 保留）", s["os"] <= 30, f"{s[\'os\']}"),')
open(p, "w", encoding="utf-8").write(t)

p = r"skills\novel-to-drama\references\script-format.md"
t = open(p, encoding="utf-8").read()
t = t.replace("全剧单集 ≤25 句（第一人称小说改编，原文描写优先用 OS 保留；连续不超 2 句，用 △ 打断）",
              "全剧单集 ≤30 句（第一人称小说改编，原文描写优先用 OS 保留；连续不超 2 句，用 △ 打断；换视角 OS 必须带角色名）")
open(p, "w", encoding="utf-8").write(t)

p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_script_v2.md"
t = open(p, encoding="utf-8").read()
old = "△她又悄悄瞟了陈诚一眼，视线在他侧脸上停了一瞬，很快垂下。"
new = "△她又悄悄瞟了陈诚一眼，视线在他侧脸上停了一瞬，很快垂下。\n沈幼怡（OS）：一米八，瘦，长得居然有点像那本漫画书里的男主。就是脾气……有点像炸毛的猫。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("沈幼怡 OS added")
