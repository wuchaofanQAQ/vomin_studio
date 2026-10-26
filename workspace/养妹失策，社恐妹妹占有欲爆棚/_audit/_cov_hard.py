# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_coverage.py"
t = open(p, encoding="utf-8").read()

t = t.replace('SKIP_HINTS = ("说道", "看着", "笑了笑")',
'''SKIP_HINTS = ("说道", "看着", "笑了笑")
# 心理/判断/动机类句子：删掉会让观众少一个"为什么"，单独列为硬问题
HARD_HINTS = ("心想", "心里", "暗道", "琢磨", "觉得", "以为", "明白", "知道", "猜",
              "判断", "不能", "必须", "得先", "不然", "否则", "为什么", "是不是",
              "难道", "要是", "怕", "担心", "希望", "打算", "只能", "只好", "应该",
              "真会", "肯定", "明显", "不可能", "凭什么", "居然", "竟然", "果然",
              "可以", "会不", "是吧", "对吧")''')

old = '''    sents = [s for s in sentences(novel) if len(s) >= args.min_len]
    rows = []
    for s in sents:
        cov = coverage(s, script_grams)
        if cov < args.threshold:
            rows.append({"text": s, "coverage": round(cov, 2)})'''
new = '''    sents = [s for s in sentences(novel) if len(s) >= args.min_len]
    rows, hard = [], []
    for s in sents:
        cov = coverage(s, script_grams)
        if cov >= args.threshold:
            continue
        item = {"text": s, "coverage": round(cov, 2)}
        rows.append(item)
        if any(h in s for h in HARD_HINTS) or "？" in s or "?" in s:
            hard.append(item)'''
assert t.count(old) == 1
t = t.replace(old, new)

t = t.replace('''        "missing": rows[:60],
        "missing_count": len(rows),''',
'''        "missing": rows[:60],
        "missing_count": len(rows),
        "hard": hard,
        "hard_count": len(hard),''')

t = t.replace('''        return 0 if not rows and not missing_quotes else 1''',
'''        return 0 if not hard and not missing_quotes else 1''')

t = t.replace('''    print(f"疑似丢失: {len(rows)} 句；引号台词 {len(quotes)} 句，其中 {len(missing_quotes)} 句没进剧本")''',
'''    print(f"疑似丢失: {len(rows)} 句（其中心理/判断/动机类 {len(hard)} 句）；"
          f"引号台词 {len(quotes)} 句，{len(missing_quotes)} 句没进剧本")''')

t = t.replace('''    if rows:
        print("\\n[疑似被删的句子]")
        for r in rows[:40]:
            print(f"  ({r['coverage']:.2f}) {r['text']}")
    return 0 if not rows and not missing_quotes else 1''',
'''    if hard:
        print("\\n[硬问题·心理/判断/动机句没落点]")
        for r in hard[:30]:
            print(f"  ({r['coverage']:.2f}) {r['text']}")
    others = [r for r in rows if r not in hard]
    if others:
        print("\\n[建议复核·描写/叙述被压缩]")
        for r in others[:30]:
            print(f"  ({r['coverage']:.2f}) {r['text']}")
    return 0 if not hard and not missing_quotes else 1''')

open(p, "w", encoding="utf-8").write(t)
print("hard classification added")
