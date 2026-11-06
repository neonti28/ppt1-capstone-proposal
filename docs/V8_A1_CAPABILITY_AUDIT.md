# V8-A1 — AUDIT KEMAMPUAN: angka evaluator nyata atau karangan?

**Auditor:** [Auditor] V8-A1 (t_263e7df0, run 3) · **Tanggal:** 2026-10-12
**Yang diaudit:** 7 dokumen `docs/V8_E_*_CAPABILITY.md` + `docs/V8_M1_CAPABILITY_MAP.md`
**Kerangka:** standar 3-lapisan A/B/C (V8-R1) — penilaian KEMAMPUAN + BATAS + KEKUATAN BUKTI, bukan LULUS/GAGAL.
**Metode:** HITUNG ULANG independen dari artefak primer (JSON hasil eksekusi nyata evaluator di `scratch/v8_e_shk/`, `scratch/v8_e/`, `scratch/v8_e_hyd/`, `scratch/v6_e1/`, workspace evaluator stuck), dibandingkan klaim per klaim; pemeriksaan kualitatif anti-overclaim, anti-gate-biner, baseline relevan, konsistensi antar-dokumen, batas jujur.

**Riset pendahuluan: `scientific-critical-thinking` — klaim absolut ("TIDAK tercapai di fold mana pun", "F-9 satu-satunya") wajib diuji pencarian pengecualian di artefak; 3 pengecualian nyata ditemukan dengan cara ini.**
**Riset pendahuluan: `verification-mandatory` — setiap angka dokumen dicek terhadap JSON primer; 7 dari 14 selisih awal ternyata kesalahan SKRIP AUDIT (kunci JSON salah), bukan dokumen — wajib diskriminasi sebelum menuduh.**
**Riset pendahuluan: `statistical-analysis` — median hitung ulang dari nilai per-baris (bukan dari rentang); CI95 tumpang-tindih diuji dengan interval aktual, bukan kutipan; FAR dibaca pada skala aslinya (per 24 jam-negatif vs per menit).**
**Riset pendahuluan: `peer-review` — temuan dilaporkan dua arah: kekeliruan yang MENGUNTUNGKAN evaluator (understate) dan yang MERUGIKAN (overclaim) keduanya dicatat; tidak ada temuan yang disembunyikan.**

---

## 1. Ringkasan hasil

| Item | Jumlah |
|---|---|
| Klaim numerik unik dihitung ulang dari artefak primer | **121** (log: `recompute.log`–`recompute5.log`, workspace t_263e7df0) |
| Sel tabel per-well shk (9 well × 5 kolom: B1, T_lead, B1-persistence, FP_engine, FP_display) | **45 sel — semua cocok** |
| Total angka dihitung ulang | **≥166** (syarat penerimaan: 8) |
| **Terverifikasi cocok** | **114 klaim** (7 di antaranya lolos setelah diskriminasi — kesalahan skrip audit, bukan dokumen) |
| **Selisih nyata** | **6 klaim** (rincian §3) |
| **Klaim tanpa angka eksekusi / tidak bisa diverifikasi** | **0** — setiap klaim utama evaluator punya jejak artefak JSON |
| **Klaim karangan (angka tidak ada di artefak sama sekali)** | **0** — TIDAK ditemukan satu pun angka karangan |

**Kesimpulan utama: angka evaluator BUKAN karangan.** Semua angka yang diuji berasal dari artefak eksekusi nyata. Masalah yang ada adalah 6 selisih (3 overclaim ringan, 1 kontradiksi internal, 2 slip aritmetika median) — bukan fabrikasi.

---

## 2. Metode hitung ulang (reproducible)

- Skrip audit: `recompute.py`–`recompute5.py`, `discriminate.py`–`discriminate3.py`, `aggregate.py` (workspace kanban t_263e7df0); log keluaran: `out/*.log`.
- Sumber primer: `scratch/v8_e_shk/e_shk_01_layerA.json`, `e_shk_02_layerB.json`; `scratch/v8_e/V8_E_A_loto.json`, `V8_E_B_warning.json`, `V8_E_C_robust.json`, `V8_E_cp_validity.json`; `scratch/v8_e_hyd/claim1_results.json`, `claim2_results.json`, `claim2b_supplement.json`, `layerB_realevent.json`; `scratch/v6_e1/E1_LOWO_RESULTS.json`, `E1d_LOWO_RESULTS.json`; workspace evaluator stuck `eval_results.json`.
- Setiap klaim dokumen dicocokkan dengan tol yang wajar (≤1,5e-3 untuk desimal, persis untuk hitungan); selisih > toleransi didiskriminasi satu per satu (apakah kunci JSON salah / unit beda / selisih nyata).

---

## 3. Tabel selisih — 6 klaim tidak cocok + 7 hasil awal yang ternyata kesalahan skrip audit

| # | Isi klaim dokumen | Metode verifikasi | Hasil | Catatan |
|---|---|---|---|---|
| 1 | hyd: "CI95 persistence vs RF **tidak tumpang tindih di 6/7 fold** (F-9 satu-satunya tumpang tindih)" (V8_E_hyd baris 63, 179; diulang M1 baris 54, 65) | Bandingkan interval CI95 aktual per fold dari `claim1_results.json` | **BERLEBIH — salah** | Tumpang tindih = **2/7**: F-9 (RF [0,283;0,829] vs pers [0,394;0,799]) **dan F-5** (RF [0,072;0,398] vs pers [0,383;0,757] — overlap 0,383–0,398). Seharusnya "tidak tumpang tindih **5/7**". M1 mewarisi kesalahan ini. Keunggulan persistence tetap nyata (ΔB<0 7/7) tapi klaim kekuatan bukti statistik terlalu kuat. |
| 2 | shk: "Persistence mengalahkan RF AUPRC di **4/9 fold (F-7, F-14, F-10, F-12)**" (V8_E_shk baris 41) | AUPRC per fold dari `e_shk_01_layerA.json` | **SALAH (understate persistence)** | Sebenarnya **5/9**: F-15_S juga (pers 0,0393 > RF 0,0285). Daftar fold keliru 1 butir. Tidak merugikan verdict — malah mengurangi jumlah kemenangan persistence. |
| 3 | shk: "**FAR ≤ 1/24 jam dengan recall > 0: TIDAK tercapai di fold mana pun** (semua ambang yang menghasilkan FAR ≤ 1 menghasilkan 0 alarm/recall 0)" (V8_E_shk baris 61, 112; diulang M1 baris 55, 169 "0 dari 9 fold") | Seluruh grid titik operasi (semua fold, semua tau) dari `e_shk_01_layerA.json` | **BERLEBIH (klaim absolut keliru)** | Ada **1 pengecualian**: F-14 tau=0,30 → FAR **0,69/24h**, recall **0,92%** (P 0,259; 9 alarm = 4 TP + 5 FP). 14 titik grid punya FAR≤1, 1 di antaranya recall>0. Dampak: verdict "BELUM alarm otomatis" TETAP BENAR (recall 0,9% tidak operasional), tapi angka "0/9" dan kalimat absolut keliru; M1 mewarisi. |
| 4 | stuck: "**FAR semua engine 9,9–185** per 24 jam-negatif" (V8_E_stuck baris 31) dan "FAR 25–185/24 jam" (baris 206) | `eval_results.json` evaluator stuck, semua fold × engine | **KONTRADIKSI INTERNAL — salah di ringkasan** | E3_RF pada LOWO F-14→F-9_A = **60/neg-jam = 1.440/24 jam** — angka ini ADA di tabel dokumen sendiri (baris 100: "1.440") dan di bagian verdict (baris 226: "FAR 9,9–1.440"); M1 baris 53 juga benar. Ringkasan/executive salah. Kategori "BELUM alarm/otomatis" tetap benar (malah lebih kuat). |
| 5 | tool_wear: engine (i) within-tool @FAR≤1/menit — "T_lead median **30 dtk** (20–36)" (V8_E_tool_wear baris 102; diulang 106, 162 "30–47,5 dtk") | `V8_E_C_robust.json` baris target=1,0: t_lead = 20, 24, 25, 36 dtk | **BERLEIH — median salah** | Median aktual = **24,5 dtk** (rentang 20–36 di dokumen cocok; hanya mediannya meleset). Lead time dit overstated ~5,5 dtk di ringkasan. |
| 6 | tool_wear: engine (ii) LOTO-RF FAR-terkalibrasi — "T_lead median **47,5 dtk** (35–59)" (baris 101; diulang 133, 162) | `V8_E_C_robust.json`: t_lead = 35, 41, 53, 59 dtk | **SLIP KECIL** | Median aktual = **47,0 dtk**. Selisih 0,5 dtk — pembulatan/slip aritmetika, tidak mengubah kesimpulan. |
| A1 | (awal FAIL) stk: CI low LOWO 9A→14 = 0,018 | `AUPRC_CI.CI95 = [0,0182; 0,0782]` | **TERVERIFIKASI — dokumen benar** | Kesalahan skrip audit (membaca bootstrap-recall-CI, bukan CI AUPRC). |
| A2 | (awal FAIL) stk: kontrol-positif F-14 = 0/10 | Artefak = 0 sejajaran | **TERVERIFIKASI — dokumen benar** | Kesalahan kunci skrip audit. |
| A3 | (awal FAIL) tw: E2 FAR-cal deteksi "4/4" | 8 baris = 4 alat × 2 setelan target; 4/4 alat unik terdeteksi | **TERVERIFIKASI — dokumen benar** | Skrip audit menghitung baris, bukan alat. |
| A4 | (awal FAIL) tw: E2 FP baseline "1–2" | E2_fp @target1,0 = [1,1,2,1] → 1–2 | **TERVERIFIKASI — dokumen benar** | Skrip audit salah memakai figur E1 ("1–3") untuk E2. |
| A5 | (awal FAIL) shk: "RF ≥ persistence B1 di 9/9 fold" | `e_shk_02_layerB.json`: RF≥P di 6/6 well evaluatable; 3 well sisanya B1 0=0 | **TERVERIFIKASI (teknis ≥ benar) + catatan interpretasi** | 9/9 benar sebagai "≥" (3 di antaranya tie 0–0: F-15A, F-9, F-9_A; 1 tie 0,071=F-10). "ML **menambah** nilai" (baris 83, 107) ketat hanya di **4 fold** (F-14 0,217>0,167; F-15_S 0,348>0,087; F-5 0,208>0,083; F-7 0,286>0,071). Interpretasi = overclaim ringan, angkanya benar. |
| A6–A7 | (awal TIDAK-BISA ×3) shk B1@tau0,05 = 0,217 & T_lead med = 3,0; tw E2 median | Jalur kunci benar: `operating/grid_05/rf` | **TERVERIFIKASI — dokumen benar** (0,2167≈0,217; 3,0 dtk) | TIDAK-BISA terselesaikan; tw E2 median = 47,0 (lihat butir 6). |

---

## 4. Contoh angka terverifikasi (per engine — melampaui syarat ≥8)

| Engine | Klaim dokumen | Nilai hitung ulang | Status |
|---|---|---|---|
| vib | F-14 AUPRC RF 0,912 / persistence 0,796; F-15_S lift 3,50; persistence>RF 2/4; RF≥canary 4/4 | 0,9117 / 0,7959; 3,50; 2/4; 4/4 | terverifikasi |
| ssi | F-14 AUPRC 0,0358; F-15_S 0,1057; F-9_A lift 1,47; F-5 canary 0,0676; CI-bawah>prev 2/5; n_pos F-9_A 55 | 0,0358; 0,1057; 1,47; 0,0676; F-15_S+F-5; 55 | terverifikasi |
| bit_wear | F-15S AUPRC 0,813/pers 0,984; F-15 n_test 1057, AUPRC 0,365/pers 0,698; persistence>RF 4/4; RF>canary 4/4 | identik semua | terverifikasi |
| stuck | F-10 E1 P 0,457, FAR 23,5/24h, T_lead 10 mnt; E2 B1 31,8%, AUPRC 0,246; E3 lift 1,65; LOWO 9A→14 lift 9,72, CI [0,018;0,078]; kontrol-positif 0/10 | identik semua | terverifikasi |
| hyd | F-14 n_test 10401, AUPRC_RF 0,117/pers 0,444; ΔB<0 7/7; P persistence 0,615–0,793; FAR 38,8–110,7; K-ii AUPRC 0,2279, lift 61,6, 124 episode; coverage 94,0–98,7%; beban 4,707 & 0,263 blok/hari | identik semua | terverifikasi |
| shk | F-14 n_pos 760, prev 6,78%, AUPRC RF 0,0918; reproduksi V6 7/7 <1e-9; RF>canary 6/9; lift spread 8,85; FAR≤6 dgn recall>0 = 4 titik (P 0,259–0,552); F-14 tau0,05 FAR 48,1, tau0,30 FAR 0,7; budget-ambang 0 alarm 9/9 | identik semua | terverifikasi |
| tool_wear | T01–T04 AUPRC 0,5433/0,7684/0,7031/0,6497; precision 0,516/0,559/0,509/0,500; FAR/menit 46,0–60,0; cp signifikan 8/8; cp <5 dtk 0/8; C3 drop maks 18,3%/26,2% | identik semua | terverifikasi |
| shk tabel per-well (M1 & doc §3) | 9 well × kolom B1/T_lead/B1-pers/FP_engine/FP_display @tau0,05/0,20 | **45/45 sel cocok** | terverifikasi |

---

## 5. Daftar OVERCLAIM (klaim berlebih vs bukti)

1. **hyd + M1 — "CI non-tumpang tindih 6/7"** → kenyataan 5/7 (F-5 juga overlap). Overclaim kekuatan bukti statistik. *(selisih #1)*
2. **shk + M1 — "FAR≤1 dgn recall>0 TIDAK tercapai / 0 dari 9 fold"** → ada 1 titik (F-14 tau0,30; recall 0,92%). Klaim batas terlalu absolut. *(selisih #3)*
3. **shk — "RF≥persistence B1 9/9 fold → ML MENAMBAH nilai peringatan dini"** → 9/9 benar untuk "≥", tapi 4 fold adalah tie (3× 0–0, 1× 0,071); "menambah" ketat hanya 4/9. *(butir A5)*
4. **stuck — ringkasan "FAR semua engine 9,9–185 / 25–185"** → menyembunyikan (tanpa maksud jahat — kontradiksi internal) E3_RF 1.440/24h yang ada di tabel dokumennya sendiri. *(selisih #4)*
5. **tool_wear — "peringatan median 30 dtk"** → 24,5 dtk; ringkasan "30–47,5 dtk" (baris 106, 162) seharusnya "24,5–47,0 dtk". *(selisih #5, #6)*

**Pemeriksaan "layak alarm otomatis" (syarat penerimaan b):** TIDAK ADA evaluator yang mengklaim layak alarm otomatis. Semua 7 dokumen menyatakan BELUM (shk: "Belum untuk alarm otomatis kritis — tidak ada di kurva"; stuck: "Alarm kritis otomatis: BELUM"; ssi: "BELUM LAYAK… B4/FAR & C3 belum diukur"; hyd: FAR 39–111 & 5,9 ≫ 1; vib/ssi: FAR&B belum terukur; bit_wear: "sebelum FAR/precision terukur"; tool_wear: "G1 0/4, precision ≈0,5"). M1 menghitung eksplisit **0/7 layak alarm otomatis**. Tidak ada overclaim kelayakan alarm.

## 6. Pemeriksaan gate biner terselubung (syarat penerimaan c)

**Bersih — 0 temuan.** G1/G2 V6 hanya dipakai sebagai (a) konteks ambang-atas "TERBUKTI-KUAT" dan (b) bagian dari syarat ambang-atas alarm otomatis yang selalu dipenuhi dengan syarat B dan C. Tidak ada evaluator yang menjatuhkan vonis pakai lift≥1,5 saja. Praktik baik ditemukan: bit_wear menyatakan fold dengan n_pos kecil "secara matematis tidak bisa mencapai lift jauh di atas 1,5 — fold 'gagal ambang' bukan bukti kegagalan"; ssi menyatakan G1 4/5+G2 5/5 tercapai TETAPI tetap BELUM alarm karena FAR/B4/C3 belum — persis perilaku kerangka baru yang diharapkan.

## 7. Baseline relevan (syarat penerimaan d)

Semua 7 evaluator mendeklarasikan baseline per-tugas (bukan satu baseline universal): shk (canary-depth, persistence, prevalence-random), ssi (persistence, canary-kedalaman, rule SSI≥1), bit_wear (canary kedalaman), vib (persistence, canary), hyd (RF vs persistence dua arah), stuck (canary-kedalaman 0,41, persistence-onset, E1 vs E2), tool_wear (canary amplitudo, identity-majority, rule 3-RMS). Klaim "bagus" selalu bersifat relatif terhadap baseline spesifik. **Lulus.**

## 8. Konsistensi antar-dokumen (syarat penerimaan e)

- **M1 mewarisi 2 kesalahan evaluator:** hyd "CI 6/7" (M1 baris 54, 65) dan shk "0/9 fold FAR≤1" (M1 baris 55, 169).
- **M1 benar, evaluator salah:** stuck FAR — M1 baris 53 menulis "9,9–1.440" (benar), dokumen stuck ringkasan menulis 9,9–185 (salah).
- **Tabel konsisten:** tier M1 "0 alarm / 3 peringatan layak / 2 bersyarat / 2 tren-saja = 7" koheren internal (3+2+2=7; baris 180 "5/7 punya jalur peringatan" cocok).
- Koherensi lain (persistence = engine status default di 4 evaluator; FAR 3 skala dilaporkan apa adanya) terverifikasi konsisten.

## 9. Batas jujur evaluator (syarat penerimaan f)

Ketujuh dokumen memuat bagian "BELUM untuk…" yang eksplisit (alarm otomatis, transfer lintas-wellbore, B3, C3, dsb.) dan M1 merangkum batas per engine. Tidak ada dokumen yang hanya menyebut kelebihan. **Lulus.**

## 10. Batas audit ini

- Hitung ulang dilakukan terhadap **artefak JSON**, bukan re-run model dari data mentah (waktu/komputasi); keaslian artefak mengikuti rantai eksekusi evaluator sebelumnya.
- Audit angka tidak memvalidasi desain eksperimen (mis. apakah H=10 menit tepat) — itu ranah R1/A2.
- 2 selisih median tool_wear (butir 5–6) tidak memeriksa kemungkinan dokumen mengutip run lebih awal yang berbeda; yang diperiksa adalah artefak final yang dikutip dokumen.

## 11. Kesimpulan & rekomendasi

**Tidak ada karangan.** 114/121 klaim numerik (dan 45/45 sel tabel shk) terverifikasi persis dari artefak primer; 6 selisih nyata — semuanya kekeliruan penyajian (median, rentang, jumlah fold, tumpang-tindih CI), bukan fabrikasi, dan tidak satu pun membalikkan verdict kemampuan apa pun.

Perbaikan yang direkomendasikan (dapat dipatch evaluator/ M1 masing-masing):
1. hyd baris 63/179 + M1 54/65: "6/7" → "5/7 (F-5 dan F-9 tumpang tindih)".
2. shk baris 41: "4/9 (F-7, F-14, F-10, F-12)" → "5/9 (…+ F-15_S)".
3. shk baris 61/112 + M1 55/169: "TIDAK tercapai di fold mana pun / 0 dari 9 fold" → "hanya 1 titik dari seluruh grid 9 fold (F-14 tau0,30: FAR 0,69/24h, recall 0,92%) — recall terlalu kecil untuk operasional".
4. shk baris 83/107 (dan M1): "RF≥persistence 9/9 → ML menambah nilai" → tambahkan "4 fold tie (3× 0–0, 1× 0,071); menambah nilai secara ketat di 4/9".
5. stuck baris 31/206: "9,9–185 / 25–185" → "9,9–1.440 (E3_RF LOWO F-14→F-9_A = 1.440/24h; engine in-well 9,9–185)".
6. tool_wear baris 102/106/133/162: median E1 "30 dtk" → "24,5 dtk"; E2 "47,5" → "47,0"; ringkasan "30–47,5 dtk" → "24,5–47,0 dtk".
