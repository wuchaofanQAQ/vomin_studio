import sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
from vomin.workspace import Workspace
ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
tpl = """【资产锁定】
场景：【S01｜陈诚公寓门口：{场景库：陈诚公寓门口}】
角色：【R01｜沈幼怡：{角色库：沈幼怡}】【R02｜陈诚：{角色库：陈诚}】
道具：【P01｜行李箱：24 寸硬壳，拉杆拉出三十厘米】

【镜头01｜00:00-00:02｜测试】
特写固定机位，R01沈幼怡……
"""
text, imgs, chars, scenes, vids = ws.expand_prompt(tpl)
print(text)
print("chars:", chars, "scenes:", scenes)
print("imgs:", [ws.rel(p) for p in imgs])
