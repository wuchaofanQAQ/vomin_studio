# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
t = open(p, encoding="utf-8").read()
old = '"资产库": ("load_assets_lib", "名称", ["file_path"]),'
new = '"资产库": ("load_assets_lib", "name", ["file_path"]),'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("key field fixed")
