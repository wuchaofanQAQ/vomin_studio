# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
dst = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\references\example-segment.md"
md = open(base + r"\drafts\ep01_storyboard_v14.md", encoding="utf-8").read()
m = re.search(r"(?ms)^## (【第01段.*?)(?=^## 【第02段)", md)
block = "## " + m.group(1).strip()
head = """# 示例段：30 秒简单档（名称版）

> 用途：校准新格式（锁定 `【名】：{...}`、时间轴 `[0s-2s]`、正文 `【名】`、台词 `「」`）与写法密度；**不是当前分镜数据**。

```text
"""
open(dst, "w", encoding="utf-8").write(head + block + "\n```\n")
print("example refreshed")
