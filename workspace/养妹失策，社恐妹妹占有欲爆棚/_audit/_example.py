import shutil, re
src = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_p01_dense.md"
dst = r"skills\drama-segment-generation\references\example-segment.md"
body = open(src, encoding="utf-8").read().strip()
head = """# 示例段：30 秒简单档（4.2 密度版）

> 用途：校准 4.2 格式、写法密度与台词写法；**不是当前分镜数据**。资产名取自本项目第 1 集，可直接用校验脚本跑通。
> 正文人物一律写 `编号+名称`（`R01沈幼怡`），不加【】；台词用「」，行首是时间窗。

```text
"""
open(dst, "w", encoding="utf-8").write(head + body + "\n```\n")
print("example replaced with dense sample")
