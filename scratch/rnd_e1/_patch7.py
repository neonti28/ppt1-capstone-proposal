p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_build.py"
s = open(p).read()

subs = [
 ('"stuck": (2, "SEBAGIAN", "B1 0 sampai 0,115 adalah masalah daya deteksi, conformal hanya mengendalikan alarm (ledger R4-10)")',
  '"stuck": (2, "SEBAGIAN", "B1 0 sampai 0,115 adalah masalah daya deteksi, conformal hanya mengendalikan alarm (ledger R2-015)")'),
 ('"hyd": (3, "ADA", "satu-satunya gerbang yang tersisa pada kandidat terkuat adalah FAR 14,6 sampai 58,4 (ledger R1-032)")',
  '"hyd": (3, "ADA", "satu-satunya gerbang yang tersisa pada kandidat terkuat adalah FAR 14,6 sampai 58,4 (ledger E1-021)")'),
 ('"stuck": (1, "SEBAGIAN", "median episode 1,0 menit berarti memori hampir nol sehingga orde-1 tidak informatif (ledger R4-10)")',
  '"stuck": (1, "SEBAGIAN", "median episode satu menit berarti memori hampir nol sehingga orde-1 tidak informatif (R2 bagian 3)")'),
 ('"hyd": (0, "SEBAGIAN", "laju alarm 6,65 kali parameter, tidak layak menetapkan laju (ledger R5-045)")',
  '"hyd": (0, "SEBAGIAN", "laju alarm 6,65 kali parameter, tidak layak menetapkan laju (ledger E1-026)")'),
]
for a, b in subs:
    assert a in s, a[:60]
    s = s.replace(a, b)
open(p, "w").write(s)

q = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
t = open(q).read()
old = '''    ("E1-025", "1,46 sampai 71,7", "cakupan waktu teramati per well (persen)", _e0, "1,46% sampai 71,7",
     "docs/RND_E0_AUDIT_ENGINE.md temuan Kritis K-4", "bagian 7, 9"),
]'''
new = '''    ("E1-025", "1,46 sampai 71,7", "cakupan waktu teramati per well (persen)", _e0, "1,46% sampai 71,7",
     "docs/RND_E0_AUDIT_ENGINE.md temuan Kritis K-4", "bagian 7, 9"),
    ("E1-026", "6,65", "rasio laju alarm One-Class SVM terhadap parameter nu", _r5, "6,65",
     "docs/RND_R5_DRIFT.md bagian 5 tabel skor (baris One-Class SVM)", "bagian 3.5 A23"),
]'''
assert old in t
t = t.replace(old, new)
t = t.replace('_e0 = _baca("docs/RND_E0_AUDIT_ENGINE.md")',
              '_e0 = _baca("docs/RND_E0_AUDIT_ENGINE.md")\n_r5 = _baca("docs/RND_R5_DRIFT.md")')
t = t.replace('f"E1-009, E1-011..E1-015), 8 RUN-KITA (E1-010, E1-019, E1-020, E1-021..E1-025), "',
              'f"E1-009, E1-011..E1-015), 9 RUN-KITA (E1-010, E1-019, E1-020, E1-021..E1-026), "')
open(q, "w").write(t)
print("ok")
