# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
md = open(f, encoding="utf-8").read()
TARGET = {1: 30.0, 2: 28.0, 3: 26.0}
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    seg = int(re.search(r"第(\d+)段", head).group(1))
    target = TARGET[seg]
    shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", body)
    info = []
    for no, a, b, title, txt in shots:
        dlg_chars = 0
        for ln in txt.split("\n"):
            m = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", ln.strip())
            if m:
                dlg_chars += len(m.group(1).replace("「", "").replace("」", ""))
        action = re.split(r"[。]", txt.split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
        e_act = min(3.4, 0.5 + 0.8 * max(1, clauses))
        e_dlg = dlg_chars / 4.8 + 0.3 if dlg_chars else 0
        floor = max(1.0, dlg_chars / 5.2 + 0.15 if dlg_chars else 1.0)
        info.append((no, a, b, title, max(e_act, e_dlg), floor))
    total_floor = sum(x[5] for x in info)
    if total_floor > target:
        print(f"第{seg}段 最短需求 {round(total_floor,1)}s > 目标 {target}s")
    extra = max(0.0, target - total_floor)
    base_sum = sum(x[4] - x[5] for x in info) or 1
    times, t = [], 0.0
    for no, a, b, title, e, fl in info:
        d = fl + extra * max(0.0, e - fl) / base_sum
        times.append((round(t, 1), round(t + max(d, fl), 1)))
        t += max(d, fl)
    times[-1] = (times[-1][0], target)
    for (no, old_a, old_b, title, _, _), (na, nb) in zip(info, times):
        body = body.replace(f"【镜头{int(no):02d}｜[{old_a}s-{old_b}s]｜{title}】",
                            f"【镜头{int(no):02d}｜[{na:g}s-{nb:g}s]｜{title}】")
        body = body.replace(f"[{old_a}s-{old_b}s]，", f"[{na:g}s-{nb:g}s]，")
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target:g}s]", head)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("done")
