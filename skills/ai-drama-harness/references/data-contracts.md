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

## 1. 剧本初始化（drama-initializer → 剧本设定 / 角色库 / 角色档案）

drama-initializer 一次性产出**三段 JSON**（剧本表不在其内，由第 1b 节的 novel-to-script 逐集产出）：

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

下游消费：角色三视图、script-to-scene-assets（画风/画幅）、director-segment-prompt（世界观/节奏/看点）。

### 1b. 剧本表（novel-to-script → 剧本表，match key: `episode`）

**Phase B · B0a** 逐集产出，**严格 1 章 = 1 集**。不属于 drama-initializer。

```json
[
  {
    "episode": 1,
    "title": "重生第一夜",
    "novel_chapter": "第1章 重生",
    "novel_text": "该章小说原文，逐字保留",
    "core_event": "张三重生回到十年前的出租屋",
    "characters": "张三、李四",
    "prev_hook": "",
    "end_hook": "手机亮起，前老板来电",
    "scenes": "1. 出租屋·内·夜（雨）；2. 街边·外·夜",
    "script": "转化后的完整剧本（带结构化场头：场号/内外景/地点/时间/出场人物/关键动作）",
    "status": "草稿"
  }
]
```

| JSON key | 飞书字段 | 说明 |
|---|---|---|
| `episode` | 集数（主键） | 集号，= 章节序号 |
| `novel_chapter` | 小说章节 | 章节号与章名 |
| `novel_text` | 小说内容 | 该章原文全文，逐字留存，**下游 skill 一律不读** |
| `script` | 完整剧本 | **转化后的剧本**，是场景抽取与分镜的唯一剧本来源 |
| 其余 | 集名/核心事件/出场角色/上集钩子/结尾钩子/场次列表/状态 | 沿用原字段，语义不变 |

- `novel_text` 必须是用户上传的原文，写入后不允许改写；`script` 是改编产物，可迭代修改
- `status` 流转：`待转剧本`（迁移后的存量行）→ `草稿` → `已确认` → `已拆分镜`
- **读取口径**：`read --table 剧本表` 默认**剔除 `novel_text`**，仅 `--with-novel` 才带出；拆分镜/抽场景一律不带
- 用户上传的是**成品剧本**时：直接写 `script`，`novel_chapter`/`novel_text` 留空，不经 novel-to-script

### 1c. 角色库 + 角色档案（match key 均为 `name`）

```json
{
  "角色库": [
    {
      "name": "林砚",
      "char_type": "核心",
      "appearance": "28岁亚洲男性，方脸，黑色短发，左眉骨伤疤..."
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
| A 基本信息 | `basic_info` | director-segment-prompt |
| B 风格 | `style_desc` | character-three-view-prompt |
| C 音色 | `voice_desc` | TTS/配音（分镜对白按说话人从角色档案匹配音色；音色字段只在角色档案，角色库没有） |
| D 外貌 | `appearance` | character-three-view-prompt、director-segment-prompt |
| E 性格 | `personality` | director-segment-prompt（角色演出分化） |
| F 战斗 | `battle_desc` | 分镜动作/特效描写 |
| G 标志性表达 | `signature_expr` | director-segment-prompt |
| H 标注 | `notes` | harness（缺失项/资产状态追踪） |

## 2. 角色三视图提示词（character-three-view-prompt → 角色库 gen_prompt）

**match key**: `name`

```json
[
  {"name": "林砚", "gen_prompt": "正面全身照，28岁亚洲男性..."}
]
```

## 3. 逐集新角色识别（novel-to-character-assets → 角色库/角色档案）

**Phase B · B0b 的角色部分**，每集运行，只读当前集的 `剧本表.novel_text`（小说原文，`read --episode N --with-novel`）；`novel_text` 为空时退回 `剧本表.script`。产出新角色识别（含完整 8 模块档案）。

> 场景抽取与空间设计已迁出，由第 4 节 `script-to-scene-assets` 负责。本节不再产出 `scene_designs`。

```json
{
  "new_characters": {
    "角色库": [
      {
        "name": "保镖甲",
        "char_type": "路人",
        "appearance": "高大壮硕，黑色西装，寸头，国字脸"
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
        "notes": "来源：小说第3章\n缺失项：五官、标志性特征、战斗风格"
      }
    ]
  },
  "skipped_characters": ["张三", "李四"]
}
```

harness 确认后写入：角色库 + 角色档案同时写入（完整 8 模块档案，无需额外深化）。

**幂等规则**：已在角色库中的角色跳过，不重复抽取。

## 4. 场景资产（script-to-scene-assets → 场景库）

**Phase B · B0b 的场景部分**，逐集增量运行，读 `剧本表.script`（定场景清单）+ 当前集 `剧本表.novel_text`（补空间细节，为空则只用剧本），取代旧版 drama-episode-analyzer 的场景抽取与 scene-image-prompt。

**match key**：`name` + `view_angle`

### 场景库字段

| JSON key | 飞书字段 | 说明 |
|---|---|---|
| `name` | 场景名 | **空间名**，同一空间的母版/主图/局部共用；**不得含 `·`**；光影变体用全角括号，如 `出租屋（夜）` |
| `view_angle` | 视角 | `母版` / `主场景` / `局部·部位` / `闪回` / `外景`；存量行可为 `全景基准图（默认）` |
| `description` | 场景描述 | 空间设计（场景基础/功能区/摄影主轴/物件/门窗/光源/画面分层/空间锚点/基准图机位） |
| `ref_scenes` | 参考场景 | 派生/咬合所依赖的源图，如 `出租屋（夜）·母版` |
| `relation_note` | 作用关联 | 作用 / 关联类型（派生·咬合·共享锚点·独立）/ 不用于 / 继承约束 |
| `gen_prompt` | 生成提示词 | 七段式提示词（作用→性质→关联→锚点→光线色调→排除→参考图句） |
| `related_episodes` | 关联集数 | 如 `1,3` |
| `source` | 来源 | `AIGC生成` 等 |
| `ref_image` | 文件路径 | 出图后由 `generate` 回填 |

> 飞书「场景库」表已新增 `视角`、`参考场景`、`作用关联` 三个字段。存量表用 `python cli.py migrate-schema <WS> --dry-run` 查看计划，确认后执行迁移。

### 场景引用语法

- `{场景库：出租屋（夜）}` → 裸名，默认取**主场景**；回退顺序：主场景 → 全景基准图 → 正视图 → 其他非母版 → 母版
- `{场景库：出租屋（夜）·母版}` / `{场景库：出租屋（夜）·局部·厨房}` → 显式指定视角
- **母版不直接挂分镜**；派生图的参考图句用显式 `·母版` 引用，由 `expand_prompt` 收集图片作为参考图

### 输出 JSON

```json
{
  "场景库": [
    {
      "name": "出租屋（夜）",
      "view_angle": "母版",
      "description": "【场景基础】...\n【功能区】...\n【摄影主轴】...\n【物件清单】...\n【门窗】...\n【光源】...\n【空间锚点】...\n【基准图机位】...",
      "gen_prompt": "【作用】...【性质】...【关联】...【锚点】...【光线色调】...【排除】...【参考图】无（母版首图）。",
      "ref_scenes": "",
      "relation_note": "作用：空间母版，派生主场景/局部；不直接挂分镜。派生：…",
      "related_episodes": "1,3",
      "source": "AIGC生成"
    },
    {
      "name": "出租屋（夜）",
      "view_angle": "主场景",
      "description": "（同空间，视角按主场景改写，锚点逐条重复母版）",
      "gen_prompt": "...{场景库：出租屋（夜）·母版} 图1：出租屋（夜）空间母版。保持参考图中的入口位置、地面材质与分界、功能区方位、门窗方位、光源方向不变，只改变视角和取景范围。",
      "ref_scenes": "出租屋（夜）·母版",
      "relation_note": "作用：场1、场3 挂参考；不用于局部特写。继承：母版（派生）。咬合：局部·厨房",
      "related_episodes": "1,3",
      "source": "AIGC生成"
    }
  ],
  "reused": [
    {"name": "写字楼大堂", "view_angle": "主场景", "reason": "场景库已有且覆盖本集所需视角"}
  ]
}
```

### harness 动作（每步均需用户确认）

1. 写入场景库文字资产（不出图）：`write --table 场景库 --data '<场景库部分>'`
2. 出图（花预算，清单须列对象与预估花费）：`generate --target 场景库:出租屋（夜）`。同一空间命中多行时，**CLI 自动按 母版 → 主场景 → 局部 → 其他 顺序出图**，保证派生图的 `·母版` 参考图已就绪
3. **一致性检查**（出图后门禁）：入口/开门方向、地面材质与分界、功能区与门窗方位、光源方向、色调，逐图比对；任一不通过先修场景图，**不得进入视频生成**。详见 `script-to-scene-assets/references/consistency-check.md`
4. 出图时机：懒加载——B1 产出 `dependencies` 后，只为本集用到的场景出图

## 5. 分段分镜与视频提示词（director-segment-prompt → 剧本分镜表）

**match key**: `shot_id`（= 段 ID，格式 `ep{两位集号}_p{两位段序}`，如 `ep10_p05`）

一段 = 一次生成任务 = 剧本分镜表一行。director-segment-prompt 一次产出分段提示词 + 依赖清单：

```json
{
  "shots": [
    {
      "shot_id": "ep10_p05",
      "episode": 10,
      "shot_number": "P05",
      "timeline": "00:00-00:20",
      "dialogue": "杨广：人有南北，国有南北吗？",
      "speaker": "杨广",
      "description": "杨广在大殿高位质问姜颜，姜颜答话后被激怒",
      "characters": ["杨广", "姜颜"],
      "scene": "隋朝皇宫大殿",
      "prompt": "【参考素材锚点】\n{角色库：杨广} 图1：【杨广 中年版】，皇帝，高位质问者\n{角色库：姜颜} 图2：【姜颜】，主角\n{场景库：隋朝皇宫大殿} 图3：【隋朝皇宫大殿】主场景，隋代宫殿，白昼\n【本段资产锁定】…（完整段文本：现场生成/整体基准/初始空间/逐镜头含对白时间码/本段终态）",
      "status": "待生成"
    }
  ],
  "dependencies": {
    "scenes": [
      {"name": "隋朝皇宫大殿"}
    ],
    "characters": ["杨广 中年版", "姜颜"],
    "new_scenes": [],
    "new_characters": []
  }
}
```

`prompt` 字段是带换行的完整段文本，以【参考素材锚点】开头；多段即 `shots` 数组里多个对象。

### 提示词中的素材锚点语法

分段提示词分**锚点块 + 正文**两层：

- **锚点块**（段首【参考素材锚点】）：每个出镜角色、每个场景（含空镜）一行，`{表：行标识} 图N：【资产名】，身份说明`；需要动作衔接时加 `{剧本分镜表：上一段ID} 视频N：…`。图/视频连续编号，同素材一段内只声明一次。
- **正文**（资产锁定、现场生成、整体基准、初始空间、镜头、终态）统一用【资产名】，**不出现 `{}`**。
- CLI 展开时移除标记、保留"图N：…"说明，素材按编号随 API 传递。

| 写法 | 收集的素材 |
|---|---|
| `{角色库：杨广}` / `{角色库:杨广}` | 角色形象图（中英文冒号均可） |
| `{场景库：隋朝皇宫大殿}` | 该空间的**主场景**图（裸名默认；`名·局部·部位` 取局部；存量 `全景基准图（默认）` 行可回退命中；**母版不挂分镜**） |
| `{剧本分镜表：ep10_p04}` | 该段已生成的图片/视频（动作衔接） |
| `{素材库：素材ID}` / `{生图工作台：任务名}` | 对应素材文件 |
| `{sheetName:rowId}` | 通用形式：表名 + 行主键 |

完整规则见 `director-segment-prompt/references/asset-binding-and-cli.md`。

harness 流程：
1. 读 `dependencies`，**差分比对场景库**：逐条检查 `scenes` / `new_scenes` 中每个「空间名 + 视角」是否已存在、场景图素材是否已生成且一致性检查已通过
   - 缺失的场景/视角 → 汇总待补清单，交 `script-to-scene-assets` 补出（母版 → 主场景 → 局部）
   - `new_characters` → 调对应 skill 补角色档案 + 三视图
2. 素材就绪后用 `python cli.py expand $WS --shot <id>` 预览锚点映射、确认锚点块外无残留 `{}`
3. 用户确认 → `write --table 剧本分镜表` → `generate --tts-only` → `generate` → `push`

## 交接铁律

1. **原文不丢不改**：小说章节逐字进入剧本表 `小说内容`（写入后不改）；转化后的剧本进入 `完整剧本`，是下游唯一剧本来源；初始化（drama-initializer）只做提取不做改编
2. **全局资产只建一次**：设定卡、角色档案、核心场景不重复抽取，全流程引用复用
3. **画风全局继承**：三视图、场景、视频提示词的画风一律取剧本设定 `画面风格`
4. **同景同名**：场景名称在 novel-to-script 阶段归一化，场次列表、场景库、分镜环境锁定三处一致；场景名不含 `·`
5. **缺项不臆造**：任一 skill 缺关键字段，标注"未指定"并列入缺失清单，不替编剧脑补
6. **JSON 代码块标记**：Automated Mode 下必须用 ` ```json:structured-output ` 标记
7. **先确认后写入**：任何 `write/generate/push` 都以用户对写入清单的确认为前提
