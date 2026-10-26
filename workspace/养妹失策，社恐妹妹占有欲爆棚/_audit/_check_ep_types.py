import json
d = json.load(open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\storyboard.json", encoding="utf-8"))
for r in d:
    print(r["shot_id"], repr(r.get("episode")), type(r.get("episode")).__name__, len(r.get("prompt","")))
