# -*- coding: utf-8 -*-
p = r"vomin\workspace.py"
t = open(p, encoding="utf-8").read()

anchor = '''    def load_settings(self) -> list[dict]:'''
add = '''    def load_props(self) -> list[dict]:
        return self._load_from_feishu("props", "pull_props", "props.json")

    def save_props(self, data: list[dict]):
        self.save_json("props.json", data)
        self._cache["props"] = data

    def load_settings(self) -> list[dict]:'''
assert t.count(anchor) == 1
t = t.replace(anchor, add)

anchor2 = '''        "场景库": ("load_scenes", "name", ["ref_image"]),'''
add2 = '''        "场景库": ("load_scenes", "name", ["ref_image"]),
        "道具库": ("load_props", "name", ["ref_image"]),'''
assert t.count(anchor2) == 1
t = t.replace(anchor2, add2)

open(p, "w", encoding="utf-8").write(t)
print("workspace.py patched")
