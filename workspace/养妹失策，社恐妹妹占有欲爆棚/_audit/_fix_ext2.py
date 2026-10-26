# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''            os.rename(paths[0], ws.abs(rel_path))
            task["result_path"] = rel_path'''
new = '''            os.rename(paths[0], ws.abs(rel_path))
            rel_path = ws.rel(_fix_image_ext(ws.abs(rel_path)))
            task["result_path"] = rel_path'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("workbench patched")
