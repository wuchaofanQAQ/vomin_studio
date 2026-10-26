# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep03_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
cn = {1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",10:"十",
      11:"十一",12:"十二",13:"十三",14:"十四",15:"十五",16:"十六",17:"十七",18:"十八"}

# 1) 镜数声明按实际
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
out = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i + 1]
    n = len(re.findall(r"^【镜头\d+", body, re.M))
    body = re.sub(r"[一二三四五六七八九十]+镜按下列时码", f"{cn.get(n, n)}镜按下列时码", body, count=1)
    out += [head, body]
s = out[0] + "".join("## " + h + "\n" + b for h, b in zip(out[1::2], out[2::2]))

# 2) p02/p03 去掉没用的待补外卖
a = s.index("## 【第02段"); b = s.index("## 【第04段")
seg = s[a:b].replace("待补：【外卖】\n", "")
s = s[:a] + seg + s[b:]

# 3) 两处过短镜头补字
s = s.replace("前景是手指与盒边，中景是汤碗，后景全虚。切在他手指停在盒边不动时。",
              "前景是他的手指与饭盒边，中景是那碗汤与碗口的塑料膜，后景全虚。切在他手指停在盒边不动、视线还没收回来时。")
s = s.replace("前景是遥控器与他的手，中景是他的侧脸，后景是暖灯。切在他把话说完、手收回来时。",
              "前景是遥控器与他的手，中景是他的侧脸与下颌，后景是暖灯下的一片暗。切在他把话说完、手收回来时。")
open(f, "w", encoding="utf-8").write(s)
print("counts + bodies fixed")
