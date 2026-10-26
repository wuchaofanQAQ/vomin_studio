import os, sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
import cli
from vomin.workspace import Workspace
ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
desc = "老式公寓走廊，浅灰地砖，深灰防盗门，西端窗光，白天，无人。\n空间锚点：入口=南侧中段防盗门，朝内开；地面=浅米灰地砖；主光=西端窗。"
img = cli._image_prompt_from_desc(desc)
print("scene image prompt:", img)
print("with style len:", len(cli._apply_global_style(ws, img)))
print("character fallback:", cli._image_prompt_from_desc("18岁清瘦男生，黑色微卷中长发，白T黑短裤人字拖"))
