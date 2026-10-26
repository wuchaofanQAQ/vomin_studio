# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()
old = "| `prompt` | 生成提示词 | **≤50 字、单句、不分节** |\n| `bible.*` | 角色档案 6 模块 | `voice_desc` **必须有**（TTS 用） |"
new = "| `prompt` | 生成提示词 | **≤50 字、单句、不分节**；写入时 CLI 自动映射到「生成提示词」 |\n| `bible.*` | 角色档案 6 模块 | `voice_desc` **必须有**（TTS 用） |"
assert t.count(old) == 1
t = t.replace(old, new)
old2 = "| `prompt` → `gen_prompt` | 生成提示词 | **≤50 字、单句、不分节** |"
new2 = "| `prompt` → `gen_prompt` | 生成提示词 | **≤50 字、单句、不分节**；CLI 写入时自动映射 |"
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("mapping notes added")
