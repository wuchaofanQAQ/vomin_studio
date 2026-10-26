# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()
old = '''    chars = ws.load_characters()
    scenes = ws.load_scenes()
    props = ws.load_props()'''
if old in c:
    new = '''    lib = ws.load_assets_lib()
    chars = [a for a in lib if a.get("kind") == "角色"]
    scenes = [a for a in lib if a.get("kind") == "场景"]
    props = [a for a in lib if a.get("kind") == "道具"]'''
    c = c.replace(old, new)
    open(p, "w", encoding="utf-8").write(c)
    print("status -> 资产库计数")
else:
    print("未匹配 status 计数段")
