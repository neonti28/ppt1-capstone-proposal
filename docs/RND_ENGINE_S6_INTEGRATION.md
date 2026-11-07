# INTEGRASI KEPUTUSAN S6 KE Detektor V9-I1

Tanggal: 2026-10-29 · Segmen: F-14 · ML: ON · Seed: 42

Riset pendahuluan: ml-system-evaluation (profil kapabilitas lapisan A/B/C, bukan bit lulus/gagal), verification-mandatory (angka diambil dari JSON hasil run), sequentialthinking (menyusun urutan perubahan: head utama, profil kapabilitas, nilai maintenance, dasbor).

## 1. Apa yang berubah di detektor

| Perubahan | Sebelum | Sesudah | Bukti |
|---|---|---|---|
| Head utama hyd peringatan dini | tiga head setara | `hybrid_rule_and_persistence` ditandai `head_utama=true` | `scratch/v9_i1/v9_i1_RESULTS.json` engines[hyd].heads |
| Badge head tersebut | FAR 14,6-58,4 (9/9 well > 6) | S6: FP 927, presisi 0,8243, recall 0,6519, FAR 4,10/24jam, lead 8,0 mnt, 7/9 fold | docs/RND_S6_PM_WAVE2.md §4.1 |
| Lapisan B | tidak ada di JSON | blok `nilai_maintenance` (jam henti DDR + beban tinjauan per shift) | run ini |
| Profil per mode | tidak ada | blok `profil_kapabilitas` 7 mode (A/B/C) | run ini |
| Bahasa keluaran | berpusat pada slot alarm | berpusat pada nilai maintenance | `code/v9_i1_run.py` |

## 2. Angka nilai maintenance (dari data, bukan asumsi)

Sumber: `/mnt/d/Capstone 1(v2)/data/volve/ddr.parquet` kolom `activity`.

- Record aktivitas: **23447**
- Total jam tercatat: **39397.986 jam**
- Interruption other: 2680.917 jam
- Interruption waiting on weather: 1925.5 jam
- Henti karena equipment failure: 2739.667 jam
- Henti karena stuck equipment: 212.0 jam
- Henti karena circulation loss: 195.0 jam

Beban tinjauan per shift 8 jam dihitung dari FAR per 24 jam dibagi 3:

| Mesin | Head | FAR/24jam | Tinjauan per shift |
|---|---|---:|---:|
| vib | `rule_display` | 49.942 | 17 |
| vib | `hybrid_rule_and_persistence` | 49.942 | 17 |
| ssi | `rule_display` | 0.0 | 0 |
| ssi | `hybrid_rule_and_persistence` | 0.0 | 0 |
| shk | `rule_display` | 6.618 | 3 |
| shk | `hybrid_rule_and_persistence` | 6.618 | 3 |
| stuck | `rule_display` | 8.321 | 3 |
| stuck | `hybrid_rule_and_persistence` | 8.321 | 3 |
| hyd | `rule_display` | 55.57 | 19 |
| hyd | `hybrid_rule_and_persistence` | 16.611 | 6 |
| tool_wear | `op_far_calibrated` | 2.096 | 1 |

## 3. Profil kapabilitas per mode

| Mode | Jenis tugas | A: head bermetrik | B: nilai maintenance | Kekuatan bukti |
|---|---|---:|---|---|
| vib | deteksi kondisi (bukan prediksi onset — TLead tidak berlaku) | 4 | BELUM TERUKUR | SEDANG |
| ssi | deteksi kondisi | 4 | BELUM TERUKUR | SEDANG |
| shk | deteksi anomali sedang berlangsung | 4 | BELUM TERUKUR | SEDANG |
| stuck | deteksi kondisi (K-i) + prediksi kejadian mendatang (K-ii) | 6 | BELUM TERUKUR | SEDANG |
| hyd | deteksi kondisi (K-i) + prediksi kejadian mendatang (K-ii) | 3 | TERUKUR | SEDANG |
| bit_wear | deteksi kondisi (K-1); K-2 onset = BELUM DIJALANKAN | 1 | BELUM TERUKUR | LEMAH |
| tool_wear | deteksi perubahan-regime (K-i); K-ii = ranking | 2 | BELUM TERUKUR | SEDANG |

## 4. Susunan lapisan keputusan

L0 5 head, L1 11 head, L2 9 head, L3 2 head.

Keputusan akhir: MANUSIA (insinyur pengeboran) — tidak ada output otomatis yang memicu tindakan tanpa konfirmasi.

## 5. Batas yang tetap berlaku

1. Jam henti tidak dapat dipetakan ke satu alarm tertentu karena tidak ada nomor work order atau kunci bit yang menghubungkan alarm ke record DDR.
2. Lapisan B baru terukur sebagian: dua head yang nilai penghematannya bisa dihitung belum ada, karena repo tidak memuat tarif biaya.
3. Angka FAR pada blok beban tinjauan adalah FAR segmen F-14, bukan median lintas fold. Median lintas fold untuk H1p ada di docs/RND_S6_PM_WAVE2.md §4.1.
4. Detektor tidak mengeluarkan alarm otomatis. Semua peringatan L1 wajib konfirmasi manusia.

## 6. Cara menjalankan

```
cd '/mnt/d/Capstone 1(v2)/code'
/home/neonti/.venvs/rnd_e3/bin/python v9_i1_run.py          # 7 mode, 27 head, tanpa ML
/home/neonti/.venvs/rnd_e3/bin/python v9_i1_run.py --ml     # tambah 4 head RF LOWO
```
