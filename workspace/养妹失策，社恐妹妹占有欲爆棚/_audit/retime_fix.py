# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

parts = re.split(r"(?m)^(## 【第\d+段.*?】)$", t)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    shots = re.findall(r"(?ms)^(【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】)\n(.+?)(?=\n\n|\Z)", body)
    data = []
    for full, no, a, b, title, txt = None, *rest:
        pass
    data = []
    for full, no, a, b, title, txt in shots:
        chars = 0
        for ln in txt.split("\n"):
            m = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", ln.strip())
            if m: chars += len(m.group(1))
        data.append({"full": full, "no": int(no), "a": float(a), "b": float(b),
                     "title": title, "chars": chars, "dur": float(b) - float(a)})
    # 需要的延长量
    for d in data:
        if d["chars"]:
            d["min"] = round(d["chars"] / 5.0 + 0.1, 1)
        else:
            d["min"] = d["dur"]
    deficit = sum(max(0, d["min"] - d["dur"]) for d in data)
    # 从最长的无台词镜头里扣
    donors = sorted([d for d in data if not d["chars"] and d["dur"] > 1.2],
                    key=lambda x: -x["dur"])
    need = deficit
    for dn in donors:
        if need <= 0: break
        take = min(need, dn["dur"] - 1.2)
        dn["dur"] = round(dn["dur"] - take, 1)
        need -= take
    # 重排时间
    tcur = 0.0
    for d in data:
        newdur = max(d["dur"], d["min"])
        a2, b2 = round(tcur, 1), round(tcur + newdur, 1)
        tcur = b2
        body = body.replace(d["full"], f"【镜头{d['no']:02d}｜[{a2:g}s-{b2:g}s]｜{d['title']}】")
        body = body.replace(f"[{d['a']:g}s-{d['b']:g}s]，", f"[{a2:g}s-{b2:g}s]，")
    target = {"01": 30, "02": 28, "03": 26}[head[5:7]]
    # 若总和偏离目标，最后一条吸收
    diff = round(tcur - target, 1)
    if abs(diff) >= 0.1 and data:
        last = data[-1]
        # 直接改最后一镜
        body = re.sub(r"【镜头%d｜\[[\d.]+s-[\d.]+s\]" % last["no"],
                      f"【镜头{last['no']:02d}｜[{round(tcur-last['dur'],1):g}s-{target:g}s]", body)
        body = re.sub(r"\[[\d.]+s-[\d.]+s\]，", f"[{round(tcur-last['dur'],1):g}s-{target:g}s]，", body, count=1) if last["chars"] else body
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target}s]", head)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("逐镜重排完成")
