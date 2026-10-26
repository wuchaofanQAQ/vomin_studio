# -*- coding: utf-8 -*-
p = r"skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace(
 "看不到正面、侧面和轮子。背景为{bg}，画面内无任何文字。电影级写实质感，保留道具的真实材质与使用痕迹。\\n道具：{desc}",
 "看不到正面、侧面和轮子。背景为{bg}，画面内无任何文字。电影级写实质感，{wear}。\\n道具：{desc}")

old = '''def pick_background(desc: str) -> str:
    return "纯绿幕背景" if any(tok in desc for tok in LIGHT_TOKENS) else "纯白背景"'''
new = '''WEAR_RE = re.compile(r"(?<!无)(?<!没有)(磨损|划痕|旧|破|锈|脏|陈旧|裂|掉漆|褪色)")


def pick_background(desc: str) -> str:
    return "纯绿幕背景" if any(tok in desc for tok in LIGHT_TOKENS) else "纯白背景"


def pick_wear(desc: str) -> str:
    """描述里写了磨损/旧化才保留痕迹，否则默认光洁无划痕。"""
    if WEAR_RE.search(desc):
        return "保留描述中的使用痕迹与磨损"
    return "表面光洁，无划痕、无破损，材质细节清晰"'''
assert t.count(old) == 1
t = t.replace(old, new)

old_build = '''    if kind == "道具":
        return TEMPLATES["道具"].format(desc=desc, bg=pick_background(desc))'''
new_build = '''    if kind == "道具":
        return TEMPLATES["道具"].format(desc=desc, bg=pick_background(desc), wear=pick_wear(desc))'''
assert t.count(old_build) == 1
t = t.replace(old_build, new_build)

if "import re" not in t.split("TEMPLATES")[0]:
    t = t.replace("import argparse\nimport json", "import argparse\nimport json\nimport re")

open(p, "w", encoding="utf-8").write(t)
print("wear clause added")
