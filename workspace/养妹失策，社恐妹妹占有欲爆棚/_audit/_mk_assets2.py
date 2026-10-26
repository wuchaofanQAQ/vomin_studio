# -*- coding: utf-8 -*-
import re, json
src = open(r"skills\script-asset-extraction\references\examples.md", encoding="utf-8").read()
m = re.search(r"```json\n(.*?)\n```", src, re.S)
doc = json.loads(m.group(1))
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_example.json", "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=2))
print("chars:", len(doc["characters"]), "scenes:", len(doc["scenes"]), "props:", len(doc["props"]))
