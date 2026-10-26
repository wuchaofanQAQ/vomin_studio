# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\scripts\check_coverage.py"
t = open(p, encoding="utf-8").read()

old = '''QUOTE_RE = re.compile(r"[“\\"「『]([^”\\"」』]{2,80})[”\\"」』]")'''
new = '''QUOTE_RE = re.compile(r"[“\\"「『]([^”\\"」』]{2,80})[”\\"」』]")
PUNCT = re.compile(r"[\\s，。！？、；：…\\.\\!\\?,\\.;:~\\-\\u2014\\u201c\\u201d\\u2018\\u2019「」『』\\(\\)（）]")'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''    quotes = [q for q in QUOTE_RE.findall(novel) if len(norm(q)) >= 3]
    missing_quotes = [q for q in quotes if norm(q) not in script_n]'''
new2 = '''    quotes = [q for q in QUOTE_RE.findall(novel) if len(norm(q)) >= 3]

    def quote_in(q: str) -> bool:
        """台词比对：去掉标点后做 3-gram 覆盖，容忍省略号/标点差异。"""
        qn = PUNCT.sub("", q)
        if not qn:
            return True
        if qn in PUNCT.sub("", script):
            return True
        g = {qn[i:i + 3] for i in range(len(qn) - 2)} if len(qn) >= 3 else {qn}
        sn = PUNCT.sub("", script)
        sg = set()
        for n in (3, 4):
            sg |= {sn[i:i + n] for i in range(len(sn) - n + 1)}
        return len(g & sg) / len(g) >= 0.9

    missing_quotes = [q for q in quotes if not quote_in(q)]'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("coverage: fuzzy quote matching")
