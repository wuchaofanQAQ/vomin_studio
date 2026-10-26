import shutil, os
src = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\workspace\\养妹失策，社恐妹妹占有欲爆棚\_audit\mom42_raw.txt"
dst = r"C:\\Users\\Heart\\PycharmProjects\\vomin_studio\\skills\\drama-segment-generation\references\mother-prompt-42.md"
raw = open(src, encoding="utf-8").read()
head = "# 剧本转提示词 4.2 · 导演级视频提示词通用母版（原文）\n\n> 本文件为 4.2 母版原文（逐条），与本项目冲突时以本文为准。项目适配见 `project-adaptation.md`。\n\n"
open(dst, "w", encoding="utf-8").write(head + raw)
print("written", dst, len(raw))
