# -*- coding: utf-8 -*-
"""单人物镜头：第 2 次及以后出现改用代词（首现仍保留【】）。"""
import io, re

P = r"workspace/养妹失策，社恐妹妹占有欲爆棚/drafts/ep01_分镜设计稿.md"
t = io.open(P, encoding="utf-8").read()
CH = ["沈幼怡", "陈诚", "林女士", "沈崇山"]
PRON = {"沈幼怡": "她", "林女士": "她", "陈诚": "他", "沈崇山": "他"}

seg_spans = [(m.start(), m.group(1)) for m in re.finditer(r"【第0?(\d+)段｜", t)]
seg_spans.append((len(t), None))
out, changed = [], 0
for i in range(len(seg_spans) - 1):
    s, no = seg_spans[i]
    e = seg_spans[i + 1][0]
    block = t[s:e]
    shots = [(m.start(), m.group(1)) for m in re.finditer(r"【镜头(\d+)｜", block)]
    if not shots:
        out.append(block); continue
    shots.append((len(block), None))
    out.append(block[:shots[0][0]])
    for j in range(len(shots) - 1):
        seg_txt = block[shots[j][0]:shots[j + 1][0]]
        head, _, body = seg_txt.partition("\n")
        body = body.split("\n", 1)[0]          # 只处理正文首行
        rest = seg_txt.partition("\n")[2][len(body):]
        present = [c for c in CH if c in body]
        if len(present) == 1:
            c = present[0]
            tok = "【" + c + "】"
            first = body.find(tok)
            nxt = body.find(tok, first + 1) if first >= 0 else -1
            if nxt > 0:
                body = body[:nxt] + PRON[c] + body[nxt + len(tok):]
                changed += 1
        out.append(head + "\n" + body + rest)

new = "".join(out)
io.open(P, "w", encoding="utf-8").write(new)
print(f"单人镜头代词化 {changed} 处；总长 {len(new)}")
