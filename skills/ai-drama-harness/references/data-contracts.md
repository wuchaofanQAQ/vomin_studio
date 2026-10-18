# 各 skill 数据交接格式与字段约定

harness 负责把上游 skill 的输出**在用户确认后**写入飞书、供下游 skill 读取。约定如下字段，保证衔接不丢信息。

## Automated Mode 输出规范

每个 skill 在 Automated Mode 下，除了产出人类可读 markdown，还必须额外输出一个 **结构化 JSON 代码块**（标记为 ` ```json:structured-output `）。harness 提取 JSON 后**只作为草案展示**，用户确认后才通过 `python cli.py write` 写入飞书。

## 0. 系统设置表（CLI 自动维护，技能不写）

「系统设置」表是项目级引导配置，由 `init` / `init-from-url` 自动写入，drama-initializer 等技能**不产出、不 write**：

| 配置项 | 配置值 | 说明 |
|---|---|---|
| `项目路径` | 本地 workspace 绝对路径，默认 `C:\Users\Heart\PycharmProjects\vomin_studio\workspace\{剧名}` | 凭飞书 URL 定位本地项目；迁移后用 `set-path` 更新 |
| `剧名` | 剧本名称 | 一个剧本一个 workspace 文件夹 |
| `创建时间` | 初始化时间 | — |

用户未指定路径时，workspace 一律默认落到 `项目根/workspace/{剧名}`；路径属于 init 写入清单，需在确认点 1 向用户列明。

## 1. 剧本初始化（drama-initializer → 剧本设定 / 剧集表 / 角色库 / 角色档案）

drama-initializer 一次性产出**四段 JSON**：

### 1a. 剧本设定（match key: `name`）

```json
[
  {"name": "剧名", "value": "重生打脸", "global_prompt": ""},
  {"name": "题材类型", "value": "都市·重生·逆袭", "global_prompt": ""},
  {"name": "画面风格", "value": "真人写实偏电影质感...", "global_prompt": "真人写实，电影色调，..."},
  {"name": "平台调性", "value": "竖屏短剧9:16", "global_prompt": ""},
  {"name": "全集大纲", "value": "第1集：...；第2集：..."}
]
```

下游消费：角色三视图、场景空镜（画风/比例）、storyboard-prompt（世界观/节奏/看点）。

### 1b. 剧集表（match key: `episode`）

```json
[
  {
    "episode": 1,
    "title": "重生第一夜",
    "core_event": "张三重生回到十年前的出租屋",
    "characters": "张三、李四",
    "prev_hook": "",
    "end_hook": "手机亮起，前老板来电",
    "scenes": "1. 出租屋·内·夜（雨）；2. 街边·外·夜",
    "script": "该集完整原文，逐字保留",
    "status": "草稿"
  }
]
```

- `script` 必须是用户上传剧本的该集原文，初始化阶段不允许改写
- `status` 初始为"草稿"，用户确认后由 harness 改为"已确认"，拆分镜后改为"已拆分镜"

### 1c. 角色库 + 角色档案（match key 均为 `name`）

```json
{
  "角色库": [
    {
      "name": "林砚",
      "char_type": "核心",
      "appearance": "28岁亚洲男性，方脸，黑色短发，左眉骨伤疤...",
      "voice_desc": "青年男，沉稳低沉",
      "source": "原始采集"
    }
  ],
  "角色档案": [
    {
      "name": "林砚",
      "char_type": "核心",
      "basic_info": "角色名：林砚\n定位：主角\n出场集数：...\n关系：...",
      "style_desc": "画风基调：电影级写实\n主色调倾向：冷蓝灰",
      "voice_desc": "青年男，沉稳低沉",
      "appearance": "脸型：方脸\n头发：黑色短发\n五官：...",
      "personality": "性格：内敛冷静\n动机：...\n说话风格：...",
      "battle_desc": "战斗风格：...（缺失标'未指定'）",
      "signature_expr": "经典动作：...\n口头禅：...",
      "notes": "来源集数：...\n缺失项：...\n推断项：..."
    }
  ]
}
```

角色档案各模块下游消费：

| 模块 | JSON key | 下游 Skill |
|---|---|---|
| A 基本信息 | `basic_info` | storyboard-prompt |
| B 风格 | `style_desc` | character-three-view-prompt |
| C 音色 | `voice_desc` | TTS/配音（分镜台词按说话人匹配音色） |
| D 外貌 | `appearance` | character-three-view-prompt、storyboard-prompt |
| E 性格 | `personality` | storyboard-prompt（角色演出分化） |
| F 战斗 | `battle_desc` | 分镜动作/特效描写 |
| G 标志性表达 | `signature_expr` | storyboard-prompt |
| H 标注 | `notes` | harness（缺失项/资产状态追踪） |

## 2. 角色三视图提示词（character-three-view-prompt → 角色库 gen_prompt）

**match key**: `name`

```json
[
  {"name": "林砚", "gen_prompt": "正面全身照，28岁亚洲男性..."}
]
```

## 3. 场景提示词（scene-image-prompt → 场景库）

**match key**: `name`

```json
[
  {
    "name": "写字楼大堂",
    "description": "现代化写字楼一层大堂...",
    "gen_prompt": "16:9横构图，现代写字楼大堂...",
    "source": "AIGC生成"
  }
]
```

## 4. 分镜与视频提示词（storyboard-prompt → 剧本分镜表）

**match key**: `shot_id`

storyboard-prompt 一次产出分镜（含 V8 提示词）+ 依赖清单：

```json
{
  "shots": [
    {
      "shot_id": "ep01_s01",
      "episode": 1,
      "shot_number": "S01",
      "timeline": "00:00-00:03",
      "cinematography": "近景·固定·平视",
      "dialogue": "这不可能...",
      "speaker": "林砚",
      "description": "林砚坐在桌前，视线猛地抬向手机屏幕",
      "composition": "三分法",
      "lighting": "低调，冷暖对比",
      "characters": ["林砚"],
      "scene": "出租屋",
      "prompt": "## [参考素材锚定]\n{角色库：林砚} 图1：林砚，男主角，28岁，黑色短发、左眉骨伤疤，黑色冲锋衣\n{场景库：出租屋} 图2：出租屋，林砚住处，筒子楼一居室，室内·夜·雨，冷蓝调\n\n## [STYLE LOCK]\n（完整十二子段；正文直接写林砚/出租屋，不出现{}）",
      "status": "待生成"
    }
  ],
  "dependencies": {
    "scenes": ["出租屋", "写字楼大堂"],
    "characters": ["林砚", "苏晴"],
    "new_scenes": ["重生前出租屋"],
    "new_characters": []
  }
}
```

### 提示词中的素材锚定语法

CLIP 提示词分**锚定段 + 正文**两层：

- **锚定段**（STYLE LOCK 之后）：每行一个引用 + 编号 + 身份说明，必须写清"是谁/是什么角色/什么场景"：
  ```
  ## [参考素材锚定]
  {角色库：林砚} 图1：林砚，男主角，28岁，黑色短发、左眉骨伤疤，黑色冲锋衣
  {场景库：出租屋} 图2：出租屋，林砚住处，筒子楼一居室，室内·夜·雨，冷蓝调
  ```
- **正文**（STYLE LOCK 场景子段/逐秒拆解/微动作）直接用角色名、场景名，不再出现 `{}`。
- CLI 展开时移除标记、保留映射说明，图1/图2 按编号随 API 传递。

| 写法 | 收集的素材 |
|---|---|
| `{角色库：林砚}` / `{角色库:林砚}` | 角色形象图（中英文冒号均可） |
| `{场景库：出租屋}` | 场景空镜图 |
| `{剧本分镜表：ep01_s01}` | 该镜头已生成的图片/视频（动作衔接） |
| `{素材库：素材ID}` / `{生图工作台：任务名}` | 对应素材文件 |
| `{sheetName:rowId}` | 通用形式：表名 + 行主键 |

完整规则见 `storyboard-prompt/references/asset-reference.md`。

harness 流程：
1. 先读 `dependencies`，`new_scenes/new_characters` 经确认后调对应 skill 补资产
2. 素材就绪后用 `python cli.py expand $WS --shot <id>` 预览锚定段映射、确认正文无残留 `{}`
3. 用户确认 → `write --table 剧本分镜表` → `generate --tts-only` → `generate` → `push`

## 交接铁律

1. **剧本原文不丢不改**：上传剧本逐集完整进入剧集表 `script`，初始化只做提取不做改编
2. **全局资产只建一次**：设定卡、角色档案、核心场景不重复抽取，全流程引用复用
3. **画风全局继承**：三视图、场景、视频提示词的画风一律取剧本设定 `画面风格`
4. **同景同名**：场景名称在初始化时归一化，场次列表、场景库、分镜环境锁定三处一致
5. **缺项不臆造**：任一 skill 缺关键字段，标注"未指定"并列入缺失清单，不替编剧脑补
6. **JSON 代码块标记**：Automated Mode 下必须用 ` ```json:structured-output ` 标记
7. **先确认后写入**：任何 `write/generate/push` 都以用户对写入清单的确认为前提
