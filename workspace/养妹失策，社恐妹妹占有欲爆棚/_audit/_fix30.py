# -*- coding: utf-8 -*-
def rep(path, pairs, all_ok=False):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:40]}")
        t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\drama-segment-generation\references\project-adaptation.md", [
 ("【本段风格】", "【本段整体基准】"),
])
rep(r"skills\drama-segment-generation\references\shot-craft.md", [
 ("# 镜头工艺（3.0 实操）", "# 镜头工艺（4.2 实操）"),
])
rep(r"CLAUDE.md", [
 ("| 剧集分段、分段生成、剧本转提示词、3.0、拆分镜、分镜脚本、视频提示词、30秒分段 |",
  "| 剧集分段、分段生成、剧本转提示词、4.2、资产绑定、拆分镜、分镜脚本、视频提示词 |"),
])
print("done")
