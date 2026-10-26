# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = '''        blk = cur.get("block")
        if blk and not line.startswith("【"):
            cur[blk] = cur.get(blk, "") + "\\n" + line
            continue
        if cur.get("in_lock"):
            m = LOCK_RE.match(line)
            if m:
                name, table, row = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
                voice = None
                vm = VOICE_RE.search(line)
                if vm:
                    voice = vm.group(2).strip()
                cur["lock"].append({"name": name, "table": table, "row": row, "voice": voice})
                continue
        if shot is not None:
            shot["body"] += line'''
new = '''        blk = cur.get("block")
        if blk == "lock":
            m = LOCK_RE.match(line)
            if m:
                name, table, row = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
                voice = None
                vm = VOICE_RE.search(line)
                if vm:
                    voice = vm.group(2).strip()
                cur["lock"].append({"name": name, "table": table, "row": row, "voice": voice})
            continue
        if blk in ("live", "style", "space", "final"):
            cur[blk] = cur.get(blk, "") + "\\n" + line
            continue
        if shot is not None:
            shot["body"] += line'''
assert t.count(old) == 1
t = t.replace(old, new)

t = t.replace('if not any(k in body[-30:] for k in STOP):', 'if not any(k in body[-45:] for k in STOP):')
open(p, "w", encoding="utf-8").write(t)
print("parse fixed")
