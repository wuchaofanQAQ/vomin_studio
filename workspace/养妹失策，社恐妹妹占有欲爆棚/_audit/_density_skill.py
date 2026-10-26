# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

anchor = "## 镜头写法速查"
section = """## 写法密度（硬指标，吸收自参考稿）

写的不是字数，是**可执行信息**：位置、比例、材质、受力、切点。低于下表直接退回重写。

| 块 | 最低字数 | 必含 |
|---|---|---|
| 【本段整体基准】 | **≥150** | 技术规格 + 光色 + 主体保持 + 尺度 + 剪辑执行 + 速度/接触反馈 + 声音层次 + 重建声明 |
| 【本段现场生成】 | **≥60**（确实没有写「无」） | 形制、材质、物理规则、与主体的关系 |
| 【本段初始空间】 | **≥90** | 世界轴 + 各主体位置/朝向 + 历史状态 + 开镜机位 |
| 单镜正文 | **≥70** | 硬切起 + 前景/中景/后景 + 动作链 + 接触 + 切点 |
| 【本段终态】 | **≥40** | 姿态/持握/承力/残留/朝向清单 |

九条规律、整体基准配方、单薄↔密度对照见 `references/prompt-density.md`。

"""
assert t.count(anchor) == 1
t = t.replace(anchor, section + anchor)

old_row = "| `references/seedance-25-rules.md` |"
new_row = "| `references/prompt-density.md` | 写法密度：九条规律、字数基线、整体基准配方、单薄↔密度对照 | 每段动笔前 |\n| `references/seedance-25-rules.md` |"
assert t.count(old_row) == 1
t = t.replace(old_row, new_row)
open(p, "w", encoding="utf-8").write(t)
print("skill density section added")
