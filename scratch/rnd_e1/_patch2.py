import re
p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()

s = s.replace(
 'w("| Algoritma dengan skor prioritas di atas 2,0 | 9 dari 28 |")',
 'w("| Algoritma dengan skor prioritas di atas 2,0 | {{N_GT2}} dari {{N_ALG}} |")')
s = s.replace(
 'w("| Ditolak permanen | 11 algoritma atau keluarga algoritma |")',
 'w("| Ditolak permanen | {{N_TOLAK}} algoritma atau keluarga algoritma |")')
s = s.replace(
 'w("| Ditunda | 5 algoritma atau keluarga algoritma |")',
 'w("| Ditunda | {{N_TUNDA}} algoritma atau keluarga algoritma |")')

old_write = '''doc = "\\n".join(L)
open(DOC, "w", encoding="utf-8").write(doc)'''
new_write = '''doc = "\\n".join(L)

# hitung jumlah baris nyata tiap tabel keputusan, lalu subsitusi placeholder
def rows_of(sec_start, sec_end):
    txt = doc.split(sec_start)[1].split(sec_end)[0]
    return [ln for ln in txt.splitlines() if ln.startswith("| ") and not ln.startswith("| Algoritma |")]

n_tolak = len(rows_of("### 8.1 Ditolak permanen", "### 8.2 Ditunda"))
n_tunda = len(rows_of("### 8.2 Ditunda", "### 8.3 Yang ditolak sebagai rujukan"))
n_gt2 = sum(1 for r in D["peringkat_algoritma"] if r["skor_prioritas"] > 2.0)
n_alg = len(D["matriks"])
assert n_tolak > 0 and n_tunda > 0, (n_tolak, n_tunda)
doc = (doc.replace("{{N_TOLAK}}", str(n_tolak))
          .replace("{{N_TUNDA}}", str(n_tunda))
          .replace("{{N_GT2}}", str(n_gt2))
          .replace("{{N_ALG}}", str(n_alg)))
assert "{{" not in doc, "placeholder tersisa"
open(DOC, "w", encoding="utf-8").write(doc)'''
assert old_write in s
s = s.replace(old_write, new_write)

s = s.replace(
 'R("E1-016", "11 / 5", "algoritma ditolak / ditunda", "KONVENSI", "hitungan baris tabel `docs/RND_E1_MATRIKS.md` bagian 8.1 dan 8.2", "bagian 0, 8", "TERVERIFIKASI (hitung baris tabel)")',
 'R("E1-016", f"{n_tolak} / {n_tunda}", "algoritma ditolak / ditunda", "KONVENSI", "hitungan baris tabel `docs/RND_E1_MATRIKS.md` bagian 8.1 dan 8.2, dihitung ulang oleh `rows_of()` di `e1_doc.py`", "bagian 0, 8", "TERVERIFIKASI (hitung baris tabel)")')
s = s.replace(
 'R("E1-015", str(len(b_b)), "algoritma", "DERIVASI", "hitung dari `e1_scores.json` `peringkat_algoritma` dengan ambang skor > 2,0", "bagian 0", "TERVERIFIKASI (hitung ulang di `e1_doc.py`)")',
 'R("E1-015", str(n_gt2), "algoritma", "DERIVASI", "hitung dari `e1_scores.json` peringkat_algoritma dengan ambang skor > 2,0", "bagian 0", "TERVERIFIKASI (hitung ulang di `e1_doc.py`)")')
s = s.replace('b_b = [r for r in D["peringkat_algoritma"] if r["skor_prioritas"] > 2.0]\n', '')
open(p, "w").write(s)
print("ok")
