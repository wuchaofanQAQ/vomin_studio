# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-asset-extraction\SKILL.md"
t = open(p, encoding="utf-8").read()
old = "--table 剧本表 --episode N --with-novel"
new = "--table 小说表"
if old in t:
    t = t.replace(old, new)
    # 顺带把注释改成小说原文
    t = t.replace("--table 小说表    # 仅当前集：小说内容（原文）", "--table 小说表    # 小说原文（按对应原小说章节取用）")
    open(p, "w", encoding="utf-8").write(t)
    print("已更新")
else:
    print("未找到 --with-novel 行")
print([l for l in t.splitlines() if "--table" in l and ("剧本表" in l or "小说表" in l)][:4])
