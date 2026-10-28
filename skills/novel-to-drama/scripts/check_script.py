#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""novel-to-drama 格式合同检查器（Step A 常规剧本 / Step B 切镜头版）。

只查“下游能不能稳定读取”和“有没有越界”，不评价戏好不好。

用法：
    # Step A 常规剧本
    python check_script.py drafts/ep01_script_plain.md --mode plain

    # Step B 切镜头版，并对照 Step A 检查台词有没有被改动
    python check_script.py drafts/ep01_script.md --mode cut --compare drafts/ep01_script_plain.md

    # 自动判断（出现「切镜头，」行 → cut）
    python check_script.py drafts/ep01_script.md

退出码：
    0  没有错误（--strict 下警告也算错误）
    1  有错误
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TIME_WORDS = ("黄昏", "傍晚", "清晨", "深夜", "白天", "晨", "夜", "日")

# 景别：从长到短匹配，避免「大特写」被「特写」先吃掉
SHOT_SIZES = (
    "超大远景", "大特写", "近特写", "贴地特写", "大远景", "中近景",
    "特写", "近景", "中景", "中全景", "全景", "远景", "大全景",
)
SHOT_SIZE_RE = re.compile("|".join(sorted(SHOT_SIZES, key=len, reverse=True)))

# Step A 里出现就是越界（Step B 才允许写镜头）
CAMERA_WORDS = (
    "景别", "近景", "中景", "全景", "特写", "机位", "运镜", "焦段",
    "分镜", "提示词", "资产库：", "剧本分镜表", "切镜头",
)

# Step B 里出现就是抢 B1 的活
CUT_FORBIDDEN = (
    (re.compile(r"\d{1,2}\s*[:：]\s*\d{2}"), "时间码（时间码归 B1 分镜）"),
    (re.compile(r"ep\d{1,2}_p\d{1,2}", re.I), "分镜段号（段号归 B1 分镜）"),
    (re.compile(r"[{｛]\s*资产库"), "资产锚点（锚点归 B1 资产绑定）"),
    (re.compile(r"\bR\d{2}"), "R 编号（编号归 B1 分镜）"),
    (re.compile(r"\d+\s*mm\b", re.I), "焦段数值"),
    (re.compile(r"光圈|快门速度|ISO\s*\d", re.I), "镜头参数（光圈/快门/ISO）"),
)

PRONOUNS = ("他", "她", "它", "他们", "她们")

# 下面三个正则只用于 --stats 的「参考」统计，不参与判定——运镜与动作速度都按需写。
SPEED_RE = re.compile(
    r"快|慢|猛|急|缓|顿|停住|停半|忽然|突然|瞬间|一下|匀速|渐渐|越来越|"
    r"用力|力道|力度|半秒|秒|轻轻|重重|颤|抖|绷|缩|蹭|甩|拖|滑|冲|撞|弹"
)

CAMERA_MOVE_RE = re.compile(
    r"轻推|缓推|前推|后拉|横移|平移|摇摄|下摇|上摇|甩镜|俯仰|抬镜|升降|"
    r"环绕|跟拍|跟摇|变焦|移焦|固定|收稳|手持|镜头"
)

# 有人在做动作，才统计动作速度；纯静物/纯空镜不算
ACTION_RE = re.compile(
    r"走|坐|站|抬|转|伸|抓|推|拉|敲|握|缩|低头|迈|掏|举|按|压|扯|扔|放|靠|凑|"
    r"退|起身|弯|脱|摆|蹭|滑|撞|震|抖|翻|关|开|戳|划|扫|摸|甩|拎|递|接|塞|捂|"
    r"掐|捏|晃|点头|摇头|转身"
)

DIALOGUE_RE = re.compile(r"^(.+?)（([^）]*)）：「(.+)」$")
DIALOGUE_NO_PAREN_RE = re.compile(r"^(.+?)：「(.+)」$")
SUBTITLE_RE = re.compile(r"^（字幕[^）]*）(.+)$")
SOUND_RE = re.compile(r"^（音效）(.+)$")
SHOT_RE = re.compile(r"^切镜头(?:\s*(\d+))?\s*[，,]\s*(.+)$")
LOCK_RE = re.compile(r"^强制一致\s*[:：]\s*(.+)$")
OPT_OUT = "（不入屏）"


@dataclass
class Issue:
    level: str  # "error" / "warn"
    line: int
    message: str


@dataclass
class Shot:
    line: int
    body: str
    size: str = ""
    subject: str = ""


@dataclass
class Scene:
    number: str
    kind: str
    location: str
    time: str
    line: int
    people: str = ""
    note: str = ""
    estimate: float | None = None
    actions: int = 0          # Step A 的 △ 行
    shots: list[Shot] = field(default_factory=list)
    dialogues: int = 0
    os_lines: int = 0
    subtitles: int = 0
    sounds: int = 0
    dialogue_chars: int = 0
    shot_chars: int = 0
    speakers: set[str] = field(default_factory=set)


@dataclass
class Report:
    path: Path
    mode: str = "plain"
    title: str = ""
    episode: str = ""
    episode_name: str = ""
    source_chapters: str = ""
    source_span: str = ""
    duration: float | None = None
    scene_count_hint: int | None = None
    shot_count_hint: int | None = None
    locks: list[tuple[str, str]] = field(default_factory=list)  # (对象, 必写短语)
    scenes: list[Scene] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    total_chars: int = 0
    ended: bool = False

    def error(self, line: int, message: str) -> None:
        self.issues.append(Issue("error", line, message))

    def warn(self, line: int, message: str) -> None:
        self.issues.append(Issue("warn", line, message))

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.level == "warn"]

    @property
    def total_shots(self) -> int:
        return sum(len(s.shots) for s in self.scenes)


def _is_body_line(stripped: str) -> bool:
    """镜头段落里的内容行：切镜头 / 台词 / 字幕 / 音效 / 本集完。"""
    if stripped.startswith("切镜头"):
        return True
    if stripped.startswith("（字幕") or stripped.startswith("（音效"):
        return True
    if stripped == "（本集完）":
        return True
    return "：「" in stripped


def _split_estimate(text: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)\s*秒", text)
    return float(m.group(1)) if m else None


def _split_scene_head(text: str) -> tuple[str, str, str, str] | None:
    """把 '1．外景　陈诚公寓走廊　日' 拆成 (场号, 内外景, 地点, 时间)。"""
    raw = text.strip()
    tokens = [t for t in re.split(r"[　\s]+", raw) if t]
    if len(tokens) < 3:
        return None
    head = tokens[0]
    m = re.match(r"^(\d+[A-Za-z]?)[．.](内景|外景|内外景)$", head)
    if not m:
        return None
    number, kind = m.group(1), m.group(2)
    time_token = tokens[-1]
    time_name = re.sub(r"（[^）]*）$", "", time_token).strip()
    if time_name not in TIME_WORDS:
        return None
    location = "　".join(tokens[1:-1]).strip()
    if not location:
        return None
    return number, kind, location, time_token


def detect_mode(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    for raw in text.splitlines():
        if "切镜头" in raw.strip():
            return "cut"
    return "plain"


def parse(path: Path, mode: str = "auto") -> Report:
    text = path.read_text(encoding="utf-8-sig")
    if mode == "auto":
        mode = detect_mode(path)
    lines = text.splitlines()
    report = Report(path=path, mode=mode)

    scene: Scene | None = None
    header_done = False
    last_content_type: str | None = None

    for idx, raw in enumerate(lines, start=1):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue

        report.total_chars += len(re.sub(r"\s+", "", stripped))

        # 场头
        head = _split_scene_head(stripped)
        if head:
            number, kind, location, time_token = head
            header_done = True
            scene = Scene(
                number=number, kind=kind, location=location,
                time=time_token, line=idx,
            )
            report.scenes.append(scene)
            last_content_type = "scene"
            if "·" in location:
                report.error(idx, f"场景名不能含「·」：{location}")
            continue

        # 切镜头版的排版：每行之间空一行，否则 Markdown 预览/飞书会并段
        if mode == "cut" and _is_body_line(stripped):
            prev_raw = lines[idx - 2] if idx >= 2 else ""
            if prev_raw.strip():
                report.error(
                    idx,
                    "这条内容和上一条之间没有空行；Markdown 预览、飞书里会并成一段，"
                    "看不出切镜。每行之间空一行",
                )

        # 抬头
        if not header_done and not report.scenes:
            if stripped.startswith("剧名："):
                report.title = stripped[len("剧名："):].strip()
                continue
            m = re.match(r"^第(\d+)集[　\s]+(.+)$", stripped)
            if m:
                report.episode = m.group(1)
                report.episode_name = m.group(2).strip()
                continue
            if stripped.startswith("对应原小说章节："):
                report.source_chapters = stripped[len("对应原小说章节："):].strip()
                continue
            if stripped.startswith("原文区间："):
                report.source_span = stripped[len("原文区间："):].strip()
                continue
            if stripped.startswith("预估时长："):
                value = stripped[len("预估时长："):].strip()
                report.duration = _split_estimate(value)
                m2 = re.search(r"｜\s*(\d+)\s*场", value)
                if m2:
                    report.scene_count_hint = int(m2.group(1))
                m3 = re.search(r"｜\s*(\d+)\s*镜", value)
                if m3:
                    report.shot_count_hint = int(m3.group(1))
                continue
            m4 = LOCK_RE.match(stripped)
            if m4:
                body = m4.group(1).strip()
                parts = re.split(r"[｜|]", body, maxsplit=1)
                if len(parts) != 2 or not parts[0].strip() or not parts[1].strip():
                    report.error(
                        idx,
                        "「强制一致」要写成「强制一致：对象｜每次入镜必写的短语」",
                    )
                else:
                    report.locks.append((parts[0].strip(), parts[1].strip()))
                continue
            report.error(idx, f"抬头里出现无法识别的一行：{stripped[:30]}")
            continue

        if scene is None:
            report.error(idx, f"场头之前出现正文：{stripped[:30]}")
            continue

        # 人物 / 备注 / 本场预估
        if stripped.startswith("人物："):
            scene.people = stripped[len("人物："):].strip()
            last_content_type = "people"
            continue
        if stripped.startswith("备注："):
            scene.note = stripped[len("备注："):].strip()
            last_content_type = "note"
            continue
        if stripped.startswith("本场预估："):
            scene.estimate = _split_estimate(stripped)
            last_content_type = "estimate"
            continue

        # 结尾
        if stripped == "（本集完）":
            report.ended = True
            last_content_type = "end"
            continue

        # 切镜头行形态：先查「是不是独立成行」
        if "切镜头" in stripped:
            if mode == "plain":
                report.error(
                    idx,
                    "这行属于 Step B（切镜头版），Step A 不许写镜头；把它留到切镜头版",
                )
                continue
            if not stripped.startswith("切镜头"):
                report.error(
                    idx,
                    "「切镜头」必须新起一行、顶格写在行首"
                    "（不要接在句末，也不要加 - / 1. / > 这类符号）",
                )
                continue
            if stripped.count("切镜头") > 1:
                report.error(idx, "一行只能写一个「切镜头」：新镜头请换行另起")
                continue

        # 切镜头行（Step B）
        m = SHOT_RE.match(stripped)
        if m:
            body = m.group(2).strip()
            size_m = SHOT_SIZE_RE.search(body)
            subject = ""
            size = ""
            if size_m:
                size = size_m.group(0)
                subject = body[: size_m.start()].strip("，,。；;：: ")
            shot = Shot(line=idx, body=body, size=size, subject=subject)
            scene.shots.append(shot)
            scene.shot_chars += len(re.sub(r"\s+", "", body))
            last_content_type = "shot"
            if not size:
                report.error(idx, f"镜头没写景别：{body[:24]}")
            if size and not subject:
                report.warn(idx, f"主体写在景别后面了；建议「切镜头，{size} + 名字 + 动作」：{body[:24]}")
            elif subject in PRONOUNS or any(subject.startswith(p) for p in PRONOUNS):
                report.error(idx, f"镜头主体用了代词「{subject}」，要写名字（下游靠名字绑资产）")
            if not body:
                report.error(idx, "空的镜头行")
            else:
                n = len(re.sub(r"\s+", "", body))
                if n < 12:
                    report.error(idx, f"镜头只有景别没有内容（{n} 字）：{body[:24]}")
                elif n < 18:
                    report.warn(idx, f"镜头偏薄（{n} 字），看看是不是漏了动作或环境")
                elif n > 170:
                    report.warn(idx, f"单镜 {n} 字偏长，考虑拆成两镜")
            for pat, label in CUT_FORBIDDEN:
                if pat.search(body):
                    report.error(idx, f"切镜头版不要写{label}：{body[:24]}")
            if any(p in body for p in PRONOUNS) and re.search(r"(?<!其)[他她它]", body):
                report.warn(idx, "镜头里出现代词（他/她/它），下游可能认错主体")
            # 强制一致项
            for obj, phrase in report.locks:
                if obj in body and phrase not in body:
                    if OPT_OUT in body:
                        report.warn(idx, f"「{obj}」入镜但没写「{phrase}」（已标不入屏）")
                    else:
                        report.error(
                            idx,
                            f"强制一致项缺失：「{obj}」入镜必须写「{phrase}」；"
                            f"确实拍不到写{OPT_OUT}",
                        )
            continue

        # Step A 的动作行
        if stripped.startswith("△"):
            if mode == "cut":
                report.error(idx, "切镜头版不写 △ 行，把动作写进「切镜头，…」")
                continue
            body = stripped[1:].strip()
            if not body:
                report.error(idx, "空的动作行（只有 △）")
            scene.actions += 1
            last_content_type = "action"
            for word in CAMERA_WORDS:
                if word in body:
                    report.warn(idx, f"动作行里出现镜头/越界词「{word}」；镜头交给 Step B")
                    break
            continue

        # 字幕
        m = SUBTITLE_RE.match(stripped)
        if m:
            if mode == "cut" and not scene.shots:
                report.warn(idx, "字幕出现在本场第一个镜头之前；确认它归属哪一镜")
            scene.subtitles += 1
            last_content_type = "subtitle"
            continue

        # 音效
        m = SOUND_RE.match(stripped)
        if m:
            scene.sounds += 1
            last_content_type = "sound"
            continue

        # 台词（带括号）
        m = DIALOGUE_RE.match(stripped)
        if m:
            speaker, how, body = m.group(1).strip(), m.group(2).strip(), m.group(3)
            scene.dialogues += 1
            scene.dialogue_chars += len(re.sub(r"\s+", "", body))
            is_os = "OS" in how.upper()
            if is_os:
                scene.os_lines += 1
                if last_content_type == "os":
                    report.warn(idx, "连续两句 OS 之间没有动作/画面/台词隔开，容易变成有声书")
                last_content_type = "os"
            else:
                last_content_type = "dialogue"
            if not speaker:
                report.error(idx, "台词缺少说话人")
            if speaker in PRONOUNS:
                report.error(idx, f"说话人不能写「{speaker}」，要写名字")
            if speaker:
                scene.speakers.add(speaker)
            if mode == "cut" and not scene.shots:
                report.warn(idx, "台词出现在本场第一个镜头之前；台词要落在发声的那一镜后面")
            continue

        # 台词（无括号）
        m = DIALOGUE_NO_PAREN_RE.match(stripped)
        if m:
            speaker, body = m.group(1).strip(), m.group(2)
            scene.dialogues += 1
            scene.dialogue_chars += len(re.sub(r"\s+", "", body))
            if not speaker:
                report.error(idx, "台词缺少说话人")
            if speaker in PRONOUNS:
                report.error(idx, f"说话人不能写「{speaker}」，要写名字")
            if speaker:
                scene.speakers.add(speaker)
            if mode == "cut" and not scene.shots:
                report.warn(idx, "台词出现在本场第一个镜头之前；台词要落在发声的那一镜后面")
            last_content_type = "dialogue"
            continue

        report.error(
            idx,
            "无法识别的一行（应为 切镜头/△动作 / 角色：「台词」 / （字幕）/（音效）/（本集完））："
            + stripped[:40],
        )

    return report


def validate(report: Report) -> None:
    if not report.title:
        report.error(0, "缺少「剧名：」")
    if not report.episode:
        report.error(0, "缺少「第N集　集名」")
    if not report.episode_name:
        report.error(0, "集名为空")
    elif not (4 <= len(report.episode_name) <= 14):
        report.warn(0, f"集名长度 {len(report.episode_name)} 字，建议 4~14 字")
    if not report.source_chapters:
        report.error(0, "缺少「对应原小说章节：」")
    elif not re.fullmatch(r"\d+(,\d+)*", report.source_chapters):
        report.error(0, f"「对应原小说章节」只能写纯数字、逗号分隔升序，当前：{report.source_chapters}")
    if report.source_span:
        if "→" not in report.source_span:
            report.error(0, "「原文区间」要写成「起始句 → 结束句」，中间有 →")
        elif report.source_chapters and re.fullmatch(r"\d+(,\d+)*", report.source_chapters):
            span_chs = set(re.findall(r"第(\d+)章", report.source_span))
            field_chs = {x.strip() for x in report.source_chapters.split(",") if x.strip()}
            missing = sorted(span_chs - field_chs)
            if missing:
                report.warn(0, f"「原文区间」里的章号 {','.join(missing)} 没出现在「对应原小说章节」里")
    elif report.source_chapters:
        report.warn(0, "有「对应原小说章节」但没写「原文区间」；建议补上本集起止句")
    if report.duration is None:
        report.error(0, "缺少「预估时长：约 N 秒」")
    elif not (60 <= report.duration <= 120):
        report.error(0, f"预估时长 {report.duration:g} 秒，不在 60~120 秒区间")
    if not report.scenes:
        report.error(0, "没有任何场次")
        return
    if report.scene_count_hint is not None and report.scene_count_hint != len(report.scenes):
        report.warn(0, f"抬头写 {report.scene_count_hint} 场，实际 {len(report.scenes)} 场")

    if report.mode == "cut":
        if report.locks:
            pass
        if report.shot_count_hint is None:
            report.warn(0, "切镜头版抬头建议写「｜N 镜」")
        elif report.shot_count_hint != report.total_shots:
            report.warn(
                0, f"抬头写 {report.shot_count_hint} 镜，实际 {report.total_shots} 镜"
            )
        if not report.locks:
            report.warn(0, "切镜头版没有「强制一致：」清单；确认真的没有要锁的道具细节")
    elif report.locks:
        report.warn(0, "「强制一致」只用于切镜头版；Step A 不需要")

    for scene in report.scenes:
        label = f"第 {scene.number} 场（{scene.location}）"
        if not scene.people:
            report.warn(scene.line, f"{label} 缺少「人物：」行")
        else:
            people = {p.strip() for p in re.split(r"[、，,]", scene.people) if p.strip()}
            for name in sorted(scene.speakers - people):
                report.warn(scene.line, f"{label} 的说话人「{name}」不在「人物：」行里")
        if report.mode == "plain":
            if scene.actions == 0:
                report.error(scene.line, f"{label} 没有 △ 动作行")
        else:
            if not scene.shots:
                report.error(scene.line, f"{label} 没有任何「切镜头，」")
        if scene.dialogues == 0 and scene.subtitles == 0 and scene.sounds == 0 and scene.shots == 0:
            report.warn(scene.line, f"{label} 没有台词/字幕/音效/镜头，确认是不是纯画面场")

    estimates = [s.estimate for s in report.scenes if s.estimate is not None]
    if estimates:
        total = sum(estimates)
        if report.duration is not None:
            tolerance = max(10.0, report.duration * 0.2)
            if abs(total - report.duration) > tolerance:
                report.warn(
                    0,
                    f"各场「本场预估」合计 {total:g} 秒，与抬头 {report.duration:g} 秒差得较多",
                )

    if not report.ended:
        report.warn(0, "缺少结尾「（本集完）」")


def _scene_signature(report: Report) -> list[tuple[str, str, str, str]]:
    return [(s.number, s.kind, s.location, s.time) for s in report.scenes]


def _dialogue_signature(report: Report, path: Path) -> list[tuple[str, str]]:
    from difflib import SequenceMatcher  # noqa: F401  (仅用于未来扩展)

    rows: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = DIALOGUE_RE.match(stripped)
        if m:
            rows.append((m.group(1).strip(), m.group(3).strip()))
            continue
        m = DIALOGUE_NO_PAREN_RE.match(stripped)
        if m:
            rows.append((m.group(1).strip(), m.group(2).strip()))
    return rows


def _subtitle_signature(path: Path) -> list[str]:
    rows: list[str] = []
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        m = SUBTITLE_RE.match(raw.strip())
        if m:
            rows.append(m.group(1).strip())
    return rows


def compare(main: Report, other_path: Path) -> list[Issue]:
    """比对 Step B 与 Step A：场头、台词、字幕必须一致。"""
    issues: list[Issue] = []
    other = parse(other_path, "auto")

    sig_a = _scene_signature(other)
    sig_b = _scene_signature(main)
    if sig_a != sig_b:
        issues.append(Issue(
            "error", 0,
            f"场头与 {other_path.name} 不一致：那份 {len(sig_a)} 场，这份 {len(sig_b)} 场；"
            "Step B 不许改场序/场数/地点/时间",
        ))
        for i, (a, b) in enumerate(zip(sig_a, sig_b), start=1):
            if a != b:
                issues.append(Issue("error", 0, f"第 {i} 场：{a} ≠ {b}"))

    dia_a = _dialogue_signature(other, other_path)
    dia_b = _dialogue_signature(main, main.path)
    if len(dia_a) != len(dia_b):
        issues.append(Issue(
            "error", 0,
            f"台词句数与 {other_path.name} 不一致：{len(dia_a)} → {len(dia_b)}；"
            "Step B 不许增删台词",
        ))
    for i, (a, b) in enumerate(zip(dia_a, dia_b), start=1):
        if a != b:
            issues.append(Issue(
                "error", 0,
                f"第 {i} 句台词被改动：「{a[0]}：{a[1][:20]}」→「{b[0]}：{b[1][:20]}」",
            ))

    sub_a = _subtitle_signature(other_path)
    sub_b = _subtitle_signature(main.path)
    if sub_a != sub_b:
        issues.append(Issue("error", 0, "字幕文本与 Step A 不一致（屏幕字是内容，不许改字）"))

    return issues


def print_report(report: Report, show_stats: bool) -> None:
    mode_label = "Step B 切镜头版" if report.mode == "cut" else "Step A 常规剧本"
    print(f"\n== 合同检查（{mode_label}）：{report.path}")
    print(
        f"   剧名：{report.title or '（缺）'}\n"
        f"   集号：{report.episode or '（缺）'}　集名：{report.episode_name or '（缺）'}\n"
        f"   对应章节：{report.source_chapters or '（缺）'}　预估："
        f"{report.duration if report.duration is not None else '（缺）'} 秒"
    )
    print(f"   原文区间：{report.source_span or '（缺）'}")
    if report.locks:
        print(f"   强制一致：{len(report.locks)} 条")
        for obj, phrase in report.locks:
            print(f"     - {obj}｜{phrase}")

    if report.errors:
        print(f"\n   错误 {len(report.errors)} 条：")
        for item in report.errors:
            where = f"第 {item.line} 行" if item.line else "抬头"
            print(f"   ✗ [{where}] {item.message}")
    if report.warnings:
        print(f"\n   警告 {len(report.warnings)} 条（--strict 下算错误）：")
        for item in report.warnings:
            where = f"第 {item.line} 行" if item.line else "全局"
            print(f"   ! [{where}] {item.message}")

    total_actions = sum(s.actions for s in report.scenes)
    total_dialogues = sum(s.dialogues for s in report.scenes)
    total_os = sum(s.os_lines for s in report.scenes)
    total_subs = sum(s.subtitles for s in report.scenes)
    total_sounds = sum(s.sounds for s in report.scenes)
    total_dialogue_chars = sum(s.dialogue_chars for s in report.scenes)

    if report.mode == "cut":
        print(
            f"\n   统计：{len(report.scenes)} 场｜{report.total_shots} 镜｜"
            f"{total_dialogues} 句台词（OS {total_os}）｜{total_subs} 条字幕｜"
            f"{total_sounds} 条音效｜台词 {total_dialogue_chars} 字｜全文 {report.total_chars} 字"
        )
        shots = [s for sc in report.scenes for s in sc.shots]
        if shots:
            cam = sum(1 for s in shots if CAMERA_MOVE_RE.search(s.body))
            act = [s.body for s in shots if ACTION_RE.search(s.body)]
            spd = sum(1 for b in act if SPEED_RE.search(b))
            print(
                f"   参考（按需，不判定）：有运镜说明 {cam}/{len(shots)} 镜｜"
                f"动作镜里带速度/力度 {spd}/{len(act)} 镜"
            )
    else:
        print(
            f"\n   统计：{len(report.scenes)} 场｜{total_actions} 条动作｜{total_dialogues} 句台词"
            f"（OS {total_os}）｜{total_subs} 条字幕｜{total_sounds} 条音效"
            f"｜台词 {total_dialogue_chars} 字｜全文 {report.total_chars} 字"
        )

    if show_stats:
        print("\n   逐场：")
        for s in report.scenes:
            if report.mode == "cut":
                avg = (s.shot_chars / len(s.shots)) if s.shots else 0
                print(
                    f"   {s.number:>3} {s.kind} {s.location} {s.time}"
                    f"｜人物：{s.people or '（缺）'}"
                    f"｜镜 {len(s.shots)}（均 {avg:.0f} 字）｜台词 {s.dialogues}（OS {s.os_lines}）"
                    f"｜字幕 {s.subtitles}｜预估 {s.estimate if s.estimate is not None else '—'}"
                )
            else:
                print(
                    f"   {s.number:>3} {s.kind} {s.location} {s.time}"
                    f"｜人物：{s.people or '（缺）'}"
                    f"｜动作 {s.actions}｜台词 {s.dialogues}（OS {s.os_lines}）"
                    f"｜字幕 {s.subtitles}｜预估 {s.estimate if s.estimate is not None else '—'}"
                )

    print(
        "\n   提醒：这只查格式合同，不查戏。格式过了，还要过 SKILL.md 的六问，并读一遍。"
    )


def print_compare(issues: list[Issue], other: Path) -> None:
    if not issues:
        print(f"\n== 与 {other.name} 对照：场头、台词、字幕一致 ✓")
        return
    print(f"\n== 与 {other.name} 对照：{len(issues)} 处不一致 ✗")
    for item in issues:
        print(f"   ✗ {item.message}")


def main() -> int:
    parser = argparse.ArgumentParser(description="novel-to-drama 格式合同检查器")
    parser.add_argument("script", type=Path, help="剧本文件路径（.md/.txt）")
    parser.add_argument(
        "--mode", choices=("auto", "plain", "cut"), default="auto",
        help="plain=Step A 常规剧本，cut=Step B 切镜头版，默认按内容自动判断",
    )
    parser.add_argument(
        "--compare", type=Path, default=None,
        help="Step B 对照的 Step A 文件：检查场头/台词/字幕有没有被改动",
    )
    parser.add_argument("--strict", action="store_true", help="把警告也当错误")
    parser.add_argument("--stats", action="store_true", help="打印逐场统计")
    args = parser.parse_args()

    if not args.script.exists():
        print(f"文件不存在：{args.script}", file=sys.stderr)
        return 1

    report = parse(args.script, args.mode)
    validate(report)

    cmp_issues: list[Issue] = []
    if args.compare:
        if not args.compare.exists():
            print(f"对照文件不存在：{args.compare}", file=sys.stderr)
            return 1
        if report.mode != "cut":
            print("--compare 只用于切镜头版（--mode cut）", file=sys.stderr)
            return 1
        cmp_issues = compare(report, args.compare)

    print_report(report, show_stats=args.stats)
    if args.compare:
        print_compare(cmp_issues, args.compare)

    failed = (
        bool(report.errors)
        or bool(cmp_issues)
        or (args.strict and bool(report.warnings))
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
