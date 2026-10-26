import json, subprocess, sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\asset-image-generation\scripts")
import asset_prompt as ap
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_assetlib"
data = {
 "characters.json": [{"name":"陈诚","appearance":"18岁清瘦男生，黑色微卷中长发，白T黑短裤"}],
 "scenes.json": [{"name":"陈诚公寓门口","description":"老式公寓走廊，浅灰地砖，深灰防盗门，西端窗光，白天，无人"}],
 "props.json": [{"name":"行李箱","description":"24寸黑色硬壳行李箱，拉杆拉出，箱角磨损"}],
}
for fname, rows in data.items():
    kind = {"characters.json":"角色","scenes.json":"场景","props.json":"道具"}[fname]
    key = "appearance" if kind=="角色" else "description"
    for r in rows:
        r["gen_prompt"] = ap.build(kind, r[key])
    json.dump(rows, open(os.path.join(base, fname), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("built library")
