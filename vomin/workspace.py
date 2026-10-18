import os
import re
import json
import shutil
from datetime import datetime

import yaml


class Workspace:
    """一个 workspace = 一部剧的所有数据和素材。
    所有路径存相对路径，运行时拼接 root 得到绝对路径。
    数据源优先级：飞书表格 > 本地 JSON 缓存。"""

    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        cfg_path = self.abs("workspace.yaml")
        if os.path.exists(cfg_path):
            self._config = self._load_config()
        else:
            self._config = {}
        self._cache = {}
        self.feishu = self._init_feishu()

    def _load_config(self) -> dict:
        with open(self.abs("workspace.yaml"), "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def save_config(self):
        with open(self.abs("workspace.yaml"), "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, default_flow_style=False)

    def _init_feishu(self):
        """根据 workspace.yaml 中的飞书配置初始化 FeishuBitable 实例。"""
        feishu_cfg = self._config.get("feishu", {})
        app_token = feishu_cfg.get("app_token", "")
        if not app_token:
            return None
        try:
            from vomin.feishu.bitable import FeishuBitable
            return FeishuBitable(app_token=app_token)
        except Exception:
            return None

    def invalidate_cache(self, key: str = None):
        if key:
            self._cache.pop(key, None)
        else:
            self._cache.clear()

    def abs(self, rel_path: str) -> str:
        return os.path.join(self.root, rel_path)

    def rel(self, abs_path: str) -> str:
        return os.path.relpath(abs_path, self.root)

    def episode_dir(self, ep: int, sub: str = "") -> str:
        d = self.abs(f"ep{ep:02d}/{sub}" if sub else f"ep{ep:02d}")
        os.makedirs(d, exist_ok=True)
        return d

    def backup(self, rel_path: str) -> str | None:
        """如果文件存在，移到 bak/ 目录并加时间戳，返回备份路径。"""
        src = self.abs(rel_path)
        if not os.path.exists(src):
            return None
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(os.path.basename(rel_path))
        bak_dir = self.abs("bak")
        os.makedirs(bak_dir, exist_ok=True)
        dst = os.path.join(bak_dir, f"{name}_{ts}{ext}")
        shutil.move(src, dst)
        return dst

    @property
    def config(self) -> dict:
        return self._config

    def load_json(self, rel_path: str) -> list | dict:
        path = self.abs(rel_path)
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, rel_path: str, data):
        with open(self.abs(rel_path), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_from_feishu(self, cache_key: str, pull_method: str, json_file: str) -> list[dict]:
        if cache_key in self._cache:
            return self._cache[cache_key]
        if self.feishu:
            try:
                data = getattr(self.feishu, pull_method)(self)
                self._cache[cache_key] = data
                return data
            except Exception as e:
                print(f"  飞书读取失败({cache_key})，降级读本地缓存: {e}")
        data = self.load_json(json_file)
        self._cache[cache_key] = data
        return data

    def load_storyboard(self) -> list[dict]:
        return self._load_from_feishu("storyboard", "pull_storyboard", "storyboard.json")

    def save_storyboard(self, data: list[dict]):
        self.save_json("storyboard.json", data)
        self._cache["storyboard"] = data

    def load_characters(self) -> list[dict]:
        return self._load_from_feishu("characters", "pull_characters", "characters.json")

    def save_characters(self, data: list[dict]):
        self.save_json("characters.json", data)
        self._cache["characters"] = data

    def load_character_bibles(self) -> list[dict]:
        return self._load_from_feishu("character_bibles", "pull_character_bibles", "character_bibles.json")

    def save_character_bibles(self, data: list[dict]):
        self.save_json("character_bibles.json", data)
        self._cache["character_bibles"] = data

    def load_scenes(self) -> list[dict]:
        return self._load_from_feishu("scenes", "pull_scenes", "scenes.json")

    def save_scenes(self, data: list[dict]):
        self.save_json("scenes.json", data)
        self._cache["scenes"] = data

    def load_settings(self) -> list[dict]:
        return self._load_from_feishu("settings", "pull_settings", "settings.json")

    def save_settings(self, data: list[dict]):
        self.save_json("settings.json", data)
        self._cache["settings"] = data

    def load_episodes(self) -> list[dict]:
        return self._load_from_feishu("episodes", "pull_episodes", "episodes.json")

    def save_episodes(self, data: list[dict]):
        self.save_json("episodes.json", data)
        self._cache["episodes"] = data

    def load_workbench(self) -> list[dict]:
        return self._load_from_feishu("workbench", "pull_workbench", "workbench.json")

    def load_assets(self) -> list[dict]:
        return self._load_from_feishu("assets", "pull_assets", "assets.json")

    def get_global_prompt(self) -> str:
        """从 settings.json 中收集所有设定项的全局提示词，拼接返回。"""
        settings = self.load_settings()
        parts = []
        for s in settings:
            gp = s.get("global_prompt", "").strip()
            if gp:
                parts.append(gp)
        return "，".join(parts) if parts else self.config.get("global", {}).get("prompt_suffix", "")

    def get_global_ref_images(self) -> list[str]:
        """从 settings.json 中收集所有全局参考图路径，返回绝对路径列表。"""
        settings = self.load_settings()
        paths = []
        for s in settings:
            ref = s.get("ref_image_path", "").strip()
            if ref:
                for p in ref.split(","):
                    p = p.strip()
                    if p:
                        abs_p = self.abs(p)
                        if os.path.exists(abs_p) and abs_p not in paths:
                            paths.append(abs_p)
        if not paths:
            for g in self.config.get("global", {}).get("ref_images", []):
                abs_g = self.abs(g)
                if os.path.exists(abs_g) and abs_g not in paths:
                    paths.append(abs_g)
        return paths

    # 提示词引用支持的表：表名 -> (加载方法名, 行主键字段, 携带素材的文件字段[按优先级])
    REF_SHEETS = {
        "角色库": ("load_characters", "name", ["ref_image"]),
        "场景库": ("load_scenes", "name", ["ref_image"]),
        "生图工作台": ("load_workbench", "name", ["result_path", "ref_image"]),
        "素材库": ("load_assets", "name", ["file_path"]),
        "剧本设定": ("load_settings", "name", ["ref_image_path"]),
        "剧本分镜表": ("load_storyboard", "shot_id", ["ref_image", "result_path", "file_path", "video_path"]),
        # 以下表不携带可传递给生成 API 的素材，仅登记引用会报错提示
        "角色档案": ("load_character_bibles", "name", []),
        "剧集表": ("load_episodes", "episode", []),
    }

    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif"}
    VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi"}

    def expand_prompt(self, template: str, *,
                      skip_self: tuple[str, str] | None = None,
                      ) -> tuple[str, list[str], list[str], list[str], list[str]]:
        """把 prompt 模板中的 {表名:行标识} 标记移除，同时收集引用到的参考素材。

        通用语法（中英文冒号均可，推荐中文冒号）：
            {角色库：林砚}          → 收集角色的形象图（等价 {角色库:林砚}）
            {场景库：写字楼大堂}     → 收集场景的参考图
            {生图工作台：任务名}     → 收集工作台任务的结果图
            {素材库：素材ID}        → 按素材文件类型收集图片/视频
            {剧本设定：画面风格}     → 收集设定项的全局参考图
            {剧本分镜表：ep01_s01}  → 收集该分镜已生成的图片/视频
            通用形式 {sheetName:rowId}：sheetName 为上表任一表名，rowId 为该行主键。

        标记会从提示词正文中移除（画面由参考素材锚定，不重复文字描述），
        引用到的图片/视频作为参考素材随 API 请求传递。

        返回 (文本, 参考图绝对路径列表, 角色名列表, 场景名列表, 参考视频绝对路径列表)。
        """
        ref_images = []
        ref_videos = []
        characters_found = []
        scenes_found = []
        errors = []
        sheet_cache: dict[str, dict] = {}

        def _row_map(sheet: str):
            if sheet not in sheet_cache:
                loader_name, key_field, _ = self.REF_SHEETS[sheet]
                rows = getattr(self, loader_name)()
                sheet_cache[sheet] = {str(r.get(key_field, "")): r for r in rows}
            return sheet_cache[sheet]

        def _collect_file(kind, name, path_val):
            if not path_val:
                errors.append(f"{{{kind}：{name}}} 对象存在但没有关联素材文件")
                return
            abs_file = self.abs(path_val)
            if not os.path.exists(abs_file):
                errors.append(f"{{{kind}：{name}}} 素材文件不存在: {path_val}")
                return
            ext = os.path.splitext(abs_file)[1].lower()
            if ext in self.IMAGE_EXTS:
                if abs_file not in ref_images:
                    ref_images.append(abs_file)
            elif ext in self.VIDEO_EXTS:
                if abs_file not in ref_videos:
                    ref_videos.append(abs_file)
            else:
                errors.append(f"{{{kind}：{name}}} 不支持的素材类型: {path_val}")

        def _replace(m):
            kind = m.group(1).strip()
            name = m.group(2).strip()
            if skip_self and (kind, name) == skip_self:
                return m.group(0)
            if kind not in self.REF_SHEETS:
                errors.append(
                    f"不支持的引用表「{kind}」；可用表：{ '、'.join(self.REF_SHEETS.keys()) }"
                )
                return ""
            if kind == "角色库" and name not in characters_found:
                characters_found.append(name)
            if kind == "场景库" and name not in scenes_found:
                scenes_found.append(name)
            _, _, file_fields = self.REF_SHEETS[kind]
            row = _row_map(kind).get(name)
            if row is None:
                errors.append(f"{kind}中找不到「{name}」")
                return ""
            if not file_fields:
                errors.append(
                    f"{{{kind}：{name}}} 该表不携带可传递的素材文件；"
                    f"引用角色请用 {{角色库：名字}}，引用场景请用 {{场景库：名字}}"
                )
                return ""
            collected = False
            for field in file_fields:
                path_val = row.get(field)
                if path_val and os.path.exists(self.abs(path_val)):
                    _collect_file(kind, name, path_val)
                    collected = True
                    break
            if not collected and not errors:
                errors.append(f"{{{kind}：{name}}} 对象存在但没有关联素材文件")
            return ""

        # 通用 {sheetName:rowId} / {sheetName：rowId}，中英文冒号均支持
        text = re.sub(r"\{([^{}:：]+)\s*[:：]\s*([^{}]+?)\s*\}", _replace, template)

        if errors:
            raise ValueError("提示词引用解析失败:\n  " + "\n  ".join(errors))

        return text, ref_images, characters_found, scenes_found, ref_videos

    def update_budget(self, cost: float):
        budget = self._config.setdefault("budget", {"total_limit": 5000, "spent": 0})
        budget["spent"] = round(budget.get("spent", 0) + cost, 2)
        if budget["spent"] > budget["total_limit"]:
            raise RuntimeError(
                f"预算超限！已花费 {budget['spent']} 元，上限 {budget['total_limit']} 元"
            )
        self.save_config()

    @staticmethod
    def init_workspace(root: str, drama_name: str = "新项目",
                       feishu_app_token: str = "",
                       feishu_tables: dict | None = None,
                       feishu_url: str = "") -> "Workspace":
        root = os.path.abspath(root)
        dirs = [
            "ref/characters", "ref/scenes", "ref/workbench", "ref/global",
            "music", "bak",
        ]
        for d in dirs:
            os.makedirs(os.path.join(root, d), exist_ok=True)

        config = {
            "drama_name": drama_name,
            "feishu": {
                "url": feishu_url,
                "app_token": feishu_app_token,
                "tables": feishu_tables or {},
            },
            "ark": {
                "video_model": "doubao-seedance-2-5-260628",
                "video_model_fast": "doubao-seedance-2-0-fast-260128",
                "image_model": "doubao-seedream-5-0-flash-260915",
                "default_resolution": "720p",
                "default_ratio": "9:16",
                "default_duration": 5,
            },
            "tts": {
                "model": "seed-audio-1.0",
                "format": "mp3",
                "sample_rate": 48000,
            },
            "budget": {
                "total_limit": 5000,
                "spent": 0,
            },
        }
        ws = Workspace(root)
        ws._config = config
        ws.save_config()

        ws.save_json("characters.json", [])
        ws.save_json("character_bibles.json", [])
        ws.save_json("scenes.json", [])
        ws.save_json("settings.json", [])
        ws.save_json("episodes.json", [])
        ws.save_storyboard([])

        return ws
