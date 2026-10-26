import io, os, sys
base = r"workspace\养妹失策，社恐妹妹占有欲爆棚"
draft = os.path.join(base, "drafts", "ep01_storyboard.md")
text = open(draft, encoding="utf-8").read()
segs = []
for i in range(1, 7):
    p = os.path.join(base, "_audit", f"seg_p{i:02d}.md")
    segs.append(open(p, encoding="utf-8").read().strip())
start = text.index("## 第01段")
end = text.index("## 资产映射表")
head, tail = text[:start], text[end:]
new = head + ("\n\n---\n\n".join(segs)) + "\n\n---\n\n" + tail
open(draft, "w", encoding="utf-8").write(new)
print("spliced; chars:", len(new))
