p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_p01_dense.md"
t = open(p, encoding="utf-8").read()
t = t.replace("P01｜P01行李箱", "P01｜行李箱").replace("P02｜P02双肩书包", "P02｜双肩书包")
open(p, "w", encoding="utf-8").write(t)
print("lock names restored")
