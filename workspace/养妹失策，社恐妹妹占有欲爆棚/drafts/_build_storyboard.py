#!/usr/bin/env python3
"""从 ep01_storyboard.md 组装 剧本分镜表 写入载荷（每段一行）。"""
import json
import re
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
SRC = WS / "drafts" / "ep01_storyboard.md"
OUT = WS / "drafts" / "_write_storyboard.json"

CHARACTERS = {"陈诚", "沈幼怡", "林女士", "沈崇山", "陈诚生父", "沈幼怡生母"}
DESC = {
    1: "沈幼怡在烈日下按门铃，把手机怼进门缝自报身份，陈诚开门。",
    2: "陈诚堵门追问“你爸呢”，沈幼怡转屏递消息，陈诚看到母亲的未读微信。",
    3: "六年前生日，林女士跟着沈崇山离开，小陈诚独自吃完那块蛋糕。",
    4: "沈幼怡一个字一个字打出“如果你不想要我，我可以走”，陈诚看完别开眼。",
    5: "陈诚说“我这儿不是民宿”，把门关上；沈幼怡弯腰去拎行李箱。",
    6: "陈诚回屋码字却坐不住，从猫眼看到她还站着，开门拎起行李箱。",
    7: "沈幼怡进门脱鞋，手机收到“你哥哥会照顾好你的”，陈诚冷笑。",
}

SEG_RE = re.compile(r"^##\s*第(\d+)段\s*(.+)$")
DLG_RE = re.compile(r"^【对白\s*[\d.]+-[\d.]+s】(.+)$")
ASSET_RE = re.compile(r"【([^【】]+)】")


def main() -> None:
    lines = SRC.read_text(encoding="utf-8").splitlines()
    segs, cur = [], None
    for ln in lines:
        s = ln.strip()
        m = SEG_RE.match(s)
        if m:
            cur = {"no": int(m.group(1)), "dur": 0, "body": [], "dialogue": [], "assets": []}
            segs.append(cur)
            continue
        if cur is None:
            continue
        if s.startswith("## "):
            cur = None
            continue
        d = re.search(r"本段总时长\s*([\d.]+)\s*秒", s)
        if d:
            cur["dur"] = float(d.group(1))
        cur["body"].append(ln)
        if s.startswith("【本段资产锁定】"):
            cur["_in_assets"] = True
            continue
        if s in ("【本段现场生成】", "【本段整体基准】", "【本段初始空间】"):
            cur["_in_assets"] = False
        if cur.get("_in_assets") and s.startswith("【"):
            cur["assets"] += ASSET_RE.findall(s)
        m = DLG_RE.match(s)
        if m:
            cur["dialogue"].append(m.group(1).strip().replace(" 内心独白：", "（画外）："))

    shots = []
    for seg in segs:
        chars = [a for a in seg["assets"] if a in CHARACTERS]
        scenes = [a for a in seg["assets"] if a not in CHARACTERS]
        dur = seg["dur"]
        shots.append({
            "shot_id": f"ep01_p{seg['no']:02d}",
            "episode": 1,
            "shot_number": f"P{seg['no']:02d}",
            "timeline": f"00:00-00:{int(dur):02d}",
            "dialogue": "\n".join(seg["dialogue"]),
            "scene_desc": DESC.get(seg["no"], ""),
            "char_lock": "、".join(chars),
            "env_lock": "、".join(scenes),
            "prompt": "\n".join(seg["body"]).strip(),
            "status": "待生成",
        })

    OUT.write_text(json.dumps(shots, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成 {len(shots)} 段 -> {OUT.name}")
    for sh in shots:
        print(f"  {sh['shot_id']} {sh['timeline']} 场景={sh['env_lock']} 提示词 {len(sh['prompt'])} 字")


if __name__ == "__main__":
    main()
