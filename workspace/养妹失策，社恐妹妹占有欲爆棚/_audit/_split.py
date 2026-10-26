import json, io, os, sys, re
p = sys.argv[1]
raw = open(p, encoding="utf-8").read()
i = raw.find("[")
data = json.loads(raw[i:])
outdir = os.path.splitext(p)[0] + "_segs"
os.makedirs(outdir, exist_ok=True)
for r in data:
    sid = r.get("shot_id")
    txt = r.get("prompt", "")
    hdr = f"SHOT_ID: {sid}\nTITLE: {r.get('title')}\nTIMELINE: {r.get('timeline')}\nCHAR_LOCK: {r.get('char_lock')}\nENV_LOCK: {r.get('env_lock')}\nSTATUS: {r.get('status')}\nCHARS: {len(re.sub(chr(92)+'s+','',txt))}\n\n"
    open(os.path.join(outdir, sid + ".md"), "w", encoding="utf-8").write(hdr + txt)
    print(sid, len(txt), len(re.sub(r"\s+","",txt)), r.get("timeline"))
