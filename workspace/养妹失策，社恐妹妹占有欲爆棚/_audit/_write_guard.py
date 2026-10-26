# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''    if isinstance(data, dict):
        data = [data]

    match_keys = {'''
new = '''    if isinstance(data, dict):
        data = [data]

    # 资产表幂等：复用项不重写（否则会用空描述覆盖库里已有资产）
    if table in ("角色库", "场景库", "道具库"):
        reused_rows = [r for r in data if isinstance(r, dict) and str(r.get("status")) == "复用"]
        if reused_rows:
            data = [r for r in data if not (isinstance(r, dict) and str(r.get("status")) == "复用")]
            print(f"  跳过复用项 {len(reused_rows)} 条（不重写已有资产）")
        if not data:
            print(f"[{table}] 没有需要写入的新建项")
            return

    match_keys = {'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("cmd_write idempotency guard added")
