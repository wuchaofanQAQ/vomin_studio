# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

start = s.index("## 【第01段")
end = s.index("## 【第02段")
seg = s[start:end]

# 新时间表（16 镜）
times = [(0,1.3),(1.3,2.6),(2.6,4.0),(4.0,6.7),(6.7,8.8),(8.8,9.8),(9.8,11.5),(11.5,13.0),
         (13.0,14.5),(14.5,16.0),(16.0,19.4),(19.4,21.0),(21.0,22.8),(22.8,24.6),(24.6,27.0),(27.0,28.0)]

# 拆出所有镜头块（header + body + 可能的台词行）
lines = seg.split("\n")
out, i = [], 0
while i < len(lines):
    ln = lines[i]
    m = re.match(r"^【镜头(\d+)｜", ln)
    if m:
        no = int(m.group(1))
        block = [ln]
        i += 1
        while i < len(lines) and not lines[i].startswith("【镜头") and not lines[i].startswith("## "):
            block.append(lines[i]); i += 1
        out.append((no, block))
        continue
    out.append((None, [ln])); i += 1

# 先按镜号建 map
shots = {no: blk for no, blk in out if no}
# 06 只保留翻转动作
shots[6] = ["【镜头06｜[0s-0s]｜把屏幕翻过来】",
 "过【陈诚】肩的机位近景，镜头不动。前景是【陈诚】虚化的肩线与门框，中景【沈幼怡】双手把【手机】翻转过来、屏幕正对着他；她的拇指还压在机身边缘，指节因为用力泛白。切在屏幕转正、手机举稳。"]
# 新插入 07：屏幕特写（给观众看字）
screen = ["【镜头07｜[0s-0s]｜屏幕上的字】",
 "屏幕正面的特写，镜头不动。画面里只有【手机】屏幕：一个微信聊天框，对方还没存名字，气泡里一行字被调到最大，白底黑字，几乎顶到屏幕两侧——「我是沈幼怡」，末尾一个句号；输入框还亮着，光标一闪一闪。屏幕边缘反出【沈幼怡】拇指的一点影。切在这行字完全定住、光把画面压成一整块白。",
 "（字幕·手机）我是沈幼怡。"]

new_seg = []
# 重建：按原顺序 1..15，遇到 6 插入 screen
order = list(range(1, 16))
for no in order:
    blk = shots[no]
    # 重新编号与时间
    idx = len(new_seg)  # 0-based
    a, b = times[idx]
    hdr = re.sub(r"\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", blk[0])
    hdr = re.sub(r"^【镜头\d+", f"【镜头{idx+1:02d}", hdr)
    body = blk[1] if len(blk) > 1 else ""
    dlg = blk[2:] if len(blk) > 2 else []
    new_seg.append(hdr); new_seg.append(body)
    for d in dlg:
        if d.strip():
            new_seg.append(re.sub(r"^\[[\d.]+s-[\d.]+s\]", f"[{a:g}s-{b:g}s]", d))
    new_seg.append("")
    if no == 6:
        ia, ib = times[len(new_seg)//1 if False else 6]
        h = re.sub(r"\[[\d.]+s-[\d.]+s\]", f"[{ia:g}s-{ib:g}s]", screen[0])
        h = re.sub(r"^【镜头\d+", f"【镜头{len([x for x in new_seg if x.startswith('【镜头')])+1:02d}", h)
        new_seg.append(h); new_seg.append(screen[1]); new_seg.append(screen[2]); new_seg.append("")

seg_new = seg[:seg.index("【镜头01")] + "\n".join(new_seg) + "\n【本段终态】\n" + seg.split("【本段终态】")[1].strip() + "\n\n"
seg_new = seg_new.replace("十五镜按下列时码依次硬切", "十六镜按下列时码依次硬切")
s = s[:start] + seg_new + s[end:]
open(f, "w", encoding="utf-8").write(s)
print("p01 插入屏幕特写镜")
