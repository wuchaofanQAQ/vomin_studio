# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\workspace.py"
w = open(p, encoding="utf-8").read()

pairs = [
("""                if sheet == "场景库":
                    # 一个场景一行，直接用场景名做键
                    mapping = {str(r.get("name", "")): r for r in rows if r.get("name")}
                    sheet_cache[sheet] = mapping
                else:
                    sheet_cache[sheet] = {str(r.get(key_field, "")): r for r in rows}""",
 """                sheet_cache[sheet] = {str(r.get(key_field, "")): r for r in rows}"""),
("""            if kind == "角色库" and name not in characters_found:
                characters_found.append(name)
            if kind == "场景库":
                base_name = name
                if base_name not in scenes_found:
                    scenes_found.append(base_name)
            _, _, file_fields = self.REF_SHEETS[kind]
            row = _row_map(kind).get(name)""",
 """            _, _, file_fields = self.REF_SHEETS[kind]
            row = _row_map(kind).get(name)
            if row:
                if row.get("kind") == "角色" and name not in characters_found:
                    characters_found.append(name)
                if row.get("kind") == "场景" and name not in scenes_found:
                    scenes_found.append(name)"""),
("{角色库：林砚}          → 收集角色的形象图（等价 {角色库:林砚}）", "{资产库：林砚}          → 收集角色的形象图（等价 {资产库:林砚}）"),
("{场景库：写字楼大堂}     → 收集场景的参考图", "{资产库：写字楼大堂}     → 收集场景的参考图"),
('f"引用角色请用 {{角色库：名字}}，引用场景请用 {{场景库：名字}}"', 'f"引用资产请用 {{资产库：名字}}"'),
]
for a, b in pairs:
    assert w.count(a) == 1, a[:40]
    w = w.replace(a, b)
open(p, "w", encoding="utf-8").write(w)
print("workspace expand_prompt 已通用化")

# ---------- bitable: 删旧方法 ----------
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
b = open(p2, encoding="utf-8").read()
for fn in ("pull_characters", "push_characters", "update_character", "pull_scenes", "push_scenes", "pull_props", "push_props", "update_scene", "update_prop"):
    marker = f"    def {fn}("
    if marker not in b:
        print("skip", fn); continue
    i = b.index(marker)
    j = b.find("\n    def ", i + 1)
    b = b[:i] + (b[j+1:] if j != -1 else "")
b = b.replace('"""检查标准表是否齐全（含道具库），缺失的自动创建。返回完整映射。"""', '"""检查标准表是否齐全（含资产库），缺失的自动创建。返回完整映射。"""')
open(p2, "w", encoding="utf-8").write(b)
print("bitable 旧方法已删")
