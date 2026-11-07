# CHANGELOG.md — Capstone 1 (PT Halliburton Indonesia · Sperry Drilling · TI UNS)

Tujuan file ini (diminta user, 2026-10-06): **transparansi masalah selama pembuatan + perubahan yang dilakukan**, termasuk mengapa verdict selalu "LULUS BERSYARAT" dan apa tindakan perbaikannya.
Aturan baca: setiap entri = masalah → dampak → tindakan → status. Angka hanya dari output eksekusi nyata.

---

## [2026-10-29 11:50 WIB] Dashboard desain dipindah ke folder capstone, disambungkan ke engine V9-I1

**Masalah:** ada dua dashboard. Desain Halliburton (`D:\Download\Magang Halliburton\dashboard-dummy`) disajikan di `http://127.0.0.1:8899` tetapi seluruh angkanya data demo yang dibangkitkan di browser. Dashboard v1 di `dashboard/` memuat angka engine tetapi tidak memakai tema DESIGN.md. Dua lokasi, dua sumber angka, rawan salah baca saat sidang.

**Tindakan:**
1. Isi `dashboard-dummy` disalin ke `dashboard/`; dashboard v1 lama dipindah utuh ke `dashboard_v8_backup/` (7 berkas, termasuk 6 PNG viz dan index.html lama).
2. `DESIGN.md` disalin ke `dashboard/DESIGN.md` supaya folder mandiri.
3. Ditambah `code/31_export_dashboard_data.py`: membaca `scratch/v9_i1/v9_i1_RESULTS.json` (57.555 byte) dan menulis `dashboard/data/engine_v9_i1.json` (62.802 byte). Skrip hanya membentuk ulang dan menghitung, tidak mengubah nilai.
4. `js/data.js` diganti: fetch JSON nyata dengan kegagalan nyata (404, timeout 12 detik, `file://`), bukan data demo.
5. `js/charts.js` ditambah `hbars`, `scatter`, `stack`; `js/app.js` ditulis ulang untuk 7 view baru; `css/styles.css` ditambah komponen (matrix, chip, hbar, head row, layer card, def list) memakai token DESIGN.md yang sama.
6. Tujuh menu: Dashboard, Engines, Heads, Analytics, Decision layers, Method and limits, Settings. Tidak ada menu tanpa halaman.
7. `README.md` dashboard ditulis ulang; dua preview PNG diambil ulang dari build baru (1440x900 dan 390x844).

**Angka yang sekarang tampil (dibaca runtime dari JSON, bukan diketik):** 7 engine, 27 head, L0 5 / L1 11 / L2 9 / L3 2, 11 peringatan L1, 0 slot alarm otomatis, tier TREN 13 / PERINGATAN-BERPENGAWAS 12 / BELUM LAYAK PAKAI 2, 24 head ber-metrik, 20 titik scatter, 4 head tidak pernah memicu (presisi tidak terdefinisi), lapisan B terukur pada 1 dari 7 engine, head utama `hyd · hybrid_rule_and_persistence` presisi 0,8243 / recall 0,5965 / FAR 16,611 / lead 8,0 menit, DDR 23.447 record / 39.397,986 jam / equipment failure 2.739,667 jam.

**Verifikasi yang dijalankan (bukan klaim):**
- `curl` 8899: `index.html` 200, `data/engine_v9_i1.json` 200 62.802 byte, css dan 3 js 200.
- Peramban headless, hook `error` + `unhandledrejection`: 0 error konsol di seluruh view.
- Hitungan elemen setelah render: KPI 4, donut layer 4 segmen, review 7 baris, gauge 3 metrik, matrix 21 sel / 7 baris, scatter 20 titik, downtime 5 baris, tabel head 8 baris, tier 3 segmen, segment 6 baris, engine 7 kartu, head 27 baris, analytics 7 baris stack + 7 bar + 10 baris active share + 5 baris nodata + 8 + 5 + 24 baris tabel, layer 4 kartu / 27 item, method 6 sumber / 5 batas / 7 meta.
- Interaksi: 7 menu, filter layer (11 baris), filter FAR>25 (3 baris), reset (27), modal head (15 pasangan dt/dd) tutup dengan Escape, modal engine (4 baris tabel), popover bell (3 notifikasi, badge 3 ke 2), menu user, About, search "hyd" (4 baris), settings animasi/kerapatan/urutan tersimpan di localStorage, tombol goto (Layers, Analytics, Heads), retry.
- Empty state: L3 + FAR<=6 menghasilkan 0 baris dan pesan kosong tampil.
- Error state nyata: berkas JSON disembunyikan sementara, halaman menampilkan "The server answered 404 for data/engine_v9_i1.json."; berkas dipulihkan, tombol Retry memuat ulang dan KPI kembali 4.
- Overflow horizontal: 1440, 1180, 1024, 900, 768, 390 px semuanya `scrollWidth` <= viewport; tabel lebar menggulir di dalam wadahnya sendiri dengan petunjuk "swipe".
- Kontras: audit otomatis 19 selector teks, tidak ada yang di bawah 4,5:1.
- Keyboard: Tab nyata lewat CDP menunjukkan focus ring 2px pada setiap kontrol.
- `grep -c "—"`: 0 pada index.html, app.js, data.js, charts.js, styles.css.

**Batas yang tetap berlaku:** tidak ada angka rupiah, tidak ada pemetaan work order ke alarm, tidak ada alarm otomatis, klaim hyd K-ii masih `BELUM TERSEDIA DI PROTOTIPE`, dan empat head Random Forest hanya hidup dengan `--ml`. Semuanya ditampilkan di view Method and limits, bukan disembunyikan.

**Status:** SELESAI.

---

## [2026-10-29 11:28 WIB] KEPUTUSAN FINAL GELOMBANG 2 — komposisi engine, nilai maintenance, penutupan audit

Catatan untuk sesi dan agent lain: entri ini adalah rujukan keputusan terbaru. Bila ada entri lain yang bertentangan soal komposisi hyd atau status catatan audit, entri ini yang berlaku.

### 1. Keputusan komposisi per kelas kerusakan

| Kelas | Komposisi terpilih | Angka penentu | Yang ditolak |
|---|---|---|---|
| hyd peringatan dini | `hybrid_rule_and_persistence` (rule kanal DAN persistence), ditandai head utama | FP 927, presisi 0,8243, recall 0,6519, FAR 4,10 per 24 jam, lead 8,0 menit, 7 dari 9 fold lolos FAR di bawah 6 dan recall minimal 0,5 | H1 rule DAN statistik (5 dari 9 fold), H1b OR (2 dari 9), CUSUM (2 dari 9) |
| hyd cakupan penuh | `rule_display` | recall 0,7507 dan 307 dari 390 onset | hibrida mengorbankan 31,82 persen true positive |
| shk | single engine ML | memotong alarm palsu 74,67 persen | hibrida menurunkan true positive 76,04 persen |
| tool_wear | logistic default | menang 2 dari 4 alat; GWO degenerate, balanced accuracy 0,5 di 4 dari 4 | metaheuristik GWO |
| vib | single engine ML | presisi median 0,4527, recall 0,6292, AUPRC 0,6204 terhadap prevalensi 0,2542 | hibrida AND (recall jatuh ke 0,0037) |
| ssi | ML untuk pemantauan tren saja | AUPRC 0,0440 hanya 2,8 kali prevalensi, presisi median 0,0237 | hibrida AND (recall 0,0000) |
| stuck onset | tidak layak dipakai | presisi 0,6404, recall 0,001, 13 dari 148 | seluruh varian onset |

### 2. Keputusan tier

Tier tetap `PERINGATAN-BERPENGAWAS`. Tidak ada kenaikan tier, dan slot ALARM-OTOMATIS tetap nol. Alasannya bukan mutu deteksi, melainkan lapisan B: nol kolom biaya dan nol berkas jadwal inspeksi di repo. Kenaikan tier hanya boleh diusulkan bila angka lintas seed mendukung dan tetap butuh persetujuan operator.

### 3. Keputusan bentuk alat: bukan mesin alarm

Alat ini tidak dibangun sebagai mesin alarm. Keluarannya: status kondisi, peringatan berpengawas yang wajib dikonfirmasi manusia, skor tren, beban tinjauan per shift, dan bahan rencana inspeksi. Rujukan metode: skill `ml-system-evaluation` (profil kapabilitas lapisan A/B/C, bukan bit lulus gagal).

### 4. Perubahan engine V9-I1 yang sudah masuk kode

| Perubahan | Bukti |
|---|---|
| `hybrid_rule_and_persistence` ditandai `head_utama=true` dengan badge angka S6 | `code/v9_i1_pipeline.py` blok REGISTRY hyd; `scratch/v9_i1/v9_i1_RESULTS.json` |
| Blok `nilai_maintenance` dari data DDR | 23.447 record aktivitas, 39.397,986 jam tercatat, henti equipment failure 2.739,667 jam, stuck equipment 212,0 jam, circulation loss 195,0 jam |
| Blok `profil_kapabilitas` tujuh engine (A/B/C) | lapisan B berstatus TERUKUR untuk hyd karena membawa lead 8,0 menit |
| Beban tinjauan per shift 8 jam | hyd rule 19, hyd H1p 6, vib 17, stuck 3, shk 3, tool_wear 1, ssi 0 |
| Dasbor diperbarui, kartu slot alarm diganti jam aktivitas | `dashboard/index.html`, diperiksa di peramban: `scrollWidth` 765 sama dengan `clientWidth` 765 |

Hasil run: `rc=0` dalam 21,75 detik tanpa ML dan 27,81 detik dengan `--ml`. Struktur 7 engine, 27 head, L0 5 / L1 11 / L2 9 / L3 2.

Perintah:
```
cd '/mnt/d/Capstone 1(v2)/code'
/home/neonti/.venvs/rnd_e3/bin/python v9_i1_run.py
/home/neonti/.venvs/rnd_e3/bin/python v9_i1_run.py --ml
```

### 5. Sembilan catatan audit gelombang 2: status

| Catatan | Status | Angka bukti |
|---|---|---|
| Baris S4-013 menulis 884 kolom | selesai | sekarang `884 record / 20 kolom` |
| Klaim cakupan ledger S1 | selesai | ditulis 64 dari 441 sel, 14,51 persen |
| Klaim cakupan ledger S3 | selesai | ditulis 74 dari 328 sel, 22,56 persen |
| Gaya angka ribuan bertitik | selesai | 334 sel dinormalkan, sisa 0 |
| Rujukan standar tanpa nomor bagian | selesai | ISO 2041:2018 §3.1.4, sisa `API RP 7G` 0 |
| Tidak ada DOI di empat dokumen | selesai sebagai pernyataan konvensi internal | tidak ada DOI palsu yang ditambahkan |
| Klaim 10 pikiran sequ di S1 | selesai | ditulis 6 yang bertranskrip, 4 dinyatakan tidak tersimpan |
| Keterlacakan tabel ke ledger | diukur dan dinyatakan | S2 369 dari 375 sel, 98,40 persen |
| Rujukan prosa S4 | selesai | 16 baris jadi satu berkas satu kunci, sisa 0 dari 95 |

### 6. Batas yang belum terukur dan tidak boleh diklaim

1. Biaya rupiah tidak ada di repo, jadi penghematan tidak boleh dinyatakan dalam uang.
2. Nomor work order tidak ada, jadi jam henti tidak dapat dipetakan ke satu alarm tertentu.
3. Angka FAR pada blok beban tinjauan adalah FAR segmen F-14, bukan median lintas fold. Median lintas fold H1p ada di `docs/RND_S6_PM_WAVE2.md` §4.1.
4. Empat head Random Forest hanya hidup bila dijalankan dengan `--ml`; tanpa flag itu statusnya `TIDAK DIJALANKAN`.
5. Klaim hyd K-ii (kick/loss) masih `BELUM TERSEDIA DI PROTOTIPE`.

### 7. Peta berkas keputusan

- `docs/RND_S6_PM_WAVE2.md` 40.271 byte: vonis gelombang 2 dan tabel tiga kolom.
- `docs/RND_ENGINE_S6_INTEGRATION.md` 3.915 byte: perubahan engine dan angkanya.
- `docs/RND_S5_DEFECT_STATUS.md` 3.418 byte: status sembilan catatan audit dalam bahasa biasa.
- `docs/RND_PROVENANCE_LEDGER.md`: 9 baris `E5-` untuk angka engine baru.
- `docs/RND_EVALUATION_POLICY.md`: kebijakan tiga lapisan tanpa gerbang biner.
- `scratch/v9_i1/v9_i1_RESULTS.json` 57.555 byte: JSON primer hasil run terakhir.

### 8. Status papan

Board `rnd-algo-2026`: 23 dari 23 kartu done, 0 running, 0 blocked. Gelombang 1 tujuh belas kartu, gelombang 2 enam kartu (S1 sampai S6).



## [Unreleased] — V9-PM2 vonis akhir: SELURUH PIPELINE MEMENUHI "Evaluasi User.txt" → LAYAK (V9)

**Masalah:** kartu `t_07d88981` — vonis akhir apakah seluruh pipeline V9 (11 dokumen: PM1, R1, D1, 3 engine, EVAL_A/B/C, I1, A1) memenuhi kerangka evaluasi operator ("Evaluasi User.txt", 3 lapisan A/B/C + 6 aturan penilaian), TANPA target baru dan tanpa menggeser ambang.

**Verifikasi yang dijalankan PM2 (bukti nyata):**
1. Baca penuh 11/11 `docs/V9_*.md` + `Evaluasi User.txt` + proposal §3.
2. Recompute independen 5 kelompok klaim dari JSON primer (`scratch/v9_e_rule`, `scratch/v9_e_ml`): hyd hybrid ΔB **8/9** (bukan 9/9) dgn FP 2091→927 eksak; ssi hybrid **< rule 6/9, = 3/9, 0 lebih buruk** (FP total 26→7 = 73,1% eksak); stuck RF τ0,5 B1 per fold = 0,0448/0,0357/**0,000**/0,0270 (rentang penuh 0,000–0,0448); vib FAR τ0,5 = 4,15–496,09 → **119,6×**; I1 verify **re-run 13/13 PASS exit 0**.
3. Scan mandiri: 14 kemunculan uppercase LULUS/GAGAL = semuanya negasi/sub-klaim (0 vonis biner); `lift 1,5` semua ditolak eksplisit (0 gate terselubung).

**Temuan & tindakan (3 koreksi penyajian + 1 pelanggaran skill — semua terselesaikan, 0 tier berubah):**
1. EVAL_A B1 stuck_k2 RF τ0,5 "0,027–0,045" membuang fold F-9=0,000 → **dikoreksi** ke "0,000–0,045 (3 fold FAR≤6: 0,027–0,045)".
2. E_RULE "hibrida hyd menang 9/9 fold (Δ +0,017…+0,391)" → **dikoreksi** ke 8/9 (Δ −0,017…+0,092) sesuai JSON; klaim FP-cut 9/9 tetap (terverifikasi).
3. EVAL_C/I1 "hybrid ssi potong FP konsisten 7/7" → **dikoreksi** jadi "≤ rule di 7/7 fold layak (memotong 6/7; F-14 tie)".
4. `V9_D1_DATA_PIPELINE.md` tanpa baris riset WIO/CC/SEQ = **PELANGGARAN prosedural** (1 dari 12 dokumen) → dicatat jujur di D1 + PM2 §a; TIDAK ditambahi retroaktif (akan mengklaim kegiatan tak terbukti).

**VONIS (docs/V9_PM2_VERDICT.md): LAYAK.** Kepatuhan user.txt poin a–e terpenuhi semua dgn bukti per poin: (a) 11 klaim × 3 lapisan, 0 vonis biner; (b) baseline relevan per tugas (R1 §4.1 + E_RULE fold-identik, 0 baseline universal); (c) kemampuan+batas+bukti per engine (A1: 0 klaim berlebihan material); (d) jenis tugas dibedakan (R1 §2: 0 salah-framing; B4 vs B1/TLead; bengkel≠rig); (e) nilai di tingkat alat: tier EVAL_C + I1 = L0 5 / L1 11 (human-in-loop) / L2 9 / L3 2, **slot alarm otomatis 0**. Kepatuhan skill 11/12 (D1 1 pelanggaran); underuse tool = 3 hal minor (delegate_task/todo/browser), tidak memengaruhi hasil. 4 pertanyaan rumusan masalah proposal §3 dijawab. Langkah lanjut = daftar syarat yang sudah ada (kampanye penguatan, pra-reg Fase 0, kalibrasi per-well) — bukan target baru.

**Status:** SELESAI.

---

## [Unreleased] — Restrukturisasi dokumen proposal: 2 file kini fokus solusi advisory; riwayat kegagalan dipindah ke CHANGELOG (V9)

**Masalah:** operator meminta `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` dan `.ipynb` hanya membahas SOLUSI BARU (alat PdM advisory7 mesin + penilaian A/B/C). Kedua file sebelumnya memuat post-mortem panjang kampanye lama (T2-d/e/f, artefak missingness, "lulus bersyarat" dikunci, R1–R8 registry kegagalan, timeline gagal) yang menyulitkan pembaca proposal melihat solusi aktual.

**Tindakan:**
1. **Riwayat kegagalan TIDAK dihapus** — seluruhnya tetap di CHANGELOG ini (entri T2-d/e/f, PM verdict #1/#2/#3, V6-PM, V7-PM, V8-PM) + dokumen kerja primer `docs/V2_*`, `V6_*`, `V7_*`, `V8_*` sebagai arsip bukti. Angka penutup kampanye lama (0/6 varian lolos T2-f, makro 0,1646 vs ambang 0,2465; makro T2-e 0,1762) dipertahankan apa adanya.
2. **Proposal .md ditulis ulang** menjadi dokumen bersih yang fokus: alat PdM advisori7 mesin, penilaian berlapis A/B/C, tingkat pemakaian 1/2/3, roadmap Tahap 1a–3a. Bagian post-mortem (§15.1/15.2/15.3 versi lama, §16.1 missingness detail, registri risiko R1–R8, timeline gagal) diringkas jadi rujukan ke CHANGELOG.
3. **Proposal .ipynb**: markdown cells disamakan dengan versi bersih; 12 code cell + visualisasi (hasil kampanye lama) DIPERTAHANKAN sebagai arsip bukti, diberi konteks "visualisasi arsip".

**Dampak:** pembaca proposal langsung melihat solusi (7 mesin advisory dengan batas jelas); riwayat kegagalan tetap transparan di CHANGELOG & arsip, tidak ada angka yang dihapus atau diubah.

**Status:** SELESAI.

---

## [Unreleased] — V8-PM vonis akhir: peta alat PdM KOHEREN & LAYAK (advisory), 0/7 alarm otomatis (V8)

**Masalah:** kartu PM `t_3b98266a` — menilai apakah 10 dokumen V8 (R1 spec + 7 profil kemampuan + M1 peta + A1 audit) menghasilkan SATU alat PdM yang koheren, dengan penilaian di TINGKAT ALAT (bukan jumlah model lolos gate biner V6/V7).

**Vonis (docs/V8_PM_VERDICT.md):**
- **KOHEREN & LAYAK PAKAI sebagai alat advisory/human-in-loop — BUKAN alarm otomatis.** Hitungan alat: 0/7 layak alarm otomatis · 3/7 peringatan terbukti (shk, stuck, hyd) · 2/7 peringatan bersyarat (vib, ssi) · 2/7 tren-saja (bit_wear, tool_wear) · 7/7 punya peran (0+3+2+2=7 ✓). Fungsi dasar alat (L0 konfirmasi status + L1 peringatan well terkalibrasi + L2 tren + L3 manusia) terpenuhi; gap G1–G8 memblokir ekspansi (alarm/diagnosis/lead panjang), bukan fungsi dasar.
- **Kepatuhan skill: 9/11 tim patuh; 2 pelanggaran** — shk tanpa deklarasi sequ-mcp (grep `sequ`=0), A1 sequ diklaim di metadata kartu tapi tak ada jejak log. Kedua-duanya prosedural, tidak mempengaruhi angka.
- **Konsistensi angka: 6 selisih A1 dikonfirmasi keberadaannya** di dokumen sumber (hyd CI 6/7→5/7; shk persistence 4/9→5/9; shk FAR≤1 "0/9"→1 titik F-14 tau0,30 recall 0,92%; stuck 9,9–185→1.440; tw median 30→24,5 & 47,5→47,0) + M1 mewarisi 2 (baris 54/65, 55/169). Arbitrase: pakai angka hitung ulang A1; **0 selisih membalikkan tier engine**. Patch = langkah eksekusi §h.1.
- **Anti-regresi: 0/7 evaluator kembali ke gate biner** (hanya penafian eksplisit/rujukan konteks V6); 7/7 punya "LAYAK X + BELUM Y"; 7/7 baseline relevan per tugas. **V8 lebih kaya & lebih jujur dari baseline V6 ("2 LULUS + 4 GAGAL" + bit_wear bersyarat yang hilang dari narasi).**
- **Deliberasi council (Empiricist/Architect/Pragmatist/Contrarian/Futurist) + what-if 5 cabang:** vonis tetap koheren di 4/5 cabang; ketegangan inti "layak pakai vs belum ada alarm" = skop eksplisit; blind spot = kalibrasi lokal per well.

**Tindakan:** 7 langkah eksekusi (§h) diserahkan ke operator: patch 6 angka → pasang L1 3 engine di 1 well terkalibrasi → kampanye ukur FAR/B4 (vib/ssi/K-2) → sinkron G7 → uji C3 → kalibrasi-per-well baku → dokumen operasional tanpa klaim alarm. Status: SELESAI.

---

## [Unreleased] — M1 sintesis & keputusan klaim §3.3 (V5): 2 jalur sah, 3 kriteria kerusakan bertingkat, §3.3 TETAP TERTUTUP

**Masalah:** kartu PM `t_299b2c15` — menyintesis hasil J1/J2/J3 + audit independen A1 + riset akar R0 untuk memutuskan apakah klaim §3.3 (prediksi dini berbasis sensor) boleh dibuka, dan apakah tuntutan "minimal 3 kriteria kerusakan" terpenuhi.

**Keputusan (docs/V5_M1_VERDICT.md, berbasis bukti audit, 0 gate digeser):**
- **Jalur sah: J1 (audit LAYAK, recompute 21/21) dan J2 (audit PERLU PERBAIKAN ringan — angka/gate LAYAK, recompute 35/35). J3 = LEMAH, tidak punya sinyal** (skill −0,2913 < gate +0,10; grade LAYAK pada A1 = integritas proses, bukan hasil).
- **"Minimal 3 kriteria kerusakan": TERPENUHI pada pembacaan literal — 6 kriteria bersinyal sah-audit** (5 sintetik: bit_wear AP 0,958 / hard_formation 0,978 / high_friction 1,000 / low_pump 1,000 / low_rpm 1,000, semua dari `V5_J1_RESULTS.json` + 1 nyata bersyarat: stuck-pipe PR-AUC 0,676 vs prev 0,096); **TIDAK TERPENUHI pada pembacaan ketat "3 kriteria dari data lapangan" (bukti: baru 1, bersyarat)** — kedua pembacaan dinyatakan terpisah, tidak digabung, agar klaim ke dosen bukan hoax.
- **Klaim §3.3 TIDAK DIBUKA:** nol jalur memenuhi syarat pencabutannya — J1 sintetik dikecualikan aturan R0 §4.3; J2 bukan prediksi dini (G3 gagal 0,105 < 0,50) dan **canary posisi-kedalaman tidak pernah diuji di data J2** (DEPT dibuang — ketiadaan tes ≠ lolos tes); J3 gagal gate. §3.3 tetap verbatim binding (V2_PM_VERDICT_FINAL §#3.7).
- **Kerangka klaim baru V5-M1 (tier:** terbukti / terbukti bersyarat / belum terbukti / dilarang — §5 dokumen) disusun **tanpa menggeser gate apa pun**; kalimat pembuka sah ada di §5.4.
- **Temuan A1 diterapkan:** F-J2-1 hash `b9ff1b6c…` sudah terkunci sebagai komentar pasca-audit di kartu `t_b8221c0d` (comment_id 5, diverifikasi PM langsung dari DB); F-J2-2 → resmi: verdict J2 = "LAYAK BERSYARAT"; F-J2-3 → tautologi konstrukt dinyatakan eksplisit (§5.2); F-J1-1/2 → 0,989 hanya sebagai kelayakan sintetik; F-J3-1 → anotasi pra-reg "3 dari 1000 jam" salah (realita **11**), koreksi hanya di laporan/CHANGELOG (file pra-reg TIDAK diedit — memutus hash); F-J3-2 → verdict J3 berdasarkan G1, G2 tidak dikutip sebagai signifikan.
- **Koreksi angka primer:** "77 file bhaRun" (entri CHANGELOG lama) **tidak dapat direproduksi** — recount independen A1 = 161 file / 114 ber-timelines / 105 durasi positif / 0 dullGrade.

**Rencana Bab II:** kartu `t_2eb30c93` **TETAP blocked** oleh sesi T5/T6 manusia (gate tidak disentuh); komentar sintesis ditambahkan berisi subbab baru "Pengolahan Data & Analisis V5" + kewajiban memakai kerangka tier M1 + placeholder verbatim tuntutan dosen (jangan ditebak).

---

## [Unreleased] — J2 kampanye stuck-pipe STUCK_RT (V5): G1 lolos, tapi verdict turun ke LAYAK BERSYARAT dalam-well

**Masalah:** jalur J2 (deteksi stuck dari label instrumen) dieksekusi sesuai tugas kanban t_b8221c0d dengan pra-registrasi wajib sebelum hasil.

**Temuan data primer yang meluruskan premis lama:**
- `STUCK_RT` TIDAK ADA di `USROP_labeled.csv` (label di sana = normal/high_MSE_bit_wear/low_ROP_efficiency); label ada di WITSML terparse, hanya 3 wellbore = **2 sumur** (F-9_A 45.712 baris berlabel, F-9 5.728, F-14 5.147; 5 wellbore lain tanpa kolom).
- `bo_tspp/` TSPP1–4 (52.905 baris) **TIDAK berlabel stuck** — dokumen lama "52.905 baris berlabel stuck" (V5_RANCANGAN_SOLUSI §30) keliru; hanya TSPP3 tumpang tindih dengan jendela F-9_A dan nilainya identik (bukan bukti independen).
- Semantik kode 0/1/2/3 tidak terdokumentasi; **nol konfirmasi naratif DDR** pada semua jendela berlabel (pencocokan kata kunci stuck/fishing/free point).

**Hasil kampanye (docs/V5_J2_PREREG.md → V5_J2_STUCK.md/.json, verifier 10/10 PASS di V5_J2_VERIFY.json):**
- G1 pooled E1 lolos: PR-AUC 0,676 vs prev 0,096, CI95% [0,478; 0,821]. G2 cross-well GAGAL (F-9_A→F-14 selisih +0,036 < +0,10; F-9 di bawah prevalensi). G3 deteksi dini GAGAL (recall@FPR≤5% = 0,105 < 0,50).
- Audit struktur label: persistence baseline mengalahkan model di F-9_A (0,876 vs 0,739) dan F-14 (0,350 vs 0,122) — label membentuk blok panjang (maks 2.119 sampel ~1,8 jam) → sinyal = autokorelasi status, bukan gejala fisika baru.

**Verdict J2: LAYAK BERSYARAT sebagai detektor kontemporer dalam-well F-9_A saja; TIDAK LAYAK untuk deteksi dini, generalisasi lintas sumur, atau klaim "deteksi stuck-pipe" fisik.** Rekomendasi: verifikasi semantik kode, target onset per-event, atau gabung J4 physics-residual.

**Deviasi protokol (dicatat di JSON):** DEPT dibuang (0% fill di F-9/F-14); bug pred_store Task B diperbaiki sebelum run final.

---

## [Unreleased] — Jalur T2-f (3 jalur perbaikan) · **REALISASI SELESAI: T2-f GAGAL GATE → LULUS PENUH DITUTUP FINAL (PM verdict #3)**

**Masalah (inti pertanyaan user):** "Kenapa lulus bersyarat terus? Apa gak ada solusi?"

**Diagnosis (dari hasil T2-e, bukan asumsi):** keterampilan prediktif 3 kampanye terakhir (T2, T2-c, T2-d) ternyata **ditopang artefak missingness** — pola "data logging hilang" sebelum kejadian, bukan sinyal sensor:
- missingness-only (TANPA sensor): macro AUPRC 0,3747 — hampir sama dengan kampanye penuh
- T2-e (syarat ketersediaan disimetrisasi, pra-registrasi): **GAGAL GATE** — semua varian makro (0,1211–0,1762) jauh di bawah target **0,2465** (lantai; canary segar 0,1494) *(koreksi PM verdict #2, 2026-10-06: angka lama "0,3806" salah — itu target T2-d, bukan T2-e)*
- 194/661 event berada tepat di zona window-kosong (downtime menjelang kejadian)

**Tindakan (3 jalur, desain dijelaskan ke user 2026-10-06, user setuju "ikuti saranmu"):**

| Jalur | Ide | Kenapa layak dicoba | Risiko jujur |
|---|---|---|---|
| **T2-f (Jalur 2 — dijalankan pertama)** | Geser horizon: fitur dari `act_start−24 jam … act_start−6 jam` (jauh sebelum kejadian, saat data masih mengalir) | Missingness TIDAK bisa jadi sinyal di horizon ini → tes paling bersih; anchor digeser, fitur & infrastruktur T10 dipakai ulang | Sinyal memudar makin jauh dari kejadian |
| Jalur 1 (T2-g, menyusul) | Model sekuens (TCN/CNN1D 1× pra-registrasi) pada raw sequence 4-detik — bukan statistik window | Gejala BHA pra-kegagalan itu transien (spike torsi, stick-slip, shock) yang diratakan oleh statistik window | 467 pos / 7 fold kecil untuk deep learning |
| Jalur 3 (T2-h, paralel kecil) | Unit per-komponen BHA (254 event label `component`) | Label campur = akar fold 5/7 jarang tercapai; per-komponen lebih homogen + klaim lebih spesifik | Sampel per kelas bisa <30 → gugur sendiri |

**Aturan yang TIDAK dilanggar (anti kecurangan):** tidak ada angka gate yang disentuh setelah hasil diketahui; semua desain → pra-registrasi → 1 kampanye → verifier independen → ML Auditor → PM. Canary selalu dihitung segar pada unit/horizon yang sama dengan varian.

**Status: DIRELEASE OLEH PM VERDICT #2 (2026-10-06)** — kartu T2-f `t_66037ed6` (Jalur 2, horizon 6–24 jam) dirilis setelah rantai T2-e → re-audit (LAYAK) → PM verdict #2 selesai; **jalur LULUS PENUH = DIBUKA**. Jalur 1 (T2-g) & Jalur 3 (T2-h) = **SAH BERSYARAT** — dicard setelah rantai T2-f (kampanye → re-audit → verdict #3) selesai; T2-h diawali precheck kelayakan sampel.

**REALISASI (2026-10-06):** T2-f selesai → **GAGAL GATE** (0/6 varian; detail di entri T2-f di bawah) → re-audit **LAYAK** → **PM verdict #3: jalur LULUS PENUH DITUTUP FINAL, LULUS BERSYARAT DIKUNCI FINAL** → Jalur 1 & Jalur 3 **TIDAK dicard** (lihat entri verdict #3).

---

## 2026-10-11 · V7-PM verdict → **VONIS: LEBIH BAIK (jalur metode-sah ke 5 kelas) + kerangka eksekusi tanpa geser gate**

**Masalah:** kartu PM `t_dd0f1591` (board capstone-v7-solve) harus membandingkan solusi V7 dengan kondisi V6 (2 LULUS + 1 bersyarat + 4 GAGAL), dinilai dengan prinsip operator: **validitas METODE, bukan angka akurasi** (analogi detektor diabetes 80%).

**Hasil (`docs/V7_PM_VERDICT.md`):**
- **VONIS: LEBIH BAIK** — jalur metode-sah ke 5 kelas: `vib`+`ssi` (LULUS, diperkuat 3 wellbore baru terverifikasi 3 pihak) + `shk` (S-B1: F-10 798 + F-12 580 positif nyata; G2 sudah 6/7) + `bit_wear` (S-F1 onset: 481/329 kandidat onset jujur; G1 3/4) + `stuck` (S-A1+S-A2, SEDANG — risiko daya: onset strict F-9_A hanya 34). Lantai skenario terburuk 4 > baseline 2. `hyd`/`tool_wear` = upside dengan tes pembeda.
- **Kepatuhan:** 12/12 output punya baris "Riset pendahuluan" + skill sci; sequ-mcp hanya 3 dokumen menyatakan sukses, 2 wrapper bug dilaporkan, 7 tidak dinyatakan, A1 DILEWATI (pelanggaran proses; M2 buktikan sequ-mcp jalan hari sama). Underuse: session_search & agentmemory tidak dipakai tim manapun; scan GAINLOSSTOT F-1 C timeout tidak dilanjutkan chunking.
- **Konsistensi angka:** labels_curated 884 EKSAK (PM reproduce); M2 "582/884 in-range" → jujur 523; "1.489 onset" → 481/329; "78.212" → 64.915; onset stuck M2 "50/74" → PM buktikan tidak reproduce definisi mana pun (strict 34 EKSAK vs A1, ffill 74; F-14 strict 0/ffill 87 sporadis) → **definisi onset wajib dikunci pra-reg (Fase 0)**; prev F-9_A 66,9% vs 49,4% tetap terbuka.
- **Dokumen fiktif: NOL** (8/9 sitasi dibuka A1, 0 URL palsu; 4 klaim kunci dihitung ulang PM ke file primer). **Anti-geser-gate: LULUS** (G1/G2/UNDERPOWERED/persistence/LOWO identik V6; onset = koreksi estimand + pra-reg baru, bukan turun ambang).
- **Kerangka eksekusi:** Fase 0 kunci definisi onset+daya+hash semua pra-reg sekaligus (anti shopping) → Fase 1 S-F1+S-A1 relabel nol parse → Fase 2 parse F-10/F-12/F-4/F-15 chunked (~825 file) → Fase 3 upside S-C1/S-D1. Stop/go rules mengikat; P(≥5 kelas) ≈ 60–70%.

**Tindakan:** eksekusi Fase 0–2 adalah keputusan operator (vonis diserahkan dengan kerangka, tanpa menggeser gate apa pun).

---

## 2026-10-11 · V6-PM sintesis akhir → **VONIS: SAH (literal pra-reg, batasan mengikat) — 3 kriteria dari data nyata berdasar, lolos 2 audit**

**Masalah:** kartu PM `t_17b983dc` harus memutuskan tegas SAH/TIDAK SAH klaim ">3 kriteria kerusakan dari data nyata" setelah A1+A2 selesai, plus cek kepatuhan skill/tool 15 tim, konsistensi angka, dan dokumen fiktif.

**Hasil (`docs/V6_PM_VERDICT.md`):**
- **VONIS: SAH** pada pembacaan literal pra-reg (3 kelas lolos G1+G2; taksonomi 7 kelas terverifikasi A2 24/24), **TIDAK** pada pembacaan ketat (final LULUS = 2) — kedua bacaan ditulis serbesar; tanpa geser gate; lanjutan = restu dosen via T5/T6 (konsisten PM verdict #3).
- **Kepatuhan skill:** E1, A1, A2 = penuh (baris + skill wajib + sequ-mcp terkonfirmasi 2 tim via metadata); D0, D2, R1 = patuh; **7 pembaca D1a–e,g,h TIDAK menulis baris "Riset pendahuluan"** (kartu mereka tak mewajibkan, tapi standar KM wajib) → 3 kartu anak dibuat untuk "minta ulang" + patch.
- **Konsistensi angka:** 12 kelompok angka kunci dicek; 8 kontradiksi RESOLVED dengan nilai otoritatif (triple USROP D0 → 134.013/49.732/15.183, spot-check PM parse CSV; D1h 16.670/151; D1c azi 2.920; EDM 947/3.539/130 dikarantina; XAI 15 kolom). Input klaim sendiri bersih: rerun A2 identik + provenansi E1d 3.953/3.953 + sha256 4/4.
- **Dokumen fiktif `V6_D1_VOLVE_INVENTORY.md`: 0 rujukan** di `docs/`, `code/`, `CHANGELOG.md` (grep PM).
- Spot-check mandiri PM: 192 file tubular (witsml_raw; jebakan find ganda = 384 dengan arsip `external/dbx_volume`) + distribusi label USROP cocok A1.

**Status: SELESAI** — patch angka + baris kepatuhan pembaca = 3 kartu anak gated: `t_7a7a6477` (D1a-h fix), `t_01a5780a` (D0 fix), `t_38cacf08` (D2 fix), parents `t_17b983dc`; angka §5.4 dokumen verdict DILARANG dikutip ke dosen sebelum patch.

---

## 2026-10-10 · V6-D2 dataset eksternal ber-label kegagalan → **SELESAI: 5 kandidat terunduh+terbuka, 3 kriteria terpenuhi gabungan, dysfunctions & NPT tetap KOSONG**

**Masalah:** kartu Data Scout `t_5c834a19` harus mencari dataset pengeboran/maintenance di luar Volve yang BER-LABEL kegagalan dan benar-benar bisa diakses, dengan bukti minimal 5 query / 3 sumber sebelum menyatakan "tidak ada".

**Tindakan:** 18 query/endpoint di 7 sumber (Tavily-9router, Figshare POST, Zenodo, Kaggle, HuggingFace, GitHub trees, Mendeley) → tiap kandidat diunduh lalu dibuka (bukan percaya README); ledger sitasi `sources.py` (18 sumber) + `verify` exit 0.

**Hasil (`docs/V6_D2_EXTERNAL_DATASETS.md`):**
- **Terkunci 3 kriteria lewat gabungan:** stuck pipe = GitHub `HaythamElmousalami/Drilling-Stuck-Pipe-Prediction` (xlsx 103×8, `stuck case` 77/26 + varian multiclass; minyak, tapi **tanpa LICENSE**); tool/bit wear = Mendeley `th4yv974r2` (CC BY 4.0, 8 xlsx 22,5 MB, sampel 60.505×4); multi-mode failure = Kaggle `xai-drilling-dataset` (CC BY-NC-SA 4.0, 20.000×14, `Main Failure` + BEF/CCF/FWF/WDF — **sintetis**, TransAI 2023).
- Pendukung: HF `nikhilr2907/Drilling-Dataset` (307 contoh, normal 220/abnormal 87 + grid spasial; **tanpa lisensi**), HF `jonasmaltebecker/synthetic_drilling_dataset` (39.133 baris, target `k_wear`; **lisensi null**).
- **Negatif terverifikasi (jangan dikutip sebagai ber-label):** `promiseeee` TSPP dibuka → kolom label NUL (21.121 & 5.634 baris × 11 sensor) — konsisten dengan temuan lama CHANGELOG baris "TSPP1–4 TIDAK berlabel stuck"; Utah FORGE Kaggle 503.905×14 tanpa label; `atashnezhad/bit-wear` cuma 9 baris tanpa label; `drilling-log-dataset` 151 baris tanpa label; `m-bizhani` well1 7.999×21 tanpa label; repo kick Aramco `Hadi-mac` **nol berkas data**; Frontiers 2026 (297 obs) → "not publicly available … Dolph and Dode Offshore Services India".
- **KOSONG setelah 18 query:** dataset eksternal publik ber-label **drilling dysfunctions** (Zenodo `q="drilling dysfunction"` total 0; Kaggle `stick slip`/`stuck pipe` = 0 hasil) dan **NPT/fishing** (Kaggle `NPT drilling` = 0; semua Zenodo `stuck pipe` type=dataset = PDF). Mendeley search API 404 (retrieval by ID tetap jalan); UCI ML repo balas HTML shell, bukan JSON.

**Status: SELESAI, semua angka dari pembukaan berkas nyata** (cache `/home/neonti/.hermes/cache/scratch/v6d2/`); belum dicek: sha256 vs API Mendeley, asal augmentasi `stuck case`, definisi kolom `P1…P7` (lihat §5 dokumen).

---

## 2026-10-10 · Papan V6 dibuat: multi-tim pecah keputusan lulus bersyarat (data NYATA, bukan sintetis)

**Masalah:** putaran "solusi → tidak bisa" berulang. Papan V5 memakai data sintetis (J1 LAYAK) tetapi ditutup karena hanya memenuhi ">3 kriteria" pada pembacaan literal, bukan data lapangan. Operator memerintahkan papan baru dengan 6 tim, wajib memakai data NYATA, dan wajib memenuhi ">3 kriteria kerusakan".

**Papan:** `capstone-v6-solve` (7 kartu, dependensi terpasang, skill terpasang di semua kartu).

| ID | Tim | Tugas | Skill terpasang | Menunggu |
|---|---|---|---|---|
| t_022ae5a8 | Data Eng | Buka & petakan SELURUH volume Volve: LAS 253 file, DLIS, time.csv 428MB, mudLog 8 file, 161 bhaRun (baru 77 dibaca) | exploratory-data-analysis, polars, uncertainty-and-units | langsung |
| t_5c834a19 | Data Scout | Cari dataset eksternal open-source ber-label kegagalan (tim KRUSIAL — "anda tidak bisa akses != datanya tidak ada") | web-search-resilience, database-lookup, grounded-citations | langsung |
| t_32e0ff8b | R&D | Riset ilmiah: rumus turunan label dari paper + uji nyata di Volve | literature-review, paper-lookup, scientific-critical-thinking | langsung |
| t_5e052df1 | ML Eng | Rancang + baseline ML ≥3 kriteria dari data NYATA (bukan sintetis) | scikit-learn, experimental-design, statistical-analysis | D1, D2, R1 |
| t_9e5e4f81 | Auditor 1 | Audit klaim tim DATA (D1+D2): berdasar atau karangan? | scientific-critical-thinking, verification-mandatory, peer-review | D1, D2 |
| t_412436b2 | Auditor 2 | Audit klaim ML & ILMIAH (E1+R1): berdasar atau karangan? | scientific-critical-thinking, verification-mandatory, statistical-analysis | E1, R1 |
| t_17b983dc | PM | Sintesis akhir: cek kepatuhan skill/tim + vonnis tegas SAH/TIDAK SAH | what-if-oracle, scientific-critical-thinking | A1, A2 |

**Anti-buntu yang ditanam di tiap kartu:** (a) DILARANG berkata "data X ada tapi belum saya buka" tanpa kemudian membukanya; (b) minimal 5 query/5 sumber sebelum menyatakan "tidak ada"; (c) auditor harus MEMBONGKAR klaim lemah, bukan memberi stempel; (d) PM harus memberi vonnis tegas SAH/TIDAK SAH, bukan "mungkin"; (e) semua klaim wajib disertai output tool nyata.

---

## 2026-10-10 · Tiga opsi ML maintenance disimpan (tersimpan, belum dieksekusi)

**Masalah:** operator meminta ketiga rekomendasi ML dari audit 115 kolom disimpan dengan presisi agar dapat dipanggil kembali saat disebut lagi, tanpa memilih jalur mana pun untuk dieksekusi.

**Tindakan:** audit fill-rate lintas 7 sumur pada kolom maintenance dijalankan ulang dan hasilnya didokumentasikan; dokumen `docs/V4_MAINTENANCE_ML_OPTIONS.md` ditulis dengan angka nyata, bukan ringkasan.

**Angka kunci (dari eksekusi langsung, bukan kutipan):**
- 12 dari 115 kolom USROP yang selama ini dipakai; 103 kolom sisanya tidak tersentuh.
- `STUCK_RT` (label instrumen rig, bukan naratif) ada di F-9A (510 baris berlabel: 457 kode 3, 49 kode 1, 4 kode 2) dan F-14 (118 baris: 114 kode 1, 4 kode 2).
- `MWD Shock Risk`/`Shock Peak`/`Turbine RPM` hadir di semua 7 sumur (5,7 hingga 14,1%).
- `Total Bit Revolutions` kuat hanya di F-9A (33,6%) dan F-7 (30,7%).
- TSPP: 4 file utama 52.905 baris (TSPP1 21.120, TSPP2 8.499, TSPP3 12.533, TSPP4 10.753), total folder 117.701 baris termasuk varian.
- `bhaRun`: 77 file di disk berisi interval `dTimStart`/`dTimStop`; tag `dullingInfo`/`dullGrade` TIDAK ada, sehingga label = kapan bit ditarik, bukan tingkat keausan.
- Artefak `V2_TSPP_AE_SCORES.csv` tidak diskriminatif (75 hingga 99% baris terdeteksi) dan tidak terdokumentasi; dinyatakan tidak boleh dikutip.

**Tiga opsi yang disimpan:** (1) pencegahan stuck-pipe via `STUCK_RT` + TSPP; (2) deteksi dysfungsi drill-string (stick-slip/shock) via kolom MWD; (3) RUL bit via `Total Bit Revolutions` + interval `bhaRun`. Kandidat dibuang: kick detection dari gas (fill 2,4 hingga 3,2%), kegagalan MWD (event terlalu sedikit), seismic, LAS.

**Status: TERSIMPAN, belum dieksekusi.** Menunggu pilihan operator. Bila dieksekusi wajib pra-registrasi baru (bukan keluarga kampanye T2 yang ditutup verdict #3).

---

## 2026-10-06 · Dokumen proposal ditulis ulang formal + sitasi + versi `.ipynb` berisi 12 visualisasi

**Masalah yang diperbaiki:** (a) draft dokumen proposal dicaci user sebagai "jelek, gak formal, tulisan gelandangan"; (b) 52 em-dash dipakai sebagai penghubung klausa tanpa hubungan logis (koreksi: tentukan hubungan dulu, baru pilih tanda baca/konjungsi); (c) narasi audit menyuruh pembaca "baca dokumen X" tanpa menguraikan hasil & sebab hasil; (d) status dokumen masih "kampanye berjalan" padahal T2-f + verdict #3 sudah keluar.

**Tindakan:**
- `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` ditulis ulang formal (431 baris → kini 46.774 bytes): kontrol dokumen CAP-1/PPDT/2026/01, petunjuk pembacaan per lapis, BAB A/B/C, blok pengesahan, Lampiran A internal, registri risiko R1-R8.
- Em-dash: 52 → **0** (semua diganti alat yang menandai hubungan logisnya: konjungsi kausalitas/kontras, koma+seperti untuk contoh, titik dua judul, kurung aposisi). Lesson disimpan di agentmemory.
- Rujukan "Lampiran A-x" mengambang → **sitasi `[A-x]`** gaya pustaka + §19.3 sebagai daftar sitasi (kode → isi → berkas).
- Audit kini **diuraikan**: §15.2 menyebut 4 temuan audit T2-e (192 unit bukan "semua unit"; 6.617 bukan 6.618; 67.731.473 baris = counter kontrol, counter event 4.274.005 dipisah; prediksi paralel beda bit terakhir) + penyebabnya (pencampuran cakupan counter, definisi unit longgar) + tindak lanjutnya (koreksi → audit ulang → LAYAK); §16.2 menguraikan audit 100 kasus uncertain (49 tetap / 50 usulan no / 1 usulan yes; 50 di luar jangkauan, 30 ambigu, 20 tipis).
- Status diperbarui ke **verdict #3**: T2-f 0/6 lolos (makro terbaik 0,1646 vs lantai 0,2465), lulus penuh ditutup final, lulus bersyarat dikunci final; Tahap 0 dinyatakan selesai; lini masa diganti baris T2-f/audit/verdict.

**File baru:** `docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.ipynb` (70 sel = 58 markdown isi MD + 12 sel kode visualisasi; builder: `scratch/build_proposal_nb.py`).

**Visualisasi (semua dari berkas primer, diverifikasi visual per figur):** VIS1 distribusi label (884/wellbore, 50/263/571 relevansi BHA); VIS2 heatmap kelengkapan 7 sumur x 16 kanal + unit jendela kosong 194/191/185 vs 1; VIS3a histogram 6 kanal per kelas (small multiples, rentang 1-99%) + VIS3b korelasi (940 baris bersih, NaN dibuang); VIS4 confusion matrix/ROC/PR/kalibrasi (LOWO demo, AP 0,3929); VIS5 learning + validation curve (gap latih 1,0 vs validasi ~0,4 = overfitting terdeteksi); VIS6 perbandingan 3 kampanye vs ambang (angka cocok JSON); VIS7 heatmap delta per lipatan; VIS8 rantai bukti missingness (0,9419 vs 0,3726; missingness-only 0,3747/0,3980/0,1005); VIS9 importance resmi + permutation; VIS10 SHAP beeswarm; VIS11 prediksi vs aktual.

**Masalah saat pembuatan (otomatis diperbaiki):** fill-rate JSON `null` → TypeError (ditahan jadi NaN); sampel 700 > populasi 661 (dipangkas 600); `calibration_curve` pindah modul sklearn 1.9 (`sklearn.calibration`); `validation_curve` tak menerima `random_state`; korelasi seluruhnya NaN (baris NaN dibuang dulu); SHAP API baru mengembalikan (n,fitur,2) (disayat ke kelas positif). Eksekusi final: **0 error, 12 PNG, semua figur diperiksa visual**.

---

## 2026-10-06 · T2-f (Jalur 2 — horizon 6–24 jam missingness-proof) → **GAGAL GATE**

**Masalah yang diperbaiki/diuji:** T2-e bersih dari missingness TAPI horizonnya masih zona 0–2 jam menjelang kejadian (zona downtime) → belum pernah ada tes di mana missingness **secara struktural mustahil** menjadi penanda kelas. Jalur 2 menggeser anchor ke `act_start−6 jam` (fitur dari −24h…−6h, rig masih logging).

**Tindakan (rantai wajib dipenuhi):** pra-registrasi komentar kartu 09:40:50 (sebelum part A 09:50:51 & run 10:01:17) → 1 kampanye `code/64` → verifier independen `code/65` → re-audit ML Auditor `t_a11bc7f5` → PM verdict #3.

**Hasil (eksekusi nyata, `docs/V2_ML_BEAT_CANARY_HORIZON.md/.json`):**
- Unit simetris: **471 pos / 3.958 neg / 4.429** (prev 0,1063; 190/661 event gugur syarat ketersediaan); `n_unit_kampanye_kosong = 0` (guard STOP); anti-leakage **0/4.208.121** + **0/43.000.442**
- canary `log_G` = **0,1573** < lantai → **target tetap 0,2465**
- **VERDICT T2-f: GAGAL GATE** — makro terbaik `hgb_F = 0,1646` (menang 5/7 fold); **0/6 varian lolos**; `ada_yang_lolos=false` (recompute PM 9/9 makro + 6/6 gate identik JSON)
- **missingness-only = 0,1005 ≈ prevalensi** (flag seragam 0) → bukti tesnya sah: gagal murni karena sinyal sensor, bukan artefak
- MD-only `hgb_G 0,1607` vs sensor terbaik `hgb_F 0,1646` → sensor **+0,0039** saja di atas kedalaman (pola T2b terulang)
- Re-audit `t_a11bc7f5` = **LAYAK** (bukti 195 PASS / 0 FAIL; verifier `code/65` diulang 32/32) → **kegagalan = hasil, bukan cacat metode**

**Dampak:** menutup pertanyaan "kenapa lulus bersyarat terus" dengan bukti terkuat yang bisa diminta: dua horizon berjauhan (0–2h dan 6–24h) keduanya di bawah lantai pada desain bersih → PM verdict #3 = penutupan final (lihat bawah).

---

## 2026-10-06 · PM verdict #3 → **LULUS PENUH DITUTUP FINAL + LULUS BERSYARAT DIKUNCI FINAL**

**Masalah:** rantai T2-f selesai (kampanye GAGAL GATE → re-audit LAYAK) → perlu keputusan akhir sesuai komitmen verdict #2 §2.5: "T2-f GAGAL → penolakan final bertulis seluruh kampanye + alasan struktural".

**Pemeriksaan PM sendiri (bukan kutipan):** `pm_v3_recompute.py` (recompute makro 9 kunci + gate 6 varian + canary/target + T3 dari JSON primer) → **9/9 + 6/6 cocok**; `code/65_verify_horizon.py` dijalankan ulang PM → **32/32 PASS exit 0**; arsip run-1 + bukti audit dicek eksistensi.

**Keputusan (`docs/V2_PM_VERDICT_FINAL.md` bagian VERDICT #3, §#3.0–#3.8):**
- **JALUR LULUS PENUH DITUTUP FINAL** — langkah 4 syarat §9 gagal dua kali pada desain bersih (T2-e 0,1762; T2-f 0,1646; keduanya < lantai 0,2465) → kriteria §3.3 tidak terpenuhi. **LULUS BERSYARAT DIKUNCI FINAL** (bukan diturunkan; syarat §8.2 utuh).
- **Penolakan final bertulis** seluruh kampanye T2, T2-c, T2-d (lolos mekanis tapi tidak sah), T2-e, T2-f + 3 akar struktural: (1) label deterministik `(wellbore, md)` → shortcut kedalaman; (2) transfer LOWO lemah; (3) artefak missingness — kini terbukti dihilangkan DAN tetap gagal → sinyalnya memang tidak ada.
- **Keputusan jalur:** jalur horizon lain = TUTUP; **Jalur 1 (T2-g TCN/CNN1D) = TUTUP** (R8 tolak iterasi kelas-model; akar #1 tak berubah oleh representasi fitur; catatan jujur: hipotesis "transien diratakan window" belum teruji empiris = keputusan nilai-harapan); **Jalur 3 (T2-h per-komponen) = TUTUP** (tak mengubah akar #1/#2; 254 event/7 fold risiko <30/kelas); **stop eksperimen ML untuk klaim §3.3 = YA**. Pembukaan kembali hanya perintah operator baru.
- **§3.3 tetap berlaku verbatim, binding.** LAYAK DIKUTIP: `V2_ML_BEAT_CANARY_HORIZON.md/.json` sebagai hasil GAGAL GATE dengan framing §3.3.

**Status: VERDICT #3 (FINAL) SELESAI** — `docs/V2_PM_VERDICT_FINAL.md` (§#3.0–#3.8) · CHANGELOG terupdate · rantai T2-f tertutup penuh (kampanye → audit LAYAK → verdict).

---

## 2026-10-06 · PM verdict #2 → **LULUS BERSYARAT DIPERTAHANKAN + jalur LULUS PENUH DIBUKA (T2-f)**

**Masalah:** re-audit T2-e = **LAYAK** (syarat audit terpenuhi, langkah 1–3 syarat upgrade §9 verdict #1 beres) **tapi** T2-e = **GAGAL GATE** (langkah 4 gagal) → perlu keputusan PM: buka atau tutup jalur LULUS PENUH.

**Pemeriksaan PM sendiri (bukan kutipan):** `pm_v2_recompute.py` (baca blok gate JSON primer) + `pm_v2_gate_check.py` (recompute makro 6 varian + fold wins + formula target + S1 + T3 dari `folds`/`pooled`) → **6/6 cocok**, `ada_yang_lolos=false`; re-audit `t_a112dc2b` dibaca langsung (3 komentar, verdict LAYAK).

**Keputusan (`docs/V2_PM_VERDICT_FINAL.md` bagian VERDICT #2):**
- **Tidak naik LULUS PENUH:** syarat naik = re-audit LAYAK **+** kriteria §3.3 → yang kedua gagal (makro terbaik 0,1762 < lantai 0,2465; S1 juga 0 lolos; T2b sensor-tidak-tambah tetap berlaku). §3.3 tetap berlaku verbatim.
- **Jalur DIBUKA (bukan ditutup):** tes missingness-proof belum pernah dijalankan — T2-e bersih dari unit kosong TAPI horizon-nya masih zona 2 jam menjelang kejadian (194/661 event di window-kosong); Jalur 2 (horizon −24h…−6h, rig masih logging) adalah tes penentu pertama. Kartu `t_66037ed6` (prabuat user, desain persis di dalamnya) **dirilis**.
- **Jalur sah:** T2-f sekarang; T2-g (Jalur 1) & T2-h (Jalur 3) = sah-bersyarat, dicard setelah rantai T2-f (kampanye → re-audit → verdict #3); T2-h diawali precheck sampel.
- **Komitmen anti-tunda:** T2-f GAGAL → PM menyiapkan penolakan final bertulis seluruh kampanye (T2, T2-c, T2-d, T2-e, T2-f) + alasan struktural; LOLOS → evaluasi naik LULUS PENUH.
- **Koreksi angka CHANGELOG:** 2 entri salah menulis target T2-e = 0,3806 (angka itu target T2-d) → dikoreksi jadi **0,2465** (lihat [Unreleased] & entri T2-e di bawah).

**Status: VERDICT #2 SELESAI** — `docs/V2_PM_VERDICT_FINAL.md` (§#2.0–#2.8) · kartu T2-f terlepas dari dependency.

---

## 2026-10-06 · T2-e: koreksi angka + tes anti-missingness → **GAGAL GATE**

**Masalah yang diperbaiki:** re-audit T2-d (`t_bdf55b10`) = **PERLU PERBAIKAN** — 4 ketidakcocokan angka (P1 window kosong 185 vs 191; P2 subset 6618 vs 6617; P3 rows_scanned; P7 determinisme rerun beda 2 sel F1) + temuan substantif **P4 (missingness artifact)**.

**Tindakan:** PM membuat `t_471b790f` (T2-e): perbaikan P1–P3+P7 + **desain evaluasi anti-missingness PRA-REGISTRASI** (keputusan ditulis di komentar kartu SEBELUM hasil dilihat: syarat ketersediaan disimetriskan — window kosong dilarang sama untuk pos & negatif, berlaku saat latih+evaluasi).

**Hasil (eksekusi nyata, `docs/V2_ML_BEAT_CANARY_TS.md`):**
- Koreksi P1–P3: 192 unit, n_eval 6617, rows 67.731.473 / 4.274.005; P7 `V2_P7_DETERMINISME.json` ✓
- Positif lolos ketersediaan: **467/661**; unit total 4.425 (prev 0,1055)
- **VERDICT T2-e: GAGAL GATE** — makro terbaik `hgb_F=0,1762` (menang 6/7 fold) vs target **0,2465**; fold tertinggi contoh `rf_F F-14=0,3113` *(koreksi PM verdict #2: target T2-e = 0,2465, bukan 0,3806 = target T2-d; `ada_yang_lolos=false` dari JSON primer + recompute PM)*
- **VERDICT S1: tidak ada varian lolos set longgar** → simpulan gate memang bergantung pada syarat ketersediaan

**Dampak:** memperkuat diagnosis P4 — sinyalnya missingness, bukan sensor. → melahirkan 3 jalur T2-f (lihat atas).

---

## 2026-10-06 · PM verdict #1 → **LULUS BERSYARAT DIPERTAHANKAN**

**Masalah:** T2-d lolos gate mekanis (4 varian: rf_E 0,4217/6-7, hgb_E 0,4537/6-7, rf_F 0,4451/5-7, hgb_F 0,4613/5-7; target 0,3806; canary log_G 0,3606) **tapi** audit = PERLU PERBAIKAN → syarat upgrade "audit LAYAK" gagal.

**Tindakan:** PM `t_742e6dd2` menulis `docs/V2_PM_VERDICT_FINAL.md` (semua angka dijudgement dari JSON/MD primer, direcompute sendiri). Verdict: pertahankan LULUS BERSYARAT; framing §3.3 belum terpenuhi.

**Inilah yang dimaksud user "lulus bersyarat terus"** — akar masalahnya sekarang terpetakan: (a) 3 kampanye mentok di temuan yang sama (missingness), (b) audit selalu menemukan selisih angka. Keduanya ditangani: (a) → 3 jalur T2-f; (b) → determinisme P7 + verifier 9/9 PASS.

---

## 2026-10-05/06 · T2-d: kampanye time-based 7 sumur → **LOLOS MEKANIS, audit PERLU PERBAIKAN**

**Masalah sebelumnya:** T2 (0,1316) & T2-c (Δ10 0,1217–0,1392 vs gate 0,2465) GAGAL — fitur kedalaman/sensor per-baris tidak cukup; hanya 1 sumur time-based (`F-9 A time.csv`) → 7 fold LOWO tidak mungkin sah.

**Tindakan:**
1. Unduh volume Databricks ws#2 → **17.368 file, 3,32 GB** (audit: 0 hilang, 0 ukuran salah)
2. Ekstrak zip Realtime 2,88 GB → `witsml_raw/` 20.086 file gagal=0
3. Parse → **8 CSV, 7.080.457 baris** (T9); fitur → **661 event × 480 fitur, anti-leakage 0/4.274.005** (T10)
4. Kampanye T2-d: unit event (7.279; 661 pos), canary time-based dihitung segar 0,3606 (canary lama 0,2265 TIDAK dipakai — unit/resolusi beda, tidak sebanding)

**Hasil:** LOLOS mekanis (4 varian) — **tapi** S1 sudah memperingatkan: 0 varian lolos tanpa positif window-kosong. Auditor `t_bdf55b10` recompute sendiri: verifier 9/9 PASS, fold-AP 63/63 cocok, leakage 0 — tapi tetap **PERLU PERBAIKAN** karena P1–P4.

---

## 2026-10-05 · Insiden teknis & proses (semua DIPERBAIKI, bukan dibiarkan)

| # | Masalah | Penyebab | Tindakan perbaikan | Status |
|---|---|---|---|---|
| 1 | 6 file `message/114…1352.xml` (F-1 C) gagal unduh | DNS `Temporary failure in name resolution` | Sweeper `dbx_sweep.py` loop inventory → unduh ulang | ✅ gagal=0 |
| 2 | "Gagal terus, nunggu status" (user marah) | Proses gagal → agent hanya lapor, tidak auto-fix | Auto-fix loop `dbx_autofix.sh` (maks 8 putaran) + **rule permanen** `mem_muv4v0p1`: gagal → perbaiki → verify → lanjut | ✅ aturan tersimpan |
| 3 | Sweeper serial lambat (18 file/menit) | 1 thread, 90 menit sisa | Di-patch jadi 6 worker paralel → 133/menit | ✅ |
| 4 | WSL `Input/output error` `/mnt/d` | transport 9p/DrvFS hang (I/O burst) | Verifikasi ulang — pulih sendiri; data tidak rusak | ✅ |
| 5 | T9 worker crash 5× (protocol violation) | Worker keluar tanpa `kanban_complete`; `_verify.json`/`_coverage.json`/laporan belum dibuat | Agent generate 3 JSON + laporan `V3_WITSML_PARSE_REPORT.md` sendiri, `complete --summary` | ✅ |
| 6 | T10 crash 2× | `504 Upstream idle timeout` (9router rusak — diperbaiki user) | `unblock` + `dispatch`; sesudah 9router beres → jalan | ✅ |
| 7 | Pemetaan wellbore→label salah (F-15_S 0 match; F-15A/F-9 bocor lintas sumur) | filter `contains()` | Ditemukan di audit T9 → dilaporkan di laporan; **diperbaikan di T10** (213 label F-15 D/C/B di-exclude jujur karena tak punya WITSML) | ✅ |

---

## 2026-10-04/05 · Akuisisi data (selesai)

- Blokir "butuh akun manusia" (§2.1 inventory lama) → **terpecahkan** via Databricks workspace #2 (PAT milik user; ws#1 ternyata kosong) → `docs/V3_DATA_ACQUISITION_INVENTORY.md` §6.
- **Catatan keamanan:** PAT user pernah diminta di-rotate (User Settings → Developer → Revoke); token tidak direproduksi di dokumen.

## Konvensi

- Semua plan/status ada di MD berstatus jelas ("belum terealisasi" / "SELESAI").
- Angka = output eksekusi; kalau gagal → dicatat apa adanya, termasuk verdict GAGAL.
- Dokumen lama diberi banner `⚠️ UPDATE STATUS` supaya tidak miskom, bukan dihapus (arsip = bukti).
