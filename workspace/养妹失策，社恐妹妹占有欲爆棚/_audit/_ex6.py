import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
m = re.search(r"(?ms)^## (\u3010\u7b2c01\u6bb5.*?)(?=^## \u3010\u7b2c02\u6bb5)", md)
block = "## " + m.group(1).strip()
head = """# \u793a\u4f8b\u6bb5\uff1a30 \u79d2\u7b80\u5355\u6863\uff08\u540d\u79f0\u7248\uff09

> \u7528\u9014\uff1a\u6821\u51c6\u65b0\u683c\u5f0f\u4e0e\u5199\u6cd5\u5bc6\u5ea6\uff1b**\u4e0d\u662f\u5f53\u524d\u5206\u955c\u6570\u636e**\u3002

```text
"""
open(r"skills\drama-segment-generation\references\example-segment.md", "w", encoding="utf-8").write(head + block + "\n```\n")
print("example refreshed")
