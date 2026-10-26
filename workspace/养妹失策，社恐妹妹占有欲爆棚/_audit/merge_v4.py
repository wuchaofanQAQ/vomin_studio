# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
t = open(f + ".bak4", encoding="utf-8").read()

shots = []
for m in re.finditer(r"(?ms)^【镜头\d+｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\n## |\Z)", t):
    blk = m.group(2).strip()
    lines = [l for l in blk.split("\n") if l.strip()]
    dlg = [l for l in lines if l.startswith("[")]
    chars = sum(len(re.findall(r"「(.+)」", d)[0]) for d in dlg if re.findall(r"「(.+)」", d))
    act = re.split(r"[。]", lines[0])[0]
    clauses = len([c for c in re.split(r"[；，、]", act) if len(c.strip()) > 3])
    e = max(1.0, min(3.0, 0.5 + 0.7 * max(1, clauses)), chars / 4.9 + 0.25 if chars else 0)
    shots.append({"title": m.group(1), "body": "\n".join(l for l in lines if not l.startswith("[")),
                  "dlg": dlg, "exp": e})

CUT = next(i for i, s in enumerate(shots) if s["title"].startswith("迈进")) + 1
zon = shots[:CUT]
gui = shots[CUT:]
print("走廊", len(zon), round(sum(s["exp"] for s in zon), 1), "| 玄关", len(gui), round(sum(s["exp"] for s in gui), 1))

def pack(seq, cap=30.0):
    groups, cur, acc = [], [], 0.0
    for s in seq:
        if cur and acc + s["exp"] > cap:
            groups.append((cur, acc)); cur, acc = [], 0.0
        cur.append(s); acc += s["exp"]
    if cur: groups.append((cur, acc))
    return groups

groups = pack(zon) + pack(gui)
print("组:", [(len(g), round(a, 1)) for g, a in groups])

def grab(name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\n## |\Z)", t, re.S)
    return mm.group(1).strip() if mm else ""

LOCK, LIVE, BASE, SPACE = grab("本段资产锁定"), grab("本段现场生成"), grab("本段整体基准"), grab("本段初始空间")
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
CN = "零一二三四五六七八九十"

def cn(n):
    if n <= 10: return CN[n]
    if n < 20: return "十" + CN[n - 10]
    return "二十" if n == 20 else str(n)

out = []
for i, (g, raw) in enumerate(groups, 1):
    dur = 30 if raw >= 28 else max(6, int(round(raw)))
    scale = dur / raw
    durs = [round(s["exp"] * scale, 1) for s in g]
    durs[-1] = round(dur - sum(durs[:-1]), 1)
    base_txt = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn(len(g))}镜按下列时码", BASE, count=1)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur / len(g), 1)}秒", base_txt)
    if DECL not in base_txt:
        base_txt += DECL
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{g[0]['title']}】\n")
    out.append("【本段资产锁定】\n" + LOCK + "\n")
    out.append("【本段现场生成】\n" + LIVE + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + SPACE + "\n")
    t0 = 0.0
    for idx, (s, d) in enumerate(zip(g, durs), 1):
        a, b = round(t0, 1), round(t0 + d, 1)
        t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append(f"【本段终态】\n本段止于「{g[-1]['title']}」：{g[-1]['body'][:70]}。下一段接续同一场，人物位置与朝向按本段终态延续。\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("完成，段长:", [30 if a >= 28 else max(6, int(round(a))) for g, a in groups])
