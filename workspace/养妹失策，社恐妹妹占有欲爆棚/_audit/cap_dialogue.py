# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-(\d+)s\]｜.*?】)$", t)
out, i = [parts[0]], 1
report = []
while i < len(parts):
    head, dur, body = parts[i], int(parts[i + 1]), parts[i + 2]
    shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body))
    info = []
    for m in shots:
        d = round(float(m.group(3)) - float(m.group(2)), 1)
        chars = sum(len(re.findall(r"「(.+)」", l)[0]) for l in m.group(5).split("\n") if re.findall(r"「(.+)」", l))
        info.append({"m": m, "d": d, "chars": chars})
    saved = 0.0
    for x in info:
        if x["chars"]:
            cap = round((x["chars"] / 4.9 + 0.6) * 2) / 2
            if x["d"] > cap:
                saved += x["d"] - cap
                report.append(f"{x['m'].group(4)} {x['d']}→{cap}")
                x["d"] = cap
    # 把省下的时间给无台词镜头（按数量均分，0.5 网格）
    silent = [x for x in info if not x["chars"]]
    if silent and saved > 0:
        add = saved / len(silent)
        for x in silent:
            x["d"] = round((x["d"] + add) * 2) / 2
    # 尾差归最后一镜
    diff = round(dur - sum(x["d"] for x in info), 1)
    info[-1]["d"] = round(info[-1]["d"] + diff, 1)
    t0 = 0.0
    for x in info:
        a, b = round(t0, 1), round(t0 + x["d"], 1); t0 = b
        m = x["m"]
        body = body.replace(f"【镜头{int(m.group(1)):02d}｜[{m.group(2)}s-{m.group(3)}s]｜{m.group(4)}】",
                            f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】", 1)
        body = body.replace(f"[{m.group(2)}s-{m.group(3)}s]，", f"[{a:g}s-{b:g}s]，", 1)
    out += [head, body]
    i += 3
open(f, "w", encoding="utf-8").write("".join(out))
print("收口调整:", report)
