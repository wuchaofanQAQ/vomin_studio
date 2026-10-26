# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

p1a = s.index("## 【第01段"); p1b = s.index("## 【第02段")
seg = s[p1a:p1b]

# 解析 p01 的镜头块
lines = seg.split("\n")
pre, shots, cur = [], [], None
for ln in lines:
    m = re.match(r"^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】$", ln)
    if m:
        cur = {"title": m.group(2), "lines": []}
        shots.append(cur); continue
    if cur is None:
        pre.append(ln)
    else:
        cur["lines"].append(ln)

# 拆 03：把「脚趾/肩带/重心」那半句挪出新镜
i3 = 2
body03 = shots[i3]["lines"][0]
new03 = ("走廊纵深的低机位全景，镜头从门口向后拉半步。地砖被晒出一层白亮，热浪把远处的墙线晃得发软，蝉声铺满整条走廊。"
         "中景【沈幼怡】站在门外约零点八米处，长发垂到腰、发尾被汗黏在颈侧，后背的裙子被汗浸出深色一片。"
         "【陈诚】在门内半步，视线停在【行李箱】的轮子上。后景是走廊尽头那扇窗的白。切在镜头拉到位、她垂着的肩线始终没抬。")
new04 = ("过【陈诚】肩的机位中景，镜头不动。前景是【陈诚】虚化的肩线。中景【沈幼怡】的脚趾在皮鞋里动了一下，"
         "右手把肩带往上提半寸又放下，重心从左脚换到右脚——每个动作之间都停半拍，像在门口已经站了很久。"
         "后景是走廊地砖的反光。切在她重心换回左脚、裙摆垂下去。")
shots[i3]["lines"][0] = new03
shots.insert(i3 + 1, {"title": "等了一个小时", "lines": [new04]})

# 时间表（17 镜，合计 30）
D = [1.5,1.5,1.8,1.6,2.4,2.0,1.4,1.6,1.8,1.7,1.6,3.2,1.2,1.7,1.5,2.2,0.9]
assert len(shots) == len(D), (len(shots), len(D))

t0 = 0.0
out = []
for idx, sh in enumerate(shots, 1):
    a, b = round(t0, 1), round(t0 + D[idx-1], 1)
    t0 = b
    out.append(f"【镜头{idx:02d}｜[{a:g}s-{b:g}s]｜{sh['title']}】")
    for ln in sh["lines"]:
        if not ln.strip():
            out.append(ln); continue
        if re.match(r"^\[[\d.]+s-[\d.]+s\]，", ln):
            out.append(re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", ln))
        else:
            out.append(ln)

newseg = "\n".join(pre) + "\n" + "\n".join(out).rstrip() + "\n\n"
newseg = re.sub(r"## 【第01段｜\[0s-[\d.]+s\]", "## 【第01段｜[0s-30s]", newseg)
s = s[:p1a] + newseg + s[p1b:]
open(f, "w", encoding="utf-8").write(s)
print("p01 拆分并重排为 17 镜 / 30 秒")
