# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace('errors_soft.append(f"第{cur[\'no\']:02d}段 台词未用『』括起：{text[:14]}")',
              'cur.setdefault("dlg_errors", []).append(f"第{cur[\'no\']:02d}段 台词未用『』括起：{text[:14]}")')

t = t.replace('''                "dialogues": [],
                "chars": 0,''',
'''                "dialogues": [],
                "dlg_errors": [],
                "chars": 0,''')

t = t.replace('''        if s["chars"] > MAX_CHARS:''',
'''        errors.extend(s.get("dlg_errors", []))

        if s["chars"] > MAX_CHARS:''')

open(p, "w", encoding="utf-8").write(t)
print("fixed")
