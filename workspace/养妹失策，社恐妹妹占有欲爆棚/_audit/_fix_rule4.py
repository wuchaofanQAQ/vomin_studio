# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "4. **台词逐字、单独成行、括号里必须有\"说\"。** `R01沈幼怡（压着声音、断续地说）：……`；画外音写 `R02陈诚画外音（门内压低地说）：……` 并给方向。"
new = "4. **台词逐字、单独成行、括号里必须有\"说\"。** `【对白 00:01-00:02】R01沈幼怡（压着声音、断续地说）：……`；画外音写 `【对白 00:09-00:10.5】R02陈诚画外音（门内压低地说）：……` 并给方向。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("ok")
