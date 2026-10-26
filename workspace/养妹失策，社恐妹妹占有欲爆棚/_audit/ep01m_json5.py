# -*- coding: utf-8 -*-
import re, json, os
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜\[0s-[\d.]+s\]｜.+?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    header, body = parts[i], parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜\[0s-([\d.]+)s\]｜(.+?)】", header)
    no, dur, title = int(m.group(1)), float(m.group(2)), m.group(3)
    rows.append({
        "shot_id": f"ep01_p{no:02d}", "episode": 1, "title": title,
        "timeline": f"0s-{dur:g}s", "prompt": header + "\n\n" + body, "status": "待生成",
    })
json.dump(rows, open(os.path.join(base, "drafts", "ep01m_shots.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("rows:", len(rows), [r["shot_id"] for r in rows])
print("durations:", [r["timeline"] for r in rows], "total", sum(float(r["timeline"].split("-")[1][:-1]) for r in rows))
