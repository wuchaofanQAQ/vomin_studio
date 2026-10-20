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

## 3. 逐集预分析（drama-episode-analyzer → 场景库 description + 角色库/角色档案）

**Phase B0**，每集开头运行，产出场景空间设计和新角色识别（含完整 8 模块档案）。

> **懒加载·单基准图**：本阶段只**建场景 + 写 description 文字设计**，不出场景图。`view_angle` 固定为 `全景基准图（默认）`，`bind_status` 置「未绑定」。场景的全景基准图在 storyboard-prompt 绑定场景（`bind_status`→「已绑定」）后由 scene-image-prompt 生成。

```json
{
  "scene_designs": [
    {
      "name": "出租屋",
      "view_angle": "全景基准图（默认）",
      "description": "【场景基础】室内·现代都市小户型出租屋...\n【功能区】...\n【摄影主轴】...\n【物件清单】...\n【门窗】...\n【光源】...\n【画面分层】前景=...；中景=...；远景=...\n【基准图机位】室内基准图：机位高1.5米平视，45°斜角置于...看向对角...，35mm...",
      "bind_status": "未绑定"
    }
  ],
  "skipped_scenes": [
    {"name": "写字楼大堂", "reason": "场景库已有 description"}
  ],
  "new_characters": {
    "角色库": [
      {
        "name": "保镖甲",
        "char_type": "路人",
        "appearance": "高大壮硕，黑色西装，寸头，国字脸",
        "voice_desc": "成年男，低沉粗犷",
        "source": "原始采集"
      }
    ],
    "角色档案": [
      {
        "name": "保镖甲",
        "char_type": "路人",
        "basic_info": "角色名：保镖甲\n定位：龙套\n出场集数：第3集\n身份：赵总私人保镖\n性别：男\n关系：赵总的手下",
        "style_desc": "画风基调：电影级写实\n主色调倾向：黑灰\n整体气质：威压",
        "voice_desc": "成年男，低沉粗犷",
        "appearance": "脸型：国字脸\n头发：寸头黑发\n五官：未指定\n肤色：小麦色\n体型：高大壮硕\n服装：黑色西装、黑色皮鞋\n标志性特征：未指定",
        "personality": "性格：沉默寡言\n动机：听从赵总指令\n说话风格：简短命令式",
        "battle_desc": "战斗风格：未指定",
        "signature_expr": "经典动作：未指定\n口头禅：未指定",
        "notes": "来源集数：第3集\n缺失项：五官、标志性特征、战斗风格"
      }
    ]
  }
}
```

harness 确认后写入：
- 场景库：`write --table 场景库 --data '[{"name":"出租屋","view_angle":"全景基准图（默认）","description":"...","bind_status":"未绑定"}]'`（只建场景行 + description，**暂不 generate 场景图**）
- 角色库 + 角色档案：新角色同时写入两张表（完整 8 模块档案，无需额外深化）

**幂等规则**：已有非空 `description` 的场景自动跳过，不重复分析。已在角色库中的角色跳过，不重复抽取。

## 4. 场景提示词（scene-image-prompt → 场景库）

**match key**: `name` + `view_angle`

**懒加载·单基准图**：每个场景默认只有一行，`view_angle` 固定为 `全景基准图（默认）`，只生成一张全景基准图，不生成其他视角图。场景行带 `bind_status`（`未绑定` / `已绑定`）。

scene-image-prompt 是**执行者**：从场景库读取 `description`（由 drama-episode-analyzer 产出，含前景/中景/远景画面分层与基准图机位），校验完整性后直接组装 `<SPACE MAP>` 段，不再自行产出空间设计。

引用语法：
- `{场景库：写字楼大堂}` → 取该场景的全景基准图

每个场景输出一批 JSON：

**全景基准图（所有场景的唯一一张）：**

```json
[
  {
    "name": "写字楼大堂",
    "view_angle": "全景基准图（默认）",
    "description": "【场景基础】...\n【画面分层】...\n【基准图机位】...",
    "gen_prompt": "<HEADER>\n9:16竖版单场景全景基准图...\n</HEADER>\n\n<STYLE LOCK>...",
    "source": "AIGC生成"
  }
]
```

harness 出图前置条件：该场景 `bind_status` 已为「已绑定」（由 storyboard-prompt 更新）；出图命令 `python cli.py generate $WS --target 场景库:写字楼大堂·全景基准图（默认）`。

## 5. 分镜与视频提示词（storyboard-prompt → 剧本分镜表）

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
      "prompt": "## [参考素材锚定]\n{角色库：林砚} 图1：林砚，男主角，28岁，黑色短发、左眉骨伤疤，黑色冲锋衣\n{场景库：出租屋} 图2：出租屋全景基准图，林砚住处，筒子楼一居室，室内·夜·雨，冷蓝调\n\n## [STYLE LOCK]\n（完整十二子段；正文直接写林砚/出租屋，不出现{}）",
      "status": "待生成"
    }
  ],
  "dependencies": {
    "scenes": [
      {"name": "出租屋"},
      {"name": "写字楼大堂"}
    ],
    "characters": ["林砚", "苏晴"],
    "new_scenes": [
      {"name": "重生前出租屋"}
    ],
    "new_characters": []
  },
  "bind_scenes": ["出租屋", "写字楼大堂"]
}
```

### 提示词中的素材锚定语法

CLIP 提示词分**锚定段 + 正文**两层：

- **锚定段**（STYLE LOCK 之后）：每行一个引用 + 编号 + 身份说明，必须写清"是谁/是什么角色/什么场景"：
  ```
  ## [参考素材锚定]
  {角色库：林砚} 图1：林砚，男主角，28岁，黑色短发、左眉骨伤疤，黑色冲锋衣
  {场景库：出租屋} 图2：出租屋全景基准图，林砚住处，筒子楼一居室，室内·夜·雨，冷蓝调
  ```
- **正文**（STYLE LOCK 场景子段/逐秒拆解/微动作）直接用角色名、场景名，不再出现 `{}`。
- CLI 展开时移除标记、保留映射说明，图1/图2 按编号随 API 传递。

| 写法 | 收集的素材 |
|---|---|
| `{角色库：林砚}` / `{角色库:林砚}` | 角色形象图（中英文冒号均可） |
| `{场景库：出租屋}` | 场景全景基准图（每个场景唯一一张） |
| `{剧本分镜表：ep01_s01}` | 该镜头已生成的图片/视频（动作衔接） |
| `{素材库：素材ID}` / `{生图工作台：任务名}` | 对应素材文件 |
| `{sheetName:rowId}` | 通用形式：表名 + 行主键 |

完整规则见 `storyboard-prompt/references/asset-reference.md`。

harness 流程：
1. 读 `dependencies`，**差分比对场景库**：逐条检查 `scenes` / `new_scenes` 中每个场景行是否已存在、`bind_status` 是否就绪、全景基准图素材是否已生成
   - 缺失/未绑定的场景 → 更新 `bind_status` 为「已绑定」并汇总待补清单，交 `scene-image-prompt` 出全景基准图
   - `new_characters` → 调对应 skill 补角色档案 + 三视图
2. 将 `bind_scenes` 中本集用到的场景行 `bind_status` 更新为「已绑定」：
   ```bash
   python cli.py write $WS --table 场景库 --data '[{"name":"出租屋","bind_status":"已绑定"}]'
   ```
3. 素材就绪后用 `python cli.py expand $WS --shot <id>` 预览锚定段映射、确认正文无残留 `{}`
4. 用户确认 → `write --table 剧本分镜表` → `generate --tts-only` → `generate` → `push`

## 交接铁律

1. **剧本原文不丢不改**：上传剧本逐集完整进入剧集表 `script`，初始化只做提取不做改编
2. **全局资产只建一次**：设定卡、角色档案、核心场景不重复抽取，全流程引用复用
3. **画风全局继承**：三视图、场景、视频提示词的画风一律取剧本设定 `画面风格`
4. **同景同名**：场景名称在初始化时归一化，场次列表、场景库、分镜环境锁定三处一致
5. **缺项不臆造**：任一 skill 缺关键字段，标注"未指定"并列入缺失清单，不替编剧脑补
6. **JSON 代码块标记**：Automated Mode 下必须用 ` ```json:structured-output ` 标记
7. **先确认后写入**：任何 `write/generate/push` 都以用户对写入清单的确认为前提
