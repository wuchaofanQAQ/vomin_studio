# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\references\prompt-density.md"
t = open(p, encoding="utf-8").read()
anchor = "## "
add = '''## 单镜四层（每镜缺一不可，正文 ≥150 字）

一条合格的镜头正文，至少四层信息：

| 层 | 写什么 | 示例 |
|---|---|---|
| **光位** | 主光从哪来、明暗比、有没有反光/逆光 | 「夕阳从画右斜切进来，他半边脸压在暗部」 |
| **表演** | 动作怎么发力 + 表情/呼吸/视线的变化 | 「指节先发白，随后整只手下意识收紧」 |
| **层次** | 前景 / 中景 / 后景分别有什么，虚实关系 | 「前景是虚化的窗帘边，中景是他的侧脸，后景是过曝的天」 |
| **运动与切点** | 固定还是微推/手持，起幅落幅，切在哪一帧 | 「固定机位微推半寸，切在他眼皮落下的瞬间」 |

低于 150 字的镜头基本只写了动作，模型只能自由发挥，成片会"空"。

'''
if "## 单镜四层" not in t:
    i = t.index(anchor)
    t = t[:i] + add + t[i:]
    open(p, "w", encoding="utf-8").write(t)
    print("density 已加四层规则")
