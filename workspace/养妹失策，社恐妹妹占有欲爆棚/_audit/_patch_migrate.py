# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

old = '''    plan = ws.feishu.plan_schema_migration()

    print("[迁移计划]")'''
new = '''    plan = ws.feishu.plan_schema_migration()
    existing_tables = ws.feishu.discover_tables()
    missing_tables = [x for x in ws.feishu.EXPECTED_TABLES if x not in existing_tables]

    print("[迁移计划]")'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''    print("  4. 本地 workspace.yaml: 将 feishu.tables 的「剧集表」键改为「剧本表」")'''
new = '''    print("  4. 本地 workspace.yaml: 将 feishu.tables 的「剧集表」键改为「剧本表」")
    print(f"  5. 补齐缺失标准表: {', '.join(missing_tables) if missing_tables else '无需'}")'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''    nothing = (not plan["rename"] and not plan["add_fields"] and plan["move_rows"] == 0)
    ws.feishu.apply_schema_migration(plan)'''
new = '''    nothing = (not plan["rename"] and not plan["add_fields"] and plan["move_rows"] == 0
               and not missing_tables)
    ws.feishu.apply_schema_migration(plan)

    if missing_tables:
        all_tables = ws.feishu.ensure_tables(existing_tables)
        tables_cfg = ws.config.get("feishu", {}).setdefault("tables", {})
        changed = False
        for name in missing_tables:
            tid = all_tables.get(name)
            if tid and tables_cfg.get(name) != tid:
                tables_cfg[name] = tid
                changed = True
        if changed:
            ws.save_config()
        print(f"  已补齐缺失表: {', '.join(missing_tables)}")'''
assert t.count(old) == 1
t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("migrate-schema patched")
