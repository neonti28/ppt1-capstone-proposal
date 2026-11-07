p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()

s = s.replace('w("### 5.2 Peringkat wakil terbaik per algoritma")',
              'w("### 5.2 Peringkat per engine sasaran")')
s = s.replace(
 'w("| # | Kode | Algoritma | Engine terbaik | Tier | Data | Risiko | Biaya | Skor |")',
 'w("| # | Kode | Algoritma | Engine sasaran | Tier | Data | Risiko | Biaya | Skor |")')

old = '''w("Kolom tier, data, risiko, biaya adalah skor komponen 0 sampai 3. Kolom Skor adalah hasil rumus 5.1.")'''
new = '''w("Engine sasaran adalah engine tempat algoritma itu direkomendasikan R1 sampai R6, bukan engine dengan "
  "skor tertinggi. Aturan ini dipakai supaya algoritma tidak diberi panggung pada engine yang jelas tidak "
  "membutuhkannya: tanpa aturan ini, Isolation Forest akan dinilai pada shk yang sudah berlabel dan "
  "tampak lebih baik daripada perannya yang sebenarnya, yaitu triase pada kelas tanpa label. Pemetaan "
  "engine sasaran ada di `scratch/rnd_e1/e1_build.py` konstanta `TARGET`.")
w("")
w("Kolom tier, data, risiko, biaya adalah skor komponen 0 sampai 3. Kolom Skor adalah hasil rumus 5.1. "
  "Algoritma dengan skor 0 tidak muncul karena gerbang tier memaksanya ke 0.")'''
assert old in s
s = s.replace(old, new)
open(p, "w").write(s)
print("ok")
