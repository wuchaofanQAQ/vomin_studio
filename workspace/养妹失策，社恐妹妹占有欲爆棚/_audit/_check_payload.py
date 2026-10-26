import json
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\storyboard_v2_payload.json"
rows = json.load(open(p, encoding="utf-8"))
for r in rows:
    print(r["shot_id"], len(r["prompt"]),
          "护角" in r["prompt"], "包口被撑" in r["prompt"],
          "木框门洞、以及" in r["prompt"], "画面左侧后景" in r["prompt"])
