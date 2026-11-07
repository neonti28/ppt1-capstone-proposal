# Capstone 1 — Workspace Halliburton Sperry Drilling

Folder ini adalah pusat kerja proyek capstone.

## Struktur Folder

```
Capstone 1/
├── docs/               # Buku riset & dokumentasi (markdown)
│   ├── BUKU_RISET.md           # Buku utama: tujuan, konsep, segmen, dataset, parameter, hipotesis
│   ├── 02_MAPPING_EVENT_BHA.md # Mapping event → komponen BHA (untuk "apa yang harus diperbaiki")
│   └── 03_SENSOR_PARAMETER.md  # Detail sensor & parameter dataset 3W
├── data/               # Dataset
│   └── 3W/             # (atau 3W-main setelah ekstrak ZIP) — Petrobras 3W dataset
└── code/               # Script Python / notebook
    ├── 01_explore_3w.py
    └── 02_verify_3w.py
```

## Cara pakai

- **Python**: pakai venv yang sudah disiapkan (`/tmp/capstone-venv/.venv`) atau buat venv sendiri:
  ```bash
  python -m venv .venv
  .venv/bin/pip install pandas pyarrow scikit-learn matplotlib
  ```
- **Jalankan eksplorasi**:
  ```bash
  cd code
  .venv/bin/python 01_explore_3w.py
  ```
  (sesuaikan path venv)

## Status dataset

| Dataset | Status | Lokasi |
|---|---|---|
| Petrobras 3W (github.com/petrobras/3W) | ✅ **TERVERIFIKASI** — sparse checkout folder `dataset/0` & `dataset/4` (419 MB) | `data/3W/` |
| USROP / Equinor Volve | Belum diunduh (perlu cek lisensi & akses) | — |

## Catatan penting

- Dataset 3W **bukan** seluruh data — notebook referensi memakai subset: real instance kelas Normal (0) + Flow Instability (4), 5 sumur, max 20 file/sumur/kondisi → 164 file.
- Lihat `docs/BUKU_RISET.md` untuk detail lengkap.