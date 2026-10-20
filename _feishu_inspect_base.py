#!/usr/bin/env python3
"""只读巡检指定 base（app_token 用参数传入）。列出全部表 + 记录数 + 场景库字段。"""
import os, sys, json, requests
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = sys.argv[1] if len(sys.argv) > 1 else ""

def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    h = feishu._headers()
    base = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"

    all_tables = {}
    page_token = ""
    while True:
        url = f"{base}/tables"
        if page_token:
            url += f"?page_token={page_token}"
        r = requests.get(url, headers=h, timeout=15)
        r.raise_for_status()
        data = r.json().get("data", {})
        for t in data.get("items", []):
            all_tables[t["table_id"]] = t.get("name")
        if data.get("has_more"):
            page_token = data.get("page_token", "")
        else:
            break

    print(f"base app_token={APP_TOKEN}  全部数据表（{len(all_tables)} 张）:")
    for tid, name in all_tables.items():
        recs = feishu.list_records(tid)
        fields_resp = requests.get(f"{base}/tables/{tid}/fields", headers=h, timeout=15)
        fields_resp.raise_for_status()
        fields = fields_resp.json()["data"]["items"]
        primary = next((f.get("field_name") for f in fields if f.get("is_primary")), "")
        fnames = [f.get("field_name") for f in fields]
        print(f"\n  table_id={tid}  name={name!r}  记录数={len(recs)}  主键={primary!r}")
        print(f"    字段({len(fnames)}): {fnames}")
        if name in ("场景库", "剧本分镜表") and recs:
            for rec in recs[:30]:
                print(f"    记录: {json.dumps(rec['fields'], ensure_ascii=False)[:160]}")

if __name__ == "__main__":
    main()
