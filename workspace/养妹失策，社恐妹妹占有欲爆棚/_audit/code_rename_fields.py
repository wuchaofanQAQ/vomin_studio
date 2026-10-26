# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

pairs = [
('                {"field_name": "人物锁定", "type": 1},\n                {"field_name": "环境锁定", "type": 1},\n', ''),
('            "primary_rename": "集数",', '            "primary_rename": "集号",'),
('                "人物锁定": shot.get("char_lock", ""),\n                "环境锁定": shot.get("env_lock", ""),\n', ''),
('                "char_lock": _text_val(f.get("人物锁定", "")),\n                "env_lock": _text_val(f.get("环境锁定", "")),\n', ''),
('            ep_num = _text_val(f.get("集数"))', '            ep_num = _text_val(f.get("集号"))'),
('"""把本地 episodes.json 同步到飞书剧本表。用集数做匹配键。"""', '"""把本地 episodes.json 同步到飞书剧本表。用集号做匹配键。"""'),
('            ep_num = _text_val(rec.get("fields", {}).get("集数"))', '            ep_num = _text_val(rec.get("fields", {}).get("集号"))'),
('                "集数": ep_key,', '                "集号": ep_key,'),
]
for a, b in pairs:
    c = t.count(a)
    print(c, a.strip()[:50])
    assert c == 1, a
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("bitable 已更新")
