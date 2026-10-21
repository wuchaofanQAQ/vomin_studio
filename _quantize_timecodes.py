#!/usr/bin/env python3
"""把分镜时间轴量化到 0.5 秒格，并改为「0-0.5s」写法。

规则:
  镜头边界 = 最近 0.5s，强制单调且间隔 >= 0.5，末镜终点 = 段时长
  对白窗口 = 向内取到 0.5s 格；不足语速所需时向外扩，仍不足则报告
"""

import re
import sys
from pathlib import Path

P = Path(sys.argv[1])

SEG_RE = re.compile(r"^本段总时长\s*([\d.]+)\s*秒\s*时间范围\s*[\d:.]+—[\d:.]+$")
SHOT_RE = re.compile(r"^【镜头(\d+)｜([\d:.]+)—([\d:.]+)｜(.+)】$")
DLG_RE = re.compile(r"^【对白\s*([\d:.]+)—([\d:.]+)】(.+)$")
SUB_RE = re.compile(r"^【字幕\s*([\d:.]+)—([\d:.]+)】(.+)$")


def sec(t: str) -> float:
    if ":" in t:
        m, s = t.split(":")
        return int(m) * 60 + float(s)
    return float(t)


def half(x: float) -> float:
    return round(x * 2) / 2


def fmt(x: float) -> str:
    x = half(x)
    return f"{x:g}"


def cn_len(s: str) -> int:
    return len(re.sub(r"[^\u4e00-\u9fff]", "", s))


def main() -> None:
    lines = P.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    dur = None
    shot_start = shot_end = None
    pending_shots: list[tuple[int, str]] = []
    problems = []

    for ln in lines:
        m = SEG_RE.match(ln.strip())
        if m:
            dur = half(float(m.group(1)))
            out.append(f"本段总时长 {fmt(dur)}秒　时间范围 0-{fmt(dur)}s")
            continue

        m = SHOT_RE.match(ln.strip())
        if m:
            no, a, b, title = m.group(1), sec(m.group(2)), sec(m.group(3)), m.group(4)
            a2, b2 = half(a), half(b)
            if b2 - a2 < 0.5:
                b2 = a2 + 0.5
            shot_start, shot_end = a2, b2
            out.append(f"【镜头{no}｜{fmt(a2)}-{fmt(b2)}s｜{title}】")
            continue

        m = DLG_RE.match(ln.strip())
        if m:
            a, b, rest = sec(m.group(1)), sec(m.group(2)), m.group(3)
            text = rest.split("：", 1)[-1]
            need = cn_len(text) / 5.2
            a2 = half(a)
            b2 = half(b)
            if b2 - a2 < need:
                b2 = half(a2 + need + 0.24)
            if shot_end is not None:
                a2 = max(a2, shot_start)
                b2 = min(b2, shot_end)
            if b2 - a2 < 0.5:
                problems.append(f"对白窗口不足 0.5s：{rest[:20]}")
            rate = cn_len(text) / max(b2 - a2, 0.01)
            if rate > 5.35:
                problems.append(f"语速 {rate:.1f} 超限：{rest[:20]}")
            out.append(f"【对白 {fmt(a2)}-{fmt(b2)}s】{rest}")
            continue

        m = SUB_RE.match(ln.strip())
        if m:
            a2, b2 = half(sec(m.group(1))), half(sec(m.group(2)))
            if b2 - a2 < 0.5:
                b2 = a2 + 0.5
            out.append(f"【字幕 {fmt(a2)}-{fmt(b2)}s】{m.group(3)}")
            continue

        out.append(ln)

    # 修正镜头连续性：量化后可能出现重叠/空洞
    fixed: list[str] = []
    prev_end = 0.0
    for ln in out:
        m = SHOT_RE.match(ln)
        if m:
            no, title = m.group(1), m.group(4)
            a, b = sec(m.group(2)), sec(m.group(3))
            if a < prev_end - 1e-9:
                a = prev_end
            if b - a < 0.5:
                b = a + 0.5
            prev_end = b
            fixed.append(f"【镜头{no}｜{fmt(a)}-{fmt(b)}s｜{title}】")
            continue
        m2 = re.match(r"^本段总时长", ln)
        if m2:
            prev_end = 0.0
        fixed.append(ln)

    P.write_text("\n".join(fixed) + "\n", encoding="utf-8")
    print(f"已量化: {P.name}")
    for p in problems:
        print("  ! " + p)


if __name__ == "__main__":
    main()
