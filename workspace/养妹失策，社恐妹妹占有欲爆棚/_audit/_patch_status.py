# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''    chars = ws.load_characters()
    scenes = ws.load_scenes()
    print(f"角色: {len(chars)} 个  |  场景: {len(scenes)} 个")'''
new = '''    chars = ws.load_characters()
    scenes = ws.load_scenes()
    props = ws.load_props()
    print(f"角色: {len(chars)} 个  |  场景: {len(scenes)} 个  |  道具: {len(props)} 个")'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("status patched")
