# -*- coding: utf-8 -*-
p = r"cli.py"
t = open(p, encoding="utf-8").read()

# 1) helper
old = '''def _image_prompt_from_desc(desc: str) -> str:'''
new = '''def _fix_image_ext(abs_path: str) -> str:
    """接口可能返回 JPEG/WebP；按文件头把扩展名改对，避免 .png 里装 JPEG。"""
    try:
        with open(abs_path, "rb") as f:
            head = f.read(12)
    except OSError:
        return abs_path
    ext = ""
    if head.startswith(b"\\x89PNG"):
        ext = ".png"
    elif head.startswith(b"\\xff\\xd8\\xff"):
        ext = ".jpg"
    elif head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        ext = ".webp"
    if ext and not abs_path.lower().endswith(ext):
        new_path = os.path.splitext(abs_path)[0] + ext
        os.replace(abs_path, new_path)
        return new_path
    return abs_path


def _image_prompt_from_desc(desc: str) -> str:'''
assert t.count(old) == 1
t = t.replace(old, new)

# 2) 四处保存后校正扩展名
reps = [
('''        os.rename(paths[0], ws.abs(rel_path))
        char["ref_image"] = rel_path''',
 '''        os.rename(paths[0], ws.abs(rel_path))
        rel_path = ws.rel(_fix_image_ext(ws.abs(rel_path)))
        char["ref_image"] = rel_path'''),
('''        os.rename(paths[0], ws.abs(rel_path))
        scene["ref_image"] = rel_path''',
 '''        os.rename(paths[0], ws.abs(rel_path))
        rel_path = ws.rel(_fix_image_ext(ws.abs(rel_path)))
        scene["ref_image"] = rel_path'''),
('''        os.rename(paths[0], ws.abs(rel_path))
        prop["ref_image"] = rel_path''',
 '''        os.rename(paths[0], ws.abs(rel_path))
        rel_path = ws.rel(_fix_image_ext(ws.abs(rel_path)))
        prop["ref_image"] = rel_path'''),
]
for old, new in reps:
    c = t.count(old)
    print("count=", c)
    assert c == 1
    t = t.replace(old, new)

open(p, "w", encoding="utf-8").write(t)
print("patched")
