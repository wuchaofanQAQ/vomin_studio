import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
p = os.path.join(base, "storyboard.json")
rows = json.load(open(p, encoding="utf-8-sig"))
keep = [r for r in rows if str(r.get("shot_id", "")) != "ep01_p07"]
json.dump(keep, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("local rows:", len(rows), "->", len(keep))
