# -*- coding: utf-8 -*-
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
t = t.replace('"""检查 6 张标准表是否齐全，缺失的自动创建。返回完整映射。"""',
              '"""检查标准表是否齐全（含道具库），缺失的自动创建。返回完整映射。"""')
t = t.replace('"""创建一个新项目的完整飞书多维表格（7 张表 + 全部字段 + 公开权限）。',
              '"""创建一个新项目的完整飞书多维表格（全部标准表 + 字段 + 公开权限）。')
open(p, "w", encoding="utf-8").write(t)
print("docstrings updated")
