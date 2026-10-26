# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:24]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\script-asset-extraction\SKILL.md", [
("- 画风词最多一个（如\"写实\"），全局画风由 `剧本设定` 负责；",
 "- 画风词最多一个（如\"写实\"）；全局画风由 `剧本设定` 负责——出资产图时 CLI 会自动给 ≤120 字的短提示词追加全局画风，不用把画风塞进 50 字里；"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("| `prompt` | 生成提示词 | **≤50 字、单句、不分节**；写入时 CLI 自动映射到「生成提示词」 |",
 "| `prompt` | 生成提示词 | **≤50 字、单句、不分节**；写入时 CLI 自动映射到「生成提示词」，出图时自动追加全局画风 |"),
("| `prompt` → `gen_prompt` | 生成提示词 | **≤50 字、单句、不分节**；CLI 写入时自动映射 |",
 "| `prompt` → `gen_prompt` | 生成提示词 | **≤50 字、单句、不分节**；CLI 写入时自动映射，出图时自动追加全局画风 |"),
])
print("docs updated")
