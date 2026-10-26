# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_coverage.py"
t = open(p, encoding="utf-8").read()

old = '''def coverage(sent: str, script_grams: set[str]) -> float:
    g = grams(sent)
    if not g:
        return 1.0
    return len(g & script_grams) / len(g)'''
new = '''def coverage(sent: str, script_grams: set[str]) -> float:
    g = grams(sent)
    if not g:
        return 1.0
    return len(g & script_grams) / len(g)


def clause_coverage(sent: str, script_grams: set[str]) -> float:
    """按逗号切小句分别比对：一句里只要多数小句有落点就算保住，
    容忍"低骂一声 + OS"这类被拆成两行的写法。"""
    clauses = [c for c in re.split(r"[，,；;、]", sent) if len(c) >= 4]
    if len(clauses) <= 1:
        return coverage(sent, script_grams)
    hit = sum(1 for c in clauses if coverage(c, script_grams) >= 0.6)
    return hit / len(clauses)'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''    for s in sents:
        cov = coverage(s, script_grams)
        if cov >= args.threshold:'''
new2 = '''    for s in sents:
        cov = max(coverage(s, script_grams), clause_coverage(s, script_grams))
        if cov >= args.threshold:'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("clause-level coverage")
