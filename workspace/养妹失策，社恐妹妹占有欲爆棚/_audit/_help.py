# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'ap.add_argument("--target", type=int, default=None, help="每段目标秒数（默认按 6~30 校验）")'
new = 'ap.add_argument("--target", type=int, default=None, help="强制每段等于该秒数（默认可选：6~30，并按复杂度校验上限）")'
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("ok")
