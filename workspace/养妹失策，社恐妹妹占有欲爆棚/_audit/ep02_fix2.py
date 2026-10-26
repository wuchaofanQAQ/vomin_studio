# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep02_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) p05 镜头09 括号笔误
s = s.replace("【镜头09｜[20.5s-22.5s]｜站着》", "【镜头09｜[20.5s-22.5s]｜站着】")

# 2) 裸名收纳
for name in ["黑拖鞋", "粉色四件套", "外卖"]:
    s = re.sub(r"(?<!【)" + name + r"(?!】)", "【" + name + "】", s)
# 沈幼怡 裸名只在正文出现处收，不动锁定/待补行
s = re.sub(r"(?<![【R\d])(?<!库：)沈幼怡(?!】)", "【沈幼怡】", s)
s = s.replace("【【沈幼怡】】", "【沈幼怡】").replace("【沈幼怡】】：", "【沈幼怡】：")

# 3) 镜数声明按实际镜头数修正
cn = {1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",10:"十",
      11:"十一",12:"十二",13:"十三",14:"十四",15:"十五",16:"十六",17:"十七",18:"十八"}
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn.get(n, n)}镜按下列时码", body, count=1)
    out.append(head); out.append(body)
s = "\n## ".join([out[0]] + [h + "\n" + b for h, b in zip(out[1::2], out[2::2])])
open(f, "w", encoding="utf-8").write(s)
print("mechanical fixes applied")
