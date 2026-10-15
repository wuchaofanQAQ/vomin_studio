---
name: ai-drama-harness
description: AI 短剧全自动生产编排层。用户给飞书表格链接+一句话想法即可启动全流程。harness 通过 CLI 读写飞书数据、调度下游 skill、触发素材生成，人只在关键节点做确认。支持 Phase A（初始化全局资产）和 Phase B（逐集滚动生产）。
---

# AI Drama Harness — 全自动编排层

## Overview

短剧生产**全自动编排层**。用户只给飞书多维表格链接 + 一句话想法，harness 自动：
1. 初始化 workspace 并绑定飞书
2. 按序调度下游 skill 产出文字内容
3. 通过 CLI 将产出写入飞书 + 触发素材生成
4. 在 7 个关键节点暂停等待人类确认
5. 循环滚动直到全集完成

## 启动协议

用户输入以下任一形式即开始：

**模式 A — 接入已有飞书表格**（推荐）：
```
飞书链接: https://xxx.feishu.cn/base/XxxYyyZzz
想法: 外卖员重生回10年前打脸前老板的短剧，30集
```

harness 执行：
```bash
python cli.py init-from-url "https://xxx.feishu.cn/base/XxxYyyZzz" ./workspace --name "重生打脸"
```

**模式 B — 从零创建**：
```
剧名: 重生打脸
想法: 外卖员重生回10年前打脸前老板的短剧，30集
```

模式 B **不在此时建表**。先聊完剧本设定、用户确认满意后，再在 A1 确认点之后执行 `init` 创建飞书表格 + 写入数据（见 Phase A 流程）。

启动后设定全局变量 `WS=./workspace`，后续所有 CLI 命令使用此路径。

## 确认点协议

harness 在以下 7 个节点暂停，等待用户确认：

### 文本确认（对话中）

```
--- 确认点 {N}: {标题} ---
{产出摘要，显示关键内容}

请确认：
  "确认" → 继续下一步
  "修改: <意见>" → 按意见调整后重来
  "重做" → 全部重新生成
```

### 飞书审核（图片/视频/音频）

```
--- 确认点 {N}: {标题} ---
已推送到飞书，请在飞书中查看并审核。

完成后回复"继续"。
如需返工，在飞书中将状态改为"返工"后回复"继续"。
```

## Phase A — 初始化（建全局资产）

### A1: 剧本设定 + 全集大纲

1. 调用 `story-developer` skill，传入用户想法
2. skill 产出结构化 JSON（`json:structured-output` 代码块）
3. **确认点 1: 剧本设定** — 对话确认设定和大纲
4. 确认后写入飞书：
   - **模式 B（从零创建）**：此时才创建飞书表格 + workspace：
     ```bash
     python cli.py init ./workspace --name "重生打脸"
     ```
   - 写入数据（模式 A/B 通用）：
     ```bash
     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     ```

### A2: 角色档案

1. 读取设定：
   ```bash
   python cli.py read $WS --table 剧本设定
   ```
2. 调用 `character-bible-extractor` skill
3. skill 产出双表 JSON（`{"角色库": [...], "角色档案": [...]}`）
4. 拆分写入两张表：
   ```bash
   python cli.py write $WS --table 角色库 --data '<角色库部分>'
   python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
   ```
5. **确认点 2: 角色档案** — 对话确认角色设定

### A3: 角色三视图 → 出图

1. 调用 `character-three-view-prompt` skill，为每个核心角色出 4 张照片提示词
2. 将 gen_prompt 写入角色库：
   ```bash
   python cli.py write $WS --table 角色库 --data '[{"name":"林砚","gen_prompt":"..."}]'
   ```
3. 逐角色触发生成：
   ```bash
   python cli.py generate $WS --target 角色库:林砚
   python cli.py generate $WS --target 角色库:苏晴
   ```
4. **确认点 3: 角色形象** — 飞书审核角色图片

### A4: 核心场景 → 出图

1. 从设定中提取 5~8 个核心高频场景
2. 调用 `scene-image-prompt` skill 生成场景提示词
3. 写入场景库并触发生成：
   ```bash
   python cli.py write $WS --table 场景库 --data '<JSON>'
   python cli.py generate $WS --target 场景库:写字楼大堂
   ```
4. **确认点 4: 核心场景** — 飞书审核场景图片

Phase A 完成后，全局资产就绪：设定卡 + 角色档案(含形象图) + 核心场景图。

## Phase B — 逐集滚动

对每一集重复：

### B1: 写分集剧本

1. 读取上下文：
   ```bash
   python cli.py read $WS --table 剧本设定
   python cli.py read $WS --table 角色库
   python cli.py read $WS --table 角色档案
   ```
2. 调用 `episode-generator` skill（传入大纲、上集钩子、角色档案中的性格/标志性表达）
3. **确认点 5: 分集剧本** — 对话确认本集剧本

### B2: 拆分镜 + 补资产

1. 调用 `storyboard-generator` skill
2. skill 产出分镜表 JSON + 依赖清单
3. 写入飞书：
   ```bash
   python cli.py write $WS --table 剧本分镜表 --data '<JSON>'
   ```
4. 比对依赖清单 vs 现有资产：
   ```bash
   python cli.py read $WS --table 场景库
   python cli.py read $WS --table 角色库
   ```
5. 新增场景/角色 → 调对应 skill 补生成提示词 → `generate`
6. **确认点 6: 分镜脚本** — 对话确认分镜

### B3: 视频提示词 → 批量生成

1. 调用 `video-shot-prompt` skill 转视频提示词
2. 更新分镜表：
   ```bash
   python cli.py write $WS --table 剧本分镜表 --data '<JSON>'
   ```
3. 批量配音 + 视频：
   ```bash
   python cli.py generate $WS --tts-only
   python cli.py generate $WS
   python cli.py push $WS
   ```
4. **确认点 7: 视频成片** — 飞书审核视频

### B4: 检查返工 → 下一集

1. 拉取状态：
   ```bash
   python cli.py pull $WS
   ```
2. 检查是否有"返工"状态的分镜，如有则重新生成
3. 全部"通过"后，进入下一集（回到 B1）

## 战斗戏分支

当分镜中包含战斗/打斗场景时，在 B2 和 B3 之间插入：
1. 调用 `battle-fx-storyboard` skill 拆战斗特效分镜
2. 合并回分镜表

## 编排的下游 Skill

| Skill | Phase | 职责 |
|---|---|---|
| `story-developer` | A1 | 想法 → 设定+大纲 |
| `character-bible-extractor` | A2 | 剧本 → 角色档案 |
| `character-three-view-prompt` | A3 | 角色 → 出图提示词 |
| `scene-image-prompt` | A4/B2 | 场景 → 出图提示词 |
| `episode-generator` | B1 | 大纲 → 分集剧本 |
| `storyboard-generator` | B2 | 剧本 → 分镜脚本 |
| `battle-fx-storyboard` | B2+ | 战斗戏 → 特效分镜 |
| `video-shot-prompt` | B3 | 分镜 → 视频提示词 |

## References

- `references/pipeline.md` — 完整编排流程图 + 场景两段式调度规则
- `references/data-contracts.md` — 各 skill 数据交接格式与字段约定
- `references/cli-commands.md` — CLI 命令速查表
- `references/checkpoint-protocol.md` — 7 个确认点标准流程
