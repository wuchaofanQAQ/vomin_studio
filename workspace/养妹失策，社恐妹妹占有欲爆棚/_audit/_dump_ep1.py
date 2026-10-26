import json, sys, os, re
base = sys.argv[1]
p = os.path.join(base, "_audit", "ep1_full.json")
s = open(p, encoding="utf-8").read()
m = list(re.finditer(r"(?m)^\[$", s))
ep = json.loads(s[m[-1].start():])[0]
open(os.path.join(base, "_audit", "ep1_script.txt"), "w", encoding="utf-8").write(ep.get("script",""))
open(os.path.join(base, "_audit", "ep1_novel.txt"), "w", encoding="utf-8").write(ep.get("novel_text",""))
print("written")
