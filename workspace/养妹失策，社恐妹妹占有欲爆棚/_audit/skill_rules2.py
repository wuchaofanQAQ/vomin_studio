# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "2. **先绑资产，再写段。** 开工先读资产库，把本集用到的资产逐一对上真实记录：有行有图=可绑；有行无图=可用描述、标待出图；库里没有=**【待补，未读取】**，不许自编名称或编号充数。资产表不是出场名单，每段只锁真正参与本段的。"
new = "2. **先取料、再绑资产、最后写段。** 取料顺序固定：剧本表（含 `涉及资产`、`对应原小说章节`）→ 小说表对应章节 → 资产库（`描述` / `备注` / `文件路径`，**先打开图看**）。外观一律**以真实图片为准**（`描述` 只是当初的出图提示词，会跑偏）；`备注` 里的反打关系、同源图、近/中/远景必须照它写。有行有图=可绑；有行无图=标待出图；库里没有=**【待补，未读取】**，不许自编名称或编号充数。资产表不是出场名单，每段只锁真正参与本段的。"
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("铁律 2 已更新")

# self-check 补两条
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\references\self-check.md"
s = open(p2, encoding="utf-8").read()
anchor = "## 第一轮"
add = """## 第零步·二 — 图与备注对过了吗

- [ ] 每个入画资产，**都亲眼打开过它的图片**（不是只读了 `描述`）
- [ ] 图片里真实的长相、服装、家具摆放、光线，和正文写的一致
- [ ] `备注` 里的反打关系 / 同源图 / 近中远景，正文的空间层次照它写了
- [ ] 光影不匹配（图是白天、戏是傍晚）时，没有用文字硬压光，而是先补图

## 情绪落点 — 这场戏的劲儿给了吗

- [ ] 每一场能说出「谁想要什么、谁在挡、谁退了一步」
- [ ] 人物在藏的东西，有对应的镜头（躲视线 / 手部 / 呼吸 / 停顿），不是全靠台词
- [ ] 原文里最扎的那句或那个动作，没有在压缩时丢掉

"""
assert s.count(anchor) == 1
s = s.replace(anchor, add + anchor)
open(p2, "w", encoding="utf-8").write(s)
print("self-check 已补两节")
