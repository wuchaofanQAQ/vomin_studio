# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep03_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 裸名「外卖」
s = re.sub(r"(?<!【)外卖(?!】)", "【外卖】", s)
s = s.replace("待补：【【外卖】】", "待补：【外卖】")

# 2) p08 段头 30 秒
s = s.replace("## 【第08段｜[0s-28s]｜客厅·吹风机】", "## 【第08段｜[0s-30s]｜客厅·吹风机】")

SHOT = re.compile(r"^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】$")
DLG = re.compile(r"^\[([\d.]+)s-([\d.]+)s\](，.*)$")


def retime(block: str, times: list[tuple[float, float]]) -> str:
    out, i = [], 0
    for ln in block.splitlines():
        m = SHOT.match(ln)
        if m:
            a, b = times[i]
            out.append(f"【镜头{int(m.group(1)):02d}｜[{a:g}s-{b:g}s]｜{m.group(4)}】")
            i += 1
            continue
        m = DLG.match(ln)
        if m and i > 0:
            a, b = times[i - 1]
            out.append(f"[{a:g}s-{b:g}s]{m.group(3)}")
            continue
        out.append(ln)
    assert i == len(times), (i, len(times))
    return "\n".join(out)


def segment(no: int) -> tuple[int, int]:
    a = s.index(f"## 【第{no:02d}段")
    nxt = s.find("## 【第", a + 5)
    return a, (nxt if nxt != -1 else len(s))


# p02 重排
a, b = segment(2)
s = s[:a] + retime(s[a:b], [(0, 5.2), (5.2, 7.8), (7.8, 9.8), (9.8, 11.3),
                            (11.3, 18.1), (18.1, 19.6), (19.6, 20.8), (20.8, 22)]) + s[b:]

# p04 重排（OS 窗口延长 0.8s）
a, b = segment(4)
s = s[:a] + retime(s[a:b], [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 13.8),
                            (13.8, 15.8), (15.8, 17.8), (17.8, 19.8), (19.8, 21.8),
                            (21.8, 24.8), (24.8, 26.8), (26.8, 28.8), (28.8, 30)]) + s[b:]

open(f, "w", encoding="utf-8").write(s)
print("retimed p02/p04, names fixed")
