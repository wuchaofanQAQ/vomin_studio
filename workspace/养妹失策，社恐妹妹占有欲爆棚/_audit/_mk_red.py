import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
prompt = open(os.path.join(base, "_audit", "prompt_luggage_red.txt"), encoding="utf-8").read().strip()
row = [{"name": "行李箱",
        "description": "酒红色亮面硬壳行李箱，24寸，玫瑰金包角，拉杆拉出",
        "gen_prompt": prompt}]
json.dump(row, open(os.path.join(base, "_audit", "write_luggage_red.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("payload ok")
