# 完整编排流程 + 节点依赖/产出/CLI 集成

> 所有写入动作（init/write/generate/push）都必须在对应确认点获得用户明确确认后执行，只读动作（read/pull/expand/status）随时可执行。详见 `checkpoint-protocol.md`。

## 一、节点总览

| 节点 | Skill | 前置输入 | 产出 | CLI 读 | CLI 写（确认后） |
|---|---|---|---|---|---|
| ① | drama-initializer | 用户上传剧本 | 剧本设定 + 剧集 + 角色库/角色档案 | — | `init`（模式B）+ `write` 剧本设定/剧集表/角色库/角色档案 |
| ② | character-bible-extractor（可选） | 角色档案初版 | 深化后的角色档案 | `read --table 剧本设定/角色档案` | `write --table 角色库/角色档案` |
| ③ | character-three-view-prompt | 角色档案+画风 | 三视图出图提示词 | `read --table 角色库` | `write --table 角色库`（gen_prompt）+ `generate` |
| ④ | scene-image-prompt | 场次列表+画风 | 场景空镜提示词 | `read --table 剧本设定/剧集表` | `write --table 场景库` + `generate` |
| ⑤ | storyboard-prompt（逐集） | 当前集±1集剧本+角色+场景 | 分镜 + 依赖清单 + 视频提示词 | `read --table 剧集表 --episode N --context 1` + 角色库/角色档案/场景库/剧本设定 | `write --table 剧本分镜表` + `generate` |

## 二、节点间依赖

```
上传剧本
  └→ ① drama-initializer ──(确认点1)──→ 剧本设定 / 剧集表 / 角色库 / 角色档案
                 │
                 ├→ ③ character-three-view-prompt（角色三视图）→ generate 出图 ──(确认点2·飞书)
                 │
                 ├→ ④ scene-image-prompt（核心场景空镜）→ generate 出图 ────────(确认点3·飞书)
                 │
                 └→ ⑤ 逐集 storyboard-prompt：
                       读 剧集表（仅 当前集±1集，共3集，禁止全量读）
                       → 据前集钩子/本集原文/后集铺垫把握心境、场景布局、人物调度
                       → 拆分镜 / 依赖场景 / 依赖角色 / 视频提示词
                       → 比对资产库，新增角色/场景先补③④
                       → (确认点4) write 分镜表 → generate 配音+视频 → push
                       → (确认点5·飞书) 审核 → 下一集
```

**关键变化**：
- 剧本由用户上传，初始化即包含**逐集完整原文**（剧集表），不再需要"从大纲写分集剧本"环节。
- 拆分镜与视频提示词由 `storyboard-prompt` 一个技能一次完成，不再分两步。
- 角色档案在初始化时已产出初版，②为可选深化。

## 三、Phase A — 初始化流程（含 CLI）

```
A1: 上传剧本 → drama-initializer 产出草案
    → [确认点1] 用户确认（清单含项目路径：默认 项目根/workspace/剧名，或用户指定）
    → 模式B：init 建表（模式A已绑定）；init 自动写系统设置（项目路径/剧名/创建时间）
    → write 剧本设定 / 剧集表 / 角色库 / 角色档案
A2: character-three-view-prompt 产出提示词草案
    → （确认）write 角色库(gen_prompt) → generate --target 角色库:X → [确认点2·飞书]
A3: scene-image-prompt 产出提示词草案
    → （确认）write 场景库 → generate --target 场景库:X → [确认点3·飞书]
```

## 四、Phase B — 逐集流程（含 CLI）

```
对每一集 N：
  read 剧集表 --episode N --context 1   # 只读 N-1、N、N+1 三集，禁止全量读
  read 剧本设定 + 角色库 + 角色档案 + 场景库
  → storyboard-prompt 产出分镜+依赖+提示词草案
  → 与用户沟通修改（不写入）
  → [确认点4] 列入库清单：
       新增资产 → 补场景/角色提示词并出图（同样需确认）
       write 剧本分镜表
       expand --shot 预览锚定与素材
       generate --tts-only → generate → push
  → [确认点5·飞书] 审核视频
  → pull 检查返工（返工重生成需再次确认）→ 下一集
```

## 五、场景两段式调度

**Phase A · 核心场景（提前定调）**
- 从剧集表场次列表中识别全剧贯穿场景，批量出 5~8 张，作全剧画风基准

**Phase B · 剧情场景（滚动补生成）**
- 每集 storyboard-prompt 产出场景依赖清单，比对场景库：新增→补，已有→复用
- 初始化时已做过场景名称归一化，同景同名直接复用

## 六、harness 维护的清单

角色库、场景库、剧集表即清单，通过飞书表格实时维护：
- `python cli.py read $WS --table 角色库` — 角色及素材状态
- `python cli.py read $WS --table 场景库` — 场景及素材状态
- `python cli.py read $WS --table 剧集表` — 仅用于总览；**拆分镜严禁全量读**，必须 `--episode N --context 1` 只取 3 集
- `python cli.py expand $WS --shot ep01_s01` — 预览某镜头提示词锚定了哪些素材

## 七、编排注意

- 下游 skill 产出文字草案 + 结构化 JSON；**展示并确认后** harness 才通过 CLI `write` 写入
- 出图/出视频通过 `generate` 触发；generate 花预算，每次都要在确认清单中列明对象与预估花费
- 用户跳过某环节 → harness 按需裁剪，不强制全流程，但跳过的写入动作同样要用户点头
- ①必须先于③④⑤；③④可并行；⑤逐集滚动，依赖资产必须先就绪
