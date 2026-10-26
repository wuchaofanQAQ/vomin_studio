# -*- coding: utf-8 -*-
p = r"skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()
anchor = "## 5. 分段分镜与视频提示词（script-to-prompt-30 → 剧本分镜表）"
section = '''## 4b. 道具库（2026-10 新增，可选表）

**用途**：存放反复出现、需要保持同一外观的道具（行李箱、蛋糕、粉色四件套、手机……）。不是每个道具都要入库——只收「跨镜头反复出现」或「需要单独出图」的。

**match key**：`name`（= `道具ID`，直接写道具名）

| 字段 | 说明 |
|---|---|
| 道具ID | 主键，= 道具名 |
| 道具名 | 与主键一致 |
| 道具类型 | 关键信物 / 手持道具 / 陈设道具 / 食物饮品 / 服装配饰 / 武器工具 / 电子设备 / 其他 |
| 道具描述 | 外形、材质、尺度、颜色、使用痕迹（只写看得见的） |
| 关联集数 | 如 `1,2` |
| 来源 | 原始采集 / AIGC生成 / 手动制作 |
| 生成提示词 | 出图用，可含 `{素材库：…}` 参考 |
| 负向提示词 | 可选 |
| 文件路径 | 出图后的相对路径（`ref/props/...`） |
| 生成模型 | 可选 |
| 出图状态 | 待出图 / 生成中 / 已出图 / 需重抽 / 已通过 |

```bash
# 写入（需确认；upsert，按道具名匹配）
python cli.py write $WS --table 道具库 --data '[{"name":"行李箱","prop_type":"手持道具","description":"24 寸硬壳，拉杆拉出三十厘米","related_episodes":"1","gen_prompt":"..."}]'

# 出图（花预算，需确认）
python cli.py generate --target 道具库:行李箱
```

提示词里引用：`道具：【P01｜行李箱：24 寸硬壳，{道具库：行李箱}】`；带图道具要写进 `【参考图映射】`。**空表也能跑**——没有行的道具只写文字、不挂锚点。

---

'''
assert t.count(anchor) == 1
t = t.replace(anchor, section + anchor)

# §5 harness 流程补道具差分
old = '''   - `new_characters` → 调对应 skill 补角色档案 + 三视图'''
new = '''   - `new_characters` → 调对应 skill 补角色档案 + 三视图
   - `props` / `new_props` → 差分比对道具库；缺的列入**待补道具**（可手工补录或 `generate --target 道具库:名`），不阻塞分镜评审'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("section added")
