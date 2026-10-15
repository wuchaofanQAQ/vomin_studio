# 各 skill 数据交接格式与字段约定

harness 负责把上游 skill 的输出写入飞书、供下游 skill 读取。约定如下字段，保证衔接不丢信息。

## Automated Mode 输出规范

每个 skill 在 Automated Mode 下，除了产出人类可读 markdown，还必须额外输出一个 **结构化 JSON 代码块**（标记为 ` ```json:structured-output `），harness 提取该 JSON 后通过 `python cli.py write` 写入飞书。

## 1. 剧本设定（story-developer → 剧本设定表）

**match key**: `name`（设定项名）

JSON 格式：
```json
[
  {"name": "剧名", "value": "重生打脸", "global_prompt": ""},
  {"name": "题材类型", "value": "都市·重生·逆袭", "global_prompt": ""},
  {"name": "画面风格", "value": "真人写实偏电影质感...", "global_prompt": "真人写实，电影色调，..."},
  {"name": "全集大纲", "value": "第1集：...；第2集：..."}
]
```

下游消费：character-bible-extractor（画风）、character-three-view-prompt（画风+比例）、scene-image-prompt（画风+比例）、episode-generator（世界观/节奏/看点）。

## 2. 角色档案（character-bible-extractor → 角色库 + 角色档案）

**match key**: `name`（角色名，两张表共用）

character-bible-extractor 产出**双表 JSON**：

```json
{
  "角色库": [
    {
      "name": "林砚",
      "char_type": "核心",
      "appearance": "28岁亚洲男性，方脸...",
      "voice_desc": "青年男，沉稳低沉",
      "source": "AIGC生成"
    }
  ],
  "角色档案": [
    {
      "name": "林砚",
      "char_type": "核心",
      "basic_info": "角色名：林砚\n定位：主角\n出场集数：...",
      "style_desc": "画风基调：电影级写实\n主色调倾向：冷蓝灰",
      "voice_desc": "青年男，沉稳低沉",
      "appearance": "脸型：方脸\n头发：黑色短发...",
      "personality": "性格：内敛冷静\n动机：...\n说话风格：...",
      "battle_desc": "战斗风格：近身格斗\n招式：...(缺失标'未指定')",
      "signature_expr": "经典动作：...\n口头禅：...",
      "notes": "来源集数：第1-5集\n缺失项：..."
    }
  ]
}
```

harness 拆分后分别写入：
```bash
python cli.py write $WS --table 角色库 --data '<角色库部分>'
python cli.py write $WS --table 角色档案 --data '<角色档案部分>'
```

下游消费（角色档案各模块）：

| 模块 | JSON key | 下游 Skill |
|---|---|---|
| A 基本信息 | `basic_info` | episode-generator, storyboard-generator |
| B 风格 | `style_desc` | character-three-view-prompt |
| C 音色 | `voice_desc` | TTS/配音（已有 voice_desc 字段） |
| D 外貌 | `appearance` | character-three-view-prompt, storyboard-generator |
| E 性格 | `personality` | **episode-generator** |
| F 战斗 | `battle_desc` | **battle-fx-storyboard** |
| G 标志性表达 | `signature_expr` | **episode-generator, battle-fx-storyboard** |
| H 标注 | `notes` | harness（资产状态追踪） |

## 3. 角色三视图提示词（character-three-view-prompt → 角色库 gen_prompt 字段）

**match key**: `name`（角色名）

JSON 格式（更新已有角色的 gen_prompt）：
```json
[
  {"name": "林砚", "gen_prompt": "正面全身照，28岁亚洲男性..."}
]
```

## 4. 场景提示词（scene-image-prompt → 场景库）

**match key**: `name`（场景名）

JSON 格式：
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

## 5. 分集剧本（episode-generator — 纯文本，不直接写表）

episode-generator 产出纯文本剧本，不输出结构化 JSON。harness 将其作为下游 skill 的输入上下文。

必须含字段：
- 集数 / 核心事件 / 出场角色
- 承接的上集钩子 / 结尾新钩
- 场次列表

## 6. 分镜脚本（storyboard-generator → 剧本分镜表）

**match key**: `shot_id`

JSON 格式：
```json
[
  {
    "shot_id": "ep01_s01",
    "episode": 1,
    "shot_number": "S01",
    "dialogue": "这不可能...",
    "description": "近景，林砚震惊地看着手机屏幕",
    "prompt": "{角色库:林砚}震惊表情，近景，手持手机",
    "status": "待生成"
  }
]
```

依赖清单（附在 JSON 外，供 harness 比对）：
```json
{"new_scenes": ["重生前出租屋"], "new_characters": []}
```

## 7. 视频提示词（video-shot-prompt → 剧本分镜表 prompt 字段）

**match key**: `shot_id`

JSON 格式（更新已有分镜的 prompt）：
```json
[
  {"shot_id": "ep01_s01", "prompt": "{角色库:林砚}在{场景库:出租屋}震惊看手机，近景推特写..."}
]
```

## 交接铁律

1. **全局资产只建一次**：设定卡、角色档案、核心场景不重复抽取，全流程引用
2. **逐集产物标注钩子**：分集剧本必须带"上集钩子+结尾新钩"，保证连续
3. **画风全局继承**：三视图、场景、续集的画风一律取剧本设定的画风基调
4. **缺项不臆造**：任一 skill 缺关键字段，标注"未指定"并提醒用户
5. **JSON 代码块标记**：Automated Mode 下必须用 ` ```json:structured-output ` 标记，harness 按此提取
