import os, sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
import cli
from vomin.workspace import Workspace
ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
short = "18岁清瘦男生，黑色微卷中长发，白T黑短裤人字拖，全身正面"
out = cli._apply_global_style(ws, short)
print("short in:", len(short), "->", len(out))
print(out[:120], "...")
longp = "【任务】" + "测试"*80
print("long unchanged:", cli._apply_global_style(ws, longp) == longp)
