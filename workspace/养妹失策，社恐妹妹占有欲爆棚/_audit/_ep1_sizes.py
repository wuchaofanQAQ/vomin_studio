import json, sys, os, re
base = sys.argv[1]
def load(name):
    p = os.path.join(base, "_audit", name)
    s = open(p, encoding="utf-8").read()
    m = list(re.finditer(r"(?m)^\[$", s))
    start = m[-1].start() if m else s.find("[")
    return json.loads(s[start:])
ep = load("ep1_full.json")[0]
print("title:", ep.get("title"))
print("script len:", len(ep.get("script","")), "novel len:", len(ep.get("novel_text","")))
for f, key in (("lib_characters.json","chars"),("lib_scenes.json","scenes"),("lib_props.json","props")):
    rows = load(f)
    print(key, len(rows), [(r["name"], bool(r.get("ref_image"))) for r in rows])
