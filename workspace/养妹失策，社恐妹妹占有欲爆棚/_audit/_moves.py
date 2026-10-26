import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), encoding="utf-8").read()
moves = ["推进", "拉远", "横移", "摇", "环绕", "跟拍", "升降", "推近", "后拉"]
bad = []
for ln in md.splitlines():
    if not ln.startswith("硬切"): continue
    hit = [m for m in moves if m in ln]
    if len(hit) >= 2: bad.append((hit, ln[:40]))
print("复合运镜镜头数:", len(bad))
for b in bad[:6]: print(" ", b[0], b[1])
