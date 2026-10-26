import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
doc = json.load(open(os.path.join(base, "drafts", "ep01_storyboard_v4.json"), encoding="utf-8"))
json.dump(doc["shots"], open(os.path.join(base, "drafts", "ep01_shots_only.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("rows:", len(doc["shots"]))
