# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()

old1 = """    → ④ script-to-scene-assets    剧本定场景 + 小说补细节：场景清单 + 空间锚点 → 写入场景库 → 一个场景出一张图 + 一致性检查
    → ⑤ novel-to-character-assets  小说原文抽新角色档案        → 写入角色库/角色档案
    → ⑥ script-to-prompt-30   拆分镜+依赖+视频提示词     → 写入分镜表 → 触发配音+视频"""
new1 = """    → ④ script-asset-extraction   剧本+小说 → 角色/场景/道具资产（文字描述 + ≤50 字提示词 + 角色档案）→ 写资产表 → 按依赖出图 + 场景一致性检查
    → ⑤ script-to-prompt-30       拆分镜+依赖+视频提示词     → 写入分镜表 → 触发配音+视频"""
assert t.count(old1) == 1
t = t.replace(old1, new1)

old2 = "逐集阶段（novel-to-character-assets）以当前章小说原文为主要依据（剧本里的外貌/性格细节常被压缩丢失），发现新角色时产出完整 6 模块角色档案；无小说原文时退回剧本。"
new2 = "逐集阶段用当前章小说原文补长相、空间与道具细节（剧本里的外貌/性格细节常被压缩丢失），每个资产给「文字描述 + ≤50 字提示词」，新角色另产 6 模块档案；无小说原文时只用剧本，库里已有的资产直接复用。"
assert t.count(old2) == 1
t = t.replace(old2, new2)

old3 = """                 ④ script-to-scene-assets：读本集剧本（定场景）+ 本章小说原文（补空间细节）→ 场景清单/图间关联/锚点 → 场景库（已有则复用）→ 出图 → 一致性检查
                 ⑥ script-to-prompt-30（只读 当前集±1集 的完整剧本）：
                    → 分段 → 依赖场景 → 依赖角色 → 视频提示词
                    → 新增角色/场景先补 → generate 配音+视频"""
new3 = """                 ④ script-asset-extraction：读本集剧本 + 小说原文 → 角色/场景/道具清单（描述 + ≤50 字提示词 + 空间锚点 + 角色档案）→ 写资产表（已有复用）→ 按依赖出图 → 场景一致性检查
                 ⑤ script-to-prompt-30（只读 当前集±1集 的完整剧本）：
                    → 分段 → 依赖场景/角色/道具 → 视频提示词
                    → 缺资产先补 → generate 配音+视频"""
assert t.count(old3) == 1
t = t.replace(old3, new3)

old4 = """- 小说章节由你上传，**严格 1 章 = 1 集**：原文逐字存入剧本表「小说内容」，转化后的剧本存「完整剧本」，抽角色读小说原文，抽场景以剧本定场景、小说原文补空间细节，拆分镜只读转化后的剧本；若上传的是成品剧本，则直接存「完整剧本」"""
new4 = """- 小说章节由你上传，**严格 1 章 = 1 集**：原文逐字存入剧本表「小说内容」，转化后的剧本存「完整剧本」，抽资产以剧本定"有什么"、小说原文补"长什么样"，拆分镜只读转化后的剧本；若上传的是成品剧本，则直接存「完整剧本」"""
assert t.count(old4) == 1
t = t.replace(old4, new4)

open(p, "w", encoding="utf-8").write(t)
print("manual pipelines updated")
