# -*- coding: utf-8 -*-
import re
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

# 1) 字幕行去【】
out = []
for ln in s.splitlines():
    if ln.startswith("（字幕"):
        ln = ln.replace("【", "").replace("】", "")
    out.append(ln)
s = "\n".join(out)

# 2) 每段补齐缺的锁定项
parts = re.split(r"(?m)^## (【第\d+段.*?】)\s*$", s)
res = [parts[0]]
for i in range(1, len(parts), 2):
    head, body = parts[i], parts[i+1]
    lock_end = body.index("【本段现场生成】")
    lock, rest = body[:lock_end], body[lock_end:]
    if "【黑拖鞋】" in rest and "【黑拖鞋】" not in lock:
        lock = lock.rstrip("\n") + "\n待出图：【黑拖鞋】\n\n"
    if "【手机】" in rest and "【手机】：" not in lock:
        lock = lock.rstrip("\n") + "\n【手机】：{道具库：手机}\n\n"
    res += [head, lock + rest]
s = res[0] + "".join("## " + h + "\n" + b for h, b in zip(res[1::2], res[2::2]))
open(f, "w", encoding="utf-8").write(s)
print("locks patched")
