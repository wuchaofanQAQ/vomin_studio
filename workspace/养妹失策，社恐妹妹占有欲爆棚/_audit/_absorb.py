# -*- coding: utf-8 -*-
import re, os, shutil
src = r"docs\director-segment-prompt\references"
dst = r"skills\drama-segment-generation\references"
files = ["cinema-foundation", "shot-grammar", "camera-space-and-visibility",
         "shot-richness-and-pitfalls", "physics-and-scale", "action-impact-vfx-crowd",
         "dialogue-and-audio", "continuity-and-anchoring", "seedance-25-rules",
         "director-self-review", "iteration-manual", "preflight-checklist", "core-principles"]
header = ("> 来源：旧 `docs/director-segment-prompt`，已并入 4.2。**格式与流程以 `SKILL.md` 的 4.2 骨架为准**，"
          "本文只保留工艺细节；与 4.2 冲突处一律按 4.2 执行。\n\n")
total = 0
for f in files:
    s = os.path.join(src, f + ".md")
    d = os.path.join(dst, f + ".md")
    t = open(s, encoding="utf-8").read()
    n0 = len(t)
    t = t.replace("【资产锁定】", "【本段资产锁定】")
    t = t.replace("【本段风格】", "【本段整体基准】")
    t = t.replace("【本段初始空间基准】", "【本段初始空间】")
    t = t.replace("check_storyboard.py", "check_segment_prompt.py")
    t = t.replace("【对白 起止时间】角色[（位置）|·画外声|内心独白][，语气标注]：台词",
                  "起-止，编号+名称（语气说）：『台词』（行首时间窗）")
    t = t.replace("`【对白 起-止】`", "行首时间窗")
    t = t.replace("【对白 起-止】", "行首时间窗")
    t = t.replace("script-to-prompt-30", "drama-segment-generation")
    t = t.replace("剧本转提示词 3.0", "剧本转提示词 4.2")
    t = t.replace(" 3.0 ", " 4.2 ")
    open(d, "w", encoding="utf-8").write(header + t)
    total += 1
    print(f"{f}.md  {n0} -> {len(t)+len(header)}")
print("copied:", total)
