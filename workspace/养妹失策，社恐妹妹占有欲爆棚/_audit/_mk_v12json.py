import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v12.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜.+?】)\s*$", md)
shots = []
for i in range(1, len(parts), 2):
    header = parts[i]; body = parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜([\d:.]+)-([\d:.]+)｜(.+?)】", header)
    no = int(m.group(1)); p = header + "\n\n" + body
    scene = re.findall(r"场景：【S\d{2}｜([^：】]+)：", p)
    role_line = re.search(r"角色：(.+)", p)
    roles = re.findall(r"【R\d{2}｜([^：】]+)：", role_line.group(1)) if role_line else []
    shots.append({"shot_id": f"ep01_p{no:02d}", "episode": 1, "title": m.group(4),
                  "timeline": f"{m.group(2)}-{m.group(3)}", "prompt": p, "status": "待生成",
                  "env_lock": "、".join(scene), "char_lock": "、".join(r.strip() for r in roles)})
json.dump(shots, open(os.path.join(base, "drafts", "ep01_shots_v12.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows:", len(shots))
