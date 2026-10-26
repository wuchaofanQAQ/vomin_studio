# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()
t = t.replace("workspace/{剧名}/drafts/ep01_storyboard_v3.md", "workspace/{剧名}/drafts/ep01_storyboard_v4.md")
t = t.replace("剧本 → 按难度分段（30 秒上限）+ 依赖解析 + 导演级视频提示词（3.0 骨架：编号资产/融合镜头/台词带\"说\"）",
              "剧本 → 资产绑定 + 按难度分段（30 秒上限）+ 依赖解析 + 导演级视频提示词（4.2 骨架：待补标注/现场生成/整体基准/初始空间/终态）")
open(p, "w", encoding="utf-8").write(t)
print("harness v3 fixed")
