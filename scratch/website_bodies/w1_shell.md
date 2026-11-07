# W1 · Shell, header, sidebar, layout

Kamu adalah pekerja visual untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki shell website: `index.html` dan `css/styles.css` saja.
Jangan mengubah `js/data.js`, `js/views.js`, atau `js/app.js`.

## Target
1. Header dan sidebar mengikuti referensi `D:\Download\Magang Halliburton\DESIGN.md` yang sudah diadopsi: topbar 64px, sidebar 212px, palet gelap Halliburton, Barlow Condensed untuk judul, Inter untuk body, JetBrains Mono untuk angka.
2. Tombol dan pola card tidak boleh copy mentah dari Halliburton. Sesuaikan dengan riset di `planning/DESIGN.md`: radius 4/6/8/10 sesuai peran, tinggi tombol konsisten, tidak semua elemen jadi pill.
3. Semua 10 tautan navigasi ada dan mengarah ke route yang benar: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
4. Tidak ada overflow horizontal pada body di 1440px dan 390px. Tabel dan `.hscroll` boleh scroll sendiri, bukan body.
5. Tidak ada kartu kosong atau ruang kosong tidak proporsional. Jika satu kartu butuh tinggi, biarkan tumbuh; jangan memaksa semua kartu sama tinggi sampai isi terpotong.
6. Layout disusun bertahap: shell, grid, lalu card. Setiap card harus punya ruang untuk judul, isi, dan foot. Jangan menaruh card tanpa isi.
7. Jika satu card tidak muat satu layar, sediakan scroll di dalam card atau `.hscroll`, bukan memaksa mengecilkan teks.
8. Skip link, focus ring, dan urutan tab tetap benar.
9. Jangan menambah dekorasi yang tidak membawa informasi.

## Cara verifikasi
- Baca `index.html` dan `css/styles.css` penuh sebelum mengubah.
- Cek 10 href di sidebar dan `id` view yang dirujuk.
- Jika browser tool tersedia: buka `file:///mnt/d/Capstone%201(v2)/production/index.html`, ukur 1440x1000 dan 390x844, cari `document.body.scrollWidth > innerWidth + 2`, dan ambil screenshot.
- Jika browser tidak tersedia, lakukan pemeriksaan statis dan tulis keterbatasan itu di laporan.

## Deliverable
Tulis `production/audit/W1_SHELL.md` berisi: defect ditemukan, perubahan per file:line, ukuran sebelum/sesudah, hasil verifikasi, dan sisa masalah.
Jangan klaim "selesai" tanpa output verifikasi.

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

