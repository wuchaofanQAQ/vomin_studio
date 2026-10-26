# -*- coding: utf-8 -*-
import re, sys, importlib.util

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"

# 1) 从飞书恢复
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
import os
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
ws = Workspace(base)
shots = ws.load_storyboard()
parts = []
for s in shots:
    p = s["prompt"].strip()
    parts.append(p if p.startswith("## ") else "## " + p)
f = os.path.join(base, "drafts", "ep01m_storyboard_v1.md")
open(f, "w", encoding="utf-8").write("\n\n".join(parts) + "\n")
print("restored", len(parts))

# 2) 取待用扩写文本（从 expand_seg.py 里 import NEW，SEG=1）
spec = importlib.util.spec_from_file_location("es", os.path.join(base, "_audit", "expand_seg.py"))
src = open(os.path.join(base, "_audit", "expand_seg.py"), encoding="utf-8").read()
# 抽出 NEW = {...} 部分
start = src.index("NEW = {")
end = src.index("\n}\n", start) + 2
ns = {}
exec(src[start:end], ns)
NEW = ns["NEW"]

# 3) 只改第 1 段：遇到段头后开始替换
lines = open(f, encoding="utf-8").read().split("\n")
out, seg = [], 0
i = 0
while i < len(lines):
    ln = lines[i]
    mseg = re.match(r"^## 【第(\d+)段", ln)
    if mseg:
        seg = int(mseg.group(1))
    out.append(ln)
    m = re.match(r"^【镜头(\d+)｜", ln)
    if m and i + 1 < len(lines):
        no = int(m.group(1))
        if seg == 1 and no in NEW:
            out.append(NEW[no])
            i += 2
            continue
    i += 1
open(f, "w", encoding="utf-8").write("\n".join(out))
print("第1段扩写完成")
