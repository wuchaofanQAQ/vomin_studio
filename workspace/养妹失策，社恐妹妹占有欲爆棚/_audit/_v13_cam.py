p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v13.md"
t = open(p, encoding="utf-8").read()
old = "硬切近景，镜头随她低头轻轻下压。"
new = "硬切近景，镜头随她低头缓缓下摇。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("camera word fixed")
