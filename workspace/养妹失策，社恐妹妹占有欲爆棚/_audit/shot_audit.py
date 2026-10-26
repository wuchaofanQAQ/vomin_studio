# -*- coding: utf-8 -*-
import re, json, os
base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01m_storyboard_v1.md"), encoding="utf-8").read()

def han(s):
    return len(re.findall(r"[\u4e00-\u9fff]", s))

parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", md)
rows = []
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    dur = float(re.search(r"\[0s-([\d.]+)s\]", head).group(1))
    shots = re.findall(r"(?ms)^【镜头(\d+)｜\[([\d.]+)s-([\d.]+)s\]｜(.+?)】\n(.+?)(?=\n\n|\Z)", body)
    for no, a, b, title, txt in shots:
        words = 0
        for line in txt.split("\n"):
            m = re.match(r"^\[[\d.]+s-[\d.]+s\]，.+?：「(.+)」$", line.strip())
            if m:
                words += han(m.group(1))
        actual = float(b) - float(a)
        # 建议时长：有台词按 字数/4.8+0.3；无台词按动作分句数 ×0.7，最少1.0
        if words:
            exp = words / 4.8 + 0.3
        else:
            clauses = max(1, txt.split("\n")[0].count("；") + 1)
            exp = min(2.4, max(1.0, clauses * 0.6 + 0.4))
        rows.append({"seg": int(re.search(r"第(\d+)段", head).group(1)), "no": int(no),
                     "title": title.strip(), "words": words, "actual": round(actual, 1),
                     "exp": round(exp, 1), "diff": round(actual - exp, 1)})

print(f"{'段':<3}{'镜':<4}{'标题':<10}{'字数':<5}{'现长':<6}{'建议':<6}{'偏差'}")
for r in rows:
    flag = "  ← 偏长" if r["diff"] > 0.4 else ("  ← 偏短" if r["diff"] < -0.4 else "")
    print(f"{r['seg']:<3}{r['no']:<4}{r['title'][:8]:<10}{r['words']:<5}{r['actual']:<6}{r['exp']:<6}{r['diff']}{flag}")

over = [r for r in rows if r["diff"] > 0.4]
under = [r for r in rows if r["diff"] < -0.4]
print(f"\n偏长 {len(over)} 镜，共多 {round(sum(r['diff'] for r in over),1)}s；偏短 {len(under)} 镜，共少 {round(sum(-r['diff'] for r in under),1)}s")
for s in (1,2,3):
    seg_rows = [r for r in rows if r["seg"] == s]
    print(f"第{s}段 合计 {round(sum(r['actual'] for r in seg_rows),1)}s / 应为 {round(sum(r['exp'] for r in seg_rows),1)}s")
