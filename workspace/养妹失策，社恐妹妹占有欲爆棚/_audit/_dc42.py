# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()

t = t.replace("`drama-segment-generation`（剧本转提示词 3.0）一次产出分段提示词 + 依赖清单 + 资产编号表：",
              "`drama-segment-generation`（剧本转提示词 4.2）一次产出分段提示词 + 依赖清单 + 资产绑定表：")

old_prompt = "【第05段｜00:00-00:30｜大殿质问】\\n\\n【资产锁定】\\n【参考图映射】图1=S01隋朝皇宫大殿；图2=R01杨广；图3=R02姜颜\\n场景：【S01｜隋朝皇宫大殿：{场景库：隋朝皇宫大殿}】\\n角色：【R01｜杨广：{角色库：杨广 中年版}】【R02｜姜颜：{角色库：姜颜}】\\n\\n【本段风格】……\\n【本段初始空间基准】……\\n\\n【镜头01｜00:00-00:02｜抬眼】\\n近景固定机位，R01杨广位于画面中央……落幅停在他的眼睛。\\n【对白 00:00.5-00:02】R01杨广（压着怒气、缓慢地说）：人有南北，国有南北吗？"
new_prompt = "【第05段｜00:00-00:30｜隋朝皇宫大殿·质问】\\n\\n【本段资产锁定】\\n【参考图映射】图1=S01隋朝皇宫大殿；图2=R01杨广；图3=R02姜颜\\n场景：【S01｜隋朝皇宫大殿：{场景库：隋朝皇宫大殿}】\\n角色：【R01｜杨广：{角色库：杨广 中年版}】【R02｜姜颜：{角色库：姜颜}】\\n待补：【P03｜玉玺：待补，未读取】\\n\\n【本段整体基准】……\\n【本段初始空间】……\\n\\n【镜头01｜00:00-00:02｜抬眼】\\n近景固定机位，R01杨广位于画面中央……落幅停在他的眼睛。\\n【对白 00:00.5-00:02】R01杨广（压着怒气、缓慢地说）：『人有南北，国有南北吗？』\\n\\n【本段终态】……"
assert t.count(old_prompt) == 1, t.count(old_prompt)
t = t.replace(old_prompt, new_prompt)

old_deps = '''    "props": ["行李箱"],
    "new_scenes": [],
    "new_characters": [],'''
new_deps = '''    "props": ["行李箱"],
    "missing": [{"type": "道具", "name": "玉玺", "reason": "库里没有，标待补"}],
    "pending_images": [{"type": "场景", "name": "陈诚童年家厨房（日）"}],
    "new_scenes": [],
    "new_characters": [],'''
assert t.count(old_deps) == 1
t = t.replace(old_deps, new_deps)
open(p, "w", encoding="utf-8").write(t)
print("data-contracts updated")
