# -*- coding: utf-8 -*-
p = r"skills\novel-to-drama\SKILL.md"
t = open(p, encoding="utf-8").read()

t = t.replace('''3. **原文逐字留存**：`novel_text` 放该章原文全文，不缩写、不润色、不纠错字；`novel_chapter` 放章节号与章名。''',
'''3. **原文逐字留存**：`novel_text` 放该章原文全文，不缩写、不润色、不纠错字；`novel_chapter` 放章节号与章名。
4. **小说逐句有落点**：引号里的每句台词逐字进剧本（对白或 OS）；心理活动、判断、动机句必须落成 OS 或可见动作；只有纯环境/外貌描写可以压缩，压缩后信息不能丢。**不许"概括掉"人物为什么这么做的句子。**''')

t = t.replace('''4. **不臆造**：原文没有的设定不补；必须补的过渡动作/场景用【补】标注，列入说明。
5. **只产出草案，绝不擅自写飞书**：先在对话中展示，用户明确确认后才由 harness 执行 `write`。用户提意见时只改草案。''',
'''5. **不臆造**：原文没有的设定不补；必须补的过渡动作/场景用【补】标注，列入说明。
6. **只产出草案，绝不擅自写飞书**：先在对话中展示，用户明确确认后才由 harness 执行 `write`。用户提意见时只改草案。''')

t = t.replace('''- 对白保留原话精神，口语化、短促；`角色：台词` 顶格，全角冒号''',
'''- **对白逐字**：小说引号里的台词原样进剧本，不改写、不合并、不概括；口语化只用于把叙述转成台词时，不用于已有台词；`角色：台词` 顶格，全角冒号
- **心理句不丢**：小说里带判断/动机/信息差的句子（心想、觉得、明白、凭什么、要是、真会…），落成 `角色（OS）：…` 或一个可拍动作；删之前先问"删了观众会不会少一个为什么"
- **压缩只压描写**：天气、街景、重复的形容可以压缩；人物的选择、误解、算计、关系变化不许压''')

t = t.replace('''- 节奏：开场 1~2 个场内进入冲突，结尾落在钩子上；密度指标见 `references/adaptation-rules.md` 十二（单集 1500~2500 字 / 可拆节拍 ≥40 / 台词 8~30），交付前用 `python skills/novel-to-drama/scripts/check_script.py <剧本.md>` 跑一遍''',
'''- 节奏：开场 1~2 个场内进入冲突，结尾落在钩子上；密度指标见 `references/adaptation-rules.md` 十二（单集 1500~2500 字 / 可拆节拍 ≥40 / 台词 8~30）
- 交付前两把尺子都要过：`check_script.py`（格式/节奏）+ `check_coverage.py`（小说逐句落点）''')

t = t.replace('''| **格式合规** | 抬头、四要素场头、人物行、△ 动作行、`角色：台词`、`（本集完）` 全部符合 `script-format.md`；`check_script.py` 的"格式错误"必须为 0 |''',
'''| **格式合规** | 抬头、四要素场头、人物行、△ 动作行、`角色：台词`、`（本集完）` 全部符合 `script-format.md`；`check_script.py` 的"格式错误"必须为 0 |
| **台词零丢失** | 小说引号台词全部进剧本（`check_coverage.py` 的「台词没进剧本」必须为空） |
| **心理句零丢失** | 判定/动机/信息差句全部有落点（`check_coverage.py` 的「硬问题」必须为 0；确需删的写进删减清单） |''')

t = t.replace('''> **机器校验是硬门槛**：交付前必须跑
> ```bash
> python skills/novel-to-drama/scripts/check_script.py workspace/{剧名}/drafts/ep01_script.md
> ```
> 任何一项 ✗ 都不许交付，也不许写飞书。''',
'''> **机器校验是硬门槛**：交付前必须跑
> ```bash
> python skills/novel-to-drama/scripts/check_script.py workspace/{剧名}/drafts/ep01_script.md
> python skills/novel-to-drama/scripts/check_coverage.py workspace/{剧名}/drafts/ep01_row.json workspace/{剧名}/drafts/ep01_script.md
> ```
> `check_coverage.py` 的第一个参数可以是小说 txt，也可以是 `cli.py read` 出来的剧本表 JSON（取该集 `novel_text`）。
> 「台词没进剧本」和「硬问题」都必须为 0；「建议复核」逐条决定保留或删，删的写进交付说明。
> 任何一项 ✗ 都不许交付，也不许写飞书。''')

t = t.replace('''输出：①剧本全文 ②字段摘要 ③说明（【补】项清单、新角色清单、场景名归一化对照表、无钩子警示、章节体量提示）。''',
'''输出：①剧本全文 ②字段摘要 ③说明（【补】项清单、新角色清单、场景名归一化对照表、无钩子警示、章节体量提示、**删减清单**：哪句没进、为什么）。

> 删减清单是交付的一部分：每一句被判"压缩/删除"的小说原文都要写一句理由（纯描写/重复/无法拍摄/合并进某句 OS）。没有清单的稿子视为静默丢失。''')

open(p, "w", encoding="utf-8").write(t)
print("SKILL updated")
