# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()

# 1) 生成分支：资产库
anchor = '''        elif kind == "剧本分镜表":'''
if 'kind == "资产库"' not in c:
    branch = '''        elif kind == "资产库":
            lib = ws.load_assets_lib()
            targets = [a for a in lib if a["name"] == target_id] or \\
                      [a for a in lib if target_id in a["name"]]
            if not targets:
                print(f"资产库中找不到: {target_id}")
                sys.exit(1)
            for a in targets:
                print(f"=== 生成资产: {a['name']}（{a['kind']}）===")
                _generate_asset_lib(ws, a, lib)

'''
    assert c.count(anchor) == 1
    c = c.replace(anchor, branch + anchor)

# 2) 生成函数
if "def _generate_asset_lib" not in c:
    fn_anchor = "def _generate_scene(ws, scene, scenes_list):"
    fn = '''def _generate_asset_lib(ws, asset, lib):
    """按资产类型生成图（角色四视角 / 场景 / 道具双视角）。"""
    import base64 as _b64
    from vomin.ark.client import ArkClient
    from vomin.ark.image import ImageClient
    import importlib.util as _ilu

    spec = _ilu.spec_from_file_location(
        "asset_prompt",
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "skills", "drama-asset-generation", "scripts", "asset_prompt.py"))
    ap = _ilu.module_from_spec(spec)
    spec.loader.exec_module(ap)

    kind = asset.get("kind") or "道具"
    desc = (asset.get("description") or "").strip()
    if not desc:
        print("  跳过：资产没有描述")
        return
    prompt = ap.build(kind, desc)

    final_prompt, ref_images, _, _, _ = ws.expand_prompt(prompt, skip_self=("资产库", asset["name"]))
    final_prompt = _apply_global_style(ws, final_prompt)

    model = ws.config.get("ark", {}).get("image_model", "doubao-seedream-5-0-flash-260915")
    ratio = {"角色": "16:9", "场景": "22:9", "道具": "16:9"}.get(kind, "16:9")
    sub = {"角色": "characters", "场景": "scenes", "道具": "props"}.get(kind, "props")

    print(f"  模型: {model}")
    print(f"  提示词: {final_prompt[:80]}...")
    if ref_images:
        print(f"  参考图: {len(ref_images)} 张")

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = ImageClient(ArkClient()).generate_to_dir(
        model=model, prompt=final_prompt, save_dir=ws.abs(f"ref/{sub}"), n=1,
        size=_resolve_image_size("2K", ratio),
        **({"ref_images": ref_images} if ref_images else {}))
    if not paths:
        print("  生成失败")
        return
    safe = str(asset["name"]).replace(" ", "_")
    rel = f"ref/{sub}/{safe}_{ts}.png"
    os.rename(paths[0], ws.abs(rel))
    rel = ws.rel(_fix_image_ext(ws.abs(rel)))
    asset["file_path"] = rel
    ws.save_json("assets_lib.json", lib)
    if ws.feishu:
        try:
            ws.feishu.push_assets_lib(ws)
            print(f"  飞书已更新: {asset['name']}")
        except Exception as e:
            print(f"  飞书更新失败: {e}")
    print(f"  已保存: {rel}")

'''
    assert c.count(fn_anchor) == 1
    c = c.replace(fn_anchor, fn + fn_anchor)

open(p, "w", encoding="utf-8").write(c)
print("generate -> 资产库 已接")
