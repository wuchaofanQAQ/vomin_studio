# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\SKILL.md"
t = open(p, encoding="utf-8").read()

# 1) 新增四条官方固定规则（放在写法密度后面）
anchor = "## 镜头写法速查"
add = """## 官方模型规则（2.5 实测）

四条固定动作，每段都要做到：

1. **台词只出现一次**：`00:05-00:06，R01沈幼怡（…地说）：「…」`，后面不再复述这句话；复述+追加情绪最容易诱发字幕。
2. **画面声明**：`【本段整体基准】` 末尾固定加一句 `画面内除指定屏幕文字外，不显示任何字幕、水印与台标。`
3. **一镜一种运镜**：推、拉、摇、移、跟、环绕、固定任选其一；要复合运动就拆镜。
4. **情绪写外化动作**：不写"悲伤/愤怒"，写"肩膀微颤、眼眶泛红、手指攥紧衣角"（见 `prompt-density.md` 第八节、`seedance-official.md` 第三节）。

其余：单段 30 秒上限、单次最多 50 个参考素材、角色按首次出场顺序绑定；屏幕文字只写一次并声明无其他字幕。

"""
assert t.count(anchor) == 1
t = t.replace(anchor, add + anchor)

# 2) References 表加一行
old_row = "| `references/seedance-25-rules.md` |"
new_row = "| `references/seedance-official.md` | 官方 2.5/2.0 规则：30s/50 素材、提示词四段式、动作量化、字幕诱发、角色对应错误 | 每次写段 |\n| `references/seedance-25-rules.md` |"
assert t.count(old_row) == 1
t = t.replace(old_row, new_row)
open(p, "w", encoding="utf-8").write(t)
print("SKILL official rules added")

# 3) 校验器：画面声明
p2 = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t2 = open(p2, encoding="utf-8").read()
old = '''    live = s.get("live", "")'''
new = '''    if "不显示任何字幕" not in (s.get("style", "") + s.get("live", "")):
        out.append(f"{tag} 缺画面声明：整体基准末尾加「画面内除指定屏幕文字外，不显示任何字幕、水印与台标。」")
    live = s.get("live", "")'''
assert t2.count(old) == 1
t2 = t2.replace(old, new)
open(p2, "w", encoding="utf-8").write(t2)
print("checker subtitle guard added")
