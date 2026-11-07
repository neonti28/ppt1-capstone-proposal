"""Ekstrak teks proposal docx 13 Agu 2026 -> scratch/ppt1/docx_draft_text.txt (paragraf bernomor).

Dipakai untuk menelusuri daftar 14 BOK versi draft dan set 9 alternatif versi draft.
Jalankan ulang: python3 scratch/ppt1/extract_docx.py
"""
import re
import zipfile

SRC = "/mnt/d/Download/Dokumen Antah Berantah/Proposal_PPT_I_SperryDrilling_ML_NPT.docx"
DST = "/mnt/d/Capstone 1(v2)/scratch/ppt1/docx_draft_text.txt"

z = zipfile.ZipFile(SRC)
xml = z.read("word/document.xml").decode("utf8")
paras = re.split(r"</w:p>", xml)
lines = []
for i, pa in enumerate(paras):
    txt = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", pa, flags=re.S))
    txt = txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    lines.append(f"{i + 1}|{txt}")
with open(DST, "w", encoding="utf8") as f:
    f.write("\n".join(lines))
print("paragraf:", len(lines), "->", DST)
print("tabel:", len(re.findall(r"<w:tbl>", xml)))
