# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

t = t.replace('''                "sections": set(),''', '''                "sections": set(),
                "live": "",''')

t = t.replace('''        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")''',
'''        if line.startswith("【本段现场生成】"):
            cur["in_lock"] = False
            cur["sections"].add("live")
            cur["live"] = line''')

t = t.replace('''        ("格式/时间/资产/台词错误 = 0", not errors, f"{len(errors)} 处"),''',
'''        ("写法密度", density_ok, density_note),
        ("格式/时间/资产/台词错误 = 0", not errors, f"{len(errors)} 处"),''')

# 密度检查函数 + 调用
old = '''def check(doc: list[dict], registry: dict[str, str], target: int | None)'''
new = '''def _block_len(line: str) -> int:
    s = line.split("】", 1)[-1] if line.startswith("【") else line
    return len(re.sub(r"\\s", "", s))


def density_issues(s: dict) -> list[str]:
    """写法密度：整体基准/现场生成/初始空间/终态/单镜的最低字数。"""
    out = []
    tag = f"第{s['no']:02d}段"
    rules = [("整体基准", s.get("style", ""), 150),
             ("初始空间", s.get("space", ""), 90),
             ("终态", s.get("final", ""), 40)]
    for name, line, need in rules:
        n = _block_len(line)
        if n < need:
            out.append(f"{tag} 【本段{name}】只 {n} 字，要求 ≥{need}")
    live = s.get("live", "")
    if _block_len(live) < 40 and "无" not in live.split("】")[-1]:
        out.append(f"{tag} 【本段现场生成】只 {_block_len(live)} 字，要求 ≥60（没有就写「无」）")
    for sh in s["shots"]:
        n = len(re.sub(r"\\s", "", sh["body"]))
        if n < 70:
            out.append(f"{tag} 镜头{sh['no']:02d} 正文只 {n} 字，要求 ≥70")
    return out


def check(doc: list[dict], registry: dict[str, str], target: int | None)'''
assert t.count(old) == 1
t = t.replace(old, new)

old2 = '''    checks = ['''
new2 = '''    dense = []
    for s in doc:
        dense.extend(density_issues(s))
    density_ok = not dense
    density_note = "全部达标" if density_ok else f"{len(dense)} 处不足"
    errors.extend(dense)

    checks = ['''
assert t.count(old2) == 1
t = t.replace(old2, new2)

open(p, "w", encoding="utf-8").write(t)
print("density checks added")
