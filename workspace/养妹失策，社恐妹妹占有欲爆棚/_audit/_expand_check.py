import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
ws = Workspace(base)
doc = json.load(open(os.path.join(base, "drafts", "ep01_storyboard_v4.json"), encoding="utf-8"))
for s in doc["shots"]:
    try:
        out, refs, chars, _, audio = ws.expand_prompt(s["prompt"])
        print(f"{s['shot_id']} ok  refs={len(refs)}  剩余锚点={'{' in out}")
    except Exception as e:
        print(f"{s['shot_id']} FAIL: {e}")
