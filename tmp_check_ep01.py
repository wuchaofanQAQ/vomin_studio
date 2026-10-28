# -*- coding: utf-8 -*-
"""分镜设计稿自检：段/镜时间轴、资产锁定、禁用词、可见性、字数。"""
import io, re, sys

P = r"workspace/养妹失策，社恐妹妹占有欲爆棚/drafts/ep01_分镜设计稿.md"
text = io.open(P, encoding="utf-8").read()

errs, warns = [], []

# ---------- 1. 切段 ----------
seg_re = re.compile(r"【第(\d+)段｜\[0s-(\d+(?:\.\d+)?)s\]｜([^】]+)】")
segs = []
idx = [(m.start(), m.end(), m) for m in seg_re.finditer(text)]
for i, (s, e, m) in enumerate(idx):
    end = idx[i + 1][0] if i + 1 < len(idx) else len(text)
    segs.append({"no": int(m.group(1)), "dur": float(m.group(2)),
                 "title": m.group(3), "body": text[s:end].strip()})

print(f"段数 = {len(segs)}")
if [s["no"] for s in segs] != list(range(1, len(segs) + 1)):
    errs.append("段号不连续")

total = 0.0
shot_total = 0
timeline = ["全段实速、无慢镜", "全段实速"]  # 只做提示

for seg in segs:
    b = seg["body"]
    total += seg["dur"]
    # 头里必须写全
    for need in ["【本段资产锁定】", "【本段现场生成】", "【本段整体基准】",
                 "【本段初始空间】", "【本段终态】"]:
        if need not in b:
            errs.append(f"段{seg['no']:02d} 缺 {need}")

    # ---------- 2. 镜头时间轴 ----------
    shots = re.findall(r"【镜头(\d+)｜\[(\d+(?:\.\d+)?)s-(\d+(?:\.\d+)?)s\]｜([^】]+)】", b)
    if not shots:
        errs.append(f"段{seg['no']:02d} 无镜头")
        continue
    shot_total += len(shots)
    nums = [int(s[0]) for s in shots]
    if nums != list(range(1, len(shots) + 1)):
        errs.append(f"段{seg['no']:02d} 镜号不连续 {nums}")
    prev = 0.0
    for n, st, en, ti in shots:
        st, en = float(st), float(en)
        if abs(st - prev) > 1e-6:
            errs.append(f"段{seg['no']:02d} 镜{n} 起 {st} != 上镜止 {prev}")
        if en <= st:
            errs.append(f"段{seg['no']:02d} 镜{n} 时长<=0")
        for t in (st, en):
            if abs(t * 2 - round(t * 2)) > 1e-6:
                errs.append(f"段{seg['no']:02d} 镜{n} 时码 {t} 不在 0.5 格")
        if not (0.5 <= en - st <= 12.0):
            warns.append(f"段{seg['no']:02d} 镜{n} 时长 {en-st}s 偏长/偏短")
        prev = en
    if abs(prev - seg["dur"]) > 1e-6:
        errs.append(f"段{seg['no']:02d} 末镜止 {prev} != 段长 {seg['dur']}")

    # ---------- 3. 台词行落在镜内 ----------
    for m in re.finditer(r"\[(\d+(?:\.\d+)?)s-(\d+(?:\.\d+)?)s\]，([^，]+)，【([^】]+)】（([^）]*)）：「(.+)」", b):
        st, en = float(m.group(1)), float(m.group(2))
        inside = any(float(s[1]) <= st and en <= float(s[2]) for s in shots)
        if not inside:
            errs.append(f"段{seg['no']:02d} 台词 [{st}-{en}]s 不在任何镜内")

    # ---------- 4. 图N 映射 ----------
    lock = b.split("【本段资产锁定】")[1].split("【本段现场生成】")[0]
    fig = dict(re.findall(r"图(\d+) =【([^】]+)】", lock))
    mp = re.search(r"【参考图映射】(.+)", lock)
    if mp:
        pairs = re.findall(r"图(\d+)=【([^】]+)】", mp.group(1))
        if [p[0] for p in pairs] != sorted(fig.keys(), key=int):
            errs.append(f"段{seg['no']:02d} 参考图映射编号与锁定不一致")
        for num, name in pairs:
            if fig.get(num) != name.strip():
                errs.append(f"段{seg['no']:02d} 图{num} 映射 {name} != 锁定 {fig.get(num)}")
        if [p[0] for p in pairs] != list(map(str, range(1, len(pairs) + 1))):
            errs.append(f"段{seg['no']:02d} 参考图映射编号不连续")
    elif fig:
        errs.append(f"段{seg['no']:02d} 有带图资产却缺【参考图映射】")

    # 正文出现的【名】必须是锁定项
    body_after = b.split("【本段整体基准】")[1] if "【本段整体基准】" in b else ""
    body_after = re.sub(r"\[\d+(?:\.\d+)?s-\d+(?:\.\d+)?s\]，[^\n]*", "", body_after)
    locked = set(fig.values()) | {"少年陈诚", "林女士", "沈崇山"}
    for tag in set(re.findall(r"【([^】]{1,12})】", body_after)):
        if tag in ("沈幼怡的手机", "陈诚的手机"):
            continue
        if tag not in locked and tag not in (
                "本段终态", "本段初始空间"):
            # 允许段头风格标签之外的合法结构名
            if tag not in ("陈诚", "沈幼怡"):
                warns.append(f"段{seg['no']:02d} 正文出现未锁定标签【{tag}】")

    # ---------- 5. 字数 ----------
    print(f"  段{seg['no']:02d} {seg['dur']:>5}s {len(shots):>2}镜 "
          f"{len(b):>5}字  {seg['title']}")

# ---------- 6. 全局禁用写法 ----------
for bad in ["同上", "同机位", "接上一段", "承接上一段", "参见第", "保持上一段",
            "不要", "禁止", "无慢镜。", "下一段从"]:
    if bad in text:
        hits = [m.start() for m in re.finditer(re.escape(bad), text)]
        if bad == "不要":
            # 允许剧本原台词里的否定
            for h in hits:
                ctx = text[max(0, h - 40):h + 40]
                if "「" not in ctx:
                    errs.append(f"出现负向指令「不要」：{ctx.strip()}")
        elif bad == "无慢镜。":
            pass
        else:
            errs.append(f"出现禁用写法「{bad}」×{len(hits)}")

print(f"\n总时长 = {total}s  /  总镜数 = {shot_total}")
if shot_total != 46:
    errs.append(f"镜数 {shot_total} != 方案B 46 镜")
if not (110 <= total <= 160):
    warns.append(f"总时长 {total}s 偏离剧本预估 118s 较多")

print("\n=== ERROR ===")
[print(" !", e) for e in errs]
print("=== WARN ===")
[print(" ~", w) for w in warns]
print(f"\n结果：{len(errs)} 错误 / {len(warns)} 提示")
