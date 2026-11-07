p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()
a = 'w("4. {{N_TOLAK}} algoritma atau keluarga algoritma ditolak permanen dengan alasan fisik atau biaya, "'
b = 'w("4. Sebanyak {{N_TOLAK}} algoritma atau keluarga algoritma ditolak permanen dengan alasan fisik atau biaya, "'
assert a in s
open(p, "w").write(s.replace(a, b))
print("ok")
