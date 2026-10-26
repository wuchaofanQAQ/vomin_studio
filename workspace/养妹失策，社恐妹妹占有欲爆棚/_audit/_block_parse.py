# -*- coding: utf-8 -*-
import re
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace('''                "sections": set(),
                "live": "",''', '''                "sections": set(),
                "block": "",
                "live": "",''')

t = t.replace('''        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")
            cur["live"] = line''',
'''        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")
            cur["block"] = "live"
            cur["live"] = line''')

t = t.replace('''            cur["sections"].add("base")
            cur["style"] = line''',
'''            cur["sections"].add("base")
            cur["block"] = "style"
            cur["style"] = line''')
t = t.replace('''            cur["sections"].add("space")
            cur["space"] = line''',
'''            cur["sections"].add("space")
            cur["block"] = "space"
            cur["space"] = line''')
t = t.replace('''            cur["sections"].add("final")
            cur["final"] = line''',
'''            cur["sections"].add("final")
            cur["block"] = "final"
            cur["final"] = line''')

# 镜头头出现时结束块
t = t.replace('''            cur["shots"].append(shot)
            continue''', '''            cur["shots"].append(shot)
            cur["block"] = ""
            continue''')

# 块内续行累积
t = t.replace('''        if cur.get("in_lock"):''', '''        blk = cur.get("block")
        if blk and not line.startswith("【"):
            cur[blk] = cur.get(blk, "") + "\\n" + line
            continue

        if cur.get("in_lock"):''')

open(p, "w", encoding="utf-8").write(t)
print("multi-line blocks captured")

# 修裸名
p2 = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_p01_dense.md"
s = open(p2, encoding="utf-8").read()
s = re.sub(r"(?<!P01)行李箱", "P01行李箱", s)
s = re.sub(r"(?<!P02)双肩书包", "P02双肩书包", s)
# 资产锁定行里本来就有 P01/P02 前缀，不会重复；检查
assert "P01P01" not in s and "P02P02" not in s
open(p2, "w", encoding="utf-8").write(s)
print("bare names fixed")
