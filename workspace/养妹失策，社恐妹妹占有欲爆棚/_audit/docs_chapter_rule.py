# -*- coding: utf-8 -*-
import re

# 1) drama-asset-extraction Step 0
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-extraction\SKILL.md"
t = open(p, encoding="utf-8").read()
t = t.replace(
"python cli.py read $WS --table 剧本表 --episode N --context 1     # N-1/N/N+1 的 script（不含小说原文）\npython cli.py read $WS --table 小说表    # 小说原文（按对应原小说章节取用）",
"python cli.py read $WS --table 剧本表 --episode N --context 1     # 拿到本集 script 与「对应原小说章节」，如 1,2\npython cli.py read $WS --table 小说表 --chapter 1,2              # 只读这几章原文，不通读全本")
t = t.replace(
"- `--with-novel` 只给当前集 N，**不与 `--context` 同用**；`小说内容` 为空（成品剧本）就只用剧本。",
"- 小说原文只按 `对应原小说章节` 精确取（`--chapter 1,2`），**禁止通读小说表全本**；该字段为空（成品剧本）就只用剧本。")
open(p, "w", encoding="utf-8").write(t)
print("extraction 已更新")

# 2) ai-drama-harness
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\ai-drama-harness\SKILL.md"
h = open(p2, encoding="utf-8").read()
h = h.replace(
"python cli.py read $WS --table 剧本表 --episode N --with-novel   # 仅当前集：小说原文，补长相/空间",
"python cli.py read $WS --table 小说表 --chapter <对应原小说章节>   # 只读本集用到的几章原文，补长相/空间")
h = h.replace(
"**剧本表只读 N-1、N、N+1 共 3 集，严禁全量读入，严禁加 `--with-novel`**",
"**剧本表只读 N-1、N、N+1 共 3 集，严禁全量读入；小说原文按 `对应原小说章节` 用 `--chapter` 精确取，禁止通读小说表**")
open(p2, "w", encoding="utf-8").write(h)
print("harness 已更新")

# 3) novel-to-drama
p3 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\novel-to-drama\SKILL.md"
n = open(p3, encoding="utf-8").read()
n = n.replace("- **不要带 `--with-novel`**：小说原文很长，承接只需要转化后的剧本",
              "- **不要再读小说表全本**：承接只需要转化后的剧本；需要原文时按 `对应原小说章节` 用 `--chapter` 精确取")
open(p3, "w", encoding="utf-8").write(n)
print("novel-to-drama 已更新")
