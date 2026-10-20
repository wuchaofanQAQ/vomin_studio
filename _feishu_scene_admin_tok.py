#!/usr/bin/env python3
"""在【指定 base】上执行：1) 场景库加「分镜绑定状态」列  2) 删空场景库  3) 删空剧本分镜表。
用法: python _feishu_scene_admin_tok.py <app_token> <场景库table_id> <剧本分镜表table_id>"""
import os, sys, requests
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = sys.argv[1]
SCENE_TID = sys.argv[2]
SHOT_TID = sys.argv[3]

def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    h = feishu._headers()
    base = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"

    # ---- 1. 场景库新增「分镜绑定状态」列（若不存在）----
    fields_resp = requests.get(f"{base}/tables/{SCENE_TID}/fields", headers=h, timeout=15)
    fields_resp.raise_for_status()
    fields = fields_resp.json()["data"]["items"]
    has = any(f.get("field_name") == "分镜绑定状态" for f in fields)
    if has:
        print("[场景库] 分镜绑定状态列已存在，跳过新增")
    else:
        body = {"field_name": "分镜绑定状态", "type": 3,
                "property": {"options": [{"name": "未绑定"}, {"name": "已绑定"}]}}
        r = requests.post(f"{base}/tables/{SCENE_TID}/fields", headers=h, json=body, timeout=15)
        r.raise_for_status()
        d = r.json()
        if d.get("code") != 0:
            raise RuntimeError(f"加列失败: {d.get('msg')}")
        print("[场景库] 已新增「分镜绑定状态」列（单选：未绑定/已绑定）")

    # ---- 2. 删除场景库全部记录 ----
    scene_recs = feishu.list_records(SCENE_TID)
    print(f"[场景库] 待删除记录: {len(scene_recs)}")
    for rec in scene_recs:
        rid = rec["record_id"]
        r = requests.delete(f"{base}/tables/{SCENE_TID}/records/{rid}", headers=h, timeout=15)
        r.raise_for_status()
        if r.json().get("code") != 0:
            print(f"  删除失败 {rid}: {r.json().get('msg')}")
    print(f"[场景库] 已删除 {len(scene_recs)} 条")

    # ---- 3. 删除剧本分镜表全部记录 ----
    shot_recs = feishu.list_records(SHOT_TID)
    print(f"[剧本分镜表] 待删除记录: {len(shot_recs)}")
    for rec in shot_recs:
        rid = rec["record_id"]
        r = requests.delete(f"{base}/tables/{SHOT_TID}/records/{rid}", headers=h, timeout=15)
        r.raise_for_status()
        if r.json().get("code") != 0:
            print(f"  删除失败 {rid}: {r.json().get('msg')}")
    print(f"[剧本分镜表] 已删除 {len(shot_recs)} 条")

    # ---- 复查 ----
    print("\n[复查]")
    print(f"  场景库剩余: {len(feishu.list_records(SCENE_TID))}")
    print(f"  剧本分镜表剩余: {len(feishu.list_records(SHOT_TID))}")
    f2 = requests.get(f"{base}/tables/{SCENE_TID}/fields", headers=h, timeout=15).json()["data"]["items"]
    print("  场景库字段:", [f.get('field_name') for f in f2])

if __name__ == "__main__":
    main()
