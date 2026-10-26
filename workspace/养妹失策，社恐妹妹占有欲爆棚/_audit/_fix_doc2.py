# -*- coding: utf-8 -*-
import re, os
for f in [r"skills\drama-segment-generation\SKILL.md",
          r"skills\drama-segment-generation\references\project-adaptation.md"]:
    t = open(f, encoding="utf-8").read()
    n = t.count("『") + t.count("』")
    t = t.replace("『", "「").replace("』", "」")
    open(f, "w", encoding="utf-8").write(t)
    print(f, "quotes fixed", n)

# 示例段换成 v14 p01
md = open(os.path.join(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚", "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
m = re.search(r"(?ms)^## (\u3010\u7b2c01\u6bb5.*?)(?=^## \u3010\u7b2c02\u6bb5)", md)
block = "## " + m.group(1).strip()
head = """# \u793a\u4f8b\u6bb5\uff1a30 \u79d2\u7b80\u5355\u6863\uff08\u540d\u79f0\u7248\uff09

> \u7528\u9014\uff1a\u6821\u51c6\u65b0\u683c\u5f0f\uff08\u9501\u5b9a `\u3010\u540d\u3011\uff1a{...}`\u3001\u65f6\u95f4\u8f74 `[0s-2s]`\u3001\u6b63\u6587 `\u3010\u540d\u3011`\u3001\u53f0\u8bcd `\u300c\u300d`\uff09\u4e0e\u5199\u6cd5\u5bc6\u5ea6\uff1b**\u4e0d\u662f\u5f53\u524d\u5206\u955c\u6570\u636e**\u3002

```text
"""
open(r"skills\drama-segment-generation\references\example-segment.md", "w", encoding="utf-8").write(head + block + "\n```\n")
print("example updated")
