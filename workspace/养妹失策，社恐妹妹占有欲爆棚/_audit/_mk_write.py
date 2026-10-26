import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
scene = [{
  "name": "陈诚童年家厨房（日）",
  "description": "老式厨房，餐桌，冷灰低饱和，白天，无人",
  "relation_note": "第1集场3 闪回；仅用于回忆时空，不用于现实时空",
  "related_episodes": "1",
  "source": "AIGC生成"
}]
props = [
  {"name": "行李箱", "prop_type": "手持道具", "description": "行李箱，拉杆拉出，立在脚边", "related_episodes": "1,2,3", "source": "AIGC生成"},
  {"name": "双肩书包", "prop_type": "服装配饰", "description": "鼓囊囊的双肩书包，双肩带，包身撑满", "related_episodes": "1,2,3", "source": "AIGC生成"},
  {"name": "生日蛋糕", "prop_type": "食物饮品", "description": "超市打折的隔夜植物奶油蛋糕，顶一颗发蔫樱桃，插着蜡烛", "related_episodes": "1", "source": "AIGC生成"}
]
json.dump(scene, open(os.path.join(base, "_audit", "write_scenes_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(props, open(os.path.join(base, "_audit", "write_props_ep1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("payloads ready")
