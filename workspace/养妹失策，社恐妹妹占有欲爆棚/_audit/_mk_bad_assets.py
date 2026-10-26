# -*- coding: utf-8 -*-
import json
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_example.json"
d = json.load(open(p, encoding="utf-8"))
d["characters"][0]["prompt"] = "【任务】制作角色三视图，18岁清瘦男生，黑色微卷中长发，白T黑短裤人字拖，8K超清电影感，全身正面站姿"
d["characters"][0]["bible"]["voice_desc"] = ""
d["scenes"][0]["description"] = "一个走廊"
d["props"].append(dict(d["props"][0]))
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_bad.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
