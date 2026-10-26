# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
md = open(f, encoding="utf-8").read()

def han(s): return len(re.findall(r"[\u4e00-\u9fff]", s))

TARGET = {1: 30.0, 2: 28.0, 3: 26.0}
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
out = [parts[0]]

for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    seg = int(re.search(r"第(\d+)段", head).group(1))
    target = TARGET[seg]
    shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", body)
    exps = []
    for no, a, b, title, txt in shots:
        words = 0
        for line in txt.split("\n"):
            m = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", line.strip())
            if m: words += han(m.group(1))
        action = re.split(r"[。]", txt.split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
        e_act = min(3.4, 0.5 + 0.8 * max(1, clauses))
        e_dlg = words / 4.8 + 0.3 if words else 0
        exps.append(max(e_act, e_dlg, 1.0))
    scale = target / sum(exps)
    times = []
    t = 0.0
    for e in exps:
        d = round(e * scale, 1)
        times.append((round(t, 1), round(t + d, 1)))
        t += d
    # 修正累计误差到最后一条
    a0, b0 = times[-1]
    times[-1] = (a0, round(target, 1))
    # 重写该段
    for (no, old_a, old_b, title, _), (na, nb) in zip(shots, times):
        body = body.replace(f"【镜头{int(no):02d}｜[{old_a}s-{old_b}s]｜{title}】",
                            f"【镜头{int(no):02d}｜[{na:g}s-{nb:g}s]｜{title}】")
        body = body.replace(f"[{old_a}s-{old_b}s]，", f"[{na:g}s-{nb:g}s]，")
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target:g}s]", head)
    out += [head, body]

open(f, "w", encoding="utf-8").write("".join(out))
print("按公式重新分配完成")
