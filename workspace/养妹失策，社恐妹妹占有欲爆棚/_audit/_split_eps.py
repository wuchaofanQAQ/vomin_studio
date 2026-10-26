import json, os, sys
p = sys.argv[1]
raw = open(p, encoding="utf-8").read()
data = json.loads(raw[raw.find("["):])
outdir = os.path.splitext(p)[0] + "_eps"
os.makedirs(outdir, exist_ok=True)
for r in data:
    ep = r.get("episode")
    open(os.path.join(outdir, f"ep{int(ep):02d}.md"), "w", encoding="utf-8").write(r.get("script",""))
    print(ep, r.get("title"), len(r.get("script","")))
