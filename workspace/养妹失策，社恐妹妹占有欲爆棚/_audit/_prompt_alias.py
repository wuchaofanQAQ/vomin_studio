# -*- coding: utf-8 -*-
p = r"vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

# 角色库
old = '''            "外貌描述": char.get("appearance", ""),
            "生成提示词": char.get("gen_prompt", ""),'''
new = '''            "外貌描述": char.get("appearance", ""),
            "生成提示词": char.get("gen_prompt") or char.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''                "外貌描述": c.get("appearance", ""),
                "生成提示词": c.get("gen_prompt", ""),'''
new = '''                "外貌描述": c.get("appearance", ""),
                "生成提示词": c.get("gen_prompt") or c.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

# 场景库
old = '''            "生成提示词": scene.get("gen_prompt", ""),'''
new = '''            "生成提示词": scene.get("gen_prompt") or scene.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''                "生成提示词": s.get("gen_prompt", ""),'''
new = '''                "生成提示词": s.get("gen_prompt") or s.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

# 道具库
old = '''            "生成提示词": prop.get("gen_prompt", ""),'''
new = '''            "生成提示词": prop.get("gen_prompt") or prop.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

old = '''                "生成提示词": pr.get("gen_prompt", ""),'''
new = '''                "生成提示词": pr.get("gen_prompt") or pr.get("prompt", ""),'''
assert t.count(old) == 1
t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("prompt->gen_prompt fallback added")
