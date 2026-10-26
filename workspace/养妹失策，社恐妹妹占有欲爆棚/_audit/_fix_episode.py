# -*- coding: utf-8 -*-
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

old = '''                "episode": f.get("集号", 1),'''
new = '''                "episode": int(float(f.get("集号", 1) or 1)),'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''                "集号": shot["episode"],'''
new2 = '''                "集号": int(float(shot.get("episode") or 1)),'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("bitable episode coercion added")

p = r"cli.py"
t = open(p, encoding="utf-8").read()
old3 = '''    print("\\n[场景库]")
    ws.feishu.push_scenes(ws)
    print("\\n[剧本设定]")'''
new3 = '''    print("\\n[场景库]")
    ws.feishu.push_scenes(ws)
    print("\\n[道具库]")
    ws.feishu.push_props(ws)
    print("\\n[剧本设定]")'''
assert t.count(old3) == 1
t = t.replace(old3, new3)

old4 = '''    print("\\n[场景库]")
    scenes = ws.feishu.pull_scenes(ws)
    print(f"  {len(scenes)} 个场景")'''
new4 = '''    print("\\n[场景库]")
    scenes = ws.feishu.pull_scenes(ws)
    print(f"  {len(scenes)} 个场景")
    print("\\n[道具库]")
    props = ws.feishu.pull_props(ws)
    print(f"  {len(props)} 个道具")'''
assert t.count(old4) == 1
t = t.replace(old4, new4)
open(p, "w", encoding="utf-8").write(t)
print("cli push/pull include props")
