# -*- coding: utf-8 -*-
import io
import re
import docx

F = r"C:\Users\Heart\Desktop\艺谋学长课程配套文件\艺谋学长的爆款作品物料\《你的两千年修行之路》05集提示词+武戏改良版\你的两千年修行之路 第五集 Seedance2.5导演级视频提示词.docx"
d = docx.Document(F)
ps = [p.text.strip() for p in d.paragraphs if p.text.strip()]
io.open("tmp_ref_all.txt", "w", encoding="utf-8").write("\n".join(ps))

# 找"镜头"开头的行
shots = [x for x in ps if re.match(r"^(镜头|Shot|【镜头)", x)]
print("镜头行数", len(shots))
print("\n\n".join(shots[:8]))
