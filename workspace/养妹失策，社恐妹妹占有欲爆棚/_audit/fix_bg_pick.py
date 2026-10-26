# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-generation\scripts\asset_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''def pick_background(desc: str) -> str:
    return "纯绿幕背景" if any(tok in desc for tok in LIGHT_TOKENS) else "纯白背景"'''
new = '''DARK_STRIP = ("深灰玻璃", "深灰", "深色", "深蓝", "黑色", "磨砂玻璃", "玻璃背板",
              "玻璃反光", "黑", "暗")


def pick_background(desc: str) -> str:
    """深色系道具即使提到「玻璃/灰」也用纯白；只有真正浅色/透明的才用绿幕。"""
    d = desc
    for w in DARK_STRIP:
        d = d.replace(w, "")
    return "纯绿幕背景" if any(tok in d for tok in LIGHT_TOKENS) else "纯白背景"'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("背景判定已修")
