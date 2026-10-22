---
name: ai-drama-harness
description: AI 短剧全自动生产编排层。用户给飞书表格链接+上传剧本即可启动全流程。harness 通过 CLI 读写飞书数据、调度下游 skill、触发素材生成。核心纪律：聊天归聊天，写入归写入——用户在对话中提意见、讨论、否定都只产生文字草案，任何对飞书表格的写入/修改/生成动作都必须在当次列出变更清单、拿到用户明确确认后才执行。支持 Phase A（初始化全局资产）和 Phase B（逐集滚动生产）。
---

# AI Drama Harness — 全自动编排层

## Overview

短剧生产**编排层**。用户给飞书多维表格链接 + 上传剧本，harness 负责：
1. 初始化 workspace 并绑定飞书
2. 按序调度下游 skill 产出文字内容
3. 在用户确认后通过 CLI 将产出写入飞书 + 触发素材生成
4. 在 4 个关键节点暂停等待人类确认
5. 循环滚动直到全集完成

## ★ 写入授权铁律（最高优先级，覆盖一切流程描述）

**用户在聊天，不代表用户授权写入。** harness 在任何时刻都处于以下两种状态之一：

### 沟通态（默认）

用户的任何消息——提意见、补充信息、否定、"再改改""我觉得不好""这段不对"——**都只是沟通**。此时 harness 只能：

- 执行**只读**操作：`read` / `pull` / `status` / `expand`
- 调用下游 skill 产出或修改**文字草案**
- 在对话中展示草案、解释方案、回答问题

**严禁**执行任何会改变飞书数据或消耗生成额度的动作：`init`、`write`、`generate`、`push`、重试生成、状态变更。用户说一句意见就立刻改飞书，属于严重错误。

### 待确认态 → 已授权

草案准备好后，harness 必须**显式列出本次写入清单**，请求确认：

```
--- 确认点 {N}: {标题} ---
{产出摘要}

本次如确认，将执行以下动作：
  1. [write] 剧本设定 ×12 行（新增 12）
  2. [write] 角色库 ×6 行 / 角色档案 ×6 行
  3. [init] 新建飞书多维表格（仅模式 B 首次）
  （逐集：[write] 剧本表 第N集（小说章节/小说内容/完整剧本，字数…）、[write] 场景库 ×K 行）
  （生成类动作另列：[generate] 角色库：张三等 6 个角色，预估 ¥xx）

请回复：
  "确认" / "写入" / "执行" → 按清单执行
  "修改：<意见>"          → 只改草案，不写入，改完重新列清单等确认
  "重做"                 → 重新生成草案，不写入
```

授权规则：

1. **确认必须针对写入清单**：用户只对草案内容表态但没看到清单、或在讨论别的话题时的"嗯""好"，不算授权；需再次确认"是否写入飞书？"
2. **一次授权只管一次清单**：写入完成后自动回到沟通态；下一批写入必须重新列清单、重新确认。
3. **草案一改，授权作废**：用户提了修改意见后，必须重新展示完整变更清单，不能凭旧确认写入新内容。
4. **确认前必须让用户看得到要写什么**：列出表名、行数、新增/更新、关键字段摘要；生成类动作还要列出对象与预估花费。
5. **只读命令无需确认**：read/pull/status/expand 随时可执行。
6. **返工同理**：用户对已生成图片/视频要求返工，重新生成前同样要列清单确认。

> 唯一例外：用户启动时明确说"全自动/不用确认/跳过确认"，则跳过**对话确认点**（#1 #3），但飞书图片/视频审核（#2 #4）必须保留，且在启动时要向用户复述一遍"将自动写入哪些内容"作为一次性总授权。

## 启动协议

**模式 A — 接入已有飞书表格 + 上传小说章节/剧本**（推荐）：

```
飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz
小说章节 / 剧本: （上传 .txt/.md/.docx/pdf 或飞书文档）
```

harness 执行（只读初始化，不写业务数据）：

```bash
# 路径可省略，默认落到 项目根/workspace/剧名；也可显式指定
python cli.py init-from-url "https://xxx.feishu.cn/base/XxxYyyZzz" --name "重生打脸"
```

**模式 B — 只有小说章节/剧本，从零开始**：

```
小说章节 / 剧本: （上传文件）
```

模式 B **不在启动时建表**。初始化草案产出、用户在确认点 1 确认后，才执行 `init` 建表并写入（见 Phase A）。

> 只有一句话想法、没有小说或剧本：不走本流程。`drama-initializer` 只处理现成的小说/剧本；请用户先提供文件。

**两种原文的分流**：
- 上传的是**小说章节** → 走 `novel-to-script`（B0a）逐章转剧本，严格 1 章 = 1 集
- 上传的是**已写好的成品剧本** → 跳过 B0a，harness 直接按集写入剧本表的 `完整剧本`（`小说章节`/`小说内容` 留空）

**项目路径策略（两种模式统一）**：

- 每个剧本一个独立文件夹，统一放在 `C:\Users\Heart\PycharmProjects\vomin_studio\workspace\{剧名}` 下
- 向用户**推荐默认路径**；用户也可指定其他路径（在写入清单中列明实际路径）
- `init` / `init-from-url` 完成后自动向飞书「系统设置」表写入 `项目路径`、`剧名`、`创建时间`，之后凭飞书 URL 即可定位本地项目
- 启动后将实际路径设为全局变量 `WS`（默认即 `.../workspace/剧名`）

## 确认点协议（共 4 个）

| # | 标题 | Phase | 方式 | 确认后动作 |
|---|---|---|---|---|
| 1 | 剧本初始化（设定+角色档案） | A1 | 对话确认 | init（模式B）+ write 三张表 |
| 2 | 角色形象 | A2 | 飞书审核 | 三视图 generate |
| 3 | 分镜与视频提示词（逐集） | B2 | 对话确认 | 补资产 + write 分镜表 + generate |
| 4 | 视频成片（逐集） | B3 | 飞书审核 | 返工/通过，进入下一集 |

标准模板与处理逻辑见 `references/checkpoint-protocol.md`。

> 逐集的 **B0a 小说转剧本** 与 **B0b 场景抽取/新角色** 属于**轻量确认**（不计入上表 4 个正式确认点、不重新编号），但写入前同样必须列清单并拿到用户明确确认——写入授权铁律不放松。

## Phase A — 初始化（建全局资产）

### A1: 剧本初始化（drama-initializer）

1. 接收并通读用户上传的小说章节/剧本（必要时一次性追问缺失项）
2. 调用 `drama-initializer` skill，产出两段草案：**剧本设定 + 角色库/角色档案**（不产出剧本表，剧本表由 B0a 逐集产出）
3. **确认点 1: 剧本初始化** — 展示草案摘要与写入清单（三张表），对话确认
4. 用户确认后才执行：
   - 模式 B：此时才建表 + workspace（路径写入清单要列明；省略则用默认 `项目根/workspace/剧名`）：
     ```bash
     python cli.py init --name "重生打脸"
     # 或用户指定：python cli.py init "D:\my_dramas\重生打脸" --name "重生打脸"
     ```
   - init 自动写入飞书「系统设置」：项目路径 / 剧名 / 创建时间（无需单独 write）
   - 依次写入（三张表都属同一份清单，一次确认后可连续执行）：
     ```bash
     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     python cli.py write $WS --table 角色库   --data '<角色库部分>'
     python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
     ```
5. 用户提修改意见 → 只改草案，重新走确认点 1，**不写入**
### A2: 角色三视图 → 出图

1. 调用 `character-three-view-prompt` skill，为每个核心角色出三视图提示词（草案）
2. 向用户展示提示词草案与"将要写入 gen_prompt + 触发 N 个角色出图"的清单，**确认后**：
   ```bash
   python cli.py write $WS --table 角色库 --data '[{"name":"林砚","gen_prompt":"..."}]'
   python cli.py generate $WS --target 角色库:林砚
   ```
3. **确认点 2: 角色形象** — 飞书审核角色图片

Phase A 完成后，全局资产就绪：设定卡 + 角色档案（含形象图）。剧本表、场景空间设计和出图统一在 Phase B 逐集处理。

## Phase B — 逐集滚动

对每一集重复：

### B0a: 小说转剧本（novel-to-script）

每集开头第一步。把本章小说转成结构化剧本，写入剧本表。**严格 1 章 = 1 集**。

1. 读取上下文（只读，无需确认）：
   ```bash
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 角色库
   python cli.py read $WS --table 剧本表 --episode N --context 1   # 仅取前一集承接；默认不含小说原文
   ```
2. 调用 `novel-to-script` skill，产出该集剧本表一整行：`小说章节`、`小说内容`（原文逐字留存）、`完整剧本`（转化后）、集名（核心事件/出场角色/钩子/场次只在说明里给，不落表）
3. **轻量确认**（不计为正式确认点）：展示剧本全文 + 字段摘要 + 说明（【补】项、新角色、场景名归一化对照、无钩子警示），并列出写入清单（集号、章节、`小说内容`/`完整剧本` 字数、状态），确认后写入：
   ```bash
   python cli.py write $WS --table 剧本表 --data '<剧本表部分>'
   ```
4. 用户提意见 → 只改剧本草案并重新列清单，**不写入**
5. 存量数据（`migrate-schema` 迁移后状态为「待转剧本」的行）同样从 B0a 开始处理

### B0b: 场景抽取 + 新角色（script-to-scene-assets + novel-to-character-assets）

B0a 写入剧本表之后、拆分镜之前运行。**逐集增量**：库里已有的空间与母版直接复用，只为新空间/新局部补图。

1. 读取上下文（只读，无需确认）：
   ```bash
   python cli.py read $WS --table 剧本表 --episode N --context 1   # N±1 的 script（不带小说原文，仅用于跨集空间延续）
   python cli.py read $WS --table 剧本表 --episode N --with-novel   # 仅当前集：小说原文，供场景/角色补细节（不与 --context 同用）
   python cli.py read $WS --table 剧本设定                          # 画风 / 画幅
   python cli.py read $WS --table 场景库                            # 已有空间、母版、主图、局部
   python cli.py read $WS --table 角色库
   ```
2. 调用 `script-to-scene-assets` skill（剧本定场景清单，当前集小说原文补空间细节），产出：场景清单、图间关联表、空间锚点表、场景图提示词包（母版 → 主场景 → 局部/闪回/外景）、复用清单
3. 调用 `novel-to-character-assets` skill（只读当前集小说原文：`python cli.py read $WS --table 剧本表 --episode N --with-novel`，不加 `--context`；`小说内容` 为空则退回剧本），产出：新角色识别 + 完整 6 模块角色档案（不在角色库中的角色）
4. **轻量确认**（不计为正式确认点）：展示场景资产三表 + 新角色列表，并列出写入清单，确认后写入文字资产（不出图）：
   ```bash
   python cli.py write $WS --table 场景库 --data '<场景库部分>'     # name + view_angle + description + gen_prompt + ref_scenes + relation_note
   python cli.py write $WS --table 角色库 --data '<new_characters.角色库>'
   python cli.py write $WS --table 角色档案 --data '<new_characters.角色档案>'
   ```
5. 场景图**懒加载出图**：待 B1 确定本集 `dependencies` 后，只为本集用到的场景 `generate`（花预算，清单须列对象与预估花费）。同一空间多行时 CLI 自动按 母版 → 主场景 → 局部 → 其他 顺序出图；出图后须过 `script-to-scene-assets` 的**一致性检查**，硬指标不过不得进入视频生成

### B1: 分镜 + 依赖解析 + 视频提示词（director-segment-prompt 一体完成）

1. 读取上下文（只读，无需确认）。设当前集为 N，**剧本表只读 N-1、N、N+1 共 3 集，严禁全量读入，严禁加 `--with-novel`**：
   ```bash
   python cli.py read $WS --table 剧本表 --episode N --context 1
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 角色库
   python cli.py read $WS --table 角色档案
   python cli.py read $WS --table 场景库    # 此时已有 B0b 产出的 description
   ```
   - 前 1 集：承接钩子、人物进场状态与情绪起点；后 1 集：本集要埋的钩子与离场状态
   - 目的：把握本集角色心境、场景布局、人物调度；全量读剧本或带入小说原文会导致上下文膨胀、输出变差
2. 调用 `director-segment-prompt` skill，只对当前集 N 产出：
   - **按段拆分**：每段 6~30 秒、一段 = 一次生成任务 = 剧本分镜表一行，段 ID 为 `ep{两位集号}_p{两位段序}`（如 `ep10_p05`）；段内多个带精确时间码的镜头与对白
   - **场景依赖清单**（空间名，需要局部时带 `view`；裸名取主场景，**母版不挂分镜**）+ 角色依赖清单
   - 每段导演级提示词：开头【参考素材锚点】块用 `{角色库：…} 图N：【资产名】，身份` / `{场景库：…} 图N：【资产名】，时空` 逐行声明（需要动作衔接时加 `{剧本分镜表：上一段ID} 视频N：…`），这是整段唯一允许出现 `{}` 的地方；正文统一用【资产名】
3. **草案沟通**：用户提意见 → 只改草案，不写飞书
4. **场景差分比对**：harness 拿 `dependencies.scenes` + `dependencies.new_scenes` 逐条检查场景库：
   - 逐个「空间名 + 视角」检查场景库中是否已有该行且场景图就绪、一致性检查已通过
   - 已有且素材就绪 → 复用
   - 缺失的场景/视角 → 汇总为**待补场景清单**，交 `script-to-scene-assets` 补出（母版 → 主场景 → 局部，派生图须先有母版），逐步生成确认
   - 新增角色 → 走角色档案 + 三视图补生成
   - **补资产期间分镜草案不变**，锚点块里的 `{场景库：…}` 引用在素材就绪后才能 expand；未出图的资产只进"待补资产"，不进锚点块
5. **确认点 3: 分镜与提示词** — 列入库清单（全部资产就绪后）：
   - 交付前先跑机器校验，错误必须为 0：
     ```bash
     python skills/director-segment-prompt/scripts/check_storyboard.py workspace/{剧名}/drafts/ep01_storyboard.md
     ```
   - `write --table 剧本分镜表` 写入分镜（一段一行，`prompt` 为完整段文本）
   - `expand --shot <id>` 可预览锚点映射与素材清单，确认锚点块外无残留 `{}`、素材齐全
   - ★ **成片时长与配音**：`generate` 按分镜行 `timeline`（如 `00:00-00:20`）的真实秒数出片，上限 30 秒，解析不出才回退 `ark.default_duration`；成本按实际秒数估算，清单里列出各段秒数。配音按 `dialogue` 每行「角色：台词」逐句、从**角色档案**取音色（`voice_desc`）合成，档案缺该角色或音色会警告并用默认音色——写分镜前先确认对白角色都有角色档案且填了音色
   - 确认后才执行（**先跑资产闸门，不过不许调模型**）：
     ```bash
     python cli.py preflight $WS --episode N    # 生产态资产复检，0 问题才继续
     python cli.py generate $WS --tts-only
     python cli.py generate $WS
     python cli.py push $WS
     ```
   - 分镜可以先在**预览态**写入评审：`preflight` 未过也能写、能 `expand` 试跑，但审计第 3 项记 `PENDING（预览）`、不得写 `PASS`；只有 preflight 全过、进入生产态后才写 `18 项硬审计：PASS`

### B2: 视频成片审核 → 下一集

1. **确认点 4: 视频成片** — 飞书审核
2. 用户回复"继续"后：
   ```bash
   python cli.py pull $WS
   ```
3. 检查"返工"状态分镜；**返工重新生成前必须再次列清单确认**
4. 全部"通过"后进入下一集（回到 B1）

## 编排的下游 Skill

| Skill | Phase | 职责 |
|---|---|---|
| `drama-initializer` | A1 | 上传小说/剧本 → 剧本设定 + 角色档案 |
| `character-three-view-prompt` | A2 | 角色 → 三视图出图提示词 |
| `novel-to-script` | B0a | 小说章节 → 剧本表（小说章节/小说内容/完整剧本，1 章 = 1 集） |
| `script-to-scene-assets` | B0b | 剧本 → 场景清单/图间关联/空间锚点/场景图提示词（母版→主场景→局部）+ 一致性检查 |
| `novel-to-character-assets` | B0b | 小说原文 → 逐集新角色识别 + 完整 6 模块档案 |
| `director-segment-prompt` | B1 | 剧本 → 分段分镜 + 依赖解析 + 导演级视频提示词 |

## References

- `references/checkpoint-protocol.md` — 4 个确认点标准流程 + 写入授权状态机
- `references/pipeline.md` — 完整编排流程图 + 场景两段式调度规则
- `references/data-contracts.md` — 各 skill 数据交接格式与字段约定
- `references/cli-commands.md` — CLI 命令速查表（标注只读 / 需确认）
