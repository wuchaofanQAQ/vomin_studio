#!/usr/bin/env python3
"""大厂标准分场景剧本格式校验 + 密度自检。

用法:
    python skills/novel-to-script/scripts/check_script.py <剧本.md> [--json]

退出码 0 = 全部通过，1 = 有硬性问题。

格式标准（详见 references/script-format.md）:
    剧名：XXX
    第N集　集名

    1．内景　地点　日
    人物：A、B
    备注：光线/色调（可选）
    △动作描述
    角色：台词
    （字幕）… / （字幕·微信，陈诚手机）… / （音效）… / （OS）
    （本集完）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED = [
    "特写", "大特写", "近景", "中景", "全景", "远景", "过肩",
    "鱼眼", "广角", "俯拍", "仰拍", "航拍", "平视机位", "机位",
    "淡入", "淡出", "叠化", "分屏", "镜头切换", "环绕运镜", "手持镜头",
]

SCENE_RE = re.compile(r"^(\d+)．(内景|外景)　([^　]+)　([^　]+?)(（闪回）)?$")
EP_RE = re.compile(r"^第(\d+)集　(.+)$")
SPEAKER_MAX = 10


def split_dialogue(ln: str, cast: set[str]):
    """把 `角色（提示）：台词` 拆成 (角色, 提示, 台词)；不是对白返回 None。

    不用正则：Python 3.15 的 re 在模式里出现「：（」时会误报 unbalanced parenthesis。
    """
    if ln.startswith("（") or "：" not in ln:
        return None
    head, tail = ln.split("：", 1)
    if "（" in head:
        speaker, _, hint = head.partition("（")
        speaker = speaker.strip()
        if speaker in cast:
            return speaker, hint.rstrip("）"), tail
        return None
    head = head.strip()
    if head in cast:
        return head, "", tail
    return None


def parse(text: str) -> dict:
    raw_lines = text.splitlines()
    lines = [ln.strip() for ln in raw_lines]
    s = {
        "chars": len(re.sub(r"\s", "", text)),
        "title": "", "episode": "", "scenes": [],
        "beats": 0, "dialogue": 0, "os": 0, "subtitles": 0,
        "sole_scenes": 0, "speakers": {},
        "errors": [], "banned_hits": [],
        "has_end": False,
    }

    # --- 抬头 ---
    idx = 0
    while idx < len(lines) and not lines[idx]:
        idx += 1
    if idx < len(lines) and lines[idx].startswith("剧名："):
        s["title"] = lines[idx].split("：", 1)[1].strip()
        idx += 1
    else:
        s["errors"].append("缺少「剧名：」抬头")
    while idx < len(lines) and not lines[idx]:
        idx += 1
    if idx < len(lines):
        m = EP_RE.match(lines[idx])
        if m:
            s["episode"] = m.group(1)
            idx += 1
        else:
            s["errors"].append("缺少「第N集　集名」抬头")
    else:
        s["errors"].append("缺少「第N集　集名」抬头")

    # --- 场次 ---
    cur = None
    for ln in lines[idx:]:
        if not ln:
            continue
        m = SCENE_RE.match(ln)
        if m:
            cur = {
                "no": int(m.group(1)), "shot": m.group(2), "place": m.group(3),
                "time": m.group(4), "flashback": bool(m.group(5)),
                "cast": [], "note": "", "body": [],
            }
            s["scenes"].append(cur)
            continue
        if ln.startswith("场") and "｜" in ln:
            s["errors"].append(f"旧格式场头：{ln[:30]}")
            continue
        if cur is None:
            s["errors"].append(f"场头之前出现正文：{ln[:30]}")
            continue
        if ln.startswith("人物："):
            raw = ln.split("：", 1)[1]
            cur["cast"] = [x.strip() for x in re.split(r"[、,，]", raw) if x.strip()]
            continue
        if ln.startswith("备注："):
            cur["note"] = ln.split("：", 1)[1]
            continue
        if ln.startswith("【注】"):
            cur["body"].append(ln)
            continue
        if ln.startswith("出场人物："):
            s["errors"].append(f"旧格式「出场人物：」：{ln[:30]}")
            continue
        if ln == "（本集完）":
            s["has_end"] = True
            continue
        cur["body"].append(ln)

    if not s["has_end"]:
        s["errors"].append("缺少「（本集完）」收尾")

    # --- 正文 ---
    for sc in s["scenes"]:
        cast = set(sc["cast"])
        if not sc["cast"]:
            s["errors"].append(f"场{sc['no']} 缺「人物：」行")
        sc_dialogue = 0
        for ln in sc["body"]:
            if ln.startswith("【注】"):
                continue
            if ln.startswith("（字幕"):
                s["subtitles"] += 1
                s["beats"] += 1
                continue
            if ln.startswith("（音效）"):
                s["beats"] += 1
                continue
            if "（OS）" in ln:
                parts = split_dialogue(ln, cast | {ln.split("（")[0].strip()})
                if not parts:
                    s["errors"].append(f"场{sc['no']} OS 行格式不对：{ln[:30]}")
                else:
                    s["speakers"][parts[0]] = s["speakers"].get(parts[0], 0) + 1
                s["os"] += 1
                s["beats"] += 1
                continue
            if ln.startswith("△"):
                s["beats"] += 1
                continue
            parts = split_dialogue(ln, cast)
            if parts:
                s["dialogue"] += 1
                s["beats"] += 1
                sc_dialogue += 1
                s["speakers"][parts[0]] = s["speakers"].get(parts[0], 0) + 1
                continue
            if "：" in ln:
                s["errors"].append(f"场{sc['no']} 未加 △ 的动作行或说话人不在人物表：{ln[:36]}")
            else:
                s["errors"].append(f"场{sc['no']} 未加 △ 的行：{ln[:36]}")
        if len(sc["cast"]) <= 1 and sc_dialogue == 0 and sc["body"]:
            s["sole_scenes"] += 1

    for word in BANNED:
        for i, ln in enumerate(lines, 1):
            if word in ln:
                s["banned_hits"].append({"word": word, "line": i, "text": ln[:50]})
    return s


def evaluate(s: dict) -> list[tuple[str, bool, str]]:
    voice_units = s["dialogue"] + s["os"] + s["subtitles"]
    return [
        ("格式错误 = 0", not s["errors"], f"{len(s['errors'])} 处"),
        ("字数 1500~2500", 1500 <= s["chars"] <= 2500, f"{s['chars']}"),
        ("场数 5~8", 5 <= len(s["scenes"]) <= 8, f"{len(s['scenes'])}"),
        ("可拆节拍 ≥40", s["beats"] >= 40, f"{s['beats']}"),
        ("台词 8~30", 8 <= s["dialogue"] <= 30, f"{s['dialogue']}"),
        ("台词+OS+字幕 ≥12", voice_units >= 12, f"{voice_units}"),
        ("OS ≤5", s["os"] <= 5, f"{s['os']}"),
        ("字幕 1~10", 1 <= s["subtitles"] <= 10, f"{s['subtitles']}"),
        ("单人无对白场 ≤1", s["sole_scenes"] <= 1, f"{s['sole_scenes']}"),
        ("无镜头语言", not s["banned_hits"], f"{len(s['banned_hits'])} 处"),
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    s = parse(Path(args.path).read_text(encoding="utf-8"))
    checks = evaluate(s)
    ok = all(c[1] for c in checks)

    if args.json:
        print(json.dumps({"stats": s, "checks": [
            {"name": c[0], "ok": c[1], "value": c[2]} for c in checks], "ok": ok},
            ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print(f"文件: {Path(args.path).name}  《{s['title']}》第{s['episode']}集")
    print(f"字数 {s['chars']} / 场 {len(s['scenes'])} / 节拍 {s['beats']} / "
          f"台词 {s['dialogue']} / OS {s['os']} / 字幕 {s['subtitles']} / 单人场 {s['sole_scenes']}")
    for name, passed, val in checks:
        print(f"  {'✓' if passed else '✗'} {name}  ({val})")
    if s["errors"]:
        for e in s["errors"]:
            print(f"    ! {e}")
    if s["banned_hits"]:
        for hit in s["banned_hits"]:
            print(f"    禁词「{hit['word']}」第{hit['line']}行: {hit['text']}")
    print("出场人物台词分布:", s["speakers"] or "无")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
