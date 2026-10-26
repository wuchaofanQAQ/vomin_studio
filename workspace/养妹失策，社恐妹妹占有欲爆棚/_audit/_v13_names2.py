import re
p = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v13.md"
t = open(p, encoding="utf-8").read()
t = t.replace("【P02双肩书包：{道具库：双肩书包}】", "【P02｜双肩书包：{道具库：双肩书包}】")
protect = {
 "P01｜行李箱": "§1", "{道具库：行李箱}": "§2", "P01行李箱": "§3",
 "P02｜双肩书包": "§4", "{道具库：双肩书包}": "§5", "P02双肩书包": "§6",
 "R01｜沈幼怡": "§7", "{角色库：沈幼怡}": "§8", "R01沈幼怡": "§9",
 "R02｜陈诚": "§A", "{角色库：陈诚}": "§B", "R02陈诚": "§C",
 "陈诚公寓": "§D",
}
for k, v in protect.items():
    t = t.replace(k, v)
t = re.sub(r"(?<!P01)行李箱", "P01行李箱", t)
t = re.sub(r"(?<!P02)双肩书包", "P02双肩书包", t)
t = re.sub(r"(?<!R01)沈幼怡", "R01沈幼怡", t)
t = re.sub(r"(?<!R02)陈诚", "R02陈诚", t)
for k, v in protect.items():
    t = t.replace(v, k)
open(p, "w", encoding="utf-8").write(t)
print("written; sample:", [l for l in t.splitlines() if "行李箱立在她" in l][:1])
