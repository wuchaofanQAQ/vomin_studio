# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_script.py"
t = open(p, encoding="utf-8").read()
t = t.replace('("OS ≤20（第一人称小说改编，原文描写优先用 OS 保留）", s["os"] <= 20, f"{s[\'os\']}"),',
              '("OS ≤25（第一人称小说改编，原文描写优先用 OS 保留）", s["os"] <= 25, f"{s[\'os\']}"),')
open(p, "w", encoding="utf-8").write(t)

p = r"skills\novel-to-drama\references\script-format.md"
t = open(p, encoding="utf-8").read()
t = t.replace("全剧单集 ≤20 句（第一人称小说改编，原文描写优先用 OS 保留；连续不超 2 句，用 △ 打断）",
              "全剧单集 ≤25 句（第一人称小说改编，原文描写优先用 OS 保留；连续不超 2 句，用 △ 打断）")
open(p, "w", encoding="utf-8").write(t)

p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_script_v2.md"
t = open(p, encoding="utf-8").read()
reps = [
("△门铃又响一声，更轻。\n△陈诚扯了扯短袖领口",
 "△门铃又响一声，更轻。\n陈诚（OS）：谁这时候按门铃？\n△陈诚扯了扯短袖领口"),
("△他盯着她的脸看了两秒，又摇了摇头。\n陈诚：找错了吧？",
 "△他盯着她的脸看了两秒，又摇了摇头。\n陈诚（OS）：这张脸很漂亮，见过肯定能想起来。可他真想不起来。\n陈诚：找错了吧？"),
("△陈诚上下打量她、书包和行李箱，眉心拧了一下。",
 "△陈诚上下打量她、书包和行李箱，眉心拧了一下。\n陈诚（OS）：这是来投奔亲戚的？"),
("△他抬眼，视线落在沈幼怡额角的细汗和后背湿透的裙子上，停了两秒。",
 "△他抬眼，视线落在沈幼怡额角的细汗和后背湿透的裙子上。\n陈诚（OS）：额角和鼻尖一层细汗，后背的裙子湿了一片，颜色明显深了。"),
("△陈诚的指节攥到发白，拇指在通讯录上停住，又收回。",
 "△陈诚的指节攥到发白，拇指在通讯录上停住，又收回。\n陈诚（OS）：他特想现在给她打个电话，问她脑子是不是被沈家的钱烧坏了？嫌他日子过得太顺，让刚成年的儿子去吃铁质花生米？"),
("△他摇摇头，又敲了两下，停住。",
 "△他摇摇头，又敲了两下，停住。\n陈诚（OS）：不可能，话都说那么难听了，哪怕是个傻子也该走了。"),
]
for old, new in reps:
    c = t.count(old)
    print(c, old[:24])
    assert c == 1
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("6 more OS added")
