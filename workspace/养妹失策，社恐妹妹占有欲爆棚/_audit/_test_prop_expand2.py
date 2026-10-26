# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from vomin.workspace import Workspace
root = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(root); ws.feishu = None
ws.save_json("props.json", [{"name": "行李箱", "ref_image": "ref/scenes/陈诚公寓走廊.jpg"}])
ws._cache.pop("props", None)
tpl = "【资产锁定】\n道具：【P01｜行李箱：24 寸硬壳，{道具库：行李箱}】\n角色：【R01｜沈幼怡：{角色库：沈幼怡}】"
text, imgs, *_ = ws.expand_prompt(tpl)
print(text)
print([ws.rel(p) for p in imgs])
os.remove(ws.abs("props.json"))
