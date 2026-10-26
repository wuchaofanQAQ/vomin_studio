#!/usr/bin/env python3
"""资产生图 · 提示词构建与校验。

用法:
    python asset_prompt.py build --type 角色|场景|道具 --desc "18岁清瘦男生..."
    python asset_prompt.py check --library <workspace 目录> [--json]

check 会读 characters.json / scenes.json / props.json，逐行核对：
有描述、有 gen_prompt、版式关键词齐全、提示词带入了描述。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEMPLATES = {
    "角色": (
        "角色四视角设定图，同一角色，四格布局：画面上三分之一，左侧为人物近景正视图，"
        "右侧为人物近景侧视图；画面下三分之二，左侧为人物全身正视图，右侧为人物全身背视图。"
        "浅净背景，画面内无任何文字。真人电影级写实质感，保留真实皮肤纹理与自然光影；"
        "四视角为同一人，五官、发型、服装、体型完全一致。\n角色外观：{desc}"
    ),
    "场景": (
        "场景四视角资料图，同一空间：画面左侧至中部为大幅场景正视图，占画面 70% 以上；"
        "画面右侧 30% 区域从上到下依次排布同一空间的前、后、左、右四个机位视角的小图。"
        "主次清晰，电影级光影设计，真实，细腻，画面干净高质感，无人，画面内无任何文字。\n场景：{desc}"
    ),
    "道具": (
        "道具双视角图，画面中只有这一件道具，没有人物、没有手、没有其它物品。左侧为道具的正偏侧视角，"
        "能看清体积与厚度；右侧为正面视角，与左侧同一件道具、同一比例。"
        "背景为{bg}，画面内无任何文字。电影级写实质感，{wear}。\n道具：{desc}"
    ),
}

RATIO = {"角色": "16:9", "场景": "22:9", "道具": "16:9"}
ALIAS = {"角色": "角色", "character": "角色", "R": "角色", "r": "角色",
         "场景": "场景", "scene": "场景", "S": "场景", "s": "场景",
         "道具": "道具", "prop": "道具", "P": "道具", "p": "道具"}

CHECKS = {
    "角色": {"key": "appearance", "markers": ["近景正视图", "近景侧视图", "全身正视图", "全身背视图", "浅净背景", "无任何文字"]},
    "场景": {"key": "description", "markers": ["70%", "前、后、左、右", "无任何文字"]},
    "道具": {"key": "description", "markers": ["正偏侧", "正面视角", "无任何文字"]},
}

FILES = {"角色": "characters.json", "场景": "scenes.json", "道具": "props.json"}


# 浅色道具词表：命中则用纯绿幕，否则纯白（白底会把浅色道具吃掉）
LIGHT_TOKENS = ("白色", "米白", "奶白", "乳白", "象牙", "浅色", "浅灰", "浅蓝", "浅粉",
                "浅黄", "浅绿", "银", "透明", "玻璃", "雪白", "淡", "发光")


WEAR_RE = re.compile(r"(?<!无)(?<!没有)(磨损|划痕|旧|破|锈|脏|陈旧|裂|掉漆|褪色)")


DARK_STRIP = ("深灰玻璃", "深灰", "深色", "深蓝", "黑色", "磨砂玻璃", "玻璃背板",
              "玻璃反光", "黑", "暗")


def pick_background(desc: str) -> str:
    """深色系道具即使提到「玻璃/灰」也用纯白；只有真正浅色/透明的才用绿幕。"""
    d = desc
    for w in DARK_STRIP:
        d = d.replace(w, "")
    return "纯绿幕背景" if any(tok in d for tok in LIGHT_TOKENS) else "纯白背景"


def pick_wear(desc: str) -> str:
    """描述里写了磨损/旧化才保留痕迹，否则默认光洁无划痕。"""
    if WEAR_RE.search(desc):
        return "保留描述中的使用痕迹与磨损"
    return "表面光洁，无划痕、无破损，材质细节清晰"


def build(kind: str, desc: str) -> str:
    desc = desc.strip()
    if kind == "道具":
        return TEMPLATES["道具"].format(desc=desc, bg=pick_background(desc), wear=pick_wear(desc))
    return TEMPLATES[kind].format(desc=desc)


def check_row(kind: str, row: dict) -> list[str]:
    name = row.get("name", "?")
    who = f"{kind}【{name}】"
    errs = []
    desc = (row.get(CHECKS[kind]["key"]) or "").strip()
    prompt = (row.get("gen_prompt") or "").strip()
    if not desc:
        errs.append(f"{who} 缺描述（先跑 script-asset-extraction）")
    if not prompt:
        errs.append(f"{who} 缺 gen_prompt（先跑 asset_prompt.py build）")
        return errs
    for m in CHECKS[kind]["markers"]:
        if m not in prompt:
            errs.append(f"{who} 提示词缺版式要素「{m}」")
    if kind == "道具":
        has_green = "纯绿幕背景" in prompt
        has_white = "纯白背景" in prompt
        if has_green and has_white:
            errs.append(f"{who} 背景只能二选一，提示词里同时出现绿幕和白底")
        elif not has_green and not has_white:
            errs.append(f"{who} 道具提示词缺「纯绿幕背景」或「纯白背景」")
        else:
            want = pick_background(desc)
            if (want == "纯绿幕背景") != has_green:
                errs.append(f"{who} 背景选错：浅色道具必须纯绿幕，其余用纯白（当前应为{want}）")
    if desc and desc not in prompt:
        errs.append(f"{who} 提示词没有带入资产描述（描述可能改了，重新 build）")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build")
    b.add_argument("--type", required=True)
    b.add_argument("--desc", required=True)

    c = sub.add_parser("check")
    c.add_argument("--library", required=True)
    c.add_argument("--json", action="store_true")

    args = ap.parse_args()

    if args.cmd == "build":
        kind = ALIAS.get(args.type.strip())
        if not kind:
            print(f"未知类型: {args.type}（角色/场景/道具）", file=sys.stderr)
            return 1
        if not args.desc.strip():
            print("描述不能为空", file=sys.stderr)
            return 1
        print(build(kind, args.desc))
        return 0

    base = Path(args.library)
    errors: list[str] = []
    counts = {}
    for kind, fname in FILES.items():
        fp = base / fname
        rows = []
        if fp.exists():
            try:
                rows = json.loads(fp.read_text(encoding="utf-8-sig"))
            except Exception as e:
                errors.append(f"{fname} 读取失败：{e}")
        counts[kind] = len(rows)
        for row in rows:
            if row.get("status") == "复用":
                continue
            errors.extend(check_row(kind, row))

    ok = not errors
    if args.json:
        print(json.dumps({"ok": ok, "counts": counts, "errors": errors}, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print(f"库: {base}")
    for kind in ("角色", "场景", "道具"):
        print(f"  {kind}: {counts.get(kind, 0)} 行（复用行跳过）")
    if errors:
        print(f"\n✗ {len(errors)} 处：")
        for e in errors[:40]:
            print(f"  - {e}")
        if len(errors) > 40:
            print(f"  … 另有 {len(errors) - 40} 条")
        return 1
    print("\n✓ 所有 gen_prompt 都符合版式")
    return 0


if __name__ == "__main__":
    sys.exit(main())
