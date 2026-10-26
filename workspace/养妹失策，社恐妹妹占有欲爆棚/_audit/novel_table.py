# -*- coding: utf-8 -*-
# 1) 小说表 schema + pull/push
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

anchor = '''    TABLE_SCHEMA = {'''
add = '''    TABLE_SCHEMA = {
        "小说表": {
            "primary_rename": "章节",
            "fields": [
                {"field_name": "标题", "type": 1},
                {"field_name": "内容", "type": 1},
            ],
        },'''
assert t.count(anchor) == 1
t = t.replace(anchor, add)

# 在 pull_episodes 前插入小说表读写
old = "    def pull_episodes(self, ws) -> list[dict]:"
new = '''    # ------ 小说表 ------
    def _novel_table_id(self) -> str:
        cfg = getattr(self, "table_map", {}) or {}
        tid = cfg.get("小说表", "")
        if not tid:
            tid = self.discover_tables().get("小说表", "")
        if not tid:
            raise RuntimeError("飞书表格中未找到「小说表」数据表")
        return tid

    def pull_novels(self, ws) -> list[dict]:
        tid = self._novel_table_id()
        rows = []
        for r in self.list_records(tid):
            f = r.get("fields", {})
            rows.append({
                "章节": self._text_val(f.get("章节")),
                "标题": self._text_val(f.get("标题")),
                "内容": self._text_val(f.get("内容")),
            })
        ws.save_json("novels.json", rows)
        return rows

    def push_novels(self, ws):
        tid = self._novel_table_id()
        existing = {}
        for r in self.list_records(tid):
            key = self._text_val(r.get("fields", {}).get("章节"))
            if key:
                existing[key] = r["record_id"]
        for row in ws.load_json("novels.json"):
            fields = {
                "章节": row.get("章节", ""),
                "标题": row.get("标题", ""),
                "内容": row.get("内容", ""),
            }
            key = str(fields["章节"])
            if key in existing:
                self.update_record(tid, existing[key], fields)
            else:
                self.create_record(tid, fields)
        print(f"  小说表已同步: {len(ws.load_json('novels.json'))} 章")

    def pull_episodes(self, ws) -> list[dict]:'''
assert t.count(old) == 1
t = t.replace(old, new, 1)
open(p, "w", encoding="utf-8").write(t)
print("bitable: 小说表 added")

# 2) cli: read / write / pull 分发
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p2, encoding="utf-8").read()
c = c.replace('''        "剧本表": ws.load_episodes, "角色档案": ws.load_character_bibles,
    }''', '''        "剧本表": ws.load_episodes, "角色档案": ws.load_character_bibles,
        "小说表": lambda: ws.load_json("novels.json"),
    }''')
c = c.replace('''        "剧本表": "episode", "角色档案": "name",
    }''', '''        "剧本表": "episode", "角色档案": "name", "小说表": "章节",
    }''')
c = c.replace('''        "剧本表": "episodes.json", "角色档案": "character_bibles.json",
    }''', '''        "剧本表": "episodes.json", "角色档案": "character_bibles.json",
        "小说表": "novels.json",
    }''')
c = c.replace('''            "剧本表": "push_episodes", "角色档案": "push_character_bibles",
        }''', '''            "剧本表": "push_episodes", "角色档案": "push_character_bibles",
            "小说表": "push_novels",
        }''')
c = c.replace('''    print("\\n[生图工作台]")
    tasks = ws.feishu.pull_workbench(ws)
    print(f"  {len(tasks)} 条任务")''', '''    print("\\n[生图工作台]")
    tasks = ws.feishu.pull_workbench(ws)
    print(f"  {len(tasks)} 条任务")
    try:
        print("\\n[小说表]")
        novels = ws.feishu.pull_novels(ws)
        print(f"  {len(novels)} 章")
    except Exception as e:
        print(f"  跳过小说表: {e}")''')
open(p2, "w", encoding="utf-8").write(c)
print("cli: 小说表 dispatch added")
