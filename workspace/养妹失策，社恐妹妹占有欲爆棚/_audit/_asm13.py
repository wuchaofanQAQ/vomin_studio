import os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts"
parts = ["_v13_p01.md", "_v13_p02p04.md", "_v13_p05p07.md"]
out = []
for p in parts:
    out.append(open(os.path.join(base, p), encoding="utf-8").read().strip())
open(os.path.join(base, "ep01_storyboard_v13.md"), "w", encoding="utf-8").write("\n\n".join(out) + "\n")
print("assembled")
