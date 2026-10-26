# -*- coding: utf-8 -*-
p = r"skills\script-asset-extraction\SKILL.md"
t = open(p, encoding="utf-8").read()

reps = [
("4. **复用优先**：库里同名且有图 → 直接复用，不改写描述；需求变了（光线/陈设/状态）→ 用新名新建，不覆盖旧资产。",
 "4. **复用优先、幂等写入**：库里同名且有图 → 直接复用，不改写描述、不重复插行；需求变了（光线/陈设/状态）→ 用新名新建，不覆盖旧资产。"),
("| 疑同一物但名字不同 | 先合并到已有名，在说明里写清；拿不准列\"待确认\" |",
 "| 疑同一物但名字不同 | 先合并到已有名，在说明里写清；拿不准列\"待确认\" |\n\n**幂等（多次调用）**：\n\n- 每次都先读 `角色库 / 场景库 / 道具库` 再判新建，**不能凭剧本直接出新资产**；\n- 名字归一后相同（去空格、半角括号统一成全角、英文小写）即视为**同一资产**，标 `复用`；\n- **复用项不写进写入 payload**（只用于交付清单）；CLI 也会跳过 `status=复用` 的行，但不要依赖它兜底；\n- 同一份输出里同名只能出现一次（校验器按归一化名字查重）；\n- 同名但确实变了（夜间/破损/换装）→ 新建带后缀的名字，这是新资产，不是重复。"),
("python skills/script-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json\n```\n\n脚本校验：字段齐全、同名唯一、场景名不含 `·`、描述 1~50 字且无【】分节、复用项有理由、待补项有说明。**任一 ✗ 不许交付。**",
 "python skills/script-asset-extraction/scripts/check_assets.py workspace/{剧名}/drafts/ep01_assets.json --library $WS\n```\n\n脚本校验：字段齐全、名字归一后唯一、场景名不含 `·`、描述 1~50 字且无【】分节、复用项有理由、待补项有说明；带 `--library` 时还会查幂等：**标新建但库里已有同名 → 报错**，标复用但库里没有 → 报错。**任一 ✗ 不许交付。**"),
("出图是 B1 之后的懒加载动作：只为本集 `dependencies` 用到的资产生成。**生成提示词字段留空**，CLI 用描述（+ 全局画风）出图；场景图出完必须过 `references/scene-consistency.md` 的一致性检查。",
 "**只写新建项**：复用项不要出现在 data 里。写入按 `name` upsert，同名不会新增行；`status=复用` 的行 CLI 会直接跳过。\n\n出图是 B1 之后的懒加载动作：只为本集 `dependencies` 用到的资产生成。**生成提示词字段留空**，CLI 用描述（+ 全局画风）出图；场景图出完必须过 `references/scene-consistency.md` 的一致性检查。"),
]
for old, new in reps:
    c = t.count(old)
    print(f"{c}  {old[:26]}")
    assert c == 1
    t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("skill idempotency documented")
