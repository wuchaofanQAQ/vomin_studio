# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
t = t.replace('if anchor not in payload and "待出图" not in payload:',
              'if anchor not in payload and "待出图" not in payload and "画外音" not in payload:')
t = t.replace('if "待出图" not in payload:\n                        anchored.append',
              'if "待出图" not in payload and "画外音" not in payload:\n                        anchored.append')
open(p, "w", encoding="utf-8").write(t)
print("checker: voice-only role skips anchor")

p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01_storyboard_v4.md"
t = open(p, encoding="utf-8").read()
t = t.replace("落幅停在行李箱停稳的位置", "落幅停在 P01行李箱停稳的位置")
t = t.replace("落幅停在两人之间的行李箱上", "落幅停在两人之间的 P01行李箱上")
open(p, "w", encoding="utf-8").write(t)
print("storyboard: bare names fixed")
