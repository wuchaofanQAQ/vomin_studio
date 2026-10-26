# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\ai-drama-harness\references\data-contracts.md"
t = open(p, encoding="utf-8").read()

start = t.index("### 1c. 资产库")
end = t.index("## 3. 逐集资产提取")
new = '''### 1c. 资产库（唯一资产表，match key: `name`）

| JSON key | 飞书字段 | 说明 |
|---|---|---|
| `name` | 名称（主字段） | 资产名，锚点用它 |
| `kind` | 类型 | 角色 / 场景 / 道具 |
| `description` | 描述 | 一句可见描述（≤50 字） |
| `id` | ID | 数字，建表时分配 |
| `file_path` | 文件路径 | 出图后回填 |

```json
{"name": "陈诚", "kind": "角色", "description": "20岁男生，黑色微卷中长发，白T黑短裤，眉峰压低。"}
```

**锚点语法只有一种**：`{资产库：陈诚}`（角色/场景/道具共用，不再有 `{角色库：…}` 这类写法）。

下游按 `kind` 分流：分镜里角色走表演/可见性规则，场景走空间一致性，道具走外观一致性。

## 2. 资产出图（drama-asset-generation → 资产库）

`generate --target 资产库:名` 按 **类型** 自动选模板：

| 类型 | 模板 | 画面比例 |
|---|---|---|
| 角色 | 四视角设定图（近景正/侧 + 全身正/背） | 16:9 |
| 场景 | 场景资料图 | 22:9 |
| 道具 | 双视角图（正偏侧 + 正面） | 16:9 |

提示词由 `描述` + 模板自动拼，**不写进表**；出图后回填 `文件路径`。

'''
t = t[:start] + new + t[end:]
open(p, "w", encoding="utf-8").write(t)
print("data-contracts 已重写 1c / 2")
