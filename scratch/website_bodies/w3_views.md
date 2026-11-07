# W3 · Isi sepuluh tampilan

Kamu adalah pekerja konten untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki `js/views.js` saja. Jangan mengubah `js/data.js`, `js/app.js`, `index.html`, atau `css/styles.css`.

## Target
1. Sepuluh view harus terisi maksimal, bukan kerangka: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
2. Setiap kartu harus punya judul, sub, isi, dan foot yang informatif. Tidak boleh ada kartu dengan body kosong atau teks kurang dari 40 karakter.
3. Gunakan data dari `window.DATA`, bukan angka hardcoded baru. Hitungan baris memakai `D.queue.length` dan `countBy(...)`.
4. Label antrean harus "Segmen", bukan "Sumur". Label keyakinan harus "K_tampil", bukan "K_segmen".
5. Jangan tampilkan nama sumur rekaan di antrean. Jika data tidak ada, tulis "belum dihitung" atau "BELUM KUTIP".
6. Semua angka yang tampil harus bisa dilacak ke `data.js` dan sumbernya. Jika ragu, tandai `BELUM KUTIP`.
7. Jangan memakai em dash sebagai penghubung klausa. Gunakan koma, titik dua, atau konjungsi.
8. Isi disusun bertahap: pertama kerangka card per view, lalu isi card satu per satu sampai penuh. Jangan mengisi satu card sampai penuh sementara card lain kosong.
9. Pola "Daftar Kerusakan": judul bagian di luar card, lalu deretan card kerusakan disusun horizontal di dalam `.hscroll`, bisa digeser kiri kanan. Setiap card punya nama, pita, K_tampil, bukti singkat, dan batas.
10. Jika isi satu card panjang, gunakan scroll vertikal di dalam card atau tabel yang bisa digeser. Jangan memotong teks sampai tidak terbaca.
11. Ruang kosong boleh ada asal proporsional. Jangan memaksa card pendek menjadi tinggi hanya untuk menyamakan baris.

## Verifikasi wajib
- `node --check js/views.js`.
- `rg -n '12 baris|K_segmen|"Sumur"|TODO|TBD|FIXME' js/views.js` harus bersih atau setiap sisa dijelaskan.
- Pastikan `window.VIEWS` berisi 10 kunci.
- Tulis `production/audit/W3_VIEWS.md` berisi daftar view, jumlah kartu, dan defect yang diperbaiki.

KERANGKA WAJIB (sama untuk semua kartu):
- Bahasa keluaran: Indonesia, langsung, tanpa basa-basi.
- File md lama di docs/ dan planning/ tetap valid dan otoritatif. Jangan menulis ulang, meregenerasi, atau mengganti 16 file planning. Ambil isi dari sana.
- Referensi visual: `D:\Download\Magang Halliburton\DESIGN.md` untuk header, sidebar, palet, dan tipografi. Tombol serta pola card disesuaikan dengan riset di `planning/DESIGN.md`, bukan copy mentah.
- Satu folder output: `/mnt/d/Capstone 1(v2)/production/`. Tidak boleh membuat website di folder lain.
- Urutan desain: kerangka layout dan susunan card dulu, baru isi tiap card maksimal. Tidak boleh ada card kosong atau ruang kosong yang tidak proporsional.
- Jika satu card tidak muat dalam satu layar, gunakan scroll horizontal atau vertikal di dalam card. Contoh pola: judul di luar card, misalnya "Daftar Kerusakan", lalu deretan card kerusakan disusun horizontal dan digeser ke kiri kanan.
- Baca skill antislop, antislop-ui, antislop-layoutmobile sebelum mengubah tampilan. Patuhi: tanpa gradien neon atau ungu, tanpa bento grid, tanpa glow halaman, tanpa shadow di semua kartu, tanpa pill di semua elemen, tanpa emoji dekoratif, tanpa logo/testimoni/delta palsu, tanpa gauge/donut/radar/dual-Y.
- Setiap angka yang ditulis atau diubah harus punya sumber file:line di docs/ atau planning/ atau scratch JSON. Kalau tidak ada sumber, tulis "BELUM KUTIP" dan jangan tampilkan sebagai fakta.
- Dilarang mengarang output, angka, path, status, atau klaim selesai. Verifikasi dengan tool output nyata.
- Jangan mengubah model atau provider. Jangan menyentuh board lain.
- Jangan memakai em dash sebagai penghubung klausa. Gunakan koma, titik dua, atau konjungsi.
- Sebelum selesai: jalankan `node --check` untuk setiap JS yang diubah, lalu tulis ringkasan bukti.
- Deliverable harus benar-benar ada di disk. Sertakan path absolut, ukuran byte, dan mtime.

