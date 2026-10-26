import json, os, subprocess
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
desc = "精致酒红色亮面硬壳行李箱，24寸，玫瑰金包角，拉杆拉出，表面光洁无划痕"
out = subprocess.run(["python", r"skills\drama-asset-generation\scripts\asset_prompt.py", "build", "--type", "道具", "--desc", desc],
                     capture_output=True, text=True, encoding="utf-8")
prompt = out.stdout.strip()
json.dump([{"name": "行李箱", "gen_prompt": prompt}],
          open(os.path.join(base, "_audit", "write_luggage_final.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(prompt)
