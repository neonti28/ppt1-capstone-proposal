p = "/mnt/d/Capstone 1(v2)/scratch/rnd_e1/e1_doc.py"
s = open(p).read()

a = 'w("Bacaan cepat kolom terakhir: yang paling sering muncul `0/T` adalah metode yang prasyarat fisiknya "\n  "tidak terpenuhi, bukan metode yang jelek.")'
b = 'w("Bacaan cepat: sel `0/T` menandai prasyarat fisik yang tidak terpenuhi, misalnya laju sampel di bawah "\n  "pita diagnostik, bukan penilaian bahwa metodenya jelek.")'
assert a in s, "kalimat bacaan cepat tidak ditemukan"
s = s.replace(a, b)

c = 'w("Catatan kejujuran atas tabel ini: lima rujukan pertama terverifikasi pada lapis registrasi dan lapis "\n  "metadata. Enam rujukan terakhir adalah arXiv dan halaman prosiding, jadi tidak punya DOI; yang "\n  "diverifikasi adalah URL terbuka dengan judul yang cocok, bukan DOI. Isi penuh 4 dari 11 rujukan tidak "\n  "dibaca karena blokir penerbit, dan itu tidak dipakai sebagai dasar angka.")'
d = 'w("Catatan kejujuran atas tabel ini: tujuh rujukan pertama terverifikasi pada lapis registrasi (doi.org) "\n  "dan lapis metadata (Crossref), masing-masing 302 dan 200. Empat rujukan terakhir adalah arXiv dan "\n  "halaman prosiding, jadi tidak punya DOI; yang diverifikasi adalah URL terbuka dengan judul halaman yang "\n  "cocok, bukan DOI. Isi penuh sebagian rujukan tidak dibaca karena blokir penerbit, dan itu tidak "\n  "dipakai sebagai dasar angka.")'
assert c in s, "catatan rujukan tidak ditemukan"
s = s.replace(c, d)
open(p, "w").write(s)
print("ok")
