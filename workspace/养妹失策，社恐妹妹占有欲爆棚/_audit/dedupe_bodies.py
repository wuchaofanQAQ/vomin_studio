# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
lines = open(f, encoding="utf-8").read().split("\n")
out, buf, i = [], [], 0
while i < len(lines):
    ln = lines[i]
    if re.match(r"^【镜头\d+｜", ln):
        # 收集该镜头直到空行/台词/下一镜
        j = i + 1
        bodies = []
        while j < len(lines) and lines[j].strip() and not lines[j].startswith("【镜头") and not lines[j].startswith("["):
            bodies.append(lines[j]); j += 1
        out.append(ln)
        if bodies:
            out.append(bodies[-1])
        i = j
        continue
    out.append(ln); i += 1
open(f, "w", encoding="utf-8").write("\n".join(out))
print("重复正文已清理")
