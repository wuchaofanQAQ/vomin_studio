p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v9.md"
t = open(p, encoding="utf-8").read()
for a, b in (("**整镜转为回忆色调**", "整镜转为回忆色调"),
             ("**延续回忆色调**", "延续回忆色调"),
             ("**画面从冷灰颗粒切回现实色调**", "画面从冷灰颗粒切回现实色调")):
    assert t.count(a) == 1, a
    t = t.replace(a, b)
assert "**" not in t, "still has markdown bold"
open(p, "w", encoding="utf-8").write(t)
print("markdown removed")
