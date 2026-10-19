# -*- coding: utf-8 -*-
"""重抽厨房视角：参考图改用"主视角 + 侧面（厨房已清晰）"，
机位描述为"从侧面机位朝厨房走近"，一次出 3 张备选。"""
import os
import shutil

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from vomin.ark.client import ArkClient
from vomin.ark.image import ImageClient

MODEL = "doubao-seedream-5-0-flash-260915"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples", "scene_i2i")

KEEP = """以参考图中的这套公寓为唯一基准：保持完全相同的房间空间结构、同一套家具与道具、所有物品的位置与朝向、墙面地面材质、傍晚淡暖橘色光线完全不变。全屋仅一张浅米灰布艺双人沙发，不得增加或移动任何家具、不得新增书桌或餐桌。画面必须是纯空镜，绝对不能出现任何人物或人影，不能出现三脚架、相机等摄影器材，无文字、无水印。"""

INSTR = """机位：参考图中"从客厅左侧横向朝厨房看"的视角，保持相同朝向，向厨房方向走近，直到贴近厨房台面：
- 前景：右手侧开放式厨房的原木台面（水槽、灶台一角、上方原木吊柜）占画面下方较大面积；
- 中景：矮腿原木茶几（台面有水杯、书本）与两个折叠小马扎；
- 画面右侧：唯一一张浅米灰布艺双人沙发的侧面（横向靠在阳台推拉门前）；
- 画面左侧：洗手间门、卧室门；
- 画面一侧深处：阳台推拉门与淡暖橘色傍晚余晖。
此视角下玄关入户门在身后、不入画。"""


def main():
    ark = ArkClient()
    img = ImageClient(ark)
    refs = [os.path.join(OUT, "01_master.png"), os.path.join(OUT, "05_side.png")]
    prompt = f"{KEEP}\n{INSTR}"
    print("re-rolling kitchen view x3 ...")
    paths = img.generate_to_dir(model=MODEL, prompt=prompt, save_dir=OUT,
                                n=3, size="2K", ref_images=refs)
    for i, p in enumerate(paths):
        dst = os.path.join(OUT, f"04_kitchen_v{i+1}.png")
        shutil.move(p, dst)
        print("saved:", dst)


if __name__ == "__main__":
    main()
