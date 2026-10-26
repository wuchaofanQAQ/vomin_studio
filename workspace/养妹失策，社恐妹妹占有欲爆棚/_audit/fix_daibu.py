# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        blk = cur.get("block")
        if blk == "lock":
            m = LOCK_RE.match(line)'''
new = '''        blk = cur.get("block")
        if blk == "lock":
            # 待补资产：没有参考图，但仍是本段合法资产名
            m = re.match(r"^待补：【([^】]+)】", line)
            if m:
                cur["lock"].append({"name": m.group(1), "table": "待补", "row": "", "voice": None})
                continue
            m = LOCK_RE.match(line)'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("待补 entries now parsed")
