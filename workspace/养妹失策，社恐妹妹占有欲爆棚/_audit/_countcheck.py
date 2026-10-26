# -*- coding: utf-8 -*-
p = r"skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()
old = '''        # 其它
        if "不显示任何字幕" not in (s["style"] + s["live"]):'''
new = '''        # 镜数声明
        cn = {"一":1,"二":2,"三":3,"四":4,"五":5,"六":6,"七":7,"八":8,"九":9,"十":10,
              "十一":11,"十二":12,"十三":13,"十四":14,"十五":15,"十六":16,"十七":17,"十八":18}
        mnum = re.search(r"([一二三四五六七八九十]+)镜按下列时码", s["style"])
        if mnum:
            claim = cn.get(mnum.group(1))
            if claim and claim != len(s["shots"]):
                errors.append(f"{tag} 声明「{mnum.group(1)}镜」但实际有 {len(s['shots'])} 个镜头")

        # 其它
        if "不显示任何字幕" not in (s["style"] + s["live"]):'''
assert t.count(old) == 1
open(p, "w", encoding="utf-8").write(t.replace(old, new))
print("shot-count check added")
