# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()
old = '''    print("\\n[角色库]")
    chars = ws.feishu.pull_characters(ws)
    print(f"  {len(chars)} 个角色")
    print("\\n[场景库]")
    scenes = ws.feishu.pull_scenes(ws)
    print(f"  {len(scenes)} 个场景")
    print("\\n[道具库]")
    props = ws.feishu.pull_props(ws)
    print(f"  {len(props)} 个道具")'''
new = '''    print("\\n[资产库]")
    try:
        alib = ws.feishu.pull_assets_lib(ws)
        print(f"  {len(alib)} 条资产")
    except Exception as e:
        print(f"  跳过资产库: {e}")'''
assert c.count(old) == 1
c = c.replace(old, new)
open(p, "w", encoding="utf-8").write(c)
print("cmd_pull: 旧三表已移除")
