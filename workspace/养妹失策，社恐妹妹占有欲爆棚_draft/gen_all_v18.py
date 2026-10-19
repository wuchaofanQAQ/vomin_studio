# -*- coding: utf-8 -*-
"""画风 v18：女主改回 v7 原版（无桃花眼）；男主 v14 清秀化。只更新陈诚+沈幼怡。"""
import json, io

DRAFT = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚_draft"

# 女主 = v7 原文
shen = json.load(io.open(DRAFT + r"\chars_v7.json", encoding="utf-8"))[0]["gen_prompt"]

# 男主 = v14 原文 + 清秀化（仅改面部/气质两段，其余逐字保留）
chen_base = json.load(io.open(DRAFT + r"\chars_v14.json", encoding="utf-8"))[0]["gen_prompt"]

old_a = "皮肤白皙自然无暇，真实细腻皮肤纹理，清冷少年感，安静疏离气质，表情淡漠自然，不微笑。"
new_a = "皮肤白皙细腻通透，真实细腻皮肤纹理，清秀少年感，干净温和气质，略带书卷气，表情淡静自然，不微笑。"
old_b = "五官精致但不女性化，清晰下颌线，干净眉眼。"
new_b = "脸部线条柔和精致，五官清秀干净，下颌线清晰柔和，眉眼清秀，少年感强，精致但不女性化。"
assert old_a in chen_base and old_b in chen_base, "v14 原文片段未命中，需人工核对"
chen = chen_base.replace(old_a, new_a).replace(old_b, new_b)

chars = [
    {"name": "陈诚", "gen_prompt": chen},
    {"name": "沈幼怡", "gen_prompt": shen},
]
io.open(DRAFT + r"\chars_v18.json", "w", encoding="utf-8").write(json.dumps(chars, ensure_ascii=False, indent=1))
print("chars_v18=%d" % len(chars))
print("女主==v7原文:", shen == json.load(io.open(DRAFT + r"\chars_v7.json", encoding="utf-8"))[0]["gen_prompt"])
print("男主清秀化:", "清秀少年感" in chen and "脸部线条柔和精致" in chen and "桃花眼" in chen and "左眉尾一颗小痣" in chen)
