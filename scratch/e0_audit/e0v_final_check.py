import re
import json

DOC = "/mnt/d/Capstone 1(v2)/docs/RND_E0_AUDIT_ENGINE.md"
LED = "/mnt/d/Capstone 1(v2)/docs/RND_PROVENANCE_LEDGER.md"
d = open(DOC, encoding="utf-8").read()
l = open(LED, encoding="utf-8").read()

print("baris dokumen:", d.count("\n") + 1)
print("em-dash:", d.count("\u2014"))
print("CJK:", len(re.findall(r"[\u4e00-\u9fff]", d)))
print("sisa '74,47%':", d.count("74,47%"))
print("baris Riset pendahuluan:", len(re.findall(r"^Riset pendahuluan:", d, re.M)))
for s in ["systematic-debugging", "statistical-analysis", "verification-mandatory", "file-editing"]:
    print("skill", s, "disebut:", d.count(s), "kali")
print("sequ disebut:", d.count("sequentialthinking"))
heads = re.findall(r"^### [0-9.]+ Temuan (S-\d)", d, re.M)
print("heading S di badan:", heads)
print("S di tabel ringkasan:", re.findall(r"^\| (S-\d) \|", d, re.M))
rows = re.findall(r"^\| (E0-\d+) \|", l, re.M)
print("baris ledger E0:", len(rows), "unik:", len(set(rows)), "terakhir:", rows[-3:])
print("baris ledger total:", len(re.findall(r"^\| [A-Z0-9]+-", l, re.M)))
print("kolom tabel ledger (header):", [c.strip() for c in l.split("\n")[21].split("|")] if "|" in l.split("\n")[21] else "cek")
print("em-dash ledger:", l.count("\u2014"))
print("CJK ledger:", len(re.findall(r"[\u4e00-\u9fff]", l)))
print("bagian 10 ada:", "## 10. VERIFIKASI ULANG INDEPENDEN" in d)
print("S-8 heading ada:", "Temuan S-8" in d)
