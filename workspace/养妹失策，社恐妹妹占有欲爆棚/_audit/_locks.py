import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
doc = json.load(open(os.path.join(base, "drafts", "ep01_storyboard_v4.json"), encoding="utf-8"))
for s in doc["shots"]:
    p = s["prompt"]
    scene = re.search(r"场景：【S\d{2}｜([^：】]+)：", p)
    roles = re.findall(r"角色：【R\d{2}｜([^：】]+)：", p)
    s["env_lock"] = scene.group(1).strip() if scene else ""
    s["char_lock"] = "、".join(r.strip() for r in roles)
json.dump(doc, open(os.path.join(base, "drafts", "ep01_storyboard_v4.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
for s in doc["shots"]:
    print(s["shot_id"], "|", s["env_lock"], "|", s["char_lock"], "|", s["timeline"])
