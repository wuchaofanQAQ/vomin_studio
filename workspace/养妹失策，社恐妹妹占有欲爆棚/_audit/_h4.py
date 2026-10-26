# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()
old = '''4. **场景差分比对**：harness 拿 `dependencies.scenes` + `dependencies.new_scenes` 逐条检查场景库：
   - 逐个场景名检查场景库中是否已有该行且场景图就绪、一致性检查已通过
   - 已有且素材就绪 → 复用
   - 缺失的场景 → 汇总为**待补场景清单**，交 `drama-asset-extraction` 补描述与提示词（一个场景一张图），逐步生成确认
   - 新增角色 → 走 `drama-asset-generation` 补四视角设定图
   - 新增道具 → 差分比对 `道具库`；缺的列入待补道具（手工补录或 `generate --target 道具库:名`），不阻塞分镜评审
   - **补资产期间分镜草案不变**，资产锁定里的 `{场景库：…}` 引用在素材就绪后才能 expand；未出图的资产只进"待补资产"，不进锁定区'''
new = '''4. **资产差分比对**：harness 拿 `dependencies`（scenes / characters / props / missing / pending_images）逐条检查三张资产表：
   - 表里有行、有图 → 复用，可绑锚点、占图号
   - 表里有行、没图 → 可绑描述（锚点照写、不占图号），列入**待出图**，交 `drama-asset-generation` 按版式补图
   - 表里没有 → 进 `missing`，锁定区写 `待补：【编号｜名：待补，未读取】`，不写锚点
   - **补资产期间分镜草案不变**；`preflight` 会把待补/缺图列为问题，不过闸不许调模型'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("harness step4 updated")
