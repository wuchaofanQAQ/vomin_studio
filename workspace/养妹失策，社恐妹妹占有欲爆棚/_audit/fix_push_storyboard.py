# -*- coding: utf-8 -*-
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\vomin\feishu\bitable.py"
t = open(p, encoding="utf-8").read()

# 1) update_shot：去掉已删除的 人物锁定/环境锁定 字段，补 镜头标题
old = '''        fields = {
            "状态": shot.get("status", ""),
            "视频提示词": shot.get("prompt", ""),
            "人物锁定": shot.get("char_lock", ""),
            "环境锁定": shot.get("env_lock", ""),
            "时间线": shot.get("timeline", ""),
            "视频路径": shot.get("video_path") or "",
            "任务ID": shot.get("task_id") or "",
            "审核备注": shot.get("notes") or "",
        }'''
new = '''        fields = {
            "状态": shot.get("status", ""),
            "镜头标题": shot.get("title", ""),
            "视频提示词": shot.get("prompt", ""),
            "时间线": shot.get("timeline", ""),
            "视频路径": shot.get("video_path") or "",
            "任务ID": shot.get("task_id") or "",
            "审核备注": shot.get("notes") or "",
        }'''
assert t.count(old) == 1
t = t.replace(old, new)

# 2) push_storyboard 的 fields：去掉锁定字段（如果还有）
t = t.replace('                "人物锁定": shot.get("char_lock", ""),\n', "")
t = t.replace('                "环境锁定": shot.get("env_lock", ""),\n', "")
open(p, "w", encoding="utf-8").write(t)
print("update_shot/push_storyboard 已修；残留锁定字段:", t.count("人物锁定"), t.count("环境锁定"))
