# -*- coding: utf-8 -*-
p = r"vomin\workspace.py"
t = open(p, encoding="utf-8").read()
old = '''        text = re.sub(r"：\\s*】", "】", text)'''
new = '''        text = re.sub(r"：\\s*】", "】", text)
        # 锚点后还有补充内容时，收掉挂在末尾的逗号/顿号：`…硬壳，】` → `…硬壳】`
        text = re.sub(r"[，、；;]\\s*】", "】", text)'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("cleanup patched")
