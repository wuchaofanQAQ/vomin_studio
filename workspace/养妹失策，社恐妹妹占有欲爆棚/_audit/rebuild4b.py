# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
md = open(f, encoding="utf-8").read()

# 解析每一段
segs = []
for m in re.finditer(r"(?ms)^## (【第\d+段.*?】)\n(.*?)(?=^## 【第|\Z)", md):
    head, body = m.group(1), m.group(2)
    def grab(name):
        mm = re.search(rf"【{name}】\n(.*?)(?=\n【|\Z)", body, re.S)
        return mm.group(1).strip() if mm else ""
    shots = []
    for sm in re.finditer(r"(?ms)^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", body):
        blk = sm.group(3).strip()
        lines = [l for l in blk.split("\n") if l.strip()]
        dlg = [l for l in lines if l.startswith("[")]
        txt = "\n".join([l for l in lines if not l.startswith("[")])
        shots.append({"title": sm.group(2), "body": txt, "dlg": dlg})
    segs.append({"head": head, "lock": grab("本段资产锁定"), "live": grab("本段现场生成"),
                 "base": grab("本段整体基准"), "space": grab("本段初始空间"), "shots": shots})

def exp_of(sh):
    chars = sum(len(re.findall(r"「(.+)」", d)[0]) if re.findall(r"「(.+)」", d) else 0 for d in sh["dlg"])
    action = re.split(r"[。]", sh["body"].split("\n")[0])[0]
    clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
    return round(max(1.0, min(3.4, 0.5 + 0.8 * max(1, clauses)), chars / 4.8 + 0.3 if chars else 0), 1)

allshots = [s for sg in segs for s in sg["shots"]]
print("镜数", len(allshots))

# 4 段：走廊前半 11 / 走廊后半 6 / 拒绝与开门 14 / 玄关 12
groups = [allshots[0:11], allshots[11:17], allshots[17:31], allshots[31:]]
titles = ["走廊·我是沈幼怡", "走廊·你爸呢", "走廊·我这儿不是民宿", "玄关客厅·你哥哥会照顾好你的"]
finals = ["【陈诚】在门内半步、视线落在【沈幼怡】脸上；【沈幼怡】还站在门外。下一段他开口拒绝。",
          "【陈诚】站在门内、【手机】和门把各在一手；【沈幼怡】在门外，【行李箱】在她脚边。下一段他关门。",
          "门开着，【陈诚】侧身站在门内、手里提着【行李箱】；【沈幼怡】已经跨进门槛、光脚站在玄关地砖上。",
          "【沈幼怡】光脚站在玄关、【手机】握在胸前；【陈诚】站在客厅里、侧身对着她，刚笑完、眼神冷着。"]

out = []
for i, g in enumerate(groups, 1):
    dur = round(sum(exp_of(s) for s in g), 1)
    src = segs[0] if i <= 2 else segs[1] if i == 3 else segs[2]
    base = src["base"]
    base = re.sub(r"^\d+镜按下列时码", f"{len(g)}镜按下列时码", base, count=1, flags=re.M)
    out.append(f"## 【第{i:02d}段｜[0s-{dur:g}s]｜{titles[i-1]}】\n")
    out.append("【本段资产锁定】\n" + src["lock"] + "\n")
    out.append("【本段现场生成】\n" + src["live"] + "\n")
    out.append("【本段整体基准】\n" + base + "\n")
    out.append("【本段初始空间】\n" + src["space"] + "\n")
    t = 0.0
    for n, s in enumerate(g, 1):
        d = exp_of(s)
        a, b = round(t, 1), round(t + d, 1); t = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{n:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append("【本段终态】\n" + finals[i-1] + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("4 段重建完成（按公式时长）")
