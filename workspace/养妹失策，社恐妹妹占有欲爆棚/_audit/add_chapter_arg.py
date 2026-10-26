# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
t = open(p, encoding="utf-8").read()

# 1) read 命令加 --chapter
old = '''    p_read.add_argument("--with-novel"'''
if old in t:
    print("--with-novel 已不存在，跳过")
else:
    # 在 read 的 --episode 后加
    m = re.search(r'(    p_read\.add_argument\("--episode".*?\n)', t, re.S)
    assert m, "找不到 p_read --episode"
    add = '    p_read.add_argument("--chapter", help="小说表专用：只读指定章节，逗号分隔，如 1,2")\n'
    t = t[:m.end()] + add + t[m.end():]

# 2) cmd_read 里做过滤
anchor = '''    # 剧本表默认剔除小说原文'''
add2 = '''    # 小说表：只读 对应原小说章节 里列出的章节
    if table == "小说表" and getattr(args, "chapter", None):
        want = {x.strip() for x in re.split(r"[,，、\\s]+", str(args.chapter)) if x.strip()}
        data = [r for r in data if str(r.get("章节", "")).strip() in want]
        print(f"[过滤] 仅章节 {sorted(want)}（实际 {len(data)} 条）", file=sys.stderr)

'''
assert t.count(anchor) == 1
t = t.replace(anchor, add2 + anchor)
open(p, "w", encoding="utf-8").write(t)
print("cli 已加 --chapter")
