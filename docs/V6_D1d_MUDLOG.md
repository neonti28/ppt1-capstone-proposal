# V6-D1d — WITSML MUDLOG: Buka & Ekstrak (lithology, chromatograph C1–C5, mud gas)

**Riset pendahuluan: `verification-mandatory` — verifikasi ulang 2026-10-11 dengan find: file mudLog XML = 8 dengan pola `*/*/mudLog/*.xml` (pola dangkal `*/mudLog/*.xml` = 0 — ada level numerik di antara well dir dan mudLog), cocok dengan klaim.**

Status: **SELESAI — semua 8 file XML dibuka & diekstrak penuh. Isi TIDAK kosong, malah kaya.**

## Target

`/mnt/d/Capstone 1/data/volve/witsml_raw/*/mudLog/*.xml` — ditemukan persis 8 file (1.4.1.1):

| # | File (relatif ke witsml_raw) | Size | Well | Wellbore | MD (m) | geologyInterval |
|---|---|---|---|---|---|---|
| 1 | `Norway-Statoil-NO 15_$47$_9-F-1 C/1/mudLog/1.xml` | 120 KB | NO 15/9-F-1 C | NO 15/9-F-1 B | 2602–3465 | 88 |
| 2 | `…/9-F-1 C/2/mudLog/1.xml` | 162 KB | NO 15/9-F-1 C | NO 15/9-F-1 C | 3056–4094 | 144 |
| 3 | `…/9-F-1 C/3/mudLog/1.xml` | 408 KB | NO 15/9-F-1 C | NO 15/9-F-1 A | 2602–3682 | 343 |
| 4 | `…/9-F-1 C/4/mudLog/1.xml` | 448 KB | NO 15/9-F-1 C | NO 15/9-F-1 | 2750–3632 | 317 |
| 5 | `…/9-F-11/1/mudLog/1.xml` | 1.10 MB | NO 15/9-F-11 | NO 15/9-F-11 T2 | 1365–4562 | 901 |
| 6 | `…/9-F-11/2/mudLog/1.xml` | 566 KB | NO 15/9-F-11 | NO 15/9-F-11 B | 2580–4771 | 431 |
| 7 | `…/9-F-11/4/mudLog/1.xml` | 441 KB | NO 15/9-F-11 | NO 15/9-F-11 A | 2590–3762 | 357 |
| 8 | `…/9-F-15/2/mudLog/1.xml` | 367 KB | NO 15/9-F-15 | NO 15/9-F-15 D | 1380–4685 | 301 |

Catatan penamaan: file di folder `9-F-1 C` berisi wellbore lintas-sumber — F-1 A, F-1 B, F-1 C, F-1 (folder ≠ wellbore). ID wellbore resmi = `nameWellbore` di dalam XML, bukan nama folder.

## 1. Struktur tag

mudLog TIDAK punya `LogCurveInfo`/`mnemonic` (bukan format curve-based). Strukturnya **interval-based**:

```
mudLogs > mudLog (uidWell, uidWellbore, uid, nameWell, nameWellbore, dTim,
                  mudLogCompany, startMd, endMd, relatedLog)
  └ geologyInterval (uid, typeLithology[interpreted|cuttings], mdTop, mdBottom, dTim)
      ├ ropAv / ropMn / ropMx      uom m/s
      ├ wobAv                      uom N
      ├ tqAv                       uom N.m
      ├ rpmAv                      uom c/s
      ├ wtMudAv / ecdTdAv          uom kg/m3
      ├ dxcAv                      (dimensionless, mechanical specific energy proxy)
      ├ lithology (n×)  → type, codeLith, lithPc (%)
      ├ qualifier (n×)  → type, abundance (%)   [mineral/texture modifier]
      ├ chromatograph  → meth/eth/prop/ibut/nbut/ipent × Av/Mn/Mx, semua uom ppm  (C1..C5)
      └ mudGas         → gasAv / gasPeak / gasBackgnd, uom ppm
```

Jumlah tag per file konsisten dengan jumlah geologyInterval (tidak ada struktur asing). Tag `priv` (4–5/file) = private extension, berisi parameter tambahan BHI; tidak diparse di ekstraksi ini.

## 2. Ekstraksi

CSV: **`/mnt/d/Capstone 1/scratch/v6_d1d_mudlog.csv`** — 2.882 baris (1 geologyInterval = 1 baris), 44 kolom, 1.0 MB.
Parser: workspace task ini (`v6_d1d_parse.py`), ElementTree murni, namespace-stripped.

Kolom: file, well_dir, run, nameWell, nameWellbore, mudLog_uid, gi_uid, typeLithology, mdTop_m, mdBottom_m, ropAv_mps, ropMn_mps, ropMx_mps, wobAv_N, tqAv_Nm, rpmAv_cs, wtMudAv_kgm3, ecdTdAv_kgm3, dxcAv, lithology_n, lithology, qualifier_n, qualifier, {meth,eth,prop,ibut,nbut,ipent}{Av,Mn,Mx}_ppm, gas{Av,Peak,Backgnd}_ppm

## 3. Populasi

- **2.882 baris** geologyInterval, **8 wellbore** (3 well: F-1 C, F-11, F-15).
- BUKAN kosong. Tidak ada klaim kosong yang perlu dibuktikan.

Non-null per kurva:

| Kurva | Unit | Non-null | % |
|---|---|---|---|
| mdTop_m / mdBottom_m / typeLithology | m / – | 2882 | 100% |
| ropAv, ropMx, tqAv, rpmAv | m/s, N.m, c/s | 2878 | 99.9% |
| ropMn | m/s | 2876 | 99.8% |
| wobAv | N | 2867 | 99.5% |
| wtMudAv | kg/m3 | 2849 | 98.9% |
| ecdTdAv | kg/m3 | 2848 | 98.8% |
| dxcAv | – | 1581 | 54.9% |
| lithology (type+codeLith+lithPc) | – / code / % | 2882 (100% punya ≥1 lithology) | 100% |
| qualifier (type+abundance) | % | 1532 | 53.2% |
| chromatograph C1–C5 (meth/eth/prop/ibut/nbut/ipent, Av/Mn/Mx) | ppm | 1316 | 45.7% |
| mudGas (gasAv/gasPeak/gasBackgnd) | ppm | 576 | 20.0% |

## 4. Kunci: kandidat LABEL geologi

**YA — ada label geologi gratis, dan ini label langsung (bukan fitur yang harus disimpulkan):**

### a) Litologi — LABEL LANGSUNG, 100% interval
Distribusi lithology type (dari `<lithology><type>`, per kemunculan; tiap interval bisa multi-litologi):

| lithology | kemunculan |
|---|---|
| claystone | 1194 |
| sandstone | 1156 |
| limestone | 780 |
| marl | 227 |
| siltstone | 216 |
| dolomite | 20 |
| no sample | 15 |
| coal | 5 |
| tuff | 4 |

Sebagai label per-interval (litologi primer): claystone 957, sandstone 884, limestone 678, marl 178, siltstone 151, dolomite 17, no sample 10, coal 5, tuff 2. Setiap litologi juga punya `codeLith` (kode numerik WITSML) dan `lithPc` (%) → bisa jadi label **multi-label/proporsi** bukan cuma kelas tunggal.

### b) Qualifier mineral/ tekstur — 53% interval, abundance %
pyrite (hingga 12%), glauconite, argillaceous, kaolinite, calcareous, mica, carbonaceous, silty, sandy. Ini memperkaya deskriptor litologi (mis. "sandstone + carbonaceous" vs "clean sandstone").

### c) Gas show — ADA, tapi coverage terbatas
- mudGas: 576 interval (20%), max gasAv = 46.145 ppm.
- Kriteria show `gasAv > 1.5 × gasBackgnd`: **17 dari 576** interval lolos → label "gas show" valid secara numerik tapi kelasnya sangat jarang (17 sampel) — terlalu kecil untuk jadi target klasifikasi mandiri.
- Chromatograph C1–C5: 1316 interval (45,7%), max methAv 35.013 ppm → cukup untuk fitur wetness ratio (C2+/C1) & ratio hidrokarbon, tapi ratio bukan label baku.

### d) Bukan label kegagalan
TIDAK ada kurva "stuck pipe", "losses", "kick", "wellbore instability" langsung di mudLog. Yang ada adalah proxy drilling parameter (rop/wob/tq/rpm/dxc/mud weight) — itu FITUR, sesuai hipotesis D1 bahwa kegagalan diprediksi dari parameter drilling. Lithology+gas di sini berperan sebagai **konteks geologi / label litologi tambahan**, bukan label kegagalan.

## 5. Relevansi dengan capstone (laporan jujur)

- **Label litologi GRATIS untuk 8 wellbore, 2.882 interval, MD 1365–4771 m** — bisa menambah target multi-task (litologi sebagai auxiliary label) atau fitur one-hot geologi.
- Cakupan litologi menutupi wellbore yang sama dengan lintasan USROP (F-1, F-11, F-15) → potensi join by (wellbore, MD).
- **Belum diverifikasi**: overlap depth-by-depth dengan USROP_labeled.csv (file tidak ditemukan di path tebakan saat analisis). Join perlu MD-interval match, karena mudLog berbasis interval (mdTop–mdBottom), bukan per-sampling.
- Gas show label terlalu jarang (17 kasus) untuk dipakai sebagai target; chromatograph lebih berguna sebagai fitur.

## 6. Artefak

- CSV: `/mnt/d/Capstone 1/scratch/v6_d1d_mudlog.csv` (2882 × 44)
- Parser: `v6_d1d_parse.py` & analisis label `v6_d1d_labels.py` (workspace task t_880f6e22)
- Dokumen: `/mnt/d/Capstone 1/docs/V6_D1d_MUDLOG.md`
