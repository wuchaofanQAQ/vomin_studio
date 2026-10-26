import json, subprocess, sys, os
base = os.path.abspath(r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚")
out = subprocess.run([sys.executable, r"skills\novel-to-drama\scripts\check_coverage.py",
                      os.path.join(base, "_audit", "ep1_novel.txt"),
                      os.path.join(base, "_audit", "ep1_script.txt"), "--json"],
                     capture_output=True, text=True, encoding="utf-8")
d = json.loads(out.stdout)
print("覆盖率", f"{d['coverage']:.0%}", "| 硬问题", d["hard_count"], "| 台词丢失", len(d["missing_quotes"]))
for h in d["hard"]:
    print(" -", h["text"])
