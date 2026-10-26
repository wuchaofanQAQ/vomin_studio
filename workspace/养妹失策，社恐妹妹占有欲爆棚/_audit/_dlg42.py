# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = r'DLG_RE = re.compile(rf"^【对白\s*({T})-({T})】(.+?)：(.*)$")'
new = r'DLG_RE = re.compile(rf"^({T})\s*[-—]\s*({T})，(.+?)：(.+)$")'
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''        m = DLG_RE.match(line)
        if m:
            cur["dialogues"].append({
                "start": sec(m.group(1)),
                "end": sec(m.group(2)),
                "speaker": m.group(3).strip(),
                "text": m.group(4).strip(),
                "shot": shot["no"] if shot else None,
            })
            continue'''
new2 = '''        m = DLG_RE.match(line)
        if m and shot is not None:
            text = m.group(4).strip()
            cur["dialogues"].append({
                "start": sec(m.group(1)),
                "end": sec(m.group(2)),
                "speaker": m.group(3).strip(),
                "text": text,
                "shot": shot["no"] if shot else None,
            })
            if not (text.startswith("『") and text.endswith("』")):
                errors_soft.append(f"第{cur['no']:02d}段 台词未用『』括起：{text[:14]}")
            continue'''
assert t.count(old2) == 1
t = t.replace(old2, new2)

open(p, "w", encoding="utf-8").write(t)
print("dialogue regex patched")
