# -*- coding: utf-8 -*-
import re
p = r"C:\Users\Heart\PycharmProjects\vomin_studio\cli.py"
c = open(p, encoding="utf-8").read()

# 1) push 命令里的旧三表
old_push = '''    print("\\n[角色库]")
    ws.feishu.push_characters(ws)
    print("\\n[场景库]")
    ws.feishu.push_scenes(ws)
    print("\\n[道具库]")
    ws.feishu.push_props(ws)
'''
if old_push in c:
    c = c.replace(old_push, '''    print("\\n[资产库]")
    try:
        ws.feishu.push_assets_lib(ws)
    except Exception as e:
        print(f"  跳过资产库: {e}")
''')
    print("push 已改")

# 2) init-from-url 的 pull 列表
c = c.replace('("pull_characters", "角色库"), ("pull_scenes", "场景库"),', '("pull_assets_lib", "资产库"),')

# 3) write 的复用跳过逻辑
c = c.replace('    if table in ("角色库", "场景库", "道具库"):', '    if table == "资产库":')

# 4) 帮助文本
c = c.replace('格式: 角色库:名 / 场景库:名 / 剧本分镜表:', '格式: 资产库:名 / 剧本分镜表:')
c = c.replace('--table 角色库 --data @characters.json', '--table 资产库 --data @assets.json')

# 5) 迁移动词里的旧描述（仅文案）
c = c.replace("补小说章节/小说内容与场景库新字段", "补对应原小说章节与资产字段")
c = c.replace("补小说字段与场景库新字段", "补小说字段与资产字段")

open(p, "w", encoding="utf-8").write(c)
print("cli 残留:", c.count("角色库"), c.count("场景库"), c.count("道具库"))
