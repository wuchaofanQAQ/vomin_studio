import json, os, sys
raw = open(sys.argv[1], encoding="utf-8").read()
data = json.loads(raw[raw.find("["):])
parts = []
for i, r in enumerate(data, 1):
    parts.append(f"## 第{i:02d}段｜{r.get('title','')}\n\n{r.get('prompt','')}\n\n---\n")
open(sys.argv[2], "w", encoding="utf-8").write("\n".join(parts))
print("segments:", len(data))
