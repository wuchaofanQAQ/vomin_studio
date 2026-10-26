# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()

old = t[t.index("### B0b: 场景抽取 + 新角色"):t.index("### B1: 分镜 + 依赖解析 + 视频提示词")]
new = '''### B0b: 资产提取（script-asset-extraction 一体完成）

B0a 写入剧本表之后、拆分镜之前运行。**逐集增量**：库里已有的资产直接复用，只为新资产补描述与提示词；一个资产 = 一行 = 一张图。

1. 读取上下文（只读，无需确认）：
   ```bash
   python cli.py read $WS --table 剧本表 --episode N --context 1   # N±1 的 script（不带小说原文，仅用于跨集延续）
   python cli.py read $WS --table 剧本表 --episode N --with-novel   # 仅当前集：小说原文，补长相/空间/道具细节（不与 --context 同用）
   python cli.py read $WS --table 剧本设定                          # 画风 / 画幅
   python cli.py read $WS --table 角色库
   python cli.py read $WS --table 角色档案
   python cli.py read $WS --table 场景库
   python cli.py read $WS --table 道具库
   ```
2. 调用 `script-asset-extraction` skill，产出：
   - **角色**（含群像）：文字描述 + 提示词（≤50 字）+ 6 模块档案（新角色）
   - **场景**：一场景一图，描述末尾带空间锚点 + 提示词（≤50 字）
   - **道具**：反复出现/推动剧情/需外观一致的，描述 + 提示词（≤50 字）
   - 复用清单、待补/未指定清单
3. **轻量确认**（不计为正式确认点）：展示资产清单表（类型/名称/新建或复用/描述/提示词字数）与写入清单，确认后写入文字资产（不出图）：
   ```bash
   python cli.py write $WS --table 角色库   --data @characters.json
   python cli.py write $WS --table 角色档案 --data @bibles.json
   python cli.py write $WS --table 场景库   --data @scenes.json
   python cli.py write $WS --table 道具库   --data @props.json
   ```
4. 机器校验（错误必须为 0）：
   ```bash
   python skills/script-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json
   ```
5. 资产图**懒加载出图**：待 B1 确定本集 `dependencies` 后，只为本集用到的资产生成（花预算，清单须列对象与预估花费）。场景图出完须过 `script-asset-extraction/references/scene-anchors.md` 的**一致性检查**，硬指标不过不得进入视频生成。要出「场景资料板」（左大正视图 + 右侧东南西北四视角、22:9）时改用 `scene-board-image` skill，默认只出 1 张
6. 旧 skill `script-to-scene-assets` / `novel-to-character-assets` 已并入本 skill，不再单独调用

'''
t = t.replace(old, new)

# B1 里对旧 skill 的引用
t = t.replace("缺失的场景 → 汇总为**待补场景清单**，交 `script-to-scene-assets` 补出（一个场景一张图），逐步生成确认",
              "缺失的场景 → 汇总为**待补场景清单**，交 `script-asset-extraction` 补描述与提示词（一个场景一张图），逐步生成确认")

# 下游 skill 表：两行并一行
t = t.replace("| `script-to-scene-assets` | B0b | 剧本 → 场景清单/图间关联/空间锚点/场景图提示词（一场景一图）+ 一致性检查 |\n| `scene-board-image` | B0b | 单个场景 → 场景资料板提示词（左大正视图+右侧东南西北四视角，22:9）+ 出图 |\n| `novel-to-character-assets` | B0b | 小说原文 → 逐集新角色识别 + 完整 6 模块档案 |",
              "| `script-asset-extraction` | B0b | 剧本+小说 → 角色/场景/道具资产（文字描述 + ≤50 字提示词）+ 角色档案 + 场景锚点 |\n| `scene-board-image` | B0b | 单个场景 → 场景资料板提示词（左大正视图+右侧东南西北四视角，22:9）+ 出图 |")
open(p, "w", encoding="utf-8").write(t)
print("harness B0b rewritten")
