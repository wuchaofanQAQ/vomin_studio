#!/usr/bin/env python3
"""把 drafts/epNN_script.md 组装成 剧本表 写入载荷（本地生成，不写飞书）。"""
import json
import os

WS = r"C:\Users\Heart\PycharmProjects\vomin_studio\workspace\养妹失策，社恐妹妹占有欲爆棚"


def main():
    with open(os.path.join(WS, "episodes.json"), encoding="utf-8") as f:
        episodes = json.load(f)

    rows = []
    for ep in episodes:
        num = str(ep["episode"])
        path = os.path.join(WS, "drafts", f"ep{int(num):02d}_script.md")
        if not os.path.exists(path):
            print(f"  跳过第{num}集：缺 {path}")
            continue
        with open(path, encoding="utf-8") as f:
            script = f.read().strip()
        first_line = (ep.get("novel_text") or "").strip().splitlines()
        chapter = first_line[0].strip() if first_line else ""
        rows.append({
            "episode": num,
            "title": ep.get("title", ""),
            "novel_chapter": chapter,
            "novel_text": ep.get("novel_text", ""),
            "script": script,
            "status": "草稿",
        })

    out = os.path.join(WS, "drafts", "_write_episodes.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"已生成 {len(rows)} 条载荷 -> {out}")
    for r in rows:
        print(f"  第{r['episode']}集 {r['title']} | {r['novel_chapter']} | 剧本 {len(r['script'])} 字 | {r['status']}")


if __name__ == "__main__":
    main()
