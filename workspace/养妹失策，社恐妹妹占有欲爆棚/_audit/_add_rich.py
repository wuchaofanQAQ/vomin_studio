# -*- coding: utf-8 -*-
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_script_v2.md"
t = open(p, encoding="utf-8").read()
old = "△他五官英挺，笑意客气，眼神却没落到任何人身上。"
new = "△他五官英挺，笑意客气，眼神却没落到任何人身上；腕上的金表和熨得笔挺的西装，跟这间旧厨房格格不入。"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("豪门 cue added")
