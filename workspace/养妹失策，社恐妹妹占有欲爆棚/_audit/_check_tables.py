# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
from vomin.feishu.bitable import FeishuBitable

ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
feis = ws.feishu
print("feishu client:", bool(feis))
tables = feis.discover_tables()
expected = set(FeishuBitable.EXPECTED_TABLES)
present = set(tables)
print("missing:", expected - present)
print("extra:", present - expected)
