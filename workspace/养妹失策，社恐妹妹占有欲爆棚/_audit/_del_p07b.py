import sys, json, os, requests
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
target = None
for r in fb.list_records(tid):
    f = r.get("fields", {})
    sid = f.get("镜头编号")
    if isinstance(sid, list):
        sid = sid[0].get("text") if sid else None
    if sid == "ep01_p07":
        target = r["record_id"]
print("p07:", target)
if target:
    resp = requests.delete(f"{fb._base(tid)}/{target}", headers=fb._headers(), timeout=15)
    print(resp.status_code, resp.json().get("code"), resp.json().get("msg"))
# 本地缓存清掉 p07，避免下次 push 复活
p = os.path.join(base, "storyboard.json")
rows = json.load(open(p, encoding="utf-8-sig"))
keep = [r for r in rows if str(r.get("shot_id")) != "ep01_p07"]
json.dump(keep, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("local rows:", len(rows), "->", len(keep))
