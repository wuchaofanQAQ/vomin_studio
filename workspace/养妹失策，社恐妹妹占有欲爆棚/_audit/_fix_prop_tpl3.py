# -*- coding: utf-8 -*-
old = "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，能看清体积与厚度；右侧为从正上方垂直向下的俯视图，只看到道具顶面与轮廓，不是正面。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。"
new = "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，能看清体积与厚度；右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），看不到正面、侧面和轮子。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。"
for p in [r"skills\drama-asset-generation\SKILL.md",
          r"skills\drama-asset-generation\references\prompt-formats.md",
          r"skills\drama-asset-generation\skills_placeholder"]:
    pass
import io
for p in [r"skills\drama-asset-generation\SKILL.md", r"skills\drama-asset-generation\references\prompt-formats.md"]:
    t = open(p, encoding="utf-8").read()
    n = t.count(old)
    if n:
        open(p, "w", encoding="utf-8").write(t.replace(old, new))
        print(p, n)

p = r"skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()
old_b = '''        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为从正上方垂直向下的俯视图，只看到道具顶面与轮廓，不是正面。"
        "背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"'''
new_b = '''        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），"
        "看不到正面、侧面和轮子。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"'''
assert t.count(old_b) == 1
open(p, "w", encoding="utf-8").write(t.replace(old_b, new_b))
print("script patched")
