# -*- coding: utf-8 -*-
import re

# 1) 分镜：图N =【名】  {资产库：名}；  去掉 = 前的等号，行尾补；
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

def fix_line(m):
    n, name, table, row = m.group(1), m.group(2), m.group(3), m.group(4)
    return f"图{n} =【{name}】  {{{table}：{row}}}；"

s = re.sub(r"^图\s*(\d+)\s*=\s*【([^】]+)】\s*=?\s*\{([^：}]+)[:：]([^}]+)\}；?\s*$",
           fix_line, s, flags=re.M)
open(f, "w", encoding="utf-8").write(s)
print("分镜锁定行已改格式")

# 2) 校验器：等号可选
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = r'LOCK_RE2 = re.compile(r"^图\s*(\d+)\s*=\s*【([^】]+)】\s*=\s*\{([^：}]+)[:：]([^}]+)\}")'
new = r'LOCK_RE2 = re.compile(r"^图\s*(\d+)\s*=\s*【([^】]+)】\s*=?\s*\{([^：}]+)[:：]([^}]+)\}")'
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("checker LOCK_RE2 已放宽")

# 3) SKILL 示例
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
g = open(p2, encoding="utf-8").read()
old_ex = """图1 =【沈幼怡】 = {资产库：沈幼怡}
图2 =【陈诚】 = {资产库：陈诚}
场景：
图3 =【陈诚公寓门口】 = {资产库：陈诚公寓门口}
道具：
图4 =【行李箱】 = {资产库：行李箱}"""
new_ex = """图1 =【沈幼怡】  {资产库：沈幼怡}；
图2 =【陈诚】  {资产库：陈诚}；
场景：
图3 =【陈诚公寓门口】  {资产库：陈诚公寓门口}；
道具：
图4 =【行李箱】  {资产库：行李箱}；"""
if old_ex in g:
    g = g.replace(old_ex, new_ex)
    open(p2, "w", encoding="utf-8").write(g)
    print("SKILL 示例已更新")
