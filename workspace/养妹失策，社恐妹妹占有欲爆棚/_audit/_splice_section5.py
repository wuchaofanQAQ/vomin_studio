# -*- coding: utf-8 -*-
import io
p = r"skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()
start_marker = "## 5. 分段分镜与视频提示词"
end_marker = "## 交接铁律"
i = t.index(start_marker)
j = t.index(end_marker)
new = open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_new_section_5.md", encoding="utf-8").read()
t = t[:i] + new + t[j:]
open(p, "w", encoding="utf-8").write(t)
print("replaced", j - i, "->", len(new))
