# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:26]}")
        if c == 1:
            t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\ai-drama-harness\references\data-contracts.md", [
("提示词里引用：`道具：【P01｜行李箱：24 寸硬壳，{道具库：行李箱}】`；带图道具要写进 `【参考图映射】`。**空表也能跑**——没有行的道具只写文字、不挂锚点。",
 "提示词里引用：`道具：【P01｜行李箱：24 寸硬壳，{道具库：行李箱}】`；带图道具要写进 `【参考图映射】`。**空表也能跑**——没有行的道具只写文字、不挂锚点。\n\n**幂等**：每次先读道具库，同名标 `复用`、不写进 payload；写入按 `道具ID` upsert，同名不会新增行。"),
])

rep(r"skills\AI短剧生产底座使用手册.md", [
("- 分镜和视频提示词由同一个技能一次完成",
 "- 资产提取可以重复跑：每次都先读三张资产表，同名标复用、不重复插行；写入只写新建项\n- 分镜和视频提示词由同一个技能一次完成"),
])
print("done")
