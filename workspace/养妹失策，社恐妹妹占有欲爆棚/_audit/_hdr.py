# -*- coding: utf-8 -*-
import glob, os
old = "> 来源：旧 `docs/director-segment-prompt`，已并入 4.2。**格式与流程以 `SKILL.md` 的 4.2 骨架为准**，本文只保留工艺细节；与 4.2 冲突处一律按 4.2 执行。"
new = ("> 来源：旧 `docs/director-segment-prompt`，已并入 4.2。**格式与流程以 `SKILL.md` 的 4.2 骨架为准**，本文只保留工艺细节；与 4.2 冲突处一律按 4.2 执行。\n"
       "> 注意：旧文示例里的 `【沈幼怡】` 是 7 块写法，**4.2 一律写 `R01沈幼怡`**（不带【】、不写裸名）；旧文的 `【对白 起-止】` 行首在 4.2 里就是行首时间窗。")
n = 0
for f in glob.glob(r"skills\drama-segment-generation\references\*.md"):
    t = open(f, encoding="utf-8").read()
    if old in t:
        open(f, "w", encoding="utf-8").write(t.replace(old, new))
        n += 1
print("headers updated:", n)
