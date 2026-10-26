# -*- coding: utf-8 -*-
import sys, docx, json
from docx.document import Document as _Doc
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

p = r"C:\Users\Heart\Desktop\艺谋学长课程配套文件\基础通用提示词\剧本转提示词3.0.docx"
d = docx.Document(p)

def iter_block_items(parent):
    body = parent.element.body
    for child in body.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

lines = []
n = 0
for b in iter_block_items(d):
    if isinstance(b, Paragraph):
        txt = b.text.strip()
        if not txt:
            continue
        n += 1
        style = b.style.name if b.style is not None else ""
        lines.append(f"[P{n:03d}|{style}] {txt}")
    else:
        n += 1
        lines.append(f"[TABLE{n:03d}] rows={len(b.rows)} cols={len(b.columns)}")
        for r in b.rows:
            cells = [c.text.replace("\n"," / ").strip() for c in r.cells]
            lines.append("  | " + " | ".join(cells))
out = "\n".join(lines)
open(sys.argv[1], "w", encoding="utf-8").write(out)
print("paras:", len(lines), "chars:", len(out))
