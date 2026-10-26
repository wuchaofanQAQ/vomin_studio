# -*- coding: utf-8 -*-
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

# 1) TABLE_SCHEMA 新增道具库（插在 素材库 之前）
anchor = '        "素材库": {\n            "primary_rename": "素材ID",'
schema = '''        "道具库": {
            "primary_rename": "道具ID",
            "fields": [
                {"field_name": "道具名", "type": 1},
                {"field_name": "道具类型", "type": 3, "property": {"options": [
                    {"name": "关键信物"}, {"name": "手持道具"}, {"name": "陈设道具"},
                    {"name": "食物饮品"}, {"name": "服装配饰"}, {"name": "武器工具"},
                    {"name": "电子设备"}, {"name": "其他"},
                ]}},
                {"field_name": "道具描述", "type": 1},
                {"field_name": "关联集数", "type": 1},
                {"field_name": "来源", "type": 3, "property": {"options": [
                    {"name": "原始采集"}, {"name": "AIGC生成"}, {"name": "手动制作"},
                ]}},
                {"field_name": "生成提示词", "type": 1},
                {"field_name": "负向提示词", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "生成模型", "type": 1},
                {"field_name": "出图状态", "type": 3, "property": {"options": [
                    {"name": "待出图"}, {"name": "生成中"}, {"name": "已出图"},
                    {"name": "需重抽"}, {"name": "已通过"},
                ]}},
            ],
        },
        "素材库": {
            "primary_rename": "素材ID",'''
assert t.count(anchor) == 1
t = t.replace(anchor, schema)

# 2) pull_props（插在 update_character 之前）
anchor2 = '    def update_character(self, ws, char: dict):'
pull = '''    def pull_props(self, ws) -> list[dict]:
        """从飞书道具库拉取到本地 props.json，返回道具列表。"""
        table_id = self._table_id(ws, "道具库", "FEISHU_TABLE_PROP")
        if not table_id:
            return ws.load_json("props.json")

        records = self.list_records(table_id)
        props = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("道具ID"))
            if not name:
                continue
            props.append({
                "name": name,
                "prop_type": _text_val(f.get("道具类型", "")),
                "description": _text_val(f.get("道具描述", "")),
                "related_episodes": _text_val(f.get("关联集数", "")),
                "ref_image": _text_val(f.get("文件路径")) or None,
                "gen_prompt": _text_val(f.get("生成提示词", "")),
                "negative_prompt": _text_val(f.get("负向提示词", "")),
                "gen_model": _text_val(f.get("生成模型")) or None,
                "gen_status": _text_val(f.get("出图状态", "")) or "待出图",
                "source": _text_val(f.get("来源", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("props.json", props)
        return props

    def update_character(self, ws, char: dict):'''
assert t.count(anchor2) == 1
t = t.replace(anchor2, pull)

# 3) update_prop（插在 update_shot 之前）
anchor3 = '    def update_shot(self, ws, shot: dict):'
upd = '''    def update_prop(self, ws, prop: dict):
        """更新飞书道具库中的单条记录。prop 必须含 _record_id。"""
        table_id = self._table_id(ws, "道具库", "FEISHU_TABLE_PROP")
        record_id = prop.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "道具ID": prop.get("name", ""),
            "道具类型": prop.get("prop_type", ""),
            "道具描述": prop.get("description", ""),
            "关联集数": prop.get("related_episodes", ""),
            "来源": prop.get("source", ""),
            "生成提示词": prop.get("gen_prompt", ""),
            "负向提示词": prop.get("negative_prompt", ""),
            "文件路径": prop.get("ref_image") or "",
            "生成模型": prop.get("gen_model") or "",
            "出图状态": prop.get("gen_status", "待出图"),
        }
        self.update_record(table_id, record_id, fields)

    def update_shot(self, ws, shot: dict):'''
assert t.count(anchor3) == 1
t = t.replace(anchor3, upd)

# 4) push_props（插在 push_settings 之前）
anchor4 = '    def push_settings(self, ws):'
push = '''    def push_props(self, ws):
        """把本地 props.json 同步到飞书道具库。一个道具一行，道具ID 即道具名。"""
        table_id = self._table_id(ws, "道具库", "FEISHU_TABLE_PROP")
        if not table_id:
            print("  未配置道具库，跳过")
            return

        props = ws.load_json("props.json")
        if not props:
            print("  本地无道具数据")
            return

        existing = self.list_records(table_id)
        key_to_record = {}
        for rec in existing:
            f = rec.get("fields", {})
            name = _text_val(f.get("道具ID"))
            if name:
                key_to_record[name] = rec["record_id"]

        for pr in props:
            label = pr["name"]
            fields = {
                "道具ID": label,
                "道具类型": pr.get("prop_type", "") or "其他",
                "道具描述": pr.get("description", ""),
                "关联集数": pr.get("related_episodes", ""),
                "来源": pr.get("source") or ("AIGC生成" if pr.get("gen_prompt") else "原始采集"),
                "生成提示词": pr.get("gen_prompt", ""),
                "负向提示词": pr.get("negative_prompt", ""),
                "文件路径": pr.get("ref_image") or "",
                "生成模型": pr.get("gen_model", ""),
                "出图状态": pr.get("gen_status", "待出图"),
            }
            record_id = key_to_record.get(label)
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新道具: {label}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建道具: {label}")

    def push_settings(self, ws):'''
assert t.count(anchor4) == 1
t = t.replace(anchor4, push)

open(p, "w", encoding="utf-8").write(t)
print("bitable.py patched")
