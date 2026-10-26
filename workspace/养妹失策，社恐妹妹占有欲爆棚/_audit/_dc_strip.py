# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()
i = t.index("## 3. 逐集资产提取 · 角色")
j = t.index("## 4b. 逐集资产提取 · 道具")
new = '''## 3. 逐集资产提取 · 角色（script-asset-extraction → 角色库）

**Phase B · B0b**：`script-asset-extraction` 一次抽出本集的角色/场景/道具。本节是角色部分——读 `剧本表.script`，用当前集 `novel_text` 补长相（为空只用剧本）。逐集增量，库里已有的同名角色复用。

只写角色库一行（描述），不写角色档案、不写音色、不写提示词。

| JSON key | 飞书字段 | 说明 |
|---|---|---|
| `name` | 角色ID / 角色名 | 与人名逐字一致 |
| `char_type` | 角色类型 | 核心 / 重要配角 / 配角 / 龙套 / 群像 |
| `appearance` | 外貌描述 | 一句，≤50 字，只写看得见的 |
| （不产） | 生成提示词 | 留空；出图时用 `appearance` + 全局画风自动拼 |

```json
{
  "characters": [
    {"name": "陈诚", "status": "新建", "char_type": "核心",
     "appearance": "18岁清瘦男生，黑色微卷中长发，白T黑短裤"}
  ],
  "reused": [{"type": "角色", "name": "沈幼怡", "reason": "角色库已有形象图"}]
}
```

规则：

- **只写描述（≤50 字）**，不写提示词、不写空间锚点、不写角色档案/音色；由 `check_assets.py` 卡死。
- 复用项不重写描述。
- 同一人不同年龄/形态（`陈诚` / `陈诚 12岁`）拆成两个资产。
- 群像单列一行，`char_type=群像`，描述写人数、服色、队形。
- 配音如需固定音色，仍在 `角色档案` 里维护（初始化阶段已产出的不受影响）；本 skill 不再写档案。

## 4. 逐集资产提取 · 场景（script-asset-extraction → 场景库）

**Phase B · B0b 的场景部分**：剧本定场景清单，当前集小说原文补空间细节（为空只用剧本）。

**match key**：`场景ID`（= 场景名），**一个场景一行一张图**。

### 场景库字段

| JSON key | 飞书字段 | 说明 |
|---|---|---|
| `name` | 场景ID（主键） | **场景名**；**不得含 `·`**；光影变体用全角括号，如 `出租屋（夜）` |
| `description` | 场景描述 | 一句，≤50 字：空间/材质/光线/无人 |
| （不产） | 生成提示词 | 留空；出图时用 `description` + 全局画风自动拼 |
| `ref_scenes` | 参考场景 | 生成该图时参考的其他场景名 |
| `relation_note` | 作用关联 | 作用 / 与其它场景共享哪些物件 |
| `related_episodes` | 关联集数 | 如 `1,3` |
| `gen_status` | 出图状态 | `待出图` / `生成中` / `已出图` / `需重抽` / `已通过` |
| `consistency` | 一致性检查 | `未检查` / `通过` / `不通过`；**不通过不得进入分镜生成** |
| `source` | 来源 | `AIGC生成` 等 |
| `ref_image` | 文件路径 | 出图后由 `generate` 回填 |

### 场景引用语法

- `{场景库：出租屋（夜）}` → 直接命中该场景那一张图
- 不支持 `·母版` / `·主场景` / `·局部` 后缀
- 场景图与描述冲突时，以图为准

### 输出 JSON

```json
{
  "scenes": [
    {
      "name": "出租屋（夜）", "status": "新建",
      "description": "夜间出租屋，水泥墙浅灰木地板，南窗冷光，无人",
      "relation_note": "第1集场1、场3 挂参考",
      "related_episodes": "1,3"
    }
  ],
  "reused": [{"type": "场景", "name": "写字楼大堂", "reason": "已有场景图，复用"}]
}
```

### harness 动作（每步均需用户确认）

1. 写入场景库文字资产（不出图）：`write --table 场景库 --data '<场景库部分>'`
2. 出图（花预算，清单须列对象与预估花费）：`generate --target 场景库:出租屋（夜）`
3. **一致性检查**（出图后门禁）：入口/开门方向、地面材质与分界、功能区与门窗方位、光源方向、色调，逐图比对；任一不通过先修场景图，**不得进入视频生成**。详见 `script-asset-extraction/references/scene-consistency.md`
4. 出图时机：懒加载——B1 产出 `dependencies` 后，只为本集用到的场景出图

'''
t = t[:i] + new + t[j:]
open(p, "w", encoding="utf-8").write(t)
print("data-contracts 3/4 rewritten")
