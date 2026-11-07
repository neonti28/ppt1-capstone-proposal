#!/usr/bin/env python3
"""Cek 9: bab mana yang memuat artefak literal \\n; keyword gap lintas kandidat."""
import json, os, re

BASE = "/mnt/d/Capstone 1(v2)/docs"
K1 = os.path.join(BASE, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md")
K2 = os.path.join(BASE, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md")


def section_of(text, pos):
    head = None
    for m in re.finditer(r"^#{1,3} .*$", text, re.M):
        if m.start() <= pos:
            head = m.group(0)
        else:
            break
    return head


t2 = open(K2, encoding="utf-8").read()
p = t2.find("v8_e_shk_02b")
print("=== artefak literal \\n ada di md kandidat_2? ===")
print("  jumlah '\\\\n' literal di md kandidat_2:", t2.count("\\n"))
print("  posisi v8_e_shk_02b -> seksi:", section_of(t2, p))

nb = json.load(open(os.path.join(BASE, "ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb")))
for i, c in enumerate(nb["cells"]):
    s = "".join(c.get("source", []))
    if "v8_e_shk_02b" in s:
        print(f"  sel ipynb #{i} tipe={c['cell_type']} literal_backslash_n={'yes' if chr(92)+'n' in s else 'no'}")
        print("  seksi kira-kira:", section_of(s, 0) or "(teks sel, bukan heading)")

print("\n=== keyword gap lintas kandidat (ML chapter) ===")
def ml1(t):
    return t[t.find("## 8. Data"):t.find("## 14. Arsitektur")]
def ml2(t):
    return t[t.find("## Bab 4: Labeling untuk Head ML"):t.find("## Bab 5: Metode Statistik")]

t1 = open(K1, encoding="utf-8").read()
KWS = ["deep learning", "Deep learning", "murni", "temporal", "Brier", "pemisahan peran",
       "lintas lapangan", "proxy", "kekuatan bukti", "tingkat pemakaian", "Lapisan B",
       "Lapisan C", "kejujuran", "stakeholder", "1,5"]
for k in KWS:
    a1 = len(re.findall(re.escape(k), ml1(t1), re.I))
    a1all = len(re.findall(re.escape(k), t1, re.I))
    b2 = len(re.findall(re.escape(k), ml2(t2), re.I))
    b2all = len(re.findall(re.escape(k), t2, re.I))
    print(f"  {k!r}: K1-babML={a1} K1-dok={a1all} | K2-babML={b2} K2-dok={b2all}")

print("\n=== apakah K1 punya baris 'Riset pendahuluan' / daftar sumber angka? ===")
print("  K1 'Riset pendahuluan':", len(re.findall("Riset pendahuluan", t1, re.I)))
print("  K1 'traceability'/sumber angka:", len(re.findall("sumber angka|traceability", t1, re.I)))
print("  K2 bab4 'SUMBER ANGKA':", len(re.findall("SUMBER ANGKA", ml2(t2), re.I)))
print("  K1 'Bab' structure? (## count):", len(re.findall(r"^## ", t1, re.M)))
print("  K1 ada tabel fold/AUPRC?", bool(re.search(r"AUPRC\s*[0-9]", t1)),
      "| ada '0,44'/'0.44'?", bool(re.search(r"0[,.]44\d", t1)))
print("  K1 sebut angka fold per kelas?", re.findall(r"\b(?:4|9|7)\s+lipatan|tujuh nilai lipatan", t1))
