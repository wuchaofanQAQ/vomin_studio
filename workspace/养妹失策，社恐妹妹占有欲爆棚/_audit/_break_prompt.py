import json, os
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_assetlib"
p = os.path.join(base, "scenes.json")
rows = json.load(open(p, encoding="utf-8"))
rows[0]["gen_prompt"] = rows[0]["gen_prompt"].replace("占画面 70% 以上", "")
json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
