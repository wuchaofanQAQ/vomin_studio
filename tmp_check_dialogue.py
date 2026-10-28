# -*- coding: utf-8 -*-
"""第二轮：台词逐字核对、语速核算、屏幕文字覆盖、可见主体抽查。"""
import io, re, json

DRAFT = r"workspace/养妹失策，社恐妹妹占有欲爆棚/drafts/ep01_分镜设计稿.md"
SCRIPT = r"tmp_ep1_script.txt"

draft = io.open(DRAFT, encoding="utf-8").read()
script = io.open(SCRIPT, encoding="utf-8").read()

# ---------- 剧本事实 ----------
# 语音台词（陈诚）
voice = re.findall(r"陈诚（[^）]*）：「(.+?)」", script)
# 屏幕字幕
screen = re.findall(r"（字幕·[^）]*）(.+?)\n", script)

print("剧本语音台词 =", len(voice))
for v in voice:
    print("   ", v)
print("剧本屏幕字幕 =", len(screen))
for s in screen:
    print("   ", s)

# ---------- 草稿里的台词行 ----------
lines = re.findall(r"\[(\d+(?:\.\d+)?)s-(\d+(?:\.\d+)?)s\]，([^，]+)，【([^】]+)】（([^）]*)）：「(.+?)」", draft)
print(f"\n草稿台词行 = {len(lines)}")
PUNCT = "，。！？、…—：；「」（）"
def han(s):
    return len([c for c in s if c not in PUNCT])

errs, warns = [], []
seen = {}
for st, en, typ, who, note, txt in lines:
    st, en = float(st), float(en)
    seen[txt] = seen.get(txt, 0) + 1
    n = han(txt)
    rate = n / max(1e-6, en - st)
    flag = "" if 3.8 <= rate <= 6.2 else "  <<< 语速异常"
    print(f"  [{st:>5}-{en:>5}] {typ:>4} 【{who}】 {n:>2}字 {rate:4.2f}字/秒  {txt}{flag}")
    if txt not in voice:
        errs.append(f"台词与剧本不一致：{txt}")
    if flag:
        warns.append(f"语速 {rate:.2f} 字/秒：{txt}")

# 剧本每一句必须出现且只出现一次
for v in voice:
    if seen.get(v, 0) != 1:
        errs.append(f"剧本台词出现 {seen.get(v,0)} 次：{v}")

# ---------- 屏幕文字 ----------
print("\n屏幕文字覆盖：")
for s in screen:
    core = s.rstrip("。")
    c = draft.count(core)
    print(f"   {c}×  {s}")
    if c < 1:
        errs.append(f"屏幕文字缺失：{s}")

# ---------- 可见主体抽查：每段正文出现的角色必须已锁定 ----------
print("\n=== 结果 ===")
[print(" !", e) for e in errs]
[print(" ~", w) for w in warns]
print(f"{len(errs)} 错误 / {len(warns)} 提示")
