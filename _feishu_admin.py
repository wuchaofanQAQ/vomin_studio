#!/usr/bin/env python3
"""只读巡检：飞书场景库/分镜表当前记录数 + 场景库是否已有「分镜绑定状态」列。"""
import os, sys, json
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = os.environ.get("FEISHU_BITABLE_APP_TOKEN", "")

def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    tables = feishu.discover_tables()
    print("发现数据表:", ", ".join(tables.keys()))
    scene_tid = tables.get("场景库", "")
    shot_tid = tables.get("剧本分镜表", "")
    if not scene_tid or not shot_tid:
        print("缺少场景库/剧本分镜表，无法继续")
        return

    # 场景库字段列表
    import requests
    h = feishu._headers()
    base = f"bitable/v1/apps/{APP_TOKEN}"
    r = requests.get(f"https://open.feishu.cn/open-apis/{base}/tables/{scene_tid}/fields", headers=h, timeout=15)
    r.raise_for_status()
    fields = r.json()["data"]["items"]
    print("\n[场景库字段]")
    for f in fields:
        mark = "★primary" if f.get("is_primary") else ""
        print(f"  {f.get('field_name')!r} type={f.get('type')} {mark}")
    has_bind = any(f.get("field_name") == "分镜绑定状态" for f in fields)
    print("  -> 分镜绑定状态列存在:", has_bind)

    def count(tid, label):
        recs = feishu.list_records(tid)
        print(f"[{label}] 记录数: {len(recs)}")
        return recs

    scene_recs = count(scene_tid, "场景库")
    shot_recs = count(shot_tid, "剧本分镜表")

    print("\n[场景库 前若干场景名]")
    for rec in scene_recs[:30]:
        f = rec.get("fields", {})
        print("  ", f.get("场景名"), "| 视角=", f.get("视角"))
    print("\n[剧本分镜表 前若干镜头ID]")
    for rec in shot_recs[:30]:
        f = rec.get("fields", {})
        print("  ", f.get("镜头编号"), "| 状态=", f.get("状态"))

if __name__ == "__main__":
    main()
