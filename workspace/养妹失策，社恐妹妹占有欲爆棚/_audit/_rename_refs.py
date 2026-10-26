# -*- coding: utf-8 -*-
import os, re
files = [
 r"skills\script-to-scene-assets\SKILL.md",
 r"skills\AI短剧生产底座使用手册.md",
 r"skills\ai-drama-harness\references\pipeline.md",
 r"skills\ai-drama-harness\references\data-contracts.md",
 r"skills\ai-drama-harness\references\checkpoint-protocol.md",
 r"skills\drama-initializer\SKILL.md",
 r"skills\novel-to-script\SKILL.md",
 r"skills\novel-to-script\references\script-format.md",
 r"skills\novel-to-character-assets\references\bible-template.md",
]
for f in files:
    t = open(f, encoding="utf-8").read()
    n = t.count("director-segment-prompt")
    t = t.replace("director-segment-prompt", "script-to-prompt-30")
    open(f, "w", encoding="utf-8").write(t)
    print(f"{f}: {n} replaced")
