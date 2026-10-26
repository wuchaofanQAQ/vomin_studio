# -*- coding: utf-8 -*-
p = r"skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()

old_tpl = '''    "道具": (
        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），"
        "看不到正面、侧面和轮子。背景为纯绿幕或纯白，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"
    ),'''
new_tpl = '''    "道具": (
        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为俯视图：镜头在道具正上方垂直向下，画面里只有它的顶面（提手与顶盖），"
        "看不到正面、侧面和轮子。背景为{bg}，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}"
    ),'''
assert t.count(old_tpl) == 1
t = t.replace(old_tpl, new_tpl)

old_build = '''def build(kind: str, desc: str) -> str:
    return TEMPLATES[kind].format(desc=desc.strip())'''
new_build = '''# 浅色道具词表：命中则用纯绿幕，否则纯白（白底会把浅色道具吃掉）
LIGHT_TOKENS = ("白色", "米白", "奶白", "乳白", "象牙", "浅色", "浅灰", "浅蓝", "浅粉",
                "浅黄", "浅绿", "银", "透明", "玻璃", "雪白", "淡", "发光")


def pick_background(desc: str) -> str:
    return "纯绿幕背景" if any(tok in desc for tok in LIGHT_TOKENS) else "纯白背景"


def build(kind: str, desc: str) -> str:
    desc = desc.strip()
    if kind == "道具":
        return TEMPLATES["道具"].format(desc=desc, bg=pick_background(desc))
    return TEMPLATES[kind].format(desc=desc)'''
assert t.count(old_build) == 1
t = t.replace(old_build, new_build)

old_check = '''    for m in CHECKS[kind]["markers"]:
        if m not in prompt:
            errs.append(f"{who} 提示词缺版式要素「{m}」")
    if kind == "道具" and not ("绿幕" in prompt or "白色背景" in prompt):
        errs.append(f"{who} 道具提示词缺「绿幕或白色背景」")'''
new_check = '''    for m in CHECKS[kind]["markers"]:
        if m not in prompt:
            errs.append(f"{who} 提示词缺版式要素「{m}」")
    if kind == "道具":
        has_green = "纯绿幕背景" in prompt
        has_white = "纯白背景" in prompt
        if has_green and has_white:
            errs.append(f"{who} 背景只能二选一，提示词里同时出现绿幕和白底")
        elif not has_green and not has_white:
            errs.append(f"{who} 道具提示词缺「纯绿幕背景」或「纯白背景」")
        else:
            want = pick_background(desc)
            if (want == "纯绿幕背景") != has_green:
                errs.append(f"{who} 背景选错：浅色道具必须纯绿幕，其余用纯白（当前应为{want}）")'''
assert t.count(old_check) == 1
t = t.replace(old_check, new_check)

open(p, "w", encoding="utf-8").write(t)
print("script updated")
