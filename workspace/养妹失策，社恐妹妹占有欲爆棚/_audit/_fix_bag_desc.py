import json
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\_audit\ep1_assets_draft.json"
d = json.load(open(p, encoding="utf-8"))
for r in d["props"]:
    if r["name"] == "双肩书包":
        r["description"] = "鼓囊囊的双肩书包，双肩带，包身撑满"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print([r["description"] for r in d["props"] if r["name"]=="双肩书包"])

