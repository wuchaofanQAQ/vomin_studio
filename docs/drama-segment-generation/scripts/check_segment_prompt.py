#!/usr/bin/env python3
"""剧本转提示词 4.2（名称版）分段提示词校验。

格式约定：
    段头  ## 【第01段｜[0s-30s]｜标题】
    锁定  【陈诚】画面参考：{角色库：陈诚}，声音参考：{音色库：陈诚}
          【沈幼怡】：{角色库：沈幼怡}
    镜头  【镜头01｜[0s-2s]｜标题】
    台词  [10s-12s]，【陈诚】（压着嗓子说）：「……」

用法:
    python check_segment_prompt.py <分镜.md> [--target 30] [--json]

退出码 0 = 全部通过，1 = 有硬性问题。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEG_RE = re.compile(r"^(?:##\s*)?【第(\d+)段｜\[0s-([\d.]+)s\]｜(.+?)】\s*$")
SHOT_RE = re.compile(r"^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\s*$")
DLG_RE = re.compile(r"^\[([\d.]+)s-([\d.]+)s\]，(.+?)：(.+)$")
LOCK_RE = re.compile(r"^【([^】]+)】\s*(?:画面参考\s*[:：])?\s*[:：]?\s*\{([^：}]+)[:：]([^}]+)\}")
VOICE_RE = re.compile(r"声音参考\s*[:：]\s*\{([^：}]+)[:：]([^}]+)\}")
MAP_RE = re.compile(r"^【参考图映射】(.+)$")
LOCK_RE2 = re.compile(r"^图\s*(\d+)\s*=\s*【([^】]+)】\s*=?\s*\{([^：}]+)[:：]([^}]+)\}")
MAP_ITEM_RE = re.compile(r"图(\d+)=【([^】]+)】")
BODY_ASSET_RE = re.compile(r"【([^】]+)】")

SHOT_SIZE = ["大特写", "特写", "中近景", "近景", "中远景", "中景", "全景", "远景", "空镜", "广角"]
CAMERA = ["固定机位", "推进", "推近", "拉远", "后拉", "横移", "平移", "升降", "跟拍",
          "跟摇", "环绕", "焦点转移", "上摇", "下摇", "摇镜", "俯拍", "仰拍", "航拍", "手持",
          "机位", "过肩", "主观", "反打", "贴地", "低机位", "高机位",
          "门内", "门外", "室内", "窗外", "视角", "机位侧", "前推", "缓推", "后拉", "下压", "跟移",
          "眼平齐", "齐高", "侧前方", "侧后方", "贴屏幕", "贴近", "平视"]
STOP = ["停", "落幅", "切", "收", "离画", "黑场", "压黑", "定住", "结束"]
BANNED = ["史诗", "震撼", "极致", "炸裂", "燃爆", "封神", "天花板"]
OMIT = ["同上", "接上段", "延续上一段", "保持之前", "如前述", "同前", "承接上段"]

# 运镜条件冲突与模糊写法（判据见 references/camera-movement-and-lens.md 第 5、10 节）
PUSH_WORDS = ["推近", "推进", "前推", "缓推", "轻推"]
SIZE_LOCK = ["大小不变", "大小保持", "保持人物大小", "主体大小不变", "保持景别", "景别不变",
             "维持景别", "取景范围不变", "构图不变"]
ORBIT_WORDS = ["环绕", "绕行", "绕弧"]
ORBIT_LOCK = ["朝向固定", "朝向不变", "朝向锁定", "机位朝向固定", "镜头朝向不变"]
FOCUS_WORDS = ["移焦", "焦点转移", "跟焦"]
FOCUS_LOCK = ["都清晰", "均清晰", "两者都清晰", "双方都清晰", "两人都清晰"]
TRACK_WORDS = ["跟拍", "跟摇", "跟随", "伴飞"]
TRACK_LOCK = ["越跟越近", "距离不断缩短", "持续逼近", "距离逐渐缩短", "越来越近"]
AMBIG_SIZE = ["近一点", "远一点", "大一点", "小一点", "放大一点", "再近些"]
# 台词括号里的内心状态：演不出来、听不出来，必须改成可听的气息/语速/音量
INNER_STATE = ["心里", "心想", "暗想", "脑海里", "琢磨", "暗自"]
# 镜头正文里的比喻/推断词：小说写法，不是可拍指令
SIMILE = ["像", "似的", "仿佛", "如同", "宛如"]
SIMILE_SAFE = ["影像", "图像", "画像", "像素", "镜像", "录像", "想象", "像样", "人像",
               "摄像头", "头像", "成像", "像差"]
# 画外方向词：只写"画外"等于没说方向
DIR_WORDS = ["画左", "画右", "画上", "画下", "上方", "下方", "左方", "右方",
             "身后", "面前", "头顶", "正前", "眼前"]
GAZE_WORDS = ["视线", "目光", "眼神", "看向", "望向", "盯着", "落向", "别开"]
# 发声证据词：参数式与自然语两种写法都认
VOICE_HINTS = ["音量", "声量", "声音", "声线", "轻声", "低声", "压着声", "压到最低", "压低", "拔高",
               "语速", "逐字", "一句", "一顿", "停", "顿", "尾音", "尾字", "尾句", "末字",
               "落重", "落稳", "落平", "平落", "平直", "砸下", "收住", "收死", "拖", "上挑", "轻挑", "一声", "先升后砸", "短促", "甩出", "挤出", "火气", "牙缝",
               "往下压", "断掉", "切断"]
IMG_TABLES = {"场景库", "角色库", "道具库", "素材库", "资产库"}
MAX_CHARS = 12000
SEG_MAX = 30
TOTAL_MAX = 180


def fmt(t: float) -> str:
    return f"{t:g}s"


def cn_len(s: str) -> int:
    return len(re.sub(r"[^\u4e00-\u9fff]", "", s))


def block_len(line: str) -> int:
    s = line.split("】", 1)[-1] if line.startswith("【") else line
    return len(re.sub(r"\s", "", s))


def parse(text: str) -> list[dict]:
    segs: list[dict] = []
    cur = None
    shot = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = SEG_RE.match(line)
        if m:
            cur = {"no": int(m.group(1)), "dur": float(m.group(2)), "title": m.group(3),
                   "shots": [], "lock": [], "map": [], "sections": set(), "block": "",
                   "live": "", "style": "", "space": "", "final": "", "in_lock": False,
                   "dlg_errors": [], "issues": []}
            segs.append(cur)
            shot = None
            continue
        if cur is None:
            continue
        m = SHOT_RE.match(line)
        if m:
            shot = {"no": int(m.group(1)), "start": float(m.group(2)), "end": float(m.group(3)),
                    "title": m.group(4), "body": "", "dlg": []}
            cur["shots"].append(shot)
            cur["block"] = ""
            continue
        m = DLG_RE.match(line)
        if m and shot is not None:
            shot["dlg"].append({"start": float(m.group(1)), "end": float(m.group(2)),
                                 "who": m.group(3).strip(), "text": m.group(4).strip()})
            continue
        if line.startswith("【本段资产锁定】"):
            cur["in_lock"] = True
            cur["sections"].add("lock")
            cur["block"] = "lock"
            continue
        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")
            cur["block"] = "live"
            cur["live"] = line
            continue
        if line.startswith("【本段整体基准】"):
            cur["in_lock"] = False
            cur["sections"].add("base")
            cur["block"] = "style"
            cur["style"] = line
            continue
        if line.startswith("【本段初始空间】"):
            cur["in_lock"] = False
            cur["sections"].add("space")
            cur["block"] = "space"
            cur["space"] = line
            continue
        if line.startswith("【本段终态】"):
            cur["in_lock"] = False
            cur["sections"].add("final")
            cur["block"] = "final"
            cur["final"] = line
            continue
        m = MAP_RE.match(line)
        if m:
            cur["map"] = [{"n": int(a), "name": b} for a, b in MAP_ITEM_RE.findall(m.group(1))]
            continue
        blk = cur.get("block")
        if blk == "lock":
            # 待补资产：没有参考图，但仍是本段合法资产名
            m = re.match(r"^待补：【([^】]+)】", line)
            if not m:
                m = re.match(r"^待出图：【([^】]+)】", line)
            if m:
                cur["lock"].append({"name": m.group(1), "table": "待补", "row": "", "voice": None})
                continue
            if line.strip().endswith("："):
                continue  # 类型分组标题（角色：/场景：/道具：）
            m2 = LOCK_RE2.match(line)
            m = LOCK_RE.match(line)
            if m2:
                name, table, row = m2.group(2).strip(), m2.group(3).strip(), m2.group(4).strip()
            elif m:
                name, table, row = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
            if m2 or m:
                voice = None
                vm = VOICE_RE.search(line)
                if vm:
                    voice = vm.group(2).strip()
                cur["lock"].append({"name": name, "table": table, "row": row, "voice": voice})
            continue
        if blk in ("live", "style", "space", "final"):
            cur[blk] = cur.get(blk, "") + "\n" + line
            continue
        if shot is not None:
            shot["body"] += line
    return segs


args_total_holder = [TOTAL_MAX]


def check(segs: list[dict], target: float) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    if not segs:
        return ["没有解析到任何段（段头应为 【第01段｜[0s-30s]｜标题】）"], notes

    total = 0.0
    for s in segs:
        tag = f"第{s['no']:02d}段"
        need = [("lock", "本段资产锁定"), ("live", "本段现场生成"), ("base", "本段整体基准"),
                ("space", "本段初始空间"), ("final", "本段终态")]
        for key, name in need:
            if key not in s["sections"]:
                errors.append(f"{tag} 缺【{name}】")
        if not s["lock"]:
            errors.append(f"{tag} 资产锁定为空")
        if not s["shots"]:
            errors.append(f"{tag} 没有镜头")

        # 时间轴
        prev = 0.0
        for sh in s["shots"]:
            if abs(sh["start"] - prev) > 1e-6:
                errors.append(f"{tag} 镜头{sh['no']:02d} 起点 {fmt(sh['start'])} ≠ 上一镜终点 {fmt(prev)}")
            if sh["end"] <= sh["start"]:
                errors.append(f"{tag} 镜头{sh['no']:02d} 时长 ≤0")
            prev = sh["end"]
        if s["shots"] and abs(prev - s["dur"]) > 1e-6:
            errors.append(f"{tag} 末镜终点 {fmt(prev)} ≠ 段长 {fmt(s['dur'])}")
        if s["dur"] > target + 1e-6:
            errors.append(f"{tag} 段长 {fmt(s['dur'])} > 上限 {fmt(target)}")
        total += s["dur"]

        # 资产
        names = [e["name"] for e in s["lock"]]
        if len(names) != len(set(names)):
            errors.append(f"{tag} 资产锁定有重名")
        img_locked = [e["name"] for e in s["lock"] if e["table"] in IMG_TABLES]
        map_names = [m["name"] for m in s["map"]]
        if map_names and map_names != img_locked:
            errors.append(f"{tag} 参考图映射 {map_names} 与锁定带图资产 {img_locked} 不一致")
        if map_names and [m["n"] for m in s["map"]] != list(range(1, len(map_names) + 1)):
            errors.append(f"{tag} 参考图映射编号不连续")

        lock_set = set(names)
        used = set()
        for nm in BODY_ASSET_RE.findall(s["style"] + s["space"] + s["final"] + s["live"]):
            if nm in lock_set:
                used.add(nm)
        for sh in s["shots"]:
            for nm in BODY_ASSET_RE.findall(sh["body"]):
                if nm in ("待补", "画外音", "待出图"):
                    continue
                if nm not in lock_set:
                    errors.append(f"{tag} 镜头{sh['no']:02d} 引用了锁定区没有的资产【{nm}】")
                else:
                    used.add(nm)
            for d in sh["dlg"]:
                if "画外" in d["who"] or "画外" in d["text"]:
                    continue  # 画外声只有声音，不需要参考图
                who = d["who"].replace("画外音", "").strip()
                m2 = BODY_ASSET_RE.search(who)
                if m2:
                    if m2.group(1) not in lock_set:
                        errors.append(f"{tag} 台词说话人【{m2.group(1)}】不在锁定区")
                    else:
                        used.add(m2.group(1))
                else:
                    errors.append(f"{tag} 台词说话人未用【】括起：{who}")
        for nm in img_locked:
            if nm not in used:
                notes.append(f"{tag} 锁定资产【{nm}】在正文里没出现")
        for nm in names:
            if nm not in used:
                notes.append(f"{tag} 锁定了【{nm}】但正文没用")

        # 裸名检查（长名优先，避免 陈诚 / 陈诚公寓玄关 互相误报）
        masked = BODY_ASSET_RE.sub("§", s["style"] + s["live"] + s["space"] + s["final"]
                                  + "".join(sh["body"] for sh in s["shots"]))
        masked = re.sub(r"「[^」]*」", "§", masked)  # 引号内是台词/屏幕文字，不是资产引用
        masked = re.sub(r"（字幕[^）]*）[^\n]*", "§", masked)  # 字幕行同样是画面内容，不是资产引用
        for nm in sorted(names, key=len, reverse=True):
            if nm in masked:
                # 【】只用于「引用锁定的那张参考图」；泛指同类物件（自己的手机/桌上的杯子）不该加【】
                notes.append(f"{tag} 正文提到「{nm}」但没加【】（若指锁定资产应写【{nm}】）")
                masked = masked.replace(nm, "§")

        # 台词
        for sh in s["shots"]:
            for d in sh["dlg"]:
                dur = d["end"] - d["start"]
                if dur <= 0 or d["start"] < sh["start"] - 1e-6 or d["end"] > sh["end"] + 1e-6:
                    errors.append(f"{tag} 镜头{sh['no']:02d} 台词窗口 [{fmt(d['start'])}-{fmt(d['end'])}] 不在镜头内")
                txt = d["text"]
                if not (txt.startswith("「") and txt.endswith("」")):
                    errors.append(f"{tag} 台词未用「」括起：{txt[:14]}")
                rate = cn_len(txt) / dur if dur > 0 else 999
                if rate > 5.3:
                    errors.append(f"{tag} 台词语速 {rate:.1f} 字/秒 > 5.3：{txt[:14]}")
                for w in INNER_STATE:
                    if w in d["who"]:
                        errors.append(f"{tag} 镜头{sh['no']:02d} 台词括号写了内心状态「{w}」："
                                      f"改成可听的气息/语速/音量（如「倒吸一口气、语速发紧地说」），"
                                      f"或说话人在画内时可见的动作")
                        break
                if "画外" in d["who"] and not any(w in d["who"] for w in DIR_WORDS):
                    notes.append(f"{tag} 镜头{sh['no']:02d} 台词括号只写「画外」没给方向："
                                 f"补画左/画右/画外上/画外下（如「压向画左画外」）")
                # 发声方式：括号里至少要能读出音量/语速/停顿/尾音中的两项
                who = d["who"]
                hits = sum(1 for w in VOICE_HINTS if w in who)
                if hits < 1:
                    notes.append(f"{tag} 镜头{sh['no']:02d} 台词括号缺发声方式：先写状态/动作，"
                                 f"再写声音与语流（音量、语速、停顿、尾音至少落到一项）")
                pm = re.search(r"（([^（）]*)）", who)
                if pm and len(re.sub(r"\s", "", pm.group(1))) > 16:
                    notes.append(f"{tag} 镜头{sh['no']:02d} 台词括号 {len(pm.group(1))} 字偏长："
                                 f"压到 8~13 字（如「突然开口，声音清晰而沉稳」）")

        # 时码格式：项目统一用 [X.Xs]，别混用 00:00.00
        for sh in s["shots"]:
            if re.search(r"\b0?0:\d{2}\.\d{2}", sh["body"]):
                notes.append(f"{tag} 镜头{sh['no']:02d} 用了 00:MM.SS 时码：改成 [X.Xs]，与镜头头统一")
                break

        # 丢台词防线：对白戏整段没有台词行，多半是漏了
        if not any(sh["dlg"] for sh in s["shots"]):
            notes.append(f"{tag} 本段没有任何台词行：确认不是漏了（脚本查不出「少台词」）")

        # 可见性：近景/特写里不得写画外资产（除非带位置词）
        LAYER = ["前景", "中景", "后景", "画左", "画右", "画面", "入画", "反射", "影子", "虚化", "画外"]
        for sh in s["shots"]:
            body_ = sh["body"]
            size = next((x for x in SHOT_SIZE if x in body_[:40]), "")
            if size not in ("近景", "中近景", "特写", "大特写"):
                continue
            found = BODY_ASSET_RE.findall(body_)
            if not found:
                continue
            subj = found[0]
            tbl = {e["name"]: e["table"] for e in s["lock"]}
            for nm in dict.fromkeys(found):
                if tbl.get(nm) != "角色库":
                    continue
                if nm == subj:
                    continue
                for m in re.finditer("【" + re.escape(nm) + "】", body_):
                    ctx = body_[max(0, m.start() - 18):m.end() + 12]
                    if not any(w in ctx for w in LAYER):
                        errors.append(f"{tag} 镜头{sh['no']:02d} {size}里写了画外资产【{nm}】，"
                                      f"应改写成画面方向（画左/画右/画外）或补位置词")

        # 镜头写法
        for sh in s["shots"]:
            body = sh["body"]
            head = body[:110]
            if not any(k in head for k in SHOT_SIZE):
                errors.append(f"{tag} 镜头{sh['no']:02d} 起笔 80 字内没写景别")
            if not any(k in head for k in CAMERA):
                errors.append(f"{tag} 镜头{sh['no']:02d} 起笔 80 字内没写机位/运镜（固定机位也算）")
            # 切点不强制：参考稿里 98% 的镜头不写切点，靠下一镜的「硬切」承接。
            # 只有运镜镜头才要求给出落幅。
            if any(k in body for k in ("推近", "拉远", "横移", "摇", "环绕", "跟移")) and not any(
                    k in body[-50:] for k in ("到位", "收稳", "停住", "落幅", "让开", "停")):
                notes.append(f"{tag} 镜头{sh['no']:02d} 有运镜但没写落幅：补「收稳/到位/停住」")

        # 运镜条件冲突：同镜里两个要求互相抵消
        for sh in s["shots"]:
            vis = re.sub(r"「[^」]*」", "§", sh["body"])
            pairs = [
                (PUSH_WORDS, SIZE_LOCK, "推近/前推的同时要求主体大小或景别不变"),
                (ORBIT_WORDS, ORBIT_LOCK, "环绕的同时锁死机位朝向"),
                (FOCUS_WORDS, FOCUS_LOCK, "移焦的同时要求两个主体都清晰"),
                (TRACK_WORDS, TRACK_LOCK, "跟拍的同时要求距离不断缩短"),
            ]
            for words, locks, msg in pairs:
                if any(w in vis for w in words) and any(w in vis for w in locks):
                    errors.append(f"{tag} 镜头{sh['no']:02d} 运镜条件打架：{msg}"
                                  f"（改法见 camera-movement-and-lens.md 第 10 节）")
            for w in AMBIG_SIZE:
                if w in vis:
                    notes.append(f"{tag} 镜头{sh['no']:02d} 出现模糊景别词「{w}」，"
                                 f"改用画面边界（腰部以上/胸部以上/面部特写）")
            sim = vis
            for safe in SIMILE_SAFE:
                sim = sim.replace(safe, "")
            for w in SIMILE:
                if w in sim:
                    notes.append(f"{tag} 镜头{sh['no']:02d} 正文出现比喻/推断词「{w}」："
                                 f"改写成可拍的物理动作（如「脚步轻得像只猫」→「脚掌先落地、脚跟再慢慢压下」）")
                    break
            for m in re.finditer("画外", vis):
                ctx = vis[max(0, m.start() - 10):m.end() + 10]
                if any(g in ctx for g in GAZE_WORDS) and not any(w in ctx for w in DIR_WORDS):
                    notes.append(f"{tag} 镜头{sh['no']:02d} 视线指向「画外」却没给方向："
                                 f"补画左/画右/画外上/画外下，并与【本段初始空间】的轴线一致")
                    break

        # 密度
        rules = [("整体基准", s["style"], 150), ("初始空间", s["space"], 90), ("终态", s["final"], 40)]
        for name, txt, need in rules:
            if block_len(txt) < need:
                errors.append(f"{tag} 【本段{name}】只 {block_len(txt)} 字，要求 ≥{need}")
        if block_len(s["live"]) < 40 and "无" not in s["live"].split("】")[-1]:
            errors.append(f"{tag} 【本段现场生成】只 {block_len(s['live'])} 字，要求 ≥60（没有就写「无」）")
        # 现场生成：只列要重建的条目，不写「取自参考图/不再重建」这类说明
        live_body = s["live"].split("】", 1)[-1]
        for w in ("不再重建", "取自参考图", "取用层", "重建层", "没有独立参考图"):
            if w in live_body:
                notes.append(f"{tag} 【本段现场生成】出现「{w}」：只列要重建的元素（1. 2. 3.），"
                             f"不写来源说明")
                break
        if live_body.strip() and live_body.strip() != "无" and not re.search(r"(?m)^\s*1[.、]", live_body):
            notes.append(f"{tag} 【本段现场生成】没有分条：用 1. / 2. / 3. 各占一行列出要重建的元素")
        for sh in s["shots"]:
            if len(re.sub(r"\s", "", sh["body"])) < 70:
                errors.append(f"{tag} 镜头{sh['no']:02d} 正文只 {len(sh['body'])} 字，要求 ≥70")

        # 镜数声明
        cn = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10,
              "十一":11,"十二":12,"十三":13,"十四":14,"十五":15,"十六":16,"十七":17,"十八":18}
        mnum = re.search(r"([一二三四五六七八九十]+)镜按下列时码", s["style"])
        if mnum:
            claim = cn.get(mnum.group(1))
            if claim and claim != len(s["shots"]):
                errors.append(f"{tag} 声明「{mnum.group(1)}镜」但实际有 {len(s['shots'])} 个镜头")

        # 终态：只记切出瞬间的状态，不写动作、不写下段指令
        for w in ("下一段", "下一集", "下一镜", "接着拍"):
            if w in s["final"]:
                notes.append(f"{tag} 【本段终态】出现「{w}」：终态只记切出瞬间的状态（位置/朝向/持握/开门角度/道具），"
                             f"不写动作、不写下段指令——否则模型会把它当镜头再演一遍")
                break


        # 其它
        if "不显示任何字幕" not in (s["style"] + s["live"]):
            errors.append(f"{tag} 缺画面声明：整体基准末尾加「画面内除指定屏幕文字外，不显示任何字幕、水印与台标。」")
        blob = s["style"] + s["space"] + "".join(sh["body"] for sh in s["shots"])
        for w in BANNED:
            if w in blob:
                errors.append(f"{tag} 出现抽象大词「{w}」")
        for w in OMIT:
            if w in blob:
                errors.append(f"{tag} 出现省略语「{w}」")
        if len(s["style"] + s["space"] + s["final"]) > MAX_CHARS:
            errors.append(f"{tag} 单段超过 {MAX_CHARS} 字")

    if total > 180 + 1e-6 and total > args_total_holder[0] + 1e-6:
        errors.append(f"全片总时长 {fmt(total)} > {fmt(args_total_holder[0])}")
    return errors, notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--target", type=float, default=SEG_MAX)
    ap.add_argument("--total", type=float, default=TOTAL_MAX)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    text = Path(args.path).read_text(encoding="utf-8-sig")
    segs = parse(text)
    args_total_holder[0] = args.total
    errors, notes = check(segs, args.target)

    total = sum(s["dur"] for s in segs)
    shots = sum(len(s["shots"]) for s in segs)
    resolved = [s for s in segs if s["map"]]
    refs = [len(s["map"]) or len([e for e in s["lock"] if e["table"] in IMG_TABLES]) for s in segs]

    if args.json:
        print(json.dumps({"segments": len(segs), "shots": shots, "total": total,
                          "errors": errors, "notes": notes}, ensure_ascii=False, indent=2))
        return 0 if not errors else 1

    print(f"文件: {Path(args.path).name}  段数 {len(segs)}  镜头数 {shots}  总时长 {fmt(total)}")
    ok = not errors
    print(f"  {'✓' if ok else '✗'} 结构/时间/资产/台词/密度  ({len(errors)} 处)")
    if errors:
        for e in errors[:40]:
            print(f"    ! {e}")
        if len(errors) > 40:
            print(f"    … 另有 {len(errors) - 40} 处")
    if notes:
        for n in notes[:10]:
            print(f"    · {n}")
    print(f"  ✓ 段数 {len(segs)} / 镜头 {shots} / 总时长 {fmt(total)}")
    print(f"  ✓ 每段 ≤{fmt(args.target)}，全片 ≤{fmt(TOTAL_MAX)}")
    print(f"  ✓ 参考图 {refs}")
    print("  · 人工项仍需逐条过：可见性三分 / 轴线一致 / 机位反算 / 过肩虚实 / 景别精度 / 起幅落幅 / 一镜一动作 / 台词只出现一次 / 运镜成立（起止景别、路径各自成立、推拉非平面缩放、接镜轴线）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
