import os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
p1 = open(os.path.join(base, "drafts", "ep01_p01_dense.md"), encoding="utf-8").read().strip()
p2 = open(os.path.join(base, "drafts", "_p0203.md"), encoding="utf-8").read().strip()
p3 = open(os.path.join(base, "drafts", "_p0405.md"), encoding="utf-8").read().strip()
p4 = open(os.path.join(base, "drafts", "_p0607.md"), encoding="utf-8").read().strip()
out = "\n\n".join([p1, p2, p3, p4])
open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), "w", encoding="utf-8").write(out + "\n")
print("v12 chars:", len(out))
