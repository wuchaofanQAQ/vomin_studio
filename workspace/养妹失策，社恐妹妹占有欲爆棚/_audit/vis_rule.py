# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\skills\drama-segment-generation\scripts\check_segment_prompt.py"
t = open(p, encoding="utf-8").read()

old = '''        # 镜头写法'''
new = '''        # 可见性：近景/特写里不得写画外资产（除非带位置词）
        LAYER = ["前景", "中景", "后景", "画左", "画右", "画面", "入画", "反射", "影子", "虚化", "画外"]
        for sh in s["shots"]:
            body_ = sh["body"]
            size = next((x for x in SHOT_SIZE if x in body_[:40]), "")
            if size not in ("近景", "特写", "大特写"):
                continue
            found = BODY_ASSET_RE.findall(body_)
            if not found:
                continue
            subj = found[0]
            for nm in dict.fromkeys(found):
                if nm == subj:
                    continue
                for m in re.finditer("【" + re.escape(nm) + "】", body_):
                    ctx = body_[max(0, m.start() - 18):m.end() + 12]
                    if not any(w in ctx for w in LAYER):
                        errors.append(f"{tag} 镜头{sh['no']:02d} {size}里写了画外资产【{nm}】，"
                                      f"应改写成画面方向（画左/画右/画外）或补位置词")

        # 镜头写法'''
assert t.count(old) == 1
t = t.replace(old, new)
open(p, "w", encoding="utf-8").write(t)
print("visibility rule added")
