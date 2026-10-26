# -*- coding: utf-8 -*-
import sys, os, json
sys.path.insert(0, r"C:\Users\Heart\PycharmProjects\vomin_studio")
os.chdir(r"C:\Users\Heart\PycharmProjects\vomin_studio")
from dotenv import load_dotenv
load_dotenv()
from vomin.workspace import Workspace

ws = Workspace(r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚")
shots = ws.load_storyboard()
for s in shots:
    try:
        p, refs, chars, _, _ = ws.expand_prompt(s["prompt"])
        missing = [x for x in refs if not os.path.exists(x)]
        print(s["shot_id"], "refs", len(refs), "missing", len(missing), "chars", len(chars))
        if missing:
            print("  ", [os.path.basename(x) for x in missing])
    except Exception as e:
        print(s["shot_id"], "ERROR", e)
