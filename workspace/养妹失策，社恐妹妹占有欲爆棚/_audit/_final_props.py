import os, sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
f = ws.feishu
tables = f.discover_tables()
print("tables:", len(tables))
print("道具库:", tables.get("道具库"), "rows:", len(f.list_records(tables["道具库"])))
props = f.pull_props(ws)
print("pull_props:", len(props))
