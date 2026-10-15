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

    def expand_prompt(self, template: str, *,
                      skip_self: tuple[str, str] | None = None,
                      ) -> tuple[str, list[str], list[str], list[str]]:
        """把 prompt 模板中的 {sheet名:名字} 标记移除，同时收集引用到的参考图。

        支持的 sheet 引用：
            {角色库:林砚}         → 收集角色的 ref_image
            {场景库:写字楼大堂}    → 收集场景的 ref_image
            {生图工作台:任务名}    → 收集工作台任务的 result_path
            {素材库:素材ID}    → 收集素材的文件路径

        返回 (去除标记后的文本, 参考图绝对路径列表, 角色名列表, 场景名列表)。
        """
        char_map = {c["name"]: c for c in self.load_characters()}
        scene_map = {s["name"]: s for s in self.load_scenes()}
        ref_images = []
        characters_found = []
        scenes_found = []
        errors = []

        workbench_map = None
        asset_map = None

        def _ensure_workbench():
            nonlocal workbench_map
            if workbench_map is None:
                workbench_map = {t["name"]: t for t in self.load_workbench()}

        def _ensure_assets():
            nonlocal asset_map
            if asset_map is None:
                asset_map = {a.get("name", ""): a for a in self.load_assets()}

        def _collect_image(kind, name, path_val):
            if not path_val:
                errors.append(f"{{{kind}:{name}}} 对象存在但没有关联图片")
                return
            abs_img = self.abs(path_val)
            if not os.path.exists(abs_img):
                errors.append(f"{{{kind}:{name}}} 图片文件不存在: {path_val}")
                return
            if abs_img not in ref_images:
                ref_images.append(abs_img)

        def _replace(m):
            kind, name = m.group(1), m.group(2)
            if skip_self and (kind, name) == skip_self:
                return m.group(0)
            if kind == "角色库":
                if name not in characters_found:
                    characters_found.append(name)
                char = char_map.get(name)
                if char:
                    _collect_image(kind, name, char.get("ref_image"))
                else:
                    errors.append(f"角色库中找不到「{name}」")
            elif kind == "场景库":
                if name not in scenes_found:
                    scenes_found.append(name)
                scene = scene_map.get(name)
                if scene:
                    _collect_image(kind, name, scene.get("ref_image"))
                else:
                    errors.append(f"场景库中找不到「{name}」")
            elif kind == "生图工作台":
                _ensure_workbench()
                task = workbench_map.get(name)
                if task:
                    _collect_image(kind, name, task.get("result_path"))
                else:
                    errors.append(f"生图工作台中找不到「{name}」")
            elif kind == "素材库":
                _ensure_assets()
                asset = asset_map.get(name)
                if asset:
                    _collect_image(kind, name, asset.get("file_path"))
                else:
                    errors.append(f"素材库中找不到「{name}」")
            return ""

        text = re.sub(r"\{(角色库|场景库|生图工作台|素材库):([^}]+)\}", _replace, template)

        if errors:
            raise ValueError("提示词引用解析失败:\n  " + "\n  ".join(errors))

        return text, ref_images, characters_found, scenes_found

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
