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
        "小说表": {
            "primary_rename": "章节",
            "fields": [
                {"field_name": "标题", "type": 1},
                {"field_name": "内容", "type": 1},
            ],
        },
        "剧本分镜表": {
            "primary_rename": "镜头编号",
            "fields": [
                {"field_name": "集号", "type": 2},
                {"field_name": "镜头标题", "type": 1},
                {"field_name": "模型", "type": 1},
                {"field_name": "视频提示词", "type": 1},
                {"field_name": "时间线", "type": 1},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待生成"}, {"name": "生成中"}, {"name": "待审核"},
                    {"name": "通过"}, {"name": "返工"}, {"name": "生成失败"},
                ]}},
                {"field_name": "视频路径", "type": 1},
                {"field_name": "任务ID", "type": 1},
                {"field_name": "审核备注", "type": 1},
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
        "剧本表": {
            "primary_rename": "集号",
            "fields": [
                {"field_name": "集名", "type": 1},
                {"field_name": "对应原小说章节", "type": 1},
                {"field_name": "完整剧本", "type": 1},
                {"field_name": "分镜设计稿", "type": 1},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待转剧本"}, {"name": "待编写"}, {"name": "草稿"},
                    {"name": "已确认"}, {"name": "已拆分镜"},
                ]}},
            ],
        },
        "音色库": {
            "primary_rename": "音色ID",
            "fields": [
                {"field_name": "角色名", "type": 1},
                {"field_name": "音色描述", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "来源", "type": 3, "property": {"options": [
                    {"name": "手动上传"}, {"name": "视频提取"}, {"name": "TTS合成"},
                ]}},
                {"field_name": "备注", "type": 1},
            ],
        },
        "生图工作台": {
            "primary_rename": "任务名",
            "fields": [
                {"field_name": "提示词", "type": 1},
                {"field_name": "模型", "type": 3, "property": {"options": [
                    {"name": "doubao-seedream-5-0-flash-260915"},
                    {"name": "doubao-seedream-4-0-250828"},
                    {"name": "doubao-seedream-3-0-t2i-250415"},
                ]}},
                {"field_name": "分辨率", "type": 3, "property": {"options": [
                    {"name": "1K"}, {"name": "2K"}, {"name": "4K"},
                ]}},
                {"field_name": "画面比例", "type": 3, "property": {"options": [
                    {"name": "16:9"}, {"name": "9:16"}, {"name": "22:9"},
                ]}},
                {"field_name": "状态", "type": 3, "property": {"options": [
                    {"name": "待生成"}, {"name": "生成中"}, {"name": "已完成"}, {"name": "生成失败"},
                ]}},
                {"field_name": "结果路径", "type": 1},
                {"field_name": "备注", "type": 1},
            ],
        },
        "资产库": {
            "primary_rename": "名称",
            "fields": [
                {"field_name": "类型", "type": 3, "property": {"options": [
                    {"name": "角色"}, {"name": "场景"}, {"name": "道具"},
                ]}},
                {"field_name": "描述", "type": 1},
                {"field_name": "文件路径", "type": 1},
                {"field_name": "备注", "type": 1},
            ],
        },
        "系统设置": {
            "primary_rename": "配置项",
            "fields": [
                {"field_name": "配置值", "type": 1},
                {"field_name": "说明", "type": 1},
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
        """检查标准表是否齐全（含资产库），缺失的自动创建。返回完整映射。"""
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

    # ------ 系统设置表：用于存放项目路径等引导配置 ------
    def _system_table_id(self, table_id: str = "") -> str:
        """获取「系统设置」表 ID：优先用传入值，否则按表名在线发现。"""
        if table_id:
            return table_id
        tables = self.discover_tables()
        tid = tables.get("系统设置", "")
        if not tid:
            raise RuntimeError("飞书表格中未找到「系统设置」数据表")
        return tid

    def get_config_value(self, key: str, table_id: str = "") -> str:
        """读取「系统设置」表中指定配置项的配置值；不存在返回空串。"""
        tid = self._system_table_id(table_id)
        for rec in self.list_records(tid):
            fields = rec.get("fields", {})
            if _text_val(fields.get("配置项")) == key:
                return _text_val(fields.get("配置值"))
        return ""

    def get_all_config(self, table_id: str = "") -> list[dict]:
        """读取「系统设置」表全部配置，返回 [{key, value, description, record_id}]。"""
        tid = self._system_table_id(table_id)
        result = []
        for rec in self.list_records(tid):
            fields = rec.get("fields", {})
            key = _text_val(fields.get("配置项"))
            if not key:
                continue
            result.append({
                "key": key,
                "value": _text_val(fields.get("配置值")),
                "description": _text_val(fields.get("说明")),
                "record_id": rec["record_id"],
            })
        return result

    def upsert_config_value(self, key: str, value: str, description: str = "",
                            table_id: str = "") -> str:
        """在「系统设置」表写入或更新一个配置项（按配置项匹配），返回 record_id。"""
        tid = self._system_table_id(table_id)
        record_id = None
        for rec in self.list_records(tid):
            if _text_val(rec.get("fields", {}).get("配置项")) == key:
                record_id = rec["record_id"]
                break

        fields = {"配置项": key, "配置值": value}
        if description:
            fields["说明"] = description

        if record_id:
            self.update_record(tid, record_id, fields)
            return record_id
        return self.create_record(tid, fields)["record_id"]

    def create_project(self, drama_name: str) -> dict:
        """创建一个新项目的完整飞书多维表格（全部标准表 + 字段 + 公开权限）。
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
                "镜头编号": shot["shot_id"],
                "镜头标题": shot.get("title") or f"第{shot['episode']}集 {shot['shot_id']}",
                "模型": shot.get("model") or "",
                "集号": int(float(shot.get("episode") or 1)),
                "视频提示词": shot.get("prompt", ""),
                "时间线": shot.get("timeline", ""),
                "状态": shot.get("status", "待生成"),
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
                "episode": int(float(f.get("集号", 1) or 1)),
                "shot_id": sid,
                "title": _text_val(f.get("镜头标题", "")),
                "model": _text_val(f.get("模型", "")),
                "prompt": _text_val(f.get("视频提示词", "")),
                "timeline": _text_val(f.get("时间线", "")),
                "status": _text_val(f.get("状态", "待生成")),
                "video_path": _text_val(f.get("视频路径")) or None,
                "task_id": _text_val(f.get("任务ID")) or None,
                "notes": _text_val(f.get("审核备注", "")),
                "_record_id": rec["record_id"],
            })

        shots.sort(key=lambda s: (s["episode"], s["shot_id"]))
        ws.save_json("storyboard.json", shots)
        print(f"  已从飞书拉取 {len(shots)} 条分镜到本地")
        return shots


    def update_shot(self, ws, shot: dict):
        """更新飞书分镜表中的单条记录。shot 必须含 _record_id。"""
        table_id = self._table_id(ws, "剧本分镜表", "FEISHU_TABLE_STORYBOARD")
        record_id = shot.get("_record_id")
        if not table_id or not record_id:
            return
        fields = {
            "状态": shot.get("status", ""),
            "镜头标题": shot.get("title", ""),
            "视频提示词": shot.get("prompt", ""),
            "时间线": shot.get("timeline", ""),
            "视频路径": shot.get("video_path") or "",
            "任务ID": shot.get("task_id") or "",
            "审核备注": shot.get("notes") or "",
        }
        self.update_record(table_id, record_id, fields)

    def _table_id(self, ws, table_name: str, env_key: str) -> str:
        """从 workspace config 或环境变量获取 table_id。"""
        tables = ws.config.get("feishu", {}).get("tables", {})
        return tables.get(table_name, "") or os.environ.get(env_key, "")

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

    # ------ 小说表 ------
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
                "章节": _text_val(f.get("章节")),
                "标题": _text_val(f.get("标题")),
                "内容": _text_val(f.get("内容")),
            })
        ws.save_json("novels.json", rows)
        return rows

    def push_novels(self, ws):
        tid = self._novel_table_id()
        existing = {}
        for r in self.list_records(tid):
            key = _text_val(r.get("fields", {}).get("章节"))
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

    def pull_episodes(self, ws) -> list[dict]:
        """从飞书剧本表拉取到本地 episodes.json，返回剧本列表。"""
        table_id = self._table_id(ws, "剧本表", "FEISHU_TABLE_EPISODE")
        if not table_id:
            return ws.load_json("episodes.json")

        records = self.list_records(table_id)
        episodes = []
        for rec in records:
            f = rec.get("fields", {})
            ep_num = _text_val(f.get("集号"))
            if not ep_num:
                continue
            episodes.append({
                "episode": ep_num,
                "title": _text_val(f.get("集名", "")),
                "source_chapters": _text_val(f.get("对应原小说章节", "")),
                "script": _text_val(f.get("完整剧本", "")),
                "status": _text_val(f.get("状态", "待编写")),
                "_record_id": rec["record_id"],
            })
        episodes.sort(key=lambda e: e["episode"])
        ws.save_json("episodes.json", episodes)
        print(f"  已从飞书拉取 {len(episodes)} 条剧本到本地")
        return episodes

    def push_episodes(self, ws):
        """把本地 episodes.json 同步到飞书剧本表。用集号做匹配键。"""
        table_id = self._table_id(ws, "剧本表", "FEISHU_TABLE_EPISODE")
        if not table_id:
            print("  未配置剧本表，跳过")
            return

        episodes = ws.load_json("episodes.json")
        if not episodes:
            print("  本地无剧本数据")
            return

        existing = self.list_records(table_id)
        ep_to_record = {}
        for rec in existing:
            ep_num = _text_val(rec.get("fields", {}).get("集号"))
            if ep_num:
                ep_to_record[ep_num] = rec["record_id"]

        for ep in episodes:
            try:
                ep_key = str(int(float(ep.get("episode"))))
            except (TypeError, ValueError):
                ep_key = str(ep.get("episode", ""))
            fields = {
                "集号": ep_key,
                "集名": ep.get("title", ""),
                "对应原小说章节": str(ep.get("source_chapters", "") or ""),
                "完整剧本": ep.get("script", ""),
                "状态": ep.get("status", "待编写"),
            }
            record_id = ep_to_record.get(ep_key) or ep_to_record.get(str(ep.get("episode")))
            if record_id:
                self.update_record(table_id, record_id, fields)
                print(f"  飞书更新剧本: {ep['episode']}")
            else:
                self.create_record(table_id, fields)
                print(f"  飞书创建剧本: {ep['episode']}")

    def ensure_fields(self, table_id: str, field_defs: list[dict]) -> list[str]:
        """给已存在的表补缺失字段；已存在则跳过。返回新建的字段名。"""
        furl = self._api(f"bitable/v1/apps/{self.app_token}/tables/{table_id}/fields")
        resp = requests.get(furl, headers=self._headers(), timeout=15)
        exist = {f.get("field_name") for f in resp.json().get("data", {}).get("items", [])}
        made = []
        for fd in field_defs:
            if fd["field_name"] in exist:
                continue
            r = requests.post(furl, headers=self._headers(), json=fd, timeout=15)
            r.raise_for_status()
            data = r.json()
            if data.get("code") != 0:
                raise RuntimeError(f"飞书建字段失败: {fd['field_name']} {data.get('msg')}")
            made.append(fd["field_name"])
        return made

    def pull_assets_lib(self, ws) -> list[dict]:
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
            rows.append({
                "name": nm,
                "kind": _text_val(f.get("类型", "")),
                "description": _text_val(f.get("描述", "")),
                "file_path": _text_val(f.get("文件路径", "")),
                "note": _text_val(f.get("备注", "")),
                "_record_id": rec["record_id"],
            })
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
                "类型": a.get("kind", ""),
                "描述": a.get("description", ""),
                "文件路径": a.get("file_path", ""),
                "备注": a.get("note", ""),
            }
            rid = existing.get(a["name"])
            if rid:
                self.update_record(table_id, rid, fields)
            else:
                self.create_record(table_id, fields)
        print(f"  资产库已同步 {len(rows)} 条")

    def pull_voices(self, ws) -> list[dict]:
        """从飞书音色库拉取到本地 voices.json，返回音色列表。"""
        table_id = self._table_id(ws, "音色库", "FEISHU_TABLE_VOICE")
        if not table_id:
            return ws.load_json("voices.json")

        voices = []
        for rec in self.list_records(table_id):
            f = rec.get("fields", {})
            name = _text_val(f.get("音色ID"))
            if not name:
                continue
            voices.append({
                "name": name,
                "character": _text_val(f.get("角色名", "")),
                "description": _text_val(f.get("音色描述", "")),
                "file_path": _text_val(f.get("文件路径", "")),
                "source": _text_val(f.get("来源", "")),
                "notes": _text_val(f.get("备注", "")),
                "_record_id": rec["record_id"],
            })
        ws.save_json("voices.json", voices)
        print(f"  已从飞书拉取 {len(voices)} 条音色到本地")
        return voices

    def pull_workbench(self, ws) -> list[dict]:
        """从飞书生图工作台拉取到本地 workbench.json，返回任务列表。"""
        table_id = self._table_id(ws, "生图工作台", "FEISHU_TABLE_WORKBENCH")
        if not table_id:
            return ws.load_json("workbench.json")

        records = self.list_records(table_id)
        tasks = []
        for rec in records:
            f = rec.get("fields", {})
            prompt = _text_val(f.get("提示词", ""))
            name = _text_val(f.get("任务名"))
            if not name:
                # 只填提示词也能跑：任务名留空时从提示词派生
                name = (prompt.strip().splitlines()[0][:20] if prompt.strip() else "")
            if not name:
                continue
            tasks.append({
                "name": name,
                "prompt": prompt,
                "model": _text_val(f.get("模型", "")),
                "size": _text_val(f.get("分辨率", "")),
                "ratio": _text_val(f.get("画面比例", "")) or "16:9",
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
            "画面比例": task.get("ratio") or "",
        }
        self.update_record(table_id, record_id, fields)

    def push_workbench(self, ws):
        """把本地 workbench.json 同步到飞书：任务名做匹配键，已有则更新，没有则新建。

        新建后把 _record_id 写回本地，保证 generate 能把状态与结果路径回填到同一条记录。"""
        table_id = self._table_id(ws, "生图工作台", "FEISHU_TABLE_WORKBENCH")
        if not table_id:
            print("  未配置生图工作台，跳过飞书同步")
            return
        tasks = ws.load_json("workbench.json") or []
        if not tasks:
            print("  本地无工作台任务")
            return

        existing = self.list_records(table_id)
        by_name = {}
        for rec in existing:
            nm = _text_val(rec.get("fields", {}).get("任务名"))
            if nm:
                by_name[nm] = rec["record_id"]

        created, updated = 0, 0
        for task in tasks:
            prompt = task.get("prompt") or ""
            name = (task.get("name") or "").strip()
            if not name and prompt.strip():
                name = prompt.strip().splitlines()[0][:20]
                task["name"] = name
            if not name:
                continue
            fields = {
                "任务名": name,
                "提示词": prompt,
                "模型": task.get("model") or "",
                "分辨率": task.get("size") or "",
                "画面比例": task.get("ratio") or "16:9",
                "状态": task.get("status") or "待生成",
                "结果路径": task.get("result_path") or "",
                "备注": task.get("notes") or "",
            }
            rid = by_name.get(name) or task.get("_record_id")
            try:
                if rid:
                    self.update_record(table_id, rid, fields)
                    updated += 1
                    print(f"  飞书更新: {name}")
                else:
                    rec = self.create_record(table_id, fields)
                    rid = (rec or {}).get("record_id")
                    if rid:
                        by_name[name] = rid
                    created += 1
                    print(f"  飞书新建: {name}")
                if rid:
                    task["_record_id"] = rid
            except Exception as e:
                print(f"  飞书同步失败（{name}）: {e}")

        ws.save_json("workbench.json", tasks)
        print(f"  工作台同步：新增 {created}，更新 {updated}")

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

    # ------ 表结构迁移：剧集表 → 剧本表 + 新字段 ------
    def plan_schema_migration(self) -> dict:
        """只读：对比线上表结构与 TABLE_SCHEMA，返回迁移计划，不做任何写入。

        返回 {
          "rename": (旧表名, 新表名) | None,
          "table_ids": {表名: table_id},
          "add_fields": {表名: [field_def, ...]},
          "move_rows": 需要把「完整剧本」挪到「小说内容」的行数,
        }
        """
        h = self._headers()
        base = f"bitable/v1/apps/{self.app_token}"
        tables = self.discover_tables()
        plan = {"rename": None, "table_ids": {}, "add_fields": {}, "move_rows": 0}

        if "剧集表" in tables and "剧本表" not in tables:
            plan["rename"] = ("剧集表", "剧本表")
            tables["剧本表"] = tables["剧集表"]
        plan["table_ids"] = tables

        for tname in ("剧本表", "场景库"):
            tid = tables.get(tname)
            if not tid:
                continue
            resp = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h, timeout=15)
            resp.raise_for_status()
            have = {f["field_name"] for f in resp.json().get("data", {}).get("items", [])}
            missing = [fd for fd in self.TABLE_SCHEMA[tname]["fields"]
                       if fd["field_name"] not in have]
            if missing:
                plan["add_fields"][tname] = missing

        tid = tables.get("剧本表")
        if tid:
            for rec in self.list_records(tid):
                f = rec.get("fields", {})
                if _text_val(f.get("完整剧本")) and not _text_val(f.get("小说内容")):
                    plan["move_rows"] += 1
        return plan

    def apply_schema_migration(self, plan: dict) -> None:
        """执行迁移（写入操作，须在用户确认后调用）。幂等：已完成的步骤自动跳过。"""
        h = self._headers()
        base = f"bitable/v1/apps/{self.app_token}"
        tables = plan["table_ids"]

        if plan["rename"]:
            old, new = plan["rename"]
            r = requests.patch(self._api(f"{base}/tables/{tables[old]}"),
                               headers=h, json={"name": new}, timeout=15)
            r.raise_for_status()
            if r.json().get("code") != 0:
                raise RuntimeError(f"飞书表改名失败: {r.json().get('msg')}")
            print(f"  已改名: {old} → {new}")

        for tname, fields in plan["add_fields"].items():
            for fd in fields:
                r = requests.post(self._api(f"{base}/tables/{tables[tname]}/fields"),
                                  headers=h, json=fd, timeout=15)
                r.raise_for_status()
                if r.json().get("code") != 0:
                    raise RuntimeError(f"飞书新增字段失败 {tname}.{fd['field_name']}: {r.json().get('msg')}")
                print(f"  已新增字段: {tname}.{fd['field_name']}")
                time.sleep(0.1)

        # 状态是单选，新增选项「待转剧本」需更新字段定义
        tid = tables.get("剧本表")
        if tid:
            r = requests.get(self._api(f"{base}/tables/{tid}/fields"), headers=h, timeout=15)
            r.raise_for_status()
            for f in r.json().get("data", {}).get("items", []):
                if f["field_name"] != "状态":
                    continue
                names = {o["name"] for o in f.get("property", {}).get("options", [])}
                if "待转剧本" not in names:
                    options = [{"name": o["name"]} for o in f.get("property", {}).get("options", [])]
                    options.insert(0, {"name": "待转剧本"})
                    ur = requests.put(self._api(f"{base}/tables/{tid}/fields/{f['field_id']}"),
                                      headers=h,
                                      json={"field_name": "状态", "type": 3,
                                            "property": {"options": options}},
                                      timeout=15)
                    ur.raise_for_status()
                    print("  已补状态选项: 待转剧本")

            moved = 0
            for rec in self.list_records(tid):
                f = rec.get("fields", {})
                old_script = _text_val(f.get("完整剧本"))
                if old_script and not _text_val(f.get("小说内容")):
                    self.update_record(tid, rec["record_id"], {
                        "小说内容": old_script,
                        "完整剧本": "",
                        "状态": "待转剧本",
                    })
                    moved += 1
            print(f"  已迁移 {moved} 行：完整剧本 → 小说内容（状态置「待转剧本」）")


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
