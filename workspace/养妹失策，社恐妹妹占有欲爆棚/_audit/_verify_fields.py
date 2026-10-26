import json, sys
base = sys.argv[1]
def load(p):
    s = open(p, encoding="utf-8").read()
    return json.loads(s[s.find("["):])
sb = load(base + r"\_audit\verify_storyboard.json")
for r in sorted(sb, key=lambda x: x["shot_id"]):
    print(r["shot_id"], "|", r.get("char_lock"), "|", r.get("env_lock"), "|", r.get("status"))
