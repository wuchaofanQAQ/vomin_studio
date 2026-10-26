# -*- coding: utf-8 -*-
import re

# 1) drama-asset-generation：补 类型→模板 规格表
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
anchor = "## "
add = '''## 按资产类型出图（唯一分叉点）

同一张「资产库」，靠 **类型** 区分出图要求：

| 类型 | 版式 | 画面比例 | 模板来源 |
|---|---|---|---|
| 角色 | 四视角设定图：近景正/侧 + 全身正/背 | 16:9 | `asset_prompt.py --type 角色` |
| 场景 | 场景资料图（空间 + 光影） | 22:9 | `--type 场景` |
| 道具 | 双视角图：正偏侧 + 正面 | 16:9 | `--type 道具` |

提示词由「描述 + 模板」自动拼，不进表；出图后只回填 `文件路径`。

'''
if "## 按资产类型出图" not in t:
    i = t.index(anchor)
    t = t[:i] + add + t[i:]
    open(p, "w", encoding="utf-8").write(t)
    print("asset-generation 已加类型表")

# 2) cli.py 帮助文本
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p2, encoding="utf-8").read()
c = c.replace("角色库/场景库/道具库/剧本设定/剧本分镜", "资产库/剧本设定/剧本分镜")
c = c.replace("角色库/场景库/剧本设定/剧本分镜表/剧本表/生图工作台/素材库", "资产库/剧本设定/剧本分镜表/剧本表/生图工作台/素材库")
c = c.replace("支持: 角色库 / 场景库 / 道具库 / 剧本分镜表 / 生图工作台", "支持: 资产库 / 剧本分镜表 / 生图工作台")
open(p2, "w", encoding="utf-8").write(c)
print("cli 帮助文本已更新")
print("残留 角色库/场景库/道具库 in cli.py:", c.count("角色库"), c.count("场景库"), c.count("道具库"))
