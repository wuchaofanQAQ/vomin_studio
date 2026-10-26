# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
t = open(p, encoding="utf-8").read()

# 1) read: --with-novel → --chapter
old = '''    p_read.add_argument("--with-novel", action="store_true",
                        help="仅剧本表：同时输出「小说内容」原文（默认剔除，避免撑爆上下文）")'''
new = '''    p_read.add_argument("--chapter", default=None,
                        help="仅小说表：只读指定章节，逗号分隔，如 1,2")'''
assert t.count(old) == 1
t = t.replace(old, new)

# 2) 删掉那条按 with_novel 剔除小说原文的逻辑
old2 = '''    # 剧本表默认剔除小说原文：拆分镜/抽场景只需转化后的 script，读 N±1 三集小说原文会撑爆上下文
    if table == "剧本表" and not getattr(args, "with_novel", False):
        data = [{k: v for k, v in r.items() if k != "novel_text"} for r in data]

'''
assert t.count(old2) == 1
t = t.replace(old2, "")
open(p, "w", encoding="utf-8").write(t)
print("read 已改为 --chapter")
