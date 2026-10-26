import re, json, os
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚"
text = open(os.path.join(base, "drafts", "ep01_storyboard.md"), encoding="utf-8").read()
body = text[text.index("## 第01段"):text.index("## 资产映射表")]
env = {
 1: "陈诚公寓门口", 2: "陈诚公寓门口", 3: "陈诚公寓门口",
 4: "陈诚公寓门口", 5: "陈诚公寓玄关客厅（日）、陈诚公寓门口",
 6: "陈诚公寓玄关客厅（日）",
}
rows = []
for p in re.split(r"\n\n---\n\n", body):
    p = p.strip()
    if not p.startswith("## 第"):
        continue
    head, rest = p.split("\n", 1)
    m = re.match(r"## 第(\d+)段　(.+)$", head)
    no, title = int(m.group(1)), m.group(2).strip()
    rest = rest.strip()
    dur = int(re.search(r"本段总时长\s*(\d+)秒", rest).group(1))
    rows.append({
        "episode": "1",
        "shot_id": f"ep01_p{no:02d}",
        "title": title,
        "prompt": rest,
        "char_lock": "沈幼怡、陈诚",
        "env_lock": env[no],
        "timeline": f"00:00-00:{dur:02d}",
        "status": "待生成",
    })
json.dump(rows, open(os.path.join(base, "_audit", "storyboard_v2_payload.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
for r in rows:
    print(r["shot_id"], r["timeline"], len(r["prompt"]), r["title"])
print("total chars:", sum(len(r["prompt"]) for r in rows))
