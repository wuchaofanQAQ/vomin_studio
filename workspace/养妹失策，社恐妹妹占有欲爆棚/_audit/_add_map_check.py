# -*- coding: utf-8 -*-
# 1) checker: 解析并校验【参考图映射】
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace(
'''ENTRY_RE = re.compile(r"【([A-Z]{1,2})(\\d{2})｜([^：】]+?)(?:：([^】]*))?】")''',
'''ENTRY_RE = re.compile(r"【([A-Z]{1,2})(\\d{2})｜([^：】]+?)(?:：([^】]*))?】")
MAP_RE = re.compile(r"^【参考图映射】(.+)$")
MAP_ITEM_RE = re.compile(r"^图(\\d+)=([A-Z]{1,2}\\d{2})(.+)$")''')

t = t.replace(
'''        if cur.get("in_lock"):
            cm = CAT_RE.match(line)
            if cm:
                cur["lock_lines"].append((cm.group(1), cm.group(2)))
            continue''',
'''        if cur.get("in_lock"):
            mm = MAP_RE.match(line)
            if mm:
                cur["map_line"] = mm.group(1).strip()
                continue
            cm = CAT_RE.match(line)
            if cm:
                cur["lock_lines"].append((cm.group(1), cm.group(2)))
            continue''')

t = t.replace(
'''                "assets": [],          # (id, name, category, extra)
                "lock_lines": [],''',
'''                "assets": [],          # (id, name, category, extra)
                "lock_lines": [],
                "map_line": "",''')

# 在资产锁定检查之后插入映射校验
t = t.replace(
'''        locked = [(aid, n) for aid, n in seen_ids.items()]

        # ---- 时间轴 ----''',
'''        locked = [(aid, n) for aid, n in seen_ids.items()]

        # ---- 参考图映射（按锁定区出现顺序编号） ----
        anchored = []
        for cat, payload in s["lock_lines"]:
            if cat not in ("场景", "角色"):
                continue
            for letter, num, name, _ in ENTRY_RE.findall(payload):
                anchored.append((f"{letter}{num}", name.strip()))
        if anchored:
            if not s["map_line"]:
                errors.append(f"{tag} 缺【参考图映射】行（多个参考图时模型无法对应 图N 与资产）")
            else:
                items = [x.strip() for x in s["map_line"].split("；") if x.strip()]
                parsed = []
                for it in items:
                    mm2 = MAP_ITEM_RE.match(it)
                    if not mm2:
                        errors.append(f"{tag} 参考图映射条目格式不对：{it[:18]}（应为 图1=S01场景名）")
                        continue
                    parsed.append((int(mm2.group(1)), mm2.group(2), mm2.group(3).strip()))
                if [n for n, _, _ in parsed] != list(range(1, len(parsed) + 1)):
                    errors.append(f"{tag} 参考图映射编号不是从 1 连续")
                if len(parsed) != len(anchored):
                    errors.append(f"{tag} 参考图映射 {len(parsed)} 条，锁定区带图资产 {len(anchored)} 条，数量不一致")
                for (n, aid, name), (eaid, ename) in zip(parsed, anchored):
                    if aid != eaid or name != ename:
                        errors.append(f"{tag} 参考图映射第{n}条「{aid}{name}」与锁定区第{n}个带图资产「{eaid}{ename}」不一致")

        # ---- 时间轴 ----''')

open(p, "w", encoding="utf-8").write(t)
print("checker updated")
