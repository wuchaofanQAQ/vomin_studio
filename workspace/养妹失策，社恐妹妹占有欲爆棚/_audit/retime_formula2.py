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
    info = []
    for no, a, b, title, txt in shots:
        words = sum(han(m.group(1)) for m in
                    (re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", ln.strip()) for ln in txt.split("\n")) if m)
        action = re.split(r"[。]", txt.split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
        e_act = min(3.4, 0.5 + 0.8 * max(1, clauses))
        e_dlg = words / 4.8 + 0.3 if words else 0
        floor = max(1.0, words / 5.3 + 0.1 if words else 1.0)
        info.append((no, a, b, title, max(e_act, e_dlg), floor))
    total_floor = sum(x[5] for x in info)
    if total_floor > target:
        print(f"第{seg}段 最短需求 {round(total_floor,1)}s > 目标 {target}s，需删镜或加时长")
    extra = max(0.0, target - total_floor)
    base_sum = sum(x[4] - x[5] for x in info) or 1
    times, t = [], 0.0
    for no, a, b, title, e, fl in info:
        d = fl + extra * (e - fl) / base_sum
        d = max(fl, d)
        times.append((round(t, 1), round(t + d, 1)))
        t += d
    times[-1] = (times[-1][0], target)
    for (no, old_a, old_b, title, _, _), (na, nb) in zip(info, times):
        body = body.replace(f"【镜头{int(no):02d}｜[{old_a}s-{old_b}s]｜{title}】",
                            f"【镜头{int(no):02d}｜[{na:g}s-{nb:g}s]｜{title}】")
        body = body.replace(f"[{old_a}s-{old_b}s]，", f"[{na:g}s-{nb:g}s]，")
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target:g}s]", head)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("按公式+语速下限重新分配完成")
