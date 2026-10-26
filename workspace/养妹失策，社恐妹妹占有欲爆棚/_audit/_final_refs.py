# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:30]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\novel-to-script\SKILL.md", [
("下游衔接：`script-to-scene-assets` 读 `完整剧本` 定场景、并读当前章 `小说内容` 补空间细节；`novel-to-character-assets` 读 `小说内容` 抽角色；`script-to-prompt-30` 只读 `完整剧本` 拆分镜。",
 "下游衔接：`script-asset-extraction` 读 `完整剧本` 定角色/场景/道具，并读当前章 `小说内容` 补长相与空间细节；`script-to-prompt-30` 只读 `完整剧本` 拆分镜。"),
])

rep(r"skills\drama-initializer\references\character-extract-init.md", [
("6. 详细字段模板可对照 `novel-to-character-assets/references/bible-template.md`",
 "6. 详细字段模板可对照 `script-asset-extraction/references/character-bible.md`"),
])

files = [
 r"skills\ai-drama-harness\references\data-contracts.md",
 r"skills\novel-to-script\SKILL.md",
 r"skills\novel-to-script\references\script-format.md",
 r"skills\drama-initializer\SKILL.md",
 r"skills\drama-initializer\references\setting-template.md",
 r"skills\drama-initializer\references\character-extract-init.md",
 r"skills\drama-initializer\references\script-intake.md",
 r"skills\director-segment-prompt\references\asset-binding-and-cli.md",
]
for f in files:
    t = open(f, encoding="utf-8").read()
    n = t.count("script-to-scene-assets") + t.count("novel-to-character-assets")
    t = t.replace("script-to-scene-assets", "script-asset-extraction").replace("novel-to-character-assets", "script-asset-extraction")
    open(f, "w", encoding="utf-8").write(t)
    print(f"{f}: {n} replaced")

# CLAUDE.md skill 数量
p = r"CLAUDE.md"
t = open(p, encoding="utf-8").read()
t = t.replace("本项目是 AI 短剧生产流水线：9 个 skill", "本项目是 AI 短剧生产流水线：8 个 skill")
open(p, "w", encoding="utf-8").write(t)
print("count updated")
