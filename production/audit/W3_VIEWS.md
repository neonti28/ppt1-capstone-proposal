# W3 · Isi sepuluh tampilan

## Ringkasan
`js/views.js` diaudit dan diperbaiki tanpa mengubah `data.js`. Semua 10 view terdaftar di `window.VIEWS`: beranda, kepercayaan, perencanaan, data, mesin, linimasa, bukti, batas, kamus, alat-bantu.

## Defect yang diperbaiki
1. Label antrean "Sumur" diubah menjadi "Segmen".
2. Label keyakinan "K_segmen" diubah menjadi "K_tampil" pada kartu, tabel, dan modal.
3. Sisa label "K_segmen" di header "Papan vonis" dan tabel "Peta suara dewan" diubah menjadi "K_tampil".
4. Hitungan baris memakai `D.queue.length` dan `countBy(...)`, bukan angka 12 tetap.
5. Kartu "Umur antrean" yang memakai umur rekaan diganti dengan "Beban per baris" yang memakai menit nyata dari `04`.
6. Pola "Daftar Kerusakan" sudah ada: judul di luar card, deretan card horizontal di `.hscroll wide`.

## Verifikasi
- `node --check js/views.js`: OK.
- `grep -n 'TODO\|TBD\|FIXME\|lorem' js/views.js`: tidak ada.
- `grep -n 'K_segmen' js/views.js`: tidak ada (kecuali data.js yang mendefinisikan istilah).
- `window.VIEWS` berisi 10 kunci.

## Sisa masalah
- Beberapa angka layer B masih memakai data contoh 6 sumur dan 6 kanal; ini sudah diberi catatan "contoh, bukan seluruh lapangan".
- Umur per baris belum tersedia; ditampilkan sebagai "—" dan dicatat di card.

## Status
LULUS BERSYARAT. Deliverable: `production/js/views.js` (82.582 byte pada 2026-11-01).