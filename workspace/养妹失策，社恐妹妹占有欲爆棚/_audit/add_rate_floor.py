# -*- coding: utf-8 -*-
# 校验器：台词过慢（<3.3 汉字/秒）提示「镜头可能空」
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
anchor = 'notes.append(f"{tag} 镜头{sh[\'no\']:02d} 台词语速'
if anchor in t:
    print("已存在语速提示逻辑")
else:
    # 在语速超限检查附近加下限提示
    old = 'if rate > RATE_MAX:'
    idx = t.find(old)
    print("找到语速检查:", idx != -1)
    if idx != -1:
        add = '''if rate < 3.3 and (d["end"] - d["start"]) >= 1.5:
                    notes.append(f"{tag} 镜头{sh['no']:02d} 语速 {rate:.1f} 字/秒偏慢（可按内容收 0.2~0.5s，别用镜头空转）")
                '''
        # 只插入一次，放在超限检查前
        t = t[:idx] + add + t[idx:]
        open(p, "w", encoding="utf-8").write(t)
        print("已加语速下限提示")
