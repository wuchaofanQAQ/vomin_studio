#!/usr/bin/env python3
"""只读：列出 base 内全部数据表（含分页），逐表给 记录数 + 主键字段 + 表名匹配，
用于定位用户看到的「场景库 / 剧本分镜表」真实 table_id。"""
import os, sys, json, requests
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = os.environ.get("FEISHU_BITABLE_APP_TOKEN", "")

def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    h = feishu._headers()
    base = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{APP_TOKEN}"

    # 全量拉取所有表（处理分页）
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

    print(f"base 内全部数据表（{len(all_tables)} 张）:")
    for tid, name in all_tables.items():
        recs = feishu.list_records(tid)
        # 主键字段
        fields_resp = requests.get(f"{base}/tables/{tid}/fields", headers=h, timeout=15)
        fields_resp.raise_for_status()
        fields = fields_resp.json()["data"]["items"]
        primary = next((f.get("field_name") for f in fields if f.get("is_primary")), "")
        fnames = [f.get("field_name") for f in fields]
        print(f"\n  table_id={tid}  name={name!r}")
        print(f"    记录数={len(recs)}  主键={primary!r}")
        print(f"    字段({len(fnames)}): {fnames}")
        if recs:
            first = recs[0]["fields"]
            shown = {k: v for k, v in list(first.items())[:6]}
            print(f"    首记录样例: {json.dumps(shown, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
