# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

D1 = [1.7,1.7,1.4,2.7,2.1,1.4,1.7,1.9,1.9,1.8,3.4,1.6,1.8,1.6,2.4,0.9]
D2 = [2.0,2.0,3.6,1.4,1.4,1.3,1.5,0.8,4.4,1.4,2.8,1.4,3.0,1.6]
D = {1: D1, 2: D2}

def lay(durs, target):
    s = sum(durs)
    durs = [round(d * target / s, 1) for d in durs]
    durs[-1] = round(target - sum(durs[:-1]), 1)
    return durs

parts = re.split(r"(?m)^(## 【第\d+段.*?】)$", t)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    seg = int(re.search(r"第(\d+)段", head).group(1))
    if seg not in D:
        out += [head, body]; continue
    shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】", body))
    durs = D[seg]
    assert len(shots) == len(durs), (seg, len(shots), len(durs))
    durs = lay(durs, 30.0 if seg == 1 else 28.0)
    t0 = 0.0
    for m, d in zip(shots, durs):
        a1, b1, a2, b2 = m.group(2), m.group(3), round(t0, 1), round(t0 + d, 1)
        body = body.replace(f"【镜头{int(m.group(1)):02d}｜[{a1}s-{b1}s]｜{m.group(4)}】",
                            f"【镜头{int(m.group(1)):02d}｜[{a2:g}s-{b2:g}s]｜{m.group(4)}】")
        body = body.replace(f"[{a1}s-{b1}s]，", f"[{a2:g}s-{b2:g}s]，")
        t0 = b2
    target = 30.0 if seg == 1 else 28.0
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target:g}s]", head)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("p01→30s / p02→28s 重排完成")
