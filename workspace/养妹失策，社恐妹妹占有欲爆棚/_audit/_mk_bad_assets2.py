import json
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_example.json"
d = json.load(open(p, encoding="utf-8"))
d["characters"][0]["prompt"] = "18岁清瘦男生，全身正面"
d["characters"][1]["bible"]["voice_desc"] = ""
d["scenes"][0]["description"] = "一间特别有氛围感、细节丰富、让人一眼就记住的现代都市出租屋客厅，白墙浅木地板，南向落地窗，白天，无人。"
d["props"][0]["description"] = "24寸黑色硬壳行李箱，拉杆拉出三十厘米，箱角有明显磨损，箱体贴着两张旧航空贴纸，颜色偏哑光"
open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\assets_bad.json", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2))
