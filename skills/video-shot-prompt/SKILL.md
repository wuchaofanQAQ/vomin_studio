---
name: video-shot-prompt
description: 把分镜脚本/战斗特效分镜转成"可直接投喂 Seedance 2.5 视频生成模型"的 V8 格式 CLIP 提示词。采用 12 子段结构（STYLE LOCK 8 + CLIP 3 + NEGATIVE 1），融合 Seedance 2.5 执行模型的五大升级（情绪物理分解、全身动力学链、环境动态、光照-表面交互、四层画面枚举），标注参考图（角色三视图/场景空镜）以锁定一致性。当用户需要"视频提示词""CLIP""把分镜转视频提示词""出片提示词"，或要把 storyboard-generator / battle-fx-storyboard 的分镜转成能出视频的提示词时使用。本 skill 产出视频提示词，不直接生成视频。
---

# Video Shot Prompt（V8 · Seedance 2.5）

## Overview

把**分镜（storyboard-generator 产出）或战斗特效分镜（battle-fx-storyboard 产出）**转成可直接投喂 Seedance 2.5 的 **V8 格式 CLIP 提示词**。这是整条流水线的**出片入口**：把文字分镜变成专业级视频提示词。

## 核心方法论

### V8 结构（12 子段，缺一不可）

每个 CLIP 提示词必须包含完整 12 子段，详见 `references/v8-structure-template.md`：
- **STYLE LOCK（①-⑧）**：风格锁定 → 色调 → 质感 → 电影质感 → 物理照明 → 人物运动物理 → 场景物理 → N 人声明
- **CLIP（⑨-⑪）**：首帧声明 → 逐秒拆解 → 微动作全程
- **NEGATIVE（⑫）**：场景特定否定限制（3-8 项精准限制，不堆通用词）

### 三反原则

1. **反比喻**：删除所有"像XX""如XX"，直接写视觉事实
2. **反衣物描写**：服装由 @Image 锚定，CLIP 中不重复描写（衣物随动可以写）
3. **反瞳色**：不写眼睛颜色，统一写"视线看向XX"

### Seedance 2.5 五大升级（必做）

详见 `references/seedance-25-execution-model.md`：

1. **情绪→物理分解**：所有情绪词替换为 2-3 个可见肌肉动作
2. **全身动力学链**：每个动作写全四层（主动件/稳定件/补偿件/不自主反应）
3. **环境动态系统**：每 Shot 至少 3-4 个环境动态元素
4. **光照-表面交互**：每个可见角色写明光源→照射部位→色温混合→反射光→阴影→边缘光
5. **四层画面枚举**：前景层/中景层/背景层/空气层全部显式写明

## Workflow

### Step 1 — 加载输入

读齐：**分镜脚本（或战斗分镜）** + **角色三视图提示词/图** + **场景空镜提示词/图** + **剧本设定（画风/平台调性）**。缺则要求提供。

### Step 2 — 导演推理（不进入 CLIP）

对每个 CLIP，先在"导演推理"段完成以下分析（此段不复制给 Seedance）：
- **时间铰链**：哪些镜头间需要连续衔接
- **Shot Function**：每个 Shot 的叙事功能
- **张力机制**：景别/运镜/节奏如何服务张力
- **演出弧线**：角色在本 CLIP 中的演出变化
- **站位**：角色在画面中的相对位置
- **质检**：检查演出是否匹配人设，角色间演出是否分化

### Step 3 — 逐 CLIP 转写

对每个 CLIP，按 V8 12 子段结构完整输出。核心规则：

**格式规则**：
- 按 `v8-structure-template.md` 的 12 子段顺序逐段填写
- 每段不可省略，即使某些信息看似重复
- @Image 全局锁定写在 STYLE LOCK 之后，后续不再重复

**内容规则**：
- **比例**：短剧 9:16 竖屏 / 16:9 横屏，从剧本设定取
- **逐秒拆解**：`[0-1s]` 格式，每秒写明主体动作+镜头运动+光影变化+物理细节
- **上一段结束状态=下一段起始状态**（动作连续性铁律）
- **战斗镜头**：继承特效/状态颜色，参考 battle-fx-storyboard skill 的 `fight-clip-rules.md`
- **2.5 执行模型**：全程应用五大升级，详见 `references/seedance-25-execution-model.md`

**写作技术**：
- 每镜运镜必须全不同——重复运镜=模型偷懒的信号
- 动词要狠——"猛然翻起"不是"缓慢起身"
- 物理细节每镜不重复有递进
- 角色演出匹配人设且角色间分化不雷同

### Step 4 — 标注参考图锁定

@Image 全局锁定（一次性声明），写法见 `v8-structure-template.md` 的"参考图全局锁定写法"。
- 人物锁定 → 角色三视图
- 环境锁定 → 场景空镜
- 战斗特效 → 继承 battle-fx-storyboard 的状态标注

### Step 5 — Preflight 检查

输出前逐项过检：

- [ ] 12 子段是否完整（STYLE LOCK 8 + CLIP 3 + NEGATIVE 1）
- [ ] 三反原则是否遵守（无比喻/无衣物描写/无瞳色）
- [ ] 情绪词是否全部替换为物理动作
- [ ] 每个角色每个时间段是否有全身动力学链
- [ ] 每 Shot 是否有 ≥3 个环境动态元素
- [ ] 每个可见角色是否写了光照-皮肤交互
- [ ] 四层画面枚举是否完整（前景/中景/背景/空气）
- [ ] @Image 锁定是否正确且仅声明一次
- [ ] 逐秒拆解是否连续（上一段末 = 下一段初）
- [ ] 每镜运镜是否全不同
- [ ] NEGATIVE 是否针对本场景具体问题（3-8 项，不堆通用词）
- [ ] 角色演出是否匹配人设且分化

> Preflight 不通过则修改后重新检查，不可跳过。

### Step 6 — 输出与说明

输出完整 CLIP 提示词（含导演推理段标注"不复制"），附 2-3 行说明：比例、镜头数、时长总量。

> 迭代修复参考 `references/iteration-manual.md`。

## References

- `references/v8-structure-template.md` — V8 格式 12 子段结构模板 + STYLE LOCK 示例 + 负面限制选题库（必读）
- `references/seedance-25-execution-model.md` — Seedance 2.5 执行模型：情绪物理分解 / 全身动力学链 / 环境动态 / 光照-表面交互 / 四层画面枚举（必读）
- `references/seedance-prompt-guide.md` — Seedance 2.0/2.5 平台速查：任务类型 / 素材映射 / 输入上限 / 常见坑
- `references/iteration-manual.md` — 迭代修复手册：常见问题修复表 + 成功 CLIP 经验
- `references/video-continuity.md` — 镜头连续性 + @Image 纯净度 + 一致性自查
- `references/video-prompt-template.md` — CLIP 完整输出模板 + 示例

## Automated Mode (Harness Integration)

当被 `ai-drama-harness` 调用时，额外输出结构化 JSON，供 harness 通过 `python cli.py write --table 剧本分镜表` 更新分镜的 `prompt` 字段。

### 读取输入

```bash
python cli.py read $WS --table 剧本分镜表
python cli.py read $WS --table 角色库
python cli.py read $WS --table 角色档案
python cli.py read $WS --table 场景库
python cli.py read $WS --table 剧本设定
```

### JSON 输出格式

````
```json:structured-output
[
  {"shot_id": "ep01_s01", "prompt": "（完整 V8 CLIP 提示词）"},
  {"shot_id": "ep01_s02", "prompt": "（完整 V8 CLIP 提示词）"}
]
```
````

harness 写入后批量执行 `python cli.py generate $WS --tts-only` 和 `python cli.py generate $WS` 触发配音和视频生成。
