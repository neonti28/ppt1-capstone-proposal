# W4 · Interaksi, router, aksesibilitas

## Ringkasan
`js/app.js` diaudit. Router hash menangani 10 route: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu. Navigasi aktif tersinkron dengan hash dan judul topbar berubah.

## Defect yang diperbaiki
1. Label `K_segmen` pada modal detail klaim diubah menjadi `K_tampil`.
2. Modal memiliki Escape, focus trap Tab, dan tombol tutup.
3. Pencarian global memakai alias: hyd, vib, shk, ssi, stuck, bit_wear, tool_wear, tk.
4. Tombol "/" memusatkan fokus ke `#global-search`.

## Verifikasi
- `node --check js/app.js`: OK.
- 10 route terdaftar di `TITLES` dan `window.VIEWS`.
- Tidak ada dependensi eksternal baru.

## Sisa masalah
- Verifikasi browser penuh untuk modal dan pencarian belum diulang setelah perubahan terakhir; audit statis menunjukkan struktur benar.
- Focus trap dan kembalikan fokus ke pemicu perlu uji browser.

## Status
LULUS BERSYARAT. Deliverable: `production/js/app.js` (24.492 byte pada 2026-11-01).