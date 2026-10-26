# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()
reps = [
("| `python cli.py migrate-schema <路径> --dry-run` | 预览存量表迁移计划（剧集表→剧本表、补字段） | 否 |",
 "| `python cli.py migrate-schema <路径> --dry-run` | 预览存量表迁移计划（剧集表→剧本表、补字段、补缺失表） | 否 |"),
("| `python cli.py migrate-schema <路径>` | 执行存量表迁移 | **是** |",
 "| `python cli.py migrate-schema <路径>` | 执行存量表迁移（含补齐「道具库」等缺失标准表） | **是** |"),
]
for old, new in reps:
    assert t.count(old) == 1, old[:20]
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("manual CLI rows updated")
