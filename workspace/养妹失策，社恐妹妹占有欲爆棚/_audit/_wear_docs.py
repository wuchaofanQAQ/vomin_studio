# -*- coding: utf-8 -*-
# docs: 质感占位符 + 规则
p = r"skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "电影级写实质感，保留道具的真实材质与使用痕迹。\n道具：{描述}"
new = "电影级写实质感，{质感}。\n道具：{描述}"
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "**道具背景必须二选一**：偏白/浅色/银色/透明/发光的道具用 `纯绿幕背景`（白底会吃掉轮廓），其余用 `纯白背景`。不许写\"绿幕或白色\"让模型自己挑；`asset_prompt.py build` 会按描述自动判定。"
new2 = old2 + "\n\n**道具质感默认光洁**：`{质感}` 默认是「表面光洁，无划痕、无破损，材质细节清晰」；只有描述里写了磨损/划痕/旧/破/锈/脏/裂/掉漆/褪色，才换成「保留描述中的使用痕迹与磨损」（写「无划痕」不算）。"
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)

p = r"skills\drama-asset-generation\references\prompt-formats.md"
t = open(p, encoding="utf-8").read()
t = t.replace("电影级写实质感，保留道具的真实材质与使用痕迹。", "电影级写实质感，{质感}。")
old = "`asset_prompt.py build` 会按描述自动判定并代入 `{背景}`；判定词表：白色/米白/奶白/乳白/象牙/浅色/浅灰/浅蓝/浅粉/浅黄/浅绿/银/透明/玻璃/雪白/淡/发光。"
new = old + "\n\n**质感默认光洁**：`{质感}` 默认「表面光洁，无划痕、无破损，材质细节清晰」；描述里写了磨损/划痕/旧/破/锈/脏/裂/掉漆/褪色才换成「保留描述中的使用痕迹与磨损」。要一条新道具就写「表面光洁无划痕」，别只写「精致」——模型会把「真实使用痕迹」画成划痕。"
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)

p = r"skills\drama-asset-generation\references\review-checklist.md"
t = open(p, encoding="utf-8").read()
old = "| 6 | 材质 | 材质与使用痕迹真实（金属、皮质、塑料分得清） |"
new = "| 6 | 材质 | 材质真实（金属、皮质、塑料分得清）；表面与描述一致——默认应光洁无划痕，写了磨损才允许有痕迹 |"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("docs updated")
