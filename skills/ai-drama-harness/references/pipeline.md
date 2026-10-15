# 完整编排流程 + 节点依赖/产出/CLI 集成

## 一、节点总览

| 节点 | Skill | 前置输入 | 产出 | CLI 读 | CLI 写 |
|---|---|---|---|---|---|
| ① | story-developer | 一句话想法 | 剧本设定+全集大纲 | — | `write --table 剧本设定` |
| ② | character-bible-extractor | 剧本设定 | 角色档案 | `read --table 剧本设定` | `write --table 角色库` + `write --table 角色档案` |
| ③ | character-three-view-prompt | 角色档案+画风 | 出图提示词 | `read --table 角色库` | `write --table 角色库`（更新 gen_prompt） |
| ④ | scene-image-prompt | 场景描述+画风 | 出图提示词 | `read --table 剧本设定` | `write --table 场景库` |
| ⑤ | episode-generator | 设定+大纲+角色 | 分集剧本 | `read --table 剧本设定/角色库/角色档案` | —（文本产出） |
| ⑥ | storyboard-generator | 剧本+角色+场景 | 分镜脚本+依赖 | `read --table 角色库/角色档案/场景库` | `write --table 剧本分镜表` |
| ⑦ | battle-fx-storyboard | 战斗戏+角色 | 特效分镜 | `read --table 角色库/角色档案` | `write --table 剧本分镜表` |
| ⑧ | video-shot-prompt | 分镜+参考图 | 视频提示词 | `read --table 剧本分镜表` | `write --table 剧本分镜表`（更新 prompt） |

## 二、节点间依赖

```
① story-developer ──(设定+大纲)──→ 可并行：②角色档案 / ④核心场景
                                     │
② character-bible-extractor ──(角色档案)──→ ③ character-three-view-prompt
                                     │                ↓
                                     │        generate --target 角色库:XXX
                                     │
④ scene-image-prompt ──────────────────────→ generate --target 场景库:XXX
                                     │
⑤ episode-generator ←─(①设定+②角色，不需要④场景图)
      ├──(本集剧本)──→ ⑥ storyboard-generator
      │                 └──(依赖清单)──→ 比对 → 补③④新增
      └──(结尾钩子)──→ 下一集 ⑤
                        ↓
⑧ video-shot-prompt → generate (配音+视频) → push
```

**关键**：写剧本（⑤）不依赖场景图（④）。

## 三、Phase A — 初始化流程（含 CLI）

```
A1: story-developer → [确认点1] → 模式B此时才 init 建表 → write --table 剧本设定
A2: read 剧本设定 → character-bible-extractor → write --table 角色库 + 角色档案 → [确认点2]
A3: character-three-view-prompt → write 角色库(gen_prompt) → generate --target 角色库:X → [确认点3·飞书]
A4: scene-image-prompt → write 场景库 → generate --target 场景库:X → [确认点4·飞书]
```

## 四、Phase B — 逐集流程（含 CLI）

```
B1: read 剧本设定+角色库+角色档案 → episode-generator → [确认点5]
B2: storyboard-generator → write 剧本分镜表 → read 场景库/角色库 比对 → 补生成 → [确认点6]
B3: video-shot-prompt → write 剧本分镜表(prompt) → generate --tts-only → generate → push → [确认点7·飞书]
B4: pull → 检查返工 → 下一集
```

## 五、场景两段式调度

**Phase A · 核心场景（提前定调）**
- 从剧本设定识别"全剧贯穿"核心场景，批量出 5~8 张，作全剧画风基准

**Phase B · 剧情场景（滚动补生成）**
- 每集提取分镜依赖清单中的场景，比对场景库：新增→补，已有→复用

## 六、harness 维护的清单

角色库和场景库即为清单，通过飞书表格实时维护：
- `python cli.py read $WS --table 角色库` — 查看所有角色及状态
- `python cli.py read $WS --table 场景库` — 查看所有场景及状态

## 七、编排注意

- 下游 skill 产出文字内容 + 结构化 JSON，harness 通过 CLI `write` 写入飞书
- 出图/出视频通过 `generate` 命令触发，不再需要用户手动执行
- 用户跳过某环节 → harness 按需裁剪，不强制全流程
- ①必须先于②③④⑤；②必须先于③；③④可独立；⑤依赖①+②，不依赖④
