import re
B = "/mnt/d/Capstone 1(v2)"
doc = open(f"{B}/docs/RND_R7_REVIEW.md").read()
led = open(f"{B}/docs/RND_PROVENANCE_LEDGER.md").read()
print("baris dokumen:", doc.count("\n") + 1, "| karakter:", len(doc))
print("em_dash:", doc.count("\u2014"), "| en_dash:", doc.count("\u2013"))
cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff]", doc)
print("cjk:", len(cjk), cjk[:10])
print("bagian:", len(re.findall(r"^## ", doc, flags=re.M)))
print("judul bagian:", [m for m in re.findall(r"^## (.+)$", doc, flags=re.M)])
print("baris wajib riset pendahuluan:", "Riset pendahuluan: scientific-critical-thinking, statistical-analysis, verification-mandatory." in doc)
print("sequ pikiran disebut:", "6 pikiran" in doc)
print("ledger blok R7 ada:", "## Bagian R7: review R&D" in led)
print("jumlah blok R7 (harus 1):", led.count("## Bagian R7:"))
rows = re.findall(r"^\| R7-\d{3} \|", led, flags=re.M)
print("baris R7:", len(rows))
print("R7-001..R7-044 lengkap:", [f"R7-{i:03d}" for i in range(1, 45)] == [r.split("|")[1].strip() for r in rows])
print("em_dash ledger:", led.count("\u2014"))
for f in ["scratch/rnd/r7/r7_probe.json", "scratch/rnd/r7/r7_measure.json",
          "scratch/rnd/r7/r7_measure2.json", "scratch/rnd/r7/r7_delay.json",
          "scratch/rnd/r7/r7_doi.json", "scratch/rnd/r7/r7_ledger.py", "docs/RND_R7_REVIEW.md"]:
    import os
    p = f"{B}/{f}"
    print(f"{f}: ada={os.path.exists(p)} ukuran={os.path.getsize(p) if os.path.exists(p) else 0}")
