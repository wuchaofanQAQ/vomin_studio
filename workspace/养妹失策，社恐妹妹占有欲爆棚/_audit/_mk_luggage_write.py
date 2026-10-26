import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
prompt = open(os.path.join(base, "_audit", "prompt_luggage.txt"), encoding="utf-8").read().strip()
payload = [{"name": "行李箱", "gen_prompt": prompt}]
p = os.path.join(base, "_audit", "write_prop_luggage.json")
json.dump(payload, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("payload:", p)
