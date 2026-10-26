# -*- coding: utf-8 -*-
import re, sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()
ws = Workspace(base)

parts = re.split(r"(?m)^(## 【第\d+段.*?】)[ \t]*$", t.replace("\r\n", "\n"))
ok = True
i = 1
while i < len(parts):
    head, body = parts[i], parts[i+1]
    dur = int(re.search(r"\[0s-(\d+)s\]", head).group(1))
    shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body)
    print(f"\n{head}")
    prev = 0.0
    for no, a, b, title, txt in shots:
        a, b = float(a), float(b)
        gap = abs(a - prev) > 1e-6
        grid = abs((b - a) * 2 - round((b - a) * 2)) < 1e-6
        dlg = [ln for ln in txt.split("\n") if ln.startswith("[")]
        rate = ""
        for d in dlg:
            mm = re.search(r"「(.+)」", d)
            if mm:
                ch = len(re.findall(r"[\u4e00-\u9fff]", mm.group(1)))
                rate = f" {ch}/{b-a:.1f}={ch/(b-a):.1f}字/秒"
                if ch / (b - a) > 5.3: ok = False; rate += " ⚠超速"
        flags = []
        if gap: flags.append("断档"); ok = False
        if not grid: flags.append("非0.5"); ok = False
        if b > dur + 1e-6: flags.append("越界"); ok = False
        print(f"  {int(no):02d} {a:g}-{b:g} ({b-a:g}s) {title}{rate} {' '.join(flags)}")
        prev = b
    if abs(prev - dur) > 1e-6:
        print(f"  ⚠ 末镜 {prev} ≠ 段长 {dur}"); ok = False
    p, refs, missing, _, _ = ws.expand_prompt(body)
    print(f"  参考图 {len(refs)} 缺失 {len(missing)}")
    if missing: ok = False; print("   缺:", missing)
    i += 2
print("\n结论:", "全部通过" if ok else "有问题")
