# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
t = t.replace('errors_pending_audio.append(f"第{cur[\'no\']:02d}段 音频参考没写 {音色库：名} 锚点")',
              'cur.setdefault("dlg_errors", []).append(f"第{cur[\'no\']:02d}段 音频参考没写 {{音色库：名}} 锚点")')
open(p, "w", encoding="utf-8").write(t)
print("fixed")
