# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = '当用户说"剧本转提示词""3.0""拆分镜""分镜脚本""视频提示词""导演级提示词""30秒分段""资产锁定""镜头提示词"时使用。'
new = '当用户说"剧集分段""分段生成""剧本转提示词""3.0""拆分镜""分镜脚本""视频提示词""导演级提示词""30秒分段""资产锁定""镜头提示词"时使用。'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))

p = r"CLAUDE.md"
t = open(p, encoding="utf-8").read()
old = "| 剧本转提示词、3.0、拆分镜、分镜脚本、视频提示词、导演级提示词、30秒分段 |"
new = "| 剧集分段、分段生成、剧本转提示词、3.0、拆分镜、分镜脚本、视频提示词、30秒分段 |"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("triggers updated")
