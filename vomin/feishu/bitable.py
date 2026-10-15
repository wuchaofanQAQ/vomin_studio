import os
import time
import requests


class FeishuBitable:
    def __init__(self, app_id: str | None = None, app_secret: str | None = None,
                 app_token: str | None = None):
        self.app_id = app_id or os.environ.get("FEISHU_APP_ID", "")
        self.app_secret = app_secret or os.environ.get("FEISHU_APP_SECRET", "")
        self.app_token = app_token or os.environ.get("FEISHU_BITABLE_APP_TOKEN", "")
        self._token = None
        self._token_expire = 0

    def _get_token(self) -> str:
        if self._token and time.time() < self._token_expire:
            return self._token
        resp = requests.post(
            "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"飞书鉴权失败: {data.get('msg')}")
        self._token = data["tenant_access_token"]
        self._token_expire = time.time() + data.get("expire", 7200) - 60
        return self._token

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._get_token()}",
            "Content-Type": "application/json",
        }

    def _api(self, path: str) -> str:
        return f"https://open.feishu.cn/open-apis/{path.lstrip('/')}"

    def _base(self, table_id: str) -> str:
        return self._api(f"bitable/v1/apps/{self.app_token}/tables/{table_id}/records")

    # ------ 以下定义表结构常量供多处复用 ------
    TABLE_SCHEMA = {
        "剧本分镜表": {
            "primary_rename": "镜头标题",
            "fields": [
                {"field_name": "集号", "type": 2},
                {"field_name": "镜头编号", "type": 1},
                {"field_name": "台词", "type": 1},
                {"field_name": "镜头说明", "type": 1},
                {"field_name": "视频提示词", "type": 1},
                {"field_name": "人物锁定", "type": 1},
                {"field_name": "环境锁定", "type": 1},
                {"field_name": "时间线", "type": 1},
                {"field_name": "景别运镜", "type": 1},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待生成"}, {"name": "生成中"}, {"name": "待审核"},
                    {"name": "通过"}, {"name": "返工"}, {"name": "生成失败"},
                ]}},
                {"field_name": "配音路径", "type": 1},
                {"field_name": "视频路径", "type": 1},
                {"field_name": "任务ID", "type": 1},
                {"field_name": "审核备注", "type": 1},
            ],
        },
        "角色库": {
            "primary_rename": "角色ID",
            "fields": [
                {"field_name": "角色名", "type": 1},
                {"field_name": "角色类型", "type": 3, "property": {"options": [
                    {"name": "核心"}, {"name": "重要配角"}, {"name": "配角"}, {"name": "龙套"},
                ]}},
                {"field_name": "外貌描述", "type": 1},
                {"field_name": "音色描述", "type": 1},
                {"field_name": "音色Speaker", "type": 1},
                {"field_name": "来源", "type": 3, "property": {"options": [
                    {"name": "原始采集"}, {"name": "AIGC生成"}, {"name": "手动制作"},
                ]}},
                {"field_name": "生成提示词", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "生成模型", "type": 1},
            ],
        },
        "场景库": {
            "primary_rename": "场景ID",
            "fields": [
                {"field_name": "场景名", "type": 1},
                {"field_name": "场景类型", "type": 3, "property": {"options": [
                    {"name": "核心"}, {"name": "剧情"}, {"name": "临时"},
                ]}},
                {"field_name": "场景描述", "type": 1},
                {"field_name": "关联集数", "type": 1},
                {"field_name": "来源", "type": 3, "property": {"options": [
                    {"name": "原始采集"}, {"name": "AIGC生成"}, {"name": "手动制作"},
                ]}},
                {"field_name": "生成提示词", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "生成模型", "type": 1},
            ],
        },
        "素材库": {
            "primary_rename": "素材ID",
            "fields": [
                {"field_name": "文件路径", "type": 1},
                {"field_name": "素材类型", "type": 3, "property": {"options": [
                    {"name": "角色形象图"}, {"name": "场景参考图"}, {"name": "视频片段"},
                    {"name": "配音音频"}, {"name": "字幕"}, {"name": "原始素材"}, {"name": "BGM"},
                ]}},
                {"field_name": "生成模型", "type": 1},
                {"field_name": "生成参数", "type": 1},
                {"field_name": "生成时间", "type": 5},
                {"field_name": "来源", "type": 3, "property": {"options": [
                    {"name": "原始采集"}, {"name": "AIGC生成"}, {"name": "手动制作"},
                ]}},
                {"field_name": "备注", "type": 1},
                {"field_name": "生成提示词", "type": 1},
            ],
        },
        "剧本设定": {
            "primary_rename": "设定项",
            "fields": [
                {"field_name": "类别", "type": 3, "property": {"options": [
                    {"name": "核心设定"}, {"name": "全集大纲"}, {"name": "画面风格"}, {"name": "配置"},
                ]}},
                {"field_name": "设定值", "type": 1},
                {"field_name": "全局提示词", "type": 1},
                {"field_name": "全局参考图路径", "type": 1},
            ],
        },
        "剧集表": {
            "primary_rename": "集数",
            "fields": [
                {"field_name": "集名", "type": 1},
                {"field_name": "核心事件", "type": 1},
                {"field_name": "出场角色", "type": 1},
                {"field_name": "上集钩子", "type": 1},
                {"field_name": "结尾钩子", "type": 1},
                {"field_name": "场次列表", "type": 1},
                {"field_name": "完整剧本", "type": 1},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待编写"}, {"name": "草稿"}, {"name": "已确认"}, {"name": "已拆分镜"},
                ]}},
            ],
        },
        "生图工作台": {
            "primary_rename": "任务名",
            "fields": [
                {"field_name": "提示词", "type": 1},
                {"field_name": "模型", "type": 1},
                {"field_name": "分辨率", "type": 1},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待生成"}, {"name": "生成中"}, {"name": "已完成"}, {"name": "生成失败"},
                ]}},
                {"field_name": "结果路径", "type": 1},
                {"field_name": "备注", "type": 1},
            ],
        },
        "角色档案": {
            "primary_rename": "角色名",
            "fields": [
                {"field_name": "角色类型", "type": 3, "property": {"options": [
                    {"name": "核心"}, {"name": "重要配角"}, {"name": "配角"}, {"name": "龙套"},
                ]}},
                {"field_name": "基本信息", "type": 1},
                {"field_name": "风格描述", "type": 1},
                {"field_name": "音色描述", "type": 1},
                {"field_name": "外貌描述", "type": 1},
                {"field_name": "性格描述", "type": 1},
                {"field_name": "战斗描述", "type": 1},
                {"field_name": "标志性表达", "type": 1},
                {"field_name": "标注交接", "type": 1},
            ],
        },
    }

    EXPECTED_TABLES = list(TABLE_SCHEMA.keys())

    def discover_tables(self) -> dict[str, str]:
        """列出当前多维表格的所有数据表，返回 {表名: table_id} 映射。"""
        resp = requests.get(
            self._api(f"bitable/v1/apps/{self.app_token}/tables"),
            headers=self._headers(), timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"飞书获取表列表失败: {data.get('msg')}")
        items = data.get("data", {}).get("items", [])
        return {item["name"]: item["table_id"] for item in items}

    def ensure_tables(self, existing: dict[str, str]) -> dict[str, str]:
        """检查 6 张标准表是否齐全，缺失的自动创建。返回完整映射。"""
        h = self._headers()
        base = f"bitable/v1/apps/{self.app_token}"
        tables = dict(existing)
        for tname in self.EXPECTED_TABLES:
            if tname in tables:
                continue
            r = requests.post(self._api(f"{base}/tables"),
                              headers=h, json={"table": {"name": tname}}, timeout=15)
            r.raise_for_status()
            tid = r.json()["data"]["table_id"]
            tables[tname] = tid
            schema = self.TABLE_SCHEMA[tname]
            fields_resp = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h)
            for f in fields_resp.json().get("data", {}).get("items", []):
                if f.get("is_primary"):
                    requests.put(self._api(f"{base}/tables/{tid}/fields/{f['field_id']}"),
                                 headers=h,
                                 json={"field_name": schema["primary_rename"], "type": f["type"]})
                    break
            fields_resp = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h)
            for f in fields_resp.json().get("data", {}).get("items", []):
                if not f.get("is_primary"):
                    requests.delete(self._api(f"{base}/tables/{tid}/fields/{f['field_id']}"), headers=h)
            for field_def in schema["fields"]:
                requests.post(self._api(f"{base}/tables/{tid}/fields"), headers=h, json=field_def)
                import time
                time.sleep(0.1)
            print(f"  已创建缺失表: {tname}")
        return tables

    @staticmethod
    def parse_app_token(feishu_url: str) -> str:
        """从飞书多维表格 URL 中解析 app_token。"""
        import re
        m = re.search(r'/(?:base|wiki)/([A-Za-z0-9]+)', feishu_url)
        if not m:
            raise ValueError(f"无法从 URL 中解析飞书 app_token: {feishu_url}")
        return m.group(1)

    def create_project(self, drama_name: str) -> dict:
        """创建一个新项目的完整飞书多维表格（7 张表 + 全部字段 + 公开权限）。
        返回 {'app_token': ..., 'url': ..., 'tables': {'剧本分镜表': tid, ...}}"""
        h = self._headers()

        # 1. 创建多维表格
        resp = requests.post(
            self._api("bitable/v1/apps"),
            headers=h,
            json={"name": f"Vomin - {drama_name}", "folder_token": ""},
        )
        resp.raise_for_status()
        app_data = resp.json()["data"]["app"]
        app_token = app_data["app_token"]
        default_tid = app_data["default_table_id"]
        url = app_data["url"]
        self.app_token = app_token
        print(f"  飞书多维表格已创建: {url}")
        time.sleep(0.3)

        base = f"bitable/v1/apps/{app_token}"

        # 2. 重命名默认表 → 剧本分镜表
        requests.patch(self._api(f"{base}/tables/{default_tid}"),
                       headers=h, json={"name": "剧本分镜表"})
        tables = {"剧本分镜表": default_tid}

        # 创建其他表（从 EXPECTED_TABLES 动态取，排除已有的默认表）
        other_tables = [t for t in self.EXPECTED_TABLES if t != "剧本分镜表"]
        for name in other_tables:
            r = requests.post(self._api(f"{base}/tables"),
                              headers=h, json={"table": {"name": name}})
            tables[name] = r.json()["data"]["table_id"]
            time.sleep(0.2)
        print(f"  {len(tables)} 张表已创建")

        # 3. 复用类级 TABLE_SCHEMA 为每张表添加字段
        for tname, schema in self.TABLE_SCHEMA.items():
            tid = tables[tname]
            fields_resp = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h)
            for f in fields_resp.json().get("data", {}).get("items", []):
                if f.get("is_primary"):
                    requests.put(self._api(f"{base}/tables/{tid}/fields/{f['field_id']}"),
                                 headers=h,
                                 json={"field_name": schema["primary_rename"], "type": f["type"]})
                    break
            fields_resp = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h)
            for f in fields_resp.json().get("data", {}).get("items", []):
                if not f.get("is_primary"):
                    requests.delete(self._api(f"{base}/tables/{tid}/fields/{f['field_id']}"), headers=h)
            for field_def in schema["fields"]:
                requests.post(self._api(f"{base}/tables/{tid}/fields"), headers=h, json=field_def)
                time.sleep(0.1)
        print(f"  所有字段已创建")

        # 4. 设置公开权限
        requests.patch(
            self._api(f"drive/v1/permissions/{app_token}/public"),
            headers=h, params={"type": "bitable"},
            json={
                "external_access_entity": "open",
                "link_share_entity": "anyone_editable",
                "invite_external": True,
            },
        )
        print(f"  权限已设为公开可编辑")

        return {"app_token": app_token, "url": url, "tables": tables}

    def list_records(self, table_id: str) -> list[dict]:
        records = []
        page_token = None
        while True:
            params = {"page_size": 100}
            if page_token:
                params["page_token"] = page_token
            resp = requests.get(self._base(table_id), headers=self._headers(),
                                params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(f"飞书读取失败: {data.get('msg')}")
            items = data.get("data", {}).get("items", [])
            records.extend(items)
            if not data.get("data", {}).get("has_more"):
                break
            page_token = data["data"].get("page_token")
        return records

    def create_record(self, table_id: str, fields: dict) -> dict:
        resp = requests.post(self._base(table_id), headers=self._headers(),
                             json={"fields": fields}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"飞书创建记录失败: {data.get('msg')}")
        return data["data"]["record"]

    def update_record(self, table_id: str, record_id: str, fields: dict) -> dict:
        url = f"{self._base(table_id)}/{record_id}"
        resp = requests.put(url, headers=self._headers(),
                            json={"fields": fields}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"飞书更新记录失败: {data.get('msg')}")
        return data["data"]["record"]

    def push_storyboard(self, ws):
        """把本地 storyboard.json 的状态/路径回写到飞书。
        用 shot_id 做匹配键：飞书已有则更新，没有则创建。"""
        table_id = self._table_id(ws, "剧本分镜表", "FEISHU_TABLE_STORYBOARD")
        if not table_id:
            print("  未配置分镜表，跳过飞书同步")
            return

        shots = ws.load_json("storyboard.json")
        if not shots:
            print("  本地无分镜数据")
            return

        existing = self.list_records(table_id)
        shot_to_record = {}
        for rec in existing:
            fields = rec.get("fields", {})
            sid = _text_val(fields.get("镜头编号"))
            if sid:
                shot_to_record[sid] = rec["record_id"]

        for shot in shots:
            fields = {
                "镜头标题": f"第{shot['episode']}集 {shot['shot_id']}",
                "集号": shot["episode"],
                "镜头编号": shot["shot_id"],
                "台词": shot.get("dialogue", ""),
                "镜头说明": shot.get("scene_desc", ""),
                "视频提示词": shot.get("prompt", ""),
                "人物锁定": shot.get("char_lock", ""),
                "环境锁定": shot.get("env_lock", ""),
                "时间线": shot.get("timeline", ""),
                "景别运镜": shot.get("camera", ""),
                "状态": shot.get("status", "待生成"),
                "配音路径": shot.get("audio_path") or "",
                "视频路径": shot.get("video_path") or "",
                "任务ID": shot.get("task_id") or "",
                "审核备注": shot.get("notes") or "",
            }

            record_id = shot_to_record.get(shot["shot_id"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新: {shot['shot_id']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建: {shot['shot_id']}")

    def pull_storyboard(self, ws) -> list[dict]:
        """从飞书拉取分镜数据到本地 storyboard.json，返回分镜列表。"""
        table_id = self._table_id(ws, "剧本分镜表", "FEISHU_TABLE_STORYBOARD")
        if not table_id:
            print("  未配置分镜表，跳过")
            return ws.load_json("storyboard.json")

        records = self.list_records(table_id)
        shots = []
        for rec in records:
            f = rec.get("fields", {})
            sid = _text_val(f.get("镜头编号"))
            if not sid:
                continue
            shots.append({
                "episode": f.get("集号", 1),
                "shot_id": sid,
                "dialogue": _text_val(f.get("台词", "")),
                "scene_desc": _text_val(f.get("镜头说明", "")),
                "prompt": _text_val(f.get("视频提示词", "")),
                "char_lock": _text_val(f.get("人物锁定", "")),
                "env_lock": _text_val(f.get("环境锁定", "")),
                "timeline": _text_val(f.get("时间线", "")),
                "camera": _text_val(f.get("景别运镜", "")),
                "status": _text_val(f.get("状态", "待生成")),
                "audio_path": _text_val(f.get("配音路径")) or None,
                "video_path": _text_val(f.get("视频路径")) or None,
                "task_id": _text_val(f.get("任务ID")) or None,
                "notes": _text_val(f.get("审核备注", "")),
                "_record_id": rec["record_id"],
            })

        shots.sort(key=lambda s: (s["episode"], s["shot_id"]))
        ws.save_json("storyboard.json", shots)
        print(f"  已从飞书拉取 {len(shots)} 条分镜到本地")
        return shots


    def pull_characters(self, ws) -> list[dict]:
        """从飞书角色库拉取到本地 characters.json，返回角色列表。"""
        table_id = self._table_id(ws, "角色库", "FEISHU_TABLE_CHARACTER")
        if not table_id:
            return ws.load_json("characters.json")

        records = self.list_records(table_id)
        chars = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("角色名"))
            if not name:
                continue
            chars.append({
                "name": name,
                "char_type": _text_val(f.get("角色类型", "")),
                "appearance": _text_val(f.get("外貌描述", "")),
                "voice_desc": _text_val(f.get("音色描述", "")),
                "speaker": _text_val(f.get("音色Speaker")) or None,
                "ref_image": _text_val(f.get("文件路径")) or None,
                "gen_prompt": _text_val(f.get("生成提示词", "")),
                "gen_model": _text_val(f.get("生成模型")) or None,
                "source": _text_val(f.get("来源", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("characters.json", chars)
        return chars

    def pull_character_bibles(self, ws) -> list[dict]:
        """从飞书角色档案表拉取到本地 character_bibles.json。"""
        table_id = self._table_id(ws, "角色档案", "FEISHU_TABLE_CHARACTER_BIBLE")
        if not table_id:
            return ws.load_json("character_bibles.json")

        records = self.list_records(table_id)
        bibles = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("角色名"))
            if not name:
                continue
            bibles.append({
                "name": name,
                "char_type": _text_val(f.get("角色类型", "")),
                "basic_info": _text_val(f.get("基本信息", "")),
                "style_desc": _text_val(f.get("风格描述", "")),
                "voice_desc": _text_val(f.get("音色描述", "")),
                "appearance": _text_val(f.get("外貌描述", "")),
                "personality": _text_val(f.get("性格描述", "")),
                "battle_desc": _text_val(f.get("战斗描述", "")),
                "signature_expr": _text_val(f.get("标志性表达", "")),
                "notes": _text_val(f.get("标注交接", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("character_bibles.json", bibles)
        return bibles

    def pull_scenes(self, ws) -> list[dict]:
        """从飞书场景库拉取到本地 scenes.json，返回场景列表。"""
        table_id = self._table_id(ws, "场景库", "FEISHU_TABLE_SCENE")
        if not table_id:
            return ws.load_json("scenes.json")

        records = self.list_records(table_id)
        scenes = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("场景名"))
            if not name:
                continue
            scenes.append({
                "name": name,
                "scene_type": _text_val(f.get("场景类型", "")),
                "description": _text_val(f.get("场景描述", "")),
                "related_episodes": _text_val(f.get("关联集数", "")),
                "ref_image": _text_val(f.get("文件路径")) or None,
                "gen_prompt": _text_val(f.get("生成提示词", "")),
                "gen_model": _text_val(f.get("生成模型")) or None,
                "source": _text_val(f.get("来源", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("scenes.json", scenes)
        return scenes

    def update_character(self, ws, char: dict):
        """更新飞书角色库中的单条记录。char 必须含 _record_id。"""
        table_id = self._table_id(ws, "角色库", "FEISHU_TABLE_CHARACTER")
        record_id = char.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "角色名": char.get("name", ""),
            "角色类型": char.get("char_type", ""),
            "外貌描述": char.get("appearance", ""),
            "音色描述": char.get("voice_desc", ""),
            "音色Speaker": char.get("speaker") or "",
            "来源": char.get("source", ""),
            "生成提示词": char.get("gen_prompt", ""),
            "文件路径": char.get("ref_image") or "",
            "生成模型": char.get("gen_model") or "",
        }
        self.update_record(table_id, record_id, fields)

    def update_scene(self, ws, scene: dict):
        """更新飞书场景库中的单条记录。scene 必须含 _record_id。"""
        table_id = self._table_id(ws, "场景库", "FEISHU_TABLE_SCENE")
        record_id = scene.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "场景名": scene.get("name", ""),
            "场景类型": scene.get("scene_type", ""),
            "场景描述": scene.get("description", ""),
            "关联集数": scene.get("related_episodes", ""),
            "来源": scene.get("source", ""),
            "生成提示词": scene.get("gen_prompt", ""),
            "文件路径": scene.get("ref_image") or "",
            "生成模型": scene.get("gen_model") or "",
        }
        self.update_record(table_id, record_id, fields)

    def update_shot(self, ws, shot: dict):
        """更新飞书分镜表中的单条记录。shot 必须含 _record_id。"""
        table_id = self._table_id(ws, "剧本分镜表", "FEISHU_TABLE_STORYBOARD")
        record_id = shot.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "状态": shot.get("status", ""),
            "视频提示词": shot.get("prompt", ""),
            "人物锁定": shot.get("char_lock", ""),
            "环境锁定": shot.get("env_lock", ""),
            "时间线": shot.get("timeline", ""),
            "景别运镜": shot.get("camera", ""),
            "配音路径": shot.get("audio_path") or "",
            "视频路径": shot.get("video_path") or "",
            "任务ID": shot.get("task_id") or "",
            "审核备注": shot.get("notes") or "",
        }
        self.update_record(table_id, record_id, fields)

    def _table_id(self, ws, table_name: str, env_key: str) -> str:
        """从 workspace config 或环境变量获取 table_id。"""
        tables = ws.config.get("feishu", {}).get("tables", {})
        return tables.get(table_name, "") or os.environ.get(env_key, "")

    def push_characters(self, ws):
        """把本地 characters.json 同步到飞书角色库。用角色名做匹配键。"""
        table_id = self._table_id(ws, "角色库", "FEISHU_TABLE_CHARACTER")
        if not table_id:
            print("  未配置角色库，跳过")
            return

        chars = ws.load_json("characters.json")
        if not chars:
            print("  本地无角色数据")
            return

        existing = self.list_records(table_id)
        name_to_record = {}
        for rec in existing:
            name = _text_val(rec.get("fields", {}).get("角色名"))
            if name:
                name_to_record[name] = rec["record_id"]

        for c in chars:
            fields = {
                "角色ID": c.get("name", ""),
                "角色名": c.get("name", ""),
                "角色类型": c.get("char_type", ""),
                "外貌描述": c.get("appearance", ""),
                "音色描述": c.get("voice_desc", ""),
                "音色Speaker": c.get("speaker") or "",
                "来源": c.get("source", "AIGC生成") if c.get("ref_image") else "原始采集",
                "生成提示词": c.get("gen_prompt", ""),
                "文件路径": c.get("ref_image") or "",
                "生成模型": c.get("gen_model", ""),
            }
            record_id = name_to_record.get(c["name"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新角色: {c['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建角色: {c['name']}")

    def push_character_bibles(self, ws):
        """把本地 character_bibles.json 同步到飞书角色档案表。用角色名做匹配键。"""
        table_id = self._table_id(ws, "角色档案", "FEISHU_TABLE_CHARACTER_BIBLE")
        if not table_id:
            print("  未配置角色档案表，跳过")
            return

        bibles = ws.load_json("character_bibles.json")
        if not bibles:
            print("  本地无角色档案数据")
            return

        existing = self.list_records(table_id)
        name_to_record = {}
        for rec in existing:
            name = _text_val(rec.get("fields", {}).get("角色名"))
            if name:
                name_to_record[name] = rec["record_id"]

        for b in bibles:
            fields = {
                "角色名": b.get("name", ""),
                "角色类型": b.get("char_type", ""),
                "基本信息": b.get("basic_info", ""),
                "风格描述": b.get("style_desc", ""),
                "音色描述": b.get("voice_desc", ""),
                "外貌描述": b.get("appearance", ""),
                "性格描述": b.get("personality", ""),
                "战斗描述": b.get("battle_desc", ""),
                "标志性表达": b.get("signature_expr", ""),
                "标注交接": b.get("notes", ""),
            }
            record_id = name_to_record.get(b["name"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新角色档案: {b['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建角色档案: {b['name']}")

    def push_scenes(self, ws):
        """把本地 scenes.json 同步到飞书场景库。用场景名做匹配键。"""
        table_id = self._table_id(ws, "场景库", "FEISHU_TABLE_SCENE")
        if not table_id:
            print("  未配置场景库，跳过")
            return

        scenes = ws.load_json("scenes.json")
        if not scenes:
            print("  本地无场景数据")
            return

        existing = self.list_records(table_id)
        name_to_record = {}
        for rec in existing:
            name = _text_val(rec.get("fields", {}).get("场景名"))
            if name:
                name_to_record[name] = rec["record_id"]

        for s in scenes:
            fields = {
                "场景ID": s.get("name", ""),
                "场景名": s.get("name", ""),
                "场景类型": s.get("scene_type", ""),
                "场景描述": s.get("description", ""),
                "关联集数": s.get("related_episodes", ""),
                "来源": s.get("source", "AIGC生成") if s.get("ref_image") else "原始采集",
                "生成提示词": s.get("gen_prompt", ""),
                "文件路径": s.get("ref_image") or "",
                "生成模型": s.get("gen_model", ""),
            }
            record_id = name_to_record.get(s["name"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新场景: {s['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建场景: {s['name']}")

    def push_settings(self, ws):
        """把本地 settings.json 同步到飞书剧本设定表。用设定项名做匹配键。"""
        table_id = self._table_id(ws, "剧本设定", "FEISHU_TABLE_SETTINGS")
        if not table_id:
            print("  未配置设定表，跳过")
            return

        settings = ws.load_json("settings.json")
        if not settings:
            print("  本地无设定数据")
            return

        existing = self.list_records(table_id)
        name_to_record = {}
        for rec in existing:
            name = _text_val(rec.get("fields", {}).get("设定项"))
            if name:
                name_to_record[name] = rec["record_id"]

        for s in settings:
            fields = {
                "设定项": s.get("name", ""),
                "类别": s.get("category", ""),
                "设定值": s.get("value", ""),
                "全局提示词": s.get("global_prompt", ""),
                "全局参考图路径": s.get("ref_image_path", ""),
            }
            record_id = name_to_record.get(s["name"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新设定: {s['name']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建设定: {s['name']}")

    def pull_episodes(self, ws) -> list[dict]:
        """从飞书剧集表拉取到本地 episodes.json，返回剧集列表。"""
        table_id = self._table_id(ws, "剧集表", "FEISHU_TABLE_EPISODE")
        if not table_id:
            return ws.load_json("episodes.json")

        records = self.list_records(table_id)
        episodes = []
        for rec in records:
            f = rec.get("fields", {})
            ep_num = _text_val(f.get("集数"))
            if not ep_num:
                continue
            episodes.append({
                "episode": ep_num,
                "title": _text_val(f.get("集名", "")),
                "core_event": _text_val(f.get("核心事件", "")),
                "characters": _text_val(f.get("出场角色", "")),
                "prev_hook": _text_val(f.get("上集钩子", "")),
                "end_hook": _text_val(f.get("结尾钩子", "")),
                "scenes": _text_val(f.get("场次列表", "")),
                "script": _text_val(f.get("完整剧本", "")),
                "status": _text_val(f.get("状态", "待编写")),
                "_record_id": rec["record_id"],
            })
        episodes.sort(key=lambda e: e["episode"])
        ws.save_json("episodes.json", episodes)
        print(f"  已从飞书拉取 {len(episodes)} 条剧集到本地")
        return episodes

    def push_episodes(self, ws):
        """把本地 episodes.json 同步到飞书剧集表。用集数做匹配键。"""
        table_id = self._table_id(ws, "剧集表", "FEISHU_TABLE_EPISODE")
        if not table_id:
            print("  未配置剧集表，跳过")
            return

        episodes = ws.load_json("episodes.json")
        if not episodes:
            print("  本地无剧集数据")
            return

        existing = self.list_records(table_id)
        ep_to_record = {}
        for rec in existing:
            ep_num = _text_val(rec.get("fields", {}).get("集数"))
            if ep_num:
                ep_to_record[ep_num] = rec["record_id"]

        for ep in episodes:
            fields = {
                "集数": ep.get("episode", ""),
                "集名": ep.get("title", ""),
                "核心事件": ep.get("core_event", ""),
                "出场角色": ep.get("characters", ""),
                "上集钩子": ep.get("prev_hook", ""),
                "结尾钩子": ep.get("end_hook", ""),
                "场次列表": ep.get("scenes", ""),
                "完整剧本": ep.get("script", ""),
                "状态": ep.get("status", "待编写"),
            }
            record_id = ep_to_record.get(ep["episode"])
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新剧集: {ep['episode']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建剧集: {ep['episode']}")

    def pull_workbench(self, ws) -> list[dict]:
        """从飞书生图工作台拉取到本地 workbench.json，返回任务列表。"""
        table_id = self._table_id(ws, "生图工作台", "FEISHU_TABLE_WORKBENCH")
        if not table_id:
            return ws.load_json("workbench.json")

        records = self.list_records(table_id)
        tasks = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("任务名"))
            if not name:
                continue
            tasks.append({
                "name": name,
                "prompt": _text_val(f.get("提示词", "")),
                "model": _text_val(f.get("模型", "")),
                "size": _text_val(f.get("分辨率", "")),
                "status": _text_val(f.get("状态", "待生成")),
                "result_path": _text_val(f.get("结果路径", "")),
                "notes": _text_val(f.get("备注", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("workbench.json", tasks)
        print(f"  已从飞书拉取 {len(tasks)} 条工作台任务到本地")
        return tasks

    def update_workbench_task(self, ws, task: dict):
        """更新飞书生图工作台中的单条记录。task 必须含 _record_id。"""
        table_id = self._table_id(ws, "生图工作台", "FEISHU_TABLE_WORKBENCH")
        record_id = task.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "状态": task.get("status", ""),
            "结果路径": task.get("result_path") or "",
            "备注": task.get("notes") or "",
        }
        self.update_record(table_id, record_id, fields)

    def pull_assets(self, ws) -> list[dict]:
        """从飞书素材库拉取到本地 assets.json，返回素材列表。"""
        table_id = self._table_id(ws, "素材库", "FEISHU_TABLE_ASSET")
        if not table_id:
            return ws.load_json("assets.json")

        records = self.list_records(table_id)
        assets = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("素材ID"))
            if not name:
                continue
            assets.append({
                "name": name,
                "file_path": _text_val(f.get("文件路径", "")),
                "asset_type": _text_val(f.get("素材类型", "")),
                "model": _text_val(f.get("生成模型", "")),
                "prompt": _text_val(f.get("生成提示词", "")),
                "source": _text_val(f.get("来源", "")),
                "notes": _text_val(f.get("备注", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("assets.json", assets)
        print(f"  已从飞书拉取 {len(assets)} 条素材到本地")
        return assets

    def add_asset(self, ws, asset: dict):
        """往飞书素材库追加一条记录。"""
        table_id = self._table_id(ws, "素材库", "FEISHU_TABLE_ASSET")
        if not table_id:
            return
        fields = {
            "素材ID": asset.get("name", ""),
            "文件路径": asset.get("file_path", ""),
            "素材类型": asset.get("asset_type", ""),
            "生成模型": asset.get("model", ""),
            "生成提示词": asset.get("prompt", ""),
            "来源": asset.get("source", "AIGC生成"),
            "备注": asset.get("notes", ""),
        }
        self.create_record(table_id, fields)

    def pull_settings(self, ws) -> list[dict]:
        """从飞书剧本设定表拉取到本地 settings.json，返回设定列表。"""
        table_id = self._table_id(ws, "剧本设定", "FEISHU_TABLE_SETTINGS")
        if not table_id:
            print("  未配置设定表，跳过")
            return ws.load_json("settings.json")

        records = self.list_records(table_id)
        settings = []
        for rec in records:
            f = rec.get("fields", {})
            name = _text_val(f.get("设定项"))
            if not name:
                continue
            settings.append({
                "name": name,
                "category": _text_val(f.get("类别", "")),
                "value": _text_val(f.get("设定值", "")),
                "global_prompt": _text_val(f.get("全局提示词", "")),
                "ref_image_path": _text_val(f.get("全局参考图路径", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("settings.json", settings)
        print(f"  已从飞书拉取 {len(settings)} 条设定到本地")
        return settings


def _text_val(v) -> str:
    """飞书多维表格字段值可能是 str、list[dict]（富文本）、int、float 等，统一转 str。"""
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        parts = []
        for item in v:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(v)
