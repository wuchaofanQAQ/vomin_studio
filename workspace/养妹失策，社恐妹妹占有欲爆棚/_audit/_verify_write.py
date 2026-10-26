import json, subprocess, os, re
base = os.path.abspath(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚")
def read(table):
    out = subprocess.run(["python", "cli.py", "read", base, "--table", table],
                         capture_output=True, text=True, encoding="utf-8", cwd=r"C:\Users\Heart\PycharmProjects\vomin_studio")
    s = out.stdout
    m = list(re.finditer(r"(?m)^\[$", s))
    return json.loads(s[m[-1].start():]) if m else []
scenes = read("场景库")
props = read("道具库")
print("场景:", len(scenes))
for s in scenes:
    print(" ", s["name"], "| 图:", bool(s.get("ref_image")), "| 描述:", (s.get("description") or "")[:30])
print("道具:", len(props))
for p in props:
    print(" ", p["name"], "|", p.get("prop_type"), "|", p.get("description"), "| 状态:", p.get("gen_status"))
