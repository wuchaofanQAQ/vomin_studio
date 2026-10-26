import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), encoding="utf-8").read()
m = re.search(r"(?ms)^## (【第01段.*?)(?=^## 【第02段)", md)
block = "## " + m.group(1).strip()
head = """# 示例段：30 秒简单档（4.2 密度版）

> 用途：校准 4.2 格式、写法密度与台词写法；**不是当前分镜数据**。资产名取自本项目第 1 集，可直接用校验脚本跑通。
> 正文人物一律写 `编号+名称`（`R01沈幼怡`），不加【】；台词用「」，行首是时间窗。

```text
"""
open(r"skills\drama-segment-generation\references\example-segment.md", "w", encoding="utf-8").write(head + block + "\n```\n")
print("example rebuilt")
