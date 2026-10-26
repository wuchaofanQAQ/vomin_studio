# -*- coding: utf-8 -*-
p = r"skills\drama-initializer\references\character-extract-init.md"
t = open(p, encoding="utf-8").read()
old = "6. 详细字段模板可对照 `script-asset-extraction/references/character-bible.md`"
new = "6. 详细字段模板见 `ai-drama-harness/references/data-contracts.md` 第 1c 节"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("fixed dangling bible ref")
