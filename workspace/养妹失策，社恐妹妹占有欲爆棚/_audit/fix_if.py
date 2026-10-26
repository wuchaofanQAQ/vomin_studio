# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()
old = '        elif kind == "资产库":'
new = '        if kind == "资产库":'
assert c.count(old) == 1
open(p, "w", encoding="utf-8").write(c.replace(old, new))
print("fixed if/elif")
