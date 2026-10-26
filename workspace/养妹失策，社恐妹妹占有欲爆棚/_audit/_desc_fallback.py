# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

helper = '''def _image_prompt_from_desc(desc: str) -> str:
    """没有 gen_prompt 时，用资产描述当出图提示词；场景先去掉给分镜用的空间锚点行。"""
    d = re.split(r"空间锚点[：:]", desc or "")[0]
    return d.strip().strip("。；;，, \\n")


def _apply_global_style(ws, prompt: str) -> str:'''
old = '''def _apply_global_style(ws, prompt: str) -> str:'''
assert t.count(old) == 1
t = t.replace(old, helper)

# 角色
old = '''    prompt_template = char.get("gen_prompt", "")
    if not prompt_template:
        print(f"  跳过 {char['name']}: 未填写生成提示词")
        return'''
new = '''    prompt_template = (char.get("gen_prompt") or "").strip() or _image_prompt_from_desc(char.get("appearance", ""))
    if not prompt_template:
        print(f"  跳过 {char['name']}: 既没有生成提示词也没有外貌描述")
        return'''
assert t.count(old) == 1
t = t.replace(old, new)

# 场景
old = '''    prompt_template = scene.get("gen_prompt", "")
    label = scene["name"]
    if not prompt_template:
        print(f"  跳过 {label}: 未填写生成提示词")
        return'''
new = '''    prompt_template = (scene.get("gen_prompt") or "").strip() or _image_prompt_from_desc(scene.get("description", ""))
    label = scene["name"]
    if not prompt_template:
        print(f"  跳过 {label}: 既没有生成提示词也没有场景描述")
        return'''
assert t.count(old) == 1
t = t.replace(old, new)

# 道具
old = '''    prompt_template = prop.get("gen_prompt", "")
    label = prop["name"]
    if not prompt_template:
        print(f"  跳过 {label}: 未填写生成提示词")
        return'''
new = '''    prompt_template = (prop.get("gen_prompt") or "").strip() or _image_prompt_from_desc(prop.get("description", ""))
    label = prop["name"]
    if not prompt_template:
        print(f"  跳过 {label}: 既没有生成提示词也没有道具描述")
        return'''
assert t.count(old) == 1
t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("generators fall back to description")
