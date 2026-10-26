# -*- coding: utf-8 -*-
import re
md = open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v7.md", encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜.+?】)\s*$", md)
segs = [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]
print("v7 segs:", [h[:12] for h, _ in segs])

merged_header = "【第01段｜00:00-00:30｜陈诚公寓玄关·门铃与手机】"
merged_body = open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\_audit\_merged_p01.txt", encoding="utf-8").read().strip()

mapping = {3: 2, 4: 3, 5: 4, 6: 5, 7: 6}
out = [f"## {merged_header}\n\n{merged_body}\n"]
for h, b in segs[2:]:
    no = int(re.match(r"【第(\d+)段", h).group(1))
    nh = re.sub(r"【第\d+段", f"【第{mapping[no]:02d}段", h, count=1)
    out.append(f"## {nh}\n\n{b.strip()}\n")
open(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v8.md", "w", encoding="utf-8").write("\n".join(out))
print("v8 rebuilt")
