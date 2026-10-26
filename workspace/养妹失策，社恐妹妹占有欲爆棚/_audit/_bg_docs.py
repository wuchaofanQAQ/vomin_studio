# -*- coding: utf-8 -*-
# 1. prompt-formats.md
p = r"skills\drama-asset-generation\references\prompt-formats.md"
t = open(p, encoding="utf-8").read()
t = t.replace("背景为纯绿幕或纯白，画面内无任何文字。", "背景为{背景}，画面内无任何文字。")
t = t.replace("""要点：左侧能看体积与厚度，右侧看顶面结构；背景统一便于抠图。""",
"""要点：左侧能看体积与厚度，右侧看顶面结构。

**背景规则（必须二选一，不许写「绿幕或白色」让模型自己挑）**：

| 道具颜色 | 背景 | 理由 |
|---|---|---|
| 偏白、浅色、银色、透明、发光 | `纯绿幕背景` | 白底会把浅色道具吃掉，抠不出轮廓 |
| 其余颜色（深色、彩色） | `纯白背景` | 通用，干净 |

`asset_prompt.py build` 会按描述自动判定并代入 `{背景}`；判定词表：白色/米白/奶白/乳白/象牙/浅色/浅灰/浅蓝/浅粉/浅黄/浅绿/银/透明/玻璃/雪白/淡/发光。""")
t = t.replace("| 背景杂乱 | `浅净背景`（角色）/ `绿幕或白色背景`（道具） |",
              "| 背景杂乱 | `浅净背景`（角色）/ `纯白背景` 或 `纯绿幕背景`（道具，按颜色二选一） |")
open(p, "w", encoding="utf-8").write(t)
print("prompt-formats ok")

# 2. SKILL.md
p = r"skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\n道具：{描述}"
new = "背景为{背景}，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\n道具：{描述}"
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "**通用**：`{描述}` 就是库里那句 ≤50 字描述，原样代入，不扩写、不加剧情；画风只在末尾由全局设定追加，提示词里不堆\"8K/超清\"。"
new2 = old2 + "\n\n**道具背景必须二选一**：偏白/浅色/银色/透明/发光的道具用 `纯绿幕背景`（白底会吃掉轮廓），其余用 `纯白背景`。不许写\"绿幕或白色\"让模型自己挑；`asset_prompt.py build` 会按描述自动判定。"
assert t.count(old2) == 1
t = t.replace(old2, new2)
old3 = "- **道具**：左侧正偏侧能看清体积与厚度，右侧俯视看顶面结构与比例；背景统一绿幕或白底，便于抠图；无文字、无 logo。"
new3 = "- **道具**：左侧正偏侧能看清体积与厚度，右侧俯视看顶面结构与比例；背景按颜色二选一（浅色用绿幕、其余用白底）；无人物、无文字、无 logo。"
assert t.count(old3) == 1
t = t.replace(old3, new3)
open(p, "w", encoding="utf-8").write(t)
print("SKILL ok")

# 3. review-checklist.md
p = r"skills\drama-asset-generation\references\review-checklist.md"
t = open(p, encoding="utf-8").read()
old = "| 4 | 背景 | 绿幕或纯白，干净可抠 |"
new = "| 4 | 背景 | 浅色道具是纯绿幕、其余是纯白，干净可抠（不能两者都出现） |"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("checklist ok")
