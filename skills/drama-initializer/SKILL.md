---
name: drama-initializer
description: 剧本初始化技能。根据用户上传的小说章节或已写好的剧本（txt/md/docx/pdf/飞书文档/粘贴文本），一次性生成两大全局资产：①剧本设定（剧集圣经：题材/基调/画风/世界观/主线/看点/全集大纲）②角色档案（跨章抽取全角色，产出角色库精简版+角色档案8模块初版）。不再产出剧本表：逐集的小说转剧本由 novel-to-script 在 Phase B 逐集完成。当用户说"剧本初始化""初始化剧本""导入剧本""导入小说""我上传了剧本""根据剧本建项目""把这个剧本拆成角色和设定"时使用。本技能只产出文字资产，不直接写飞书、不直接出图——写入必须经用户确认后由 harness 执行。
---

# Drama Initializer — 剧本初始化

## Overview

流水线的**起点技能**（替代旧的 story-developer）。输入是用户**已经写好的小说章节或剧本**，不是一句想法：通读后，产出下游生产所需的两大全局资产：

```
用户上传小说章节 / 剧本
  → ① 剧本设定（剧集圣经）          → 飞书·剧本设定表
  → ② 角色档案（角色库 + 角色档案）  → 飞书·角色库 + 角色档案
```

**不产出剧本表。** 逐集的「小说 → 剧本」转化由 `novel-to-script` 在 Phase B 每集开头完成，写入飞书·剧本表（小说章节、小说内容、完整剧本）。

产出后下游衔接：角色三视图（character-three-view-prompt）、逐集小说转剧本（novel-to-script）、场景抽取（script-to-scene-assets）、分镜与提示词（director-segment-prompt）。

## 核心铁律

1. **原文是唯一事实来源**：剧情、人物、台词以原文为准，不改编、不续写、不"优化"。
2. **不臆造**：原文没有的设定标"未指定"，必要的补全（如画风、时长）按题材惯例推断并标注【推断】/【默认】，列入待确认清单。
3. **只产出草案，绝不擅自写飞书**：所有产物先在对话中展示；只有用户明确说"确认/写入"后，才由 harness 执行 CLI 写入。用户在讨论、提意见、问问题时，只改草案，不触发任何写入。

## Workflow

### Step 1 — 接收并通读原文

按 `references/script-intake.md` 执行：

- 读取用户上传的小说章节/剧本全文（多格式/多文件），建立结构索引：剧名、章节（集）边界、角色名单、时空设定、画风线索
- 完整性检查：预计集数（= 章节数，**严格 1 章 = 1 集**）、单集时长、画面比例、画风基调、已上传到第几章——缺项**合并成一次提问**，不逐条轰炸
- 超长原文按章分段读完，避免遗漏

### Step 2 — 生成剧本设定（剧集圣经）

按 `references/setting-template.md` 从原文中提取/归纳，必须含：

1. 剧名 + 一句话卖点（logline）
2. 题材类型与定位（受众、平台调性、对标作品）
3. 基调（爽/虐/甜/燃…）
4. 剧情简介（一句话 + 300 字 + 世界观规则，规则必须自洽）
5. 主线与冲突（主冲突、主角目标、对抗力量）
6. **画面风格**（画风/色调/光影/质感/比例，★ 全局画风锚点，下游出图出片统一继承）
7. 剧本节奏（单集时长、集数、钩子密度、爽点分布）
8. 看点 / 爽点清单
9. 从原文事实提炼的剧情弧线与全集大纲（不重新设计走向；已上传的章节才写，未上传的不替用户续写）

每项标注【原文】/【推断】/【默认】。

### Step 3 — 抽取角色档案（初版）

按 `references/character-extract-init.md` 跨全部已上传章节抽取，产出**双表数据**：

- **角色库**（精简版）：`name` / `char_type` / `appearance`（外貌+标志性特征）；音色 `voice_desc` 只放角色档案
- **角色档案**（8 模块初版）：`basic_info` / `style_desc` / `voice_desc` / `appearance` / `personality` / `battle_desc` / `signature_expr` / `notes`

要求：有台词有动作的角色全抽；别名归一；缺失项标"未指定"进 `notes`；画风从剧本设定继承。逐集阶段如发现新角色，由 `novel-to-character-assets` 补充完整档案。

### Step 4 — 输出、说明与确认

1. 在对话中展示两部分产物摘要（设定核心项、角色清单与关键设定）+ 完整 markdown
2. 附说明：信息来源汇总（原文/推断/默认各有哪些）、待确认项清单、缺失项清单
3. 用户提意见 → 只修改对应草案并重新展示，**不写飞书**
4. 用户明确确认后，harness 才执行写入（见下）

> 剧本表（逐集的小说章节、小说内容、完整剧本）**不在本技能产出范围**，由 `novel-to-script` 在 Phase B 逐集产出。若用户上传的是**已写好的成品剧本**（而非小说），由 harness 直接按集写入剧本表的 `script`，同样不经本技能。

## Automated Mode (Harness Integration)

被 `ai-drama-harness` 调用时，在 markdown 末尾输出一个结构化 JSON 代码块。harness **必须在用户确认后**才执行写入；用户未确认时 JSON 仅作草案展示。

### 读取输入

- 主输入：用户上传的小说章节 / 剧本文件 / 粘贴文本 / 飞书文档链接
- 无已建设定时无需 read（本技能是流程起点）

### JSON 输出格式（三段）

````
```json:structured-output
{
  "剧本设定": [
    {"name": "剧名", "value": "重生打脸", "global_prompt": ""},
    {"name": "题材类型", "value": "都市·重生·逆袭", "global_prompt": ""},
    {"name": "基调", "value": "...", "global_prompt": ""},
    {"name": "剧情简介", "value": "...", "global_prompt": ""},
    {"name": "世界观规则", "value": "...", "global_prompt": ""},
    {"name": "主线与冲突", "value": "...", "global_prompt": ""},
    {"name": "画面风格", "value": "真人写实偏电影质感...", "global_prompt": "画风描述，供全局继承"},
    {"name": "平台调性", "value": "竖屏短剧9:16", "global_prompt": ""},
    {"name": "剧本节奏", "value": "...", "global_prompt": ""},
    {"name": "剧本看点", "value": "...", "global_prompt": ""},
    {"name": "全集大纲", "value": "第1集：...；第2集：..."}
  ],
  "角色库": [
    {
      "name": "张三",
      "char_type": "核心",
      "appearance": "28岁亚洲男性，方脸，黑色短发，左眉骨伤疤，黑色冲锋衣"
    }
  ],
  "角色档案": [
    {
      "name": "张三",
      "char_type": "核心",
      "basic_info": "角色名：张三\n别名：...\n定位：主角\n身份：...\n出场集数：第1-30集\n关系：...",
      "style_desc": "画风基调：...（继承画面风格）\n主色调：...\n气质：...",
      "voice_desc": "青年男，沉稳低沉，语速中等",
      "appearance": "年龄：...\n脸型：...\n发型：...\n标志性特征：...\n常驻服装：...",
      "personality": "性格：...\n动机：...\n弱点：...\n说话风格：...",
      "battle_desc": "（非战斗题材标'未指定'）",
      "signature_expr": "经典动作：...\n口头禅：...\n标志道具：...",
      "notes": "来源集数：第1-5集\n缺失项：...\n推断项：..."
    }
  ]
}
```
````

### 确认后的写入顺序（harness 执行，每步均需用户确认）

**项目路径策略（先问用户，再 init）**：

- 推荐默认路径：`C:\Users\Heart\PycharmProjects\vomin_studio\workspace\{剧名}`
- 一个剧本一个文件夹，workspace 根目录下并存多个剧本；用户也可指定任意其他路径
- 剧名中的非法文件名字符（`\ / : * ? " < > |`）由 CLI 自动替换为 `_`
- 向用户说明默认路径并征得同意（或接收用户指定路径）后，再执行 init

```bash
# 模式 B（从零开始）：用户确认后才建表 + workspace
#   省略路径 → 自动落到 项目根/workspace/剧名
python cli.py init --name "剧名"
#   或用户指定路径
python cli.py init "D:\my_dramas\剧名" --name "剧名"

# 模式 A（已有飞书链接）：同样可省略路径（建议带上 --name）
python cli.py init-from-url "<飞书URL>" --name "剧名"
```

`init` / `init-from-url` 完成后会**自动向飞书「系统设置」表写入**：
- `项目路径`：本地 workspace 绝对路径（之后仅凭飞书 URL 即可定位本地项目）
- `剧名`、`创建时间`

随后写入三张业务表：

```bash
python cli.py write $WS --table 剧本设定 --data '<剧本设定部分>'
python cli.py write $WS --table 角色库   --data '<角色库部分>'
python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
```

> 系统设置由 CLI init 自动维护，drama-initializer 不需要、也不要手写该表。
> 剧本表由 `novel-to-script` 逐集写入，本技能不写。

## 产出交接

- 角色三视图/定妆照 → `character-three-view-prompt`（吃角色库 appearance + 画面风格）
- 逐集小说转剧本 → `novel-to-script`（吃剧本设定 + 角色库 + 小说章节）
- 逐集场景抽取 → `script-to-scene-assets`（吃剧本设定 + 剧本表 script + 当前章小说内容补空间细节）
- 逐集分镜 + 视频提示词 → `director-segment-prompt`（吃剧本表 + 角色档案 + 场景库）
- 逐集新角色识别与档案产出 → `novel-to-character-assets`

## References

- `references/script-intake.md` — 原文接收、通读、结构索引与完整性检查（Step 1）
- `references/setting-template.md` — 剧本设定（剧集圣经）12 节模板（Step 2）
- `references/character-extract-init.md` — 角色档案初始化抽取规则与 8 模块（Step 3）
