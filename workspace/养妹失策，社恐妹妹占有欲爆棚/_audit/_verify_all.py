import json, sys
base = sys.argv[1]
def load(p):
    s = open(p, encoding="utf-8").read()
    return json.loads(s[s.find("["):])
sb = load(base + r"\_audit\verify_storyboard.json")
for r in sorted(sb, key=lambda x: x["shot_id"]):
    print(r["shot_id"], r.get("timeline"), len(r.get("prompt","")), r.get("title"))
sc = load(base + r"\_audit\verify_scenes.json")
for s in sc:
    if s["name"].startswith("陈诚公寓玄关客厅（日）"):
        print("REF:", s["name"], "->", s.get("ref_image"))
