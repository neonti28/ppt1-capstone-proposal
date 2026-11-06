# V6-A2 — AUDIT KLAIM ML (V6-E1) + KLAIM ILMIAH (V6-R1): BERDASAR ATAU KARANGAN?

Task: `t_412436b2` [Auditor 2] · Board: capstone-v6-solve · Tanggal: 2026-10-10 (WIB)
Objek audit: `docs/V6_E1_ML_DESIGN.md` (+ kode & hasil run di `code/v6_e1_*.py`,
`scratch/v6_e1/`) dan `docs/V6_R1_SCIENCE.md`.
Independensi: SEMUA angka di bawah dihitung ulang oleh skrip milik auditor
(`evidence/audit_*.py`, log & JSON di workspace kartu ini), bukan disalin dari dokumen.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiap klaim dipisah
> OBSERVASI (output tool) / INFERENSI / HIPOTESIS; tes pembeda dipakai untuk
> membedakan "label memang terprediksi" vs "label bisa dihafal" (kontrol
> tumpang-tindih jendela) dan "sinyal lintas-sumur" vs "sinyal dalam-sumur".
> **Riset pendahuluan: `statistical-analysis`** — gate dihitung ulang bukan hanya
> dari titik AUPRC tetapi dari CI95 bawah (moving-block bootstrap sudah tersimpan
> di JSON hasil); prevalensi & lift diperiksa per fold, tidak dirata-rata.
> **Riset pendahuluan: `peer-review`** — peta klaim→bukti→vonnis per baris,
> kelemahan dilaporkan proporsional, tidak ada tuduhan niat; cacat proses audit
> sendiri (lihat §6) ikut ditulis.
> **Riset pendahuluan: `verification-mandatory`** — bukti mentah disertakan,
> cross-check minimal 1 sumber berbeda per klaim kunci, daftar "belum diverifikasi"
> wajib di §7.

---

## 0. RINGKASAN Vonnis (1 kalimat per kelompok)

| Kelompok klaim | Vonnis |
|---|---|
| Angka hasil run V6-E1 (AUPRC/lift/CI per fold, 4 kampanye) | **TERVERIFIKASI REPRODUKSI** — 4/4 kampanye dijalankan ulang, semua metrik identik |
| Pra-registrasi & anti-geser-gate | **TERVERIFIKASI** — hash cocok, timestamp komentar mendahului file hasil, gate di kode = gate di pra-reg |
| "3 jenis kerusakan benar-benar berbeda" | **TERVERIFIKASI** — kanal & fisika berbeda, ko-positif vib×ssi nyaris nol (phi 0,025) |
| Klaim "label bukan fungsi deterministik dari fitur" (E1d `bit_wear`) | **TERBANTAH untuk pembacaan dalam-sumur** — label ~deterministik dari fitur yang DIIZINKAN bila diinterpolasi dalam sumur (AUPRC 0,83–0,99 pada jendela non-tumpang-tindih) |
| "3 kriteria terpenuhi" | **SAH secara literal pra-reg (3 kelas lolos G1+G2), TIDAK pada pembacaan ketat (2 kelas LULUS penuh)** — dokumen sudah membuka kedua bacaan, tidak disembunyikan |
| Kelemahan statistik gate `ssi` | **DIBONGKAR** — G1 `ssi` dihitung dari titik; dengan CI95 bawah, hanya 2/5 fold lift≥1 dan 1/5 fold lift≥1,5 |
| Populasi kelas rumus paper di Volve (V6-R1) | **TERVERIFIKASI REPRODUKSI** — 24 klaim populasi dihitung ulang dari CSV mentah, semua cocok |
| Sitasi V6-R1 | **TERVERIFIKASI** — 9 sumber dicek langsung; isi sumber cocok dengan klaim dokumen; 2 koreksi dokumen (DOI Tunkiel, satuan kuantil MSE/DS) terbukti benar |

---

## 1. Metode audit & peta bukti

| Prosedur (dari kartu) | Aksi auditor | Artefak bukti |
|---|---|---|
| 1. Jalankan ulang | 4 kampanye training dijalankan ulang penuh: `v6_e1_30_lowo.py` (E1a), `32_hyd_lowo.py` (E1b), `51_toolwear_lowo.py` (E1c), `61_usrop_lowo.py` (E1d) | `evidence/E1*_RERUN_*`, `cmp_e1d.py`, `cmp_e1.py`, `cmp_e1b.py` |
| 2. Anti-kabur 3 kelas | Cek sumber kanal per kelas + hitung ko-positif/phi/jaccard antar label pada jendela yang sama | `audit_circularity2.py` → `audit_circularity.json` |
| 3. Sirkularitas label | (a) rekonstruksi label USROP dari kolom terlarang vs diizinkan (CV); (b) kedalaman-saja vs RF; (c) kontrol tumpang-tindih jendela; (d) provenansi label E1d dibangun ulang dari data mentah | `audit_circularity.py`→`audit_partAB.json`, `audit_circularity2.py`, `audit_overlap_control.py`, `audit_label_provenance.py` |
| 4. Anti-geser-gate | `sha256sum` 4 dokumen pra-reg vs hash di komentar kartu; bandingkan timestamp komentar vs mtime file hasil; baca gate di pra-reg vs gate di kode vs angka di dokumen | §3 tabel |
| 5. Klaim ilmiah V6-R1 | Hitung ulang populasi kelas untuk SEMUA rumus paper yang diklaim "sudah diuji di Volve"; verifikasi langsung 9 sitasi (Crossref API, PDF penerbit, halaman arXiv, README dataset) | `audit_r1_recompute.py`→`audit_r1_recompute.json`, §5 |

Lingkup data: `data/USROP_labeled.csv` (198.928 baris), `data/volve/witsml_parsed/F-14.csv`
(1.648.026 baris), `scratch/v6_e1/windows/*.csv.gz` (7 sumur), `usrop_windows.csv`
(3.953 jendela). Lingkup yang tidak diulang: skrip pembangun jendela (00/01/10/20/31/50/60),
SHAP (40) — lihat §7.

---

## 2. AUDIT V6-E1 — tabel per klaim

| # | Klaim (V6_E1_ML_DESIGN.md) | Metode audit | Hasil (angka auditor) | Vonnis |
|---|---|---|---|---|
| 1 | vib: AUPRC 0,912 / 0,562 / 0,491 / 0,441, lift 1,61–3,50, G1 4/4 G2 4/4 → LULUS | Jalankan ulang `v6_e1_30_lowo.py` penuh (4 kelas) | Fold identik persis (contoh F-14 0,9117 lift 1,6133; F-15_S 0,4914 lift 3,4972); JSON beda HANYA di `fit_time_s`/`elapsed_s` (21 diff, 0 diff non-timing) | **TERVERIFIKASI REPRODUKSI** |
| 2 | ssi: lift 1,47–6,64, G1 4/5 G2 5/5, persistence 0/5 → LULUS | Sama (rerun) + hitung ulang gate dari CI95 | Titik identik (F-15_S 0,1057 lift 6,6442; F-9_A 0,0961 lift 1,4701). **TAPI** CI95 bawah < prevalensi di 3/5 fold (F-14 0,0096 vs prev 0,0137; F-15A 0,0043 vs 0,0051; F-9_A 0,0297 vs 0,0654) → lift-CI-bawah ≥1 hanya 2/5, ≥1,5 hanya 1/5 | **Angka reproduksi; vonnis LULUS sah menurut gate pra-reg (titik) tetapi RAPUH — tidak diungkap dokumen** |
| 3 | stuck GAGAL (1/2 fold), shk GAGAL (3/7) | Rerun + CI | Identik; CI-bawah stuck F-9_A lift 0,839 (<1), shk ≥1 hanya 2/7 | **TERVERIFIKASI — kegagalan dilaporkan jujur** |
| 4 | hyd GAGAL (lift 0,80–2,35, persistence > RF 7/7) | Rerun `v6_e1_32_hyd_lowo.py` | 7/7 fold identik (n, pos, prev, AUPRC, lift, depth-canary, logreg, persistence, CI) | **TERVERIFIKASI REPRODUKSI** |
| 5 | tool_wear GAGAL (lift 1,09–1,42 <1,5 di 4/4) | Rerun `v6_e1_51_toolwear_lowo.py` | T01–T04 identik (0,5433/1,087 · 0,7684/1,388 · 0,7031/1,418 · 0,6497/1,299) | **TERVERIFIKASI REPRODUKSI** |
| 6 | bit_wear LAYAK BERSYARAT (G1 3/4, G2 4/4, persistence > RF 4/4) | Rerun `v6_e1_61_usrop_lowo.py` | 7 fold identik (F-14 0,2982/3,110; F-15 0,3645/2,486; F-15S 0,8133/1,495; F-5 0,7830/1,652); JSON beda hanya waktu | **TERVERIFIKASI REPRODUKSI** |
| 7 | 3 kelas = jenis kerusakan BERBEDA, bukan tingkatan/bukan pengukuran ganda | Kanal label dicek per kelas (VIBLAT_RT vs SSI(CRPM_RT) vs label MSE-USROP); ko-positif dihitung | Kanal berbeda, dataset berbeda (WITSML vs USROP) untuk kelas ke-3; phi(vib,ssi)=**0,0247**, Jaccard 0,0174 (n=15.776 jendela co-valid) → bukan gejala yang sama; WHIRL_RT/BOUNCE_RT (duplikat) terbukti tidak dipakai | **TERVERIFIKASI** |
| 8 | Label E1d = ">50% dari 100 baris SESUDAH anchor ber-label high_MSE_bit_wear" | Bangun ulang jendela dari `USROP_labeled.csv` (skrip auditor, W=100, stride=50, filter SPP≥60) | 7/7 sumur: jumlah jendela, anchor, dan label **100% cocok** (3.953/3.953; positif 91/155/561/174/3/0/0) | **TERVERIFIKASI** |
| 9 | Pra-registrasi ditulis & di-hash SEBELUM training (4 hash) | `sha256sum` vs hash di komentar kartu; timestamp komentar vs mtime JSON hasil | 4/4 hash cocok persis (54277262…, 411366be…, e2179bde…, 986f45a1…); komentar E1a 22:05 < hasil 22:17; E1b 22:35 < 22:39; E1c 22:49 < 22:50; E1d 23:01 < 23:03 | **TERVERIFIKASI** (catatan: backdating teknis tidak bisa dikecualikan penuh — keduanya berasal dari proses yang sama) |
|10 | Gate di kode = gate di pra-reg (tidak digeser) | Baca 4 skrip training + 4 dokumen pra-reg | E1a `g1 > n_eval/2` (mayoritas), <30 pos = UNDERPOWERED ✓; E1b mayoritas 7 fold ✓; E1c `g1>=3` dari 4 ✓ + canary-RMS ✓; E1d `g1>=3` dari 4, kanal MSE dilarang via asersi ✓; ambang lift 1,5 di semua kampanye, tidak ada yang diturunkan | **TERVERIFIKASI — TIDAK ADA GESER GATE** |
|11 | Angka tabel dokumen = angka hasil run | Banding JSON/log vs tabel §4.1–§4.4 | Semua angka tabel yang dicek cocok dengan log | **TERVERIFIKASI** |
|12 | "3 kriteria terpenuhi" | Bandingkan dengan gate gabungan pra-reg (E1a §6: "≥3 kelas LULUS") | Literal: 3 kelas lolos G1+G2 (vib, ssi, bit_wear). Ketat: 2 LULUS penuh + 1 diturunkan (persistence > model). Dokumen §4.5 menyatakan keduanya | **SAH LITERAL / TIDAK PADA PEMBACAAN KETAT — dibuka, bukan disembunyikan** |
|13 | SHAP: 6 fitur teratas per kelas + additivity 5/7 lolos | Tidak dijalankan ulang | — | **BELUM DIVERIFIKASI (lihat §7)** |

---

## 3. PEMBONGKARAN: sirkularitas & kedalaman-saja (temuan utama audit)

### 3.1 `bit_wear` (E1d) — label ~DETERMINISTIK dari fitur yang DIIZINKAN dalam sumur

| Tes (skrip auditor) | Hasil |
|---|---|
| Rekonstruksi baris USROP (198.928) dari kolom `MSE` saja | AUPRC **1,0000** → label memang fungsi ambang dari MSE (sesuai definisi) |
| Rekonstruksi dari kanal TERLARANG (WOB/TQ/Torque/ROP/Hookload), pohon depth-4 | AUPRC 0,961 · akurasi 0,961 → pemblokiran kanal itu BERGUNA (tanpa blokir, hampir deterministik) |
| Rekonstruksi dari kanal YANG DIIZINKAN (SPP/FLOW/MUD/GAM/MD/TVD), pohon depth-4, **split acak dalam sumur** | AUPRC **0,876**; pohon tanpa batas kedalaman **0,993** → dalam-sumur, label hampir bisa direkonstruksi penuh dari fitur yang sah |
| Sama, **GroupKFold lintas sumur** (pembatas LOWO) | AUPRC rata-rata **0,425** (lipatan 0,030–0,845) → rekonstruksi hampir hilang di sumur tak dikenal |
| Jendela NON-tumpang-tindih dalam sumur (kontrol kebocoran tumpang-tindih) | F-15S **0,992** · F-14 **0,829** · F-5 **0,922** → TETAP tinggi: bukan artefak tumpang-tindih, label memang blok kedalaman/formasi |
| **Kedalaman saja** (rank-AUPRC `anchor_depth`) per sumur uji | F-14 lift **1,65** · F-15 **1,40** · F-15S **1,68** · F-5 **0,83** → **satu fitur kedalaman saja sudah lolos gate G1 (lift≥1,5) di 3/4 fold** |
| Canary kedalaman (RF MD+TVD) vs RF penuh (angka dokumen) | RF unggul tipis: 0,298 vs 0,191 · 0,365 vs 0,288 · 0,813 vs 0,756 · 0,783 vs 0,691 → G2 lolos, tetapi margin hanya 0,058–0,107 AUPRC |
| Sebaran label vs kedalaman-formasi | Prevalensi per sumur **0% – 54%**, semuanya ditentukan median MSE per sumur (4.478 psi F-7 … 297.658 psi F-15S) terhadap **ambang GLOBAL P75 = 256.600 psi** → label lebih menandai IDENTITAS SUMUR/FORMASI daripada kondisi bit |
| Struktur blok (urut depth) | lag-1 agreement **0,915–0,987**; run positif rata-rata 5,4–80 jendela; maks 218 → menjelaskan persistence > RF di 4/4 fold |

**Vonnis:** klaim §3 E1d "label bukan fungsi deterministik dari fitur yang tersisa" **hanya
benar untuk generalisasi lintas-sumur**; pada pembacaan dalam-sumur (yang persis yang
dilakukan persistence & canary) label hampir deterministik dari fitur yang diizinkan,
dan G1 bisa dipenuhi oleh kedalaman saja. Kesimpulan jujur kelas ini = **SIRKULAR-DALAM-SUMUR /
konfuk kedalaman**, konsisten dengan downgrade "LAYAK BERSYARAT" yang sudah dipilih tim,
tetapi dokumen tidak menyebut dua fakta ini (kedalaman-saja lolos G1; label = ambang global
yang menandai formasi).

### 3.2 `vib` / `ssi` (E1a) — tidak sirkular, tetapi `ssi` rapuh

| Tes | vib | ssi |
|---|---|---|
| Sumber label | `VIBLAT_RT` (MWD lateral), kanal tidak pernah masuk daftar fitur (dicek: FEATS = 11 kanal permukaan) | SSI dari `CRPM_RT` (RPM collar MWD), kanal tidak masuk fitur |
| Rekonstruksi in-well, split acak | 0,974–0,991 | 0,657–0,718 |
| Rekonstruksi in-well, **jendela non-tumpang-tindih** (kontrol) | **0,831–0,919** (lift 1,59–5,97) → label memang terikat rezim operasi permukaan dalam sumur | F-5 **jatuh 0,718 → 0,068** (lift 33 → 3,2) → sebagian besar rekonstruksi = tumpang-tindih/autokorelasi pendek |
| LOWO (angka tim, reproduksi) | lift 1,61–3,50, CI-bawah ≥ prevalensi di **4/4** fold | lift 1,47–6,64, CI-bawah ≥ prevalensi hanya **2/5** fold |
| Persistence | > RF di 2/4 fold (bukan mayoritas) | 0/5 fold |

**Vonnis:** `vib` = **klaim terkuat** di seluruh kampanye (gate + CI + beda-jenis terverifikasi).
`ssi` = **LULUS secara ketetapan pra-reg, tetapi tidak kokoh**: separuh fold tidak memisahkan
diri dari prevalensi pada taraf CI95, dan sinyal dalam-sumurnya sebagian besar berasal dari
tumpang-tindih jendela. Dokumen melaporkan CI di tabel (jujur) tetapi tidak menarik kesimpulan
kekuatan bukti dari CI itu.

### 3.3 `hyd`, `tool_wear`, `stuck`, `shk` — sudah GAGAL, tidak ada yang dilebih-lebihkan
Gate dihitung ulang dari JSON: semua konsisten dengan dokumen (hyd G1 2/7; tool_wear G1 0/4;
stuck G1 1/2; shk G1 3/7). Tidak ada kegagalan yang digelar sebagai sukses.

---

## 4. AUDIT V6-R1 — populasi kelas rumus paper (dihitung ulang dari CSV mentah)

Skrip auditor `evidence/audit_r1_recompute.py` (bukan skrip R1). Semua klaim di bawah
diambil dari rumus yang **diklaim sudah diuji di Volve**.

| Rumus paper | Klaim dokumen | Hasil auditor | Vonnis |
|---|---|---|---|
| Teale 1965 MSE (USROP, 198.928 baris) | selisih median 4,98e-05; korelasi log10 0,9999999999989; median 102.631 psi | **5,006e-05**; **0,9999999999996**; kolom MSE tersimpan terkonfirmasi Teale | **TERVERIFIKASI** |
| Rule lama MSE>P75 elif ROC<P25 | 49.732 / 15.183 / 134.013 · kecocokan 100% | **49.732 / 15.183 / 134.013** · P75 = 256.600 psi · kecocokan **100,00%** | **TERVERIFIKASI** |
| Menand & Mills 2017 MSE/DS (DOC = ROP[m/h]/(60·RPM)) | n 198.602 · 12.501 / 93.334 / 78.212 / 14.555 · kuantil 0,824/2,318/3,990/6,438/15,557 | **identik semua** (kuantil 0,824/2,318/3,990/6,438/15,557) | **TERVERIFIKASI** (angka "setelah koreksi satuan" = versi benar; versi salah tersimpan di JSON v2 sesuai peringatan §10.3) |
| Liu 2025 SSI (permukaan RPM, jendela 180 s, F-14) | 344.396 jendela · moderate 320 · severe 0 | **344.396 · 320 · 0** | **TERVERIFIKASI** |
| TVI (torque variation index) F-14 | 330.121 jendela · P75 0,1224 · >P75 82.530 | **330.121 · 0,1224 · 82.530** | **TERVERIFIKASI** |
| Kanal MWD F-14 (SHKRSK≥1, VIBLAT≥32,174, STUCK≥1) | 180 · 714 · 394 (non-null 21.643/2.247/5.147) | **180 · 714 · 394**; non-null **21.643 · 2.247 · 5.147** | **TERVERIFIKASI** |
| Hidraulik residual SPPA vs `qcut(TFLO,10)` | n 299.228 · 58.317 (19,49%) | **299.228 · 58.317** | **TERVERIFIKASI** |
| SSI collar-MWD F-14 (§8.2: 22.976 jendela, 1.005 moderate, 38 severe) | populasi kelas lintas-sumur | Dihitung ulang auditor dengan jendela berbasis WAKTU 180 s di baris pengeboran → hanya **59 jendela** (CRPM pengeboran non-null 3.258 baris); angka §8.2 memakai jendela berbasis JUMLAH BARIS pada subseri CRPM non-null (23.110 baris) → **dua metode berbeda, keduanya tidak salah, tetapi angka §8.2 sensitif metode dan tidak boleh dikutip tanpa menyebut jendela-count** | **TERVERIFIKASI DENGAN CAVEAT METODE** |

Catatan batas rumus: grading Liu 2025 di sumbernya `SSI<1 / 1<SSI≤3 / SSI≥3` dan SSI
dihitung dari RPM DOWNHOLE; R1 §4.2 memakai `1≤SSI<3` pada RPM permukaan (selisih batas
= nol praktis untuk variabel kontinu, tetapi pemindahan ke RPM permukaan adalah TRANSPLANTASI
metode, bukan replikasi; kelas `ssi` E1a justru memakai CRPM = RPM collar MWD = sesuai sumber).

## 5. AUDIT V6-R1 — verifikasi sitasi (langsung, bukan salinan)

| Sitasi | Sumber yang dibuka auditor | Isi yang diverifikasi | Vonnis |
|---|---|---|---|
| Teale 1965, DOI 10.1016/0148-9062(65)90022-7 | `api.crossref.org/works/...` | "The concept of specific energy in rock drilling", Vol. 2 Issue 1, hlm. 57–73, 1965 | **HIDUP & SESUAI** |
| Menand & Mills 2017, AADE-17-NTCE-033 | PDF aade.org (dibuka segar; catatan TLS-transien dokumen tidak terulang) | Eq.1 MSE identik; Eq.5 `DS=WOB/(R·DOC)`; *"typical MSE/DS ratio for efficient drilling is between 1 and 1.5 and can be largely above 5"*; TOB dari ΔP motor (Eq.2–3) & torque-drag (Eq.4); studi kasus Eagle Ford | **HIDUP & SESUAI (kutipan harfiah)** |
| Liu 2025, Thermal Science 29(2B), DOI 10.2298/TSCI2502521L | PDF thermalscience.rs | Judul/vol/hlm cocok; grading Eq(2) `SSI<1 torsional; 1<SSI≤3 moderate; ≥3 severe` (sumber memakai RPM downhole) | **HIDUP & SESUAI** (batas atas 3 vs `<3` dokumen = selisih nol praktis) |
| Cao 2025, arXiv:2503.07440 | PDF arXiv + README github `promiseeee/Time-series-stuck-pipe-prediction` | *"time-based data from the Volve drilling dataset"*; tabel warning time τ=15 → **2,67** menit dan τ=45 → **7,37** menit → rentang "2,67–7,37 menit" dokumen akurat; dataset TSPP = turunan Volve (Equinor 2018) | **HIDUP & SESUAI** |
| Al-Mamoori 2025, DOI 10.3390/app15095042 | halaman MDPI | *"time series drilling data from the Volve field"*, AE dilatih hanya kondisi normal; akurasi **99,06%**, AUC **0,958**, precision 97,12%, recall 91,34%, F1 94,15% — angka persis seperti dikutip | **HIDUP & SESUAI** |
| Saadeldin 2023, DOI 10.1038/s41598-023-33411-9 (PMC10110595) | halaman PMC | *"surface rig data"*, *"three types of downhole vibrations (axial, torsional, and lateral)"*, *"correlation coefficient (higher than 0.9)"*, *"average absolute percentage error (below 7.5%)"*, validasi well tak terlihat | **HIDUP & SESUAI** |
| Saini 2020, DOI 10.2118/200006-MS (abstrak via scilit) | halaman scilit | *"commonly available rig surface sensor data and mud motor parameters"*, *"Over 100 historical unconventional wells"*, *"10 different dysfunction categories were classified"*, paling umum whirl/stick-slip/bit balling | **HIDUP & SESUAI** |
| Sumber [7] Tunkiel — koreksi DOI run-3 | Crossref untuk 108069 DAN 108128 | 108069 = "Reference dataset for rate of penetration benchmarking" (Tunkiel/Sui/Wiktorski); 108128 = "Training-while-drilling approach to inclination prediction…" → **koreksi dokumen terbukti benar** | **KOREKSI TERVERIFIKASI** |
| arXiv 2302.11135 (diklaim WITHDRAWN) | tidak dibuka ulang oleh auditor ini | — | **BELUM DIVERIFIKASI ULANG (lihat §7)** |

Vonnis sitasi: **tidak ada sitasi hiasan/karangan** pada 8 dari 9 sumber yang dibuka;
setiap kutipan yang dicek memuat klaim persis seperti yang dipakai dokumen.

---

## 6. Kesalahan proses audit ini (ditulis apa adanya)

1. Skrip pertama auditor (`audit_circularity.py`) gagal di bagian C (ZeroDivisionError
   pada pasangan label yang tidak pernah co-valid) dan sempat menghitung rekonstruksi
   in-well secara IN-SAMPLE (angka 1,00 = pohon menghafal, bukan bukti sirkularitas).
   Diperbaiki: bagian A/B disimpan lebih dulu, lalu seluruh pengukuran diulang dengan
   validasi silang (`audit_circularity2.py`) + kontrol tumpang-tindih (`audit_overlap_control.py`).
2. Bug kesalahan sendiri kedua: mask boolean kehilangan index setelah `set_index` →
   TVI/SSI sempat terhitung 0 jendela (keliru awalnya dikira ketidakcocokan dokumen);
   setelah diperbaiki semua angka F-14 cocok. Klaim "0 jendela" DIBATALKAN.
3. Rerun E1a/E1d menimpa file hasil asli; backup diambil SEBELUM rerun dan file asli
   sudah dikembalikan (sha256 identik dengan backup). Rerun E1b/E1c TIDAK dibackup lebih
   dulu → pembanding memakai teks log yang ditangkap sesi ini sebelum rerun; 3 selisih
   digit terakhir pada ujung CI bila dibandingkan berasal dari penyalinan teks panjang
   oleh auditor, bukan dari run (semua metrik substansial identik).

## 7. Belum diverifikasi (daftar wajib)

1. **SHAP V6-E1** (`v6_e1_40_shap.py`, `E1_SHAP.json`): peringkat fitur & klaim additivity
   tidak dijalankan ulang.
2. **Skrip pembangun jendela/bin** (00, 01, 10, 20, 31, 50, 60): rerun audit hanya
   mengulang TRAINING/EVALUASI; provenansi label E1d diverifikasi terpisah (§2 #8),
   tetapi pembangunan jendela E1a/E1b/E1c tidak diulang.
3. **Populasi multi-sumur R1 §8.2** (F-5/F-9/F-15_S/F-15A/F-7) dihitung ulang hanya untuk
   F-14; sumur lain tidak diulang auditor.
4. **Klaim R1 §9** (I1 TOB, I5 RPM, I8 CCS, I9 UCS) tidak dihitung ulang di audit ini.
5. **Status WITHDRAWN arXiv 2302.11135** tidak dibuka ulang oleh audit ini (klaim berasal
   dari run-3 R1 yang menyimpan bukti liveness-nya).
6. **Kebenaran historis timestamp pra-reg** (apakah file memang tidak pernah ditulis
   ulang sebelum hash) tidak bisa dibuktikan penuh dari luar proses yang sama.

## 8. Kesimpulan & rekomendasi

1. **Tidak ada klaim angka karangan** di V6-E1 maupun V6-R1 yang berhasil ditemukan audit ini.
   Semua angka hasil run yang diuji (4 kampanye, 24 klaim populasi) tereproduksi dari
   eksekusi ulang / data mentah, dan sitasi yang dicek hidup serta isinya persis.
2. **Yang dibongkar bukan angkanya, melainkan kekuatan bukti di balik dua vonnis:**
   - `ssi` LULUS bertumpu pada titik; pada CI95 hanya 2/5 fold lift≥1 (1/5 fold lift≥1,5).
   - `bit_wear` = kelas konfuk kedalaman/formasi: label hampir deterministik dari fitur
     yang diizinkan dalam sumur (AUPRC 0,83–0,99 non-tumpang-tindih), **kedalaman saja
     lolos G1 di 3/4 fold**, dan prevalensi 0–54% ditentukan ambang global P75 terhadap
     median MSE per sumur.
3. **Klaim ">3 kriteria"** sah pada pembacaan literal pra-reg (3 kelas lolos G1+G2) dan
   tidak sah pada pembacaan ketat (2 kelas LULUS penuh). Dokumen sudah membuka keduanya —
   ini BUKAN penggelapan, tetapi kalimat "TERPENUHI BERSYARAT" jangan dipakai sendirian
   di depan dosen tanpa dua kalimat pembatas di §4.5.
4. Rekomendasi perbaikan dokumen (opsional, bukan syarat kelulusan kartu): (a) tambahkan
   baris CI-bawah-lift per fold untuk `ssi`; (b) catat bahwa G1 `bit_wear` bisa dipenuhi
   kedalaman saja dan bahwa labelnya ambang global lintas-formasi; (c) §8.2 R1 diberi
   catatan metode jendela-count untuk angka SSI collar-MWD.

**Pernyataan akhir:** berdasar eksekusi ulang 4 kampanye + 24 hitung-ulang populasi +
9 sitasi, klaim ML/ilmiah di V6-E1 & V6-R1 **BERDASAR**; dua kelemahan kekuatan bukti
(`ssi` rapuh pada CI, `bit_wear` = konfuk kedalaman) **DIBONGKAR di §3** dan tidak boleh
digelar sebagai detektor siap pakai.

Lampiran bukti (durable): `/mnt/d/Capstone 1/scratch/v6_a2_evidence/` (27 file — skrip +
JSON + log; salinan di workspace kartu `t_412436b2`/`evidence/`): `E1_RERUN_*`, `E1d_RERUN_*`,
`ORIG_captured_E1b_LOWO_RUN_LOG.txt`, `cmp_e1*.py`, `audit_circularity.py`,
`audit_circularity2.py`, `audit_overlap_control.py`, `audit_final_analysis.py`,
`audit_r1_recompute.py`, `audit_label_provenance.py`, `grep_citations.py`,
dan JSON: `audit_partAB.json`, `audit_circularity.json`, `audit_overlap_control.json`,
`audit_final_analysis.json`, `audit_r1_recompute.json`, `audit_label_provenance.json`.
