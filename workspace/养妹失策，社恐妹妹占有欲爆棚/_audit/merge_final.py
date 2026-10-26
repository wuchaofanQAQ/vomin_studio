# -*- coding: utf-8 -*-
import re, shutil
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
src = f + ".bak4"
t = open(src, encoding="utf-8").read()

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
                  "dlg": dlg, "exp": e, "chars": chars})

def lock_of(s):
    return "K" if "【陈诚公寓客厅】" in s["body"] else "Z"

# 贪心：锁不变 且 累加 ≤30
groups, cur, acc, key = [], [], 0.0, None
for s in shots:
    k = lock_of(s)
    if cur and (k != key or acc + s["exp"] > 30):
        groups.append((cur, acc)); cur, acc = [], 0.0
    cur.append(s); acc += s["exp"]; key = k
if cur: groups.append((cur, acc))
print("分镜组:", [(len(g), round(a,1)) for g, a in groups])

def grab(name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\n## |\Z)", t, re.S)
    return mm.group(1).strip() if mm else ""

LOCK = grab("本段资产锁定")
LIVE = grab("本段现场生成")
BASE = grab("本段整体基准")
SPACE = grab("本段初始空间")
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
CN = "零一二三四五六七八九十"

def cn(n):
    if n <= 10: return CN[n]
    if n < 20: return "十" + CN[n-10]
    return str(n)

out = []
for i, (g, raw) in enumerate(groups, 1):
    # 目标时长：接近 30 的取 30，明显不足的取整数自身
    dur = 30 if raw >= 26 else max(6, round(raw))
    # 等比缩放到目标时长（只会拉长或微缩）
    scale = dur / raw
    durs = [round(s["exp"] * scale, 1) for s in g]
    durs[-1] = round(dur - sum(durs[:-1]), 1)
    base_txt = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn(len(g))}镜按下列时码", BASE, count=1)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/len(g),1)}秒", base_txt)
    if DECL not in base_txt: base_txt += DECL
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{g[0]['title']}】\n")
    out.append("【本段资产锁定】\n" + LOCK + "\n")
    out.append("【本段现场生成】\n" + LIVE + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + SPACE + "\n")
    t0 = 0.0
    for idx, (s, d) in enumerate(zip(g, durs), 1):
        a, b = round(t0, 1), round(t0 + d, 1); t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append(f"【本段终态】\n本段止于「{g[-1]['title']}」：{g[-1]['body'][:70]}。下一段接续同一场，人物位置与朝向按本段终态延续。\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("按时长贪心合并完成:", [30 if a>=26 else max(6,round(a)) for g,a in groups])
