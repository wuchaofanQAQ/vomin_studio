# -*- coding: utf-8 -*-
import re, shutil
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
shutil.copy(f, f + ".bak5")
t = open(f, encoding="utf-8").read()

# 用备份的稳定版重建
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
                  "dlg": dlg, "exp": round(e, 1)})

# 走廊/玄关边界：迈进门槛 是走廊最后一镜
cut = next(i for i, s in enumerate(shots) if s["title"].startswith("迈进")) + 1
z, k = shots[:cut], shots[cut:]
print("走廊", len(z), round(sum(s['exp'] for s in z),1), "s | 玄关", len(k), round(sum(s['exp'] for s in k),1), "s")

def pack(seq, cap=30):
    groups, cur, acc = [], [], 0.0
    for s in seq:
        if cur and acc + s["exp"] > cap:
            groups.append((cur, round(acc))); cur, acc = [], 0.0
        cur.append(s); acc += s["exp"]
    if cur: groups.append((cur, round(acc)))
    return groups

groups = pack(z) + pack(k)
print("段:", [(len(g), d) for g, d in groups])

def grab(name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\n## |\Z)", t, re.S)
    return mm.group(1).strip() if mm else ""

LOCK = grab("本段资产锁定")
LIVE = grab("本段现场生成")
BASE = grab("本段整体基准")
SPACE = grab("本段初始空间")
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
CN = {8:"八",9:"九",10:"十",11:"十一",12:"十二",13:"十三",14:"十四"}

out = []
for i, (g, dur) in enumerate(groups, 1):
    is_k = g[0] is k[0] if k else False
    dur = 30 if 29 <= dur <= 30 else dur
    base_txt = re.sub(r"^\d+镜按下列时码", f"{CN.get(len(g), len(g))}镜按下列时码", BASE, count=1, flags=re.M)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/max(1,len(g)),1)}秒", base_txt)
    if DECL not in base_txt: base_txt += DECL
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{'玄关客厅' if is_k else '走廊'}·{g[0]['title']}】\n")
    out.append("【本段资产锁定】\n" + LOCK + "\n")
    out.append("【本段现场生成】\n" + LIVE + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + SPACE + "\n")
    t0 = 0.0
    for idx, s in enumerate(g, 1):
        a, b = round(t0, 1), round(t0 + s["exp"], 1); t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    fin = (f"本段止于「{g[-1]['title']}」：{g[-1]['body'][:60]}。下一段接续同一场。")
    out.append("【本段终态】\n" + fin + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("合并完成")
