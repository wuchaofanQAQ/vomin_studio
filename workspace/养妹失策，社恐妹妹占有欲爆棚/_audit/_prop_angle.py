# -*- coding: utf-8 -*-
# 1) 脚本模板 + 校验标记
p = r"skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        "能看清体积与厚度；右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），"
        "看不到正面、侧面和轮子。背景为{bg}，画面内无任何文字。电影级写实质感，{wear}。\\n道具：{desc}"'''
new = '''        "能看清体积与厚度；右侧为正面视角，与左侧同一件道具、同一比例。"
        "背景为{bg}，画面内无任何文字。电影级写实质感，{wear}。\\n道具：{desc}"'''
assert t.count(old) == 1
t = t.replace(old, new)
t = t.replace('"道具": {"key": "description", "markers": ["正偏侧", "俯视图", "无任何文字"]}',
              '"道具": {"key": "description", "markers": ["正偏侧", "正面视角", "无任何文字"]}')
open(p, "w", encoding="utf-8").write(t)
print("script ok")

# 2) SKILL.md
p = r"skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
t = t.replace("右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），看不到正面、侧面和轮子。",
              "右侧为正面视角，与左侧同一件道具、同一比例。")
t = t.replace("道具双视角图（左正偏侧 + 右俯视，绿幕或白底、无文字）", "道具双视角图（左正偏侧 + 右正面，绿幕或白底、无文字）")
t = t.replace("- **道具**：左侧正偏侧能看清体积与厚度，右侧俯视看顶面结构与比例；背景按颜色二选一（浅色用绿幕、其余用白底）；无人物、无文字、无 logo。",
              "- **道具**：左侧正偏侧能看清体积与厚度，右侧正面看整体比例与五金；背景按颜色二选一（浅色用绿幕、其余用白底）；无人物、无文字、无 logo。")
t = t.replace("左侧为道具的正偏侧视角，能看清体积与厚度；右侧为俯视图：", "左侧为道具的正偏侧视角，能看清体积与厚度；右侧为正面视角：")
open(p, "w", encoding="utf-8").write(t)
print("SKILL ok")

# 3) prompt-formats.md
p = r"skills\drama-asset-generation\references\prompt-formats.md"
t = open(p, encoding="utf-8").read()
t = t.replace("右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），看不到正面、侧面和轮子。",
              "右侧为正面视角，与左侧同一件道具、同一比例。")
t = t.replace("## 三、道具 · 双视角图", "## 三、道具 · 双视角图（正偏侧 + 正面）")
t = t.replace("要点：左侧能看体积与厚度，右侧看顶面结构。", "要点：左侧能看体积与厚度，右侧正面看整体比例与五金。")
open(p, "w", encoding="utf-8").write(t)
print("formats ok")

# 4) checklist
p = r"skills\drama-asset-generation\references\review-checklist.md"
t = open(p, encoding="utf-8").read()
t = t.replace("| 1 | 双视角 | 左侧正偏侧、右侧俯视，两个视角都在 |",
              "| 1 | 双视角 | 左侧正偏侧、右侧正面，两个视角都在 |")
open(p, "w", encoding="utf-8").write(t)
print("checklist ok")
