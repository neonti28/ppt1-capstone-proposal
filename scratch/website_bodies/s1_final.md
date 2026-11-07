# S1 · Integrasi dan verdict akhir

Kamu adalah integrator terakhir. Kamu boleh mengedit semua file di `/mnt/d/Capstone 1(v2)/production/`, tetapi hanya untuk menutup defect dari `production/audit/V1_VERDICT.md`.

## Tugas
1. Baca `production/audit/V1_VERDICT.md`, `W1_SHELL.md`, `W2_DATA.md`, `W3_VIEWS.md`, dan `W4_APP.md`.
2. Tutup semua defect P0 dan P1. Untuk P2, perbaiki bila murah; jika tidak, catat alasan.
3. Jangan mengubah `docs/` atau `planning/`.
4. Jalankan verifikasi akhir: `node --check` untuk 3 file JS, buka 10 route, cek 1440px dan 390px, cek kontras, cek antrean 10 baris dan label "Segmen"/"K_tampil".
5. Cek khusus desain: header dan sidebar mengadopsi referensi Halliburton, tombol tidak copy mentah, ada pola card horizontal "Daftar Kerusakan", tidak ada card kosong, dan setiap view disusun layout dulu baru isi.
6. Tulis `production/REVIEW.md` berisi: verdict akhir, defect yang ditutup, bukti perbaikan, sisa masalah, dan daftar yang belum dicek.

## Aturan
- Jangan menutup defect dengan menghapus fitur atau mengosongkan kartu.
- Jangan mengarang hasil browser. Jika browser tidak tersedia, tulis keterbatasan.
- Jangan menyebut "siap produksi" jika masih ada P0/P1 terbuka.

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

