# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep03_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 裸名「外卖」收纳正文（避开待补行）
s = re.sub(r"(?<!【)外卖(?!】)", "【外卖】", s)
s = s.replace("待补：【【外卖】】", "待补：【外卖】")

# 2) p08 段头改 30 秒
s = s.replace("## 【第08段｜[0s-28s]｜客厅·吹风机】", "## 【第08段｜[0s-30s]｜客厅·吹风机】")

# 3) p02 重排时间
p02_head = "## 【第02段"
p02_i = s.index(p02_head)
p02_j = s.index("## 【第03段")
seg = s[p02_i:p02_j]
new_times = [("【镜头01｜[0s-5.2s]｜三十七八度】", "[0s-5.2s]"),
             ("【镜头02｜[5.2s-7s]｜开条缝】", "[5.2s-7.8s]"),
             ("【镜头03｜[7s-9.5s]｜就这条件】", "[7.8s-9.8s]"),
             ("【镜头04｜[9.5s-11.5s]｜她听】", "[9.8s-11.3s]"),
             ("【镜头05｜[11.5s-16.5s]｜快捷酒店】", "[11.3s-18.1s]"),
             ("【镜头06｜[16.5s-18s]｜她看】", "[18.1s-19.6s]"),
             ("【镜头07｜[18s-19.5s]｜他躲】", "[19.6s-20.8s]"),
             ("【镜头08｜[19.5s-22s]｜手收紧】", "[20.8s-22s]")]
for old, new in new_times:
    name = old[old.index("｜", 6):old.index("】")]
    mm = re.search(re.escape(name) + r"】", seg)
# 直接整段重建更稳妥：按镜头序号替换头与台词窗
lines = seg.splitlines()
out = []
idx = 0
mapping = [("[0s-5.2s]", "[5.2s-7.8s]", "[7.8s-9.8s]", "[9.8s-11.3s]",
            "[11.3s-18.1s]", "[18.1s-19.6s]", "[19.6s-20.8s]", "[20.8s-22s]")]
titles = []
for ln in lines:
    m = re.match(r"^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】$", ln)
    if m:
        titles.append((int(m.group(1)), m.group(4)))
print("p02 shots:", len(titles))
open(f, "w", encoding="utf-8").write(s)
print("step1 ok")
