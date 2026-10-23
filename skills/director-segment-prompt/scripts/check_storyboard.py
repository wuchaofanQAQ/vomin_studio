#!/usr/bin/env python3
"""分镜（Seedance 分段提示词）自检：时间码、对白、禁词、锚点、资产一致性。

用法:
    python skills/director-segment-prompt/scripts/check_storyboard.py <分镜.md> [--json]

退出码 0 = 全部通过，1 = 有硬性问题。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Seedance 2.5 禁用情绪词（画面描写里不得出现）
BANNED = [
    "微笑", "笑容", "愤怒", "生气", "悲伤", "犹豫", "轻蔑", "紧张", "恐惧", "惊讶",
    "疑惑", "不屑", "欣慰", "失落", "痛苦", "得意", "尴尬", "满足", "疲惫", "期待",
    "失望", "警惕", "放松", "困惑", "厌恶", "心疼", "委屈", "开心",
]

# 身体部位词：出现时必须先写清是谁的【资产名】
BODY_WORDS = [
    "半张脸", "脸", "下巴", "颈侧", "颈部", "锁骨", "鼻尖", "鼻梁", "睫毛", "眉心",
    "眼睑", "眼窝", "喉结", "嘴唇", "指尖", "手指", "拇指", "食指", "手背", "掌心",
    "手腕", "肩线", "胸口", "脚趾", "脚背", "光脚", "后脑", "头发", "刘海",
]

# 负向指令词：正式提示词只写应出现的画面（台词不检查，剧本自带的否定词原样保留）
NEGATIVE_CMD = ["不要", "禁止", "切勿", "严禁", "避免", "不得", "勿"]
MAX_SEG_CHARS = 12000

T = r"([\d.]+)"
SEG_RE = re.compile(r"^##\s*第(\d+)段\s*[｜|]?\s*(.*)$")
DUR_RE = re.compile(r"本段总时长\s*([\d.]+)\s*秒\s*时间范围\s*" + T + r"\s*-\s*" + T + r"s")
SHOT_RE = re.compile(r"^【镜头(\d+)｜" + T + r"-" + T + r"s｜(.+)】")
DLG_RE = re.compile(r"^【对白\s*" + T + r"-" + T + r"s】(.+?)：(.*)$")
SUB_RE = re.compile(r"^【字幕\s*" + T + r"-" + T + r"s】")
ASSET_RE = re.compile(r"【([^【】]+)】")


def to_sec(value: str) -> float:
    return float(value)


def on_grid(t: float) -> bool:
    """时间码必须是 0.5 秒的整数倍。"""
    return abs(t * 2 - round(t * 2)) < 1e-6


def fmt(t: float) -> str:
    return f"{t:g}s"


def cn_len(s: str) -> int:
    return len(re.sub(r"[^\u4e00-\u9fff]", "", s))


def parse(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines()]
    segs: list[dict] = []
    cur = None
    cur_shot = None
    in_assets = False
    in_anchor = False

    for ln in lines:
        if not ln:
            continue

        if cur is not None and not ln.startswith("## ") and ln != "---":
            cur["chars"] += len(re.sub(r"\s", "", ln))

        m = SEG_RE.match(ln)
        if m:
            cur = {"no": int(m.group(1)), "title": m.group(2).strip(),
                   "dur": None, "start": None, "end": None,
                   "shots": [], "assets": [], "anchor_braces": 0,
                   "dialogue": [], "subs": 0, "chars": 0}
            cur_shot = None
            in_assets = in_anchor = in_scene = False
            segs.append(cur)
            continue
        if ln.startswith("## ") or ln == "---":
            cur = None
            cur_shot = None
            continue
        if cur is None:
            continue

        m = DUR_RE.search(ln)
        if m:
            cur["dur"] = float(m.group(1))
            cur["start"] = to_sec(m.group(2))
            cur["end"] = to_sec(m.group(3))
            continue

        if ln == "【参考素材锚点】":
            in_anchor, in_assets, in_scene = True, False, False
            continue
        if ln == "【本段资产锁定】":
            in_assets, in_anchor, in_scene = True, False, False
            continue
        if ln == "【本段现场生成】":
            in_scene, in_anchor, in_assets = True, False, False
            continue
        if ln in ("【本段整体基准】", "【本段初始空间】", "【本段终态】"):
            in_anchor = in_assets = in_scene = False
            if ln == "【本段终态】":
                cur_shot = None
            continue

        if in_scene:
            for name in ASSET_RE.findall(ln):
                cur.setdefault("scene_assets", []).append(name)
            if "图" in ln and not ASSET_RE.search(ln):
                cur["scene_loose"] = cur.get("scene_loose", 0) + 1
            continue

        if in_anchor:
            cur["anchor_braces"] += ln.count("{")
            if "{" in ln and ("}" not in ln or "图" not in ln.split("}", 1)[-1]):
                cur["bad_anchor"] = cur.get("bad_anchor", 0) + 1
            for token in re.findall(r"\{([^}]*)\}", ln):
                if "【" in token or "】" in token:
                    cur["nested_bracket"] = cur.get("nested_bracket", 0) + 1
            for name in ASSET_RE.findall(ln):
                cur.setdefault("anchor_assets", []).append(name)
            continue
        if in_assets:
            for name in ASSET_RE.findall(ln):
                cur["assets"].append(name)
            continue

        m = SHOT_RE.match(ln)
        if m:
            s = {"no": int(m.group(1)), "start": to_sec(m.group(2)),
                 "end": to_sec(m.group(3)), "title": m.group(4), "body": []}
            cur["shots"].append(s)
            cur_shot = s
            continue

        m = DLG_RE.match(ln)
        if m:
            cur["dialogue"].append({
                "start": to_sec(m.group(1)),
                "end": to_sec(m.group(2)),
                "speaker": m.group(3).strip(),
                "text": m.group(4),
                "shot": cur_shot["no"] if cur_shot else None,
            })
            continue
        if SUB_RE.match(ln):
            cur["subs"] += 1
            continue
        if cur_shot is not None:
            cur_shot["body"].append(ln)

    return {"segments": segs}


def evaluate(doc: dict) -> tuple[list[tuple[str, bool, str]], list[str]]:
    errors: list[str] = []
    segs = doc["segments"]
    total = 0.0

    for s in segs:
        if s["dur"] is None or s["start"] is None:
            errors.append(f"第{s['no']:02d}段 缺「本段总时长/时间范围」")
            continue
        if abs(s["start"]) > 1e-6:
            errors.append(f"第{s['no']:02d}段 起始时间不是 00:00.00")
        if abs(s["end"] - s["dur"]) > 0.01:
            errors.append(f"第{s['no']:02d}段 时间范围终点 {fmt(s['end'])} ≠ 时长 {s['dur']}s")
        if s["dur"] > 30:
            errors.append(f"第{s['no']:02d}段 超过 30 秒上限")
        total += s["dur"]

        if not s["shots"]:
            errors.append(f"第{s['no']:02d}段 没有镜头")
            continue

        prev = s["start"]
        for sh in s["shots"]:
            if abs(sh["start"] - prev) > 0.011:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 起点 {fmt(sh['start'])} 与上一镜终点 {fmt(prev)} 不连续")
            if sh["end"] <= sh["start"]:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 起止时间非法")
            prev = sh["end"]
        if abs(prev - s["end"]) > 0.011:
            errors.append(f"第{s['no']:02d}段 末镜终点 {fmt(prev)} ≠ 本段终点 {fmt(s['end'])}")

        # 对白落在镜头窗口内 + 语速
        shot_map = {sh["no"]: sh for sh in s["shots"]}
        for d in s["dialogue"]:
            sh = shot_map.get(d["shot"])
            if not sh:
                errors.append(f"第{s['no']:02d}段 对白未挂在任何镜头下：{d['text'][:12]}")
                continue
            if d["start"] < sh["start"] - 0.011 or d["end"] > sh["end"] + 0.011:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 对白窗口超出镜头窗口")
            dur = d["end"] - d["start"]
            n = cn_len(d["text"])
            if dur > 0 and n / dur > 5.35:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 语速 {n / dur:.1f} 字/秒 > 5.3：{d['text'][:14]}")
            if dur <= 0:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 对白时长非正")

        # 时间码必须落在 0.5 秒格上
        if not on_grid(s["dur"]):
            errors.append(f"第{s['no']:02d}段 时长 {fmt(s['dur'])} 不在 0.5 秒格上")
        for sh in s["shots"]:
            if not (on_grid(sh["start"]) and on_grid(sh["end"])):
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 时间码不在 0.5 秒格上："
                              f"{fmt(sh['start'])}-{fmt(sh['end'])}")
        for d in s["dialogue"]:
            if not (on_grid(d["start"]) and on_grid(d["end"])):
                errors.append(f"第{s['no']:02d}段 对白时间码不在 0.5 秒格上：{d['text'][:12]}")

        # 镜头编号必须从 01 连续
        nums = [sh["no"] for sh in s["shots"]]
        if nums != list(range(1, len(nums) + 1)):
            errors.append(f"第{s['no']:02d}段 镜头编号不是从 01 连续：{nums}")

        if s["chars"] > MAX_SEG_CHARS:
            errors.append(f"第{s['no']:02d}段 全文 {s['chars']} 字（去空白）> {MAX_SEG_CHARS}，请精简或拆段")

        # 禁止省略写法（每段独立输入）
        seg_text = "".join("".join(sh["body"]) for sh in s["shots"])
        for w in ("同上", "接上段", "保持之前", "如前述", "同前", "承接上段"):
            if w in seg_text:
                errors.append(f"第{s['no']:02d}段 出现省略写法「{w}」，每段必须独立重建")

        # 禁词（只查画面描写，不查对白）
        for sh in s["shots"]:
            body = "".join(sh["body"])
            for w in BANNED:
                if w in body:
                    errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 出现禁用情绪词「{w}」")
            # 身体部位必须写清是谁的（在原始句子上判断，保留【】）
            for clause in re.split(r"[；。]", body):
                if not clause.strip():
                    continue
                idx = min((clause.find(w) for w in BODY_WORDS if w in clause), default=-1)
                if idx >= 0 and "【" not in clause[:idx]:
                    errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 身体部位没写归属："
                                  f"…{clause.strip()[:16]}…，请写成【资产名】的…")
                    break
            for w in NEGATIVE_CMD:
                if w in body:
                    errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 出现负向指令词「{w}」："
                                  f"请改写成应出现的画面（正向表达）")
                    break
            if "后期贴字" in body:
                errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 出现「后期贴字」："
                              f"屏幕文字属于画面内容，必须写进正文由模型生成")
            bare = re.sub(r"【[^】]*】", "", body)
            bare = re.sub(r"「[^」]*」", "", bare)  # 引号内是屏幕文字/原话，不算叙述代词
            for label, pat in (("她", r"(?<!其)她"), ("他", r"(?<!其)他"), ("自己", r"自己")):
                mm = re.search(pat, bare)
                if mm:
                    ctx = bare[max(0, mm.start() - 6):mm.start() + 4]
                    errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 正文出现代词「{label}」：…{ctx}…，请改用【资产名】")

        # 资产一致性
        lock = set(s["assets"])
        for sh in s["shots"]:
            for name in ASSET_RE.findall("".join(sh["body"])):
                if name not in lock:
                    errors.append(f"第{s['no']:02d}段 镜头{sh['no']:02d} 用了未锁定的资产【{name}】")
        # 锚点里的花括号闭合
        if s.get("bad_anchor"):
            errors.append(f"第{s['no']:02d}段 锚点块有未闭合的 {{}} 或缺「图N：」说明")
        if s.get("nested_bracket"):
            errors.append(f"第{s['no']:02d}段 锚点 {{表：行}} 内出现【】，行标识会解析失败")

        anchor_assets = set(s.get("anchor_assets", []))
        if anchor_assets != lock:
            missing = lock - anchor_assets
            extra = anchor_assets - lock
            if missing:
                errors.append(f"第{s['no']:02d}段 锚点块缺资产：{'、'.join(sorted(missing))}")
            if extra:
                errors.append(f"第{s['no']:02d}段 锚点块有未锁定的资产：{'、'.join(sorted(extra))}")

        scene_assets = set(s.get("scene_assets", []))
        bad_scene = scene_assets - lock
        if bad_scene:
            errors.append(f"第{s['no']:02d}段 现场生成引用了未锁定资产：{'、'.join(sorted(bad_scene))}")
        if s.get("scene_loose"):
            errors.append(f"第{s['no']:02d}段 现场生成提到「图」但没写【资产名】（如“走廊图”）")
        # 锚点资产名与锁定名一致
        # （锚点块内 {表：行} 后的【名】应出现在锁定表）

    # 台词全片只出现一次
    seen: dict[str, int] = {}
    for s in segs:
        for d in s["dialogue"]:
            t = d["text"].strip()
            if t and t in seen:
                errors.append(f"台词重复出现：{t[:16]}（第{seen[t]}段与第{s['no']}段）")
            elif t:
                seen[t] = s["no"]

    checks = [
        ("格式/时间/对白错误 = 0", not errors, f"{len(errors)} 处"),
        ("段数 ≥1", len(segs) >= 1, f"{len(segs)} 段"),
        ("总时长 ≤ 180 秒", total <= 180, f"{total:.0f} 秒"),
        ("每段 ≤ 30 秒", all((s["dur"] or 0) <= 30 for s in segs), "ok"),
        (f"每段 ≤ {MAX_SEG_CHARS} 字", all(s["chars"] <= MAX_SEG_CHARS for s in segs),
         f"最长 {max((s['chars'] for s in segs), default=0)} 字"),
    ]
    return checks, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    doc = parse(Path(args.path).read_text(encoding="utf-8"))
    checks, errors = evaluate(doc)
    ok = all(c[1] for c in checks)

    if args.json:
        print(json.dumps({"checks": [{"name": c[0], "ok": c[1], "value": c[2]} for c in checks],
                          "errors": errors, "ok": ok}, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    total_shots = sum(len(s["shots"]) for s in doc["segments"])
    print(f"文件: {Path(args.path).name}  段数 {len(doc['segments'])}  镜头数 {total_shots}")
    for name, passed, val in checks:
        print(f"  {'✓' if passed else '✗'} {name}  ({val})")
    for e in errors[:40]:
        print(f"    ! {e}")
    if len(errors) > 40:
        print(f"    … 另有 {len(errors) - 40} 条")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
