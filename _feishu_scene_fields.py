#!/usr/bin/env python3
"""只读：打印指定 base 场景库字段明细（含单选选项）。"""
import os, sys, requests
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""
SCENE_TID = sys.argv[2] if len(sys.argv) > 2 else ""

def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    h = feishu._headers()
    base = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"
    r = requests.get(f"{base}/tables/{SCENE_TID}/fields", headers=h, timeout=15)
    r.raise_for_status()
    for f in r.json()["data"]["items"]:
        prop = f.get("property") or {}
        opts = prop.get("options") or []
        optnames = [o.get("name") for o in opts]
        mark = "★primary" if f.get("is_primary") else ""
        print(f"{f.get('field_name')!r} type={f.get('type')} {mark} options={optnames}")

if __name__ == "__main__":
    main()
