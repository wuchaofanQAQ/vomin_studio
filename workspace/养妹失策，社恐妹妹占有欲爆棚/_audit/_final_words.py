# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:24]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\script-asset-extraction\references\asset-rules.md", [
("| 同名 + 已出图 | 复用，`status=复用`，描述与提示词都不动 |",
 "| 同名 + 已出图 | 复用，`status=复用`，描述不动 |"),
("| 同名 + 未出图 | 补齐描述与提示词，`status=新建` |",
 "| 同名 + 未出图 | 补齐描述，`status=新建` |"),
])

rep(r"skills\script-asset-extraction\references\scene-anchors.md", [
("| 光源方向 | 主光方向与锚点一致 | 改提示词重抽 |",
 "| 光源方向 | 主光方向与锚点一致 | 改描述重抽 |"),
("| 共享物件 | 跨场景的门/窗/五金外观一致 | 改提示词重抽 |",
 "| 共享物件 | 跨场景的门/窗/五金外观一致 | 改描述重抽 |"),
("2. 先改提示词：把没遵守的锚点写进 ≤50 字的提示词（用词更具体），必要时加一句参考图约束；",
 "2. 先改描述：把没遵守的锚点写进那句 ≤50 字描述（用词更具体），必要时单独写一句参考图约束；"),
])

rep(r"skills\script-asset-extraction\SKILL.md", [
("- 不抽不存在的资产；不把剧情、情绪、比喻写进描述与提示词。",
 "- 不抽不存在的资产；不把剧情、情绪、比喻写进描述。"),
])
print("done")
