#!/usr/bin/env python3
"""以飞书为准：把本地 scenes.json / storyboard.json 同步为飞书当前（空）状态。
旧数据备份到 bak/sync_<时间戳>/ 以防需要找回。"""
import os, sys, json, shutil
from datetime import datetime

WS = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"

def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak_dir = os.path.join(WS, "bak", f"sync_feishu_empty_{ts}")
    os.makedirs(bak_dir, exist_ok=True)

    for fname in ("scenes.json", "storyboard.json"):
        p = os.path.join(WS, fname)
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"{fname}: 读取失败 {e}，跳过")
                continue
            n = len(data) if isinstance(data, list) else "?"
            # 备份旧内容
            shutil.copy2(p, os.path.join(bak_dir, fname))
            # 写空列表，对齐飞书当前空状态
            with open(p, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)
            print(f"{fname}: 旧 {n} 条 -> 已清空；备份至 {bak_dir}")
        else:
            print(f"{fname}: 不存在，跳过")

if __name__ == "__main__":
    main()
