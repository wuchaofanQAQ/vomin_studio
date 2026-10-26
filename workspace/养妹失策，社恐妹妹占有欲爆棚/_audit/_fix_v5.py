p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v5.md"
t = open(p, encoding="utf-8").read()
t = t.replace("R02陈诚（盯着行李箱、低声问）：", "R02陈诚（盯着行李箱、低声说）：")
t = t.replace("R02陈诚（OS、轻声问）：", "R02陈诚（OS、轻声说）：")
t = t.replace("落幅停在行李箱停稳的位置", "落幅停在 P01行李箱停稳的位置")
open(p, "w", encoding="utf-8").write(t)
print("fixed")
