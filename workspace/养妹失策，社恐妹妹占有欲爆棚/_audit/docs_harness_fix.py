# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\ai-drama-harness\SKILL.md"
t = open(p, encoding="utf-8").read()

pairs = [
("""     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     python cli.py write $WS --table 资产库   --data '<资产库部分>'""",
 """     python cli.py write $WS --table 剧本设定 --data '<JSON>'
     python cli.py write $WS --table 资产库   --data '[{"name":"陈诚","kind":"角色","description":"..."}, ...]'"""),

("""1. 调用 `drama-asset-generation` skill，为每个核心角色写四视角设定图提示词（草案）
2. 向用户展示提示词草案与"将要写入 gen_prompt + 触发 N 个角色出图"的清单，**确认后**：
   ```bash
   python cli.py write $WS --table 资产库 --data '[{"name":"林砚","gen_prompt":"..."}]'
   python cli.py generate $WS --target 资产库:林砚
   ```""",
 """1. 调用 `drama-asset-generation` skill，按角色描述生成四视角设定图（提示词由 描述 + 模板自动拼，不写进表）
2. 向用户展示"将要写出图清单 + 触发 N 个角色出图"的清单，**确认后**：
   ```bash
   python cli.py write $WS --table 资产库 --data '[{"name":"林砚","kind":"角色","description":"..."}]'
   python cli.py generate $WS --target 资产库:林砚   # 类型=角色 → 自动走四视角模板
   ```"""),

("""   python cli.py write $WS --table 资产库 --data @characters.json
   python cli.py write $WS --table 资产库 --data @scenes.json
   python cli.py write $WS --table 资产库 --data @props.json""",
 """   python cli.py write $WS --table 资产库 --data @assets.json
   # 每行必须带 kind（角色/场景/道具），CLI 按 kind 落 类型 字段"""),

("""- **资产绑定表**：本集角色/场景/道具逐条对三张表（有图/无图/库里没有→待补），登记 `drafts/asset_ids.json`""",
 """- **资产绑定表**：本集角色/场景/道具逐条对「资产库」（按 类型 过滤；有图/无图/库里没有→待补），登记 `drafts/asset_ids.json`"""),
]
for a, b in pairs:
    assert t.count(a) == 1, a[:40]
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("harness 已修")
