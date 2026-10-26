# -*- coding: utf-8 -*-
import re

# 1) novel-to-drama：屏幕文字改口径
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\novel-to-drama\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "- **字幕与屏幕文字**：手机短信、微信、打字内容一律按 `references/script-format.md` 的三种字幕写法标注，"
if old in t:
    new = "- **屏幕文字**：手机短信、微信、打字内容一律写进正文的动作/画面描述里（写成“屏幕上打着……”），**不要单独起一行字幕**；剧本阶段可用 `（字幕·手机）` 只是记录，分镜阶段必须并进正文——"
    t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    print("novel-to-drama 已更新")

# 2) drama-asset-extraction 的表格行
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-extraction\SKILL.md"
s = open(p2, encoding="utf-8").read()
s = s.replace("| `（字幕…）` | 屏幕字、手机字、时间卡 |",
              "| `（字幕…）` | 仅剧本阶段的记录；分镜里屏幕字要写进正文 |")
open(p2, "w", encoding="utf-8").write(s)
print("asset-extraction 已更新")

# 3) drama-segment-generation：加一条屏幕文字规则
p3 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
g = open(p3, encoding="utf-8").read()
if "屏幕文字规则" not in g:
    anchor = "## 场景锁定（防穿帮）"
    add = '''## 屏幕文字规则（手机/微信/打字）

屏幕上的字是**画面内容**，不是字幕：

- 必须写进镜头正文：「微信聊天框里一行被打到最大的字——“妈妈说，给你发过信息了。”，末尾一个句号，光标还在闪」
- **禁止**另起一行 `（字幕·手机）……`
- 社恐角色不说话，靠"打完字 → 翻转手机 → 屏幕对着对方"完成对话，这个动作链要写全
- 需要观众看清字时，单独给一个屏幕正面的特写镜头

'''
    g = g.replace(anchor, add + anchor)
    open(p3, "w", encoding="utf-8").write(g)
    print("segment-generation 已加屏幕文字规则")
