# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()
old = '''    def _row_key(r):
        return r.get(mk)'''
new = '''    def _row_key(r):
        v = r.get(mk)
        if mk == "episode":
            # 剧本表集数在飞书是文本字段，本地/入参可能是数字，统一成 "1" 再比对
            try:
                return str(int(float(v)))
            except (TypeError, ValueError):
                return str(v) if v not in (None, "") else None
        return v'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)

p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
old2 = '''        for ep in episodes:
            fields = {
                "集数": ep.get("episode", ""),'''
new2 = '''        for ep in episodes:
            try:
                ep_key = str(int(float(ep.get("episode"))))
            except (TypeError, ValueError):
                ep_key = str(ep.get("episode", ""))
            fields = {
                "集数": ep_key,'''
assert t.count(old2) == 1
t = t.replace(old2, new2)
old3 = '''            record_id = ep_to_record.get(ep["episode"])'''
new3 = '''            record_id = ep_to_record.get(ep_key) or ep_to_record.get(str(ep.get("episode")))'''
assert t.count(old3) == 1
t = t.replace(old3, new3)
open(p, "w", encoding="utf-8").write(t)
print("episode key normalized")
