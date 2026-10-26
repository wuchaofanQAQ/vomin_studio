p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\storyboard_v2_payload.json"
import json
rows = json.load(open(p, encoding="utf-8"))
env = {
 "ep01_p01": "陈诚公寓门口",
 "ep01_p02": "陈诚公寓门口",
 "ep01_p03": "陈诚公寓门口",
 "ep01_p04": "陈诚公寓门口",
 "ep01_p05": "陈诚公寓玄关客厅（日）、陈诚公寓门口",
 "ep01_p06": "陈诚公寓玄关客厅（日）",
}
for r in rows:
    r["env_lock"] = env[r["shot_id"]]
json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for r in rows:
    print(r["shot_id"], r["timeline"], r["env_lock"], len(r["prompt"]))
