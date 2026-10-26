# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace('"""剧本转提示词 3.0 分段提示词校验。', '"""剧本转提示词 4.2 分段提示词校验。')

t = t.replace(r'CAT_RE = re.compile(r"^(场景|角色|道具|特效|群像|生物|载具|建筑|服装|装置)：(.+)$")',
              r'CAT_RE = re.compile(r"^(场景|角色|道具|特效|群像|动物|生物|载具|建筑|服装|装置|待补)：(.+)$")')

t = t.replace('''CAT_LETTER = {
    "场景": "S", "角色": "R", "群像": "M", "道具": "P", "特效": "FX",
    "生物": "C", "载具": "V", "建筑": "B", "服装": "W", "装置": "D",
}''',
'''CAT_LETTER = {
    "场景": "S", "角色": "R", "群像": "M", "道具": "P", "特效": "FX",
    "动物": "C", "生物": "C", "载具": "V", "建筑": "B", "服装": "W", "装置": "D",
}''')

# parse: 段结构标记 + 待补
t = t.replace('''                "map_line": "",
                "style": "",''',
'''                "map_line": "",
                "sections": set(),
                "pending": [],
                "style": "",''')

t = t.replace('''        if line == "【资产锁定】":
            cur["in_lock"] = True
            continue
        if line.startswith("【本段风格】"):
            cur["in_lock"] = False
            cur["style"] = line
            shot = None
            continue
        if line.startswith("【本段初始空间基准】"):
            cur["in_lock"] = False
            cur["space"] = line
            shot = None
            continue''',
'''        if line == "【本段资产锁定】":
            cur["in_lock"] = True
            cur["sections"].add("lock")
            continue
        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")
            shot = None
            continue
        if line.startswith("【本段整体基准】"):
            cur["in_lock"] = False
            cur["sections"].add("base")
            cur["style"] = line
            shot = None
            continue
        if line.startswith("【本段初始空间】"):
            cur["in_lock"] = False
            cur["sections"].add("space")
            cur["space"] = line
            shot = None
            continue
        if line.startswith("【本段终态】"):
            cur["in_lock"] = False
            cur["sections"].add("final")
            shot = None
            continue''')

t = t.replace('''            cm = CAT_RE.match(line)
            if cm:
                cur["lock_lines"].append((cm.group(1), cm.group(2)))''',
'''            cm = CAT_RE.match(line)
            if cm:
                if cm.group(1) == "待补":
                    for letter, num, name, extra in ENTRY_RE.findall(cm.group(2)):
                        cur["pending"].append((f"{letter}{num}", name.strip(), extra))
                else:
                    cur["lock_lines"].append((cm.group(1), cm.group(2)))''')

open(p, "w", encoding="utf-8").write(t)
print("parse patched")
