# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:40]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\SKILL.md", [
("台词行 `【对白 00:01-00:02】R01沈幼怡（…地说）：『……』`",
 "台词行 `00:01-00:02，R01沈幼怡（…地说）：『……』`"),
("     python cli.py preflight $WS --episode N    # 生产态资产复检，0 问题才继续\n       python cli.py generate $WS\n     python cli.py push $WS",
 "     python cli.py preflight $WS --episode N    # 生产态资产复检，0 问题才继续\n     python cli.py generate $WS\n     python cli.py push $WS"),
("只有 preflight 全过、进入生产态后才写 `12 项自检：PASS`",
 "只有 preflight 全过、进入生产态后才写 `自检：PASS`"),
])

rep(r"skills\AI短剧生产底座使用手册.md", [
("| `python cli.py generate <路径> --tts-only` | 仅配音 | **是** |",
 "| `python cli.py generate <路径> --tts-only` | 仅配音（本项目 `tts.enabled=false`，已停用） | **是** |"),
("| C 音色层 | 音色/语速/口音 | `voice_desc` | 配音、TTS |",
 "| C 音色层 | 音色/语速/口音 | `voice_desc` | 音色参考（`{音色库：名}`） |"),
])

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("| C 音色 | `voice_desc` | TTS/配音（分镜对白按说话人从角色档案匹配音色；音色字段只在角色档案，角色库没有） |",
 "| C 音色 | `voice_desc` | 音色参考（需要固定音色时写 `音频参考：{音色库：名}`，本项目不做 TTS） |"),
])
print("done")
