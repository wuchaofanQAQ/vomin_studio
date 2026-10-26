# -*- coding: utf-8 -*-
import re, shutil, os
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
shutil.copy(f, f + ".bak")

md = open(f, encoding="utf-8").read()

def section(body, name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\Z)", body, re.S)
    return mm.group(1).strip() if mm else ""

segs = []
for m in re.finditer(r"(?ms)^## (【第\d+段.*?】)\n(.*?)(?=^## 【第|\Z)", md):
    body = m.group(2)
    shots = []
    for sm in re.finditer(r"(?ms)^【镜头\d+｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body):
        blk = sm.group(2).strip()
        lines = [l for l in blk.split("\n") if l.strip()]
        shots.append({"title": sm.group(1),
                      "body": "\n".join(l for l in lines if not l.startswith("[")),
                      "dlg": [l for l in lines if l.startswith("[")]})
    segs.append({"lock": section(body, "本段资产锁定"), "live": section(body, "本段现场生成"),
                 "base": section(body, "本段整体基准"), "space": section(body, "本段初始空间"),
                 "shots": shots})

allshots = [s for sg in segs for s in sg["shots"]]
def exp_of(sh):
    chars = 0
    for d in sh["dlg"]:
        mm = re.findall(r"「(.+)」", d)
        if mm: chars += len(mm[0])
    action = re.split(r"[。]", sh["body"].split("\n")[0])[0]
    clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
    return round(max(1.0, min(3.4, 0.5 + 0.8 * max(1, clauses)), chars / 4.8 + 0.3 if chars else 0), 1)

for s in allshots: s["exp"] = exp_of(s)
total = sum(s["exp"] for s in allshots)
print("镜数", len(allshots), "公式总时长", round(total, 1))

# 贪心装段：≤30s，且尽量 ≥24s
groups, cur, acc = [], [], 0.0
for s in allshots:
    if cur and acc + s["exp"] > 30:
        groups.append(cur); cur, acc = [], 0.0
    cur.append(s); acc += s["exp"]
if cur: groups.append(cur)
print("段数", len(groups), [round(sum(x["exp"] for x in g),1) for g in groups])

titles = ["走廊·我是沈幼怡", "走廊·你爸呢", "走廊·我这儿不是民宿", "玄关客厅·你哥哥会照顾好你的"]
finals = ["【陈诚】在门内半步、视线落在【沈幼怡】脸上；【沈幼怡】还站在门外。下一段他开口拒绝。",
          "【陈诚】站在门内、【手机】和门把各在一手；【沈幼怡】在门外，【行李箱】在她脚边。下一段他关门。",
          "门开着，【陈诚】侧身站在门内、手里提着【行李箱】；【沈幼怡】已经跨进门槛、光脚站在玄关地砖上。下一段她走进客厅。",
          "【沈幼怡】光脚站在玄关、【手机】握在胸前；【陈诚】站在客厅里、侧身对着她，刚笑完、眼神冷着。下一集从这句「照顾？」接。"]
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"

out = []
for i, g in enumerate(groups, 1):
    dur = round(sum(s["exp"] for s in g), 1)
    src = segs[0] if i <= 2 else segs[1] if i == 3 else segs[2]
    base_txt = src["base"]
    base_txt = re.sub(r"^\d+镜按下列时码", f"{len(g)}镜按下列时码", base_txt, count=1, flags=re.M)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/len(g),1)}秒", base_txt)
    if DECL not in base_txt:
        base_txt += DECL
    out.append(f"## 【第{i:02d}段｜[0s-{dur:g}s]｜{titles[i-1]}】\n")
    out.append("【本段资产锁定】\n" + src["lock"] + "\n")
    out.append("【本段现场生成】\n" + src["live"] + "\n")
    out.append("【本段整体基准】\n" + base_txt + "\n")
    out.append("【本段初始空间】\n" + src["space"] + "\n")
    t = 0.0
    for n, s in enumerate(g, 1):
        a, b = round(t, 1), round(t + s["exp"], 1); t = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{n:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append("【本段终态】\n" + finals[i-1] + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("重建完成")
