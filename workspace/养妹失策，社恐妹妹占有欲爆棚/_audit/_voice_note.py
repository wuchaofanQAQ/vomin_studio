# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "| 音色 | 需要固定音色时，锁定区单起一行 `音频参考：【R01沈幼怡：{音色库：沈幼怡-清冷少女}】`；音色库里没有这一行就不要写（本项目不做 TTS） |"
new = "| 音色 | 需要固定音色时直接写 `{音色库：音色名}`（建议单起一行 `音频参考：【R01沈幼怡：{音色库：沈幼怡-清冷少女}】`）；CLI 收集该音频作为 `reference_audio`；音色库里没有这一行就不要写（本项目不做 TTS） |"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("ok")
