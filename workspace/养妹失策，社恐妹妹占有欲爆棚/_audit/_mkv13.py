import json, re, os
base = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚"
md = open(os.path.join(base, "drafts", "ep01_storyboard_v13.md"), encoding="utf-8").read()
parts = re.split(r"(?m)^## (\u3010\u7b2c\d+\u6bb5\uff5c.+?\u3011)\s*$", md)
shots = []
for i in range(1, len(parts), 2):
    header = parts[i]; body = parts[i + 1].strip()
    m = re.match(r"\u3010\u7b2c(\d+)\u6bb5\uff5c([\d:.]+)-([\d:.]+)\uff5c(.+?)\u3011", header)
    no = int(m.group(1)); p = header + "\n\n" + body
    scene = re.findall(r"\u573a\u666f\uff1a\u3010S\d{2}\uff5c([^\uff1a\u3011]+)\uff1a", p)
    role_line = re.search(r"\u89d2\u8272\uff1a(.+)", p)
    roles = re.findall(r"\u3010R\d{2}\uff5c([^\uff1a\u3011]+)\uff1a", role_line.group(1)) if role_line else []
    shots.append({"shot_id": f"ep01_p{no:02d}", "episode": 1, "title": m.group(4),
                  "timeline": f"{m.group(2)}-{m.group(3)}", "prompt": p, "status": "\u5f85\u751f\u6210",
                  "env_lock": "\u3001".join(scene), "char_lock": "\u3001".join(r.strip() for r in roles)})
json.dump(shots, open(os.path.join(base, "drafts", "ep01_shots_v13.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("rows:", len(shots))
