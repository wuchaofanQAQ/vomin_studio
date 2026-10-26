p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v12.md"
t = open(p, encoding="utf-8").read()
old = "周围墙面、地砖与空气连续完整。"
new = "周围墙面、地砖与空气连续完整。画面内除指定屏幕文字外，不显示任何字幕、水印与台标。"
n = t.count(old)
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("declaration added to", n, "segments")
