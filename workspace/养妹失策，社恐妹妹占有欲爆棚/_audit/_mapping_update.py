p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard.md"
t = open(p, encoding="utf-8").read()
reps = [
("| 【陈诚公寓玄关客厅（日）】 | 场景 | 场景库：陈诚公寓玄关客厅（日） | 已有（ref/scenes/陈诚公寓玄关客厅（日）_资料板_20261024_134029.jpg） |",
 "| 【陈诚公寓玄关客厅（日）】 | 场景 | 场景库：陈诚公寓玄关客厅（日） | 已有（ref/scenes/陈诚公寓玄关.jpg） |"),
("2. 玄关客厅的参考图目前指向 22:9 五视角资料板（画面内含「正视图/东视角/南视角/西视角/北视角」标签）。同目录已有干净的 `陈诚公寓客厅.jpg` 与 `陈诚公寓玄关.jpg`，只需把场景库的 `文件路径` 换一行即可，不需要重出图。",
 "2. 玄关客厅参考图已于 2026-10-24 换成单张反打图 `陈诚公寓玄关.jpg`（16:9、无文字、无标签），不再使用 22:9 五视角资料板。"),
]
for old, new in reps:
    c = t.count(old)
    print("count=", c)
    assert c == 1
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("draft mapping updated")
