import json
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_example.json"
d = json.load(open(p, encoding="utf-8"))
d["props"][0]["description"] = "24寸黑色硬壳行李箱，拉杆拉出三十厘米，箱角磨损，箱体贴着两张旧航空贴纸，颜色哑光偏旧，轮子上还沾着干泥"
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_long.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
