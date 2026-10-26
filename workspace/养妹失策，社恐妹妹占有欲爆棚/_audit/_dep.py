# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        if line.startswith("音频参考：") and "{音色库：" not in line:'''
new = '''        if line.startswith("【对白"):
            cur.setdefault("dlg_errors", []).append(
                f"第{cur['no']:02d}段 用了已废弃的【对白】前缀，4.2 写成 `00:05-00:06，角色（…地说）：『…』`")

        if line.startswith("音频参考：") and "{音色库：" not in line:'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("deprecation check added")
