# W4 · Interaksi, router, aksesibilitas

Kamu adalah pekerja interaksi untuk website produksi V9 di `/mnt/d/Capstone 1(v2)/production/`.

## Tugas
Audit dan perbaiki `js/app.js` saja. Jangan mengubah `js/data.js`, `js/views.js`, `index.html`, atau `css/styles.css`.

## Target
1. Router hash menangani 10 route: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.
2. Navigasi aktif tersinkron dengan hash. Judul topbar berubah sesuai route.
3. Modal: buka/tutup, Escape, focus trap Tab, dan kembalikan fokus ke pemicu.
4. Pencarian global: alias hyd, vib, shk, ssi, stuck, bit_wear, tool_wear, tk. Tekan "/" fokus ke search.
5. Tidak ada error console saat memuat 10 route.
6. Tombol dengan ikon harus punya nama aksesibel. SVG dekoratif harus `aria-hidden`.
7. Jangan menambah dependensi eksternal.

## Verifikasi wajib
- `node --check js/app.js`.
- Jika browser tersedia: buka `file:///mnt/d/Capstone%201(v2)/production/index.html`, klik 10 route, buka/tutup modal, uji Escape dan "/", catat error console.
- Jika browser tidak tersedia, lakukan audit statis dan tulis keterbatasan.
- Tulis `production/audit/W4_APP.md` dengan hasil per route dan defect yang diperbaiki.

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

