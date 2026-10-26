import re
src = open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\skills\\drama-segment-generation\references\example-segment.md", encoding="utf-8").read()
b1 = src.replace("00:09-00:10.5，R02陈诚画外音（画右门板后、压低地说）：『谁啊？』",
                 "【对白 00:09-00:10.5】R02陈诚画外音（画右门板后、压低地说）：『谁啊？』")
open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\\_audit\bad_old_dlg.md", "w", encoding="utf-8").write(b1)
b2 = src.replace("【本段资产锁定】", "【本段资产锁定】\n音频参考：【R01沈幼怡】")
open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\\_audit\bad_audio.md", "w", encoding="utf-8").write(b2)
print("ok")
