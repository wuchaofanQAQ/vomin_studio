# -*- coding: utf-8 -*-
import re
for f in [r"skills\drama-segment-generation\SKILL.md",
          r"skills\drama-segment-generation\references\project-adaptation.md"]:
    t = open(f, encoding="utf-8").read()
    before = len(re.findall(r"【([^】]+)】\1", t))
    t = re.sub(r"【([^】]+)】\1", r"【\1】", t)
    open(f, "w", encoding="utf-8").write(t)
    print(f, "deduped", before)

p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
old4 = "4. **编号即身份。** 资产在【本段资产锁定】里写成 `【沈幼怡】：{角色库：沈幼怡}`；正文每次出现都写 `【沈幼怡】`，不带【】、不写裸名；同一名称跨段同号，新资产不占旧号。"
new4 = "4. **名称即身份。** 资产在【本段资产锁定】里写成 `【沈幼怡】：{角色库：沈幼怡}`（需要固定音色时写 `【陈诚】画面参考：{角色库：陈诚}，声音参考：{音色库：陈诚}`）；正文每次出现都写 `【沈幼怡】`，必须带【】、不写裸名，也不用编号。"
c = t.count(old4)
print("rule4 hit:", c)
t = t.replace(old4, new4)
open(p, "w", encoding="utf-8").write(t)
