import re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v8.md"), encoding="utf-8").read()
T = r"\d{2}:\d{2}(?:\.\d)?"
seg_re = re.compile(rf"(?m)^## (【第(\d+)段｜({T})-({T})｜(.+?)】)\s*$")
parts = md.split("## ")[1:]
def sec(t):
    m, s = t.split(":"); return int(m)*60 + float(s)
print("段  行  时间窗      字数  字/秒  文本")
for b in parts:
    lines = b.splitlines()
    header = lines[0]
    m = re.match(r"(【第(\d+)段｜(" + T + r")-(" + T + r")｜(.+?)】)", header)
    no = int(m.group(2)); seg_start, seg_end = sec(m.group(3)), sec(m.group(4))
    for ln in lines:
        mm = re.match(rf"^({T})-({T})，(.+?)：(.+)$", ln.strip())
        if not mm: continue
        a, z = sec(mm.group(1)), sec(mm.group(2))
        txt = re.sub(r"[^\u4e00-\u9fff]", "", mm.group(4))
        dur = max(z - a, 1e-6)
        flag = "  <<< 太快" if len(txt)/dur > 6.2 else ""
        print(f"{no:02d}  {mm.group(1)}-{mm.group(2)}  {len(txt):3d}  {len(txt)/dur:5.1f}  {mm.group(3)[:12]}：{mm.group(4)[:30]}{flag}")
