# -*- coding: utf-8 -*-
"""v21：玄关+客厅合并为一个连通空间场景「陈诚公寓·玄关客厅·内·傍晚」；分镜 s01/s07/s08/s09 引用替换。"""
import json, io, re

DRAFT = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚_draft"

# ============ 1. 合并场景 prompt ============
SCENE_STYLE = ("<STYLE LOCK>\n现代都市风格（韩式真人影视剧质感）：场景干净明亮现代，真人影视剧质感，浅景深背景虚化，"
               "空间比例真实，材质精致真实（暖白墙面原木地板原木家具布艺），现代简约家装，自然光与柔和布光，"
               "轻微胶片颗粒不过度锐化，色彩明快通透低饱和暖调，拒绝破旧斑驳锈蚀脏乱年代感；现代都市生活剧，"
               "夏末暖色温馨日常基调，清新明亮，不要暗黑或赛博朋克风。\n</STYLE LOCK>")
QUALITY = ("<QUALITY>\n纯空镜场景，四个面板均无任何人物，无文字，无水印，无标注线框；16:9横版四宫格布局，白色间隙分隔清晰；"
           "四个面板为同一连通空间（玄关+客厅）的四个固定机位视角，光源方向一致、色温一致、材质一致，"
           "玄关与客厅地面同为原木色木地板、墙面同为暖白墙、木饰面同为原木色，完全统一；"
           "场景主体占各面板画面约四分之三，留出约四分之一空旷空间（为角色叠加留位）；"
           "高清，细节丰富，透视准确，禁止俯视顶视图、禁止鱼眼畸变。\n</QUALITY>")

merged = {"name": "陈诚公寓·玄关客厅·内·傍晚",
     "description": "陈诚公寓玄关与客厅连通空间（暖白墙面、原木色木地板、原木鞋柜与餐桌、布艺沙发、开放式厨房、卧室门），八月末傍晚柔和淡暖光从客厅窗照入并向玄关渗透，光色一致",
     "gen_prompt": ("<HEADER>\n16:9横版四宫格场景设定图，白色间隙间隔，2×2布局：左上、右上、左下、右下四个面板，"
                    "每面板为同一连通空间（玄关+客厅）从不同固定机位拍摄的视角；面板之间以清晰白色间隙分隔，无重叠、无裁切。\n</HEADER>\n\n"
                    + SCENE_STYLE + "\n\n<PANELS>\n"
                    "本场景为陈诚公寓的玄关与客厅连通空间，全屋暖白墙面（#F5F0E8）、原木色木地板、原木色木饰面家具"
                    "（玄关鞋柜/客厅餐桌/柜体）、深色入户门，暖白低饱和色调；玄关与客厅地面同为原木色木地板、墙面同为暖白墙、"
                    "木饰面同为原木色，光源为同一傍晚柔和淡暖光（从客厅窗照入，向玄关门洞方向渗透渐弱），"
                    "光色完全一致、不偏深不偏橙；玄关通往客厅的门洞位置在画面各面板中保持一致，禁止装修风格割裂。\n\n"
                    "左上 — 玄关主入口机位：摄像机固定于入户门内侧，平视拍摄，主体是玄关空间与原木鞋柜，前景是门槛与原木色木地板，"
                    "中景是原木鞋柜、暖白墙挂钩与地垫，背景是通往客厅的门洞透出柔和淡暖光；光从客厅方向轻透入玄关，"
                    "浅暖雅致、不偏深。\n\n"
                    "右上 — 玄关纵深机位：摄像机固定于玄关中段，平视沿通道拍摄，主体是玄关过道延伸向客厅门洞的透视，"
                    "前景是原木鞋柜一角，中景是过道与暖白墙面，背景是门洞内客厅沙发区与窗的淡暖光；同一暖光方向，"
                    "木地板反射淡暖光。\n\n"
                    "左下 — 客厅主区机位：摄像机固定于玄关门洞处，平视拍摄，主体是客厅空间与布艺沙发，前景是门洞框边，"
                    "中景是沙发、矮茶几与书桌，背景是窗与开放式厨房台面；傍晚柔和淡暖光从窗外照入，光色与玄关一致。\n\n"
                    "右下 — 客厅整体空间机位：摄像机固定于客厅对角高处，略俯拍摄，主体是客厅整体空间关系（含玄关门洞），"
                    "前景是原木餐桌与椅，中景是沙发区与开放式厨房区，背景是卧室门与窗；柔和浅暖光覆盖全屋，"
                    "玄关与客厅同光色、同材质，布局清晰。\n</PANELS>\n\n" + QUALITY)}

# 旧两行标注合并
old_xuan = {"name": "陈诚公寓·玄关·内·傍晚",
            "description": "【已合并】并入「陈诚公寓·玄关客厅·内·傍晚」，不再单独出图；保留本行防旧引用断裂",
            "gen_prompt": "【已合并】并入「陈诚公寓·玄关客厅·内·傍晚」，不再单独出图。请勿再引用本行。",
            "source": "已合并"}
old_keting = {"name": "陈诚公寓·客厅·内·傍晚",
              "description": "【已合并】并入「陈诚公寓·玄关客厅·内·傍晚」，不再单独出图；保留本行防旧引用断裂",
              "gen_prompt": "【已合并】并入「陈诚公寓·玄关客厅·内·傍晚」，不再单独出图。请勿再引用本行。",
              "source": "已合并"}
io.open(DRAFT + r"\scenes_v21.json", "w", encoding="utf-8").write(
    json.dumps([merged, old_xuan, old_keting], ensure_ascii=False, indent=1))

# ============ 2. 分镜替换 s01/s07/s08/s09 ============
raw = io.open(DRAFT + r"\read_storyboard_now.log", encoding="utf-8").read()
# 跳过首行 "已从飞书拉取..."，取 JSON 部分
start = raw.find("[")
sb = json.loads(raw[start:])
OLD_X, OLD_K, NEW = "陈诚公寓·玄关·内·傍晚", "陈诚公寓·客厅·内·傍晚", "陈诚公寓·玄关客厅·内·傍晚"
TARGETS = {"ep01_s01", "ep01_s07", "ep01_s08", "ep01_s09"}
out = []
for row in sb:
    sid = row["shot_id"]
    if sid not in TARGETS:
        continue
    p = row["prompt"]
    env = row["env_lock"]
    # 锚定段引用替换：玄关行/客厅行 → 合并行
    p2 = p.replace("{场景库：" + OLD_X + "}", "{场景库：" + NEW + "}").replace("{场景库：" + OLD_K + "}", "{场景库：" + NEW + "}")
    # 同一分镜里原有两行场景引用时，去掉重复的合并行（保留第一行，删除后续相同行）
    lines = p2.split("\n")
    seen_new = 0
    new_lines = []
    for ln in lines:
        if ("{场景库：" + NEW + "}") in ln:
            seen_new += 1
            if seen_new > 1:
                continue  # 删除重复合并行
        new_lines.append(ln)
    p3 = "\n".join(new_lines)
    env2 = NEW if (env == OLD_X or env == OLD_K) else env
    out.append({"shot_id": sid, "prompt": p3, "env_lock": env2})
    print("== %s env: %s -> %s | 锚定含合并: %s | 重复行已去重" % (sid, env, env2, NEW in p3))
io.open(DRAFT + r"\storyboard_v21.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print("storyboard_v21 rows=%d" % len(out))
print("合并场景:", "玄关+客厅" in merged["gen_prompt"] and "同一傍晚柔和淡暖光" in merged["gen_prompt"])
