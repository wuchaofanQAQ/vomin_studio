#!/usr/bin/env python3
"""把母版改成三视角组：改名 母版→母版·45°俯视图，新增 主视图/反打图 两行（不填图）。"""
import json
import os
import sys

import requests
from dotenv import load_dotenv

ROOT = r"C:\Users\Heart\PycharmProjects\vomin_studio"
WS = os.path.join(ROOT, "workspace", "养妹失策，社恐妹妹占有欲爆棚")
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = "UWhZbNm8ba7fUlsC0WqcetrJnsd"
SPACE = "陈诚公寓玄关客厅（日）"
OLD_ID = f"{SPACE}·母版"
NEW_ID = f"{SPACE}·母版·45°俯视图"
REF = f"{SPACE}·母版·45°俯视图"

COMMON = "空间参考图，无人，16:9横版；画风锁定：电影感实景场景，实景拍摄质感，单反相机拍摄，柔和自然光，低饱和灰调，氛围感，真实环境纹理，8K，全画面清晰，墙体门窗家具边界可读，不使用浅景深虚化。"

VIEWS = [
    {
        "id": f"{SPACE}·母版·主视图",
        "view": "母版·主视图",
        "desc": "平视主视角：机位 1.5 米，站在玄关内侧朝客厅看，客厅、沙发、茶几、小马扎、开放式厨房侧沿与阳台推拉门在同一画面；奶油白+浅木，圆角哑光家具。",
        "prompt": (
            f"【作用】{SPACE} 空间母版·主视图，交代人眼高度下的客厅主方向关系；不直接挂分镜。\n"
            f"【性质】{COMMON}\n"
            f"【机位】机位高 1.5 米，位于玄关内侧偏右，朝客厅方向平视，35mm，画面下方保留约一成地面，画面上方留出天花板约一成。\n"
            "【锚点】以【母版·45°俯视图】为家具位置、材质、颜色与光线的唯一依据：沙发、茶几、两个小马扎、电脑桌、厨房侧柜体、阳台推拉门与纱帘、墙面色调全部 1:1 一致，家具为奶油白+浅木、圆角、哑光；不新增、不移动家具；玄关地面材质与客厅木地板的分界在画面近景可见。\n"
            "【光线色调】白天，主光自南侧阳台推拉门斜射入室，中性冷白，地面柔和高光；奶油白与浅木的低饱和暖灰调。\n"
            "【排除】无人物，无文字，无logo，无水印；不要高饱和色，不要金属冷光，不要豪华装修，不要大平层尺度，不要过曝。\n"
            f"【参考图】{{场景库：{REF}}} 图1：母版·45°俯视图，作为空间结构与家具依据。"
        ),
    },
    {
        "id": f"{SPACE}·母版·反打图",
        "view": "母版·反打图",
        "desc": "平视反向视角：机位 1.5 米，站在阳台侧朝北回看，玄关、入户门内侧、鞋柜、两扇内门与空调同框；奶油白+浅木。",
        "prompt": (
            f"【作用】{SPACE} 空间母版·反打图，交代玄关、入户门与两扇内门的位置关系；不直接挂分镜。\n"
            f"【性质】{COMMON}\n"
            f"【机位】机位高 1.5 米，位于客厅南侧靠阳台处，朝北正对玄关方向平视，35mm，画面下方保留约一成地面。\n"
            "【锚点】以【母版·45°俯视图】为家具位置、材质、颜色与光线的唯一依据：入户门在其北墙正中、朝内开；门内为狭长玄关，浅色瓷砖地面，与客厅木地板在门洞处分界；鞋柜在玄关东侧，柜下摆拖鞋；经无门原木门框进入客厅；东墙自北向南为卧室门、洗手间门；西侧为一字型厨房柜体与冰箱；墙面挂老式壁挂空调；全部 1:1 一致，家具奶油白+浅木、圆角、哑光，不新增不移动。\n"
            "【光线色调】白天，主光自南侧（机位后方）推拉门斜射入室，玄关一侧比客厅暗一档，地面柔和高光；奶油白与浅木的低饱和暖灰调。\n"
            "【排除】无人物，无文字，无logo，无水印；不要高饱和色，不要金属冷光，不要豪华装修，不要过曝。\n"
            f"【参考图】{{场景库：{REF}}} 图1：母版·45°俯视图，作为空间结构与家具依据。"
        ),
    },
]


def text(v):
    if isinstance(v, list):
        return "".join(x.get("text", "") if isinstance(x, dict) else str(x) for x in v)
    return str(v or "")


def main():
    f = FeishuBitable(app_token=APP_TOKEN)
    tid = f.discover_tables()["场景库"]
    base = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}/tables/{tid}"
    h = f._headers()

    # 1. 改名
    for rec in f.list_records(tid):
        if text(rec["fields"].get("场景ID")) == OLD_ID:
            r = requests.put(f"{base}/records/{rec['record_id']}", headers=h, json={"fields": {
                "场景ID": NEW_ID,
                "视角": "母版·45°俯视图",
                "作用关联": "作用：空间母版三视角之一（45°俯视），定义整体骨架；与主视图、反打图共同构成母版组。约束入口位置、地面材质与分界、功能区方位、门窗方位、主光方向。",
            }}, timeout=20).json()
            print("改名:", r.get("code"), r.get("msg"))

    # 2. 新增两行
    existing = {text(r["fields"].get("场景ID")) for r in f.list_records(tid)}
    for v in VIEWS:
        if v["id"] in existing:
            print("已存在，跳过:", v["id"])
            continue
        body = {"fields": {
            "场景ID": v["id"],
            "场景名": SPACE,
            "视角": v["view"],
            "场景描述": v["desc"],
            "关联集数": "1,2,3",
            "来源": "AIGC生成",
            "生成提示词": v["prompt"],
            "文件路径": "",
            "参考场景": REF,
            "作用关联": f"作用：空间母版三视角之一（{v['view'].split('·')[-1]}），以 45°俯视图为准补全该朝向；不直接挂分镜。",
            "出图状态": "待出图",
            "一致性检查": "未检查",
        }}
        r = requests.post(f"{base}/records", headers=h, json=body, timeout=20).json()
        print("新增", v["view"], ":", r.get("code"), r.get("msg"))

    # 3. 本地 scenes.json
    p = os.path.join(WS, "scenes.json")
    rows = json.load(open(p, encoding="utf-8"))
    for row in rows:
        if row.get("name") == SPACE and row.get("view_angle") == "母版":
            row["view_angle"] = "母版·45°俯视图"
    have = {(r.get("name"), r.get("view_angle")) for r in rows}
    for v in VIEWS:
        if (SPACE, v["view"]) not in have:
            rows.append({
                "name": SPACE, "view_angle": v["view"], "description": v["desc"],
                "ref_scenes": REF, "relation_note": f"作用：空间母版三视角之一；不直接挂分镜。",
                "related_episodes": "1,2,3", "bind_scenes": "",
                "ref_image": "", "gen_prompt": v["prompt"],
                "negative_prompt": "人物，人脸，文字，字幕，logo，水印，高饱和，金属冷光，豪华装修，过曝，广角畸变",
                "gen_model": "", "source": "AIGC生成",
                "gen_status": "待出图", "consistency": "未检查",
            })
    json.dump(rows, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("本地 scenes.json 已同步")


if __name__ == "__main__":
    main()
