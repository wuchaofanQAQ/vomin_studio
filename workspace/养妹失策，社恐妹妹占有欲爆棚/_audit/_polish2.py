p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard.md"
t = open(p, encoding="utf-8").read()
reps = [
 ("玄关与客厅同为浅色木纹地板，木地板一直铺到门口，没有材质分界；客厅东墙南段靠白色布艺沙发",
  "玄关与客厅之间是一道无门原木门框门洞，两处同为浅色木纹地板，木地板一直铺到门口，没有材质分界；客厅东墙南段靠白色布艺沙发"),
 ("两人隔着门洞的墙体与地面的光影站着",
  "两人隔着玄关与客厅之间的木框门洞、以及地面的光影站着"),
]
for old, new in reps:
    c = t.count(old)
    print(f"count={c}")
    assert c == 1
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("ok")
