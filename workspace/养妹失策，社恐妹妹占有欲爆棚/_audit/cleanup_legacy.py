# -*- coding: utf-8 -*-
import re

# ---------- cli.py ----------
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()

def cut_block(text, start_marker, end_markers):
    i = text.index(start_marker)
    j = len(text)
    for em in end_markers:
        k = text.find(em, i + len(start_marker))
        if k != -1:
            j = min(j, k)
    return text[:i] + text[j:]

# 1) 删除三个旧生成分支（角色库/场景库/道具库）
for name in ("角色库", "场景库", "道具库"):
    start = f'        if kind == "{name}":' if name == "角色库" else f'        elif kind == "{name}":'
    if start not in c:
        print("skip branch", name); continue
    i = c.index(start)
    j = c.find('        elif kind ==', i + len(start))
    c = c[:i] + c[j:]

# 2) 删除旧生成函数
for fn in ("_generate_character(", "_generate_scene(", "_generate_prop("):
    if f"def {fn}" not in c:
        print("skip fn", fn); continue
    i = c.index(f"def {fn}")
    j = c.find("\ndef ", i + 1)
    c = c[:i] + (c[j+1:] if j != -1 else "")

# 3) 读表分发去掉三张旧表
c = c.replace('        "角色库": ws.load_characters, "场景库": ws.load_scenes, "道具库": ws.load_props,\n', "")
# 4) 写表 match_keys / json_files / push_methods 去掉
c = re.sub(r'\s*"角色库": "name", "场景库": "name", "道具库": "name",', "", c)
c = re.sub(r'\s*"角色库": "characters.json", "场景库": "scenes.json", "道具库": "props.json",', "", c)
c = re.sub(r'\s*"角色库": "push_characters", "场景库": "push_scenes", "道具库": "push_props",', "", c)
# 5) TTS 音色改从资产库取
c = c.replace('char_map = {x["name"]: x for x in ws.load_characters()}',
              'char_map = {x["name"]: x for x in ws.load_assets_lib() if x.get("kind") == "角色"}')
# 6) 帮助文本
c = c.replace('"--target 格式: 角色库:名 / 场景库:名 / 道具库:名 / 剧本分镜表:ID / 生图工作台:任务名或all"',
              '"--target 格式: 资产库:名 / 剧本分镜表:ID / 生图工作台:任务名或all"')
open(p, "w", encoding="utf-8").write(c)
print("cli 清理完成；残留:", c.count("角色库"), c.count("场景库"), c.count("道具库"))

# ---------- workspace.py ----------
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
w = open(p2, encoding="utf-8").read()
for fn in ("load_characters", "save_characters", "load_scenes", "save_scenes", "load_props", "save_props"):
    if f"def {fn}(" in w:
        i = w.index(f"    def {fn}(")
        j = w.find("\n    def ", i + 1)
        w = w[:i] + (w[j+1:] if j != -1 else "")
w = re.sub(r'\s*"角色库": \("load_characters", "name", \["ref_image"\]\),', "", w)
w = re.sub(r'\s*"场景库": \("load_scenes", "name", \["ref_image"\]\),', "", w)
w = re.sub(r'\s*"道具库": \("load_props", "name", \["ref_image"\]\),', "", w)
open(p2, "w", encoding="utf-8").write(w)
print("workspace 清理完成；残留:", w.count("load_characters"), w.count("load_scenes"), w.count("load_props"))
