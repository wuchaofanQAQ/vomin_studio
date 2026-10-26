# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

anchor = "## 镜头写法速查"
add = """## 交付前自检（人工项，脚本替代不了）

**脚本只覆盖机械项**（结构/时间/资产锚点/台词引号与语速/密度/景别与切点词/可见性关键词）。下面 8 条必须人工逐镜过，任何一条没做就等于没自检：

1. **可见性三分**：每镜在心里列「可见集 / 可听集 / 画外因果集」，正文里每个名字、物件、身体部位都要在可见集里；画外只写方向（画左/画右/画外上/画外下），**不写画外人物的名字**。
2. **轴线一致**：同一段内同一人物的目线方向要一致；「别开视线」要写明往哪边躲，不能和对方所在方向撞上。
3. **机位反算**：这个景别 + 角度 + 遮挡，能不能同时拍到写的全部内容？不能就拆镜。
4. **过肩**：确实有后肩/耳侧/后脑进画才写「过肩」，否则写「干净反打」。
5. **景别精度**：远景不写表情与手指，特写不写三层空间。
6. **起幅/落幅**：镜内有运动时，写清哪些元素是后来才入画的，不能写成从头可见。
7. **一镜一动作**：动作分句数 ÷ 秒数，超过约 3 就拆镜或加时长。
8. **台词只出现一次**：台词后再复述一遍最容易诱出字幕。

自检结论要逐条报「过了 / 改了什么」，不能只报「校验 0 错」。

"""
assert t.count(anchor) == 1
t = t.replace(anchor, add + anchor)
open(p, "w", encoding="utf-8").write(t)
print("SKILL checklist added")

# 校验器通过后打印人工清单提醒
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t2 = open(p2, encoding="utf-8").read()
old = '''    print(f"  ✓ 参考图 {refs}")
    return 0 if ok else 1'''
new = '''    print(f"  ✓ 参考图 {refs}")
    print("  · 人工项仍需逐条过：可见性三分 / 轴线一致 / 机位反算 / 过肩虚实 / 景别精度 / 起幅落幅 / 一镜一动作 / 台词只出现一次")
    return 0 if ok else 1'''
assert t2.count(old) == 1
open(p2, "w", encoding="utf-8").write(t2.replace(old, new))
print("checker reminder added")
