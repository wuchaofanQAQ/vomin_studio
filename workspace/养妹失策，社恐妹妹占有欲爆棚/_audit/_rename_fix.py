# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:30]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"CLAUDE.md", [
("本项目是 AI 短剧生产流水线：7 个 skill", "本项目是 AI 短剧生产流水线：6 个 skill"),
("| director-segment-prompt（回退） | `skills/director-segment-prompt/SKILL.md` | 旧版 7 块分镜格式，默认不调用 |\n", ""),
])

rep(r"skills\ai-drama-harness\SKILL.md", [
("6. **回退**：只有用户明确要求旧版 7 块结构时，才改用 `director-segment-prompt`；两套格式不得在同一集混用（旧格式 `【对白 0-2s】陈诚：…`，新格式 `【对白 00:00-00:02】R02陈诚（…地说）：…`）。\n", ""),
("| `director-segment-prompt` | 回退 | 旧版 7 块分镜格式；默认不调用，仅用户明确要求时使用 |\n", ""),
])

rep(r"skills\drama-segment-generation\SKILL.md", [
("# 剧本转提示词 3.0", "# 剧集分段生成（剧本转提示词 3.0）"),
("- **旧 skill `director-segment-prompt` 保留但不再默认调用**（回退、对照用）。两套格式不兼容，不要混用块结构。\n", ""),
])

rep(r"skills\drama-segment-generation\references\project-adaptation.md", [
("| 项 | 旧 director-segment-prompt | 新 3.0 |", "| 项 | 旧 7 块格式 | 3.0 |"),
])
print("done")
