# R2 · Audit sci dan provenance

## Ringkasan
Audit ilmiah pada klaim dan angka website. Semua angka kunci di antrean memakai sumber `04` bagian 6.2. Angka rekaan (0,58, 0,47, 0,51, 0,35) dan nama sumur rekaan sudah dibuang dari `data.js`.

## Temuan
1. `focus` 3 kartu: hyd K-i 0,6100 P4, vib 0,4950 P3, shk 0,5188 P3.
2. `queue` 10 baris: semua segmen F-14, age "—", menit 6,4,4,4,4,2,2,2,2,0, total 30.
3. `damages` 11 kelas: `k` dan `pita` dari `04`; `vote` dan `weight` dari `06`.
4. Label TERUKUR/TURUNAN/BELUM KUTIP dipakai di halaman bukti.
5. Metrik dibaca sesuai artinya: recall 0,6519 bukan "sumur aman"; FAR per menit tidak disamakan dengan per 24 jam.
6. Abstain AB-1 sampai AB-5 dijelaskan dengan alasan yang bisa diaudit.
7. Tidak ada klaim "siap produksi".

## Sisa ketidakpastian
- Layer B masih memakai 6 sumur contoh dan 6 kanal; ditandai contoh, bukan seluruh lapangan.
- Umur per baris belum tersedia; ditampilkan "—".
- Beberapa metrik S2/S3 memakai potongan data; sumber dicatat di ledger.

## Verdict
LULUS BERSYARAT. Deliverable: `production/audit/R2_SCI.md`.