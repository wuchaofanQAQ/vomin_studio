# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
start = s.index("## 【第01段")
end = s.index("## 【第02段")
seg = s[start:end]

# 解析：镜号 -> (标题, 正文, 台词行列表)
shots = {}
cur = None
for ln in seg.split("\n"):
    m = re.match(r"^【镜头(\d+)｜\[[\d.]+s-[\d.]+s\]｜(.+?)】$", ln)
    if m:
        cur = int(m.group(1)); shots[cur] = {"title": m.group(2), "body": "", "lines": []}
        continue
    if cur is None:
        continue
    if ln.startswith("["):
        shots[cur]["lines"].append(ln)
    elif ln.strip() and not ln.startswith("【本段"):
        shots[cur]["body"] = ln

# 06 改为纯翻转
shots[6]["title"] = "把屏幕翻过来"
shots[6]["body"] = "过【陈诚】肩的机位近景，镜头不动。前景是【陈诚】虚化的肩线与门框，中景【沈幼怡】双手把【手机】翻转过来、屏幕正对着他；她的拇指还压在机身边缘，指节因为用力泛白。切在屏幕转正、手机举稳。"
shots[6]["lines"] = []

# 新增屏幕镜
screen = {"title": "屏幕上的字",
          "body": "屏幕正面的特写，镜头不动。画面里只有【手机】屏幕：一个微信聊天框，对方还没存名字，气泡里一行字被调到最大，白底黑字，几乎顶到屏幕两侧——「我是沈幼怡」，末尾一个句号；输入框还亮着，光标一闪一闪。屏幕边缘反出【沈幼怡】拇指的一点影。切在这行字完全定住、光把画面压成一整块白。",
          "lines": ["（字幕·手机）我是沈幼怡。"]}

times = [(0,1.3),(1.3,2.6),(2.6,4.0),(4.0,6.7),(6.7,8.8),(8.8,9.8),(9.8,11.5),(11.5,13.0),
         (13.0,14.5),(14.5,16.0),(16.0,19.4),(19.4,21.0),(21.0,22.8),(22.8,24.6),(24.6,27.0),(27.0,28.0)]

seq = [1,2,3,4,5,6,"S",7,8,9,10,11,12,13,14,15]
blocks = []
for i, key in enumerate(seq):
    a, b = times[i]
    sh = screen if key == "S" else shots[key]
    blocks.append(f"【镜头{i+1:02d}｜[{a:g}s-{b:g}s]｜{sh['title']}】\n{sh['body']}" +
                  ("\n" + "\n".join(sh["lines"]) if sh["lines"] else ""))

head = seg[:seg.index("【镜头01")]
head = head.replace("十五镜按下列时码依次硬切", "十六镜按下列时码依次硬切")
tail = "【本段终态】\n" + seg.split("【本段终态】")[1].strip() + "\n\n"
s = s[:start] + head + "\n\n".join(blocks) + "\n\n" + tail + s[end:]
open(f, "w", encoding="utf-8").write(s)
print("p01 重排为 16 镜，含屏幕特写")
