#!/usr/bin/env python3
"""只读：把剧本表全部记录备份为本地 JSON（删除字段前使用）。"""
import json
import os
import sys

from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
from vomin.feishu.bitable import FeishuBitable

APP_TOKEN = "UWhZbNm8ba7fUlsC0WqcetrJnsd"
SCRIPT_TID = "tbluiZYU9urE5ALm"
WS = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"


def main():
    feishu = FeishuBitable(app_token=APP_TOKEN)
    records = feishu.list_records(SCRIPT_TID)
    out_dir = os.path.join(WS, "backup")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "剧本表_删除字段备份_20261021.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"已备份 {len(records)} 条记录 -> {out}")
    for rec in records:
        ep = rec["fields"].get("集数")
        keys = [k for k in ("核心事件", "出场角色", "上集钩子", "结尾钩子", "场次列表")
                if rec["fields"].get(k)]
        print(f"  第{ep}集: 含 {len(keys)}/5 个待删字段 -> {keys}")


if __name__ == "__main__":
    main()
