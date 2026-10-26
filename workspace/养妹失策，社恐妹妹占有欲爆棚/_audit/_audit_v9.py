import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\鍏诲澶辩瓥锛岀ぞ鎭愬濡瑰崰鏈夋鐖嗘"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v9.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
seg_re = re.compile(rf"(?m)^## (銆愮(\d+)娈碉綔({T})-({T})锝?.+?)銆?\s*$")
parts = md.split("## ")[1:]
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
print("娈? 琛? 鏃堕棿绐?     瀛楁暟  瀛?绉? 鏂囨湰")
for b in parts:
    lines = b.splitlines()
    header = lines[0]
    m = re.match(r"(銆愮(\d+)娈碉綔(" + T + r")-(" + T + r")锝?.+?)銆?", header)
    no = int(m.group(2)); seg_start, seg_end = sec(m.group(3)), sec(m.group(4))
    for ln in lines:
        mm = re.match(rf"^({T})-({T})锛?.+?)锛?.+)$", ln.strip())
        if not mm: continue
        a, z = sec(mm.group(1)), sec(mm.group(2))
        txt = re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4))
        dur = max(z - a, 1e-6)
        flag = "  <<< 澶揩" if len(txt)/dur > 6.2 else ""
        print(f"{no:02d}  {mm.group(1)}-{mm.group(2)}  {len(txt):3d}  {len(txt)/dur:5.1f}  {mm.group(3)[:12]}锛歿mm.group(4)[:30]}{flag}")
