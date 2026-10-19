# -*- coding: utf-8 -*-
"""画风 v4：真人影视剧质感 + 韩漫现代人物。更新画面风格设定 + 5角色/4场景 STYLE LOCK 段替换。"""
import json, io, re

DRAFT = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚_draft"

# ============ 1. 剧本设定「画面风格」 v4 ============
STYLE_VALUE = ("真人影视剧质感+韩漫现代人物风格：整体画风接近真人影视剧，浅景深背景虚化，35mm相机镜头质感；柔光+轮廓发丝光，"
               "夜景常用冷暖对比（室内暖黄、城市夜景冷蓝）；轻微胶片颗粒，不过度锐化；色调低饱和暖调、明亮干净。"
               "人物为韩漫现代风格：男女主五官精致放大、眼睛更大，面部阴影厚涂（韩漫式立体打光），人体比例偏修长、头小身长、"
               "腿长占比足；发色丰富（棕、黑茶、浅棕）且高光明显；穿搭现代时装。"
               "场景为现代都市风格：干净明亮现代，空间比例真实，材质精致（白墙原木金属玻璃布艺），现代简约家装与城市建筑质感。"
               "现代都市生活剧，竖屏9:16构图；夏末暖色温馨日常基调，不要暗黑或赛博朋克风【用户指定】")
STYLE_GLOBAL = ("真人影视剧质感+韩漫现代人物风格：整体画风接近真人影视剧，浅景深背景虚化，35mm相机镜头质感；柔光+轮廓发丝光，"
                "夜景常用冷暖对比（室内暖黄、城市夜景冷蓝）；轻微胶片颗粒，不过度锐化；色调低饱和暖调、明亮干净。"
                "人物为韩漫现代风格：男女主五官精致放大、眼睛更大更有神，面部阴影厚涂（韩漫式立体打光），人体比例偏修长、头小身长、"
                "腿长占比足；发色丰富（棕、黑茶、浅棕）且高光明显、层次分明；穿搭现代时装，配色低饱和暖调明亮干净。"
                "场景为现代都市风格：干净明亮现代，空间比例真实，材质精致（白墙原木金属玻璃布艺），现代简约家装与城市建筑质感。"
                "现代都市生活剧，竖屏9:16构图；夏末暖色温馨日常基调，不要暗黑或赛博朋克风。")
settings = [{"name": "画面风格", "category": "画面风格", "value": STYLE_VALUE, "global_prompt": STYLE_GLOBAL}]
io.open(DRAFT + r"\settings_style_v4.json", "w", encoding="utf-8").write(json.dumps(settings, ensure_ascii=False, indent=1))

# ============ 2. 角色 STYLE LOCK v4（韩漫现代人物） ============
CHAR_STYLE = ("<STYLE LOCK>\n韩漫现代人物风格：男女主五官精致放大、眼睛更大更有神，面部阴影厚涂（韩漫式立体打光），"
              "人体比例偏修长、头小身长、腿长占比足；发色丰富（棕、黑茶、浅棕）且发丝高光明显、层次分明；穿搭现代时装，"
              "配色低饱和暖调、明亮干净；整体画风接近真人影视剧质感，柔光+轮廓发丝光，轻微胶片颗粒不过度锐化；"
              "拒绝大众脸网红脸整容脸、拒绝扁平卡通上色、拒绝塑料皮肤。\n</STYLE LOCK>")

def replace_style(prompt, new_style):
    # 替换 <STYLE LOCK>...</STYLE LOCK> 整段
    return re.sub(r"<STYLE LOCK>\n.*?\n</STYLE LOCK>", new_style, prompt, count=1, flags=re.S)

chars = json.load(io.open(DRAFT + r"\chars_v3.json", encoding="utf-8"))
for c in chars:
    c["gen_prompt"] = replace_style(c["gen_prompt"], CHAR_STYLE)
io.open(DRAFT + r"\chars_v4.json", "w", encoding="utf-8").write(json.dumps(chars, ensure_ascii=False, indent=1))

# ============ 3. 场景 STYLE LOCK v4（真人影视剧质感+现代都市） ============
SCENE_STYLE = ("<STYLE LOCK>\n真人影视剧画面质感：接近真人实拍电影，35mm相机镜头质感，浅景深背景虚化，柔光+轮廓发丝光，"
               "夜景常用冷暖对比（室内暖黄、城市夜景冷蓝），轻微胶片颗粒不过度锐化；色调低饱和暖调、明亮干净；"
               "现代都市风格：场景干净明亮现代，空间比例真实，材质精致（白墙原木金属玻璃布艺），现代简约家装与城市建筑质感；"
               "拒绝破旧斑驳锈蚀脏乱年代感、拒绝卡通动画风。\n</STYLE LOCK>")

scenes = json.load(io.open(DRAFT + r"\scenes_v3.json", encoding="utf-8"))
for s in scenes:
    s["gen_prompt"] = replace_style(s["gen_prompt"], SCENE_STYLE)
io.open(DRAFT + r"\scenes_v4.json", "w", encoding="utf-8").write(json.dumps(scenes, ensure_ascii=False, indent=1))

print("settings_v4=%d chars_v4=%d scenes_v4=%d" % (len(settings), len(chars), len(scenes)))
print("char has 韩漫:", all("韩漫现代人物风格" in c["gen_prompt"] for c in chars))
print("scene has 35mm:", all("35mm" in s["gen_prompt"] for s in scenes))
print("style replaced once:", all(c["gen_prompt"].count("<STYLE LOCK>") == 1 for c in chars) and all(s["gen_prompt"].count("<STYLE LOCK>") == 1 for s in scenes))
