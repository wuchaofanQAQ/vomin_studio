# -*- coding: utf-8 -*-
p = r"CLAUDE.md"
t = open(p, encoding="utf-8").read()
t = t.replace("本项目是 AI 短剧生产流水线：8 个 skill", "本项目是 AI 短剧生产流水线：7 个 skill")
t = t.replace("| 抽资产、抽角色、抽场景、抽道具、资产图提示词、补角色档案 |",
              "| 抽资产、抽角色、抽场景、抽道具、资产描述 |")
open(p, "w", encoding="utf-8").write(t)
print("CLAUDE count fixed")
