import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v5.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (【第\d+段｜.+?】)\s*$", md)
shots = []
for i in range(1, len(parts), 2):
    header = parts[i]; body = parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜([\d:.]+)-([\d:.]+)｜(.+?)】", header)
    no = int(m.group(1))
    p = header + "\n\n" + body
    scene = re.search(r"场景：【S\d{2}｜([^：】]+)：", p)
    role_line = re.search(r"角色：(.+)", p)
    roles = re.findall(r"【R\d{2}｜([^：】]+)：", role_line.group(1)) if role_line else []
    shots.append({
        "shot_id": f"ep01_p{no:02d}", "episode": 1, "title": m.group(4),
        "timeline": f"{m.group(2)}-{m.group(3)}", "prompt": p, "status": "待生成",
        "env_lock": scene.group(1).strip() if scene else "闪回（无场景资产）",
        "char_lock": "、".join(r.strip() for r in roles),
    })
deps = {
    "scenes": [{"name": "陈诚公寓走廊"}, {"name": "陈诚公寓客厅"}],
    "characters": ["沈幼怡", "陈诚", "林女士", "沈崇山"],
    "props": ["行李箱", "双肩书包"],
    "missing": [], "pending_images": [],
}
ids = [
    {"id": "S01", "category": "场景", "name": "陈诚公寓走廊", "table": "场景库", "has_image": True},
    {"id": "S02", "category": "场景", "name": "陈诚公寓客厅", "table": "场景库", "has_image": True},
    {"id": "R01", "category": "角色", "name": "沈幼怡", "table": "角色库", "has_image": True},
    {"id": "R02", "category": "角色", "name": "陈诚", "table": "角色库", "has_image": True},
    {"id": "R03", "category": "角色", "name": "林女士", "table": "角色库", "has_image": True},
    {"id": "R04", "category": "角色", "name": "沈崇山", "table": "角色库", "has_image": True},
    {"id": "P01", "category": "道具", "name": "行李箱", "table": "道具库", "has_image": True},
    {"id": "P02", "category": "道具", "name": "双肩书包", "table": "道具库", "has_image": True},
]
json.dump({"shots": shots, "dependencies": deps, "asset_ids": ids},
          open(os.path.join(base, "drafts", "ep01_storyboard_v5.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(shots, open(os.path.join(base, "drafts", "ep01_shots_v5.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows:", len(shots))
