import json
d = {
  "characters": [
    {"name": "陈诚", "status": "复用"},
    {"name": "沈幼怡", "status": "复用"}
  ],
  "scenes": [
    {"name": "陈诚公寓门口", "status": "复用"}
  ],
  "props": [
    {"name": "生日蛋糕", "status": "新建", "prop_type": "食物饮品",
     "description": "超市折扣蛋糕，圆形十八厘米，隔夜奶油，顶上一颗发蔫樱桃"}
  ],
  "reused": [{"type": "角色", "name": "陈诚", "reason": "已有形象图"}],
  "missing": []
}
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_reuse.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
