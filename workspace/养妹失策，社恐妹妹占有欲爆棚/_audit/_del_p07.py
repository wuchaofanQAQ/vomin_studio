import sys, os, json, requests
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
from vomin.feishu.bitable import FeishuBitable
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
cfg = ws.config
app_token = cfg.get("feishu", {}).get("app_token") or os.environ.get("FEISHU_BITABLE_APP_TOKEN")
tid = cfg.get("feishu", {}).get("tables", {}).get("剧本分镜表")
fb = FeishuBitable(app_token=app_token)
recs = fb.list_records(tid)
target = None
for r in recs:
    f = r.get("fields", {})
    sid = f.get("镜头编号")
    if isinstance(sid, list):
        sid = sid[0].get("text") if sid else None
    if sid == "ep01_p07":
        target = r["record_id"]
        break
print("p07 record:", target)
if target:
    url = f"{fb._base(tid)}/{target}"
    resp = requests.delete(url, headers=fb._headers(), timeout=15)
    print(resp.status_code, resp.json().get("code"), resp.json().get("msg"))
