# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:34]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\drama-segment-generation\SKILL.md", [
("| 音效 | 只写有助于判断动作因果与空间方向的音效，带归属与方向；不写装饰清单 |",
 "| 音效 | 只写有助于判断动作因果与空间方向的音效，带归属与方向；不写装饰清单 |\n| 音色 | 需要固定音色时，锁定区单起一行 `音频参考：【R01沈幼怡：{音色库：沈幼怡-清冷少女}】`；音色库里没有这一行就不要写（本项目不做 TTS） |"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("| `{素材库：素材ID}` / `{生图工作台：任务名}` | 移除 | 对应素材文件 |",
 "| `{素材库：素材ID}` / `{生图工作台：任务名}` | 移除 | 对应素材文件 |\n| `音频参考：【R01沈幼怡：{音色库：音色名}】` | `音频参考：【R01沈幼怡】` | 音色库里的音频文件（`reference_audio`） |"),
])

# checker: 音频参考 必须带音色库锚点
rep(r"skills\drama-segment-generation\scripts\check_segment_prompt.py", [
('''        if cur.get("in_lock"):''',
'''        if line.startswith("音频参考：") and "{音色库：" not in line:
            errors_pending_audio.append(f"第{cur['no']:02d}段 音频参考没写 {音色库：名} 锚点")

        if cur.get("in_lock"):'''),
])
print("done")
