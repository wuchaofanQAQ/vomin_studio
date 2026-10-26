import re, json, sys
p = sys.argv[1]
lines = open(p, encoding="utf-8").read().splitlines()
cn = lambda s: len(re.sub(r"[^\u4e00-\u9fff]", "", s))
seg = None
for ln in lines:
    m = re.match(r"^## 第(\d+)段", ln)
    if m:
        seg = m.group(1); print(f"\n=== 第{seg}段 ==="); continue
    m = re.match(r"^【镜头(\d+)｜([\d.]+)-([\d.]+)s｜(.+?)】", ln)
    if m:
        d = float(m.group(3)) - float(m.group(2))
        print(f"  镜头{m.group(1)} {m.group(2)}-{m.group(3)}s ({d:g}s) {m.group(4)}"); continue
    m = re.match(r"^【对白\s*([\d.]+)-([\d.]+)s】(.+?)：(.*)$", ln)
    if m:
        d = float(m.group(2)) - float(m.group(1)); n = cn(m.group(4))
        print(f"     对白 {m.group(1)}-{m.group(2)} {n}字 {n/d:.2f}字/秒  {m.group(3)}")
