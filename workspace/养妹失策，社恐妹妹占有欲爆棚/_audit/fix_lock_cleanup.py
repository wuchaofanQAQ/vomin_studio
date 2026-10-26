# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
t = open(p, encoding="utf-8").read()
old = '''        text = re.sub(r"[，、；;]\\s*】", "】", text)'''
new = '''        text = re.sub(r"[，、；;]\\s*】", "】", text)
        # 名称版锁定行「【名】：{…}」去掉锚点后会剩一个空冒号，收掉：`【沈幼怡】：` → `【沈幼怡】`
        text = re.sub(r"(?m)^(【[^】]+】)\\s*(?:画面参考\\s*[：:])?\\s*[：:]\\s*$", r"\\1", text)'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("expand_prompt cleanup patched")
