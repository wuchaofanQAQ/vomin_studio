# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()

reps = [
("2. 调用 `drama-segment-generation` skill（剧本转提示词 3.0），只对当前集 N 产出：",
 "2. 调用 `drama-segment-generation` skill（剧本转提示词 4.2），只对当前集 N 产出："),
("   - **场景依赖清单**（场景名）+ 角色依赖清单 + 资产编号表（`drafts/asset_ids.json`）",
 "   - **资产绑定表**：本集角色/场景/道具逐条对三张表（有图/无图/库里没有→待补），登记 `drafts/asset_ids.json`\n   - **场景依赖清单**（场景名）+ 角色依赖清单 + 道具依赖清单 + 待补清单"),
("   - 每段按 3.0 骨架写：`【第NN段｜00:00-本段时长｜标题】` → `【资产锁定】`（场景/角色/道具/特效分行，条目写成 `【R01｜沈幼怡：{角色库：沈幼怡}】`，角色/场景必须带锚点）→ `【本段风格】` → `【本段初始空间基准】` → 逐镜融合式段落 → 台词行 `【对白 00:01-00:02】R01沈幼怡（…地说）：……`",
 "   - 每段按 4.2 骨架写：`【第NN段｜00:00-本段时长｜场景·事件】` → `【本段资产锁定】`（场景/角色/群像/道具/动物/载具/特效分行，条目 `【R01｜沈幼怡：{角色库：沈幼怡}】`，场景/角色必须带锚点；库里没有的写 `待补：【P02｜名：待补，未读取】`）→ `【本段现场生成】`（可选）→ `【本段整体基准】` → `【本段初始空间】` → 逐镜融合式段落 → 台词行 `【对白 00:01-00:02】R01沈幼怡（…地说）：『……』` → `【本段终态】`"),
("   python cli.py read $WS --table 场景库    # 此时已有 B0b 产出的 description\n   python cli.py read $WS --table 剧本分镜表 --episode N   # 重写时避免在旧段上叠写",
 "   python cli.py read $WS --table 场景库    # 此时已有 B0b 产出的 description\n   python cli.py read $WS --table 道具库    # 道具绑定用\n   python cli.py read $WS --table 剧本分镜表 --episode N   # 重写时避免在旧段上叠写"),
]
for old, new in reps:
    c = t.count(old)
    print(c, old[:40])
    if c == 1:
        t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("harness patched")
