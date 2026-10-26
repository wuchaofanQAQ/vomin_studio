# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:36]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\drama-segment-generation\references\self-check.md", [
("| 8 | 段长 | 按难度 6~30 秒；参考图 ≤5 张；换场景/多人/打斗已缩段 | 为凑 30 秒加镜头；5 人戏压进 30 秒 |",
 "| 8 | 段长 | 按难度 6~30 秒；换场景/多人/打斗已缩段（参考图不设上限） | 为凑 30 秒加镜头；5 人戏压进 30 秒 |"),
])
rep(r"skills\drama-segment-generation\references\core-principles.md", [
("| **生产态** | 调模型出图 / 配音 / 出视频 | 18 项必须全 PASS，且 preflight 必须 0 问题 |",
 "| **生产态** | 调模型出图 / 出视频 | 自检必须全 PASS，且 preflight 必须 0 问题 |"),
])
rep(r"skills\drama-segment-generation\references\dialogue-and-audio.md", [
("- 屏幕文字**不进 `dialogue`、不配音**；打字声/震动声用（音效）承担",
 "- 屏幕文字**不进 `dialogue`、不发声**；打字声/震动声用（音效）承担。本项目不做 TTS，对白由视频模型原生发声"),
])
rep(r"skills\drama-segment-generation\references\preflight-checklist.md", [
("## E2. 镜头写厚与块间一致", "## E2. 镜头写厚与段间一致"),
])
print("done")
