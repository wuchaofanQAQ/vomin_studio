# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-initializer\SKILL.md"
lines = open(p, encoding="utf-8").read().splitlines()

# 找到 角色库 数组结束行 "  ],"
i = next(k for k, l in enumerate(lines) if l.strip() == '"角色库": [')
j = next(k for k in range(i, len(lines)) if lines[k] == "  ],")
# 后面紧跟的多余对象：从 j+1 的 "    {" 开始，到下一个单独 "  ]" 之前
k = j + 1
while lines[k].strip() != "{":
    k += 1
m = next(x for x in range(k, len(lines)) if lines[x] == "  ]")
new = lines[:j] + ["  ]"] + lines[m + 1:]
open(p, "w", encoding="utf-8").write("\n".join(new) + "\n")
print("删除行:", m - k + 1)
