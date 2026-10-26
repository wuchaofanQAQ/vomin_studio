# -*- coding: utf-8 -*-
p = r"skills\script-to-prompt-30\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
t = t.replace('doc = parse(Path(args.path).read_text(encoding="utf-8"))',
              'doc = parse(Path(args.path).read_text(encoding="utf-8-sig"))')
t = t.replace('data = json.loads(Path(args.registry).read_text(encoding="utf-8"))',
              'data = json.loads(Path(args.registry).read_text(encoding="utf-8-sig"))')
open(p, "w", encoding="utf-8").write(t)
print("ok")
