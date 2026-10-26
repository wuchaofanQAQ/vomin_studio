import json, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
script = open(os.path.join(base, "drafts", "ep01_script_v2.md"), encoding="utf-8").read().strip()
rows = [{
  "episode": 1,
  "title": "如果你不想要我，我可以走",
  "script": script,
  "status": "草稿",
}]
json.dump(rows, open(os.path.join(base, "drafts", "ep01_row_v2.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("chars:", len(script))
