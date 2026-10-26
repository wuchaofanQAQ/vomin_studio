# -*- coding: utf-8 -*-
import re

# ---------- CLI 分发 ----------
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()
pairs = [
('        "剧本表": ws.load_episodes,\n', '        "剧本表": ws.load_episodes, "资产库": ws.load_assets_lib,\n'),
('"剧本表": "episode", "小说表": "章节",', '"剧本表": "episode", "小说表": "章节", "资产库": "name",'),
('        "剧本表": "episodes.json",\n', '        "剧本表": "episodes.json", "资产库": "assets_lib.json",\n'),
('            "剧本表": "push_episodes",\n', '            "剧本表": "push_episodes", "资产库": "push_assets_lib",\n'),
]
for a, b in pairs:
    assert c.count(a) == 1, a[:40]
    c = c.replace(a, b)

# pull 里补一段
anchor = '    print("\\n[小说表]")'
add = '''    print("\\n[资产库]")
    try:
        alib = ws.feishu.pull_assets_lib(ws)
        print(f"  {len(alib)} 条资产")
    except Exception as e:
        print(f"  跳过资产库: {e}")
'''
assert c.count(anchor) == 1
c = c.replace(anchor, add + anchor)
open(p, "w", encoding="utf-8").write(c)
print("cli: 资产库 read/write/pull 已接")

# ---------- 分镜锚点切换到资产库 ----------
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()
s = s.replace("{角色库：", "{资产库：").replace("{场景库：", "{资产库：").replace("{道具库：", "{资产库：")
open(f, "w", encoding="utf-8").write(s)
print("storyboard anchors -> 资产库")
