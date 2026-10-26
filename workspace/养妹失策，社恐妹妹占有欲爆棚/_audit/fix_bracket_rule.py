# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        for nm in sorted(names, key=len, reverse=True):
            if nm in masked:
                errors.append(f"{tag} 正文出现裸资产名「{nm}」，应写【{nm}】")
                masked = masked.replace(nm, "§")'''
new = '''        for nm in sorted(names, key=len, reverse=True):
            if nm in masked:
                # 【】只用于「引用锁定的那张参考图」；泛指同类物件（自己的手机/桌上的杯子）不该加【】
                notes.append(f"{tag} 正文提到「{nm}」但没加【】（若指锁定资产应写【{nm}】）")
                masked = masked.replace(nm, "§")'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("裸名改为提示")

# 文档口径
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
g = open(p2, encoding="utf-8").read()
if "【】的用法" not in g:
    anchor = "## 屏幕文字规则（手机/微信/打字）"
    add = '''## 【】的用法（容易写错）

`【】` 只表示**引用本段锁定的那张参考图**：

- 角色名一律带：`【陈诚】`、`【沈幼怡】`
- 道具/场景**只有指锁定资产时**才带：`【手机】`＝沈幼怡那部顶配苹果
- 泛指同类物件**不带**：`陈诚掏出自己的手机`、`桌上的杯子`、`路边的车`——它们不是那张参考图

写错会污染参考图绑定：把陈诚的旧手机写成 `【手机】`，模型会拿沈幼怡那部顶配机的参考图去生成他的手机。

'''
    g = g.replace(anchor, add + anchor)
    open(p2, "w", encoding="utf-8").write(g)
    print("SKILL 已加【】用法")
