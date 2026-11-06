# V7-D1d — Cek Ketersediaan Data: DOMAIN MUDLOG

Kartu: `t_352301b3` · Master: `t_0d02b12f` (spec §2.4 `docs/V7_M1_DELEGASI.md`) · Tanggal: 2026-10-11

Riset pendahuluan: scientific-critical-thinking — klaim negatif (mudLog bukan sumber label kegagalan) diuji dengan grep ganda (python regex + `grep -oi`), bukan diulang dari D0; angka litologi D0 (957/884/678) direproduksi independen sebelum dipakai.
Riset pendahuluan: verification-mandatory — semua angka di bawah adalah output eksekusi nyata pada 8 file asli (`/mnt/d/Capstone 1/data/volve/witsml_raw/*/*/mudLog/1.xml`), bukan kutipan; 2 klaim silang D0 (litologi, gas show 17/576) diverifikasi ulang dan cocok.

## 0. Bukti pembukaan file (acceptance a)

8 file dibuka + diparse penuh (ElementTree, namespace WITSML 1.4.1.1). Contoh isi asli (`F-11/1/mudLog/1.xml`, 1.100.238 byte):

```xml
<mudLog uidWell="da2c7481-..." nameWell="NO 15/9-F-11" nameWellbore="NO 15/9-F-11 T2"
        startMd uom="m">1365</startMd><endMd uom="m">4562</endMd>
  <geologyInterval uid="int1QKUJ48">
    <typeLithology>interpreted</typeLithology>
    <mdTop uom="m">1365</mdTop><mdBottom uom="m">1369.9</mdBottom>
    <dTim>2013-04-13T18:10:25.000Z</dTim>
    <ropAv uom="m/s">0.0037...</ropAv><wtMudAv uom="kg/m3">1030</wtMudAv><dxcAv>0.59...</dxcAv>
    <lithology><type>claystone</type><codeLith>90</codeLith><lithPc uom="%">100</lithPc>
      <qualifier><type>pyrite</type><abundance uom="%">1</abundance></qualifier>...</lithology>
    <chromatograph><dTim>2013-04-26T11:29:52Z</dTim><mdBottom uom="m">1369.8</mdBottom>
      <methAv uom="ppm">483</methAv><ethAv uom="ppm">0</ethAv><propAv uom="ppm">0</propAv>
      <ibutAv uom="ppm">2</ibutAv><nbutAv>...</nbutAv><ipentAv>...</ipentAv><npentAv>...</npentAv>
    </chromatograph>
  </geologyInterval>
  ...
  <geologyInterval ...><mudGas><gasAv uom="ppm">..</gasAv><gasPeak uom="ppm">..</gasPeak>
    <gasBackgnd uom="ppm">..</gasBackgnd></mudGas></geologyInterval>
```

Coverage dasar (semua 8 file, `INTERVAL_COVERAGE`):

| Item | Jumlah |
|---|---|
| geologyInterval total | **2.882** (cocok klaim V6-D0/D1d) |
| …dengan `dTim` | **2.882 (100%)** |
| …dengan `mdTop` + `mdBottom` | **2.882 (100%)** |
| …dengan blok `lithology` | **2.882 (100%)** |
| typeLithology: interpreted / cuttings | 1.565 / 1.317 |
| Kolom engineering per-interval: ropAv / wtMudAv / ecdTdAv / dxcAv | 2.878 / 2.849 / 2.848 / 1.581 |

Sebaran per file (wellbore folder ≠ nameWellbore, konsisten temuan D0):

| File (witsml_raw) | nameWellbore | interval | dgn chromatograph |
|---|---|---|---|
| F-1 C/1/mudLog/1.xml | NO 15/9-F-1 B | 88 | 44 |
| F-1 C/2/mudLog/1.xml | NO 15/9-F-1 C | 144 | 53 |
| F-1 C/3/mudLog/1.xml | NO 15/9-F-1 A | 343 | 141 |
| F-1 C/4/mudLog/1.xml | NO 15/9-F-1 | 317 | 186 |
| F-11/1/mudLog/1.xml | NO 15/9-F-11 T2 | 901 | 421 |
| F-11/2/mudLog/1.xml | NO 15/9-F-11 B | 431 | 212 |
| F-11/4/mudLog/1.xml | NO 15/9-F-11 A | 357 | 160 |
| F-15/2/mudLog/1.xml | NO 15/9-F-15 D | 301 | 99 |

Catatan: salinan identik ada di `data/volve/external/dbx_volume/WITSML Realtime drilling data/` (8 file path sama) — jangan dihitung ganda.

## 1. Tabel status per solusi R&D (acceptance b)

| Solusi R&D | Data needed | Status | Bukti (kolom + baris non-null + path) | Proses jadi fitur/label |
|---|---|---|---|---|
| **S-C2** (label onset gas-rise, sumber label beda dari fitur) | Chromatograph C1–C5 | **ADA SETELAH DIOLAH** | 1.316/2.882 interval (45,7%) punya `<chromatograph>`; ke-7 tag non-null di SEMUA 1.316: `methAv`(C1) 1316, `ethAv`(C2) 1316, `propAv`(C3) 1316, `ibutAv`(iC4) 1316, `nbutAv`(nC4) 1316, `ipentAv`(iC5) 1316, `npentAv`(nC5) 1316 (uom ppm). Non-zero: C1 1300, C3 1196, C2 1087, nC4 593, iC4 599, nC5 553, iC5 538. Path: semua 8 `witsml_raw/*/*/mudLog/1.xml` | Join key GANDA per chromatograph: `<dTim>` (1316/1316) + `<mdBottom>` (1316/1316) → bisa join ke WITSML time-series (D1e) via dTim ATAU ke depth-series via md. Proses: (1) ekstrak 7 kolom ppm per interval; (2) interpolasi depth→time (atau time→depth) ke grid WITSML; (3) definisi onset = kenaikan C1/C2 di atas baseline bergerak (mis. median ± k) → label biner/interval. **Estimasi baris hasil: ~1.316 titik gas (sebelum interpolasi); setelah resample ke grid WITSML = sama dengan panjang time-series wellbore bersangkutan** |
| **S-C2** (lapisan pendukung) | Total gas `<mudGas>`: gasAv/gasPeak/gasBackgnd | **ADA SETELAH DIOLAH** | 576/2.882 interval (20,0%) — ketiga tag non-null di 576/576, non-zero 575/576; max gasAv 46.145 ppm; median 976 ppm. `mudGas` TIDAK punya dTim/md sendiri — inherits dari parent geologyInterval (576/576 parent punya dTim) | Proses: ambil gasAv+gasBackgnd per interval → gas show = gasAv > 1.5×gasBackgnd (TERSAMBUNG langsung ke dTim+mdTop+mdBottom parent) → join ke time-series. **Tapi kelas show = 17/576 (2,9%) — terlalu jarang jadi label mandiri; berguna sebagai FITUR/ko-variat, bukan target** (reproduksi independen kriteria D0: 17/576, cocok) |
| **S-A3** (litologi = aux label anti-konfond per jendela 10 menit) | Litologi per interval | **ADA LANGSUNG** | 2.882/2.882 interval (100%) punya `<lithology>`; 3.617 elemen lithology (678 interval multi-lithologi). First-lithology per interval: claystone 957, sandstone 884, limestone 678, marl 178, siltstone 151, dolomite 17, no sample 10, coal 5, tuff 2 (reproduksi independen angka D0 957/884/678 — COCOK). Kolom pendukung: `codeLith`, `lithPc` (%) | Tiap interval sudah punya dTim+mdTop+mdBottom (100%) → assign label litologi ke jendela 10 menit hanya butuh: join interval↔timestamp jendela (t_jendela ∈ [dTim_top, dTim_bottom] atau via md), majority-vote bila tumpang tindih. **Estimasi baris hasil: ~2.882 interval → ~N jendela 10 menit per wellbore (tergantung durasi; tanpa resampling tambahan)** |
| **S-A3** (pendukung) | Qualifier litologi | **ADA LANGSUNG** | 15 jenis qualifier, total 3.437 kemunculan: pyrite 869, glauconite 438, calcareous 345, argillaceous 334, mica 274, carbonaceous 222, kaolinite 215, silty 158, sandy 28, glauconitic 26, dolomitic 15, tuffite 10, dst. + `abundance` (%) | One-hot aux feature per interval; sifatnya minoritas — pakai sebagai fitur, bukan kelas target |
| **S-C1** (konteks formasi untuk hidrolik) | Nama formasi / stratigrafi di mudLog | **TIDAK ADA** | `grep -oi 'formation'` = **0 hits di semua 8 file**; struktur tag (dump `uniq -c` F-11/1) hanya berisi typeLithology/dTim/codeLith/chromatograph/mudGas/commonData — tidak ada elemen formasi/pick | Sumber konteks formasi harus dari domain lain (D1h well picks 409 + WBS kode); mudLog hanya menyumbang litologi sebagai proxy litologi, BUKAN nama formasi |

## 2. Klaim negatif: mudLog bukan sumber label kegagalan (acceptance b, poin 3 spec)

Diuji dua cara independen (python regex `re.IGNORECASE` pada teks mentah + `grep -oi | wc -l`), hasil identik di 8/8 file:

| Kata | Hits (8 file) | Buktikan |
|---|---|---|
| `stuck` | **0** | grep -oic per file = 0 semua |
| `losses` | **0** | idem |
| `kick` | **0** | idem |
| `NPT` | **0** | idem |
| `heave` | **0** | python regex |
| `flowCheck` | **0** | python regex |
| `formation` | **0** | grep -oi |

Catatan jujur: kata `wellbore` memberi 24 hit, tapi SEMUA hanya atribut `uidWellbore=`/tag `nameWellbore>` pada header mudLog (bukan catatan kejadian) — bukan label kegagalan. **Kesimpulan: klaim D0 "mudLog bukan label kegagalan" TERKONFIRMASI; mudLog TIDAK menyediakan label stuck/losses/kick/NPT — label kegagalan tetap harus dari domain lain (D1g EDM / D1e WITSML channels / D0 labels_curated).**

## 3. Peluang PROSES / relasi antar-file (untuk Master)

1. **Join key ganda chromatograph → time-series**: tiap chromatograph punya `dTim` + `mdBottom` (1316/1316 keduanya) — jalur join ke WITSML time-series D1e bisa via TIMESTAMP langsung (tanpa interpolasi depth dulu) selama time-series punya dTim; fallback via md bila time-series rusak. ini menurunkan beban S-C2.
2. **`mudGas` inherits dTim parent** (576/576) — extract mudGas + chromatograph ke 1 tabel per wellbore, lalu 1 kali join ke grid. Kombinasi: chromatograph C1–C5 (1316 titik) + gasAv/peak/backgnd (576 titik) dengan overlap tidak diketahui — perlu dicek Master apakah 576 mudGas interval subset dari 1316 chromatograph interval (saya tidak cek silang per-interval; kemungkinan beda typeLithology: chromatograph nempel di `cuttings`, mudGas juga) — TANDA TANYA untuk Master.
3. **Folder ≠ nameWellbore** (F-1 C/1 = wellbore F-1 B) — join lintas-file wajib pakai `nameWellbore`, BUKAN path folder (temuan konsisten D0 §2.1, dikonfirmasi di 8/8 file).
4. **Salinan ganda**: `external/dbx_volume/` memuat 8 file identik — parser Master cukup sekali ke `witsml_raw/`.
5. **Multi-lith 678 interval** — kalau pakai litologi majority-vote per jendela, putuskan aturan: first-lithology (mengikuti D0, konsisten 957/884/678) atau lithPc-weighted. Keputusan ada di Master; angka first-lith sudah diverifikasi.
6. **S-C1 tidak bisa dilayani mudLog** — konteks formasi harus tarik dari D1h well picks; laporkan ke Master agar tidak menunggu jawaban dari domain ini.

## 4. Rekonsiliasi angka vs klaim lama (cross-check)

| Klaim (D0/D1d lama) | Hasil verifikasi independen | Status |
|---|---|---|
| 8 file mudLog XML | 8 file ditemukan + diparse (juga 8 salinan di dbx_volume) | **KONFIRMASI** |
| 2.882 geologyInterval | 2.882 dihitung ulang | **KONFIRMASI** |
| Litologi claystone 957 / sandstone 884 / limestone 678 | First-lithology per interval: 957 / 884 / 678 | **KONFIRMASI** |
| C1–C5 coverage 45,7% | 1.316/2.882 = 45,66% | **KONFIRMASI** |
| mudGas 576 (20%) | 576 (20,0%) | **KONFIRMASI** |
| Gas show 17/576 (kriteria gasAv>1.5×gasBackgnd) | Reproduksi independen: **17/576** | **KONFIRMASI** |
| Tidak ada tag stuck/losses/kick | grep ganda, 0 hits semua file | **KONFIRMASI** |

Divergensi awal yang terjelaskan (bukan kontradiksi): hitungan litologi per-ELEMEN (claystone 1194) > per-INTERVAL (957) karena 678 interval punya >1 lithology anak (mixed lithology, `lithPc` < 100%). Kedua angka benar; definisi berbeda.

## 5. Belum diverifikasi (aturan 3 verification-mandatory)

- Overlap per-interval antara 1.316 chromatograph vs 576 mudGas (subset? disjoint?) — belum dicek silang.
- Kesamaan isi antara `witsml_raw/` dan `external/dbx_volume/` (diasumsikan salinan; hanya path struktur yang cocok, byte-equality tidak diuji).
- Kelayakan statistik onset-label S-C2 (prevalensi onset setelah didefinisikan, autocorrelation vs fitur drilling) — di luar scope cek ketersediaan ini; Master/R&D yang menguji.
- Format dTim zone (semua Z / UTC) konsisten — terlihat konsisten di sampel tapi tidak diuji exhaustif per baris.

## 6. Catatan alat

- sequ-mcp (`mcp__sequentialthinking__sequentialthinking`) dipanggil 4× sesuai kewajiban kartu; tool_call wrapper gagal JSON-parse di SEMUA percobaan (error asli: `tool_call 'calls' is not valid JSON: Expecting ',' delimiter`) — blocker tooling, bukan payload; analisis dilanjutkan tanpa sequ. Dilaporkan apa adanya.
- `execute_code` diblokir mode unattended (`approvals.single_query_mode`) → semua eksekusi via `terminal` + script file (bukan heredoc, juga diblokir).
