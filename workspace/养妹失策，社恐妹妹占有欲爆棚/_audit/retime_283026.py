# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

T2 = [(0,2),(2,4),(4,8),(8,9.5),(9.5,11),(11,12.5),(12.5,14),(14,15.2),(15.2,20.7),
      (20.7,22.2),(22.2,25.2),(25.2,26.4),(26.4,29.4),(29.4,30)]
T3 = [(0,2),(2,4.5),(4.5,6.5),(6.5,9),(9,11.5),(11.5,14),(14,16),(16,19),(19,21),
      (21,22.5),(22.5,24.5),(24.5,26)]

def retime(seg_text, times):
    lines = seg_text.split("\n")
    out, i = [], 0
    for ln in lines:
        m = re.match(r"^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】$", ln)
        if m:
            no = int(m.group(1)); a, b = times[no-1]
            out.append(f"【镜头{no:02d}｜[{a:g}s-{b:g}s]｜{m.group(2)}】")
            continue
        m2 = re.match(r"^\[[\d.]+s-[\d.]+s\](.*)$", ln)
        if m2:
            no = len([x for x in out if x.startswith("【镜头")])
            a, b = times[no-1]
            out.append(f"[{a:g}s-{b:g}s]{m2.group(1)}")
            continue
        out.append(ln)
    return "\n".join(out)

i2 = s.index("## 【第02段"); i3 = s.index("## 【第03段")
p2 = s[i2:i3]; p3 = s[i3:]
p2 = p2.replace("## 【第02段｜[0s-28s]", "## 【第02段｜[0s-30s]")
p3 = p3.replace("## 【第03段｜[0s-28s]", "## 【第03段｜[0s-26s]")
p2 = retime(p2, T2); p3 = retime(p3, T3)
s = s[:i2] + p2 + p3
open(f, "w", encoding="utf-8").write(s)
print("p02→30s, p03→26s")
