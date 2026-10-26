# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

# 1) loaders
old = '''        "角色库": ws.load_characters, "场景库": ws.load_scenes,'''
new = '''        "角色库": ws.load_characters, "场景库": ws.load_scenes, "道具库": ws.load_props,'''
assert t.count(old) == 1
t = t.replace(old, new)

# 2) match keys
old = '''        "角色库": "name", "场景库": "name", "剧本设定": "name",'''
new = '''        "角色库": "name", "场景库": "name", "道具库": "name", "剧本设定": "name",'''
assert t.count(old) == 1
t = t.replace(old, new)

# 3) json files
old = '''        "角色库": "characters.json", "场景库": "scenes.json",'''
new = '''        "角色库": "characters.json", "场景库": "scenes.json", "道具库": "props.json",'''
assert t.count(old) == 1
t = t.replace(old, new)

# 4) push methods
old = '''            "角色库": "push_characters", "场景库": "push_scenes",'''
new = '''            "角色库": "push_characters", "场景库": "push_scenes", "道具库": "push_props",'''
assert t.count(old) == 1
t = t.replace(old, new)

# 5) generate: help 文案
old = '''            print("--target 格式: 角色库:名 / 场景库:名 / 剧本分镜表:ID / 生图工作台:任务名或all")'''
new = '''            print("--target 格式: 角色库:名 / 场景库:名 / 道具库:名 / 剧本分镜表:ID / 生图工作台:任务名或all")'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''        elif kind == "剧本分镜表":'''
new = '''        elif kind == "道具库":
            props = ws.load_props()
            matched = [x for x in props if x["name"] == target_id]
            if not matched:
                print(f"道具库中找不到: {target_id}")
                sys.exit(1)
            for prop in matched:
                print(f"=== 生成道具: {prop['name']} ===")
                _generate_prop(ws, prop, props)

        elif kind == "剧本分镜表":'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''            print(f"未知类型: {kind}，支持: 角色库 / 场景库 / 剧本分镜表 / 生图工作台")'''
new = '''            print(f"未知类型: {kind}，支持: 角色库 / 场景库 / 道具库 / 剧本分镜表 / 生图工作台")'''
assert t.count(old) == 1
t = t.replace(old, new)

# 6) _generate_prop（插在 _resolve_image_size 之前）
anchor = '''def _resolve_image_size(resolution: str, ratio: str) -> str:'''
func = '''def _generate_prop(ws, prop, props_list):
    """生成单个道具图。"""
    from vomin.ark.client import ArkClient
    from vomin.ark.image import ImageClient

    prompt_template = prop.get("gen_prompt", "")
    label = prop["name"]
    if not prompt_template:
        print(f"  跳过 {label}: 未填写生成提示词")
        return

    ark = ArkClient()
    image = ImageClient(ark)
    model = prop.get("gen_model") or ws.config.get("ark", {}).get("image_model", "doubao-seedream-5-0-flash-260915")

    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("道具库", label))

    print(f"  模型: {model}")
    print(f"  提示词: {final_prompt[:80]}...")
    if ref_images:
        print(f"  参考图: {len(ref_images)} 张")

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{label}".replace(" ", "_")
    rel_path = f"ref/props/{safe_name}_{ts}.png"

    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/props"), n=1,
                                  **({"ref_images": ref_images} if ref_images else {}))
    if paths:
        os.rename(paths[0], ws.abs(rel_path))
        prop["ref_image"] = rel_path
        prop["gen_status"] = "已出图"
        prop.setdefault("source", "AIGC生成")
        ws.save_json("props.json", props_list)
        if ws.feishu:
            try:
                ws.feishu.update_prop(ws, prop)
                print(f"  飞书已更新: {label}")
            except Exception as e:
                print(f"  飞书更新失败: {e}")
        size = os.path.getsize(ws.abs(rel_path)) / 1024
        print(f"  已保存: {rel_path} ({size:.0f} KB)")


def _resolve_image_size(resolution: str, ratio: str) -> str:'''
assert t.count(anchor) == 1
t = t.replace(anchor, func)

open(p, "w", encoding="utf-8").write(t)
print("cli.py patched")
