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
  2. [write] 资产库 ×6 行
  3. [init] 新建飞书多维表格（仅模式 B 首次）
  （逐集：[write] 剧本表 第N集（小说章节/小说内容/完整剧本，字数…）、[write] 资产库 ×K 行）
  （生成类动作另列：[generate] 资产库：张三等 6 个角色，预估 ¥xx）

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
- 上传的是**小说章节** → 走 `novel-to-drama`（B0a）逐章转剧本，严格 1 章 = 1 集
- 上传的是**已写好的成品剧本** → 跳过 B0a，harness 直接按集写入剧本表的 `完整剧本`（`小说章节`/`小说内容` 留空）

**项目路径策略（两种模式统一）**：

- 每个剧本一个独立文件夹，统一放在 `C:\Users\Heart\PycharmProjects\vomin_studio\workspace\{剧名}` 下
- 向用户**推荐默认路径**；用户也可指定其他路径（在写入清单中列明实际路径）
- `init` / `init-from-url` 完成后自动向飞书「系统设置」表写入 `项目路径`、`剧名`、`创建时间`，之后凭飞书 URL 即可定位本地项目
- 启动后将实际路径设为全局变量 `WS`（默认即 `.../workspace/剧名`）

## 确认点协议（共 4 个）

| # | 标题 | Phase | 方式 | 确认后动作 |
|---|---|---|---|---|
| 2 | 角色形象 | A2 | 飞书审核 | 四视角 generate |
| 3 | 分镜与视频提示词（逐集） | B2 | 对话确认 | 补资产 + write 分镜表 + generate |
| 4 | 视频成片（逐集） | B3 | 飞书审核 | 返工/通过，进入下一集 |

标准模板与处理逻辑见 `references/checkpoint-protocol.md`。

> 逐集的 **B0a 小说转剧本** 与 **B0b 场景抽取/新角色** 属于**轻量确认**（不计入上表 4 个正式确认点、不重新编号），但写入前同样必须列清单并拿到用户明确确认——写入授权铁律不放松。

## Phase A — 初始化（建全局资产）

### A1: 剧本初始化（drama-initializer）

1. 接收并通读用户上传的小说章节/剧本（必要时一次性追问缺失项）
2. 调用 `drama-initializer` skill，产出两段草案：**剧本设定 + 资产库**（不产出剧本表，剧本表由 B0a 逐集产出）
3. **确认点 1: 剧本初始化** — 展示草案摘要与写入清单（两张表），对话确认
4. 用户确认后才执行：
   - 模式 B：此时才建表 + workspace（路径写入清单要列明；省略则用默认 `项目根/workspace/剧名`）：
     ```bash
     python cli.py init --name "重生打脸"
     # 或用户指定：python cli.py init "D:\my_dramas\重生打脸" --name "重生打脸"
     ```
   - init 自动写入飞书「系统设置」：项目路径 / 剧名 / 创建时间（无需单独 write）
   - 依次写入（两张表都属同一份清单，一次确认后可连续执行）：
     ```bash
     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     python cli.py write $WS --table 资产库   --data '[{"name":"陈诚","kind":"角色","description":"..."}, ...]'
     ```
5. 用户提修改意见 → 只改草案，重新走确认点 1，**不写入**
### A2: 角色资产图 → 出图

1. 调用 `drama-asset-generation` skill，按角色描述生成四视角设定图（提示词由 描述 + 模板自动拼，不写进表）
2. 向用户展示"将要写出图清单 + 触发 N 个角色出图"的清单，**确认后**：
   ```bash
   python cli.py write $WS --table 资产库 --data '[{"name":"林砚","kind":"角色","description":"..."}]'
   python cli.py generate $WS --target 资产库:林砚   # 类型=角色 → 自动走四视角模板
   ```
3. **确认点 2: 角色形象** — 飞书审核角色图片

Phase A 完成后，全局资产就绪：设定卡 + 资产库（含形象图）。剧本表、场景空间设计和出图统一在 Phase B 逐集处理。

## Phase B — 逐集滚动

对每一集重复：

### B0a: 小说转剧本（novel-to-drama）

每集开头第一步。把本章小说转成结构化剧本，写入剧本表。**严格 1 章 = 1 集**。

1. 读取上下文（只读，无需确认）：
   ```bash
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 资产库
   python cli.py read $WS --table 剧本表 --episode N --context 1   # 仅取前一集承接；默认不含小说原文
   ```
2. 调用 `novel-to-drama` skill，产出该集剧本表一整行：`小说章节`、`小说内容`（原文逐字留存）、`完整剧本`（转化后）、集名（核心事件/出场角色/钩子/场次只在说明里给，不落表）
3. **轻量确认**（不计为正式确认点）：展示剧本全文 + 字段摘要 + 说明（【补】项、新角色、场景名归一化对照、无钩子警示），并列出写入清单（集号、章节、`小说内容`/`完整剧本` 字数、状态），确认后写入：
   ```bash
   python cli.py write $WS --table 剧本表 --data '<剧本表部分>'
   ```
4. 用户提意见 → 只改剧本草案并重新列清单，**不写入**
5. 存量数据（`migrate-schema` 迁移后状态为「待转剧本」的行）同样从 B0a 开始处理

### B0b: 资产提取（drama-asset-extraction 一体完成）

B0a 写入剧本表之后、拆分镜之前运行。**逐集增量**：库里已有的资产直接复用，只为新资产补一句描述；一个资产 = 一行 = 一张图。

1. 读取上下文（只读，无需确认）：
   ```bash
   python cli.py read $WS --table 剧本表 --episode N --context 1   # N±1 的 script（不带小说原文，仅用于跨集延续）
   python cli.py read $WS --table 小说表 --chapter <对应原小说章节>   # 只读本集用到的几章原文，补长相/空间/道具细节（不与 --context 同用）
   python cli.py read $WS --table 剧本设定                          # 画风 / 画幅
   python cli.py read $WS --table 资产库
   python cli.py read $WS --table 资产库
   python cli.py read $WS --table 资产库
   ```
2. 调用 `drama-asset-extraction` skill，产出：
   - **角色**（含群像）：一句文字描述（≤50 字）
   - **场景**：一场景一图，一句描述（≤50 字）
   - **道具**：反复出现/推动剧情/需外观一致的，一句描述（≤50 字）
   - 复用清单、待补/未指定清单
3. **轻量确认**（不计为正式确认点）：展示资产清单表（类型/名称/新建或复用/描述字数）与写入清单，确认后写入文字资产（不出图）。**只写新建项**；复用项不进 data（写入按 `name` upsert，`status=复用` 的行 CLI 也会跳过）：
   ```bash
   python cli.py write $WS --table 资产库 --data @assets.json
   # 每行必须带 kind（角色/场景/道具），CLI 按 kind 落 类型 字段
   ```
4. 机器校验（错误必须为 0）：
   ```bash
   python skills/drama-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json --library $WS
   ```
5. 资产图**懒加载出图**：待 B1 确定本集 `dependencies` 后，调用 `drama-asset-generation` 按类型套版式（角色四视角 / 场景四视角资料图 / 道具双视角），只为本集用到的资产生成（花预算，清单须列对象与预估花费）。逐张过验收清单；场景图出完还须过 `drama-asset-extraction/references/scene-consistency.md` 的**一致性检查**，硬指标不过不得进入视频生成
6. 旧 skill `script-to-scene-assets` / `novel-to-character-assets` 已并入本 skill，不再单独调用

### B1: 分镜 + 依赖解析 + 视频提示词（drama-segment-generation 一体完成）

1. 读取上下文（只读，无需确认）。设当前集为 N，**剧本表只读 N-1、N、N+1 共 3 集，严禁全量读入；小说原文按 `对应原小说章节` 用 `--chapter` 精确取，禁止通读小说表**：
   ```bash
   python cli.py read $WS --table 剧本表 --episode N --context 1
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 资产库
   python cli.py read $WS --table 资产库    # 此时已有 B0b 产出的 description
   python cli.py read $WS --table 资产库    # 道具绑定用
   python cli.py read $WS --table 剧本分镜表 --episode N   # 重写时避免在旧段上叠写
   ```
   - 前 1 集：承接钩子、人物进场状态与情绪起点；后 1 集：本集要埋的钩子与离场状态
   - 目的：把握本集角色心境、场景布局、人物调度；全量读剧本或带入小说原文会导致上下文膨胀、输出变差
2. 调用 `drama-segment-generation` skill（剧本转提示词 4.2），只对当前集 N 产出：
   - **按段拆分**：**30 秒是模型上限、不是固定值**——按难度定段长（单场景 1~2 人可吃满 30 秒；3 人/有动作 12~20 秒；换场景、≥4 人、群像、打斗、大特效 6~12 秒；参考图 >5 张必须拆段），一段 = 一次生成任务 = 剧本分镜表一行，段 ID 为 `ep{两位集号}_p{两位段序}`（如 `ep10_p05`）；段内镜头从 01 起、时间码从 00:00 起，末镜终点 = 段长
   - **资产绑定表**：本集角色/场景/道具逐条对「资产库」（按 类型 过滤；有图/无图/库里没有→待补），登记 `drafts/asset_ids.json`
   - **场景依赖清单**（场景名）+ 角色依赖清单 + 道具依赖清单 + 待补清单
   - 每段按 4.2 骨架写：`【第NN段｜00:00-本段时长｜场景·事件】` → `【本段资产锁定】`（场景/角色/群像/道具/动物/载具/特效分行，条目 `【R01｜沈幼怡：{资产库：沈幼怡}】`，场景/角色必须带锚点；库里没有的写 `待补：【P02｜名：待补，未读取】`）→ `【本段现场生成】`（可选）→ `【本段整体基准】` → `【本段初始空间】` → 逐镜融合式段落 → 台词行 `00:01-00:02，R01沈幼怡（…地说）：『……』` → `【本段终态】`
   - 正文一律"编号+名称"（`R01沈幼怡`），不写裸名、不加【】；画外音写 `R02陈诚画外音（…地说）` 并给画外方向
3. **草案沟通**：用户提意见 → 只改草案，不写飞书
4. **资产差分比对**：harness 拿 `dependencies`（scenes / characters / props / missing / pending_images）逐条检查三张资产表：
   - 表里有行、有图 → 复用，可绑锚点、占图号
   - 表里有行、没图 → 可绑描述（锚点照写、不占图号），列入**待出图**，交 `drama-asset-generation` 按版式补图
   - 表里没有 → 进 `missing`，锁定区写 `待补：【编号｜名：待补，未读取】`，不写锚点
   - **补资产期间分镜草案不变**；`preflight` 会把待补/缺图列为问题，不过闸不许调模型
5. **确认点 3: 分镜与提示词** — 列入库清单（全部资产就绪后）：
   - 交付前先跑机器校验，错误必须为 0：
     ```bash
     python skills/drama-segment-generation/scripts/check_segment_prompt.py workspace/{剧名}/drafts/ep01_storyboard_v4.md
     ```
   - `write --table 剧本分镜表` 写入分镜（一段一行，`prompt` 为完整段文本，含段头）
   - `expand --shot <id>` 可预览锚点映射与素材清单：确认 `【R01｜沈幼怡：{资产库：沈幼怡}】` 已收成 `【R01｜沈幼怡】`、提示词里没有残留 `{}`、素材齐全
   - ★ **成片时长与声音**：`generate` 按分镜行 `timeline`（如 `00:00-00:30`）的真实秒数出片，上限 30 秒，解析不出才回退 `ark.default_duration`；成本按实际秒数估算，清单里列出各段秒数。本项目**不做 TTS**：对白由视频模型原生发声；需要固定音色时写 `音频参考：{音色库：音色名}`，CLI 会把它作为 `reference_audio` 传给模型
   - 确认后才执行（**先跑资产闸门，不过不许调模型**）：
     ```bash
     python cli.py preflight $WS --episode N    # 生产态资产复检，0 问题才继续
     python cli.py generate $WS
     python cli.py push $WS
     ```
   - 分镜可以先在**预览态**写入评审：`preflight` 未过也能写、能 `expand` 试跑，但审计记 `PENDING（预览）`、不得写 `PASS`；只有 preflight 全过、进入生产态后才写 `自检：PASS`

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
| `drama-initializer` | A1 | 上传小说/剧本 → 剧本设定 + 资产库 |
| `drama-asset-generation` | A2/B0b | 角色/场景/道具 → 版式化提示词 + 出图 + 逐张验收 |
| `novel-to-drama` | B0a | 小说章节 → 剧本表（小说章节/小说内容/完整剧本，1 章 = 1 集） |
| `drama-asset-extraction` | B0b | 剧本+小说 → 角色/场景/道具资产（一句 ≤50 字描述） |
| `drama-segment-generation` | B1 | 剧本 → 资产绑定 + 按难度分段（30 秒上限）+ 依赖解析 + 导演级视频提示词（4.2 骨架：待补标注/现场生成/整体基准/初始空间/终态） |

## References

- `references/checkpoint-protocol.md` — 4 个确认点标准流程 + 写入授权状态机
- `references/pipeline.md` — 完整编排流程图 + 场景两段式调度规则
- `references/data-contracts.md` — 各 skill 数据交接格式与字段约定
- `references/cli-commands.md` — CLI 命令速查表（标注只读 / 需确认）