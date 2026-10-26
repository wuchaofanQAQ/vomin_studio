# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

old = """| 文件 | 内容 | 何时读 |
|---|---|---|
| `references/mother-prompt-42.md` | 4.2 母版原文（权威顺序/资产调用/先建空间/可见性/时间/动作/冲击/群战/特效/巨物/关键帧/唯美/正向表达/自检） | 每次任务开始 |
| `references/shot-craft.md` | 镜头工艺：坐标系、可见集合、状态重建、受力链、特效阶段、文戏/动作强度、台词与音效 | 写任何镜头前 |
| `references/project-adaptation.md` | 与本项目 CLI/飞书/音色的对接、资产绑定、编号登记、字段映射、写入与生成 | 解析依赖、交付、写入时 |
| `references/self-check.md` | 两轮自检清单 + 常见失败对照 | 交付前 |
| `scripts/check_segment_prompt.py` | 机器校验：结构/时间轴/编号/锚点/待补/裸名/台词/语速/停点/字数 | 交付前必跑 |"""
new = """| 文件 | 内容 | 何时读 |
|---|---|---|
| `references/mother-prompt-42.md` | 4.2 母版原文（权威顺序/资产调用/先建空间/可见性/时间/动作/冲击/群战/特效/巨物/关键帧/唯美/正向表达/自检） | 每次任务开始 |
| `references/core-principles.md` | 24 条核心执行原则（权威顺序、资产、分段、时间、写法、自检、交付） | 每次任务开始 |
| `references/cinema-foundation.md` | 影视基础：导演意图卡、景别、角度、运镜安全等级、组接、调度、光、色、节奏 | 设计镜头前 |
| `references/shot-grammar.md` | 单镜句式、景别/机位/运镜词库、段长与镜头数分配、短剧节奏 | 写镜头时 |
| `references/camera-space-and-visibility.md` | 先建空间、屏幕坐标系、可见边界、切镜重建、景别精度、运镜起落幅、文戏镜头语言 | 写任何镜头前 |
| `references/shot-richness-and-pitfalls.md` | 六个「写厚」点、七个自相矛盾坑、改写对照、改进顺序 | 镜头太干或自检时 |
| `references/physics-and-scale.md` | 情绪物理化、先后因果、惯性滞后、0.2 秒爆发、短震与尺度量化 | 动作/特效镜头 |
| `references/action-impact-vfx-crowd.md` | 题材强度、受力—环境—摄影机反馈链、武戏、撞击、群战、特效、巨物、关键帧、唯美 | 打斗/群像/特效段 |
| `references/dialogue-and-audio.md` | 台词行、时间码、语速、长句拆分、画外声、内心独白、声桥、屏幕文字 | 写台词与声音 |
| `references/continuity-and-anchoring.md` | 同一性锚定、版本区分、终态=下一段初态、左右轴、光风一致、群体数量、跨段尺度 | 写段首尾 |
| `references/seedance-25-rules.md` | Seedance 2.5 执行规则：情绪→物理、全身动力学链、环境动态、光与表面、四层画面、反规则、篇幅 | 每次写段 |
| `references/director-self-review.md` | 导演级 16 项逐镜自检与改写 | 每段写完 |
| `references/iteration-manual.md` | 迭代修复手册：常见问题修复表、成功经验、写作前确认 | 返工时 |
| `references/preflight-checklist.md` | 交付前 A~F 分组自查清单 | 交付前 |
| `references/shot-craft.md` | 镜头工艺速查：坐标系、可见集合、状态重建、受力链、特效阶段、文戏/动作强度、台词与音效 | 写任何镜头前 |
| `references/project-adaptation.md` | 与本项目 CLI/飞书/音色的对接、资产绑定、编号登记、字段映射、写入与生成 | 解析依赖、交付、写入时 |
| `references/self-check.md` | 两轮自检清单 + 常见失败对照 | 交付前 |
| `scripts/check_segment_prompt.py` | 机器校验：结构/时间轴/编号/锚点/待补/裸名/台词/语速/停点/字数 | 交付前必跑 |

> 以上 13 篇工艺参考吸收自旧 `docs/director-segment-prompt`，已按 4.2 改写；**格式、分段、资产绑定、交付流程一律以本 SKILL.md 为准**，工艺参考只解决「怎么写好」。"""
assert t.count(old) == 1
t = t.replace(old, new)

old2 = "- 母版是《剧本转提示词 4.2》：`references/mother-prompt-42.md`（原文，冲突时以它为准）。"
new2 = "- 母版是《剧本转提示词 4.2》：`references/mother-prompt-42.md`（原文，冲突时以它为准）。\n- 旧 `docs/director-segment-prompt` 的工艺细节已吸收进 `references/`（13 篇），与 4.2 冲突处一律按 4.2。"
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("SKILL references updated")
