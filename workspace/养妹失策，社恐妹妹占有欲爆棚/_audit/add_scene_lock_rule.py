# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
anchor = "## 官方模型规则（2.5 实测）"
add = """## 场景锁定（防穿帮）

**只要本段有镜头能看见另一个空间，就必须把那个空间的场景图一起锁进本段**，宁可多挂一张，也不要让模型自由补空间：

| 可能看见相邻空间的镜头 | 必须额外锁定 |
|---|---|
| 门内/门外过肩、开门瞬间 | 门另一侧的场景 |
| 从阳台/窗户反打室内 | 室内场景 |
| 猫眼、镜子、玻璃反射 | 被反射的空间 |
| 走廊尽头的门、楼梯口 | 门后空间 |

场景图还没出图的，先出图再写段；不能拿"文字描述"顶场景一致性。
跨空间但属于人物连续位移（从客厅走到阳台）的段，两个空间都要锁。

"""
assert t.count(anchor) == 1
t = t.replace(anchor, add + anchor)
open(p, "w", encoding="utf-8").write(t)
print("场景锁定规则已写入 skill")
