# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
t = open(p, encoding="utf-8").read()
anchor = "    def load_settings(self) -> list[dict]:"
restore = '''    def load_scenes(self) -> list[dict]:
        return self._load_from_feishu("scenes", "pull_scenes", "scenes.json")

    def save_scenes(self, data: list[dict]):
        self.save_json("scenes.json", data)
        self._cache["scenes"] = data

    def load_props(self) -> list[dict]:
        return self._load_from_feishu("props", "pull_props", "props.json")

    def save_props(self, data: list[dict]):
        self.save_json("props.json", data)
        self._cache["props"] = data

'''
assert t.count(anchor) == 1
assert "def load_scenes" not in t
t = t.replace(anchor, restore + anchor)
open(p, "w", encoding="utf-8").write(t)
print("restored load/save scenes+props")
