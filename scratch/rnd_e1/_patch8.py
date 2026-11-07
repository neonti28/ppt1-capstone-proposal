p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()
subs = [
 ('w("1. Matriks 28 algoritma x 7 engine berisi 196 sel, dan hanya 9 algoritma yang punya skor prioritas di "\n  "atas 2,0 dari skala 3.")',
  'w("1. Matriks {{N_ALG}} algoritma x 7 engine berisi 196 sel, dan {{N_GT2}} algoritma punya skor prioritas di "\n  "atas 2,0 dari skala 3.")'),
 ('w("4. Sebelas algoritma ditolak permanen dengan alasan fisik atau biaya, lima ditunda karena keadaan, dan "\n  "satu DOI conformal populer ditolak karena menunjuk makalah lain.")',
  'w("4. {{N_TOLAK}} algoritma atau keluarga algoritma ditolak permanen dengan alasan fisik atau biaya, "\n  "{{N_TUNDA}} ditunda karena keadaan, dan satu DOI conformal populer ditolak karena menunjuk makalah lain.")'),
]
for a, b in subs:
    assert a in s, a[:60]
    s = s.replace(a, b)
open(p, "w").write(s)
print("ok")
