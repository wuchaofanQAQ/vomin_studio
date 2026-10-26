# -*- coding: utf-8 -*-
import re

# A. 校验器支持「待出图：【名】」
cp = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(cp, encoding="utf-8").read()
old = '''            m = re.match(r"^待补：【([^】]+)】", line)'''
new = '''            m = re.match(r"^待补：【([^】]+)】", line)
            if not m:
                m = re.match(r"^待出图：【([^】]+)】", line)'''
assert t.count(old) == 1
t = t.replace(old, new)
open(cp, "w", encoding="utf-8").write(t)
print("checker: 待出图 支持")

# B. 分镜：无图道具改为待出图，映射去掉它们并重排编号
f = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚\drafts\ep01m_storyboard_v1.md"
s = open(f, encoding="utf-8").read()

for name in ("手机", "玻璃杯"):
    s = s.replace(f"【{name}】：{{道具库：{name}}}\n", f"待出图：【{name}】\n")

# 映射：删掉 图N=【手机】/【玻璃杯】 并重排
def fix_map(m):
    items = [x for x in m.group(1).split("；") if "【手机】" not in x and "【玻璃杯】" not in x]
    return "【参考图映射】" + "；".join(f"图{i+1}={x.split('=',1)[1]}" for i, x in enumerate(items))
s = re.sub(r"【参考图映射】([^\n]+)", fix_map, s)

# p02/p03 加黑拖鞋待出图
s = s.replace("待出图：【手机】\n\n【本段现场生成】\n回忆两镜", "待出图：【手机】\n待出图：【黑拖鞋】\n\n【本段现场生成】\n回忆两镜", 1)
s = s.replace("待出图：【玻璃杯】\n\n【本段现场生成】\n42码旧塑料黑拖鞋", "待出图：【玻璃杯】\n待出图：【黑拖鞋】\n待出图：【手机】\n\n【本段现场生成】\n42码旧塑料黑拖鞋", 1)
s = s.replace("待出图：【玻璃杯】\n\n【本段现场生成】\n手机屏幕冷白", "待出图：【玻璃杯】\n待出图：【手机】\n\n【本段现场生成】\n手机屏幕冷白", 1)
open(f, "w", encoding="utf-8").write(s)
print("storyboard: 无图道具改待出图")
