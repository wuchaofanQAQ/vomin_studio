# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
md = open(f, encoding="utf-8").read()

# 抽出所有镜头（全局顺序）
shots = []
for m in re.finditer(r"(?ms)^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", md):
    shots.append({"title": m.group(2), "body": m.group(3).strip()})
print("镜头总数", len(shots))

def exp_of(txt):
    chars = 0
    for ln in txt.split("\n"):
        mm = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", ln.strip())
        if mm: chars += len(mm.group(1))
    action = re.split(r"[。]", txt.split("\n")[0])[0]
    clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
    return round(max(1.0, min(3.4, 0.5 + 0.8 * max(1, clauses)), chars / 4.8 + 0.3 if chars else 0), 1)

for s in shots:
    s["exp"] = exp_of(s["body"])

BOUNDS = [12, 23, 32, len(shots)]  # 4 段
segs, prev = [], 0
for b in BOUNDS:
    segs.append(shots[prev:b]); prev = b
for i, s in enumerate(segs, 1):
    print(f"第{i}段 {round(sum(x['exp'] for x in s),1)}s / {len(s)}镜")

# 段头/锁定/现场/基准/空间/终态
LOCK = """【本段资产锁定】
角色：
图1 =【沈幼怡】  {资产库：沈幼怡}；
图2 =【陈诚】  {资产库：陈诚}；
场景：
图3 =【陈诚公寓走廊】  {资产库：陈诚公寓走廊}；
图4 =【陈诚公寓玄关】  {资产库：陈诚公寓玄关}；
道具：
图5 =【行李箱】  {资产库：行李箱}；
图6 =【双肩书包】  {资产库：双肩书包}；
图7 =【手机】  {资产库：手机}；"""

LIVE = "回忆两镜用回忆质感：旧木桌上一块插着蜡烛的方形蛋糕、砸碎的白碗、女人拎深棕软皮包跟深灰西装男人出门。走廊门铃是深灰金属圆钮。这些元素没有独立参考图，按上述形制在真实空间中重建。"
BASE = "16:9，24fps，真人电影质感，八月末下午两点。走廊 40℃白炽直射，硬光比，浅米灰地砖上是硬边光斑；回忆转低饱和冷灰、四角压暗、细颗粒。整体低饱和灰调。【沈幼怡】保持角色资产的面容、浅蓝碎花连衣裙，长发被汗黏在颊侧；【陈诚】保持黑色微卷中长发、白 T 黑短裤。"
SPACE = "【陈诚公寓走廊】：入户门在画右中段、门板朝画左；【沈幼怡】在门外画面中央偏左、正面朝画右，【行李箱】在右脚边、拉杆拉出，【双肩书包】挂右肩；【陈诚】在门内、只入半个身位。机位在走廊内、与胸口平齐。"

D_LOCK = """【本段资产锁定】
角色：
图1 =【沈幼怡】  {资产库：沈幼怡}；
图2 =【陈诚】  {资产库：陈诚}；
场景：
图3 =【陈诚公寓客厅】  {资产库：陈诚公寓客厅}；
图4 =【陈诚公寓玄关】  {资产库：陈诚公寓玄关}；
道具：
图5 =【双肩书包】  {资产库：双肩书包}；
图6 =【手机】  {资产库：手机}；"""
D_BASE = "16:9，24fps，真人电影质感，八月末下午两点半。客厅没开灯，光从玄关和厨房窗进来，一半亮一半暗；整体低饱和灰调，空气里有一点肥皂味。【沈幼怡】光脚、怯、不抬眼；【陈诚】站得很直、手不知道往哪放。"
D_SPACE = "【陈诚公寓客厅】：入户门在画左，玄关地砖与客厅木地板在画面下三分之一分界；沙发在画左靠墙，矮茶几在中央，开放式厨房在画右后，通往卧室的门在画右；机位在客厅中央、与站姿平齐。"

FINALS = [
 "【沈幼怡】还站在门外、【手机】举在胸前；【陈诚】在门内半步、视线落在她脸上。下一段他开口拒绝。",
 "【陈诚】凑在猫眼上，【沈幼怡】在门外纹丝不动，【行李箱】在她脚边。下一段他拉开门。",
 "门开着，【陈诚】侧身站在门内、手里提着【行李箱】；【沈幼怡】已经跨进门槛、光脚站在玄关地砖上。下一段她走进客厅。",
 "【沈幼怡】光脚站在玄关、【手机】握在胸前；【陈诚】站在客厅里、侧身对着她，刚笑完、眼神冷着。",
]

out = []
for idx, seg in enumerate(segs, 1):
    dur = round(sum(x["exp"] for x in seg), 1)
    title = ["走廊·我是沈幼怡", "走廊·我这儿不是民宿", "走廊·进不进", "玄关客厅·你哥哥会照顾好你的"][idx-1] if idx <= 4 else "玄关客厅"
    if idx <= 3:
        lock, live, base, space = LOCK, LIVE, BASE, SPACE
    else:
        lock, live, base, space = D_LOCK, "玄关地砖上留着一小片被晒出的热气；门边的鞋架空着两层；客厅的沙发、茶几、开放式厨房与通往卧室的门在同一个通间里。", D_BASE, D_SPACE
    out.append(f"## 【第{idx:02d}段｜[0s-{dur:g}s]｜{title}】\n")
    out.append(lock + "\n")
    out.append("【本段现场生成】\n" + live + "\n")
    out.append(f"【本段整体基准】\n{base}\n{len(seg)}镜按下列时码依次硬切，平均每镜约{round(dur/len(seg),1)}秒；前一镜切出的姿态是后一镜的动作起点。声音层次：门铃、蝉鸣、空调外机低频嗡声、门板闷响、行李箱拉杆的金属声。画面内除指定屏幕文字外，不显示任何字幕、水印与台标。\n")
    out.append("【本段初始空间】\n" + space + "\n")
    t = 0.0
    for n, sh in enumerate(seg, 1):
        a, b = round(t, 1), round(t + sh["exp"], 1); t = b
        body = sh["body"]
        body = re.sub(r"\[[\d.]+s-[\d.]+s\]，", f"[{a:g}s-{b:g}s]，", body)
        out.append(f"【镜头{n:02d}｜[{a:g}s-{b:g}s]｜{sh['title']}】\n{body}\n")
    out.append("【本段终态】\n" + FINALS[idx-1] + "\n")

open(f, "w", encoding="utf-8").write("\n".join(out))
print("4 段重建完成")
