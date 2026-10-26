p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v4.md"
t = open(p, encoding="utf-8").read()
t = t.replace("陈诚公寓玄关客厅·", "陈诚公寓客厅·")
t = t.replace("下一段回到门口。", "下一段回到走廊。")
open(p, "w", encoding="utf-8").write(t)
print("titles aligned")
