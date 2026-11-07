p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()

start = s.index("# --- verifikasi angka yang dikutip di bagian 7 tetapi belum punya baris ledger sendiri ---")
end = s.index('rows = []\ndef R(no, angka, satuan, kelas, rujuk, dipakai, status):')
block = s[start:end]
s = s[:start] + s[end:]

anchor = '''def R(no, angka, satuan, kelas, rujuk, dipakai, status):
    rows.append(f"| {no} | {angka} | {satuan} | {kelas} | {rujuk} | {TANGGAL} | {dipakai} | {status} |")
'''
assert anchor in s
s = s.replace(anchor, anchor + "\n" + block, 1)

s = s.replace(
 'f"Rekap kelas: 5 KONVENSI (E1-001..E1-004, E1-007), 8 DERIVASI (E1-005, E1-008, E1-009, "\n                  f"E1-011..E1-015), 2 RUN-KITA (E1-010, E1-019, E1-020), 1 JURNAL ditolak (E1-017), "\n                  f"1 BELUM (E1-018), 1 KONVENSI rubrik (E1-006), 1 KONVENSI hitungan (E1-016)."',
 'f"Rekap kelas: 7 KONVENSI (E1-001..E1-004, E1-006, E1-007, E1-016), 8 DERIVASI (E1-005, E1-008, "\n                  f"E1-009, E1-011..E1-015), 8 RUN-KITA (E1-010, E1-019, E1-020, E1-021..E1-025), "\n                  f"1 JURNAL ditolak (E1-017), 1 BELUM (E1-018)."')
open(p, "w").write(s)
print("moved")
