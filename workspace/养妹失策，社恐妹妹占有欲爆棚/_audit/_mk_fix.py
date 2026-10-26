import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
row = [{"name": "行李箱", "ref_image": "ref/props/行李箱_20261024_175214.jpg", "gen_status": "已出图"}]
json.dump(row, open(os.path.join(base, "_audit", "fix_prop_luggage.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
