# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 裸名收纳（只处理正文行，跳过锁定/映射行）
out = []
for ln in s.splitlines():
    if ln.startswith("【") and ("】：" in ln or "参考图映射" in ln):
        out.append(ln); continue
    for name in ("沈幼怡", "陈诚", "手机", "玻璃杯", "行李箱", "双肩书包", "黑拖鞋"):
        ln = re.sub(r"(?<!【)" + name + r"(?!】)", "【" + name + "】", ln)
    out.append(ln)
s = "\n".join(out)
s = s.replace("【【", "【").replace("】】", "】")

SHOT = re.compile(r"^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】$")
DLG = re.compile(r"^\[([\d.]+)s-([\d.]+)s\](，.*)$")

def retime(block, times):
    out, i = [], 0
    for ln in block.splitlines():
        m = SHOT.match(ln)
        if m:
            a, b = times[i]
            out.append(f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】")
            i += 1; continue
        m = DLG.match(ln)
        if m and i > 0:
            a, b = times[i - 1]
            out.append(f"[{a:g}s-{b:g}s]{m.group(3)}"); continue
        out.append(ln)
    assert i == len(times), (i, len(times))
    return "\n".join(out)

def seg(no):
    a = s.index(f"## 【第{no:02d}段")
    b = s.find("## 【第", a + 5)
    return a, (b if b != -1 else len(s))

# p01: 14 镜，OS 旧疤给 3.6s
a, b = seg(1)
s = s[:a] + retime(s[a:b], [(0,1.5),(1.5,3),(3,4.5),(4.5,6),(6,8),(8,10),(10,12),(12,13.5),
                            (13.5,17.1),(17.1,19.1),(19.1,21.1),(21.1,23.1),(23.1,26),(26,28)]) + s[b:]

# p02: 13 镜
a, b = seg(2)
s = s[:a] + retime(s[a:b], [(0,2),(2,4),(4,8),(8,9.5),(9.5,11.5),(11.5,13.5),(13.5,15.5),
                            (15.5,17),(17,21.5),(21.5,23),(23,26),(26,27),(27,28)]) + s[b:]

# p04: 12 镜，段长 28
s = s.replace("## 【第04段｜[0s-27s]｜客厅·叫我陈诚】", "## 【第04段｜[0s-28s]｜客厅·叫我陈诚】")
a, b = seg(4)
s = s[:a] + retime(s[a:b], [(0,1.6),(1.6,5.6),(5.6,7.1),(7.1,8.6),(8.6,10.6),(10.6,13.6),
                            (13.6,15.6),(15.6,17.1),(17.1,19.1),(19.1,22.6),(22.6,25.1),(25.1,28)]) + s[b:]

# 镜数声明
cn = {11:"十一", 12:"十二", 13:"十三", 14:"十四"}
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn.get(n, n)}镜按下列时码", body, count=1)
    out += [head, body]
s = out[0] + "".join("## " + h + "\n" + b for h, b in zip(out[1::2], out[2::2]))

# p04 两个短镜补字
s = s.replace("前景是手机边缘，中景是他的眼睛，后景是暗客厅。切在他嘴角落下时。",
              "前景是手机边缘与她的拇指，中景是他的眼睛与鼻梁，后景是暗下来的客厅。切在他嘴角落下、笑意收干净时。")
s = s.replace("前景是他的下颌，中景是眼睛，后景是暗部。切在他把话说完、嘴唇还抿着时。",
              "前景是他的下颌与颈侧，中景是盯着她的眼睛，后景是落地灯照不到的一片暗。切在他把话说完、嘴唇还抿着时。")
open(f, "w", encoding="utf-8").write(s)
print("fixed")
