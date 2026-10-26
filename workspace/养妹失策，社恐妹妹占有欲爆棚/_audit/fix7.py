# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

reps = [
    # 段02：实际 12 镜 / 27 秒
    ("## 【第02段｜[0s-30s]｜", "## 【第02段｜[0s-27s]｜"),
    # 段04：实际 13 镜 / 27.5 秒 → 28
    ("## 【第04段｜[0s-26s]｜", "## 【第04段｜[0s-28s]｜"),
]
for a, b in reps:
    assert a in t, a
    t = t.replace(a, b)

# 镜数声明按段修正
parts = re.split(r"(?m)^(## 【第\d+段.*?】)$", t)
CN = {10:"十",11:"十一",12:"十二",13:"十三",14:"十四"}
out = [parts[0]]
i = 1
while i < len(parts):
    head, body = parts[i], parts[i+1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{CN.get(n, n)}镜按下列时码", body, count=1)
    dur = int(re.search(r"\[0s-(\d+)s\]", head).group(1))
    if n:
        body = re.sub(r"平均每镜[约\d.]+秒", f"平均每镜约{round(dur/n,1)}秒", body)
    if not n:
        out += [head, body]
        i += 3
        continue
    # 末镜收口
    ms = list(re.finditer(r"【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]", body))
    last = ms[-1]
    if abs(float(last.group(3)) - dur) > 0.05:
        body = body.replace(f"[{last.group(2)}s-{last.group(3)}s]｜", f"[{last.group(2)}s-{dur}s]｜", 1)
        body = body.replace(f"[{last.group(2)}s-{last.group(3)}s]，", f"[{last.group(2)}s-{dur}s]，", 1)
    out += [head, body]
    i += 3
t = "".join(out)

# 空间补足到 90 字以上
t = t.replace("【陈诚公寓走廊】：门已开到一掌宽，【陈诚】半张脸和肩卡在缝里，光从门缝漏到他下颌；【沈幼怡】在门外偏左、正对门，【行李箱】在脚边。机位在门外、与【陈诚】眼平齐。",
              "【陈诚公寓走廊】：门已开到一掌宽，【陈诚】半张脸和肩卡在缝里，门内是暗的，走廊白光从他脸侧切过来；【沈幼怡】在门外偏左、正对门，【行李箱】在脚边、拉杆拉出，【双肩书包】挂右肩。机位在门外、与【陈诚】眼平齐，略侧向门缝。")
t = t.replace("【陈诚公寓走廊】：门大开约一肩宽，【陈诚】侧身站在门内、刚把【行李箱】拎离地面；【沈幼怡】在门外半步、正面朝门。机位在门外、略低于【陈诚】下巴。",
              "【陈诚公寓走廊】：门大开约一肩宽，门板朝画左；【陈诚】侧身站在门内、右手刚把【行李箱】拎离地面，左手还搭在门把上；【沈幼怡】在门外半步、正面朝门，【双肩书包】挂右肩。机位在门外、略低于【陈诚】下巴。")

open(f, "w", encoding="utf-8").write(t)
print("修完")
