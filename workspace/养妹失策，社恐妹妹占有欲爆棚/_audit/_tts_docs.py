# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:34]}")
        if c != 1:
            continue
        t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("【对白 00:00.5-00:02】R01角色名（情绪/语气地说）：『台词。』",
 "00:00.5-00:02，R01角色名（情绪/语气地说）：『台词。』"),
('''【对白 00:01-00:02】R02陈诚（压着火、短促地说）：『你爸呢？』
【对白 00:09-00:10.5】R02陈诚画外音（画右门板后、压低地说）：『谁啊？』
【对白 00:18.5-00:20】R02陈诚（内心独白、嘴唇不动地说）：『沈幼怡。这三个字，』''',
'''00:01-00:02，R02陈诚（压着火、短促地说）：『你爸呢？』
00:09-00:10.5，R02陈诚画外音（画右门板后、压低地说）：『谁啊？』
00:18.5-00:20，R02陈诚（内心独白、嘴唇不动地说）：『沈幼怡。这三个字，』'''),
("- 前缀 `【对白 起-止】` 供配音与对白窗口校验；时间窗必须落在所在镜头内；",
 "- 行首 `起-止` 是时间窗，必须落在所在镜头内；不加 `【对白】` 前缀；"),
("- 配音时 CLI 会剥掉括号表演提示、编号前缀与\"画外音\"，按名称去 `角色档案` 取音色。",
 "- 本项目不做 TTS：对白由视频模型原生发声；需要固定音色时写 `音频参考：{音色库：音色名}`。"),
("- 分镜表不单独存台词字段；`【对白】` 行是唯一台词来源。",
 "- 分镜表不单独存台词字段；行首时间窗的台词行是唯一台词来源。"),
("4. 用户确认 → `write --table 剧本分镜表` → `generate --tts-only` → `generate` → `push`",
 "4. 用户确认 → `write --table 剧本分镜表` → `generate` → `push`"),
])

rep(r"skills\ai-drama-harness\SKILL.md", [
("   - ★ **成片时长与配音**：`generate` 按分镜行 `timeline`（如 `00:00-00:30`）的真实秒数出片，上限 30 秒，解析不出才回退 `ark.default_duration`；成本按实际秒数估算，清单里列出各段秒数。配音按提示词里的 `【对白 起-止】R01角色（…地说）：台词` 行逐句、从**角色档案**取音色（`voice_desc`）合成（编号与括号表演提示会被剥离），档案缺该角色或音色会警告并用默认音色——写分镜前先确认对白角色都有角色档案且填了音色",
 "   - ★ **成片时长与声音**：`generate` 按分镜行 `timeline`（如 `00:00-00:30`）的真实秒数出片，上限 30 秒，解析不出才回退 `ark.default_duration`；成本按实际秒数估算，清单里列出各段秒数。本项目**不做 TTS**：对白由视频模型原生发声；需要固定音色时写 `音频参考：{音色库：音色名}`，CLI 会把它作为 `reference_audio` 传给模型"),
("   python cli.py generate $WS --tts-only\n", ""),
])

rep(r"skills\ai-drama-harness\references\pipeline.md", [
("  → (确认点3) write 分镜表 → generate 配音+视频 → push",
 "  → (确认点3) write 分镜表 → generate 出片 → push"),
("generate --tts-only → generate → push", "generate → push"),
])

rep(r"skills\ai-drama-harness\references\cli-commands.md", [
("# 仅生成配音（不出视频，省钱）\npython cli.py generate <workspace> --tts-only",
 "# 仅生成配音（本项目已关闭 TTS，tts.enabled=false 时此命令为空操作）\npython cli.py generate <workspace> --tts-only"),
])

rep(r"skills\ai-drama-harness\references\checkpoint-protocol.md", [
("| 写入/消费 | `generate`（出图/视频/配音，花预算） | **每次必须确认** |",
 "| 写入/消费 | `generate`（出图/视频，花预算） | **每次必须确认** |"),
])

rep(r"skills\drama-segment-generation\references\example-segment.md", [
("> 正文每次写资产都用\"编号+名称\"（`R01沈幼怡`），不写裸名、不加【】；台词行保留 `【对白 起-止】` 前缀（本项目 TTS 要用），行内是「角色 + 语气 + 说 + 『台词』」。",
 "> 正文每次写资产都用\"编号+名称\"（`R01沈幼怡`），不写裸名、不加【】；台词直接写在发声位置：`00:09-00:10.5，R02陈诚（…地说）：『…』`（行首时间窗，不用【对白】前缀）。"),
])

rep(r"skills\novel-to-drama\references\adaptation-rules.md", [
("- 说话人每句都要标出，供下游 TTS 匹配音色",
 "- 说话人每句都要标出，供下游绑定角色与音色"),
("1. **字幕不是台词**：短信、微信、打字内容一律走字幕行，不进对白（下游 TTS 不配音，只做画面字幕）",
 "1. **字幕不是台词**：短信、微信、打字内容一律走字幕行，不进对白（下游只做画面字幕，不当台词发声）"),
])

rep(r"skills\novel-to-drama\references\script-format.md", [
("字幕**不是台词**：不参与 TTS 配音，只做画面文字。",
 "字幕**不是台词**：不发声，只做画面文字。"),
("1. **不挂角色名**。`沈幼怡：（屏幕字幕）…` 是错的——挂了名字就变成台词，TTS 会用她的音色念字幕",
 "1. **不挂角色名**。`沈幼怡：（屏幕字幕）…` 是错的——挂了名字就变成台词，会被当成她开口说话"),
])

rep(r"skills\drama-initializer\references\character-extract-init.md", [
("| C 音色层 | `voice_desc` | 性别、年龄感、音色、语速、口音/方言；供 TTS |",
 "| C 音色层 | `voice_desc` | 性别、年龄感、音色、语速、口音/方言；供音色绑定参考 |"),
("## 三、角色库（精简版，与生图/TTS 直接对接）",
 "## 三、角色库（精简版，与生图/音色直接对接）"),
])
print("done")
