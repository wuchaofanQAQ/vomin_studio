# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "| 文戏 | 稳定中景/近景/过肩/缓推/微横移/焦点转移；目光、呼吸、停顿、手指嘴角 | 环绕、甩镜、爆炸特效 |"
new = """| 文戏 | 稳定中景/近景/过肩/缓推/微横移/焦点转移；目光、呼吸、停顿、手指嘴角 | 环绕、甩镜、爆炸特效 |
| 表演 | 用可拍动作写情绪：捧脸、抹泪、唇角发颤、眼神稳住；台词前后都带准备与余势 | 写"难过""愤怒""很感动" |
| 切点 | 写成「切在…时」：谁仍处于什么状态、手停在哪儿 | 只写「落幅停在他脸上」 |
| 机位 | 写上「随…下摇/上摇/轻推」，机位跟着表演走 | 全段只写「镜头固定」 |"""
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("cheatsheet updated")
