# -*- coding: utf-8 -*-
import re

# 1) 校验器：没有参考图映射行时，参考图数按锁定带图资产算
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = 'if map_names and map_names != img_locked:'
new = 'if map_names and map_names != img_locked:'
# 找到打印参考图的那行
t = t.replace('print(f"  ✓ 参考图 {[len(s[\'map\']) for s in segs]}")',
              'print(f"  ✓ 参考图 {[len(s[\'map\']) or len([e for e in s[\'lock\'] if e[\'table\'] in IMG_TABLES]) for s in segs]}")')
open(p, "w", encoding="utf-8").write(t)

# 2) SKILL.md 锁定格式示例更新
p2 = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\SKILL.md"
g = open(p2, encoding="utf-8").read()
old_ex = """场景：【陈诚公寓门口】：{资产库：陈诚公寓门口}
角色：【沈幼怡】：{资产库：沈幼怡}【陈诚】：{资产库：陈诚}
道具：【行李箱】：{资产库：行李箱}"""
new_ex = """角色：
图1 =【沈幼怡】 = {资产库：沈幼怡}
图2 =【陈诚】 = {资产库：陈诚}
场景：
图3 =【陈诚公寓门口】 = {资产库：陈诚公寓门口}
道具：
图4 =【行李箱】 = {资产库：行李箱}
待出图：
【玻璃杯】"""
if old_ex in g:
    g = g.replace(old_ex, new_ex)
    open(p2, "w", encoding="utf-8").write(g)
    print("SKILL 锁定格式示例已更新")
else:
    print("未找到旧示例，需手工确认")
