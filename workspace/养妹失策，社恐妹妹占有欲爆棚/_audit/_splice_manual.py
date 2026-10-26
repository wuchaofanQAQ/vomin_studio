# -*- coding: utf-8 -*-
p = r"skills\AI短剧生产底座使用手册.md"
t = open(p, encoding="utf-8").read()
i = t.index("## 六、素材锚定语法")
j = t.index("## 七、CLI 命令速查")
new = open(r"workspace\养妹失策，社恐妹妹占有欲爆棚\_audit\_manual_section6.md", encoding="utf-8").read()
t = t[:i] + new + t[j:]
open(p, "w", encoding="utf-8").write(t)
print("manual section replaced")
