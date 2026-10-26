# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()
old = '| 拆分镜并出视频提示词 | "拆分镜 / 分镜脚本 / 出片提示词 / CLIP" | script-to-prompt-30 |'
new = '| 拆分镜并出视频提示词（3.0） | "剧本转提示词 / 3.0 / 拆分镜 / 分镜脚本 / 视频提示词 / 30秒分段" | script-to-prompt-30 |'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("manual updated")
