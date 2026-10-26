# -*- coding: utf-8 -*-
import re, shutil, math
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
shutil.copy(f, f + ".bak2")
t = open(f, encoding="utf-8").read()

parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-[\d.]+s\]｜.*?】)$", t)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body))
    infos = []
    for m in shots:
        blk = m.group(5).strip()
        dlg = [l for l in blk.split("\n") if l.startswith("[")]
        chars = 0
        for d in dlg:
            mm = re.findall(r"「(.+)」", d)
            if mm: chars += len(mm[0])
        act = re.split(r"[。]", blk.split("\n")[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", act) if len(c.strip()) > 3])
        e = max(1.0, min(3.0, 0.5 + 0.7 * max(1, clauses)), chars / 5.0 + 0.2 if chars else 0)
        floor = max(1.0, chars / 5.2 + 0.1 if chars else 1.0)
        infos.append({"m": m, "e": e, "floor": floor, "chars": chars})
    raw = sum(x["e"] for x in infos)
    # 目标：整数，≤30，取满足内容的最小整数（最多补到 30）
    target = min(30, max(math.ceil(raw), round(raw)))
    # 若补量能均摊到动作镜，且 raw 距离 30 不到 3 秒，则补到 30
    if 30 - raw <= 3.0:
        target = 30
    floor_sum = sum(x["floor"] for x in infos)
    extra = max(0.0, target - floor_sum)
    wsum = sum(x["e"] - x["floor"] for x in infos) or 1
    t0 = 0.0
    for x in infos:
        d = x["floor"] + extra * max(0.0, x["e"] - x["floor"]) / wsum
        d = max(d, x["floor"])
        a, b = round(t0, 1), round(t0 + d, 1)
        t0 = b
        a1, b1 = x["m"].group(2), x["m"].group(3)
        body = body.replace(f"【镜头{int(x['m'].group(1)):02d}｜[{a1}s-{b1}s]｜{x['m'].group(4)}】",
                            f"【镜头{int(x['m'].group(1)):02d}｜[{a:g}s-{b:g}s]｜{x['m'].group(4)}】")
        body = body.replace(f"[{a1}s-{b1}s]，", f"[{a:g}s-{b:g}s]，")
    # 段尾收口到整数
    head = re.sub(r"\[0s-[\d.]+s\]", f"[0s-{target}s]", head)
    out += [head, body]
open(f, "w", encoding="utf-8").write("".join(out))
print("整数段长重算完成")
