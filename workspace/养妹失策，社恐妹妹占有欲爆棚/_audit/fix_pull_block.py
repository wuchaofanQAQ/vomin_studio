# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()
broken = '''    try:
        print("\\n[资产库]")
    try:
        alib = ws.feishu.pull_assets_lib(ws)
        print(f"  {len(alib)} 条资产")
    except Exception as e:
        print(f"  跳过资产库: {e}")
    print("\\n[小说表]")
        novels = ws.feishu.pull_novels(ws)
        print(f"  {len(novels)} 章")
    except Exception as e:
        print(f"  跳过小说表: {e}")'''
fixed = '''    try:
        print("\\n[资产库]")
        alib = ws.feishu.pull_assets_lib(ws)
        print(f"  {len(alib)} 条资产")
    except Exception as e:
        print(f"  跳过资产库: {e}")
    try:
        print("\\n[小说表]")
        novels = ws.feishu.pull_novels(ws)
        print(f"  {len(novels)} 章")
    except Exception as e:
        print(f"  跳过小说表: {e}")'''
assert c.count(broken) == 1
open(p, "w", encoding="utf-8").write(c.replace(broken, fixed))
print("fixed pull block")
