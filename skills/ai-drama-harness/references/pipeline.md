# 完整编排流程 + 节点依赖/产出/CLI 集成

> 所有写入动作（init/write/generate/push）都必须在对应确认点获得用户明确确认后执行，只读动作（read/pull/expand/status）随时可执行。详见 `checkpoint-protocol.md`。

## 一、节点总览

| 节点 | Skill | 前置输入 | 产出 | CLI 读 | CLI 写（确认后） |
|---|---|---|---|---|---|
| ① | drama-initializer | 用户上传剧本 | 剧本设定 + 剧集 + 角色库/角色档案 | — | `init`（模式B）+ `write` 剧本设定/剧集表/角色库/角色档案 |
| ② | character-three-view-prompt | 角色档案+画风 | 三视图出图提示词 | `read --table 角色库` | `write --table 角色库`（gen_prompt）+ `generate` |
| ③ | drama-episode-analyzer（逐集 B0） | 当前集±1集剧本+场景库+角色库 | 场景空间设计(description)+新角色(含完整档案) | `read --table 剧集表/剧本设定/场景库/角色库` | `write --table 场景库`(description) + `write --table 角色库/角色档案`(新角色) |
| ④ | storyboard-prompt（逐集 B1） | 当前集±1集剧本+角色+场景（含 description） | 分镜 + 依赖清单 + 视频提示词 | `read --table 剧集表 --episode N --context 1` + 角色库/角色档案/场景库/剧本设定 | `write --table 剧本分镜表` + `generate` |
| ⑤ | scene-image-prompt（B1 补缺） | 待补场景清单+场景库 description | 场景空镜提示词 | `read --table 剧本设定/场景库` | `write --table 场景库` + `generate` |

## 二、节点间依赖

```
上传剧本
  └→ ① drama-initializer ──(确认点1)──→ 剧本设定 / 剧集表 / 角色库 / 角色档案
                 │
                 ├→ ② character-three-view-prompt（角色三视图）→ generate 出图 ──(确认点2·飞书)
                 │
                 └→ 逐集滚动（Phase B）：
                       ③ drama-episode-analyzer（B0 逐集预分析）
                         读 剧集表 N±1 + 场景库 + 角色库
                         → 产出场景空间设计(description) + 识别新角色(含完整8模块档案)
                         → [轻量确认] → write 场景库 description + 新角色进角色库/角色档案
                       ④ storyboard-prompt（B1 分镜+依赖+提示词）
                         读 剧集表 N±1（禁止全量读）+ 角色库/角色档案 + 场景库(含 description)
                         → 拆分镜 / 依赖场景（含视角需求）/ 依赖角色 / 视频提示词
                         → harness 差分比对场景库：缺失的场景·视角 → 调⑤补生成
                         → 比对角色库：新增角色先补②
                       ⑤ scene-image-prompt（B1 补缺场景/视角）
                         读 场景库 description → 组装提示词 → generate 出图
                       → (确认点3) write 分镜表 → generate 配音+视频 → push
                       → (确认点4·飞书) 审核 → 下一集
```

**关键设计**：
- 剧本由用户上传，初始化即包含**逐集完整原文**（剧集表），不再需要"从大纲写分集剧本"环节。
- 拆分镜与视频提示词由 `storyboard-prompt` 一个技能一次完成，不再分两步。
- 角色档案在初始化时已产出初版；逐集分析（③ analyzer）如发现新角色，直接产出完整 8 模块档案。
- **Phase A 不再提前出场景**。所有场景的空间设计（④ analyzer）和出图（⑥ scene-image-prompt）统一在 Phase B 按需处理，避免鸡生蛋依赖。
- **依赖链无循环**：analyzer(剧本→description+新角色档案) → storyboard(分镜+视角需求) → harness 差分 → scene-image-prompt(description→提示词)。

## 三、Phase A — 初始化流程（含 CLI）

```
A1: 上传剧本 → drama-initializer 产出草案
    → [确认点1] 用户确认（清单含项目路径：默认 项目根/workspace/剧名，或用户指定）
    → 模式B：init 建表（模式A已绑定）；init 自动写系统设置（项目路径/剧名/创建时间）
    → write 剧本设定 / 剧集表 / 角色库 / 角色档案
A2: ② character-three-view-prompt 产出提示词草案
    → （确认）write 角色库(gen_prompt) → generate --target 角色库:X → [确认点2·飞书]
```

Phase A 完成后进入逐集 Phase B，场景空间设计和出图统一在 B0/B1 按需处理。

## 四、Phase B — 逐集流程（含 CLI）

```
对每一集 N：
  B0: ③ drama-episode-analyzer（逐集预分析）
    read 剧集表 --episode N --context 1 + 剧本设定 + 场景库 + 角色库
    → 产出场景空间设计(description) + 新角色识别(含完整 8 模块档案)
    → [轻量确认] → write 场景库 description + 新角色进角色库/角色档案
  B1: ④ storyboard-prompt（分镜+依赖+提示词）
    read 剧集表 --episode N --context 1   # 只读 N-1、N、N+1 三集，禁止全量读
    read 剧本设定 + 角色库 + 角色档案 + 场景库（此时已有 description）
    → 产出分镜+依赖（含场景视角需求）+提示词草案
    → 与用户沟通修改（不写入）
    → harness 差分比对场景库：
         逐条检查 dependencies.scenes/new_scenes 中每个 name·view
         缺失的 → 汇总为待补场景清单，交 scene-image-prompt 逐步出图
         （scene-image-prompt 从场景库 description 读取空间设计，直接组装提示词）
    → 比对角色库：新增角色 → 补角色档案 + 三视图
  → [确认点3] 全部资产就绪后列入库清单：
       write 剧本分镜表
       expand --shot 预览锚定与素材
       generate --tts-only → generate → push
  → [确认点4·飞书] 审核视频
  → pull 检查返工（返工重生成需再次确认）→ 下一集
```

## 五、场景调度：analyzer 产出空间设计 → storyboard 定义视角需求 → harness 差分 → scene-image-prompt 执行

**空间设计权在 drama-episode-analyzer（B0）**：分析剧本原文，为场景产出结构化空间设计（description），写入场景库。

**需求定义权在 storyboard-prompt（B1）**：拆分镜时确定每个场景需要哪些视角。

**执行权在 scene-image-prompt（B1 补缺）**：从场景库读取 description，直接组装 `<SPACE MAP>` 段，产出提示词。

**Phase B · 按需差分补生成（逐集滚动）**
- B0: ③ drama-episode-analyzer 为该集场景产出空间设计（已有 description 的场景跳过），为新角色产出完整档案
- B1: storyboard-prompt 产出场景依赖清单（含每个场景的视角需求列表）
- harness 逐条差分比对场景库：
  - 已有 name·view 且素材就绪 → 复用
  - 缺失 → 交 scene-image-prompt 补生成（description 已就绪；正视图优先，后续视角引用正视图作母版）
- 提示词中的 `{场景库：…}` 只是文字占位引用，不要求素材此刻存在；真正解析到图片文件是 `expand` / `generate` 时
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
- ①必须先于②③④⑤；③必须先于④⑤（description 是 scene-image-prompt 的前提）；④⑤逐集滚动，依赖资产必须先就绪
