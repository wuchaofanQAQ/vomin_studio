#!/usr/bin/env python3
"""剧本资产提取 · 输出校验（只产描述：不产提示词 / 空间锚点 / 角色档案）。

用法:
    python check_assets.py <assets.json> [--max-desc 50] [--json]

退出码 0 = 全部通过，1 = 有硬性问题。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CHAR_TYPES = {"核心", "重要配角", "配角", "龙套", "群像"}
PROP_TYPES = {"关键信物", "手持道具", "陈设道具", "食物饮品",
              "服装配饰", "武器工具", "电子设备", "其他"}
BANNED = ["8K", "8k", "4K", "4k", "超清", "高清", "史诗", "震撼", "极致", "大片"]
FORBIDDEN_KEYS = ("prompt", "gen_prompt", "bible", "voice_desc", "anchors")


def norm_name(s: str) -> str:
    """名字归一：去空白、半角括号统一成全角、英文小写，用于跨次幂等比对。"""
    n = re.sub(r"\s+", "", s or "")
    n = n.replace("(", "（").replace(")", "）")
    return n.lower()


def load_library(path: str) -> dict[str, set[str]]:
    """读 workspace 里的三张资产表缓存，返回 {type: {归一化名字}}。"""
    lib = {"角色": set(), "场景": set(), "道具": set()}
    if not path:
        return lib
    base = Path(path)
    for kind, fname in (("角色", "characters.json"), ("场景", "scenes.json"), ("道具", "props.json")):
        fp = base / fname
        if not fp.exists():
            continue
        try:
            rows = json.loads(fp.read_text(encoding="utf-8-sig"))
        except Exception:
            continue
        for r in rows:
            if r.get("name"):
                lib[kind].add(norm_name(r["name"]))
    return lib


def clen(s: str) -> int:
    return len(re.sub(r"\s", "", s or ""))


def check_desc(s: str, who: str, limit: int, errors: list[str]):
    if not (s or "").strip():
        errors.append(f"{who} 缺描述")
        return
    if "\n" in (s or "").strip():
        errors.append(f"{who} 描述含换行（应一句）")
    if "【" in s or "】" in s:
        errors.append(f"{who} 描述含【】分节（只写一句描述）")
    if "空间锚点" in s:
        errors.append(f"{who} 描述里不要写空间锚点")
    for w in BANNED:
        if w in s:
            errors.append(f"{who} 描述含堆叠质量词「{w}」")
    n = clen(s)
    if n > limit:
        errors.append(f"{who} 描述 {n} 字 > {limit} 字：{s[:20]}…")


def check(doc: dict, limit: int, lib: dict[str, set[str]] | None = None) -> tuple[list[tuple[str, bool, str]], list[str]]:
    errors: list[str] = []
    chars = doc.get("characters") or []
    scenes = doc.get("scenes") or []
    props = doc.get("props") or []
    reused = doc.get("reused") or []
    missing = doc.get("missing") or []
    lib = lib or {"角色": set(), "场景": set(), "道具": set()}

    for label, rows in (("角色", chars), ("场景", scenes), ("道具", props)):
        names = [norm_name(r.get("name", "")) for r in rows]
        dup = {n for n in names if n and names.count(n) > 1}
        for n in sorted(dup):
            errors.append(f"{label}「{n}」重复出现")
        for r in rows:
            name = (r.get("name") or "").strip()
            if not name:
                errors.append(f"{label}有条目缺 name")
                continue
            who = f"{label}【{name}】"
            for k in FORBIDDEN_KEYS:
                if r.get(k):
                    errors.append(f"{who} 不应产出 {k}（本 skill 只写描述）")
            status = r.get("status")
            if status not in ("新建", "复用"):
                errors.append(f"{who} status 必须是 新建/复用，当前 {status!r}")
            key = norm_name(name)
            if status == "复用":
                if key not in lib[label]:
                    errors.append(f"{who} 标了复用，但库里没有同名资产")
                continue
            if key in lib[label]:
                errors.append(f"{who} 库里已有同名资产（多次提取会重复插入）；标复用或改名区分")

            if label == "角色":
                check_desc(r.get("appearance", ""), who, limit, errors)
                ct = r.get("char_type")
                if ct and ct not in CHAR_TYPES:
                    errors.append(f"{who} char_type 非法：{ct}")
            elif label == "场景":
                check_desc(r.get("description", ""), who, limit, errors)
                if "·" in name:
                    errors.append(f"{who} 场景名含「·」（会被当分隔符）")
            else:
                check_desc(r.get("description", ""), who, limit, errors)
                pt = r.get("prop_type")
                if pt and pt not in PROP_TYPES:
                    errors.append(f"{who} 道具类型非法：{pt}")

    for i, r in enumerate(reused, 1):
        if not (r.get("name") or "").strip():
            errors.append(f"reused 第{i}条缺 name")
        if not (r.get("reason") or "").strip():
            errors.append(f"reused 第{i}条缺 reason")
    for i, r in enumerate(missing, 1):
        if not (r.get("name") or "").strip():
            errors.append(f"missing 第{i}条缺 name")
        if not (r.get("reason") or "").strip():
            errors.append(f"missing 第{i}条缺 reason")

    rows = [r for r in (chars + scenes + props) if r.get("status") != "复用"]
    longest = max([clen(r.get("appearance") or r.get("description") or "") for r in rows] or [0])
    checks = [
        ("字段/重复/字数错误 = 0", not errors, f"{len(errors)} 处"),
        ("角色 / 场景 / 道具", True, f"{len(chars)} / {len(scenes)} / {len(props)}"),
        (f"描述 ≤ {limit} 字", longest <= limit, f"最长 {longest} 字"),
    ]
    return checks, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--max-desc", type=int, default=50)
    ap.add_argument("--library", default="", help="workspace 目录（含 characters.json / scenes.json / props.json），用于幂等检查")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    doc = json.loads(Path(args.path).read_text(encoding="utf-8-sig"))
    if isinstance(doc, dict) and "assets" in doc and isinstance(doc["assets"], dict):
        doc = doc["assets"]
    lib = load_library(args.library)
    checks, errors = check(doc, args.max_desc, lib)
    ok = all(c[1] for c in checks)

    if args.json:
        print(json.dumps({
            "checks": [{"name": c[0], "ok": c[1], "value": c[2]} for c in checks],
            "errors": errors, "ok": ok,
        }, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print(f"文件: {Path(args.path).name}")
    for name, passed, val in checks:
        print(f"  {'✓' if passed else '✗'} {name}  ({val})")
    for e in errors[:40]:
        print(f"    ! {e}")
    if len(errors) > 40:
        print(f"    … 另有 {len(errors) - 40} 条")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
