import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts"
t = open(os.path.join(base, "ep01_storyboard_v13.md"), encoding="utf-8").read()

# 1) 时间轴：[0s-30s] / [0s-2s] / [10s-12s]
def tm(m):
    a = int(m.group(1)) * 60 + float(m.group(2))
    b = int(m.group(3)) * 60 + float(m.group(4))
    return f"[{a:g}s-{b:g}s]"
t = re.sub(r"(\d{2}):(\d{2}(?:\.\d)?)-(\d{2}):(\d{2}(?:\.\d)?)", tm, t)

# 2) 资产锁定
lock_pairs = [
("场景：【S02｜陈诚公寓玄关：{场景库：陈诚公寓玄关}】", "【陈诚公寓玄关】：{场景库：陈诚公寓玄关}"),
("场景：【S01｜陈诚公寓走廊：{场景库：陈诚公寓走廊}】", "【陈诚公寓走廊】：{场景库：陈诚公寓走廊}"),
("角色：【R01｜沈幼怡：{角色库：沈幼怡}】", "【沈幼怡】：{角色库：沈幼怡}"),
("角色：【R02｜陈诚：{角色库：陈诚}】", "【陈诚】：{角色库：陈诚}"),
("道具：【P01｜行李箱：{道具库：行李箱}】", "【行李箱】：{道具库：行李箱}"),
("道具：【P02｜双肩书包：{道具库：双肩书包}】", "【双肩书包】：{道具库：双肩书包}"),
]
for a, b in lock_pairs:
    assert a in t, a
    t = t.replace(a, b)

# 3) 参考图映射
ID2NAME = {"S01": "陈诚公寓走廊", "S02": "陈诚公寓玄关", "R01": "沈幼怡",
           "R02": "陈诚", "P01": "行李箱", "P02": "双肩书包"}
t = re.sub(r"图(\d+)=(S\d{2}|R\d{2}|P\d{2})", lambda m: f"图{m.group(1)}=【{ID2NAME[m.group(2)]}】", t)

# 4) 正文资产名：先处理带场景前缀的，再保护长名
for a, b in (("S02 陈诚公寓玄关", "【陈诚公寓玄关】"), ("S01 陈诚公寓走廊", "【陈诚公寓走廊】"),
             ("S02陈诚公寓玄关", "【陈诚公寓玄关】"), ("S01陈诚公寓走廊", "【陈诚公寓走廊】")):
    t = t.replace(a, b)
t = t.replace("陈诚公寓", "§D")
for a, b in (("R02陈诚", "【陈诚】"), ("R01沈幼怡", "【沈幼怡】"),
             ("P01行李箱", "【行李箱】"), ("P02双肩书包", "【双肩书包】")):
    t = t.replace(a, b)
t = t.replace("§D", "陈诚公寓")

open(os.path.join(base, "ep01_storyboard_v14.md"), "w", encoding="utf-8").write(t)
print("v14 written; heads:")
for ln in t.splitlines():
    if ln.startswith("## 【第") or ln.startswith("【镜头01"):
        print(" ", ln[:60])
    if ln.startswith("## 【第02段"): break
