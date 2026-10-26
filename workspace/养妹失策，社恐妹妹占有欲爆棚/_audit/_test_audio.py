import sys, os
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
ws = Workspace(r"workspace\养妹失策，社恐妹妹占有欲爆棚")
prompt = """【本段资产锁定】
角色：【R01｜沈幼怡：{角色库：沈幼怡}】
音频参考：【沈幼怡：{音色库：沈幼怡-清冷少女}】
"""
out, refs, chars, _, audio = ws.expand_prompt(prompt)
print("--- 展开后 ---")
print(out)
print("chars:", chars)
print("audio:", audio)
