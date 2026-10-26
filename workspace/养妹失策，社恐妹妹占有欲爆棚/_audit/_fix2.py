p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard.md"
t = open(p, encoding="utf-8").read()
old = "屏幕朝北对着她的脸、也正对镜头"
new = "屏幕朝北对着【沈幼怡】的脸、也正对镜头"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("ok")
