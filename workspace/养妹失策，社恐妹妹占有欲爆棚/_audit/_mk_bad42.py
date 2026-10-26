import re
src = open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\skills\\drama-segment-generation\references\example-segment.md", encoding="utf-8").read()
# 1) 去掉终态
bad1 = re.sub(r"\n【本段终态】.*", "", src, flags=re.S)
open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\\_audit\bad_no_final.md", "w", encoding="utf-8").write(bad1)
# 2) 待补写成已绑定
bad2 = src.replace("待补：【P02｜门铃面板：待补，未读取】", "待补：【P02｜门铃面板：{道具库：门铃面板}】")
open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\\_audit\bad_pending.md", "w", encoding="utf-8").write(bad2)
print("ok")
