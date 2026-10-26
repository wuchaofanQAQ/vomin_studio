# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:40]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

# 1) 校验器：台词改用「」，『』视为旧写法
rep(r"skills\drama-segment-generation\scripts\check_segment_prompt.py", [
('''            if not (text.startswith("『") and text.endswith("』")):
                cur.setdefault("dlg_errors", []).append(f"第{cur['no']:02d}段 台词未用『』括起：{text[:14]}")''',
 '''            if not (text.startswith("「") and text.endswith("」")):
                cur.setdefault("dlg_errors", []).append(f"第{cur['no']:02d}段 台词未用「」括起：{text[:14]}")'''),
])

# 2) SKILL：示例与规则改成「」
rep(r"skills\drama-segment-generation\SKILL.md", [
("`00:05-00:06，R01沈幼怡（压着声音、断续地说）：『台词』`", "`00:05-00:06，R01沈幼怡（压着声音、断续地说）：「台词」`"),
("00:02-00:03，R01沈幼怡（几乎不发声、气声说）：『我是沈幼怡。』", "00:02-00:03，R01沈幼怡（几乎不发声、气声说）：「我是沈幼怡。」"),
("00:03.5-00:05，R02陈诚（压着火、短促地说）：『谁啊？』", "00:03.5-00:05，R02陈诚（压着火、短促地说）：「谁啊？」"),
("`00:05-00:06，编号名称（情绪/语气/状态地说）：『台词』`；行首是时间窗，不用【对白】前缀",
 "`00:05-00:06，编号名称（情绪/语气/状态地说）：「台词」`；行首是时间窗，不用【对白】前缀；台词一律用「」"),
("`00:09-00:10.5，编号名称画外音（画左/画右、…地说）：『台词』`", "`00:09-00:10.5，编号名称画外音（画左/画右、…地说）：「台词」`"),
])

# 3) project-adaptation：台词示例改「」
rep(r"skills\drama-segment-generation\references\project-adaptation.md", [
("00:05-00:06，R02陈诚（压着火、短促地说）：『你爸呢？』", "00:05-00:06，R02陈诚（压着火、短促地说）：「你爸呢？」"),
("00:09-00:10.5，R02陈诚画外音（画右门板后、压低地说）：『谁啊？』", "00:09-00:10.5，R02陈诚画外音（画右门板后、压低地说）：「谁啊？」"),
("- 台词用 `『』` 括起，逐字，不改写、不合并、不删；每句只在真正发声的位置出现一次；",
 "- 台词用 `「」` 括起，逐字，不改写、不合并、不删；每句只在真正发声的位置出现一次；"),
])
print("quote rules updated")
