# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

helper = '''def _apply_global_style(ws, prompt: str) -> str:
    """短提示词（≤120 字，资产图）自动追加剧本设定的全局画风；长提示词视为已自带画风。"""
    gp = (ws.get_global_prompt() or "").strip()
    if gp and len(prompt) < 120 and gp[:12] not in prompt:
        return f"{prompt}，{gp}"
    return prompt


def _generate_character(ws, char, chars_list):'''
old = '''def _generate_character(ws, char, chars_list):'''
assert t.count(old) == 1
t = t.replace(old, helper)

# 角色
old = '''    final_prompt, _, _, _, _ = ws.expand_prompt(prompt_template, skip_self=("角色库", char["name"]))'''
new = '''    final_prompt, _, _, _, _ = ws.expand_prompt(prompt_template, skip_self=("角色库", char["name"]))
    final_prompt = _apply_global_style(ws, final_prompt)'''
assert t.count(old) == 1
t = t.replace(old, new)

# 场景
old = '''    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("场景库", label))'''
new = '''    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("场景库", label))
    final_prompt = _apply_global_style(ws, final_prompt)'''
assert t.count(old) == 1
t = t.replace(old, new)

# 道具
old = '''    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("道具库", label))'''
new = '''    final_prompt, ref_images, _, _, _ = ws.expand_prompt(
        prompt_template, skip_self=("道具库", label))
    final_prompt = _apply_global_style(ws, final_prompt)'''
assert t.count(old) == 1
t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("global style applied to short asset prompts")
