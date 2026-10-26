# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 拆 镜头03 → 03 全景 / 04 等待细节
old3 = """【镜头03｜[1.4s-2.8s]｜门外】
走廊纵深的低机位全景，镜头从门口向后拉半步。地砖被晒出一层白亮，热浪把远处的墙线晃得发软，蝉声铺满整条走廊。中景【沈幼怡】站在门外约零点八米处，长发垂到腰、发尾被汗黏在颈侧，后背的裙子被汗浸出深色一片；她的脚趾在皮鞋里动了一下，右手把肩带往上提半寸又放下，重心从左脚换到右脚。【陈诚】在门内半步，视线仍停在【行李箱】的轮子上。后景是走廊尽头那扇窗的白。切在她垂着的肩线始终没抬。
[1.4s-2.8s]，【陈诚】（OS、心里过了一遍说）：「来投奔亲戚的？」"""
if old3 not in s:
    # 时间可能不同，用正则找
    m = re.search(r"【镜头03｜\[[\d.]+s-[\d.]+s\]｜门外】.*?(?=\n\n)", s, re.S)
    old3 = m.group(0)
new3 = """【镜头03｜[0s-0s]｜门外】
走廊纵深的低机位全景，镜头从门口向后拉半步。地砖被晒出一层白亮，热浪把远处的墙线晃得发软，蝉声铺满整条走廊。中景【沈幼怡】站在门外约零点八米处，长发垂到腰、发尾被汗黏在颈侧，后背的裙子被汗浸出深色一片。【陈诚】在门内半步，视线停在【行李箱】的轮子上。后景是走廊尽头那扇窗的白。切在镜头拉到位、她垂着的肩线始终没抬。
[0s-0s]，【陈诚】（OS、心里过了一遍说）：「来投奔亲戚的？」

【镜头04｜[0s-0s]｜等了一个小时】
过【陈诚】肩的机位中景，镜头不动。前景是【陈诚】虚化的肩线。中景【沈幼怡】的脚趾在皮鞋里动了一下，右手把肩带往上提半寸又放下，重心从左脚换到右脚——每个动作之间都停半拍，像在门口已经站了很久。后景是走廊地砖的反光。切在她重心换回左脚、裙摆垂下去。"""
s = s.replace(old3, new3)

# 2) p01 重新编号（原 04-16 → 05-17）并重排时间
p1_start = s.index("## 【第01段")
p1_end = s.index("## 【第02段")
seg = s[p1_start:p1_end]
shots = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】", seg))
# 重编号
for idx, m in enumerate(shots, 1):
    seg = seg.replace(m.group(0).split("｜")[0] + "｜", f"【镜头{idx:02d}｜", 1) if False else seg
# 统一用顺序编号（从 1 开始）
lines = seg.split("\n")
out, n = [], 0
for ln in lines:
    m = re.match(r"^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】$", ln)
    if m:
        n += 1
        out.append(f"【镜头{n:02d}｜[0s-0s]｜{m.group(2)}】")
    else:
        out.append(ln)
seg = "\n".join(out)
s = s[:p1_start] + seg + s[p1_end:]

# 3) p01 时间表（17 镜，合计 30）
D1 = [1.5,1.5,1.8,1.6,2.4,2.0,1.4,1.6,1.8,1.7,1.6,3.2,1.2,1.7,1.5,2.2,0.9]
# 4) p02 28→30、p03 26→30（等比放大，台词更宽松）
def retime(body, durs, target):
    ms = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】", body))
    assert len(ms) == len(durs), (len(ms), len(durs))
    t0 = 0.0
    for m, d in zip(ms, durs):
        a, b = round(t0, 1), round(t0 + d, 1)
        body = body.replace(m.group(0), f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】", 1)
        body = body.replace(f"[{m.group(2)}s-{m.group(3)}s]，", f"[{a:g}s-{b:g}s]，")
        t0 = b
    return body

# 应用 p01
p1_start = s.index("## 【第01段"); p1_end = s.index("## 【第02段")
seg = retime(s[p1_start:p1_end], D1, 30)
seg = re.sub(r"## 【第01段｜\[0s-[\d.]+s\]", "## 【第01段｜[0s-30s]", seg)
s = s[:p1_start] + seg + s[p1_end:]

# p02 / p03 等比放大到 30
for segno, newtarget in ((2, 30), (3, 30)):
    a = s.index(f"## 【第{segno:02d}段"); b = s.index("## 【第", a + 5) if segno != 3 else len(s)
    body = s[a:b]
    ms = list(re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】", body))
    durs = [round((float(m.group(3)) - float(m.group(2))) * newtarget / float(re.search(r'\[0s-([\d.]+)s\]', body).group(1)), 1) for m in ms]
    durs[-1] = round(newtarget - sum(durs[:-1]), 1)
    body = retime(body, durs, newtarget)
    body = re.sub(r"## 【第\d+段｜\[0s-[\d.]+s\]", f"## 【第{segno:02d}段｜[0s-{newtarget}s]", body)
    s = s[:a] + body + s[b:]

open(f, "w", encoding="utf-8").write(s)
print("3×30 重排完成")
