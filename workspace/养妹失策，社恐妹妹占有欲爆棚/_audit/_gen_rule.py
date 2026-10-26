# -*- coding: utf-8 -*-
p = r"skills\drama-asset-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "**本 skill 只负责\"怎么把描述变成图\"**：选题、套版式、写提示词、出图、验收。资产有什么、叫什么，由 `drama-asset-extraction` 决定。"
new = old + "\n\n> **生图必须逐次确认**：每次调用 `generate`（包括重抽、补抽、换版式）之前，单独列出「资产名 / 版式 / 比例 / 张数」，等用户明确说\"确认\"再调用。没有确认就停在提示词草案，不许直接打接口。写 `gen_prompt` 也算写操作，一并列入确认清单。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("rule added")
