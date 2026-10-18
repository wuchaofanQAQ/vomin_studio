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
4. 在 5 个关键节点暂停等待人类确认
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
  2. [write] 剧集表 ×30 行（新增 30）
  3. [write] 角色库 ×6 行 / 角色档案 ×6 行
  4. [init] 新建飞书多维表格（仅模式 B 首次）
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

> 唯一例外：用户启动时明确说"全自动/不用确认/跳过确认"，则跳过**对话确认点**（#1 #4），但飞书图片/视频审核（#2 #3 #5）必须保留，且在启动时要向用户复述一遍"将自动写入哪些内容"作为一次性总授权。

## 启动协议

**模式 A — 接入已有飞书表格 + 上传剧本**（推荐）：

```
飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz
剧本: （上传 .txt/.md/.docx/pdf 或飞书文档）
```

harness 执行（只读初始化，不写业务数据）：

```bash
# 路径可省略，默认落到 项目根/workspace/剧名；也可显式指定
python cli.py init-from-url "https://xxx.feishu.cn/base/XxxYyyZzz" --name "重生打脸"
```

**模式 B — 只有剧本，从零开始**：

```
剧本: （上传剧本文件）
```

模式 B **不在启动时建表**。剧本初始化草案产出、用户在确认点 1 确认后，才执行 `init` 建表并写入（见 Phase A）。

> 只有一句话想法、没有剧本：不走本流程。`drama-initializer` 只处理现成剧本；请用户先提供剧本文件。

**项目路径策略（两种模式统一）**：

- 每个剧本一个独立文件夹，统一放在 `C:\Users\Heart\PycharmProjects\vomin_studio\workspace\{剧名}` 下
- 向用户**推荐默认路径**；用户也可指定其他路径（在写入清单中列明实际路径）
- `init` / `init-from-url` 完成后自动向飞书「系统设置」表写入 `项目路径`、`剧名`、`创建时间`，之后凭飞书 URL 即可定位本地项目
- 启动后将实际路径设为全局变量 `WS`（默认即 `.../workspace/剧名`）

## 确认点协议（共 5 个）

| # | 标题 | Phase | 方式 | 确认后动作 |
|---|---|---|---|---|
| 1 | 剧本初始化（设定+剧集+角色档案） | A1 | 对话确认 | init（模式B）+ write 四张表 |
| 2 | 角色形象 | A3 | 飞书审核 | 三视图 generate |
| 3 | 核心场景 | A4 | 飞书审核 | 场景图 generate |
| 4 | 分镜与视频提示词（逐集） | B1 | 对话确认 | 补资产 + write 分镜表 + generate |
| 5 | 视频成片（逐集） | B2 | 飞书审核 | 返工/通过，进入下一集 |

标准模板与处理逻辑见 `references/checkpoint-protocol.md`。

## Phase A — 初始化（建全局资产）

### A1: 剧本初始化（drama-initializer）

1. 接收并通读用户上传的剧本（必要时一次性追问缺失项）
2. 调用 `drama-initializer` skill，产出三段草案：**剧本设定 + 剧集表 + 角色库/角色档案**
3. **确认点 1: 剧本初始化** — 展示草案摘要与写入清单（四张表），对话确认
4. 用户确认后才执行：
   - 模式 B：此时才建表 + workspace（路径写入清单要列明；省略则用默认 `项目根/workspace/剧名`）：
     ```bash
     python cli.py init --name "重生打脸"
     # 或用户指定：python cli.py init "D:\my_dramas\重生打脸" --name "重生打脸"
     ```
   - init 自动写入飞书「系统设置」：项目路径 / 剧名 / 创建时间（无需单独 write）
   - 依次写入（四张表都属同一份清单，一次确认后可连续执行）：
     ```bash
     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     python cli.py write $WS --table 剧集表   --data '<JSON>'
     python cli.py write $WS --table 角色库   --data '<角色库部分>'
     python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
     ```
5. 用户提修改意见 → 只改草案，重新走确认点 1，**不写入**
6. 角色档案如需深化（补全缺失项），可在确认后另调 `character-bible-extractor`，更新档案前仍需列清单确认

### A2: 角色三视图 → 出图

1. 调用 `character-three-view-prompt` skill，为每个核心角色出三视图提示词（草案）
2. 向用户展示提示词草案与"将要写入 gen_prompt + 触发 N 个角色出图"的清单，**确认后**：
   ```bash
   python cli.py write $WS --table 角色库 --data '[{"name":"林砚","gen_prompt":"..."}]'
   python cli.py generate $WS --target 角色库:林砚
   ```
3. **确认点 2: 角色形象** — 飞书审核角色图片

### A3: 核心场景 → 出图

1. 从剧集表场次列表中提取 5~8 个核心高频场景（名称已在初始化时归一化）
2. 调用 `scene-image-prompt` skill 生成场景提示词（草案）
3. 确认后才写入并触发生成：
   ```bash
   python cli.py write $WS --table 场景库 --data '<JSON>'
   python cli.py generate $WS --target 场景库:写字楼大堂
   ```
4. **确认点 3: 核心场景** — 飞书审核场景图片

Phase A 完成后，全局资产就绪：设定卡 + 剧集表（含原文）+ 角色档案（含形象图）+ 核心场景图。

## Phase B — 逐集滚动

对每一集重复：

### B1: 分镜 + 依赖解析 + 视频提示词（storyboard-prompt 一体完成）

1. 读取上下文（只读，无需确认）。设当前集为 N，**剧集表只读 N-1、N、N+1 共 3 集，严禁全量读入**：
   ```bash
   python cli.py read $WS --table 剧集表 --episode N --context 1
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 角色库
   python cli.py read $WS --table 角色档案
   python cli.py read $WS --table 场景库
   ```
   - 前 1 集：承接钩子、人物进场状态与情绪起点；后 1 集：本集要埋的钩子与离场状态
   - 目的：把握本集角色心境、场景布局、人物调度；全量读剧集会导致上下文膨胀、输出变差
2. 调用 `storyboard-prompt` skill，只对当前集 N 产出：
   - 逐镜头分镜（含时间线/景别运镜/描述/台词/构图光影）
   - 场景依赖清单 + 角色依赖清单（含新增待补）
   - 每个镜头的 V8 视频提示词：开头「参考素材锚定」段用 `{角色库：…} 图N：是谁+身份` / `{场景库：…} 图N：什么场景+时空` 逐行声明，正文直接用角色名/场景名、不出现 `{}`
3. **草案沟通**：用户提意见 → 只改草案，不写飞书
4. **确认点 4: 分镜与提示词** — 列入库清单：
   - 新增场景/角色：先列出补资产动作（补提示词 + 出图），确认后补齐
   - `write --table 剧本分镜表` 写入分镜
   - `expand --shot <id>` 可预览锚定段映射与素材清单，确认正文无残留 `{}`、素材齐全
   - 确认后才执行：
     ```bash
     python cli.py generate $WS --tts-only
     python cli.py generate $WS
     python cli.py push $WS
     ```

### B2: 视频成片审核 → 下一集

1. **确认点 5: 视频成片** — 飞书审核
2. 用户回复"继续"后：
   ```bash
   python cli.py pull $WS
   ```
3. 检查"返工"状态分镜；**返工重新生成前必须再次列清单确认**
4. 全部"通过"后进入下一集（回到 B1）

## 编排的下游 Skill

| Skill | Phase | 职责 |
|---|---|---|
| `drama-initializer` | A1 | 上传剧本 → 剧本设定 + 剧集 + 角色档案 |
| `character-bible-extractor` | A1+（可选深化） | 角色档案补全/深化 |
| `character-three-view-prompt` | A2 | 角色 → 三视图出图提示词 |
| `scene-image-prompt` | A3/B1 | 场景 → 空镜出图提示词 |
| `storyboard-prompt` | B1 | 剧本 → 分镜 + 依赖解析 + 视频提示词 |

## References

- `references/checkpoint-protocol.md` — 5 个确认点标准流程 + 写入授权状态机
- `references/pipeline.md` — 完整编排流程图 + 场景两段式调度规则
- `references/data-contracts.md` — 各 skill 数据交接格式与字段约定
- `references/cli-commands.md` — CLI 命令速查表（标注只读 / 需确认）
