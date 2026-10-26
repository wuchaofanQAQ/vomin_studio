p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()
t = t.replace("写入飞书、出图、配音、出片都要用户确认。", "写入飞书、出图、出片都要用户确认。")
open(p, "w", encoding="utf-8").write(t)
print("desc fixed")
