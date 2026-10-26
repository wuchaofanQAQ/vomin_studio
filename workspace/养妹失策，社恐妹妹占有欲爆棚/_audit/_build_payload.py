import re, json, os
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚"
text = open(os.path.join(base, "drafts", "ep01_storyboard.md"), encoding="utf-8").read()
start = text.index("## 第01段")
end = text.index("## 资产映射表")
body = text[start:end]
parts = re.split(r"\n\n---\n\n", body)
rows = []
for p in parts:
    p = p.strip()
    if not p.startswith("## 第"):
        continue
    head, rest = p.split("\n", 1)
    m = re.match(r"## 第(\d+)段　(.+)$", head)
    no, title = int(m.group(1)), m.group(2).strip()
    rest = rest.strip()
    dur = re.search(r"本段总时长\s*(\d+)秒", rest).group(1)
    row = {
        "episode": "1",
        "shot_id": f"ep01_p{no:02d}",
        "title": title,
        "prompt": rest,
        "char_lock": "沈幼怡、陈诚",
        "env_lock": "",
        "timeline": f"00:00-00:{int(dur):02d}",
        "status": "待生成",
    }
    rows.append(row)
    print(row["shot_id"], title, len(rest), row["timeline"])
json.dump(rows, open(os.path.join(base, "_audit", "storyboard_v2_payload.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows:", len(rows))
