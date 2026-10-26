# -*- coding: utf-8 -*-
import re
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
md = open(base + r"\drafts\ep01m_storyboard_v1.md", encoding="utf-8").read()

def han(s): return len(re.findall(r"[\u4e00-\u9fff]", s))

parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", body)
    for no, a, b, title, txt in shots:
        words = 0
        for line in txt.split("\n"):
            m = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", line.strip())
            if m: words += han(m.group(1))
        body0 = txt.split("\n")[0]
        action = re.split(r"[。]", body0)[0]
        clauses = len([c for c in re.split(r"[；，、]", action) if len(c.strip()) > 3])
        actual = float(b) - float(a)
        if words:
            exp = words / 4.8 + 0.3
            kind = "台词"
        else:
            exp = min(3.4, 0.5 + 0.8 * max(1, clauses))
            kind = f"动作{clauses}"
        rows.append((int(re.search(r"第(\d+)段", head).group(1)), int(no), title.strip(), kind, words,
                     round(actual,1), round(exp,1), round(actual-exp,1)))

print(f"{'段':<2}{'镜':<3}{'标题':<10}{'依据':<7}{'现长':<6}{'应有':<6}{'偏差'}")
for seg, no, t, k, w, a, e, d in rows:
    flag = " ←偏长" if d > 0.5 else (" ←偏短" if d < -0.5 else "")
    print(f"{seg:<2}{no:<3}{t[:8]:<10}{k:<7}{a:<6}{e:<6}{d}{flag}")
over = [r for r in rows if r[7] > 0.5]; under = [r for r in rows if r[7] < -0.5]
print(f"\n偏长 {len(over)} 镜（多 {round(sum(r[7] for r in over),1)}s）| 偏短 {len(under)} 镜（少 {round(-sum(r[7] for r in under),1)}s）")
