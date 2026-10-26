# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read().replace("\r\n", "\n")

def han(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))

parts = re.split(r"(?m)^(## 【第\d+段.*?】)[ \t]*$", t)
out, report, i = [parts[0]], [], 1
while i < len(parts):
    head, body = parts[i], parts[i+1]
    dur = int(re.search(r"\[0s-(\d+)s\]", head).group(1))
    shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body))
    info = []
    for m in shots:
        blk = m.group(5)
        dlg = [l for l in blk.split("\n") if l.startswith("[")]
        chars = 0
        for d in dlg:
            mm = re.findall(r"「(.+)」", d)
            if mm:
                chars += han(mm[0])
        act = re.split(r"[。]", blk.strip().split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", act) if len(c.strip()) > 3])
        t_act = min(3.5, max(1.0, round((0.6 + 0.7 * max(1, clauses)) * 2) / 2))
        t_dlg = round((chars / 4.9 + 0.4) * 2) / 2 if chars else 0
        tgt = t_dlg if chars else t_act
        if '拎箱' in m.group(4):
            tgt = 3.0
        cur = round(float(m.group(3)) - float(m.group(2)), 1)
        info.append({"m": m, "chars": chars, "cur": cur, "tgt": tgt})
        if chars:
            report.append((int(m.group(1)), m.group(4), chars, cur, tgt, round(cur - tgt, 1)))
    # 段内配平到 dur
    s = sum(x["tgt"] for x in info)
    if s > dur:  # 超出：等比压缩（仍保 0.5）
        k = dur / s
        for x in info:
            x["tgt"] = max(1.0, round(x["tgt"] * k * 2) / 2)
    # 全部对齐 0.5 网格
    for x in info:
        x["tgt"] = max(1.0, round(x["tgt"] * 2) / 2)
    # 用 0.5 的整数倍补齐到段长
    diff = round(dur - sum(x["tgt"] for x in info), 1)
    steps = int(round(diff / 0.5))
    silent = [x for x in info if not x["chars"]] or info
    k = 0
    while steps != 0:
        x = silent[k % len(silent)]
        nxt = round(x["tgt"] + (0.5 if steps > 0 else -0.5), 1)
        if nxt >= 1.0:
            x["tgt"] = nxt
            steps += -1 if steps > 0 else 1
        k += 1
        if k > 200:
            break
    t0 = 0.0
    for x in info:
        a, b = round(t0, 1), round(t0 + x["tgt"], 1)
        t0 = b
        m = x["m"]
        body = body.replace(f"【镜头{int(m.group(1)):02d}｜[{m.group(2)}s-{m.group(3)}s]｜{m.group(4)}】",
                            f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】", 1)
        body = body.replace(f"[{m.group(2)}s-{m.group(3)}s]，", f"[{a:g}s-{b:g}s]，", 1)
    out += [head, body]
    i += 2

open(f, "w", encoding="utf-8").write("".join(out))
print("镜号 标题 字数 原时长 应有 偏差")
for r in report:
    flag = "←" if abs(r[5]) >= 0.5 else ""
    print(f"{r[0]:02d} {r[1][:8]:<9}{r[2]:<4}{r[3]:<6}{r[4]:<6}{r[5]} {flag}")
