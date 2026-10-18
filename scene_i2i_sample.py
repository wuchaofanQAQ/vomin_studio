# -*- coding: utf-8 -*-
"""图生图场景小样：
  1) 先生成一张"主视角定版图"（空间基准）
  2) 以主视角为参考图，逐机位"换视角"延展（一次一张）
目的：验证以图生图的空间一致性，替代一次出九宫格。
"""
import os
import shutil

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from vomin.ark.client import ArkClient
from vomin.ark.image import ImageClient

MODEL = "doubao-seedream-5-0-flash-260915"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples", "scene_i2i")
os.makedirs(OUT, exist_ok=True)

# 主视角：从玄关朝客厅尽头阳台看（空间唯一基准）
MASTER_PROMPT = """16:9横版，现代都市小户型出租屋（一室一厅）的客厅正面广角视角，纯空镜、无任何人物。
画面从玄关朝客厅尽头阳台方向看，由近到远依次为：
- 玄关（画面近处）：浅色瓷砖地面，左手侧一只原木简易鞋柜，柜下整齐摆放拖鞋；
- 穿过无门扇的原木框门洞进入客厅：地面为原木色木地板、暖白墙面；
- 客厅中央：一张原木矮腿茶几，台面放一只水杯、一本书，茶几靠玄关一侧的左右两边各放一个折叠小马扎；
- 客厅最靠阳台一端：唯一一张浅米灰布艺沙发，横向摆放、背靠阳台墙、正面朝向玄关；
- 右手侧墙面：开放式厨房一字台面（含水槽、灶台、原木吊柜）；
- 左手侧墙面：相邻开着洗手间门与卧室门，门内可见单人床一角与书桌一角；
- 客厅尽头：原木框玻璃推拉门通向小阳台，门外可见城市远景。
光线：八月末傍晚，柔和淡暖橘色余晖从阳台玻璃门外照入，越过沙发、茶几，向玄关渗透渐弱，在家具上形成暖橘高光与柔和长影，干净温暖。
现代韩式真人影视剧质感，浅景深背景虚化，材质真实，轻微胶片颗粒，低饱和暖调；高清，细节丰富，透视准确；无人物、无文字、无水印、无三脚架或相机等任何摄影器材。"""

# 逐机位延展：前缀锁定"保持不变"，后缀只描述视角如何移动
KEEP = """以参考图中的这套公寓为唯一基准：保持完全相同的房间空间结构、同一套家具与道具、所有物品的位置与朝向、墙面地面材质、以及傍晚淡暖橘色光线完全不变，只把观察位置移动到指定机位，得到该机位看到的画面。全屋仅一张浅米灰布艺沙发，不得增加或移动任何家具，不得出现人物、人影、三脚架或相机等摄影器材、文字或水印。"""

VIEWS = [
    ("02_front_sofa", """机位：从主视角向前走到客厅矮腿茶几靠玄关一侧、紧靠茶几边缘，面朝客厅尽头阳台方向、视线对准布艺沙发正面；前景为矮茶几台面（水杯、书本），中景为唯一一张布艺沙发正面，背景为沙发后方阳台推拉门的橘色余晖；折叠小马扎在茶几两侧。"""),
    ("03_reverse", """机位：走到布艺沙发与阳台推拉门之间、紧靠沙发靠背背面，面朝玄关方向，视线对准玄关无门门洞与入户门；前景为沙发靠背背面，中景为矮腿茶几，背景为玄关无门门洞与深色入户防盗门（厨房在右手侧、鞋柜在左手侧）；与正面机位严格180度空间连续。"""),
    ("04_kitchen", """机位：走到客厅右手侧的开放式厨房台面最靠阳台一端、站在台面内侧（吊柜下方），面朝客厅与玄关方向；前景为厨房台面、水槽与吊柜边缘，中景为矮腿茶几与折叠小马扎，背景为唯一一张布艺沙发的侧面与玄关无门门洞；阳台推拉门在身后、不入画。"""),
    ("05_side", """机位：站在客厅左手侧、紧靠卧室门与洗手间门之间的墙边，视线垂直于玄关—阳台方向，横向朝右手侧厨房看；画面沿视线从近到远依次为洗手间门/卧室门墙面、矮腿茶几与小马扎、布艺沙发左端与侧面、远端开放式厨房台面，阳台推拉门位于画面一侧边缘。"""),
]


def main():
    ark = ArkClient()
    img = ImageClient(ark)

    # 1) 主视角定版
    print("[1] generating master view ...")
    paths = img.generate_to_dir(model=MODEL, prompt=MASTER_PROMPT,
                                save_dir=OUT, n=1, size="2K")
    master = os.path.join(OUT, "01_master.png")
    shutil.move(paths[0], master)
    print("    master:", master)

    # 2) 逐机位以图生图延展
    for i, (name, view_instr) in enumerate(VIEWS, start=2):
        print(f"[{i}] rolling view: {name} ...")
        prompt = f"{KEEP}\n{view_instr}"
        got = img.generate_to_dir(model=MODEL, prompt=prompt,
                                  save_dir=OUT, n=1, size="2K",
                                  ref_images=[master])
        dst = os.path.join(OUT, f"{name}.png")
        shutil.move(got[0], dst)
        print("    saved:", dst)

    print("DONE ->", OUT)


if __name__ == "__main__":
    main()
