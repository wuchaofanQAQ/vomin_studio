# -*- coding: utf-8 -*-
# 1) workspace.yaml 关闭 TTS
p = r"workspace\养妹失策，社恐妹妹占有欲爆棚\workspace.yaml"
t = open(p, encoding="utf-8").read()
old = "tts:\n  format: mp3\n  model: seed-audio-1.0\n  sample_rate: 48000"
new = "tts:\n  enabled: false\n  format: mp3\n  model: seed-audio-1.0\n  sample_rate: 48000"
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("yaml: tts disabled")

# 2) cli.py: 尊重 tts.enabled
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''    dialogue = shot.get("dialogue") or _dialogue_from_prompt(shot.get("prompt", ""))
    if dialogue:'''
new = '''    dialogue = shot.get("dialogue") or _dialogue_from_prompt(shot.get("prompt", ""))
    tts_enabled = (cfg.get("tts", {}) or {}).get("enabled", True)
    if dialogue and tts_enabled:'''
assert t.count(old) == 1
t = t.replace(old, new)
old2 = '''        tts = DoubaoTTS()
        tts_cfg = cfg.get("tts", {})'''
new2 = '''        tts = DoubaoTTS()
        tts_cfg = cfg.get("tts", {}) or {}'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
open(p, "w", encoding="utf-8").write(t)
print("cli: tts gate added")
