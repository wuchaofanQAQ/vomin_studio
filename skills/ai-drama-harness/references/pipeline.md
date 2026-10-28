# 完整编排流程 + 节点依赖/产出/CLI 集成

> 所有写入动作（init/write/generate/push）都必须在对应确认点获得用户明确确认后执行，只读动作（read/pull/expand/status）随时可执行。详见 `checkpoint-protocol.md`。

## 一、节点总览

| 节点 | Skill | 前置输入 | 产出 | CLI 读 | CLI 写（确认后） |
|---|---|---|---|---|---|
| ① | drama-initializer | 用户上传小说章节/剧本 | 剧本设定 + 资产库/角色档案（**不含剧本表**） | — | `init`（模式B）+ `write` 剧本设定/资产库/角色档案 |
| ② | drama-asset-generation | 资产库描述+画风 | 角色四视角提示词 + 出图（可选，主角用） | `read --table 资产库` | `write --table 资产库`（gen_prompt）+ `generate` |
| ③ | novel-to-drama（逐集 B0a） | 阅读窗口（可多章）+ 剧本设定 + 资产库 + 前一集 script | 剧本表一行：集号 / 集名 / 对应原小说章节 / 初版剧本（含原文区间） / 状态 | `read --table 剧本设定/资产库`、`read --table 剧本表 --episode N --context 1`、`read --table 小说表 --chapter <阅读窗口>` | `write --table 剧本表` |
| ④ | drama-asset-extraction（逐集 B0b） | 当前集±1集 script + 当前集原文（`小说表 --chapter`）+ 剧本设定 + 资产库 | 角色/场景/道具资产：一句 ≤50 字描述 + 复用/待补清单 | `read --table 剧本表 --episode N --context 1` + `read --table 小说表 --chapter <对应原小说章节>` + 三张资产表 | `write --table 资产库` + `generate`（懒加载） |
| ⑤ | drama-segment-generation（逐集 B1） | 当前集±1集 script + 角色 + 场景（含 description 锚点）+ 道具 | 分镜 + 依赖清单 + 视频提示词；**懒加载：只为本集用到的资产生图** | `read --table 剧本表 --episode N --context 1` + 资产库/角色档案/资产库/资产库/剧本设定 | `write --table 剧本分镜表` + `generate` |

> 剧本表不含小说原文；原文在 `小说表`，用 `read --table 小说表 --chapter <对应原小说章节>` 精确取，**禁止通读全本**。

## 二、节点间依赖

```
上传小说章节 / 剧本
  └→ ① drama-initializer ──(确认点1)──→ 剧本设定 / 资产库 / 角色档案
                 │
                 ├→ ② drama-asset-generation（主角四视角设定图，可选）→ generate ──(确认点2·飞书)
                 │
                 └→ 逐集滚动（Phase B）：
                       ③ novel-to-drama（B0a 小说转剧本；集与章不绑定）
                         读 剧本设定 + 资产库 + 前一集 script
                         → 结构化剧本（场头：场号/内外景/地点/时间/出场人物/关键动作）
                         → [轻量确认] → write 剧本表
                       ④ drama-asset-extraction（B0b 资产提取）
                         读 剧本表 N±1 script + 本集所用章节原文 + 剧本设定 + 四张资产表
                         → 角色（描述+≤50字提示词+档案）/ 场景（描述+锚点+提示词）/ 道具
                         → 逐集增量：同名同图复用，只补新资产
                         → [轻量确认] → write 资产库/角色档案/资产库/资产库（只写文字，不出图）
                       ⑤ drama-segment-generation（B1 分镜+依赖+提示词）
                         读 剧本表 N±1 script（禁止全量、禁止带原文）+ 资产库/档案 + 资产库(含锚点) + 资产库
                         → 分段 / 依赖场景 / 依赖角色 / 依赖道具 / 视频提示词
                         → harness 差分：缺失资产 → 回 ④ 补；已有未出图 → 出图 + 场景过一致性检查
                       → (确认点3) write 分镜表 → generate 出片 → push
                       → (确认点4·飞书) 审核 → 下一集
```

**关键设计**：

- 小说转剧本是独立一层：小说章节逐字存在 `小说表`（`章节` / `标题` / `内容`，下游按 `对应原小说章节` 精确取）；`初版剧本` 存转化后的剧本，是资产提取与分镜的**唯一剧本来源**。
- 用户上传**成品剧本**时跳过 ③，直接写入 `初版剧本`，`对应原小说章节` 留空。
- 角色、场景、道具由 ④ 一个技能统一提取，**每个资产一行一张图**，只产一句 ≤50 字描述。
- 拆分镜与视频提示词由 `drama-segment-generation` 一个技能完成。
- **懒加载**：④ 只写文字资产，不出图；⑤ 产出 `dependencies` 后，才为本集用到的资产生成。
- **依赖链无循环**：novel-to-drama(小说→script) → drama-asset-extraction(script→资产) → drama-segment-generation(分镜+依赖) → harness 差分 → 出图 + 场景一致性检查。

## 三、Phase A — 初始化流程（含 CLI）

```
A1: 上传小说章节/剧本 → drama-initializer 产出草案（剧本设定 + 资产库/角色档案）
    → [确认点1] 用户确认（清单含项目路径：默认 项目根/workspace/剧名，或用户指定）
    → 模式B：init 建表（模式A已绑定）；init 自动写系统设置（项目路径/剧名/创建时间）
    → write 剧本设定 / 资产库 / 角色档案
A2: ② drama-asset-generation 产出角色提示词草案（可选）
    → （确认）write 资产库(gen_prompt) → generate --target 资产库:X → [确认点2·飞书]
```

Phase A 完成后进入逐集 Phase B，剧本、资产提取和出图统一在 B0a/B0b/B1 逐集处理。

## 四、Phase B — 逐集流程（含 CLI）

```
对每一集 N：
  B0a: ③ novel-to-drama（小说转剧本）
    read 剧本设定 + 资产库 + 剧本表 --episode N --context 1（取前一集承接，剧本表不含原文）
    read 小说表 --chapter <阅读窗口，默认往后 2~3 章；不够再扩>
    → 在窗口里定本集原文区间（起始句 → 结束句），再回填章号
    → 转化为剧本，抬头写 原文区间；提取集名
    → [轻量确认] → write 剧本表（集名/对应原小说章节/初版剧本/…，status=草稿）
    # 重做第 N 集：旧 对应原小说章节 不是范围；按新要求重读窗口，写完更新 原文区间 / 对应原小说章节
  B0b: ④ drama-asset-extraction（资产提取）
    read 剧本表 --episode N --context 1
    read 小说表 --chapter <对应原小说章节>
    read 剧本设定 + 资产库 + 资产库 + 资产库
    → 角色/场景/道具清单：一句描述 + 复用判定
    → 新角色补 6 模块档案
    → check_assets.py 校验（0 错）
    → [轻量确认] → write 资产库/角色档案/资产库/资产库（只写文字，不出图）
  B1: ⑤ drama-segment-generation（分镜+依赖+提示词）
    read 剧本表 --episode N --context 1   # 只读 N-1、N、N+1 三集，禁止全量读；禁止通读小说表（原文按 --chapter 精确取）
    read 剧本设定 + 资产库 + 角色档案 + 资产库 + 资产库
    → 分段（按场景 description 的锚点/轴线设计站位与调度）+ 依赖场景/角色/道具 + 提示词草案
    → 与用户沟通修改（不写入）
    → harness 差分资产：
         缺失的 → 回 ④ 补描述与提示词 → 出图
         已有未出图的 → generate → 场景过一致性检查
  → [确认点3] 全部资产就绪（含场景一致性检查通过）后列入库清单：
       write 剧本分镜表
       expand --shot 预览锚定与素材
       generate → push
  → [确认点4·飞书] 审核视频
  → pull 检查返工（返工重生成需再次确认）→ 下一集
```

## 五、资产调度：剧本 → 资产提取 → 分镜依赖 → 差分 → 出图

**剧本来源权在 novel-to-drama（B0a）**：把小说转为带结构化场头的剧本，写入 `初版剧本`；场景名在此阶段归一化。

**资产定义权在 drama-asset-extraction（B0b）**：按「空间连通性 + 光影时刻」拆场景（一场景一图），按出现/剧情功能/一致性需求挑角色与道具；每个资产给一句 ≤50 字描述（不写提示词、锚点、档案）。逐集增量：同名同图复用。

**调用权在 drama-segment-generation（B1）**：依据场景描述设计站位与调度，产出本集 `dependencies`（scenes / characters / props），作为懒加载依据。

**出图与门禁**：本集依赖清单中的资产由 harness 触发 `generate`。场景图出完过 `drama-asset-extraction/references/scene-consistency.md` 的一致性检查（入口/开门方向、地面材质与分界、功能区与门窗方位、光源方向、色调、跨场景共享物件），**硬指标不过不得进入视频生成**。

**Phase B · 懒加载差分**

- B0a：novel-to-drama 产出本集剧本
- B0b：drama-asset-extraction 产出新资产（已有的复用）
- B1：drama-segment-generation 产出依赖清单
- harness 逐条差分：
  - 已有资产、图就绪、一致性通过 → 复用
  - 缺失 → 回 ④ 补文字资产 → 出图
  - 已有未出图 → `generate` → 场景过一致性检查
- 提示词里的 `{资产库：名}` / `{资产库：名}` / `{资产库：名}` 是文字占位引用，`expand`/`generate` 时才解析成图片文件

## 六、harness 维护的清单

资产库、剧本表即清单，通过飞书表格实时维护：

- `python cli.py read $WS --table 资产库` — 角色及素材状态
- `python cli.py read $WS --table 资产库` — 场景及素材状态（一个场景一行一张图）
- `python cli.py read $WS --table 资产库` — 关键道具及素材状态
- `python cli.py read $WS --table 剧本表` — 仅用于总览；**拆分镜/抽资产严禁全量读**，必须 `--episode N --context 1` 只取 3 集
- `python cli.py expand $WS --shot ep01_p01` — 预览某段提示词锚定了哪些素材

存量飞书表迁移（剧集表→剧本表、补字段、补缺失标准表）：`python cli.py migrate-schema $WS --dry-run` 查看计划，确认后再执行。

## 七、编排注意

- 下游 skill 产出文字草案 + 结构化 JSON；**展示并确认后** harness 才通过 CLI `write` 写入
- 出图/出视频通过 `generate` 触发；generate 花预算，每次都要在确认清单中列明对象与预估花费
- 用户跳过某环节 → harness 按需裁剪，不强制全流程，但跳过的写入动作同样要用户点头
- ①必须先于②③④⑤；③必须先于④⑤（`初版剧本` 是资产提取与分镜的前提）；④必须先于⑤（资产描述与锚点是分镜的前提）；⑤逐集滚动，依赖资产必须先就绪
