import json, os, subprocess
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
desc = "精致白色大号双肩书包，女生款，宽肩带，装得鼓囊囊"
out = subprocess.run(["python", r"skills\drama-asset-generation\scripts\asset_prompt.py", "build", "--type", "道具", "--desc", desc],
                     capture_output=True, text=True, encoding="utf-8")
prompt = out.stdout.strip()
json.dump([{"name": "双肩书包", "description": desc, "gen_prompt": prompt}],
          open(os.path.join(base, "_audit", "write_bag.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(prompt)
