# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = '''        if not s["shots"]:
            errors.append(f"{tag} 没有镜头")
        if not s["lock_lines"]:
            errors.append(f"{tag} 没有【资产锁定】")'''
new = '''        if not s["shots"]:
            errors.append(f"{tag} 没有镜头")
        need = [("lock", "本段资产锁定"), ("base", "本段整体基准"),
                ("space", "本段初始空间"), ("final", "本段终态")]
        miss = [n for k, n in need if k not in s["sections"]]
        if miss:
            errors.append(f"{tag} 缺结构段：{'、'.join(miss)}")
        if not s["lock_lines"] and not s["pending"]:
            errors.append(f"{tag} 【本段资产锁定】里没有任何资产条目")'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''        locked = [(aid, n) for aid, n in seen_ids.items()]'''
new2 = '''        # ---- 待补资产 ----
        for aid, name, extra in s["pending"]:
            if not name:
                errors.append(f"{tag} 待补资产【{aid}】缺名称")
            if "待补" not in (extra or ""):
                errors.append(f"{tag} 待补【{aid}｜{name}】没写「待补，未读取」")
            if "{" in (extra or ""):
                errors.append(f"{tag} 待补【{aid}｜{name}】不应带库锚点（库里没有这个资产）")
            if name in name_map:
                errors.append(f"{tag} 「{name}」既在锁定区又标待补，二选一")

        locked = [(aid, n) for aid, n in seen_ids.items()]'''
assert t.count(old2) == 1
t = t.replace(old2, new2)

open(p, "w", encoding="utf-8").write(t)
print("check patched")
