import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v14.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5\uff5c\[0s-[\d.]+s\]\uff5c.+?\u3011)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    header = parts[i]; body = parts[i + 1].strip()
    m = re.match(r"\u3010\u7b2c(\d+)\u6bb5\uff5c\[0s-([\d.]+)s\]\uff5c(.+?)\u3011", header)
    no = int(m.group(1)); dur = m.group(2); p = header + "\n\n" + body
    scenes = re.findall(r"\u3010([^\u3011]+)\u3011\uff1a\{\u573a\u666f\u5e93", p)
    roles = re.findall(r"\u3010([^\u3011]+)\u3011\uff1a\{\u89d2\u8272\u5e93", p)
    rows.append({"shot_id": f"ep01_p{no:02d}", "episode": 1, "title": m.group(3),
                 "timeline": f"0s-{dur}s", "prompt": p, "status": "\u5f85\u751f\u6210",
                 "env_lock": "\u3001".join(scenes), "char_lock": "\u3001".join(roles)})
json.dump(rows, open(os.path.join(base, "drafts", "ep01_shots_v14.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows:", len(rows))
for r in rows: print(" ", r["shot_id"], r["timeline"], r["title"], "|", r["env_lock"], "|", r["char_lock"])
