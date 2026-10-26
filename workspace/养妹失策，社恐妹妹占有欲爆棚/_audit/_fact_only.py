import json, os
p = os.path.join(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚", "_audit", "ep1_assets_draft.json")
d = json.load(open(p, encoding="utf-8-sig"))
for s in d["scenes"]:
    if s["name"] == "陈诚童年家厨房（日）":
        s["description"] = "老式厨房，餐桌，冷灰低饱和，白天，无人"
for r in d["props"]:
    if r["name"] == "行李箱":
        r["description"] = "行李箱，拉杆拉出，立在脚边"
    if r["name"] == "生日蛋糕":
        r["description"] = "超市打折的隔夜植物奶油蛋糕，顶一颗发蔫樱桃，插着蜡烛"
with open(p, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print("scene:", d["scenes"][2]["description"])
print("props:", [r["description"] for r in d["props"]])
