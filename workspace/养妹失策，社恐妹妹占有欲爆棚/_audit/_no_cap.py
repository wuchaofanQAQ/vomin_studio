# -*- coding: utf-8 -*-
def rep(path, pairs):
    t = open(path, encoding="utf-8").read()
    for old, new in pairs:
        c = t.count(old)
        print(f"{path}: {c}  {old[:40]}")
        assert c == 1
        t = t.replace(old, new)
    open(path, "w", encoding="utf-8").write(t)

rep(r"skills\novel-to-drama\scripts\check_script.py", [
 ('("字数 1500~2500", 1500 <= s["chars"] <= 2500, f"{s[\'chars\']}"),',
  '("字数 ≥1500（上限交给分镜时长，单集 ≤180 秒）", s["chars"] >= 1500, f"{s[\'chars\']}"),'),
])

rep(r"skills\novel-to-drama\references\adaptation-rules.md", [
 ("| 剧本字数 | 1500~2500 | 低于 1500 基本撑不住 2 分钟 |",
  "| 剧本字数 | ≥1500 | 低于 1500 基本撑不住 2 分钟；**不设上限**，真实上限由分镜时长（单集 ≤180 秒）与段落数决定 |"),
 ("**禁止注水**：堆形容词、拉长环境描写、重复心理独白、加没有信息量的寒暄。宁可 1800 字全是戏，不要 2500 字一半是水。",
  "**禁止注水**：堆形容词、拉长环境描写、重复心理独白、加没有信息量的寒暄。判断标准是「有没有戏」，不是字数——别为了凑字数写水，也别为了压字数删戏。"),
])

rep(r"skills\novel-to-drama\SKILL.md", [
 ("密度指标见 `references/adaptation-rules.md` 十二（单集 1500~2500 字 / 可拆节拍 ≥40 / 台词 8~30）",
  "密度指标见 `references/adaptation-rules.md` 十二（单集 ≥1500 字，不设上限；可拆节拍 ≥40 / 台词 8~30）"),
])
print("cap removed")
