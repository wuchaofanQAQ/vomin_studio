import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v13.md"), encoding="utf-8").read()
m = re.search(r"(?ms)^## (\u3010\u7b2c01\u6bb5.*?)(?=^## \u3010\u7b2c02\u6bb5)", md)
block = "## " + m.group(1).strip()
head = """# \u793a\u4f8b\u6bb5\uff1a30 \u79d2\u7b80\u5355\u6863\uff084.2 \u5bc6\u5ea6\u7248\uff09

> \u7528\u9014\uff1a\u6821\u51c6 4.2 \u683c\u5f0f\u3001\u5199\u6cd5\u5bc6\u5ea6\u4e0e\u53f0\u8bcd\u5199\u6cd5\uff1b**\u4e0d\u662f\u5f53\u524d\u5206\u955c\u6570\u636e**\u3002\u8d44\u4ea7\u540d\u53d6\u81ea\u672c\u9879\u76ee\u7b2c 1 \u96c6\uff0c\u53ef\u76f4\u63a5\u7528\u6821\u9a8c\u811a\u672c\u8dd1\u901a\u3002
> \u6b63\u6587\u4eba\u7269\u4e00\u5f8b\u5199 `\u7f16\u53f7+\u540d\u79f0`\uff08`R01\u6c88\u5e7c\u6021`\uff09\uff0c\u4e0d\u52a0\u3010\u3011\uff1b\u53f0\u8bcd\u7528\u300c\u300d\uff0c\u884c\u9996\u662f\u65f6\u95f4\u7a97\uff1b\u6bcf\u955c\u4ee5\u300c\u5207\u5728\u2026\u65f6\u300d\u6536\u5c3e\u3002

```text
"""
open(r"skills\drama-segment-generation\references\example-segment.md", "w", encoding="utf-8").write(head + block + "\n```\n")
print("example updated to v13 p01")
