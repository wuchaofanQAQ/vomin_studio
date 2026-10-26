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
    if chars:
        dur = round((chars / 4.9 + 0.4) * 2) / 2          # 台词：按 4.9 字/秒 + 0.4 余量，0.5 网格
        dur = max(1.0, dur)
    else:
        dur = round((0.6 + 0.7 * max(1, clauses)) * 2) / 2  # 动作：每动作 0.7s + 0.6 起幅，0.5 网格
        dur = min(3.5, max(1.0, dur))
    shots.append({"title": m.group(1), "body": "\n".join(l for l in lines if not l.startswith("[")),
                  "dlg": dlg, "chars": chars, "dur": dur})

CUT = next(i for i, s in enumerate(shots) if s["title"].startswith("迈进")) + 1
regions = [(shots[:CUT], "走廊"), (shots[CUT:], "玄关")]

groups = []
for seq, name in regions:
    cur, acc = [], 0.0
    for s in seq:
        if cur and acc + s["dur"] > 30:
            groups.append((cur, acc, name)); cur, acc = [], 0.0
        cur.append(s); acc += s["dur"]
    if cur: groups.append((cur, acc, name))

print("段:", [(n, len(g), round(a,1)) for g, a, n in groups])

def grab(name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\n## |\Z)", t, re.S)
    return mm.group(1).strip() if mm else ""

LOCK, LIVE, BASE, SPACE = grab("本段资产锁定"), grab("本段现场生成"), grab("本段整体基准"), grab("本段初始空间")
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
CN = "零一二三四五六七八九十"
def cn(n):
    if n <= 10: return CN[n]
    if n < 20: return "十" + CN[n-10]
    return str(n)

out = []
for i, (g, raw, region) in enumerate(groups, 1):
    dur = int(round(raw))
    base_txt = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn(len(g))}镜按下列时码", BASE, count=1)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(raw/len(g),1)}秒", base_txt)
    if DECL not in base_txt: base_txt += DECL
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{g[0]['title']}】\n")
    out.append("【本段资产锁定】\n" + LOCK + "\n")
    out.append("【本段现场生成】\n" + LIVE + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + SPACE + "\n")
    t0 = 0.0
    for idx, s in enumerate(g, 1):
        a, b = round(t0, 1), round(t0 + s["dur"], 1); t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append(f"【本段终态】\n本段止于「{g[-1]['title']}」：{g[-1]['body'][:70]}。下一段接续同一场，人物位置与朝向按本段终态延续。\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("完成")
