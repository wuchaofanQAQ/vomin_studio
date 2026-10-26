# -*- coding: utf-8 -*-
import re

# ---------- 1) bitable: 资产库 读写 ----------
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

if '"资产库": {' not in t:
    anchor = '        "系统设置": {'
    schema = '''        "资产库": {
            "primary_rename": "名称",
            "fields": [
                {"field_name": "ID", "type": 2},
                {"field_name": "类型", "type": 3, "property": {"options": [
                    {"name": "角色"}, {"name": "场景"}, {"name": "道具"},
                ]}},
                {"field_name": "描述", "type": 1},
                {"field_name": "文件路径", "type": 1},
            ],
        },
'''
    assert t.count(anchor) == 1
    t = t.replace(anchor, schema + anchor)

if "def pull_assets_lib" not in t:
    anchor2 = "    def pull_voices(self, ws) -> list[dict]:"
    funcs = '''    def pull_assets_lib(self, ws) -> list[dict]:
        """从飞书资产库拉取到本地 assets_lib.json。"""
        table_id = self._table_id(ws, "资产库", "FEISHU_TABLE_ASSET_LIB")
        if not table_id:
            return ws.load_json("assets_lib.json")
        rows = []
        for rec in self.list_records(table_id):
            f = rec.get("fields", {})
            nm = _text_val(f.get("名称"))
            if not nm:
                continue
            idv = f.get("ID")
            try:
                idv = int(idv) if idv is not None else None
            except (TypeError, ValueError):
                idv = None
            rows.append({
                "id": idv,
                "name": nm,
                "kind": _text_val(f.get("类型", "")),
                "description": _text_val(f.get("描述", "")),
                "file_path": _text_val(f.get("文件路径", "")),
                "_record_id": rec["record_id"],
            })
        rows.sort(key=lambda x: (x["id"] is None, x["id"]))
        ws.save_json("assets_lib.json", rows)
        return rows

    def push_assets_lib(self, ws):
        """把本地 assets_lib.json 同步到飞书资产库。用名称做匹配键。"""
        table_id = self._table_id(ws, "资产库", "FEISHU_TABLE_ASSET_LIB")
        if not table_id:
            print("  未配置资产库，跳过")
            return
        rows = ws.load_json("assets_lib.json")
        existing = {}
        for rec in self.list_records(table_id):
            nm = _text_val(rec.get("fields", {}).get("名称"))
            if nm:
                existing[nm] = rec["record_id"]
        for a in rows:
            fields = {
                "名称": a.get("name", ""),
                "ID": a.get("id"),
                "类型": a.get("kind", ""),
                "描述": a.get("description", ""),
                "文件路径": a.get("file_path", ""),
            }
            rid = existing.get(a["name"])
            if rid:
                self.update_record(table_id, rid, fields)
            else:
                self.create_record(table_id, fields)
        print(f"  资产库已同步 {len(rows)} 条")

'''
    assert t.count(anchor2) == 1
    t = t.replace(anchor2, funcs + anchor2)

open(p, "w", encoding="utf-8").write(t)
print("bitable: 资产库 schema + pull/push")

# ---------- 2) workspace: loader + REF ----------
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
w = open(p2, encoding="utf-8").read()

if "def load_assets_lib" not in w:
    anchor3 = "    def load_settings(self) -> list[dict]:"
    add = '''    def load_assets_lib(self) -> list[dict]:
        return self._load_from_feishu("assets_lib", "pull_assets_lib", "assets_lib.json")

'''
    assert w.count(anchor3) == 1
    w = w.replace(anchor3, add + anchor3)

if '"资产库": ("load_assets_lib"' not in w:
    anchor4 = '        "角色库": ("load_characters", "name", ["ref_image"]),'
    w = w.replace(anchor4, '        "资产库": ("load_assets_lib", "名称", ["file_path"]),\n' + anchor4)

open(p2, "w", encoding="utf-8").write(w)
print("workspace: load_assets_lib + REF_SHEETS")
