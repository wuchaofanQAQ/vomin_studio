# -*- coding: utf-8 -*-
import re, shutil
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
f = base + r"\drafts\ep01m_storyboard_v1.md"
shutil.copy(f, f + ".bak3")
t = open(f, encoding="utf-8").read()

# 解析段与镜头
segs = []
for m in re.finditer(r"(?ms)^## (【第\d+段.*?】)\n(.*?)(?=^## 【第|\Z)", t):
    body = m.group(2)
    shots = []
    for sm in re.finditer(r"(?ms)^【镜头\d+｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body):
        blk = sm.group(2).strip()
        lines = [l for l in blk.split("\n") if l.strip()]
        dlg = [l for l in lines if l.startswith("[")]
        chars = sum(len(re.findall(r"「(.+)」", d)[0]) for d in dlg if re.findall(r"「(.+)」", d))
        act = re.split(r"[。]", lines[0])[0]
        clauses = len([c for c in re.split(r"[；，、]", act) if len(c.strip()) > 3])
        e_act = min(3.0, 0.5 + 0.7 * max(1, clauses))
        e_dlg = chars / 5.0 + 0.3 if chars else 0
        exp = round(max(1.0, e_act, e_dlg), 1)
        if chars:
            exp = min(exp, round(chars / 5.0 + 0.4, 1))
        shots.append({"title": sm.group(1), "body": "\n".join(l for l in lines if not l.startswith("[")),
                      "dlg": dlg, "exp": exp})
    segs.append({"head": m.group(1), "body": body, "shots": shots})

allshots = [s for sg in segs for s in sg["shots"]]
print("镜数", len(allshots), "总时长", round(sum(s["exp"] for s in allshots),1))

# 贪心装段，目标 26s，上限 30s
groups, cur, acc = [], [], 0.0
for s in allshots:
    if cur and acc + s["exp"] > 26.5:
        groups.append((cur, round(acc))); cur, acc = [], 0.0
    cur.append(s); acc += s["exp"]
if cur: groups.append((cur, round(acc)))
print("段:", [(len(g), d) for g, d in groups])

# 保留原有段头/锁/现场/基准/空间文本（按段序号取源）
srcs = [sg["body"] for sg in segs]
def grab(src, name):
    mm = re.search(rf"【{name}】\n(.*?)(?=\n【本段|\n【镜头|\Z)", src, re.S)
    return mm.group(1).strip() if mm else ""

titles = ["走廊·我是沈幼怡", "走廊·你爸呢", "走廊·我这儿不是民宿", "玄关客厅·你哥哥会照顾好你的"]
finals = ["【陈诚】在门内半步、视线落在【沈幼怡】脸上；【沈幼怡】还站在门外。下一段他开口拒绝。",
          "【陈诚】站在门内、【手机】和门把各在一手；【沈幼怡】在门外，【行李箱】在她脚边。下一段他关门。",
          "门开着，【陈诚】侧身站在门内、手里提着【行李箱】；【沈幼怡】已经跨进门槛、光脚站在玄关地砖上。下一段她走进客厅。",
          "【沈幼怡】光脚站在玄关、【手机】握在胸前；【陈诚】站在客厅里、侧身对着她，刚笑完、眼神冷着。下一集从这句「照顾？」接。"]
DECL = "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
CN = {9:"九",10:"十",11:"十一",12:"十二",13:"十三",14:"十四"}

out = []
for i, (g, dur) in enumerate(groups, 1):
    src = srcs[0] if i <= 2 else (srcs[1] if i == 3 else srcs[2])
    base_txt = re.sub(r"^\d+镜按下列时码", f"{CN.get(len(g), len(g))}镜按下列时码", grab(src, "本段整体基准"), count=1, flags=re.M)
    base_txt = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/len(g),1)}秒", base_txt)
    if DECL not in base_txt: base_txt += DECL
    space = grab(src, "本段初始空间")
    out.append(f"## 【第{i:02d}段｜[0s-{dur}s]｜{titles[i-1]}】\n")
    out.append("【本段资产锁定】\n" + grab(src, "本段资产锁定") + "\n")
    out.append("【本段现场生成】\n" + grab(src, "本段现场生成") + "\n")
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
    out.append("【本段终态】\n" + finals[i-1] + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("按 26s 目标重排完成")
