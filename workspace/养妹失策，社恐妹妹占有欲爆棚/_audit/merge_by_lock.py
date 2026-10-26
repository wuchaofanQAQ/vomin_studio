# -*- coding: utf-8 -*-
import re, shutil, math
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
shutil.copy(f, f + ".bak4")
t = open(f, encoding="utf-8").read()

# 解析所有镜头（保序）
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
                  "dlg": dlg, "exp": round(e, 1), "chars": chars})
print("镜数", len(shots), "内容总时长", round(sum(s["exp"] for s in shots),1))

# 每镜的锁定资产集合：走廊组 vs 玄关组（按是否出现【陈诚公寓客厅】判断）
def lock_key(s):
    return "客厅" if "【陈诚公寓客厅】" in s["body"] else "走廊"

# 贪心：锁不变 且 累加 ≤30 就合并
groups, cur, acc, key = [], [], 0.0, None
for s in shots:
    k = lock_key(s)
    if cur and (k != key or acc + s["exp"] > 30):
        groups.append((cur, round(acc)))
        cur, acc = [], 0.0
    cur.append(s); acc += s["exp"]; key = k
if cur: groups.append((cur, round(acc)))
print("段:", [(len(g), d) for g, d in groups])

src_full = t  # 用于取段落模板

def grab(name, src):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\n## |\Z)", src, re.S)
    return mm.group(1).strip() if mm else ""

LOCK_Z = grab("本段资产锁定", t)
space_z = grab("本段初始空间", t)

# 玄关段的锁与空间（从原文找含【陈诚公寓客厅】的段）
m_k = re.search(r"(?ms)## 【第\d+段.*?【本段资产锁定】\n(.*?)(?=\n【本段现场生成】)", t)
lock_k = m_k.group(1).strip()
live_z = grab("本段现场生成", t)
base_z = grab("本段整体基准", t)
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"

titles = []
for i, (g, d) in enumerate(groups, 1):
    titles.append(f"段{i:02d}·{'玄关' if lock_key(g[0])=='客厅' else '走廊'}")
finals = ["下一段继续。"] * len(groups)

out = []
for i, (g, dur) in enumerate(groups, 1):
    is_k = lock_key(g[0]) == "客厅"
    lock = lock_k if is_k else LOCK_Z
    base_txt = base_z
    base_txt = re.sub(r"^\d+镜按下列时码", f"{len(g)}镜按下列时码", base_txt, count=1, flags=re.M)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/max(1,len(g)),1)}秒", base_txt)
    if DECL not in base_txt: base_txt += DECL
    space = space_z if not is_k else "【陈诚公寓客厅】：入户门在画左，玄关地砖与客厅木地板在画面下三分之一分界；沙发在画左靠墙，矮茶几在中央，开放式厨房在画右后，通往卧室的门在画右；机位在客厅中央、与站姿平齐。"
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{'玄关客厅·你哥哥会照顾好你的' if is_k else '走廊'}】\n")
    out.append("【本段资产锁定】\n" + lock + "\n")
    out.append("【本段现场生成】\n" + grab("本段现场生成", t) + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + space + "\n")
    t0, idx = 0.0, 0
    for s in g:
        idx += 1
        a, b = round(t0, 1), round(t0 + s["exp"], 1); t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append("【本段终态】\n" + f"本段止于{g[-1]['title']}。" + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("按「锁不变+30s」合并完成")
