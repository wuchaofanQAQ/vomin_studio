import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v4.md"), encoding="utf-8").read()

parts = re.split(r"(?m)^## (【第\d+段｜.+?】)\s*$", md)
shots = []
for i in range(1, len(parts), 2):
    header = parts[i]
    body = parts[i + 1].strip()
    m = re.match(r"【第(\d+)段｜([\d:.]+)-([\d:.]+)｜(.+?)】", header)
    no = int(m.group(1)); start = m.group(2); end = m.group(3); title = m.group(4)
    shots.append({
        "shot_id": f"ep01_p{no:02d}",
        "episode": 1,
        "title": title,
        "timeline": f"{start}-{end}",
        "prompt": header + "\n\n" + body,
        "status": "待生成",
    })

deps = {
    "scenes": [{"name": "陈诚公寓门口", "image": True},
               {"name": "陈诚公寓玄关客厅（日）", "image": True},
               {"name": "陈诚童年家厨房（日）", "image": False}],
    "characters": ["沈幼怡", "陈诚", "林女士", "沈崇山"],
    "props": [{"name": "行李箱", "image": True},
              {"name": "双肩书包", "image": True},
              {"name": "生日蛋糕", "image": False}],
    "missing": [{"type": "角色", "name": "陈诚 12岁", "reason": "剧本只写'小陈诚'，库里没有；闪回只入侧背"}],
    "pending_images": [{"type": "场景", "name": "陈诚童年家厨房（日）"},
                       {"type": "道具", "name": "生日蛋糕"}],
}
ids = [
    {"id": "S01", "category": "场景", "name": "陈诚公寓门口", "table": "场景库", "has_image": True},
    {"id": "S02", "category": "场景", "name": "陈诚公寓玄关客厅（日）", "table": "场景库", "has_image": True},
    {"id": "S03", "category": "场景", "name": "陈诚童年家厨房（日）", "table": "场景库", "has_image": False},
    {"id": "R01", "category": "角色", "name": "沈幼怡", "table": "角色库", "has_image": True},
    {"id": "R02", "category": "角色", "name": "陈诚", "table": "角色库", "has_image": True},
    {"id": "R03", "category": "角色", "name": "林女士", "table": "角色库", "has_image": True},
    {"id": "R04", "category": "角色", "name": "沈崇山", "table": "角色库", "has_image": True},
    {"id": "R05", "category": "角色", "name": "陈诚 12岁", "table": "", "has_image": False, "pending": True},
    {"id": "P01", "category": "道具", "name": "行李箱", "table": "道具库", "has_image": True},
    {"id": "P02", "category": "道具", "name": "双肩书包", "table": "道具库", "has_image": True},
    {"id": "P03", "category": "道具", "name": "生日蛋糕", "table": "道具库", "has_image": False},
]
json.dump({"shots": shots, "dependencies": deps, "asset_ids": ids},
          open(os.path.join(base, "drafts", "ep01_storyboard_v4.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
json.dump({"assets": ids}, open(os.path.join(base, "drafts", "asset_ids.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("shots:", len(shots), [ (s["shot_id"], s["timeline"], s["title"]) for s in shots ])
