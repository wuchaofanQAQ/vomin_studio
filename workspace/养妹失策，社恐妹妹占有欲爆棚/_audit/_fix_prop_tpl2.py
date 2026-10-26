# -*- coding: utf-8 -*-
old_tpl = "道具双视角图，同一件道具：画面左侧为道具正偏侧视角，右侧为道具的俯视图。绿幕或白色背景，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。"
new_tpl = "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，能看清体积与厚度；右侧为从正上方垂直向下的俯视图，只看到道具顶面与轮廓，不是正面。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。"

p = r"skills\drama-asset-generation\references\prompt-formats.md"
t = open(p, encoding="utf-8").read()
n = t.count(old_tpl)
t = t.replace(old_tpl, new_tpl)
open(p, "w", encoding="utf-8").write(t)
print("prompt-formats:", n)

p = r"skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()
old_block = '''    "道具": (
        "道具双视角图，同一件道具：画面左侧为道具正偏侧视角，右侧为道具的俯视图。"
        "绿幕或白色背景，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"
    ),'''
new_block = '''    "道具": (
        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为从正上方垂直向下的俯视图，只看到道具顶面与轮廓，不是正面。"
        "背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"
    ),'''
print("script count:", t.count(old_block))
assert t.count(old_block) == 1
open(p, "w", encoding="utf-8").write(t.replace(old_block, new_block))
print("done")
