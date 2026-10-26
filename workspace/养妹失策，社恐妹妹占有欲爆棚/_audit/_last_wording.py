# -*- coding: utf-8 -*-
p = r"skills\drama-initializer\references\character-extract-init.md"
t = open(p, encoding="utf-8").read()
t = t.replace("三视图出图", "资产图出图").replace("供三视图", "供资产图")
open(p, "w", encoding="utf-8").write(t)
print("fixed")
