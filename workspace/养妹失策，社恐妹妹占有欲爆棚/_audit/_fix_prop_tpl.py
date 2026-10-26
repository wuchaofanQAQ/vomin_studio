# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

old_tpl = '''道具双视角图，同一件道具：画面左侧为道具正偏侧视角，右侧为道具的俯视图。绿幕或白色背景，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。'''
new_tpl = '''道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，能看清体积与厚度；右侧为从正上方垂直向下的俯视图，只看到道具顶面与轮廓，不是正面。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。'''

rep(r"skills\drama-asset-generation\SKILL.md", [(old_tpl, new_tpl)])
rep(r"skills\drama-asset-generation\references\prompt-formats.md", [(old_tpl, new_tpl)])
rep(r"skills\drama-asset-generation\scripts\asset_prompt.py", [(old_tpl, new_tpl)])
print("templates updated")
