import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v13.md"), encoding="utf-8").read()
lines = re.findall(r"^\d{2}:\d{2}(?:\.\d)?-\d{2}:\d{2}(?:\.\d)?，(.+?)：(.+)$", md, re.M)
texts = [l[1].strip() for l in lines]
dups = [t for t in set(texts) if texts.count(t) > 1]
print("台词行:", len(lines), "| 重复台词:", len(dups))
print("字幕声明段数:", md.count("不显示任何字幕"))
moves = ["推进", "拉远", "横移", "摇", "环绕", "跟拍", "升降", "推近", "后拉"]
bad = [l for l in md.splitlines() if l.startswith("硬切") and sum(m in l for m in moves) >= 2]
print("复合运镜镜头:", len(bad))
