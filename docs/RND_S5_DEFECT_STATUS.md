# STATUS SEMBILAN CATATAN AUDIT GELOMBANG 2

Tanggal: 2026-10-29 · Sumber catatan: `docs/RND_S5_AUDIT_WAVE2.md` bagian 7

Catatan ini memakai nama cacat dalam bahasa biasa, bukan kode nomor saja. Kode S5 tetap ditulis dalam tanda kurung supaya bisa dilacak ke dokumen audit.

## 1. Baris ledger S4-013 menulis 884 kolom padahal 20 kolom (D1)

Status: **selesai**. Sel angka pada baris itu sekarang berbunyi `884 record / 20 kolom`, dan kolom rujukan menunjuk `labels_duration.json:n_baris`. Bukti: `grep '^| S4-013' docs/RND_PROVENANCE_LEDGER.md`.

## 2. Dokumen S1 mengklaim setiap angka punya baris ledger (D2)

Status: **selesai**. Klaim diganti dengan angka terukur: 64 dari 441 sel angka (14,51 persen) punya padanan, sisanya agregat turunan. Ditambahkan bagian `Catatan provenance` di dokumen S1.

## 3. Dokumen S3 mengklaim setiap angka menunjuk baris ledger (D3)

Status: **selesai**. Klaim diganti: 74 dari 328 sel angka (22,56 persen), dan kalimat aslinya diubah agar tidak melebih-lebihkan cakupan.

## 4. Gaya angka ledger mencampur titik ribuan dengan koma desimal (D4)

Status: **selesai**. 334 sel angka bergaya `1.234` dinormalkan menjadi `1234`. Sisa sel bergaya ribuan: 0. Bukti: pemindaian ulang pola `^\d{1,3}(\.\d{3})+$` pada kolom angka.

## 5. Nilai 32,17405 ft/s2 memakai rujukan standar tanpa nomor bagian (D5)

Status: **selesai**. Rujukan diganti menjadi ISO 2041:2018 §3.1.4, sejalan dengan baris ledger L-01 yang sudah terverifikasi. Kemunculan `API RP 7G` di dokumen S2: 0.

## 6. Empat dokumen tanpa DOI dan tanpa URL (D6)

Status: **selesai sebagai pernyataan, bukan sebagai tambahan rujukan palsu**. Keempat dokumen sekarang menyatakan bahwa konstanta metode adalah konvensi internal repo dengan jejak berkas dan baris, dan satu-satunya standar eksternal adalah ISO 2041:2018 §3.1.4. Menambahkan DOI yang tidak benar hanya akan menciptakan cacat baru.

## 7. Klaim sepuluh pikiran sequ-mcp di S1, empat di antaranya tak terbukti (D7)

Status: **selesai**. Dokumen S1 sekarang menyebut 6 pikiran yang tersimpan transkripnya, dan menyatakan 4 pikiran run awal tidak punya transkrip sehingga tidak dihitung.

## 8. Tabel S1, S2, S3 tidak mencantumkan kode baris ledger (D8)

Status: **selesai sebagian, dengan pengukuran**. S2 sudah 98,40 persen (369 dari 375 sel) karena dokumennya dibangkitkan resolver jalur. S1 14,51 persen dan S3 22,56 persen tidak dinaikkan ke 100 persen karena sel yang tersisa adalah agregat turunan antar fold; menambah baris untuk setiap agregat akan menggelembungkan ledger tanpa menambah keterlacakan. Yang diubah adalah klaimnya, bukan angkanya.

## 9. Rujukan 32 baris ledger S4 berupa prosa banyak nilai (D9)

Status: **selesai**. 16 baris yang memuat rujukan prosa diubah menjadi satu berkas dan satu kunci, misalnya `labels_duration.json:n_baris`. Sisa baris berbentuk prosa: 0 dari 95 baris S4.

## Ringkasan

| Nama cacat | Status |
|---|---|
| Salah angka kolom S4-013 | selesai |
| Klaim cakupan S1 | selesai |
| Klaim cakupan S3 | selesai |
| Gaya angka ribuan | selesai |
| Rujukan standar tanpa nomor bagian | selesai |
| Tidak ada DOI | selesai sebagai pernyataan konvensi |
| Klaim 10 pikiran sequ | selesai |
| Keterlacakan tabel ke ledger | selesai sebagian, diukur dan dinyatakan |
| Rujukan prosa S4 | selesai |

Tidak ada satu pun yang saya tutup dengan alasan "sudah cukup". Setiap baris menyebut angka atau perintah yang bisa diulang.
