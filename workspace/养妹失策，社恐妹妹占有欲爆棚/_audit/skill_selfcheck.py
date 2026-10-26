# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

old = """### Step 4 — 自检 + 机器校验

先按 4.2 做两轮自检（材料覆盖 → 逐镜模拟拍摄），过 `references/self-check.md`，再跑：

```bash
python skills/drama-segment-generation/scripts/check_segment_prompt.py workspace/{剧名}/drafts/ep01_storyboard_v4.md
# 有编号登记表时加 --registry workspace/{剧名}/drafts/asset_ids.json
```

脚本校验：段头与时长、四段结构（资产锁定/整体基准/初始空间/终态）、镜头时间码首尾相接、末镜=段长、资产分类与编号格式、角色/场景锚点、待补标注、正文裸名、台词格式（含"说"）、画外音方向、台词语速、跨段依赖词、空泛形容词、每镜景别/运镜/停点、单段字数。**任一 ✗ 不许交付。**"""

new = """### Step 4 — 亲自通读 + 两轮自检 + 机器校验

**必须亲自从头到尾读一遍全稿，不许用脚本代替。** 脚本只查机械项；「这句话拍不拍得出来、和前一句冲不冲突」只能读出来。

顺序不能颠倒：

1. **通读全稿**：从第 1 段第 1 镜读到末段终态，逐句问「这个景别拍得到吗、和前一句矛盾吗、时间够吗」。
2. **第一轮：材料与覆盖**（段界/时长/原切镜/事件/台词/身份/资产名/待补/用户最新要求/字数/平台/材料是否真读到/旧项目残留）。
3. **第二轮：逐镜模拟拍摄**（机位与可见/遮挡、动作时间线、接触先于结果、摄影机反馈、特效传播、群像、光影声音、切镜终态、动作密度、文戏目线与受光）。
4. **修正闭环**：改实际提示词 → 复检受影响镜头与相邻衔接 → 空间轴/身份/资产替换/世界尺度改动回查全场 → 高风险项定向第三轮。
5. 最后才跑脚本：

```bash
python skills/drama-segment-generation/scripts/check_segment_prompt.py workspace/{剧名}/drafts/ep01_storyboard_v4.md
```

完整清单、检查表、高风险回归类型、武戏专项与失败反馈处理见 `references/self-check.md`。

**脚本任一 ✗ 不许交付；但脚本全 ✓ 也不等于自检通过——必须报「通读了几段几镜、发现并改了什么」。**"""

assert t.count(old) == 1
t = t.replace(old, new)

# 人工项小节改成指向 self-check.md 的硬规矩
old2 = """**脚本只覆盖机械项**（结构/时间/资产锚点/台词引号与语速/密度/景别与切点词/可见性关键词）。下面 8 条必须人工逐镜过，任何一条没做就等于没自检："""
new2 = """**脚本只覆盖机械项**（结构/时间/资产锚点/台词引号与语速/密度/景别与切点词/可见性关键词）。**必须先亲自通读全稿**，再按下表逐镜过，任何一条没做就等于没自检（完整版见 `references/self-check.md`）："""
assert t.count(old2) == 1
t = t.replace(old2, new2)

old3 = "| `references/self-check.md` | 两轮自检清单 + 常见失败对照 | 交付前 |"
new3 = "| `references/self-check.md` | 必须通读 + 两轮自检 + 修正闭环 + 检查表 + 高风险回归 + 武戏专项 + 失败反馈处理 | 每次交付前 |"
assert t.count(old3) == 1
t = t.replace(old3, new3)

open(p, "w", encoding="utf-8").write(t)
print("SKILL updated")
