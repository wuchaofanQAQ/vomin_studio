# -*- coding: utf-8 -*-
import re

# harness
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()
t = t.replace("角色库 ×6 行 / 角色库 ×6 行", "角色库 ×6 行")
t = t.replace("展示草案摘要与写入清单（三张表）", "展示草案摘要与写入清单（两张表）")
t = t.replace("三张表都属同一份清单", "两张表都属同一份清单")
t = t.replace("剧本设定 + 角色库（不产出剧本表", "剧本设定 + 角色库（不产出剧本表")
open(p, "w", encoding="utf-8").write(t)
print("harness 修复:", t.count("角色库 ×6 行"), "处 ×6；三张表剩", t.count("三张表"))

# initializer
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-initializer\SKILL.md"
s = open(p2, encoding="utf-8").read()
s = s.replace("产出**双表数据**：", "产出**角色库数据**：")
# 删掉遗留的 bible 对象（在 角色库 数组结束后多出来的一段）
pat = re.compile(r"\n    \},\n    \{\n      \"name\": \"张三\",\n      \"char_type\": \"核心\",\n      \"basic_info\".*?\n    \}\n  \]\n\}", re.S)
s2, n = pat.subn("\n    }\n  ]\n}", s)
print("initializer bible 块删除:", n)
open(p2, "w", encoding="utf-8").write(s2)
