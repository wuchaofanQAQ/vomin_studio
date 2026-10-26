# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

# 1) 恢复段头与空行
t = re.sub(r"(?m)^(【第\d+段｜)", r"## \1", t)
t = re.sub(r"(?m)^(【镜头\d+｜)", r"\n\1", t)
t = re.sub(r"(?m)^(【本段资产锁定】|【本段现场生成】|【本段整体基准】|【本段初始空间】|【本段终态】)", r"\n\1", t)
t = re.sub(r"\n{3,}", "\n\n", t)
open(f, "w", encoding="utf-8").write(t.strip() + "\n")
print("段头/空行已恢复:", t.count("## 【第"))
