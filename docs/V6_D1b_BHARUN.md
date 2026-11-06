# V6-D1b — Ekstraksi Penuh WITSML bhaRun (161 XML)

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan glob (berbeda dari parser penulis): file bhaRun XML = 161, cocok dengan klaim ringkasan angka di bawah.**

Tanggal: 2026-10-10
Task: t_07d76f62 (board capstone-v6-solve)
CSV: `/mnt/d/Capstone 1/scratch/v6_d1b_bharun.csv`

## Ringkasan angka (SEMUA dihitung dari file asli, bukan klaim)

| Metrik | Nilai |
|---|---|
| Total file XML bhaRun | 161 |
| Berhasil di-parse (XML valid, elemen `bhaRun` ada) | 161 (0 error) |
| Punya `dTimStart` | 161 (100%) |
| Punya `dTimStop` | 114 (70.8%) |
| Punya `numBitRun` | **11** (6.8%) |
| Punya `dTimStartDrilling` | **15** (9.3%) |
| Punya `dTimStopDrilling` | **10** (6.2%) |
| Drilling window lengkap (start+stop drilling) | **9** (5.6%) |
| Tag `dullingInfo` di semua 161 file | **0 — V4 §1.6 KONFIRMASI benar** |
| Tag `dullGrade` | **0 — konfirmasi** |
| Tag `bitName` | **0 — konfirmasi** |
| Jumlah wellbore berbeda | 14 |
| Source: INTEQ | 105 |
| Source: Baker Hughes | 56 |
| Run dengan durasi negatif (stop < start) | **6 — cacat data** |

Lokasi direktori: `witsml_raw/<well-dir>/<N>/bhaRun/*.xml` — ada level numerik tambahan
di antara well dir dan bhaRun (glob `*/bhaRun/*.xml` TIDAK work; pakai `*/*/bhaRun/*.xml`).

## Konten file (raw, 3 contoh dicetak langsung)

Ketiga file dibuka dengan `cat` sebelum parse. Struktur identik:

```xml
<bhaRuns xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1">
  <bhaRun uidWell="..." uidWellbore="..." uid="23RGUI47">
    <nameWell>NO 15/9-F-1 C</nameWell>
    <nameWellbore>NO 15/9-F-1 B</nameWellbore>
    <name>15/9-F-1 B-22</name>
    <tubular uidRef="23RGUI47">15/9-F-1 B_23RGUI47</tubular>
    <dTimStart>2013-09-23T07:59:00.000Z</dTimStart>
    <dTimStop>2013-09-23T09:10:00.000Z</dTimStop>
    <numStringRun>22</numStringRun>
    <commonData><sourceName>INTEQ</sourceName>...</commonData>
  </bhaRun>
</bhaRuns>
```

Catatan penting dari file F-14 (`.../9-F-14/1/bhaRun/1.xml`): `sourceName=Baker Hughes`,
`dTimStart=2016-08-12T04:40Z`, `numStringRun=7`, TIDAK ada `dTimStop`.
File F-15 C (`.../9-F-15/1/bhaRun/1.xml`): `dTimStop` (2013-11-07) MENDAHULUI
`dTimStart` (2013-11-08) — cacat data (lihat §Cacat data).

## numBitRun — 11 file, tersebar di 5 wellbore

| Wellbore | Run | numBitRun | StartDrilling | StopDrilling |
|---|---|---|---|---|
| F-1 C | 15/9-F-1 C - 3 | 3 | 2014-03-10T21:50Z | 2014-03-10T22:00Z |
| F-1 C | 15/9-F-1 C - 3 RR 1 | "3 RR 1" | 2014-03-12T04:20Z | 2014-03-14T13:50Z |
| F-1 C | 15/9-F-1 C - 1 | 1 | 2014-02-21T00:50Z | 2014-02-26T21:30Z |
| F-1 C | 15/9-F-1 C - 2 | 2 | 2014-03-03T06:20Z | 2014-03-04T20:00Z |
| F-1 | 15/9-F-1 - 2 | 2 | 2013-08-04T08:15Z | 2013-08-26T15:45Z |
| F-1 | 15/9-F-1 - 1 | 1 | 2013-07-22T22:00Z | 2013-07-26T18:20Z |
| F-1 | 15/9-F-1 - 3 | 3 | — | — |
| F-1 | 15/9-F-1 - 1 | 1 | — | — |
| F-11 T2 | 15/9-F-11 - 4 | 4 | — | — |
| F-11 T2 | 15/9-F-11 - 4RR1 | "4RR1" | — | — |
| F-15 D | 15/9-F-15 - 1 | 1 | — | — |

PERINGATAN downstream: 2 dari 11 nilai `numBitRun` BUKAN integer murni
("3 RR 1", "4RR1" = re-entry). Parse sebagai string, jangan `int()` langsung.

## Drilling window (dTimStartDrilling → dTimStopDrilling) — 9 lengkap + 5 tanpa stop

9 run dengan window lengkap (kandidat index waktu untuk label):

1. F-1 C run-1: 2014-02-21T00:50Z → 2014-02-26T21:30Z (5.9 hari)
2. F-1 run-2: 2013-08-04T08:15Z → 2013-08-26T15:45Z (22.3 hari)
3. F-11 T2-10: 2013-04-12T23:25Z → 2013-04-21T04:47Z (8.2 hari)

Plus: F-1 C-3 (10 menit), F-1 C-3 RR 1 (2.4 hari), F-1 C-2 (1.6 hari),
F-11 T2-13 (8 menit), F-11 B-21 (4.3 hari).

6 run punya `dTimStartDrilling` TANPA `dTimStopDrilling` (15 start − 9 window
lengkap): F-1-9, F-1-1, F-1-4, F-11 T2-14, F-15 D-6, F-5-3.

## Cacat data (ditemukan, bukan diasumsikan)

1. **6 run durasi negatif** (dTimStop < dTimStart) — contoh ekstrem: F-15 C-15
   start 2013-11-08T23:15Z, stop 2013-11-07T13:01Z (delta -2.6 hari). Jangan pakai
   selisih mentah tanpa filter durasi negatif.
2. **Nama direktori well ≠ nameWellbore di isi file**: folder `9-F-1 C` berisi file
   dengan `nameWellbore=NO 15/9-F-1 B`. Join downstream harus pakai field XML,
   bukan path.
3. `dTimStart` selalu ada (161/161) tapi `dTimStop` hanya 114 — run berjalan/tanpa
   tutup.

## Per-wellbore coverage (14 wellbore)

F-1 C 26, F-11 B 26, F-15 D 16, F-1 B 17, F-15 C 14, F-11 T2 12, F-1 11, F-5 11,
F-12 10, F-14 7, F-4 4, F-1 A 3, F-11 A 2, F-9 A 2.

## Kesimpulan vs klaim V4 §1.6

- "numBitRun + dTimStartDrilling/dTimStopDrilling ada di SEBAGIAN file" → **BENAR**:
  11/161 dan 15/161 file — minoritas kecil, hanya 5 wellbore (numBitRun) /
  5 wellbore (drilling window).
- "Tag dullingInfo/dullGrade/bitName TIDAK ada" → **KONFIRMASI**: grep regex
  `<tag[ >]` di isi semua 161 file = 0 hit untuk ketiga tag. Tidak ada label dull
  grade di bhaRun Volve.
- Interval drilling time tersedia tapi SANGAT sedikit (9 window lengkap) —
  berguna sebagai anchor waktu untuk well F-1 C, F-1, F-11 T2/B saja, bukan seluruh
  dataset.
