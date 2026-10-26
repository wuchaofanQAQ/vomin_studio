# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:30]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\SKILL.md", [
("python skills/script-to-prompt-30/scripts/check_segment_prompt.py workspace/{剧名}/drafts/ep01_storyboard_v3.md --target 30",
 "python skills/script-to-prompt-30/scripts/check_segment_prompt.py workspace/{剧名}/drafts/ep01_storyboard_v3.md"),
])
rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("3. 跑 `python skills/script-to-prompt-30/scripts/check_segment_prompt.py <草稿> --target 30`，错误必须为 0",
 "3. 跑 `python skills/script-to-prompt-30/scripts/check_segment_prompt.py <草稿>`，错误必须为 0（脚本按复杂度算段长上限；确需固定段长才加 `--target`）"),
])
rep(r"skills\script-to-prompt-30\references\project-adaptation.md", [
("[--target 30]", "[--target 秒数]"),
])
rep(r"skills\script-to-prompt-30\SKILL.md", [
("- 段内必须严格覆盖 `00:00 → 本段时长`；段 ID `ep{两位集号}_p{两位段序}`（如 `ep10_p05`），与飞书分镜表主键一致。",
 "- 段内必须严格覆盖 `00:00 → 本段时长`；段 ID `ep{两位集号}_p{两位段序}`（如 `ep10_p05`），与飞书分镜表主键一致。\n- 校验脚本按同一套标准兜底：复杂度评分 0 → 30 秒上限，1~2 → 24，3~4 → 20，≥5 → 15；参考图 >5 张直接报错。评分只看场景数、角色数、参考图数、特效/群像有无，动作密度由你自己判断。"),
])
rep(r"skills\script-to-prompt-30\references\example-segment.md", [
("# 示例段：30 秒完整格式",
 "# 示例段：简单档 30 秒（单场景、两人、无特效）"),
])
print("done")
