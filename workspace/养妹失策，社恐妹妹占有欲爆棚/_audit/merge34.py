# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
t = open(f, encoding="utf-8").read().replace("\r\n", "\n")

def parse_seg(name):
    a = t.index(f"## 【第{name}段")
    b = t.index("## 【第", a + 5) if name != "04" else len(t)
    seg = t[a:b]
    shots = []
    for m in re.finditer(r"(?ms)^【镜头\d+｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.*?)(?=\n【镜头|\n【本段终态】|\Z)", seg):
        blk = m.group(4).strip()
        lines = [l for l in blk.split("\n") if l.strip()]
        shots.append({"title": m.group(3), "dur": round(float(m.group(2)) - float(m.group(1)), 1),
                      "body": "\n".join(l for l in lines if not l.startswith("[")),
                      "dlg": [l for l in lines if l.startswith("[")]})
    return a, b, seg, shots

a3, b3, s3, sh3 = parse_seg("03")
a4, b4, s4, sh4 = parse_seg("04")
print("p3", [s["title"] for s in sh3], sum(s["dur"] for s in sh3))
print("p4", [s["title"] for s in sh4], sum(s["dur"] for s in sh4))

new3 = sh3 + sh4[:9]
new4 = sh4[9:]
# p3 配平到 30（三百平 3.0→2.5）
for s in new3:
    if s["title"] == "三百平的别墅":
        s["dur"] = 2.5
total3 = sum(s["dur"] for s in new3)
print("新 p3 合计", total3, "新 p4", [s["title"] for s in new4], sum(s["dur"] for s in new4))

def render(idx, shots, dur, rhythm, space, final, base_light, sil, lock):
    out = [f"## 【第{idx}段｜[0s-{dur}s]｜{shots[0]['title']}】\n"]
    out.append("【本段资产锁定】\n" + lock + "\n")
    out.append("【本段现场生成】\n" + LIVE + "\n")
    out.append(f"【本段整体基准】\n16:9，24fps，真人电影质感。{base_light}\n{sil}\n{rhythm}"
               "各资产在真实空间中重建材质、体积、透视、投光与动态身份，周围墙面、地砖与空气连续完整。"
               "画面内除指定屏幕文字外，不显示任何字幕、水印与台标。\n\n")
    out.append("【本段初始空间】\n" + space + "\n\n")
    t0 = 0.0
    for i, s in enumerate(shots, 1):
        a, b = round(t0, 1), round(t0 + s["dur"], 1); t0 = b
        body = s["body"]
        for dl in s["dlg"]:
            body += "\n" + re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", dl)
        out.append(f"【镜头{i:02d}｜[{a:g}s-{b:g}s]｜{s['title']}】\n{body}\n")
    out.append("【本段终态】\n" + final + "\n")
    return "\n".join(out)

LOCK = re.search(r"(?ms)【本段资产锁定】\n(.*?)(?=\n【本段现场生成】)", s3).group(1).strip()
LIVE = re.search(r"(?ms)【本段现场生成】\n(.*?)(?=\n【本段整体基准】)", s3).group(1).strip()

R3 = "十三镜按下列时码依次硬切：拎箱子→她抬头→进不进→迈进门槛→猫一样的脚步→把鞋摆好→双手交叠→打量→三百平的别墅→家的味道→偷瞄→炸毛的猫→只有一张床；前半在门外的走廊，跨过门槛后收在她光脚站在玄关的局促上。表演基调：【陈诚】的硬只到嗓子、手先软；【沈幼怡】的拘谨全在脚尖、手指和呼吸上。"
R4 = "三镜按下列时码依次硬切：手机震了→最后一行→气笑；这是全集的钩子，屏幕上的字要看清，气笑要收在眼睛里。表演基调：【陈诚】的笑意只停在嘴角、眼睛里没有。"
SP3 = "【陈诚公寓走廊】：门大开约一肩宽，门板朝画左；【陈诚】侧身站在门内、右手刚把【行李箱】拎离地面；【沈幼怡】在门外半步、正面朝门，【双肩书包】挂右肩。机位在门外、略低于【陈诚】下巴。本段开始时箱子刚离地，后半段两人走进玄关。"
F3 = "【沈幼怡】光脚站在玄关、【手机】握在胸前；【陈诚】站在客厅中央、刚挠完后脑勺，视线落在玄关。下一段她的手机震动。"
SP4 = "【陈诚公寓客厅】：入户门在画左，玄关地砖与客厅木地板在画面下三分之一分界；沙发在画左靠墙，矮茶几在中央，开放式厨房在画右后；机位在客厅中央、朝玄关。【沈幼怡】站在玄关、双手握着【手机】；【陈诚】站在客厅中央、侧身对着她。"
F4 = "【沈幼怡】还站在玄关、【手机】握在胸前；【陈诚】站在客厅里，刚笑完、眼神冷着。下一集从这句「照顾？」接。"
LIGHT3 = "八月末下午两点半，门外的走廊白光过曝，门内玄关偏暗，客厅没开灯、一半亮一半暗。整体低饱和灰调。"
LIGHT4 = "八月末下午两点半，客厅没开灯，光从玄关和厨房窗进来，一半亮一半暗。整体低饱和灰调，空气里有一点肥皂味。"
SIL3 = "【沈幼怡】保持浅蓝碎花连衣裙、白袜黑皮鞋，进门后光脚；【陈诚】黑色微卷中长发、白 T 黑短裤。"
SIL4 = "【沈幼怡】保持浅蓝碎花连衣裙、光脚；【陈诚】黑色微卷中长发、白 T 黑短裤，站得很直。"

newtext = render("03", new3, 30, R3, SP3, F3, LIGHT3, SIL3, LOCK) + "\n" + render("04", new4, 6, R4, SP4, F4, LIGHT4, SIL4, LOCK)
t = t[:a3] + newtext
open(f, "w", encoding="utf-8").write(t)
print("重切完成")
