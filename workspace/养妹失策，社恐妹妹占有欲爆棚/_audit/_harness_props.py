# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()
old = '''   - 新增角色 → 走角色档案 + 三视图补生成'''
new = '''   - 新增角色 → 走角色档案 + 三视图补生成
   - 新增道具 → 差分比对 `道具库`；缺的列入待补道具（手工补录或 `generate --target 道具库:名`），不阻塞分镜评审'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("harness updated")
