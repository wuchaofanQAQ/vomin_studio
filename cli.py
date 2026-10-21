#!/usr/bin/env python3
"""Vomin Studio CLI — AI 短剧制作流水线"""
import argparse
import os
import re
import sys
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# 所有剧本 workspace 的默认根目录：项目根/workspace，一个剧本一个文件夹
DEFAULT_WORKSPACE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workspace")


def sanitize_dirname(name: str) -> str:
    """把剧名清洗成合法的 Windows 文件夹名。"""
    cleaned = re.sub(r'[\\/:*?"<>|]', "_", (name or "").strip()).rstrip(". ")
    return cleaned or "未命名剧本"


def resolve_init_path(workspace: str | None, drama_name: str) -> str:
    """workspace 未显式指定时，默认落到 <项目根>/workspace/{剧名}。"""
    if workspace:
        return os.path.abspath(workspace)
    path = os.path.join(DEFAULT_WORKSPACE_ROOT, sanitize_dirname(drama_name))
    print(f"未指定路径，使用默认项目目录: {path}")
    return os.path.abspath(path)


def write_system_config(feishu, tables: dict, ws_root: str, drama_name: str):
    """初始化后把项目级引导配置写入飞书「系统设置」表。"""
    table_id = (tables or {}).get("系统设置", "")
    items = [
        ("项目路径", os.path.abspath(ws_root),
         "当前剧本项目 workspace 的本地绝对路径；切换目录或电脑后运行 set-path 更新"),
        ("剧名", drama_name, "剧本名称；workspace 根目录下一个剧本一个文件夹"),
        ("创建时间", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "项目初始化时间"),
    ]
    for key, value, desc in items:
        feishu.upsert_config_value(key, value, description=desc, table_id=table_id)
    print("  系统设置已写入: 项目路径 / 剧名 / 创建时间")


def resolve_workspace(target: str):
    """把命令行传入的目标解析为 Workspace。

    target 支持两种形式：
      1. 本地 workspace 目录路径（原有行为）；
      2. 飞书多维表格 URL（含 /base/ 或 /wiki/）：先连飞书读取「系统设置」
         表中的「项目路径」，再用该路径定位本地 workspace。

    这样本地目录可以随时迁移，只需在飞书系统设置里更新一次路径。
    """
    from vomin.workspace import Workspace
    from vomin.feishu.bitable import FeishuBitable

    if not (target.startswith("http://") or target.startswith("https://")):
        return Workspace(target)

    try:
        app_token = FeishuBitable.parse_app_token(target)
    except ValueError as e:
        print(e)
        sys.exit(1)

    feishu = FeishuBitable(app_token=app_token)
    try:
        root = feishu.get_config_value("项目路径")
    except Exception as e:
        print(f"读取飞书「系统设置」失败: {e}")
        sys.exit(1)

    if not root:
        print("飞书「系统设置」中未配置「项目路径」。")
        print("请先用本地路径执行一次注册: python cli.py set-path <workspace目录>")
        sys.exit(1)

    root = os.path.abspath(root)
    if not os.path.exists(os.path.join(root, "workspace.yaml")):
        print(f"飞书配置的「项目路径」无效，该目录下找不到 workspace.yaml:\n  {root}")
        print("若本地目录已迁移，请在新目录执行: python cli.py set-path <workspace目录>")
        sys.exit(1)

    print(f"已从飞书定位到本地项目: {root}")
    return Workspace(root)


def cmd_set_path(args):
    """把当前本地 workspace 的绝对路径写回飞书「系统设置」（换目录后执行一次）。"""
    from vomin.workspace import Workspace

    ws_path = os.path.abspath(args.workspace)
    if not os.path.exists(os.path.join(ws_path, "workspace.yaml")):
        print(f"该目录不是有效的 workspace（缺少 workspace.yaml）: {ws_path}")
        sys.exit(1)

    ws = Workspace(ws_path)
    if not ws.feishu:
        print("未配置飞书（缺少 app_token 或 FEISHU_APP_ID/SECRET 凭据），无法更新")
        sys.exit(1)

    table_id = ws.config.get("feishu", {}).get("tables", {}).get("系统设置", "")
    try:
        ws.feishu.upsert_config_value(
            "项目路径",
            ws.root,
            description="当前剧本项目 workspace 的本地绝对路径；切换本地目录或电脑后，运行 set-path 更新",
            table_id=table_id,
        )
    except Exception as e:
        print(f"写入飞书失败: {e}")
        sys.exit(1)
    print(f"已将项目路径写入飞书「系统设置」: {ws.root}")


def cmd_init(args):
    from vomin.workspace import Workspace
    from vomin.feishu.bitable import FeishuBitable

    ws_path = resolve_init_path(args.workspace, args.name)
    if os.path.exists(os.path.join(ws_path, "workspace.yaml")):
        print(f"workspace 已存在: {ws_path}")
        print("如需重新初始化，请先删除该目录或使用新路径")
        sys.exit(1)

    print(f"初始化项目: {args.name}")
    print()

    # 1. 创建飞书多维表格
    print("[飞书]")
    feishu = FeishuBitable()
    project = feishu.create_project(args.name)
    print()

    # 2. 创建本地 workspace
    print("[本地]")
    ws = Workspace.init_workspace(
        ws_path,
        drama_name=args.name,
        feishu_app_token=project["app_token"],
        feishu_tables=project["tables"],
        feishu_url=project["url"],
    )
    print(f"  workspace 已创建: {ws.root}")

    # 3. 写入飞书「系统设置」表
    try:
        write_system_config(feishu, project["tables"], ws.root, args.name)
    except Exception as e:
        print(f"  警告: 写入系统设置失败（不影响本地初始化）: {e}")
    print()
    print(f"飞书表格: {project['url']}")
    print(f"本地目录: {ws.root}")
    print()
    print("下一步（drama-initializer 产出确认后）:")
    print(f"  1. python cli.py write {ws.root} --table 剧本设定 --data @settings.json")
    print(f"  2. python cli.py write {ws.root} --table 角色库 --data @characters.json")
    print(f"  3. python cli.py write {ws.root} --table 角色档案 --data @bibles.json")
    print(f"  4. 逐集：novel-to-script 转剧本后 write --table 剧本表（见 harness B0a）")
    print(f"  5. python cli.py push {ws.root}")


def cmd_status(args):
    from vomin.workspace import Workspace
    ws = resolve_workspace(args.workspace)
    cfg = ws.config
    shots = ws.load_storyboard()

    print(f"=== {cfg.get('drama_name', '未命名')} ===")
    feishu_url = cfg.get("feishu", {}).get("url", "")
    if feishu_url:
        print(f"飞书表格: {feishu_url}")
    print(f"本地目录: {ws.root}")
    print(f"预算: {cfg.get('budget', {}).get('spent', 0):.2f} / {cfg.get('budget', {}).get('total_limit', 5000)} 元")
    print(f"分镜: {len(shots)} 个")

    chars = ws.load_characters()
    scenes = ws.load_scenes()
    print(f"角色: {len(chars)} 个  |  场景: {len(scenes)} 个")
    print()

    status_count = {}
    for s in shots:
        st = s.get("status", "未知")
        status_count[st] = status_count.get(st, 0) + 1

    for st, cnt in sorted(status_count.items()):
        print(f"  {st}: {cnt}")
    print()

    for s in shots:
        audio = "✓" if s.get("audio_path") else "·"
        video = "✓" if s.get("video_path") else "·"
        print(f"  {s['shot_id']:12s}  [{s.get('status', '?'):6s}]  音频{audio}  视频{video}  {s.get('dialogue', '')[:30]}")


def _add_asset(ws, asset_type, name, file_path, model, prompt):
    """往飞书素材库追加一条记录（静默失败）。"""
    from datetime import datetime
    asset_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        ws.feishu.add_asset(ws, {
            "name": asset_id,
            "file_path": file_path,
            "asset_type": asset_type,
            "model": model,
            "prompt": prompt[:500],
            "source": "AIGC生成",
        })
    except Exception as e:
        print(f"  素材库记录失败: {e}")


def _generate_character(ws, char, chars_list):
    """生成单个角色形象图。"""
    from vomin.ark.client import ArkClient
    from vomin.ark.image import ImageClient

    prompt_template = char.get("gen_prompt", "")
    if not prompt_template:
        print(f"  跳过 {char['name']}: 未填写生成提示词")
        return

    ark = ArkClient()
    image = ImageClient(ark)
    model = char.get("gen_model") or ws.config.get("ark", {}).get("image_model", "doubao-seedream-5-0-flash-260915")

    final_prompt, _, _, _, _ = ws.expand_prompt(prompt_template, skip_self=("角色库", char["name"]))

    print(f"  模型: {model}")
    print(f"  提示词: {final_prompt[:80]}...")

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = char["name"].replace(" ", "_")
    rel_path = f"ref/characters/{safe_name}_{ts}.png"

    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/characters"), n=1)
    if paths:
        os.rename(paths[0], ws.abs(rel_path))
        char["ref_image"] = rel_path
        char.setdefault("source", "AIGC生成")
        ws.save_json("characters.json", chars_list)
        if ws.feishu:
            try:
                ws.feishu.update_character(ws, char)
                print(f"  飞书已更新: {char['name']}")
            except Exception as e:
                print(f"  飞书更新失败: {e}")
        size = os.path.getsize(ws.abs(rel_path)) / 1024
        print(f"  已保存: {rel_path} ({size:.0f} KB)")
        if ws.feishu:
            _add_asset(ws, "角色形象图", char["name"], rel_path, model, final_prompt)


def _generate_scene(ws, scene, scenes_list):
    """生成单个场景视角参考图。"""
    from vomin.ark.client import ArkClient
    from vomin.ark.image import ImageClient

    prompt_template = scene.get("gen_prompt", "")
    view_angle = scene.get("view_angle", "全景基准图（默认）")
    label = f"{scene['name']}·{view_angle}"
    if not prompt_template:
        print(f"  跳过 {label}: 未填写生成提示词")
        return

    ark = ArkClient()
    image = ImageClient(ark)
    model = scene.get("gen_model") or ws.config.get("ark", {}).get("image_model", "doubao-seedream-5-0-flash-260915")

    skip_key = f"{scene['name']}·{view_angle}"
    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("场景库", skip_key))

    print(f"  视角: {view_angle}")
    print(f"  模型: {model}")
    print(f"  提示词: {final_prompt[:80]}...")
    if ref_images:
        print(f"  参考图: {len(ref_images)} 张")

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{scene['name']}_{view_angle}".replace(" ", "_")
    rel_path = f"ref/scenes/{safe_name}_{ts}.png"

    paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                  save_dir=ws.abs("ref/scenes"), n=1,
                                  **({"ref_images": ref_images} if ref_images else {}))
    if paths:
        os.rename(paths[0], ws.abs(rel_path))
        scene["ref_image"] = rel_path
        scene["gen_status"] = "已出图"
        scene.setdefault("source", "AIGC生成")
        ws.save_json("scenes.json", scenes_list)
        if ws.feishu:
            try:
                ws.feishu.update_scene(ws, scene)
                print(f"  飞书已更新: {label}")
            except Exception as e:
                print(f"  飞书更新失败: {e}")
        size = os.path.getsize(ws.abs(rel_path)) / 1024
        print(f"  已保存: {rel_path} ({size:.0f} KB)")
        if ws.feishu:
            _add_asset(ws, "场景参考图", label, rel_path, model, final_prompt)


def _resolve_image_size(resolution: str, ratio: str) -> str:
    """把「2K + 16:9」换算成具体像素；分辨率本身写了 1024x768 时原样使用。"""
    r = (resolution or "").strip()
    if re.fullmatch(r"\d+\s*[xX×]\s*\d+", r):
        return r.replace(" ", "").replace("×", "x").replace("X", "x")
    base = {"1K": 1024, "2K": 2048, "4K": 4096}.get(r.upper(), 2048)
    if (ratio or "16:9").strip() == "9:16":
        return f"{base * 9 // 16}x{base}"
    return f"{base}x{base * 9 // 16}"


def _generate_workbench_task(ws, task, tasks_list):
    """执行一条生图工作台任务。"""
    from vomin.ark.client import ArkClient
    from vomin.ark.image import ImageClient

    prompt_template = (task.get("prompt") or "").strip()
    if not prompt_template:
        print("  跳过：未填写提示词")
        return
    if not task.get("name"):
        task["name"] = prompt_template.splitlines()[0][:20]

    ark = ArkClient()
    image = ImageClient(ark)
    default_model = ws.config.get("ark", {}).get("image_model", "doubao-seedream-5-0-flash-260915")
    model = task.get("model") or default_model
    ratio = task.get("ratio") or "16:9"
    size = _resolve_image_size(task.get("size") or "2K", ratio)

    final_prompt, ref_images_abs, _, _, _ = ws.expand_prompt(prompt_template)

    ref_images = ref_images_abs if ref_images_abs else None
    if ref_images:
        for p in ref_images:
            print(f"  参考图: {ws.rel(p)}")

    task["status"] = "生成中"
    ws.save_json("workbench.json", tasks_list)
    if ws.feishu:
        try:
            ws.feishu.update_workbench_task(ws, task)
        except Exception:
            pass

    print(f"  模型: {model}")
    print(f"  画面: {ratio} / {size}")
    print(f"  提示词: {final_prompt[:80]}...")

    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = task["name"].replace(" ", "_").replace("/", "_")
    rel_path = f"ref/workbench/{safe_name}_{ts}.png"

    try:
        paths = image.generate_to_dir(model=model, prompt=final_prompt,
                                      save_dir=ws.abs("ref/workbench"), n=1,
                                      size=size, ref_images=ref_images)
        if paths:
            os.rename(paths[0], ws.abs(rel_path))
            task["result_path"] = rel_path
            task["status"] = "已完成"
            ws.save_json("workbench.json", tasks_list)
            if ws.feishu:
                try:
                    ws.feishu.update_workbench_task(ws, task)
                except Exception as e:
                    print(f"  飞书更新失败: {e}")
            fsize = os.path.getsize(ws.abs(rel_path)) / 1024
            print(f"  已保存: {rel_path} ({fsize:.0f} KB)")
    except Exception as e:
        task["status"] = "生成失败"
        task["notes"] = str(e)[:200]
        ws.save_json("workbench.json", tasks_list)
        if ws.feishu:
            try:
                ws.feishu.update_workbench_task(ws, task)
            except Exception:
                pass
        print(f"  生成失败: {e}")


_TIMELINE_RE = re.compile(r"\s*(\d+):(\d+)\s*[-–—~]\s*(\d+):(\d+)")
_DIALOGUE_LINE_RE = re.compile(r"^\s*([^：:\n]{1,20}?)\s*[：:]\s*(.+?)\s*$")
MAX_SHOT_SECONDS = 30


def _shot_duration(shot, default):
    """成片时长取分段 timeline（如 00:00-00:20）的真实秒数，上限 30 秒；解析不出则用配置默认值。"""
    m = _TIMELINE_RE.match(shot.get("timeline") or "")
    if m:
        span = (int(m[3]) * 60 + int(m[4])) - (int(m[1]) * 60 + int(m[2]))
        if span > 0:
            return min(span, MAX_SHOT_SECONDS)
    return default


def _dialogue_lines(shot, fallback_speaker):
    """把分镜 dialogue 拆成 [(说话人, 台词)]；无「角色：」前缀的行归给 fallback_speaker。"""
    lines = []
    for raw in (shot.get("dialogue") or "").splitlines():
        if not raw.strip():
            continue
        m = _DIALOGUE_LINE_RE.match(raw)
        if m:
            speaker = re.sub(r"[（(].*?[）)]", "", m[1]).strip() or fallback_speaker
            lines.append((speaker, m[2]))
        else:
            lines.append((fallback_speaker, raw.strip()))
    return lines


def _generate_shot(ws, shot, shots_list, *, tts_only=False):
    """生成单个分镜的配音和/或视频。"""
    import base64 as b64
    from vomin.tts.doubao import DoubaoTTS

    cfg = ws.config
    bible_map = {b["name"]: b for b in ws.load_character_bibles()}
    ep = shot["episode"]
    shot_id = shot["shot_id"]

    # --- TTS 配音：按对白每行的说话人，从角色档案取音色描述 ---
    if shot.get("dialogue"):
        _, _, prompt_chars, _, _ = ws.expand_prompt(shot.get("prompt", ""))
        fallback = shot.get("speaker") or (prompt_chars[0] if prompt_chars else "旁白")
        lines = _dialogue_lines(shot, fallback)

        for old_rel in filter(None, (shot.get("audio_path") or "").split(";")):
            bak = ws.backup(old_rel)
            if bak:
                print(f"  备份旧配音: {bak}")

        tts = DoubaoTTS()
        tts_cfg = cfg.get("tts", {})
        audio_rels = []
        for idx, (speaker_name, text) in enumerate(lines, 1):
            bible = bible_map.get(speaker_name)
            if bible is None or not bible.get("voice_desc"):
                print(f"  警告: 角色档案中找不到「{speaker_name}」的音色描述，使用默认音色")
                bible = bible or {}
            voice_desc = bible.get("voice_desc") or "青年，普通话标准"
            text_prompt = f'{speaker_name}（{voice_desc}）说道："{text}"'

            audio_rel = f"ep{ep:02d}/audio/{shot_id}_{idx:02d}.mp3"
            os.makedirs(os.path.dirname(ws.abs(audio_rel)), exist_ok=True)
            print(f"  TTS[{idx}/{len(lines)}]: {text_prompt[:50]}...")
            result = tts.create_to_file(
                text_prompt, ws.abs(audio_rel),
                model=tts_cfg.get("model", "seed-audio-1.0"),
                fmt=tts_cfg.get("format", "mp3"),
                sample_rate=tts_cfg.get("sample_rate", 48000),
            )
            audio_rels.append(audio_rel)
            print(f"  配音完成: {audio_rel} ({result.get('original_duration', 0):.1f}s)")
        shot["audio_path"] = ";".join(audio_rels)

    # --- 视频生成 ---
    if not tts_only:
        from vomin.ark.client import ArkClient
        from vomin.ark.video import VideoClient

        if shot.get("video_path"):
            bak = ws.backup(shot["video_path"])
            if bak:
                print(f"  备份旧视频: {bak}")

        final_prompt, ref_images, chars_found, scenes_found, ref_videos = ws.expand_prompt(shot["prompt"])

        global_prompt_raw = ws.get_global_prompt()
        if global_prompt_raw:
            global_expanded, global_refs, _, _, global_videos = ws.expand_prompt(global_prompt_raw)
            final_prompt = f"{final_prompt}，{global_expanded}"
            ref_images = list(ref_images) + [r for r in global_refs if r not in ref_images]
            ref_videos = list(ref_videos) + [r for r in global_videos if r not in ref_videos]

        print(f"  提示词: {final_prompt[:80]}...")
        content = [{"type": "text", "text": final_prompt}]

        all_refs = list(ref_images)
        for abs_gimg in ws.get_global_ref_images():
            if abs_gimg not in all_refs:
                all_refs.append(abs_gimg)

        for img_path in all_refs:
            with open(img_path, "rb") as imgf:
                img_b64 = b64.b64encode(imgf.read()).decode()
            ext = os.path.splitext(img_path)[1].lstrip(".").lower() or "png"
            mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "gif": "image/gif", "bmp": "image/bmp"}.get(ext, "image/png")
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{img_b64}"},
                "role": "reference_image",
            })
            print(f"  参考图: {ws.rel(img_path)}")

        for vid_path in ref_videos:
            with open(vid_path, "rb") as vidf:
                vid_b64 = b64.b64encode(vidf.read()).decode()
            ext = os.path.splitext(vid_path)[1].lstrip(".").lower() or "mp4"
            mime = {"mp4": "video/mp4", "mov": "video/quicktime", "webm": "video/webm"}.get(ext, "video/mp4")
            content.append({
                "type": "video_url",
                "video_url": {"url": f"data:{mime};base64,{vid_b64}"},
                "role": "reference_video",
            })
            print(f"  参考视频: {ws.rel(vid_path)}")

        has_audio_ref = False
        for audio_rel in filter(None, (shot.get("audio_path") or "").split(";")):
            audio_abs = ws.abs(audio_rel)
            if not os.path.exists(audio_abs):
                continue
            with open(audio_abs, "rb") as af:
                audio_b64 = b64.b64encode(af.read()).decode()
            content.append({
                "type": "audio_url",
                "audio_url": {"url": f"data:audio/mp3;base64,{audio_b64}"},
                "role": "reference_audio",
            })
            has_audio_ref = True
            print(f"  参考音频: {audio_rel}")

        video_rel = f"ep{ep:02d}/video/{shot_id}.mp4"
        os.makedirs(os.path.dirname(ws.abs(video_rel)), exist_ok=True)

        ark_cfg = cfg.get("ark", {})
        duration = _shot_duration(shot, ark_cfg.get("default_duration", 5))
        print(f"  成片时长: {duration} 秒")
        shot["status"] = "生成中"
        ws.save_storyboard(shots_list)
        if ws.feishu:
            try:
                ws.feishu.update_shot(ws, shot)
            except Exception:
                pass

        try:
            ark = ArkClient()
            video_client = VideoClient(ark)
            video_model = ark_cfg.get("video_model", "doubao-seedance-2-5-260628")
            if not has_audio_ref:
                video_model = ark_cfg.get("video_model_fast", video_model)

            task = video_client.create_and_download(
                model=video_model,
                content=content,
                save_path=ws.abs(video_rel),
                resolution=ark_cfg.get("default_resolution", "720p"),
                ratio=ark_cfg.get("default_ratio", "9:16"),
                duration=duration,
                generate_audio=has_audio_ref,
            )
            shot["video_path"] = video_rel
            shot["task_id"] = task.get("id")
            shot["status"] = "待审核"
            cost = duration * 0.6
            ws.update_budget(cost)
            print(f"  视频完成: {video_rel} (预估 {cost:.1f} 元)")
        except Exception as e:
            shot["status"] = "生成失败"
            shot["notes"] = str(e)[:200]
            print(f"  视频失败: {e}")
    elif tts_only and shot.get("audio_path"):
        shot["status"] = "待审核"

    ws.save_storyboard(shots_list)
    if ws.feishu:
        try:
            ws.feishu.update_shot(ws, shot)
        except Exception:
            pass


def _scene_generate_order(view: str) -> int:
    """场景出图顺序：母版 → 主场景 → 局部 → 其他（闪回/外景/全景基准图）。"""
    view = view or ""
    for i, prefix in enumerate(("母版", "主场景", "局部")):
        if view.startswith(prefix):
            return i
    return 3


def _preflight_shots(ws, shots) -> list[str]:
    """逐个分镜校验资产引用，返回问题列表。"""
    problems = []
    for shot in shots:
        for p in ws.validate_asset_refs(shot.get("prompt", "")):
            problems.append(f"{shot.get('shot_id', '?')}: {p}")
    return problems


def cmd_preflight(args):
    """生产态前置校验：分镜引用的角色图/场景图是否真的存在且格式正确。"""
    from vomin.workspace import Workspace

    ws = resolve_workspace(args.workspace)
    shots = ws.load_storyboard()
    if args.episode is not None:
        shots = [s for s in shots if str(s.get("episode")) == str(args.episode)]
    if not shots:
        print("没有分镜数据（先 write 分镜表或 pull）")
        sys.exit(1)

    print(f"资产前置校验：{len(shots)} 个分镜")
    problems = _preflight_shots(ws, shots)
    if problems:
        print(f"\n✗ 未通过 {len(problems)} 项：")
        for p in problems:
            print(f"  - {p}")
        print("\n预览可以继续，但禁止调用模型生成视频。")
        sys.exit(1)
    print("✓ 全部资产就绪，可进入生成")


def cmd_generate(args):
    from vomin.workspace import Workspace
    ws = resolve_workspace(args.workspace)

    if args.target:
        parts = args.target.split(":", 1)
        if len(parts) != 2:
            print("--target 格式: 角色库:名 / 场景库:名 / 剧本分镜表:ID / 生图工作台:任务名或all")
            sys.exit(1)
        kind, target_id = parts

        if kind == "角色库":
            chars = ws.load_characters()
            char = next((c for c in chars if c["name"] == target_id), None)
            if not char:
                print(f"角色库中找不到: {target_id}")
                sys.exit(1)
            print(f"=== 生成角色: {target_id} ===")
            _generate_character(ws, char, chars)

        elif kind == "场景库":
            scenes = ws.load_scenes()
            if "·" in target_id:
                scene_name, view = target_id.split("·", 1)
                matched = [s for s in scenes
                           if s["name"] == scene_name and s.get("view_angle", "全景基准图（默认）") == view]
            else:
                matched = [s for s in scenes if s["name"] == target_id]
            if not matched:
                print(f"场景库中找不到: {target_id}")
                sys.exit(1)
            # 母版 → 主场景 → 局部 → 闪回/外景：派生图的参考图句引用母版，母版须先出图
            matched.sort(key=lambda s: _scene_generate_order(s.get("view_angle", "")))
            for scene in matched:
                label = f"{scene['name']}·{scene.get('view_angle', '全景基准图（默认）')}"
                print(f"=== 生成场景: {label} ===")
                _generate_scene(ws, scene, scenes)

        elif kind == "剧本分镜表":
            shots = ws.load_storyboard()
            shot = next((s for s in shots if s["shot_id"] == target_id), None)
            if not shot:
                print(f"分镜表中找不到: {target_id}")
                sys.exit(1)
            if not args.tts_only:
                problems = _preflight_shots(ws, [shot])
                if problems:
                    print("✗ 资产未就绪，已阻止生成视频：")
                    for p in problems:
                        print(f"  - {p}")
                    sys.exit(1)
            print(f"=== 生成分镜: {target_id} ===")
            _generate_shot(ws, shot, shots, tts_only=args.tts_only)

        elif kind == "生图工作台":
            tasks = ws.load_workbench()
            if target_id in ("all", "*", "全部"):
                pending = [t for t in tasks if t.get("status") not in ("已完成", "已生成")]
                if not pending:
                    print("没有待生成的工作台任务")
                    return
                print(f"批量生成工作台任务: {len(pending)} 条")
                for task in pending:
                    print(f"\n=== {task.get('name') or '（无任务名）'} ===")
                    _generate_workbench_task(ws, task, tasks)
            else:
                task = next((t for t in tasks if t.get("name") == target_id), None)
                if not task:
                    print(f"生图工作台中找不到: {target_id}")
                    sys.exit(1)
                print(f"=== 工作台任务: {target_id} ===")
                _generate_workbench_task(ws, task, tasks)

        else:
            print(f"未知类型: {kind}，支持: 角色库 / 场景库 / 剧本分镜表 / 生图工作台")
            sys.exit(1)
    else:
        shots = ws.load_storyboard()
        pending = [s for s in shots if s.get("status") in ("待生成", "返工")]
        if not pending:
            print("没有待生成的分镜")
            return
        print(f"批量生成: {len(pending)} 个分镜" + (" (仅TTS)" if args.tts_only else ""))
        if not args.tts_only:
            problems = _preflight_shots(ws, pending)
            if problems:
                print("✗ 资产未就绪，已阻止生成视频：")
                for p in problems:
                    print(f"  - {p}")
                sys.exit(1)
        for shot in pending:
            print(f"\n=== {shot['shot_id']} ===")
            _generate_shot(ws, shot, shots, tts_only=args.tts_only)

    print("\n生成完成。")


def cmd_workbench(args):
    """生图工作台批量出图：所有未完成的任务依次生成。"""
    from vomin.workspace import Workspace

    ws = resolve_workspace(args.workspace)
    tasks = ws.load_workbench()
    pending = [t for t in tasks if t.get("status") not in ("已完成", "已生成")]
    if not pending:
        print("没有待生成的工作台任务")
        return
    print(f"生图工作台开始工作：{len(pending)} 条待生成")
    for task in pending:
        print(f"\n=== {task.get('name') or '（无任务名）'} ===")
        _generate_workbench_task(ws, task, tasks)
    print("\n全部完成")


def cmd_push(args):
    from vomin.workspace import Workspace
    ws = resolve_workspace(args.workspace)
    if not ws.feishu:
        print("未配置飞书，跳过")
        return

    print("同步本地数据到飞书...")
    print("\n[剧本分镜表]")
    ws.feishu.push_storyboard(ws)
    print("\n[角色库]")
    ws.feishu.push_characters(ws)
    print("\n[场景库]")
    ws.feishu.push_scenes(ws)
    print("\n[剧本设定]")
    ws.feishu.push_settings(ws)
    print("\n[剧本表]")
    ws.feishu.push_episodes(ws)
    print("\n[角色档案]")
    ws.feishu.push_character_bibles(ws)
    print("\n完成")


def cmd_pull(args):
    from vomin.workspace import Workspace
    ws = resolve_workspace(args.workspace)
    if not ws.feishu:
        print("未配置飞书，跳过")
        return

    print("从飞书拉取到本地缓存...")
    ws.invalidate_cache()
    print("\n[角色库]")
    chars = ws.feishu.pull_characters(ws)
    print(f"  {len(chars)} 个角色")
    print("\n[场景库]")
    scenes = ws.feishu.pull_scenes(ws)
    print(f"  {len(scenes)} 个场景")
    print("\n[剧本分镜表]")
    shots = ws.feishu.pull_storyboard(ws)
    print("\n[剧本设定]")
    settings = ws.feishu.pull_settings(ws)
    print("\n[剧本表]")
    episodes = ws.feishu.pull_episodes(ws)
    print(f"  {len(episodes)} 条剧集")
    print("\n[角色档案]")
    bibles = ws.feishu.pull_character_bibles(ws)
    print(f"  {len(bibles)} 份角色档案")
    print("\n[素材库]")
    assets = ws.feishu.pull_assets(ws)
    print(f"  {len(assets)} 条素材")
    print("\n[生图工作台]")
    tasks = ws.feishu.pull_workbench(ws)
    print(f"  {len(tasks)} 条任务")
    print("\n完成")


def cmd_init_from_url(args):
    from vomin.workspace import Workspace
    from vomin.feishu.bitable import FeishuBitable

    ws_path = resolve_init_path(args.workspace, args.name)
    if os.path.exists(os.path.join(ws_path, "workspace.yaml")):
        print(f"workspace 已存在: {ws_path}")
        sys.exit(1)

    app_token = FeishuBitable.parse_app_token(args.url)
    print(f"解析飞书 app_token: {app_token}")

    feishu = FeishuBitable(app_token=app_token)
    existing = feishu.discover_tables()
    print(f"已发现 {len(existing)} 张表: {', '.join(existing.keys())}")

    tables = feishu.ensure_tables(existing)
    print(f"表结构已就绪（共 {len(tables)} 张）")

    ws = Workspace.init_workspace(
        ws_path,
        drama_name=args.name,
        feishu_app_token=app_token,
        feishu_tables=tables,
        feishu_url=args.url,
    )
    print(f"workspace 已创建: {ws.root}")

    # 绑定已有表格后，同样把项目路径等引导配置写回「系统设置」
    try:
        write_system_config(feishu, tables, ws.root, args.name)
    except Exception as e:
        print(f"  警告: 写入系统设置失败（不影响本地初始化）: {e}")

    ws.feishu = feishu
    ws.invalidate_cache()
    for pull_method, label in [
        ("pull_characters", "角色库"), ("pull_scenes", "场景库"),
        ("pull_settings", "剧本设定"), ("pull_storyboard", "剧本分镜表"),
        ("pull_episodes", "剧本表"), ("pull_character_bibles", "角色档案"),
    ]:
        try:
            data = getattr(feishu, pull_method)(ws)
            print(f"  已拉取 {label}: {len(data)} 条")
        except Exception as e:
            print(f"  拉取 {label} 失败: {e}")

    print(f"\n飞书表格: {args.url}")
    print(f"本地目录: {ws.root}")


def cmd_write(args):
    import json as _json
    from vomin.workspace import Workspace

    ws = resolve_workspace(args.workspace)
    table = args.table

    raw = args.data
    if raw.startswith("@"):
        with open(raw[1:], "r", encoding="utf-8") as f:
            data = _json.load(f)
    else:
        data = _json.loads(raw)

    if isinstance(data, dict):
        data = [data]

    match_keys = {
        "角色库": "name", "场景库": "name", "剧本设定": "name",
        "剧本分镜表": "shot_id", "生图工作台": "name", "素材库": "name",
        "剧本表": "episode", "角色档案": "name",
    }
    mk = match_keys.get(table)
    if not mk:
        print(f"不支持写入的表: {table}")
        sys.exit(1)

    json_files = {
        "角色库": "characters.json", "场景库": "scenes.json",
        "剧本设定": "settings.json", "剧本分镜表": "storyboard.json",
        "生图工作台": "workbench.json", "素材库": "assets.json",
        "剧本表": "episodes.json", "角色档案": "character_bibles.json",
    }
    json_file = json_files[table]
    existing = ws.load_json(json_file)
    def _row_key(r):
        # 场景库同一空间有母版/主场景/局部多行，主键是 name + view_angle
        if table == "场景库" and r.get(mk):
            return f"{r.get(mk)}·{r.get('view_angle') or '全景基准图（默认）'}"
        return r.get(mk)

    existing_map = {_row_key(r): r for r in existing if r.get(mk)}

    updated, created = 0, 0
    for row in data:
        if not row.get(mk):
            print(f"  跳过: 缺少 {mk} 字段")
            continue
        key = _row_key(row)
        if key in existing_map:
            existing_map[key].update(row)
            updated += 1
        else:
            existing.append(row)
            existing_map[key] = row
            created += 1

    ws.save_json(json_file, existing)
    print(f"[{table}] 新增 {created}, 更新 {updated}")

    if ws.feishu:
        push_methods = {
            "角色库": "push_characters", "场景库": "push_scenes",
            "剧本设定": "push_settings", "剧本分镜表": "push_storyboard",
            "剧本表": "push_episodes", "角色档案": "push_character_bibles",
        }
        push_method = push_methods.get(table)
        if push_method:
            try:
                getattr(ws.feishu, push_method)(ws)
                print(f"  已同步到飞书")
            except Exception as e:
                print(f"  飞书同步失败: {e}")


def cmd_read(args):
    import json as _json
    from vomin.workspace import Workspace

    ws = resolve_workspace(args.workspace)
    table = args.table

    loaders = {
        "角色库": ws.load_characters, "场景库": ws.load_scenes,
        "剧本设定": ws.load_settings, "剧本分镜表": ws.load_storyboard,
        "生图工作台": ws.load_workbench, "素材库": ws.load_assets,
        "剧本表": ws.load_episodes, "角色档案": ws.load_character_bibles,
    }
    loader = loaders.get(table)
    if not loader:
        print(f"不支持读取的表: {table}", file=sys.stderr)
        sys.exit(1)

    data = loader()

    # 按集数过滤（剧本表 / 剧本分镜表）：拆分镜时只读当前集 ± 相邻集，
    # 禁止一次性读入全部剧集原文，避免上下文膨胀
    if args.episode is not None and table in ("剧本表", "剧本分镜表"):
        def _ep_num(rec):
            try:
                return int(rec.get("episode"))
            except (TypeError, ValueError):
                return None

        context = max(int(args.context or 0), 0)
        lo, hi = args.episode - context, args.episode + context
        data = [r for r in data if (e := _ep_num(r)) is not None and lo <= e <= hi]
        data.sort(key=lambda r: int(r["episode"]))
        if context:
            print(f"[过滤] 第 {lo}~{hi} 集（实际 {len(data)} 条）", file=sys.stderr)
        else:
            print(f"[过滤] 仅第 {args.episode} 集（实际 {len(data)} 条）", file=sys.stderr)
    elif args.episode is not None:
        print(f"--episode/--context 仅支持剧本表、剧本分镜表，已忽略", file=sys.stderr)

    # 剧本表默认剔除小说原文：拆分镜/抽场景只需转化后的 script，读 N±1 三集小说原文会撑爆上下文
    if table == "剧本表" and not getattr(args, "with_novel", False):
        data = [{k: v for k, v in r.items() if k != "novel_text"} for r in data]

    print(_json.dumps(data, ensure_ascii=False, indent=2))


def cmd_expand(args):
    from vomin.workspace import Workspace
    ws = resolve_workspace(args.workspace)
    shots = ws.load_storyboard()

    global_prompt_raw = ws.get_global_prompt()
    global_refs = ws.get_global_ref_images()
    if global_prompt_raw or global_refs:
        print(f"[全局设定]")
        if global_prompt_raw:
            global_expanded, _, _, _, _ = ws.expand_prompt(global_prompt_raw)
            print(f"  全局提示词（原文）: {global_prompt_raw}")
            if global_expanded != global_prompt_raw:
                print(f"  全局提示词（展开）: {global_expanded}")
        if global_refs:
            print(f"  全局参考图: {', '.join(ws.rel(p) for p in global_refs)}")
        print()

    targets = shots
    if args.shot:
        targets = [s for s in shots if s["shot_id"] == args.shot]

    for s in targets:
        template = s.get("prompt", "")
        expanded, ref_imgs, chars, scenes, ref_vids = ws.expand_prompt(template)
        if global_prompt_raw:
            global_expanded, global_extra_refs, _, _, global_extra_vids = ws.expand_prompt(global_prompt_raw)
            full_prompt = f"{expanded}，{global_expanded}"
            ref_imgs = list(ref_imgs) + [r for r in global_extra_refs if r not in ref_imgs]
            ref_vids = list(ref_vids) + [r for r in global_extra_vids if r not in ref_vids]
        else:
            full_prompt = expanded
        all_refs = list(ref_imgs) + [g for g in global_refs if g not in ref_imgs]
        print(f"=== {s['shot_id']} ===")
        print(f"  模板:     {template}")
        print(f"  最终提示词: {full_prompt}")
        print(f"  角色:     {', '.join(chars) if chars else '(无)'}")
        print(f"  场景:     {', '.join(scenes) if scenes else '(无)'}")
        print(f"  参考图:   {', '.join(ws.rel(p) for p in all_refs) if all_refs else '(无)'}")
        print(f"  参考视频: {', '.join(ws.rel(p) for p in ref_vids) if ref_vids else '(无)'}")
        print()


def cmd_migrate_schema(args):
    """存量飞书表迁移：剧集表→剧本表，补小说章节/小说内容与场景库新字段。

    --dry-run 只读，打印计划；不带则执行写入（须先在对话里列清单并拿到用户确认）。
    """
    ws = resolve_workspace(args.workspace)
    if not ws.feishu:
        print("未配置飞书（缺少 app_token 或 FEISHU_APP_ID/SECRET 凭据），无法迁移")
        sys.exit(1)

    plan = ws.feishu.plan_schema_migration()

    print("[迁移计划]")
    if plan["rename"]:
        print(f"  1. 表改名: {plan['rename'][0]} → {plan['rename'][1]}")
    else:
        print("  1. 表改名: 无需（已是「剧本表」或不存在「剧集表」）")
    if plan["add_fields"]:
        for tname, fields in plan["add_fields"].items():
            print(f"  2. {tname} 新增字段: {', '.join(f['field_name'] for f in fields)}")
    else:
        print("  2. 新增字段: 无需")
    print(f"  3. 完整剧本 → 小说内容（并置状态「待转剧本」）: {plan['move_rows']} 行")
    print("  4. 本地 workspace.yaml: 将 feishu.tables 的「剧集表」键改为「剧本表」")

    if args.dry_run:
        print("\n--dry-run：以上为计划，未执行任何写入")
        return

    nothing = (not plan["rename"] and not plan["add_fields"] and plan["move_rows"] == 0)
    ws.feishu.apply_schema_migration(plan)

    tables_cfg = ws.config.get("feishu", {}).setdefault("tables", {})
    if "剧集表" in tables_cfg and "剧本表" not in tables_cfg:
        tables_cfg["剧本表"] = tables_cfg.pop("剧集表")
        ws.save_config()
        print("  已更新本地 workspace.yaml: 剧集表 → 剧本表")
    elif nothing:
        print("\n无需迁移，已是最新结构")
    ws.invalidate_cache()
    print("\n迁移完成")


def main():
    parser = argparse.ArgumentParser(description="Vomin Studio — AI 短剧制作流水线")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="初始化 workspace（创建新飞书表格）")
    p_init.add_argument("workspace", nargs="?", default=None,
                        help="workspace 目录路径；省略时默认为 项目根/workspace/{剧名}")
    p_init.add_argument("--name", default="demo短剧", help="剧名")

    p_init_url = sub.add_parser("init-from-url", help="从飞书链接初始化 workspace")
    p_init_url.add_argument("url", help="飞书多维表格 URL")
    p_init_url.add_argument("workspace", nargs="?", default=None,
                            help="workspace 目录路径；省略时默认为 项目根/workspace/{剧名}")
    p_init_url.add_argument("--name", default="新项目", help="剧名（建议显式传入，用作默认目录名）")

    p_status = sub.add_parser("status", help="查看状态和预算")
    p_status.add_argument("workspace", help="workspace 目录路径")

    p_gen = sub.add_parser("generate", help="生成素材（角色图/场景图/配音/视频）")
    p_gen.add_argument("workspace", help="workspace 目录路径")
    p_gen.add_argument("--target", help="指定生成目标，格式: 角色库:名 / 场景库:名 / 剧本分镜表:ID / 生图工作台:任务名或all")
    p_gen.add_argument("--tts-only", action="store_true", help="分镜只生成配音，不生成视频（省钱）")

    p_pre = sub.add_parser("preflight", help="生产态前置校验：分镜引用的资产是否真的就绪")
    p_pre.add_argument("workspace", help="workspace 目录路径")
    p_pre.add_argument("--episode", type=int, default=None, help="只校验指定集")
    p_push = sub.add_parser("push", help="回写状态到飞书")
    p_push.add_argument("workspace", help="workspace 目录路径")

    p_pull = sub.add_parser("pull", help="从飞书拉取分镜到本地")
    p_pull.add_argument("workspace", help="workspace 目录路径")

    p_wb = sub.add_parser("workbench", help="生图工作台：批量生成所有未完成任务")
    p_wb.add_argument("workspace", help="workspace 目录路径或飞书 URL")

    p_expand = sub.add_parser("expand", help="预览提示词模板展开结果")
    p_expand.add_argument("workspace", help="workspace 目录路径")
    p_expand.add_argument("--shot", help="只看指定镜头")

    p_write = sub.add_parser("write", help="写入数据到指定表（JSON upsert）")
    p_write.add_argument("workspace", help="workspace 目录路径")
    p_write.add_argument("--table", required=True, help="目标表名（角色库/角色档案/场景库/剧本设定/剧本分镜表/剧本表/生图工作台/素材库）")
    p_write.add_argument("--data", required=True, help="JSON 数据字符串，或 @文件路径")

    p_setpath = sub.add_parser("set-path", help="把当前本地 workspace 路径写回飞书系统设置")
    p_setpath.add_argument("workspace", help="workspace 本地目录路径")

    p_read = sub.add_parser("read", help="读取指定表数据并输出 JSON")
    p_read.add_argument("workspace", help="workspace 目录路径")
    p_read.add_argument("--table", required=True, help="表名（角色库/角色档案/场景库/剧本设定/剧本分镜表/剧本表/生图工作台/素材库）")
    p_read.add_argument("--episode", type=int, default=None,
                        help="仅剧本表/剧本分镜表：只读指定集（拆分镜时禁止无过滤读全量剧集）")
    p_read.add_argument("--context", type=int, default=0,
                        help="配合 --episode：连同前后各 N 集（拆分镜建议 --context 1）")
    p_read.add_argument("--with-novel", action="store_true",
                        help="仅剧本表：同时输出「小说内容」原文（默认剔除，避免撑爆上下文）")

    p_mig = sub.add_parser("migrate-schema",
                           help="存量飞书表迁移：剧集表→剧本表，补小说字段与场景库新字段")
    p_mig.add_argument("workspace", help="workspace 目录路径或飞书 URL")
    p_mig.add_argument("--dry-run", action="store_true", help="只读：打印迁移计划，不执行写入")

    args = parser.parse_args()
    {"init": cmd_init, "init-from-url": cmd_init_from_url,
     "status": cmd_status, "generate": cmd_generate, "preflight": cmd_preflight,
     "workbench": cmd_workbench,
     "push": cmd_push, "pull": cmd_pull, "expand": cmd_expand,
     "write": cmd_write, "read": cmd_read,
     "set-path": cmd_set_path, "migrate-schema": cmd_migrate_schema}[args.command](args)


if __name__ == "__main__":
    main()
