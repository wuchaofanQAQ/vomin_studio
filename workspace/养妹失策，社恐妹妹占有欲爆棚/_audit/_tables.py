# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()
old = '''| 抽场景 | "剧本抽场景 / 场景图提示词 / 这场戏有哪些空间" | script-to-scene-assets |
| 逐集新角色识别 | "抽角色 / 新角色识别 / 补角色档案" | novel-to-character-assets |'''
new = '''| 逐集资产提取 | "抽资产 / 抽角色 / 抽场景 / 抽道具 / 资产图提示词 / 补角色档案" | script-asset-extraction |'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("manual skill table updated")

# CLAUDE.md 两行并一行
p = r"CLAUDE.md"
t = open(p, encoding="utf-8").read()
old = '''| script-to-scene-assets | `skills/script-to-scene-assets/SKILL.md` | 剧本抽场景、场景图提示词、母版/主场景/局部、图间关联 |'''
new = '''| script-asset-extraction | `skills/script-asset-extraction/SKILL.md` | 抽资产、抽角色、抽场景、抽道具、资产图提示词、补角色档案 |'''
assert t.count(old) == 1
t = t.replace(old, new)
old2 = '''| novel-to-character-assets | `skills/novel-to-character-assets/SKILL.md` | 小说抽角色、新角色识别、补角色档案 |\n'''
assert t.count(old2) == 1
t = t.replace(old2, "")
open(p, "w", encoding="utf-8").write(t)
print("CLAUDE.md updated")
