# -*- coding: utf-8 -*-
import re, json, os
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep03_storyboard_v1.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜\[0s-[\d.]+s\]｜.+?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    header, body = parts[i], parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜\[0s-([\d.]+)s\]｜(.+?)】", header)
    no, dur, title = int(m.group(1)), m.group(2), m.group(3)
    p = header + "\n\n" + body
    scenes = re.findall(r"【([^】]+)】：\{场景库", p)
    roles = re.findall(r"【([^】]+)】：\{角色库", p)
    rows.append({
        "shot_id": f"ep03_p{no:02d}", "episode": 3, "title": title,
        "timeline": f"0s-{dur}s", "prompt": p, "status": "待生成",
        "env_lock": "、".join(scenes), "char_lock": "、".join(roles),
    })
json.dump(rows, open(os.path.join(base, "drafts", "ep03_shots.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("rows:", len(rows), [r["shot_id"] for r in rows])
