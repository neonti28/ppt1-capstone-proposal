B="/mnt/d/Capstone 1(v2)"
doc=open(B+"/docs/V10_E_STAT_BAB.md",encoding="utf-8").read()
flat=" ".join(doc.split())
print("thr semua 4 nilai (whitespace-normalized):",
      "2,4649 / 2,8219 / 2,7621 / 2,5144" in flat)
print("kosakata 7/11/27 hadir:", "7/11/27" in doc)
print("'27 head' hadir:", "27 head" in doc)
print("'11 klaim' hadir:", "11 klaim" in doc)
print("'7 engine' hadir:", "7 engine" in doc)
