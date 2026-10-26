# -*- coding: utf-8 -*-
import re
md = open(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v14.md", encoding="utf-8").read()
segs = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
print("段/镜 | 陈诚视线 | 沈幼怡视线 | 门位置")
for i in range(1, len(segs), 2):
    sno = re.match(r"【第(\d+)段", segs[i]).group(1)
    for m in re.finditer(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【|\Z)", segs[i+1]):
        no, a, b, title, txt = m.groups()
        chen = re.findall(r"【陈诚】[^。；]*?(画左|画右|画外)", txt)
        shen = re.findall(r"【沈幼怡】[^。；]*?(画左|画右|画外)", txt)
        door = re.findall(r"门在(画左|画右|画面中央)", txt)
        if chen or shen or door:
            print(f"{sno}/{no} | {','.join(chen) or '-'} | {','.join(shen) or '-'} | {','.join(door) or '-'}")
