import json, sys
base = sys.argv[1]
s = open(base + r"\_audit\verify_scenes.json", encoding="utf-8").read()
sc = json.loads(s[s.find("["):])
for r in sc:
    if r["name"] == "陈诚公寓玄关客厅（日）":
        print("name:", r["name"])
        print("ref_image:", r.get("ref_image"))
        print("desc chars:", len(r.get("description","")))
        print("gen_prompt chars:", len(r.get("gen_prompt","")))
        print("gen_status:", r.get("gen_status"), "| consistency:", r.get("consistency"), "| related:", r.get("related_episodes"))
