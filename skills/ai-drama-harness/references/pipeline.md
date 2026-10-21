# 完整编排流程 + 节点依赖/产出/CLI 集成

> 所有写入动作（init/write/generate/push）都必须在对应确认点获得用户明确确认后执行，只读动作（read/pull/expand/status）随时可执行。详见 `checkpoint-protocol.md`。

## 一、节点总览

| 节点 | Skill | 前置输入 | 产出 | CLI 读 | CLI 写（确认后） |
|---|---|---|---|---|---|
| ① | drama-initializer | 用户上传小说章节/剧本 | 剧本设定 + 角色库/角色档案（**不含剧本表**） | — | `init`（模式B）+ `write` 剧本设定/角色库/角色档案 |
| ② | character-three-view-prompt | 角色档案+画风 | 三视图出图提示词 | `read --table 角色库` | `write --table 角色库`（gen_prompt）+ `generate` |
| ③ | novel-to-script（逐集 B0a） | 本章小说 + 剧本设定 + 角色库 + 前一集 script | 剧本表一整行：小说章节 / 小说内容（原文）/ 完整剧本（转化后）/ 集名 / 状态 | `read --table 剧本设定/角色库`、`read --table 剧本表 --episode N --context 1` | `write --table 剧本表` |
| ④ | script-to-scene-assets（逐集 B0b） | 当前集±1集 script + 当前集小说原文（`--with-novel`，补空间细节）+ 剧本设定 + 场景库 | 场景清单 + 图间关联表 + 空间锚点表 + 场景图提示词包（母版→主场景→局部/闪回/外景）；**只建文字资产**；出图后过一致性检查 | `read --table 剧本表 --episode N --context 1` + `--episode N --with-novel` + `剧本设定/场景库` | `write --table 场景库` + `generate`（懒加载） |
| ⑤ | novel-to-character-assets（逐集 B0b） | 当前集小说原文（`--with-novel`，仅 N 集；无原文退回 script）+ 角色库 | 新角色识别 + 完整 8 模块档案 | `read --table 剧本表 --episode N --with-novel` + `剧本设定/角色库` | `write --table 角色库/角色档案`（新角色） |
| ⑥ | director-segment-prompt（逐集 B1） | 当前集±1集 script + 角色 + 场景（含 description） | 分镜 + 依赖清单 + 视频提示词；**懒加载：只为本集用到的场景出图** | `read --table 剧本表 --episode N --context 1` + 角色库/角色档案/场景库/剧本设定 | `write --table 剧本分镜表 + `generate` |

> `read --table 剧本表` 默认**剔除小说内容**（`novel_text`）；除 ③ 在需要对照原文时可加 `--with-novel` 外，其余节点一律不带。

## 二、节点间依赖

```
上传小说章节 / 剧本
  └→ ① drama-initializer ──(确认点1)──→ 剧本设定 / 角色库 / 角色档案
                 │
                 ├→ ② character-three-view-prompt（角色三视图）→ generate 出图 ──(确认点2·飞书)
                 │
                 └→ 逐集滚动（Phase B）：
                       ③ novel-to-script（B0a 小说转剧本，1 章 = 1 集）
                         读 剧本设定 + 角色库 + 前一集 script
                         → 转化为结构化剧本（场头：场号/内外景/地点/时间/出场人物/关键动作）+ 提取其余字段
                         → [轻量确认] → write 剧本表（小说章节/小说内容/完整剧本…）
                       ④ script-to-scene-assets（B0b 场景抽取）  ⑤ novel-to-character-assets（B0b 新角色）
                         读 剧本表 N±1 的 script + 剧本设定 + 场景库 + 角色库
                         ④ → 空间拆分（连通性+光影）→ 场景清单/图间关联/锚点 → 母版/主场景/局部提示词；已有则复用
                         ⑤ → 新角色识别 + 完整 8 模块档案
                         → [轻量确认] → write 场景库（只建文字资产，不出图）+ 新角色进角色库/角色档案
                       ⑥ director-segment-prompt（B1 分镜+依赖+提示词）
                         读 剧本表 N±1 的 script（禁止全量读，禁止带小说原文）+ 角色库/角色档案 + 场景库(含 description)
                         → 分段 / 依赖场景 / 依赖角色 / 视频提示词（按场景 description 设计站位/调度）
                         → harness 差分比对场景库：缺失/缺视角 → 调④补出；已有未出图 → 出图并过一致性检查
                         → 比对角色库：新增角色先补②
                       → (确认点3) write 分镜表 → generate 配音+视频 → push
                       → (确认点4·飞书) 审核 → 下一集
```

**关键设计**：
- 小说转剧本是独立一层：`小说内容` 存原文（逐字，不改，下游不读），`完整剧本` 存转化后的剧本，是场景抽取与分镜的**唯一剧本来源**。
- 用户上传**成品剧本**时跳过 ③，直接写入 `完整剧本`，`小说章节`/`小说内容` 留空。
- 拆分镜与视频提示词由 `director-segment-prompt` 一个技能一次完成，不再分两步。
- 角色档案在初始化时已产出初版；逐集阶段（⑤）如发现新角色，直接产出完整 8 模块档案。
- **场景分层 + 懒加载**：场景由 ④ 先文字设计（母版→主场景→局部，description + gen_prompt），B1 产出 `dependencies` 后，只为本集用到的场景出图。**Phase A 不再提前出场景**。
- **依赖链无循环**：novel-to-script(小说→script) → script-to-scene-assets(script→场景资产) → director-segment-prompt(分镜+依赖清单) → harness 差分 → 出图 + 一致性检查。

## 三、Phase A — 初始化流程（含 CLI）

```
A1: 上传小说章节/剧本 → drama-initializer 产出草案（剧本设定 + 角色库/角色档案）
    → [确认点1] 用户确认（清单含项目路径：默认 项目根/workspace/剧名，或用户指定）
    → 模式B：init 建表（模式A已绑定）；init 自动写系统设置（项目路径/剧名/创建时间）
    → write 剧本设定 / 角色库 / 角色档案
A2: ② character-three-view-prompt 产出提示词草案
    → （确认）write 角色库(gen_prompt) → generate --target 角色库:X → [确认点2·飞书]
```

Phase A 完成后进入逐集 Phase B，剧本表、场景空间设计和出图统一在 B0a/B0b/B1 逐集处理。

## 四、Phase B — 逐集流程（含 CLI）

```
对每一集 N：
  B0a: ③ novel-to-script（小说转剧本）
    read 剧本设定 + 角色库 + 剧本表 --episode N --context 1（取前一集承接，不含小说原文）
    → 转化为结构化剧本，提取集名（核心事件/出场角色/钩子/场次只在说明里给，不落表）
    → [轻量确认] → write 剧本表（小说章节/小说内容/完整剧本/…，status=草稿）
  B0b: ④ script-to-scene-assets + ⑤ novel-to-character-assets
    read 剧本表 --episode N --context 1 + 剧本设定 + 场景库 + 角色库
    → ④ 场景清单/图间关联/锚点/提示词包（已有空间与母版复用，只补新空间/新局部）
    → ⑤ 新角色识别（含完整 8 模块档案）
    → [轻量确认] → write 场景库（只建文字资产，不出图）+ 新角色进角色库/角色档案
  B1: ⑥ director-segment-prompt（分镜+依赖+提示词）
    read 剧本表 --episode N --context 1   # 只读 N-1、N、N+1 三集，禁止全量读，禁止 --with-novel
    read 剧本设定 + 角色库 + 角色档案 + 场景库（此时已有 description）
    → 分段（按场景 description 的画面分层/主轴/锚点设计站位与调度）+ 依赖场景 + 依赖角色 + 提示词草案
    → 与用户沟通修改（不写入）
    → harness 差分比对场景库：
         逐条检查 dependencies.scenes/new_scenes 中每个「空间名+视角」是否已存在、场景图是否已生成、一致性检查是否通过
         缺失/缺视角的 → 汇总为待补场景清单，交 script-to-scene-assets 补出
         已有未出图的 → generate（母版→主场景→局部自动排序）→ 一致性检查
    → 比对角色库：新增角色 → 补角色档案 + 三视图
  → [确认点3] 全部资产就绪（含场景一致性检查通过）后列入库清单：
       write 剧本分镜表
       expand --shot 预览锚定与素材
       generate --tts-only → generate → push
  → [确认点4·飞书] 审核视频
  → pull 检查返工（返工重生成需再次确认）→ 下一集
```

## 五、场景调度：novel-to-script 产剧本 → script-to-scene-assets 建场景文字资产 → director-segment-prompt 依赖清单 → harness 差分 → 出图 + 一致性检查

**剧本来源权在 novel-to-script（B0a）**：把小说转为带结构化场头的剧本，写入剧本表 `完整剧本`；场景名在此阶段归一化。

**空间设计权在 script-to-scene-assets（B0b）**：按「空间连通性 + 光影时刻」拆分空间，先总后分——母版 → 主场景 → 局部（闪回/外景独立）；产出图间关联（派生/咬合/共享锚点/独立）与空间锚点；写入场景库 `description`、`gen_prompt`、`ref_scenes`、`relation_note`，不出图。逐集增量：库里已有的空间/母版/主图直接复用。

**调用权在 director-segment-prompt（B1）**：依据各场景 `description` 设计镜头站位/人物调度，产出本集场景依赖清单（懒加载依据）。**母版不挂分镜**。

**出图与门禁**：本集依赖清单中的场景由 harness 触发 `generate`。同一空间多行自动按 母版 → 主场景 → 局部 → 其他 顺序出图（派生图的参考图句 `{场景库：名·母版}` 需要母版已有图）。出图后过 script-to-scene-assets 的一致性检查（入口/开门方向、地面材质与分界、功能区与门窗方位、光源方向、色调），**硬指标不过不得进入视频生成**。

**Phase B · 懒加载·按需差分补生成（逐集滚动）**
- B0a: novel-to-script 产出本集剧本（写入剧本表）
- B0b: script-to-scene-assets 为该集新空间/新局部产出场景文字资产（已有的复用）；novel-to-character-assets 为新角色产出完整档案
- B1: director-segment-prompt 产出场景依赖清单，并给出本集用到的场景依赖清单
- harness 逐条差分比对场景库：
  - 已有场景、场景图就绪、一致性检查通过 → 复用
  - 缺失 / 缺视角 → 交 script-to-scene-assets 补出
  - 已有未出图 → generate 后过一致性检查
- 提示词中的 `{场景库：…}` 只是文字占位引用：裸名默认解析为该空间的**主场景**，`名·局部·部位` 取局部，存量 `全景基准图（默认）` 行可回退命中；真正解析到图片文件是 `expand` / `generate` 时
- 场景名在 novel-to-script 阶段已归一化，同景同名直接复用；场景名不含 `·`，光影变体用全角括号（`出租屋（夜）`）

## 六、harness 维护的清单

角色库、场景库、剧本表即清单，通过飞书表格实时维护：
- `python cli.py read $WS --table 角色库` — 角色及素材状态
- `python cli.py read $WS --table 场景库` — 场景及素材状态（同一空间多行：母版/主场景/局部…）
- `python cli.py read $WS --table 剧本表` — 仅用于总览（默认不含小说原文）；**拆分镜/抽场景严禁全量读**，必须 `--episode N --context 1` 只取 3 集
- `python cli.py expand $WS --shot ep01_p01` — 预览某段提示词锚定了哪些素材

存量飞书表迁移（剧集表→剧本表、补字段）：`python cli.py migrate-schema $WS --dry-run` 查看计划，确认后再执行。

## 七、编排注意

- 下游 skill 产出文字草案 + 结构化 JSON；**展示并确认后** harness 才通过 CLI `write` 写入
- 出图/出视频通过 `generate` 触发；generate 花预算，每次都要在确认清单中列明对象与预估花费
- 用户跳过某环节 → harness 按需裁剪，不强制全流程，但跳过的写入动作同样要用户点头
- ①必须先于②③④⑤⑥；③必须先于④⑤⑥（`完整剧本` 是场景抽取与分镜的前提）；④必须先于⑥（description 是分镜站位设计的前提）；⑥逐集滚动，依赖资产必须先就绪
