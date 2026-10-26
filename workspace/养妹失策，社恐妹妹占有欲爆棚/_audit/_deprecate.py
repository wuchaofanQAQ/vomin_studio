# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\SKILL.md"
t = open(p, encoding="utf-8").read()
reps = [
("R02陈诚（压着火、短促地说）：谁啊？",
 "【对白 00:03.5-00:05】R02陈诚（压着火、短促地说）：谁啊？"),
("| 台词 | 单独成行，`编号+名称（情绪/语气/状态地说）：台词。`，台词逐字 |",
 "| 台词 | 单独成行，行首 `【对白 起-止】`，后接 `编号+名称（情绪/语气/状态地说）：台词。`，台词逐字 |"),
]
for old, new in reps:
    assert t.count(old) == 1, old[:20]
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)

p2 = r"skills\director-segment-prompt\SKILL.md"
t2 = open(p2, encoding="utf-8").read()
h = "# Director Segment Prompt — 导演级分段视频提示词"
note = h + "\n\n> **已停用（默认不调用）**：B1 由 `script-to-prompt-30`（剧本转提示词 3.0）接管。本 skill 保留作回退与对照，仅当用户明确要求旧版 7 块格式时使用；两套格式不得在同一集混用。"
assert t2.count(h) == 1
t2 = t2.replace(h, note, 1)
open(p2, "w", encoding="utf-8").write(t2)
print("ok")
