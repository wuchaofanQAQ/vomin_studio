import json
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\storyboard_v2_payload.json"
rows = json.load(open(p, encoding="utf-8"))
for r in rows:
    print(r["shot_id"], r["timeline"], len(r["prompt"]), "| 15.5-16.5 麻烦" in r["prompt"] or "-")
