# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

# 角色 16:9
old = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/characters"), n=1)'''
new = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/characters"), n=1,
                                  size=_resolve_image_size("2K", "16:9"))'''
assert t.count(old) == 1
t = t.replace(old, new)

# 场景 22:9
old = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/scenes"), n=1,
                                  **({"ref_images": ref_images} if ref_images else {}))'''
new = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/scenes"), n=1,
                                  size=_resolve_image_size("2K", "22:9"),
                                  **({"ref_images": ref_images} if ref_images else {}))'''
assert t.count(old) == 1
t = t.replace(old, new)

# 道具 16:9
old = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/props"), n=1,
                                  **({"ref_images": ref_images} if ref_images else {}))'''
new = '''    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/props"), n=1,
                                  size=_resolve_image_size("2K", "16:9"),
                                  **({"ref_images": ref_images} if ref_images else {}))'''
assert t.count(old) == 1
t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("asset sizes wired")
