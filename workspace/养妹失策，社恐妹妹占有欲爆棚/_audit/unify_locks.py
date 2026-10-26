# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read()

FULL = """【本段资产锁定】
角色：
图1 =【沈幼怡】  {资产库：沈幼怡}；
图2 =【陈诚】  {资产库：陈诚}；
场景：
图3 =【陈诚公寓走廊】  {资产库：陈诚公寓走廊}；
图4 =【陈诚公寓玄关】  {资产库：陈诚公寓玄关}；
图5 =【陈诚公寓客厅】  {资产库：陈诚公寓客厅}；
道具：
图6 =【行李箱】  {资产库：行李箱}；
图7 =【双肩书包】  {资产库：双肩书包}；
图8 =【手机】  {资产库：手机}；"""

CN = {8:"八",9:"九",10:"十",11:"十一",12:"十二",13:"十三",14:"十四",15:"十五"}
parts = re.split(r"(?m)^(## 【第\d+段｜\[0s-(\d+)s\]｜.*?】)$", t)
out, i = [parts[0]], 1
while i < len(parts):
    head, dur, body = parts[i], int(parts[i+1]), parts[i+2]
    body = re.sub(r"(?ms)【本段资产锁定】\n.*?(?=\n【本段现场生成】)", FULL, body, count=1)
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{CN.get(n, n)}镜按下列时码", body, count=1)
    ms = list(re.finditer(r"【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]", body))
    last = ms[-1]
    body = body.replace(f"[{last.group(2)}s-{last.group(3)}s]｜", f"[{last.group(2)}s-{dur}s]｜", 1)
    body = body.replace(f"[{last.group(2)}s-{last.group(3)}s]，", f"[{last.group(2)}s-{dur}s]，", 1)
    out += [head, body]
    i += 3
open(f, "w", encoding="utf-8").write("".join(out))
print("统一锁定 + 镜数 + 段尾")
