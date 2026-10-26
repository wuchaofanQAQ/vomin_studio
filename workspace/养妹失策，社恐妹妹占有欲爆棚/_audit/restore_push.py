# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

anchor = "    def push_settings(self, ws):"
assert t.count(anchor) == 1
assert "def push_scenes" not in t and "def push_props" not in t

add = '''    def push_scenes(self, ws):
        """把本地 scenes.json 同步到飞书场景库。用场景名做匹配键。"""
        table_id = self._table_id(ws, "场景库", "FEISHU_TABLE_SCENE")
        if not table_id:
            print("  未配置场景库，跳过")
            return
        rows = ws.load_json("scenes.json")
        if not rows:
            print("  本地无场景数据")
            return
        existing = {}
        for rec in self.list_records(table_id):
            nm = _text_val(rec.get("fields", {}).get("场景ID"))
            if nm:
                existing[nm] = rec["record_id"]
        for s in rows:
            fields = {
                "场景ID": s.get("name", ""),
                "场景描述": s.get("description", ""),
                "参考场景": s.get("ref_scenes", ""),
                "作用关联": s.get("relation_note", ""),
                "关联集数": s.get("related_episodes", ""),
                "绑定场次": s.get("bind_scenes", ""),
                "来源": s.get("source", ""),
                "生成提示词": s.get("gen_prompt") or "",
                "负向提示词": s.get("negative_prompt", ""),
                "文件路径": s.get("ref_image") or "",
                "生成模型": s.get("gen_model") or "",
                "出图状态": s.get("gen_status") or "待出图",
                "一致性检查": s.get("consistency", "") or "未检查",
            }
            rid = existing.get(s["name"])
            if rid:
                self.update_record(table_id, rid, fields)
                print(f"  飞书更新场景: {s['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建场景: {s['name']}")

    def push_props(self, ws):
        """把本地 props.json 同步到飞书道具库。用道具名做匹配键。"""
        table_id = self._table_id(ws, "道具库", "FEISHU_TABLE_PROP")
        if not table_id:
            print("  未配置道具库，跳过")
            return
        rows = ws.load_json("props.json")
        if not rows:
            print("  本地无道具数据")
            return
        existing = {}
        for rec in self.list_records(table_id):
            nm = _text_val(rec.get("fields", {}).get("道具ID"))
            if nm:
                existing[nm] = rec["record_id"]
        for p_ in rows:
            fields = {
                "道具ID": p_.get("name", ""),
                "道具名": p_.get("name", ""),
                "道具类型": p_.get("prop_type", ""),
                "道具描述": p_.get("description", ""),
                "关联集数": p_.get("related_episodes", ""),
                "来源": p_.get("source", ""),
                "生成提示词": p_.get("gen_prompt") or "",
                "负向提示词": p_.get("negative_prompt", ""),
                "文件路径": p_.get("ref_image") or "",
                "生成模型": p_.get("gen_model") or "",
                "出图状态": p_.get("gen_status") or "待出图",
            }
            rid = existing.get(p_["name"])
            if rid:
                self.update_record(table_id, rid, fields)
                print(f"  飞书更新道具: {p_['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建道具: {p_['name']}")

'''
t = t.replace(anchor, add + anchor)
open(p, "w", encoding="utf-8").write(t)
print("restored push_scenes / push_props")
