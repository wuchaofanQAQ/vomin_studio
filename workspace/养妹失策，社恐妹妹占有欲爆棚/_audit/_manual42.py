# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()
reps = [
("→ ⑤ drama-segment-generation       拆分镜+依赖+视频提示词     → 写入分镜表 → 触发配音+视频",
 "→ ⑤ drama-segment-generation       资产绑定+拆分镜+依赖+视频提示词 → 写入分镜表 → 触发配音+视频"),
('| 剧集分段并出视频提示词（3.0） | "剧集分段 / 分段生成 / 剧本转提示词 / 3.0 / 拆分镜 / 分镜脚本 / 视频提示词 / 30秒分段" | drama-segment-generation |',
 '| 剧集分段并出视频提示词（4.2） | "剧集分段 / 分段生成 / 剧本转提示词 / 4.2 / 资产绑定 / 拆分镜 / 分镜脚本 / 视频提示词" | drama-segment-generation |'),
("⑤ drama-segment-generation（只读 当前集±1集 的完整剧本）：",
 "⑤ drama-segment-generation（读 当前集±1集 剧本 + 三张资产表做绑定）："),
]
for old, new in reps:
    c = t.count(old)
    print(c, old[:30])
    if c == 1:
        t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("manual updated")
