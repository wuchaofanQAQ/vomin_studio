# -*- coding: utf-8 -*-
import sys, os, json, re, time, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

base = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
fb = ws.feishu
tables = ws.config["feishu"]["tables"]

# 1) 备份 + 删飞书表
tid = tables.get("角色档案")
if tid:
    recs = fb.list_records(tid)
    rows = []
    for r in recs:
        f = r.get("fields", {})
        rows.append({k: (v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)) for k, v in f.items()})
    path = os.path.join(base, "bak", f"角色档案_删除备份_{time.strftime('%Y%m%d_%H%M%S')}.json")
    json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("已备份角色档案", len(rows), "条 ->", os.path.basename(path))
    r = requests.delete(fb._api(f"bitable/v1/apps/{fb.app_token}/tables/{tid}"), headers=fb._headers())
    print("删除飞书表:", r.status_code, r.json().get("msg"))
    tables.pop("角色档案", None)
    ws.config["feishu"]["tables"] = tables
    ws.save_config()

# 2) bitable 代码
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()
t = re.sub(r'        "角色档案": \{.*?\n        \},\n(?=        "系统设置")', "", t, flags=re.S)
t = re.sub(r"    def pull_character_bibles\(self, ws\) -> list\[dict\]:.*?\n\n    def pull_scenes", "    def pull_scenes", t, flags=re.S)
t = re.sub(r"    def push_character_bibles\(self, ws\):.*?\n\n    def push_settings", "    def push_settings", t, flags=re.S)
open(p, "w", encoding="utf-8").write(t)
print("bitable: 已移除角色档案 schema/pull/push")

# 3) workspace
p2 = r"vomin\workspace.py"
w = open(p2, encoding="utf-8").read()
w = re.sub(r"    def load_character_bibles\(self\) -> list\[dict\]:.*?    def load_settings", "    def load_settings", w, flags=re.S)
w = w.replace('        "角色档案": ("load_character_bibles", "name", []),\n', "")
w = w.replace('        ws.save_json("character_bibles.json", [])\n', "")
open(p2, "w", encoding="utf-8").write(w)
print("workspace: 已移除角色档案读写")

# 4) cli
p3 = r"cli.py"
c = open(p3, encoding="utf-8").read()
c = c.replace('    print(f"  3. python cli.py write {ws.root} --table 角色档案 --data @bibles.json")\n', "")
c = c.replace('    bible_map = {b["name"]: b for b in ws.load_character_bibles()}\n',
              '    char_map = {x["name"]: x for x in ws.load_characters()}\n')
c = c.replace('            bible = bible_map.get(speaker_name)\n            if bible is None or not bible.get("voice_desc"):\n                print(f"  警告: 角色档案中找不到「{speaker_name}」的音色描述，使用默认音色")\n                bible = bible or {}\n            voice_desc = bible.get("voice_desc") or "青年，普通话标准"',
              '            voice_desc = (char_map.get(speaker_name) or {}).get("voice_desc") or "青年，普通话标准"')
c = c.replace('    print("\\n[角色档案]")\n    ws.feishu.push_character_bibles(ws)\n', "")
c = c.replace('    print("\\n[角色档案]")\n    bibles = ws.feishu.pull_character_bibles(ws)\n    print(f"  {len(bibles)} 份角色档案")\n', "")
c = c.replace('("pull_episodes", "剧本表"), ("pull_character_bibles", "角色档案"),', '("pull_episodes", "剧本表"),')
c = c.replace('"剧本表": "episode", "角色档案": "name", "小说表": "章节",', '"剧本表": "episode", "小说表": "章节",')
c = c.replace('        "剧本表": "episodes.json", "角色档案": "character_bibles.json",\n', '        "剧本表": "episodes.json",\n')
c = c.replace('            "剧本表": "push_episodes", "角色档案": "push_character_bibles",\n', '            "剧本表": "push_episodes",\n')
c = c.replace('        "剧本表": ws.load_episodes, "角色档案": ws.load_character_bibles,\n', '        "剧本表": ws.load_episodes,\n')
c = c.replace("角色库/角色档案/场景库", "角色库/场景库").replace("角色库/角色档案/", "角色库/")
open(p3, "w", encoding="utf-8").write(c)
print("cli: 已移除角色档案分发")

# 5) 本地缓存文件
cb = os.path.join(base, "character_bibles.json")
if os.path.exists(cb):
    os.rename(cb, os.path.join(base, "bak", f"character_bibles_删除备份_{time.strftime('%Y%m%d_%H%M%S')}.json"))
    print("本地 character_bibles.json 已移入 bak")
