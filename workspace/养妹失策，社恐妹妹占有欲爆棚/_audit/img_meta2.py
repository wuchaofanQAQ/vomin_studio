# -*- coding: utf-8 -*-
import os
from PIL import Image
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
for f in ["ref/characters/沈幼怡.jpg", "ref/characters/陈诚.jpg",
          "ref/scenes/陈诚公寓玄关.jpg", "ref/scenes/陈诚公寓走廊.jpg"]:
    p = os.path.join(base, f)
    im = Image.open(p)
    exif = im.getexif()
    print(f, im.size, im.mode, "exif entries:", len(exif), "bytes:", os.path.getsize(p))
