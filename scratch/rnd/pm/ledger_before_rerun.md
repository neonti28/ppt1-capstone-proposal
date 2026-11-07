# RND-P0: LEDGER PROVENANCE ANGKA ALAT PdM (7 ENGINE, 11 KLAIM)

Kartu: `t_b90b3272` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Dokumen pendamping: `docs/RND_P0_PARAMETER.md`

Riset pendahuluan: literature-review (pencarian bertahap ke ISO/API/SPE dan Crossref untuk memastikan nomor standar + bagian, bukan hanya nama), scientific-critical-thinking (memisahkan nilai yang dapat diturunkan secara aritmetik dari nilai yang hanya kesepakatan internal, dan menolak peminjaman standar yang ruang lingkupnya berbeda), verification-mandatory (setiap baris ledger menyebut file+baris kode atau DOI/URL yang benar-benar dibuka; baris yang tidak dapat dibuka ditandai, bukan dikarang).

Riset pendahuluan: sequentialthinking, 5 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..5, thoughtHistoryLength 5). Ringkas: (1) inventaris lokasi kode nyata per angka, (2) uji asal-usul tiga angka yang tampak "ajaib" (32,17405; 0,6745; SSI >= 1) dan pemisahan satuan-lawan-ambang, (3) penolakan standar yang tidak relevan ruang lingkupnya, (4) pemisahan ambang FAR/horizon sebagai konvensi operasional, (5) gerbang verifikasi sebelum menulis dan daftar yang tetap belum.

---

## 0. CATATAN STRUKTUR TABEL

Kartu menyebut "template 7 kolom" tetapi daftar field yang diberikan berjumlah 8 (No, Angka, Satuan, Kelas sumber, Rujukan persis, Tanggal akses, Dipakai di, Status). Sesuai `docs/RND_ALGO_RESEARCH_PLAN.md` §2 baris 22, ledger ini memakai **8 kolom**. Perbedaan ini dicatat, bukan disembunyikan.

Kelas sumber mengikuti plan §2, berurut kekuatan: `STANDAR` > `JURNAL` > `RUN-KITA` > `KONVENSI` > `BELUM-TERUKUR`.

Kolom Status memakai tiga tingkat yang dapat diaudit:
- `TERVERIFIKASI`: nilai dan sumbernya dibuka langsung (dokumen standar/jurnal terbaca atau Crossref/penerbit mengonfirmasi).
- `TERUKUR`: angka hasil eksekusi kita sendiri, ada file hasil + timestamp + definisi hitung.
- `BELUM`: angka dipakai di kode tetapi tidak ada rujukan eksternal atau turunan yang dapat dipertanggungjawabkan. Angka tetap boleh dipakai sebagai konvensi, tetapi dilarang diklaim sebagai bukti ilmiah.

Tanggal akses seluruh baris: 2026-10-27 (WIB), kecuali baris RUN-KITA yang menyebut tanggal eksekusi aslinya.

---

## 1. LEDGER

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| L-01 | 32,17405 | ft/s² | STANDAR (turunan) | ISO 2041:2018 §3.1.4 "standard acceleration due to gravity, gn = 9,806 65 m/s²", Note 2: "approximately 32,174 0 ft/s²". Konversi eksak 9,80665 × 3,280839895 = 32,1740486 (dihitung ulang, `verify_arith.py`) | 2026-10-27 | `code/v9_d1_02_rig_windows.py:35`; `code/v9_e_RULE_01_status.py:49` | TERVERIFIKASI |
| L-02 | 9,80665 | m/s² | STANDAR | ISO 2041:2018 §3.1.4 + Note 1: diadopsi 1901 oleh Resolusi CGPM ke-3 (CR 70) | 2026-10-27 | dasar L-01 | TERVERIFIKASI |
| L-03 | 3,280839895 | ft/m | STANDAR (definisi satuan) | 1 ft = 0,3048 m (definisi internasional), maka 1/0,3048 = 3,280839895013123 (dihitung ulang) | 2026-10-27 | konversi L-01 | TERVERIFIKASI |
| L-04 | SSI = (RPM_max − RPM_min) / (2 × RPM_mean) | rasio tak berdimensi | JURNAL | Liu, W. et al. 2025, "Intelligent identification method for stick-slip vibration based on downhole data", Thermal Science 29(2B):1521-1526, DOI 10.2298/TSCI2502521L, persamaan (1). PDF dibuka dan terbaca | 2026-10-27 | `code/v9_d1_02_rig_windows.py:92`; `code/v9_e_RULE_01_status.py:202` | TERVERIFIKASI |
| L-05 | SSI >= 1 | rasio | JURNAL | Liu et al. 2025, persamaan (2): SSI < 1 = torsional vibration; 1 <= SSI < 3 = moderate stick-slip; SSI >= 3 = severe stick-slip. Ambang 1 adalah batas bawah kelas "moderate", bukan angka pilihan sendiri | 2026-10-27 | `code/v9_d1_02_rig_windows.py:96`; `code/v9_e_RULE_01_status.py:203` dan `:260` | TERVERIFIKASI |
| L-06 | SSI = 1 bila RPM_min = 0 dan mean = (max+min)/2 | rasio | DERIVASI aritmetik | Substitusi ke rumus L-04: (max−0)/(2×max/2) = 1 untuk mean 50, 80, 120 RPM (dihitung ulang). Menjelaskan mengapa 1 bermakna "bit berhenti penuh" pada idealisasi sinusoidal | 2026-10-27 | penjelasan `docs/RND_P0_PARAMETER.md` §3.2 | TERVERIFIKASI sebagai aritmetika; asumsi midrange dicatat |
| L-07 | 10 | sampel (crpm_n) | KONVENSI | `code/v9_d1_02_rig_windows.py:34`; `code/v9_e_RULE_01_status.py:50` | 2026-10-27 | syarat validitas SSI | BELUM |
| L-08 | SHKRSK_RT >= 1 | hitungan kanal | KONVENSI (kanal diskret vendor) | `code/v9_e_RULE_01_status.py:180`; definisi label `code/v9_d1_02_rig_windows.py:41` | 2026-10-27 | label `y_shk`, shk rule | BELUM |
| L-09 | stuck_max >= 1 | hitungan kanal | KONVENSI | `code/v9_e_RULE_01_status.py:181`; `code/v9_d1_02_rig_windows.py:39` | 2026-10-27 | label `y_stuck`, stuck K-i | BELUM |
| L-10 | z(TQA) > 2 | unit sigma robust | KONVENSI | `code/v9_e_RULE_01_status.py:326` (kondisi `zt > 2`) | 2026-10-27 | stuck E1 2-dari-3 | BELUM |
| L-11 | z(HKLD) > 2 | unit sigma robust | KONVENSI | `code/v9_e_RULE_01_status.py:327` (kondisi `zh > 2`) | 2026-10-27 | stuck E1 2-dari-3 | BELUM |
| L-12 | ROP drop >= 30% | persen dari median 60 menit | KONVENSI | `code/v9_e_RULE_01_status.py:55` (`ROP_DROP = 0.30`), dipakai `:328` | 2026-10-27 | stuck E1 2-dari-3 | BELUM |
| L-13 | 60 | menit | KONVENSI | `code/v9_e_RULE_01_status.py:52` (`E1_WIN = 60`), dipakai `:314` | 2026-10-27 | jendela median/MAD stuck E1 | BELUM |
| L-14 | 10 | observasi minimum | KONVENSI | `code/v9_e_RULE_01_status.py:53` (`E1_MIN_OBS = 10`), dipakai `:314` | 2026-10-27 | syarat z terdefinisi | BELUM |
| L-15 | 0,6745 | faktor skala z | STANDAR (turunan aritmetik) | 0,6745 = Φ⁻¹(0,75) = 0,6744898, yaitu kebalikan 1,4826 (dihitung ulang: 0,6745 × 1,4826 = 1,00001). Catatan: komentar kode di `:54` mengatribusikan angka ini ke "NIST, R1 [7][8]", tetapi halaman NIST §1.3.5.6 yang saya buka tidak mencetak 0,6745 maupun 1,4826, sehingga atribusi NIST itu belum terbukti | 2026-10-27 | `code/v9_e_RULE_01_status.py:54` (`Z_SCALE`), dipakai `:319` dan `:320` | TERVERIFIKASI (konstanta sebagai aritmetika); atribusi NIST BELUM-TERVERIFIKASI |
| L-16 | 1,4826 | faktor skala MAD | STANDAR (turunan aritmetik) + definisi NIST | Definisi MAD: NIST/SEMATECH e-Handbook of Statistical Methods §1.3.5.6 (halaman dibuka). Konstanta 1,4826 = 1/Φ⁻¹(0,75) = 1,4826022 (dihitung ulang). Halaman NIST tersebut mendefinisikan MAD dan sifat robustnya, tetapi tidak mencetak angka 1,4826 | 2026-10-27 | `code/v9_d1_03_rig_datasets.py:69`; `code/v9_e_RULE_01_status.py:224`; `code/v9_i1_pipeline.py:619`; `code/v9_e_STAT_03_tool_wear.py:40` | TERVERIFIKASI (konstanta + definisi); atribusi angka ke NIST dicatat sebagai turunan, bukan kutipan |
| L-17 | abs(z) > 2 pada SPPA | unit sigma robust | KONVENSI | `code/v9_d1_03_rig_datasets.py:70`; `code/v9_e_RULE_01_status.py:225` | 2026-10-27 | label `y_hyd` (K-i) dan display hyd | BELUM |
| L-18 | qcut(TFLO, 10) | 10 bin | KONVENSI | `code/v9_d1_03_rig_datasets.py:28` (`NQ = 10`), `:63`; `code/v9_e_RULE_01_status.py:217` | 2026-10-27 | normalisasi SPPA per laju alir | BELUM |
| L-19 | >= 50 | bin berlabel | KONVENSI | `code/v9_d1_03_rig_datasets.py:61` (`if len(d) >= 50`) | 2026-10-27 | syarat label hyd terbentuk | BELUM |
| L-20 | MSE > P75 | kuantil ke-75 | KONVENSI untuk ambang; JURNAL untuk rumus MSE | Rumus MSE: Teale, R. 1965, "The concept of specific energy in rock drilling", Int. J. Rock Mech. Min. Sci. & Geomech. Abstr. 2(1):57-73, DOI 10.1016/0148-9062(65)90022-7 (terkonfirmasi di registri Crossref). Ambang P75: `code/06_xgb_fuzzy.py:77`; audit label `code/10_audit_maintenance_claim.py:86` | 2026-10-27 | label `high_MSE_bit_wear`, bit_wear K-1 | JURNAL untuk rumus, BELUM untuk ambang P75 (Teale tidak menetapkan P75) |
| L-21 | >= 5 dari 27 fitur | hitungan fitur | KONVENSI | `code/v9_e_STAT_03_tool_wear.py:40` (`N_FEAT_ALARM = 5`), `:206`; `code/v9_i1_pipeline.py:627`; jumlah 27 dipaksakan oleh asersi `code/v9_i1_pipeline.py:605` dan `code/v9_e_RULE_03_bitwear_toolwear.py:145` | 2026-10-27 | tool_wear `calib_5of27` | BELUM |
| L-22 | abs(z) > 3 | unit sigma | KONVENSI | `code/v9_e_STAT_03_tool_wear.py:40` (`Z_THR = 3.0`); `code/v9_i1_pipeline.py:624` | 2026-10-27 | tool_wear `calib_5of27` | BELUM (aturan 3 sigma adalah konvensi statistik, bukan ambang PdM terbit) |
| L-23 | 30% awal R01 | persen jendela | KONVENSI | `code/v9_e_STAT_03_tool_wear.py:40` (`CAL_FRAC = 0.30`), `:195`; `code/v9_i1_pipeline.py:616` | 2026-10-27 | kalibrasi within-tool | BELUM |
| L-24 | minimal 5 | jendela kalibrasi | KONVENSI | `code/v9_i1_pipeline.py:616` (`ncal = max(5, ceil(0.30 * len(r01)))`); `code/v9_e_STAT_03_tool_wear.py:195` | 2026-10-27 | kalibrasi within-tool | BELUM |
| L-25 | <= 1 | alarm/menit | KONVENSI | `code/v9_i1_pipeline.py:612` (`TARGET_FP_PER_MIN = 1.0`); `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2 | 2026-10-27 | titik operasi tool_wear (domain bengkel, jendela 1 detik) | BELUM (target, bukan hasil ukur) |
| L-26 | FAR <= 6 | alarm palsu per 24 jam | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2; `code/v9_eval_a_01_compute.py:37` dan `:108` | 2026-10-27 | gerbang tier LAYER-1 | BELUM |
| L-27 | FAR_24j = FP / (n_neg/60) × 24 | alarm palsu/24 jam | KONVENSI (rumus internal) | `code/v9_i1_pipeline.py:307` sampai `:325` (dokumentasi + implementasi) | 2026-10-27 | semua badge FAR | TERVERIFIKASI (kode terbaca); rumus ini bukan standar |
| L-28 | 10 | menit (horizon) | KONVENSI | `code/v9_d1_02_rig_windows.py:31` (`W = 10`); `code/v9_e_RULE_04_hyd_k2.py:30` (`H = 10`) | 2026-10-27 | label horizon, persistence `[t0-10, t0)` | BELUM (konsisten dengan TLead 4,5-8,5 menit di EVAL_C, bukan diturunkan dari situ) |
| L-29 | 10 | menit (jendela agregasi) | KONVENSI | `code/v9_d1_02_rig_windows.py:31`; `code/v9_e_RULE_01_status.py:51` (`W = 10`) | 2026-10-27 | jendela label `[t0, t0+10)` | BELUM |
| L-30 | 5 bin / 60 baris | bin, baris | KONVENSI | `code/v9_d1_02_rig_windows.py:32` (`MIN_DRILL_BINS = 5`), `:33` (`MIN_DRILL_ROWS = 60`) | 2026-10-27 | syarat fitur valid (baris drilling) | BELUM |
| L-31 | P 0,9444 · R 0,4537 · FAR 49,942 · TP 510 / FP 30 / FN 614 | rasio; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, `meta.generated_at` = 2026-10-12 12:32:19, segmen rig F-14, head `vib.rule_display`, n=1989 | 2026-10-27 (baca) | badge vib rule L1 | TERUKUR |
| L-32 | P 0,8243 · R 0,5965 · FAR 16,611 | rasio; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, segmen F-14, head `hyd.hybrid_rule_and_persistence`, n=10401 | 2026-10-27 (baca) | badge hyd hybrid L1 | TERUKUR |
| L-33 | FP 1-3 per alat · TLead 20-36 detik · deteksi 4/4 | hitungan; detik | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, head `tool_wear.op_far_calibrated`, blok `per_alat` (T01..T04), 4 alat x 2 run = 469 jendela | 2026-10-27 (baca) | badge tool_wear L1 | TERUKUR |
| L-34 | P 0,534 · R 0,0724 · FAR 6,618 | rasio; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, segmen F-14, head `shk.rule_display`, n=11205 | 2026-10-27 (baca) | badge shk rule | TERUKUR |
| L-35 | P 0,0192 · R 0,0154 · FAR 4,627 | rasio; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, head `stuck.e1_2of3`, n=95925 | 2026-10-27 (baca) | badge stuck E1 | TERUKUR |
| L-36 | P 0,9927 · R 0,9925 · FAR 1,213 | rasio | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`, head `bit_wear.persistence`, n=47645, grid kedalaman USROP | 2026-10-27 (baca) | badge bit_wear | TERUKUR, dengan catatan sirkular: label = Teale high_MSE, penilai = y(t-1) |
| L-37 | 5 | menit beruntun (sustain) | KONVENSI | `code/v9_e_RULE_04_hyd_k2.py:32` (`SUSTAIN = 5`), dipakai `:88` | 2026-10-27 | episode kick/loss hyd K-ii | BELUM |
| L-38 | 30 | menit (gap penggabungan episode) | KONVENSI | `code/v9_e_RULE_04_hyd_k2.py:31` (`EPISODE_GAP = 30`), dipakai `:93`; blok +30 menit pasca-onset dibuang dari baris evaluasi `:144` | 2026-10-27 | pembentukan episode dan pengecualian evaluasi hyd K-ii | BELUM (perlu alasan mengapa 30, bukan 15 atau 60) |
| L-39 | 500 | L/min (syarat sirkulasi, Flow Pumps) | KONVENSI | `code/v9_e_RULE_04_hyd_k2.py:33` (`QMIN = 500.0`) | 2026-10-27 | validitas z-pit hyd K-ii | BELUM (ambang operasional sumur F-9 A, bukan standar) |

---

## 2. STANDAR YANG DIPERIKSA DAN HASILNYA

| No | Standar | Bagian yang dibaca | Isi yang terverifikasi | Dipakai untuk | Keputusan |
|---|---|---|---|---|---|
| S-1 | ISO 2041:2018 Mechanical vibration, shock and condition monitoring: Vocabulary | §3.1.4 | gn = 9,806 65 m/s², diadopsi 1901 oleh CGPM ke-3; Note 2 menyebut ≈ 32,174 0 ft/s² | asal L-01, L-02 | DIPAKAI |
| S-2 | ISO 20816-1:2016 Mechanical vibration: Measurement and evaluation of machine vibration, Part 1: General guidelines | §1 Scope (pratinjau resmi ISO) | Berlaku untuk pengukuran pada bagian berputar/tidak berputar dari MESIN lengkap (poros, rumah bantalan), dan secara eksplisit "does not include consideration of torsional vibration" | tidak dipakai untuk VIBLAT_RT maupun SSI | DITOLAK sebagai dasar ambang; ruang lingkupnya mesin rotasi permukaan, bukan drillstring |
| S-3 | ISO 20816-1:2016 catatan rujukan torsional | Note 3 pada §1 | Untuk getaran torsional dirujuk ISO 3046-5, ISO 22266-1, atau VDI 2039 | menunjukkan bahwa standar keluarga torsional pun menyasar shaft train/turbomachinery | DITOLAK sebagai dasar ambang SSI; hanya penunjuk arah |
| S-4 | API RP 7G Recommended Practice for Drill Stem Design and Operating Limits, edisi 16 (1998, dengan R2015/R2026) | judul + tujuan standar (halaman penjual resmi) | Ruang lingkup = desain drill stem dan batas operasi aman; tidak ditemukan klausul ambang severity getaran atau stick-slip | pemeriksaan "apakah ada API RP untuk getaran" | TIDAK ADA KLAUSUL AMBANG; dicatat sebagai ketiadaan, bukan kesimpulan dari nama standar |

Catatan kejujuran: nomor bagian S-4 tidak dicantumkan karena teks penuh API RP 7G berbayar dan tidak dibuka. Karena itu S-4 tidak dipakai sebagai dasar rekomendasi mana pun, hanya sebagai catatan bahwa celah standar memang ada.

---

## 3. RUJUKAN ILMIAH TERVERIFIKASI

| Kode | Rujukan | Verifikasi |
|---|---|---|
| J-1 | Teale, R. (1965). The concept of specific energy in rock drilling. International Journal of Rock Mechanics and Mining Sciences & Geomechanics Abstracts, 2(1), 57-73. DOI 10.1016/0148-9062(65)90022-7 | Registri Crossref mengembalikan judul, penulis, volume, halaman, dan DOI yang cocok. Catatan: permintaan langsung ke doi.org untuk DOI ini mengembalikan 404 pada pengambil halaman, sehingga status verifikasi bersandar pada registri Crossref, bukan halaman pendaratan Elsevier |
| J-2 | Kyllingstad, Å., & Halsey, G. W. (1988). A study of slip/stick motion of the bit. SPE Drilling Engineering, 3(4), 369-373. DOI 10.2118/16659-PA | Registri Crossref mengembalikan judul, penulis, volume, issue, halaman, tahun, dan abstrak (menyebut drill collar berhenti penuh secara periodik) |
| J-3 | Liu, W., Pan, T., Fang, C., Li, Q.-F., Zhou, C., Li, X.-C., Zhu, Z., Zhu, L., & Wang, C.-C. (2025). Intelligent identification method for stick-slip vibration based on downhole data. Thermal Science, 29(2B), 1521-1526. DOI 10.2298/TSCI2502521L | PDF terbuka dan terbaca; rumus SSI (persamaan 1) dan kriteria grading (persamaan 2) dikutip langsung |
| J-4 | Reckmann, H., Jogi, P., Kpetehoto, F. T., Chandrasekaran, S., & Macpherson, J. D. (2010). MWD failure rates due to drilling dynamics. IADC/SPE Drilling Conference and Exhibition, New Orleans, SPE-127413-MS. DOI 10.2118/127413-MS | Registri Crossref mengembalikan judul, tahun, venue, nomor kertas; halaman OnePetro mengonfirmasi judul yang sama |
| J-5 | NIST/SEMATECH e-Handbook of Statistical Methods, §1.3.5.6 "Measures of Scale" | Halaman dibuka dan terbaca; mendefinisikan MAD dan sifat robustnya |

Rujukan yang ditemukan tetapi TIDAK dipakai sebagai dasar: Hegde et al. (2019) hanya muncul sebagai sitasi sekunder di daftar pustaka J-3 dan DOI-nya belum diperiksa; klaim ambang akselerasi lateral 25 g hanya ditemukan di glosarium vendor, bukan di J-4 yang teks penuhnya berbayar. Keduanya masuk daftar belum terverifikasi di §5.

---

## 4. REKAP

| Kelas | Jumlah baris | No baris |
|---|---|---|
| STANDAR (termasuk turunan aritmetik) | 5 | L-01, L-02, L-03, L-15, L-16 |
| JURNAL | 3 | L-04, L-05, L-20 (JURNAL untuk rumus, BELUM untuk ambang) |
| RUN-KITA | 6 | L-31 sampai L-36 |
| KONVENSI | 24 | L-07 sampai L-14, L-17 sampai L-19, L-21 sampai L-30, L-37 sampai L-39 |
| DERIVASI aritmetik | 1 | L-06 |
| BELUM-TERUKUR | 0 angka baru dikarang | semua angka yang tidak bersumber ditulis `BELUM`, tidak diisi taksiran |

Jumlah baris total: 39 (5 + 3 + 6 + 24 + 1).

---

## 5. YANG BELUM TERVERIFIKASI

1. `BELUM-TERVERIFIKASI`: ambang akselerasi lateral 25 g untuk keandalan MWD/LWD. Sumber yang terbaca hanya halaman glosarium vendor yang mengutip Reckmann et al. (2010); teks penuh SPE-127413-MS berbayar dan tidak dibuka. Tidak dipakai sebagai dasar rekomendasi.
2. `BELUM-TERVERIFIKASI`: DOI Hegde et al. (2019) "Classification of drilling stick slip severity using machine learning", J. Petroleum Science and Engineering 179:1023-1036. Hanya diketahui sebagai sitasi sekunder di J-3.
3. `BELUM-TERVERIFIKASI`: klausul tepat di ISO 80000-3:2019 yang mencantumkan gn. Nilai gn sendiri terverifikasi lewat ISO 2041:2018 §3.1.4 (standar yang sama-sama berlaku), teks penuh ISO 80000-3 tidak dibuka.
4. `BELUM-TERVERIFIKASI`: klausul apa pun di dalam API RP 7G. Yang terverifikasi hanya judul, edisi, dan ruang lingkup umum.
5. `BELUM`: dasar ilmiah untuk 24 baris KONVENSI (SSI_MIN_SAMPLES 10, SHKRSK >= 1, stuck_max >= 1, z > 2, ROP drop 30%, jendela 60 menit, E1_MIN_OBS 10, abs(z) > 2 hyd, qcut 10, min 50 bin, ambang P75 MSE, 5/27 fitur, abs(z) > 3, kalibrasi 30%, min 5 jendela, 1 alarm/menit, FAR <= 6, horizon 10 menit, jendela 10 menit, 5 bin/60 baris, sustain 5 menit, gap episode 30 menit, syarat sirkulasi 500, rumus FAR internal). Cara menaikkannya ada di `docs/RND_P0_PARAMETER.md` §3 per baris.
6. `BELUM-TERVERIFIKASI`: atribusi langsung angka 1,4826 ke NIST. Halaman NIST §1.3.5.6 mendefinisikan MAD dan memberi contoh numerik (0,997 lawan 0,681) tetapi tidak mencetak 1,4826. Angka tersebut sah sebagai turunan 1/Φ⁻¹(0,75) yang dihitung ulang.

## Ringkasan 5 baris

1. Dari 39 baris ledger, 5 baris bersandar pada STANDAR (termasuk 2 turunan aritmetik), 3 pada JURNAL, 1 derivasi aritmetik murni, 6 pada eksekusi sendiri (RUN-KITA), dan 24 masih KONVENSI internal.
2. Empat angka yang tampak "ajaib" ternyata dapat diturunkan: 32,17405 ft/s² = 1 g (ISO 2041:2018 §3.1.4), 0,6745 = Φ⁻¹(0,75), 1,4826 = 1/Φ⁻¹(0,75), SSI >= 1 = batas kelas "moderate stick-slip" (Liu et al. 2025, persamaan 2).
3. Dua standar populer DITOLAK sebagai dasar ambang: ISO 20816-1:2016 (ruang lingkup mesin permukaan, dan eksplisit tidak mencakup torsional) dan API RP 7G (desain drill stem, tanpa klausul severity getaran).
4. Seluruh ambang operasional (FAR <= 6/24 jam, <= 1 alarm/menit, horizon 10 menit, jendela 10 menit) tetap KONVENSI; ia keputusan desain, bukan temuan ilmiah.
5. Tidak ada angka baru yang dikarang: setiap parameter yang tidak bersumber ditulis BELUM beserta jalur menaikkannya.

## Bagian D0: kelayakan data per algoritma (kartu t_34c20c78)

Penomoran memakai awalan `D0-` agar tidak bertabrakan dengan id `L-xx` bagian P0. Jumlah baris D0 = 785. Semua angka dihitung ulang dengan skrip pengukur di workspace kartu `t_34c20c78`.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| D0-001 | 23.922 | jendela | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `well`/`y_vib`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-002 | 4 | well | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `well`/`y_vib`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-003 | 5.429 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `well`/`y_vib`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-004 | 22,69 | % | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `well`/`y_vib`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-005 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-006 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `SPPA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-007 | 6,10 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `TFLO_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-008 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-009 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-010 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-011 | 0,02 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-012 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-013 | 100,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `SPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-014 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-015 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-016 | 1.989 jendela / 1.124 positif / 56,51% | per well | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-017 | 6.482 jendela / 1.543 positif / 23,80% | per well | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group `well=F-15A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-018 | 10.903 jendela / 1.532 positif / 14,05% | per well | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group `well=F-15_S`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-019 | 4.548 jendela / 1.230 positif / 27,04% | per well | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group `well=F-5`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-020 | 35.906 | jendela | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `well`/`y_ssi`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-021 | 9 | well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `well`/`y_ssi`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-022 | 607 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `well`/`y_ssi`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-023 | 1,69 | % | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `well`/`y_ssi`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-024 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-025 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `SPPA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-026 | 3,04 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `TFLO_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-027 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-028 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-029 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-030 | 3,39 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-031 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-032 | 100,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `SPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-033 | 0,22 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-034 | 0,26 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-035 | 7.133 jendela / 161 positif / 2,26% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-10`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-036 | 4.293 jendela / 83 positif / 1,93% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-12`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-037 | 5.455 jendela / 75 positif / 1,37% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-038 | 6.020 jendela / 31 positif / 0,51% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-15A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-039 | 5.342 jendela / 85 positif / 1,59% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-15_S`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-040 | 4.714 jendela / 102 positif / 2,16% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-5`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-041 | 982 jendela / 3 positif / 0,31% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-7`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-042 | 1.126 jendela / 12 positif / 1,07% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-9`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-043 | 841 jendela / 55 positif / 6,54% | per well | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group `well=F-9_A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-044 | 56.495 | jendela | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `well`/`y_shk`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-045 | 9 | well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `well`/`y_shk`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-046 | 2.005 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `well`/`y_shk`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-047 | 3,55 | % | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `well`/`y_shk`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-048 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-049 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `SPPA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-050 | 2,84 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `TFLO_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-051 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-052 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-053 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-054 | 2,59 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-055 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-056 | 100,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `SPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-057 | 0,02 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-058 | 0,02 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-059 | 7.899 jendela / 146 positif / 1,85% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-10`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-060 | 5.405 jendela / 217 positif / 4,01% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-12`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-061 | 11.205 jendela / 760 positif / 6,78% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-062 | 6.484 jendela / 41 positif / 0,63% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-15A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-063 | 11.394 jendela / 259 positif / 2,27% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-15_S`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-064 | 7.140 jendela / 240 positif / 3,36% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-5`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-065 | 2.761 jendela / 267 positif / 9,67% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-7`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-066 | 1.851 jendela / 45 positif / 2,43% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-9`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-067 | 2.356 jendela / 30 positif / 1,27% | per well | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group `well=F-9_A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-068 | 5.555 | jendela | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `well`/`y_stuck`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-069 | 2 | well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `well`/`y_stuck`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-070 | 2.007 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `well`/`y_stuck`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-071 | 36,13 | % | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `well`/`y_stuck`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-072 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-073 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `SPPA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-074 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `TFLO_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-075 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-076 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-077 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-078 | 2,90 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-079 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-080 | 100,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `SPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-081 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-082 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-083 | 3.201 jendela / 432 positif / 13,50% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-084 | 2.354 jendela / 1.575 positif / 66,91% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group `well=F-9_A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-085 | 118.567 | jendela | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `well`/`y_stuck_onset`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-086 | 4 | well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `well`/`y_stuck_onset`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-087 | 1.975 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `well`/`y_stuck_onset`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-088 | 1,67 | % | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `well`/`y_stuck_onset`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-089 | 0,53 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-090 | 0,53 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `SPPA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-091 | 0,50 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `TFLO_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-092 | 3,06 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-093 | 0,13 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-094 | 0,18 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-095 | 1,03 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-096 | 0,13 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-097 | 0,29 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `SPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-098 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-099 | 0,15 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-100 | 4.216 jendela / 772 positif / 18,31% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group `well=F-10`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-101 | 95.925 jendela / 389 positif / 0,41% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-102 | 16.184 jendela / 311 positif / 1,92% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group `well=F-9`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-103 | 2.242 jendela / 503 positif / 22,44% | per well | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group `well=F-9_A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-104 | 52.509 | jendela | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `well`/`y_hyd`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-105 | 9 | well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `well`/`y_hyd`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-106 | 7.172 | jendela positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `well`/`y_hyd`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-107 | 13,66 | % | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `well`/`y_hyd`; skrip workspace `meas1.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-108 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `TQA_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-109 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `RPM_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-110 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `SWOB_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-111 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `HKLD_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-112 | 3,05 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `ROP_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-113 | 0,00 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `BPOS_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-114 | 0,15 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `depth_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-115 | 0,17 | % baris NaN | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` kolom `dbtm_mean`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel missing | TERUKUR |
| D0-116 | 7.571 jendela / 1.394 positif / 18,41% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-10`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-117 | 7.390 jendela / 1.426 positif / 19,30% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-12`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-118 | 10.401 jendela / 865 positif / 8,32% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-14`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-119 | 6.156 jendela / 698 positif / 11,34% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-15A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-120 | 8.355 jendela / 993 positif / 11,89% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-15_S`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-121 | 6.332 jendela / 621 positif / 9,81% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-5`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-122 | 2.482 jendela / 421 positif / 16,96% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-7`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-123 | 1.616 jendela / 423 positif / 26,18% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-9`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-124 | 2.206 jendela / 331 positif / 15,00% | per well | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group `well=F-9_A`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel per well | TERUKUR |
| D0-125 | 41.446 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-126 | 11,8 | jam | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-127 | 773.674 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-128 | 14 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-129 | 34 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-130 | 2 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-131 | 1 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-132 | 0,00 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-133 | 31,55 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-134 | 11,64 | % bin dengan STUCK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-135 | 25,22 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-136 | 180.958 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-137 | 1.209,1 | jam | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-138 | 2.081.567 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-139 | 11 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-140 | 26 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-141 | 16 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-142 | 7 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-143 | 11,03 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-144 | 13,11 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-145 | 96.698 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-146 | 1.151,6 | jam | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-147 | 1.648.026 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-148 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-149 | 32 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-150 | 8 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-151 | 2,31 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-152 | 13,55 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-153 | 4,44 | % bin dengan STUCK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-154 | 12,20 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-155 | 44.347 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-156 | 991,6 | jam | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-157 | 778.162 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-158 | 14 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-159 | 34 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-160 | 7 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-161 | 3 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-162 | 27,26 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-163 | 28,65 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-164 | 26,04 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-165 | 101.630 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-166 | 1.028,1 | jam | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-167 | 1.883.062 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-168 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-169 | 42 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-170 | 14 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-171 | 6 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-172 | 11,75 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-173 | 13,31 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-174 | 11,52 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-175 | 67.934 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-176 | 1.147,3 | jam | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-177 | 1.286.967 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-178 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-179 | 34 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-180 | 6 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-181 | 3 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-182 | 10,12 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-183 | 15,18 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-184 | 11,58 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-185 | 34.533 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-186 | 1.171,7 | jam | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-187 | 547.500 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-188 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-189 | 31 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-190 | 7 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-191 | 5 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-192 | 8,88 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-193 | 6,62 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-194 | 25.460 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-195 | 1.142,6 | jam | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-196 | 457.545 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-197 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-198 | 33 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-199 | 6 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-200 | 5 | gap > 5 menit | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-201 | 4,67 | % bin dengan VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-202 | 13,87 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-203 | 4,22 | % bin dengan STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-204 | 9,67 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-205 | 27.282 | bin 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-206 | 911,1 | jam | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-207 | 419.706 | baris mentah | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-208 | 13 | baris/menit (median) | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-209 | 31 | baris/menit (p95) | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-210 | 1 | gap > 1 menit | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas1.py` | 2026-10-27 | RND_D0 §2 tabel bins | TERUKUR |
| D0-211 | 8,64 | % bin dengan SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `shkrsk_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-212 | 8,63 | % bin dengan STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-213 | 2,92 | % bin dengan CRPM | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `crpm_n`; `meas1.py` | 2026-10-27 | RND_D0 §1 tabel ketersediaan kanal | TERUKUR |
| D0-214 | 85.921 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-215 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-216 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-217 | 7 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-218 | 17.692 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-219 | 14,74 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-220 | 83.557 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-221 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-222 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-223 | 7 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-224 | 752 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-225 | 0,63 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-226 | 86.306 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-227 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-228 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-229 | 6 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-230 | 17.692 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-231 | 14,74 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-232 | 45.927 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-233 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-234 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-235 | 66 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-236 | 3.828 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-237 | 3,19 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-238 | 45.712 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-239 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-240 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-241 | 65 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-242 | 3.827 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-243 | 3,19 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-244 | 85.921 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-245 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-246 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-247 | 7 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-248 | 17.692 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-249 | 14,74 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-250 | 74.219 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-251 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-252 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-253 | 6 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-254 | 12.508 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-255 | 10,42 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-256 | 15.184 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-257 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-258 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-259 | 35 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-260 | 2.340 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-261 | 1,95 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9_A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-262 | 405.567 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-263 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-264 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-265 | 13 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-266 | 110.735 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-267 | 151,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `HKLD`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-268 | 3.659 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-269 | 48,038 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-270 | 0,0208 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-271 | 1.064 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-272 | 213 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-273 | 2,84 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-274 | 405.563 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-275 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-276 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-277 | 13 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-278 | 110.735 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-279 | 151,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `SPPA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-280 | 405.567 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-281 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-282 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-283 | 13 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-284 | 110.735 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-285 | 151,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `ROP`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-286 | 405.488 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-287 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-288 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-289 | 14 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-290 | 105.988 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-291 | 145,00 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-292 | 405.567 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-293 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-294 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-295 | 13 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-296 | 110.735 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-297 | 151,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `TFLO`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-298 | 2.769 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-299 | 47,952 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-300 | 0,0209 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-301 | 873 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-302 | 144 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-303 | 1,92 | jam | RUN-KITA | `data/volve/witsml_parsed/F-7.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-304 | 865.089 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-305 | 4,061 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-306 | 0,2462 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-307 | 27 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-308 | 44.649 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-309 | 50,37 | jam | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-310 | 46.529 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-311 | 3,974 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-312 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-313 | 760 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-314 | 6.789 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-315 | 7,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-316 | 53.738 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-317 | 3,974 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-318 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-319 | 961 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-320 | 6.785 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-321 | 7,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-322 | 43.565 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-323 | 3,974 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-324 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-325 | 728 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-326 | 6.789 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-327 | 7,49 | jam | RUN-KITA | `data/volve/witsml_parsed/F-5.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-328 | 320.609 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-329 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-330 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-331 | 8 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-332 | 74.730 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-333 | 102,23 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-334 | 13.817 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-335 | 17,971 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-336 | 0,0556 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-337 | 60 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-338 | 1.929 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-339 | 9,63 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-340 | 9.875 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-341 | 17,971 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-342 | 0,0556 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-343 | 46 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-344 | 1.928 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-345 | 9,62 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-346 | 6.475 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-347 | 3,974 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-348 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-349 | 10 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-350 | 1.931 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-351 | 2,13 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-352 | 5.728 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-353 | 3,974 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-354 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-355 | 10 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-356 | 1.929 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-357 | 2,13 | jam | RUN-KITA | `data/volve/witsml_parsed/F-9.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-358 | 69.192 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-359 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-360 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-361 | 326 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-362 | 3.321 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-363 | 2,77 | jam | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-364 | 258.441 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-365 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-366 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-367 | 21 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-368 | 55.723 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-369 | 46,44 | jam | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-370 | 64.295 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-371 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-372 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-373 | 324 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-374 | 3.324 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-375 | 2,77 | jam | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-376 | 9.545 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-377 | 30,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-378 | 0,0333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-379 | 91 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-380 | 402 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-381 | 3,35 | jam | RUN-KITA | `data/volve/witsml_parsed/F-10.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-382 | 169.185 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-383 | 3,024 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-384 | 0,3307 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-385 | 8.616 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-386 | 7.834 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-387 | 6,58 | jam | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-388 | 1.667.867 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-389 | 5,011 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-390 | 0,1996 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-391 | 76 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-392 | 97.707 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-393 | 136,00 | jam | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-394 | 25.970 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-395 | 59,961 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-396 | 0,0167 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-397 | 9.591 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-398 | 467 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-399 | 7,78 | jam | RUN-KITA | `data/volve/witsml_parsed/F-12.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-400 | 1.226.483 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-401 | 4,925 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-402 | 0,2030 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-403 | 40 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-404 | 163.117 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-405 | 223,15 | jam | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-406 | 21.643 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-407 | 47,952 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-408 | 0,0209 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-409 | 5.408 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-410 | 2.959 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-411 | 39,41 | jam | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-412 | 23.110 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-413 | 20,995 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-414 | 0,0476 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-415 | 4.784 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-416 | 2.212 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-417 | 12,90 | jam | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-418 | 5.147 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-419 | 50,976 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-420 | 0,0196 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-421 | 74 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-422 | 298 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-423 | 4,22 | jam | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `STUCK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-424 | 2.247 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-425 | 60,048 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-426 | 0,0167 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-427 | 1.550 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-428 | 332 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-429 | 5,54 | jam | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-430 | 50.794 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-431 | 3,975 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-432 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-433 | 4.608 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-434 | 3.972 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-435 | 4,39 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-436 | 202.903 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-437 | 3,024 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-438 | 0,3307 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-439 | 169 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-440 | 19.446 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-441 | 16,33 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-442 | 50.413 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-443 | 3,975 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-444 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-445 | 4.571 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-446 | 3.974 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-447 | 4,39 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-448 | 52.126 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-449 | 3,975 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-450 | 0,2516 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-451 | 5.168 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-452 | 3.974 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-453 | 4,39 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15A.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-454 | 1.537.360 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-455 | 4,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-456 | 0,2500 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-457 | 24 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-458 | 160.156 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-459 | 177,95 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `TQA`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-460 | 141.114 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-461 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-462 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-463 | 4.125 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-464 | 4.138 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-465 | 3,45 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `VIBLAT_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-466 | 137.170 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-467 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-468 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-469 | 4.138 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-470 | 3,45 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `CRPM_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-471 | 152.923 | sampel | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-472 | 3,000 | detik (median dt) | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-473 | 0,3333 | Hz | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-474 | 5.176 | gap > 60 detik | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-475 | 4.139 | sampel berurutan | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-476 | 3,45 | jam | RUN-KITA | `data/volve/witsml_parsed/F-15_S.csv` kolom `SHKRSK_RT`; `meas2.py` | 2026-10-27 | RND_D0 §2 tabel cadence | TERUKUR |
| D0-477 | 2.132 | menit state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-478 | 160 | episode STUCK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-479 | 320 | perubahan state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-480 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-481 | 4,3 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-482 | 30 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-483 | 23 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-484 | 46 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-485 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-486 | 0 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-487 | NA | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-488 | 9.730 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-489 | 94,78 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-10.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-490 | 202 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-491 | 166 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-492 | 332 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-493 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-494 | 1,1 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-495 | 77.604 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-496 | 99,89 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-12.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-497 | 339 | menit state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-498 | 87 | episode STUCK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-499 | 174 | perubahan state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-500 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-501 | 1,9 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-502 | 160 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-503 | 122 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-504 | 244 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-505 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-506 | 1,1 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-507 | 712 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-508 | 200 | episode VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-509 | 400 | perubahan state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-510 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-511 | 2,0 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-512 | 27.062 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-513 | 98,81 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-14.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-514 | 10 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-515 | 20 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-516 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-517 | 1.096 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-518 | 553 | episode VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-519 | 1.106 | perubahan state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-520 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-521 | 2,8 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-522 | 11.271 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-523 | 97,51 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-15A.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-524 | 46 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-525 | 31 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-526 | 62 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-527 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-528 | 1.083 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-529 | 297 | episode VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-530 | 594 | perubahan state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-531 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-532 | 1,9 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-533 | 39.488 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-534 | 98,90 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-15_S.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-535 | 40 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-536 | 37 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-537 | 74 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-538 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-539 | 1.009 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-540 | 152 | episode VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-541 | 304 | perubahan state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-542 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-543 | 6,5 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-544 | 27.679 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-545 | 98,46 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-5.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-546 | 174 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-547 | 80 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-548 | 160 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-549 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-550 | 1,1 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-551 | 11.632 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-552 | 99,50 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-7.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-553 | 135 | menit state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-554 | 61 | episode STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-555 | 122 | perubahan state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-556 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-557 | 1,4 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-558 | 16 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-559 | 10 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-560 | 20 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-561 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-562 | 1,1 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-563 | 989 | menit state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-564 | 36 | episode VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-565 | 72 | perubahan state VIBLAT | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-566 | 1,1 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-567 | 7,6 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz` kolom `viblat_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-568 | 8.991 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-569 | 96,08 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-9.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-570 | 1.235 | menit state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-571 | 110 | episode STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-572 | 220 | perubahan state STUCK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-573 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-574 | 2,2 | menit (episode terpanjang) | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `stuck_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-575 | 6 | menit state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-576 | 4 | episode SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-577 | 8 | perubahan state SHKRSK | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-578 | 1,0 | menit (median episode) | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz` kolom `shkrsk_max`; `meas5.py` | 2026-10-27 | RND_D0 §3 tabel state | TERUKUR |
| D0-579 | 12.014 | menit baseline bersih gabungan | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-580 | 95,47 | % menit bersih | RUN-KITA | `scratch/v9_d1/bins/F-9_A.csv.gz`; `meas5.py` | 2026-10-27 | RND_D0 §5 baseline gabungan | TERUKUR |
| D0-581 | 55 | onset (ffill) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9.onsets_ffill | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-582 | 61 | onset (strict) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9.onsets_strict | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-583 | 55 | onset skorable | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9.onsets_scorable | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-584 | 311 | jendela positif | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9.positives | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-585 | 16.184 | baris eligible | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9.eligible_rows | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-586 | 72 | onset (ffill) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9_A.onsets_ffill | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-587 | 72 | onset (strict) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9_A.onsets_strict | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-588 | 72 | onset skorable | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9_A.onsets_scorable | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-589 | 503 | jendela positif | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9_A.positives | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-590 | 2.242 | baris eligible | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-9_A.eligible_rows | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-591 | 93 | onset (ffill) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-10.onsets_ffill | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-592 | 111 | onset (strict) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-10.onsets_strict | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-593 | 93 | onset skorable | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-10.onsets_scorable | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-594 | 772 | jendela positif | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-10.positives | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-595 | 4.216 | baris eligible | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-10.eligible_rows | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-596 | 61 | onset (ffill) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-14.onsets_ffill | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-597 | 81 | onset (strict) | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-14.onsets_strict | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-598 | 61 | onset skorable | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-14.onsets_scorable | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-599 | 389 | jendela positif | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-14.positives | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-600 | 95.925 | baris eligible | RUN-KITA | `scratch/v9_d1/v9_d1_04_qc.json` wells.F-14.eligible_rows | 2026-10-27 | RND_D0 §4 tabel onset | TERUKUR |
| D0-601 | 124 | episode | RUN-KITA | `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` meta.n_episodes | 2026-10-27 | RND_D0 §4 tabel hyd | TERUKUR |
| D0-602 | 30 | jendela positif | RUN-KITA | `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` test.fold.pos | 2026-10-27 | RND_D0 §4 tabel hyd | TERUKUR |
| D0-603 | 0,370 | % | RUN-KITA | `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` test.fold.prev | 2026-10-27 | RND_D0 §4 tabel hyd | TERUKUR |
| D0-604 | 372 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-605 | 34 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-606 | 1.989 | baris | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-607 | 1.124 | positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-608 | 886 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-609 | 71 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-610 | 6.482 | baris | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-611 | 1.543 | positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-612 | 2.523 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-613 | 70 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-614 | 10.903 | baris | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-615 | 1.532 | positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-616 | 548 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-617 | 41 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-618 | 4.548 | baris | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-619 | 1.230 | positif | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-620 | 1.549 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-621 | 28 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-622 | 7.133 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-623 | 161 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-624 | 305 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-625 | 22 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-626 | 4.293 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-627 | 83 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-628 | 1.359 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-629 | 13 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-630 | 5.455 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-631 | 75 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-632 | 2.808 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-633 | 7 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-634 | 6.020 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-635 | 31 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-636 | 681 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-637 | 27 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-638 | 5.342 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-639 | 85 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-640 | 676 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-641 | 19 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-642 | 4.714 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-643 | 102 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-644 | 185 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-645 | 1 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-646 | 982 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-647 | 3 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-648 | 354 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-649 | 3 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-650 | 1.126 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-651 | 12 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-652 | 168 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-653 | 12 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-654 | 841 | baris | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-655 | 55 | positif | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-656 | 1.718 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-657 | 15 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-658 | 7.899 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-659 | 146 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-660 | 696 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-661 | 20 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-662 | 5.405 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-663 | 217 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-664 | 1.376 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-665 | 62 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-666 | 11.205 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-667 | 760 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-668 | 1.800 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-669 | 6 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-670 | 6.484 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-671 | 41 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-672 | 2.979 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-673 | 25 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-674 | 11.394 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-675 | 259 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-676 | 638 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-677 | 30 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-678 | 7.140 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-679 | 240 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-680 | 448 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-681 | 14 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-682 | 2.761 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-683 | 267 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-684 | 486 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-685 | 6 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-686 | 1.851 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-687 | 45 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-688 | 1.375 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-689 | 3 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-690 | 2.356 | baris | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-691 | 30 | positif | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-692 | 573 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-693 | 20 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-694 | 3.201 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-695 | 432 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-696 | 74 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-697 | 41 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-698 | 2.354 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-699 | 1.575 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-700 | 734 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-701 | 67 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-702 | 4.216 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-703 | 772 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-704 | 28.820 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-705 | 28 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-706 | 95.925 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-707 | 389 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-708 | 7.248 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-709 | 16 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-710 | 16.184 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-711 | 311 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-712 | 300 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-713 | 37 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-714 | 2.242 | baris | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-715 | 503 | positif | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-716 | 1.329 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-717 | 23 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-718 | 7.571 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-719 | 1.394 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-10; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-720 | 393 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-721 | 92 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-722 | 7.390 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-723 | 1.426 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-12; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-724 | 1.063 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-725 | 58 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-726 | 10.401 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-727 | 865 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-14; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-728 | 1.902 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-729 | 33 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-730 | 6.156 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-731 | 698 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-732 | 1.027 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-733 | 64 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-734 | 8.355 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-735 | 993 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-15_S; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-736 | 707 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-737 | 40 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-738 | 6.332 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-739 | 621 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-5; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-740 | 229 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-741 | 28 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-742 | 2.482 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-743 | 421 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-7; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-744 | 324 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-745 | 28 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-746 | 1.616 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-747 | 423 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-748 | 816 | menit baseline bersih | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-749 | 24 | segmen positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-750 | 2.206 | baris | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-751 | 331 | positif | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` group well=F-9_A; `meas5.py` | 2026-10-27 | RND_D0 §5 tabel baseline | TERUKUR |
| D0-752 | 198.928 | baris | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-753 | 18 | kolom | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-754 | 7 | well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-755 | 134.013 | baris | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` label='normal' | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-756 | 49.732 | baris | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` label='high_MSE_bit_wear' | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-757 | 15.183 | baris | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` label='low_ROP_efficiency' | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-758 | 25,00 | % | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` label='high_MSE_bit_wear' | 2026-10-27 | RND_D0 §6.1 | TERUKUR |
| D0-759 | 13.746 baris / 182 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 0 N-NA_F-9_Ad.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-760 | 6.389 baris / 0 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 1 N-S_F-7d.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-761 | 47.645 baris / 4.918 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 2 N-SH_F-14d.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-762 | 53.041 baris / 7.622 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 3 N-SH-F-15d.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-763 | 51.708 baris / 28.051 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 4 N-SH_F-15Sd.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-764 | 18.548 baris / 8.959 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 5 N-SH-F-5d.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-765 | 7.851 baris / 0 high_MSE | per well | RUN-KITA | `data/USROP_labeled.csv`; `meas3.py` well='USROP_A 6 N-SH_F-9d.csv' | 2026-10-27 | RND_D0 §6.1 tabel per well | TERUKUR |
| D0-766 | 469 | jendela | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-767 | 27 | fitur | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-768 | 4 | alat | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-769 | 240 | jendela y=1 | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; `meas3.py` y=1 | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-770 | 229 | jendela y=0 | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; `meas3.py` y=0 | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-771 | 9 | well diperiksa | RUN-KITA | `data/volve/witsml_parsed/*.qc.json`; `meas4.py` | 2026-10-27 | RND_D0 §6.3 | TERUKUR |
| D0-772 | 419.748 | baris | RUN-KITA | `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (wc -l) dan `meas4.py` | 2026-10-27 | RND_D0 §6.3 | TERUKUR |
| D0-773 | 13 | kolom MudPit Volume Average | RUN-KITA | `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` header; `meas4.py` | 2026-10-27 | RND_D0 §6.3 | TERUKUR |
| D0-774 | 0 | kanal GAINLOSSTOT ditemukan | RUN-KITA | `data/volve/witsml_parsed/*.qc.json` 9 well; `meas4.py` | 2026-10-27 | RND_D0 §6.3 | TERUKUR |
| D0-775 | 10 | menit (H) | KONVENSI | `code/v9_d1_02_rig_windows.py` H=10 dan `code/v9_d1_04_stuck_k2.py` H=10 | 2026-10-27 | RND_D0 §4 horizon | TERUKUR |
| D0-776 | 32,17405 | ft/s2 (1 g) | STANDAR | standar gravitasi 9,80665 m/s2 x 3,280839895 ft/m (BIPM: 9,80665 m/s2) | 2026-10-27 | RND_D0 §3 ambang VIBLAT | TERUKUR |
| D0-777 | 0,1667 | Hz (Nyquist dari 0,3333 Hz) | DERIVASI | turunan dari cadence terukur `meas2.py` (median dt 3,0 dtk) | 2026-10-27 | RND_D0 §2 tafsir | TERUKUR |
| D0-778 | DOI 10.1109/TSP.2013.2288675 | DOI | JURNAL | Dragomiretskiy 2014, divertifikasi lewat https://doi.org/10.1109/TSP.2013.2288675 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-779 | DOI 10.1098/rspa.1998.0193 | DOI | JURNAL | Huang 1998, divertifikasi lewat https://api.crossref.org/works/10.1098/rspa.1998.0193 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-780 | DOI 10.1109/5.18626 | DOI | JURNAL | Rabiner 1989, divertifikasi lewat https://api.crossref.org/works/10.1109/5.18626 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-781 | DOI 10.1111/j.2517-6161.1972.tb00899.x | DOI | JURNAL | Cox 1972, divertifikasi lewat https://api.crossref.org/works/10.1111/j.2517-6161.1972.tb00899.x | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-782 | DOI 10.1214/08-AOAS169 | DOI | JURNAL | Ishwaran 2008, divertifikasi lewat https://api.crossref.org/works/10.1214/08-AOAS169 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-783 | DOI 10.1109/ICDM.2008.17 | DOI | JURNAL | Liu 2008, divertifikasi lewat https://api.crossref.org/works/10.1109/ICDM.2008.17 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-784 | DOI 10.1093/biomet/41.1-2.100 | DOI | JURNAL | Page 1954, divertifikasi lewat https://api.semanticscholar.org/graph/v1/paper/DOI:10.1093/biomet/41.1-2.100 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-785 | DOI 10.1016/j.advengsoft.2013.12.007 | DOI | JURNAL | Mirjalili 2014, divertifikasi lewat https://api.semanticscholar.org/graph/v1/paper/DOI:10.1016/j.advengsoft.2013.12.007 | 2026-10-27 | RND_D0 §8 rujukan | TERVERIFIKASI |
| D0-786 | 3,8 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-787 | 12,4 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/ssi.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-788 | 12,4 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/shk.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-789 | 7,1 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/stuck_k1.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-790 | 10,2 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/stuck_k2.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-791 | 12,4 hari | hari | RUN-KITA | `scratch/v9_d1/datasets/hyd_ki.csv.gz` selisih `ts_bin`; `build_doc.py` | 2026-10-27 | RND_D0 §1 tabel engine | TERUKUR |
| D0-792 | 2007-11-04T13:00:13.968Z | timestamp ISO | RUN-KITA | `data/volve/witsml_parsed/F-14.csv` kolom `timestamp` baris 1; `probe_ts.py` | 2026-10-27 | RND_D0 §1 catatan waktu | TERUKUR |
| D0-793 | 0 | tanggal absolut dari ts_bin | BELUM-TERUKUR | `ts_bin` = detik relatif tanpa titik nol epoch, sehingga tanggal absolut per jendela belum dipetakan | 2026-10-27 | RND_D0 §1 catatan waktu | BELUM |
| D0-794 | 120 | jendela | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv` group tool=T01; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-795 | 112 | jendela | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv` group tool=T02; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-796 | 121 | jendela | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv` group tool=T03; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-797 | 116 | jendela | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv` group tool=T04; `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |
| D0-798 | 2 | run kondisi | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv` kolom `run` (unique); `meas3.py` | 2026-10-27 | RND_D0 §6.2 | TERUKUR |

---

## Bagian R5: deteksi perubahan dan anomali tanpa label (kartu t_56d8d11d)

Tanggal akses seluruh baris: 2026-10-27 (WIB). Kelas sumber mengikuti plan §2 (`STANDAR` > `JURNAL` > `RUN-KITA` > `KONVENSI` > `BELUM-TERUKUR`). Baris RUN-KITA menyebut berkas dan perintah yang dapat dijalankan ulang; baris KONVENSI menyebut dokumen yang menetapkannya; skor 1 s.d. 5 dicatat sebagai KONVENSI karena itu penilaian rekayasa, bukan pengukuran.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R5-001 | 52.509 | baris | RUN-KITA | `scratch/rnd_r5/grid_structure.json` (`n_rows`), perintah `python3 scratch/rnd_r5/grid_check.py` | 2026-10-27 | RND_R5 §2 | TERUKUR |
| R5-002 | 9 | well | RUN-KITA | `scratch/rnd_r5/grid_structure.json` (`per_well` berisi 9 kunci), perintah `grid_check.py` | 2026-10-27 | RND_R5 §2.1 | TERUKUR |
| R5-003 | 50 | kolom | RUN-KITA | `scratch/rnd_r5/probe_env.py` mengeluarkan `NCOL 50` untuk `scratch/v9_d1/datasets/hyd_ki.csv.gz` | 2026-10-27 | RND_R5 §2 | TERUKUR |
| R5-004 | 1 | menit per selisih satu | RUN-KITA | `grid_structure.json` F-10 `delta_top5_seconds` = [1, 7483] dari 7.570 pasangan; bukti `ts_bin` = indeks menit, bukan detik | 2026-10-27 | RND_R5 §2.0 | TERUKUR |
| R5-005 | 11.248 | menit (187,5 jam) | RUN-KITA | `grid_structure.json` F-10 `ts_min` 20672177 dan `ts_max` 20683425, selisih 11.248 | 2026-10-27 | RND_R5 §2.0 | TERUKUR |
| R5-006 | 5 | dari 9 well | RUN-KITA | `scratch/rnd_r5/drift_measured_v2.json` (`summary.n_wells_dipakai`), perintah `python3 scratch/rnd_r5/measure_drift_v2.py` | 2026-10-27 | RND_R5 §2.1 | TERUKUR |
| R5-007 | 257 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-008 | 358 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-009 | 284 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-010 | 297 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-011 | 361 | menit baseline bersih | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.baseline_minutes` | 2026-10-27 | RND_R5 §2.1, §2.2 | TERUKUR |
| R5-012 | 297 | menit (median baseline) | RUN-KITA | `drift_measured_v2.json` `summary.baseline_minutes_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-013 | 16,81 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-014 | 4,02 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-015 | 10,14 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-016 | 9,70 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.cusum_far_24h` dan `summary.cusum_far24_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-017 | 7,98 | episode CUSUM per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.cusum_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-018 | 0,00 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-10.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-019 | 8,04 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-14.ph_far_24h` dan `summary.ph_far24_median` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-020 | 10,14 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15A.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-021 | 4,85 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-15_S.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-022 | 11,97 | episode PH per 24 jam | RUN-KITA | `drift_measured_v2.json` `per_well.F-9_A.ph_far_24h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-023 | 0,987 | autokorelasi lag-1 (median) | RUN-KITA | `drift_measured_v2.json` `summary.ac1_median`; rentang `ac1_min` 0,9765 dan `ac1_max` 0,9954 | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-024 | 3 | dari 5 well | RUN-KITA | `drift_measured_v2.json` `summary.wells_half2_bersih_pada_h_kalibrasi` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-025 | 40 / 4 / 60 / 60 / 60 | ambang h CUSUM (sigma) | RUN-KITA | `drift_measured_v2.json` `per_well.*.half1_h_calibrated` untuk F-10, F-14, F-15A, F-15_S, F-9_A | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-026 | 0,986 | statistik D KS (median) | RUN-KITA | `drift_measured_v2.json` `summary.ks_between_well_D_median`; min 0,723 dan maks 1,000 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-027 | 10 | dari 10 pasangan, p < 0,05 | RUN-KITA | `drift_measured_v2.json` `summary.ks_between_well_p_lt_0_05` = 10 dan `ks_between_well_pairs` = 10 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-028 | 0,211 | statistik D KS dalam well (median) | RUN-KITA | `drift_measured_v2.json` `summary.ks_within_well_D_median`; F-14 `D` 0,9777 | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-029 | 4 | dari 5 well, p < 0,05 | RUN-KITA | `drift_measured_v2.json` `summary.ks_within_well_p_lt_0_05` | 2026-10-27 | RND_R5 §2.3 | TERUKUR |
| R5-030 | 0,7523 s.d. 1,0000 | recall horizon 10 menit (CUSUM, deret penuh) | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_recall_h10_full_series` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-031 | 0,2387 s.d. 0,9069 | recall horizon 10 menit (PH, deret penuh) | RUN-KITA | `drift_measured_v2.json` `per_well.*.ph_recall_h10_full_series` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-032 | 52,293 s.d. 60,000 | menit alarm CUSUM per jam di luar baseline | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_alarm_rate_outside_per_hour` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-033 | 4.281 | positif `y_hyd` pada 5 well | RUN-KITA | `drift_measured_v2.json` `summary.total_positives` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-034 | 0,5 sigma | parameter k CUSUM | KONVENSI | bentuk dari Page 1954 (DOI 10.1093/biomet/41.1-2.100); nilai 0,5 sigma dipilih tim, di `scratch/rnd_r5/measure_drift_v2.py` baris `K_SIGMA` | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (bentuk) |
| R5-035 | 5 sigma | parameter h CUSUM | KONVENSI | dipilih tim, `measure_drift_v2.py` baris `H_SIGMA`; alasan memakai ambang konvensional adalah untuk menunjukkan bahwa nilai buku teks gagal pada data nyata | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (konvensi) |
| R5-036 | 0,005 sigma dan 50 sigma | parameter delta dan lambda Page-Hinkley | KONVENSI | bentuk dari Hinkley 1971 (DOI 10.1093/biomet/58.3.509); nilai di `measure_drift_v2.py` baris `PH_DELTA` dan `PH_LAMBDA` | 2026-10-27 | RND_R5 §2, §2.2 | TERVERIFIKASI (bentuk) |
| R5-037 | 240 | menit (panjang minimum baseline bersih) | KONVENSI | `measure_drift_v2.py` baris `MIN_BASE`; dipilih agar setara 4 jam operasi dan tetap menyisakan 5 well | 2026-10-27 | RND_R5 §2.1 | TERVERIFIKASI (konvensi) |
| R5-038 | 30 | menit (jarak penggabungan episode alarm) | KONVENSI | `measure_drift_v2.py` baris `MERGE_GAP` | 2026-10-27 | RND_R5 §2.2 | TERVERIFIKASI (konvensi) |
| R5-039 | 10 | menit (horizon label onset) | KONVENSI | `measure_drift_v2.py` baris `HORIZON`; sama dengan horizon yang dipakai V9 (`scratch/v9_i1/v9_i1_RESULTS.json`) | 2026-10-27 | RND_R5 §2.4 | TERVERIFIKASI (konvensi) |
| R5-040 | 6 | episode alarm maksimum per 24 jam | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 gate A (FAR rig) | 2026-10-27 | RND_R5 §2.2, §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-041 | 32 | fitur | RUN-KITA | `scratch/rnd_r5/anomaly_unsup.json` `meta.n_fitur`; 8 kanal x 4 statistik, daftar di `meta.fitur` | 2026-10-27 | RND_R5 §2.5 | TERUKUR |
| R5-042 | 2 | well dipakai pada uji anomali | RUN-KITA | `anomaly_unsup.json` `summary.n_well_dipakai` (F-10, F-15_S); perintah `scratch/rnd_r5/.venv/bin/python scratch/rnd_r5/anomaly_unsup.py` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-043 | 0,01 | contamination | KONVENSI | `anomaly_unsup.py` baris `CONTAM`; dipilih agar sesuai laju alarm 1% yang diminta | 2026-10-27 | RND_R5 §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-044 | 1.500 | baris batas fit | KONVENSI | `anomaly_unsup.py` baris `FIT_CAP` | 2026-10-27 | RND_R5 §2.5.1 | TERVERIFIKASI (konvensi) |
| R5-045 | 0,0109 | laju alarm baseline Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-046 | 11,21 dan 9,70 | FAR per 24 jam Isolation Forest (F-10, F-15_S) | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.iforest.far_per_24h` dan `per_well.F-15_S.iforest.far_per_24h` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-047 | 0,6131 | recall horizon 10 menit Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.recall_h10_median`; per well 0,3793 dan 0,8470 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-048 | 0,2240 | presisi alarm-menit Isolation Forest (median) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-049 | 1.353 dan 6.096 | menit alarm total Isolation Forest | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.iforest.alarm_menit_total` dan `per_well.F-15_S.iforest.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-050 | 0,0089 | laju alarm baseline LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-051 | 0,9970 | recall horizon 10 menit LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.recall_h10_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-052 | 5.920 dan 7.896 | menit alarm total LOF | RUN-KITA | `anomaly_unsup.json` `per_well.*.lof.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-053 | 0,2032 | presisi alarm-menit LOF (median) | RUN-KITA | `anomaly_unsup.json` `summary.lof.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-054 | 0,0665 | laju alarm baseline One-Class SVM (median) | RUN-KITA | `anomaly_unsup.json` `summary.ocsvm.laju_alarm_baseline_median`; rentang 0,0623 s.d. 0,0707 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-055 | 11,21 dan 14,55 | FAR per 24 jam One-Class SVM | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.ocsvm.far_per_24h` dan `per_well.F-15_S.ocsvm.far_per_24h` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-056 | 0,0109 | laju alarm baseline autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.laju_alarm_baseline_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-057 | 1,0000 | recall horizon 10 menit autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.recall_h10_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-058 | 6.154 dan 8.006 | menit alarm total autoencoder | RUN-KITA | `anomaly_unsup.json` `per_well.*.ae.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-059 | 0,2011 | presisi alarm-menit autoencoder (median) | RUN-KITA | `anomaly_unsup.json` `summary.ae.presisi_menit_median` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-060 | 0,5000 dan 1,0000 | laju alarm pada baseline well lain (median dan maksimum) | RUN-KITA | `anomaly_unsup.json` `summary.iforest.transfer_laju_alarm_median` 0,5 dan `summary.lof.transfer_laju_alarm_median` 1,0; OCSVM dan AE juga 1,0; `transfer_pasangan` = 2 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-061 | 2 dan 3 | titik diskord matrix profile | RUN-KITA | `anomaly_unsup.json` `per_well.F-10.matrix_profile.titik_diskord` = 2 dan `per_well.F-15_S.matrix_profile.titik_diskord` = 3; jendela 60 menit | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-062 | 0 | well dipakai pada percobaan pertama | RUN-KITA | `scratch/rnd_r5/drift_far_measured.json` `summary.n_wells_dipakai` = 0; **artefak satuan** (langkah 60 pada indeks menit), tidak dipakai sebagai bukti | 2026-10-27 | RND_R5 §2.0 | TERUKUR (hasil dibatalkan) |
| R5-063 | 6 s.d. 28 | menit blok maksimum pada percobaan pertama | RUN-KITA | `drift_far_measured.json` `skipped.*.block_max_minutes`; artefak satuan yang sama, dicatat sebagai kesalahan yang sudah dikoreksi | 2026-10-27 | RND_R5 §2.0 | TERUKUR (artefak) |
| R5-064 | 1 s.d. 5 | skor kriteria data, biaya, interpretasi | KONVENSI | penilaian rekayasa tim R&D, kriteria dinyatakan di RND_R5 §1 dan §3.3; bukan hasil pengukuran | 2026-10-27 | RND_R5 §1, §3.3, §5 | TERVERIFIKASI (konvensi) |
| R5-065 | 0,3 / 0,3 / 0,4 | bobot skor gabungan (data / biaya / interpretasi) | KONVENSI | RND_R5 §5; bobot dinyatakan terbuka agar dapat dibantah | 2026-10-27 | RND_R5 §5 | TERVERIFIKASI (konvensi) |
| R5-066 | 124 | episode onset hyd K-ii (1 wellbore) | RUN-KITA | dikutip dari handoff kartu `t_34c20c78` (`onsets.hyd_K_ii`) dan `docs/RND_D0_DATA_FEASIBILITY.md`; tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.1 | TERUKUR (kutipan) |
| R5-067 | 78,7 | persen jendela sign-flip hyd K-ii | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 (6.377 dari 8.107 jendela); tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.1 | TERUKUR (kutipan) |
| R5-068 | 0,119 s.d. 0,984 | AUPRC persistence bit_wear K-1 | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1; tidak dihitung ulang di R5 | 2026-10-27 | RND_R5 §4.2 | TERUKUR (kutipan) |
| R5-069 | 20 s.d. 36 | detik TLead tool_wear K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 dan `docs/RND_P0_PARAMETER.md`; 4 alat | 2026-10-27 | RND_R5 §0, §1.1 | TERUKUR (kutipan) |
| R5-070 | 0,50 | presisi biner tool_wear K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` tabel §1 (4 FP di alat baru) | 2026-10-27 | RND_R5 §1.1 | TERUKUR (kutipan) |
| R5-071 | 0,3333 | Hz laju sampel kanal maksimum | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` tabel sampling; mengikat keputusan menolak metode yang butuh laju lebih tinggi | 2026-10-27 | RND_R5 §0 | TERUKUR (kutipan) |
| R5-072 | 119 | rasio sebar FAR ambang RF vib antar well | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 (τ0,5 FAR 4,1 s.d. 496); alasan menolak ambang global | 2026-10-27 | RND_R5 §1.1 | TERUKUR (kutipan) |

### Rujukan R5 yang diverifikasi (JURNAL)

Perintah: `bash scratch/rnd_r5/dois.sh`; hasil: `scratch/rnd_r5/doi_check.txt`. Status "TERVERIFIKASI" berarti rekaman Crossref cocok pada penulis pertama, tahun, judul, wadah, dan halaman; halaman penerbit mengembalikan 403 (bot wall) atau 202 dari host ini, sehingga isi penuh tidak dibuka.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R5-073 | Page 1954 | rujukan | JURNAL | Page, E. S. (1954). Continuous inspection schemes. Biometrika 41(1-2), 100-115. DOI 10.1093/biomet/41.1-2.100 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-074 | Hinkley 1971 | rujukan | JURNAL | Hinkley, D. V. (1971). Inference about the change-point from cumulative sum tests. Biometrika 58(3), 509-523. DOI 10.1093/biomet/58.3.509 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-075 | Adams dan MacKay 2007 | rujukan | JURNAL | Adams, R. P., MacKay, D. J. C. (2007). Bayesian Online Changepoint Detection. arXiv:0710.3742 (arXiv API OK, HTTP 200) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-076 | Bifet dan Gavaldà 2007 | rujukan | JURNAL | Bifet, A., Gavaldà, R. (2007). Learning from Time-Changing Data with Adaptive Windowing. Proc. SIAM Int. Conf. Data Mining, 443-448. DOI 10.1137/1.9781611972771.42 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-077 | Liu dkk. 2008 | rujukan | JURNAL | Liu, F. T., Ting, K. M., Zhou, Z.-H. (2008). Isolation Forest. ICDM 2008, 413-422. DOI 10.1109/ICDM.2008.17 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-078 | Breunig dkk. 2000 | rujukan | JURNAL | Breunig, M. M., Kriegel, H.-P., Ng, R. T., Sander, J. (2000). LOF: Identifying Density-Based Local Outliers. Proc. ACM SIGMOD, 93-104. DOI 10.1145/342009.335388 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-079 | Schölkopf dkk. 2001 | rujukan | JURNAL | Schölkopf, B., Platt, J. C., Shawe-Taylor, J., Smola, A. J., Williamson, R. C. (2001). Estimating the Support of a High-Dimensional Distribution. Neural Computation 13(7), 1443-1471. DOI 10.1162/089976601750264965 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-080 | Yeh dkk. 2016 | rujukan | JURNAL | Yeh, C.-C. M., Zhu, Y., Ulanova, L., dkk. (2016). Matrix Profile I: All Pairs Similarity Joins for Time Series. ICDM 2016, 1317-1322. DOI 10.1109/ICDM.2016.0179 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-081 | Zhu dkk. 2016 | rujukan | JURNAL | Zhu, Y., Yeh, C.-C. M., Zimmerman, Z., Kamgar, K., Keogh, E. (2016). Matrix Profile II. ICDM 2016, 739-748. DOI 10.1109/ICDM.2016.0085 (Crossref OK; doi.org 202) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-082 | Sakurada dan Yairi 2014 | rujukan | JURNAL | Sakurada, M., Yairi, T. (2014). Anomaly Detection Using Autoencoders with Nonlinear Dimensionality Reduction. Proc. MLSDA 2014, 4-11. DOI 10.1145/2689746.2689747 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §3.3, §6 | TERVERIFIKASI |
| R5-083 | Massey 1951 | rujukan | JURNAL | Massey, F. J. (1951). The Kolmogorov-Smirnov Test for Goodness of Fit. JASA 46(253), 68-78. DOI 10.1080/01621459.1951.10500769 (Crossref OK; doi.org 403) | 2026-10-27 | RND_R5 §1, §6 | TERVERIFIKASI |
| R5-084 | 1 | DOI dibuang | BELUM-TERUKUR | 10.1214/09-AOAS282 terverifikasi sebagai makalah berbeda (Shirley dkk. 2010, HMM uji alkohol) dan dibuang; tidak dipakai di RND_R5 | 2026-10-27 | RND_R5 §6 | TERVERIFIKASI (penolakan) |
| R5-085 | 3 / 1 / 2 / 2 / 2 dan 0 / 2 / 2 / 1 / 3 | episode alarm baseline (CUSUM dan PH) | RUN-KITA | `scratch/rnd_r5/drift_measured_v2.json` `per_well.*.cusum_episodes` dan `per_well.*.ph_episodes` untuk F-10, F-14, F-15A, F-15_S, F-9_A | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-086 | 0 / 1 / 1 / 0 / 0 | episode paruh kedua pada h kalibrasi | RUN-KITA | `drift_measured_v2.json` `per_well.*.half2_episodes_at_cal_h` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-087 | 0,9779 / 0,9954 / 0,9948 / 0,9765 / 0,9865 | autokorelasi lag-1 per well | RUN-KITA | `drift_measured_v2.json` `per_well.*.ac1` | 2026-10-27 | RND_R5 §2.2 | TERUKUR |
| R5-088 | 7.312 / 7.314 / 10.042 / 10.043 / 5.853 / 5.872 / 8.058 / 8.058 / 1.608 / 1.845 | menit alarm di luar baseline dan menit di luar baseline per well | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_alarm_minutes_outside_baseline` dan `per_well.*.minutes_outside_baseline` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-089 | 59,98 / 59,99 / 59,81 / 60,00 / 52,29 | menit alarm CUSUM per jam di luar baseline per well | RUN-KITA | `drift_measured_v2.json` `per_well.*.cusum_alarm_rate_outside_per_hour` | 2026-10-27 | RND_R5 §2.4 | TERUKUR |
| R5-090 | 6.408 / 8.300 dan 1.176 / 974 | baris dinilai dan jumlah positif per well (uji anomali) | RUN-KITA | `scratch/rnd_r5/anomaly_unsup.json` `per_well.F-10.baris_dinilai` 6408, `per_well.F-10.positif` 1176, `per_well.F-15_S.baris_dinilai` 8300, `per_well.F-15_S.positif` 974 | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-091 | 6.167 / 8.024 | menit alarm total One-Class SVM | RUN-KITA | `anomaly_unsup.json` `per_well.*.ocsvm.alarm_menit_total` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-092 | 0,2461 / 0,2198 / 0,2147 / 0,2151 / 0,2018 / 0,1867 / 0,1868 / 0,1872 | presisi alarm-menit per well per detektor | RUN-KITA | `anomaly_unsup.json` `per_well.*.*.presisi_menit_alarm` (F-10: iforest, lof, ocsvm, ae; F-15_S: iforest, lof, ocsvm, ae) | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-093 | 5,60 / 9,70 / 11,21 / 14,55 | FAR per 24 jam detektor anomali per well | RUN-KITA | `anomaly_unsup.json` `per_well.*.*.far_per_24h` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |
| R5-094 | 1 / 2 / 3 | episode alarm pada baseline per detektor per well | RUN-KITA | `anomaly_unsup.json` `per_well.*.*.episode_baseline` | 2026-10-27 | RND_R5 §2.5.1 | TERUKUR |

---

## 3. BAGIAN R4 — BOOSTING, KALIBRASI, CONFORMAL (kartu `t_246de62e`)

Dokumen pendamping: `docs/RND_R4_BOOSTING.md`. Tanggal pengukuran: 2026-10-27 (WIB).
Skrip ukur: `/home/neonti/.hermes/cache/scratch/rnd_r4/` (`rnd_r4_inventory.py`, `bench_a_models.py`, `bench_a_fast.py`).

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R4-01 | 23.922 | baris | RUN-KITA | `scratch/v9_d1/datasets/vib.csv.gz`, dihitung `rnd_r4_inventory.py`; cocok dengan jumlah windows D0 (23.922) | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-02 | 1.989 | baris | RUN-KITA | `vib.csv.gz` group well=F-14; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2, §4.2 | TERUKUR |
| R4-03 | 4.548 | baris | RUN-KITA | `vib.csv.gz` group well=F-5 | 2026-10-27 | RND_R4 §3.2, §4.2 | TERUKUR |
| R4-04 | 6.482 | baris | RUN-KITA | `vib.csv.gz` group well=F-15A | 2026-10-27 | RND_R4 §3.2, §4.2 | TERUKUR |
| R4-05 | 10.903 | baris | RUN-KITA | `vib.csv.gz` group well=F-15_S | 2026-10-27 | RND_R4 §3.2, §4.2 | TERUKUR |
| R4-06 | 55 | fitur | RUN-KITA | `vib.csv.gz` kolom non-meta non-label; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-07 | 4 | fitur | RUN-KITA | fitur `SPM_mean`, `SPM_std`, `SPM_slope`, `SPM_last` seluruhnya kosong pada kelas vib; peringatan `SimpleImputer` di `rnd_r4/bench_vib.log` | 2026-10-27 | RND_R4 §9 butir 8 | TERUKUR |
| R4-08 | 35.906 | baris | RUN-KITA | `ssi.csv.gz`; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-09 | 56.495 | baris | RUN-KITA | `shk.csv.gz`; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-10 | 5.555 | baris | RUN-KITA | `stuck_k1.csv.gz`; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-11 | 118.567 | baris | RUN-KITA | `stuck_k2.csv.gz`; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-12 | 52.509 | baris | RUN-KITA | `hyd_ki.csv.gz`; `rnd_r4_inventory.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-13 | 40 | fitur | RUN-KITA | `hyd_ki.csv.gz` kolom non-meta non-label (lebih sedikit dari 55 kelas rig lain) | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-14 | 21.933 | baris latih | RUN-KITA | `bench_vib.log` baris JSON fold F-14 model rf_v9; `bench_a_models.py` | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-15 | 0,9117 | AUPRC | RUN-KITA | `bench_vib.log` fold F-14 model rf_v9 (`average_precision_score`) | 2026-10-27 | RND_R4 §3.2, §10 | TERUKUR |
| R4-16 | 0,5651 | proporsi | RUN-KITA | `bench_vib.log` fold F-14, prevalensi `y_vib` pada well uji | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-17 | +0,3466 | selisih AUPRC | DERIVASI aritmetik | 0,9117 − 0,5651 = 0,3466 (dihitung ulang); definisi ΔB = AUPRC − prevalensi | 2026-10-27 | RND_R4 §3.2 | TERVERIFIKASI sebagai aritmetika |
| R4-18 | 7,41 | detik | RUN-KITA | `bench_vib.log` fold F-14, `RandomForestClassifier(300, leaf 5, n_jobs=-1)` fit | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-19 | 0,30 | detik | RUN-KITA | `bench_vib.log` fold F-14, `predict_proba` pada 1.989 baris | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-20 | 420 | detik | RUN-KITA | batas waktu tool yang terlewati saat run 4 model dg `n_jobs=-1`; proses tidak selesai (`bench_vib.log` hanya memuat 1 baris) | 2026-10-27 | RND_R4 §3.2, §9 butir 1 | TERUKUR (kegagalan waktu) |
| R4-21 | 1.300 | persen CPU | RUN-KITA | `ps -o %cpu` pid 126668 selama run 4 model; indikasi thread over-subscription | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-22 | 18 | core | RUN-KITA | `nproc` pada host WSL2 sesi ini | 2026-10-27 | RND_R4 §3.2 | TERUKUR |
| R4-23 | 300 pohon; leaf 5; balanced_subsample; seed 42 | parameter | KONVENSI | `code/v9_i1_pipeline.py:423-426` (kontrak RF V9) | 2026-10-27 | RND_R4 §3.1, §7.1 | BELUM (tanpa rujukan eksternal) |
| R4-24 | 0,441–0,912 | AUPRC | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.1 baris C1 RF vib; JSON `scratch/v9_eval_c/` | 2026-10-27 | RND_R4 §3.2 (pembanding silang), §4.2 | TERUKUR |
| R4-25 | 4,1–496 (119 kali) | FAR per 24 jam | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.1 baris C3 (tau 0,5) | 2026-10-27 | RND_R4 §4.3, §5.3 | TERUKUR |
| R4-26 | 62,3 | persen baris | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.2 C4 (`n_nodata` 22.385/35.906) | 2026-10-27 | RND_R4 §3.3 | TERUKUR |
| R4-27 | 4,6 | persen onset | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.4 (anchor absorbed 13/281) | 2026-10-27 | RND_R4 §3.3 | TERUKUR |
| R4-28 | 0,14–0,57 | proporsi | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.1 C4 (prevalensi vib antar well) | 2026-10-27 | RND_R4 §4.2, §5.3 | TERUKUR |
| R4-29 | hyd 0,1366; shk 0,0355; ssi 0,0169; stuck_k2 0,0167; vib 0,2269; stuck_k1 0,3613 | proporsi | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` tabel prevalensi engine (ledger D0) | 2026-10-27 | RND_R4 §6.2 | TERUKUR |
| R4-30 | 6 | alarm per 24 jam | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2 (gerbang A) | 2026-10-27 | RND_R4 §7.3 | BELUM (konvensi internal) |
| R4-31 | 1,0 | alarm per menit | KONVENSI | `code/v9_i1_pipeline.py:615` `TARGET_FP_PER_MIN = 1.0` | 2026-10-27 | RND_R4 §5.1 | BELUM (konvensi internal) |
| R4-32 | q = 1 − 1,0·(n/60)/n | level kuantil | DERIVASI aritmetik | `code/v9_i1_pipeline.py:632-633`; untuk target 1 alarm/menit bentuknya menyederhana menjadi q = 1 − 1/60 | 2026-10-27 | RND_R4 §5.1 | TERVERIFIKASI sebagai aritmetika |
| R4-33 | q95 → TP 0, FP 177 | hitungan | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.5 (hyd K-ii, `code/v9_e_STAT_02_stuck_e2.py`) | 2026-10-27 | RND_R4 §5.1 | TERUKUR |
| R4-34 | 28 | fold | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` baris 76 (vib 4 + ssi 9 + shk 9 + stuck_k2 4, x 3 model) | 2026-10-27 | RND_R4 §3.1 | TERUKUR |
| R4-35 | 469 jendela x 27 fitur | ukuran dataset | RUN-KITA | `scratch/v6_e1/toolwear_windows.csv`; juga ledger D0-* | 2026-10-27 | RND_R4 §3.3 | TERUKUR |
| R4-36 | 0,05 | alpha (target FAR) | KONVENSI | pilihan dokumen ini untuk uji conformal, bukan angka literatur; wajib ditulis di pra-registrasi sebelum run | 2026-10-27 | RND_R4 §5.2 | BELUM (belum diuji) |
| R4-37 | 2.000 | resample bootstrap | KONVENSI | rencana uji §7.1; belum dijalankan | 2026-10-27 | RND_R4 §7.1 | BELUM (belum diuji) |
| R4-38 | 10 kali | rasio sampel kalibrasi | KONVENSI | aturan operasional yang diusulkan dokumen ini untuk isotonic, bukan kutipan literatur; belum diuji pada data kita | 2026-10-27 | RND_R4 §4.2 | BELUM (usulan, bukan bukti) |
| R4-39 | 7 engine / 11 klaim / 27 head | cakupan | KONVENSI | `docs/V9_EVAL_C_LAYERC.md` §0 EC-1 dan `code/v9_i1_pipeline.py` REGISTRY | 2026-10-27 | RND_R4 header | BELUM (konvensi internal) |
| R4-40 | 0 | hasil pembanding LightGBM/XGBoost/CatBoost | BELUM-TERUKUR | run pembanding tidak selesai dalam anggaran waktu (R4-20); sengaja tidak diisi angka literatur | 2026-10-27 | RND_R4 §3.2, §9 | BELUM |

## Bagian R2: stokastik + survival (kartu t_c24b3640)

Penomoran memakai awalan `R2-` agar tidak bertabrakan dengan `L-xx` (P0) dan `D0-xxx` (D0).
Angka D0 yang dipakai ulang di dokumen R2 tidak diduplikasi di sini: rujukannya id D0 yang sudah ada
(mis. 95.925 = D0-600, 389 positif = D0-599, 469 jendela = D0-766, onset 55 = D0-581). Jumlah baris R2 = 20.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R2-001 | 95.925 baris / 40 FP / FAR 0,603 | jendela; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json` head `stuck.rf_lowo` metrik_segmen (`fp`=40, `far_segmen`=0,603); populasi D0-600 (95.925) + D0-599 (389 positif) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 kasus A; §7.2 | TERUKUR |
| R2-002 | 10.401 baris / 110 FP / FAR 16,611 | jendela; FP/24 jam | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json` head `hyd.hybrid_rule_and_persistence` metrik_segmen (`n`=10.401, `fp`=110, `far_segmen`=16,611) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 kasus B | TERUKUR |
| R2-003 | 0,005 FAR absolut; 1% lebar CI; N=2.000 default; N=10.000 utk FAR < 1/24 jam | FP/24 jam; %; iterasi | KONVENSI | kriteria berhenti ditetapkan sebelum run di `scratch/rnd_r2/mc_iterations.py` docstring; hasil uji di RND_R2_STOKASTIK.md §4.2 | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 | BELUM |
| R2-004 | SE(lo)=0,0176 SE(hi)=0,0113 lebar=0,3710 (N=200, stuck K-ii) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel A | TERUKUR |
| R2-005 | SE(lo)=0,0095 SE(hi)=0,0074 lebar=0,3679 (N=500, stuck K-ii) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel A | TERUKUR |
| R2-006 | SE(lo)=0,0060 SE(hi)=0,0060 lebar=0,3770 (N=1.000, stuck K-ii) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel A | TERUKUR |
| R2-007 | SE(lo)=0,0060 SE(hi)=0,0000 lebar=0,3800 (N=2.000, stuck K-ii) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel A | TERUKUR |
| R2-008 | SE(lo)=0,4125 SE(hi)=0,2169 lebar=6,2316 (N=200, hyd K-i) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel B | TERUKUR |
| R2-009 | SE(lo)=0,1666 SE(hi)=0,1227 lebar=6,1713 (N=500, hyd K-i) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel B | TERUKUR |
| R2-010 | SE(lo)=0,0608 SE(hi)=0,0614 lebar=6,2631 (N=1.000, hyd K-i) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel B | TERUKUR |
| R2-011 | SE(lo)=0,0745 SE(hi)=0,0614 lebar=6,2935 (N=2.000, hyd K-i) | FAR; FAR; FAR | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55) | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel B | TERUKUR |
| R2-012 | galat baku relatif 4,82% (N=200) dan 2,02% (N=2.000) dan 0,14% (N=10.000) pada FAR 0,6/24 jam | % | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55); blok `threshold_sim` kunci `q=0.0035` | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel C | TERUKUR |
| R2-013 | galat baku relatif 0,68% (N=200) dan 0,18% (N=2.000) pada FAR 16,6/24 jam | % | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55); blok `threshold_sim` kunci `q=0.0115` | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel C | TERUKUR |
| R2-014 | galat baku relatif 1,89% (N=200) dan 0,50% (N=2.000) pada FAR 6,6/24 jam | % | RUN-KITA | `scratch/rnd_r2/mc_result.json`; `python3 scratch/rnd_r2/mc_iterations.py` (run 2026-10-27 04:02 WIB, seed 11/22/33/44/55); blok `threshold_sim` kunci `q=0.0416` | 2026-10-27 | RND_R2_STOKASTIK.md §4.2 tabel C | TERUKUR |
| R2-015 | B1 0-0,115; TLead 4,5-8,5 | probabilitas Brier; menit | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris stuck K-ii (turunan `scratch/v9_e_stat/*.json`) | 2026-10-27 | RND_R2_STOKASTIK.md §7.2 | TERUKUR |
| R2-016 | median episode 1,0 | menit | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §3 tabel state (kolom median episode); dihitung `scratch/rnd_d0/*` | 2026-10-27 | RND_R2_STOKASTIK.md §2, §3, §11 | TERUKUR |
| R2-017 | 4 dari 9 well punya kanal STUCK | well | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §3 kesimpulan; tabel per well | 2026-10-27 | RND_R2_STOKASTIK.md §1, §2, §3, §11 | TERUKUR |
| R2-018 | 31 DOI terdaftar, HTTP 200 | entri DOI | RUN-KITA | `scratch/rnd_r2/doi_verified.json` (13 DOI kanonik) + `scratch/rnd_r2/doi_verified_apps.json` (18 DOI aplikasi); `python3 scratch/rnd_r2/doi_verify.py` dan `doi_verify_apps.py` | 2026-10-27 | RND_R2_STOKASTIK.md §9 | TERUKUR |
| R2-019 | vib FAR tau0,5 sebar 4,1-496; ssi AUPRC sebar 30x | FP/24 jam; rasio | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.1 (C3 vib) dan §2.2 (C1 ssi) | 2026-10-27 | RND_R2_STOKASTIK.md §4.1, §5 | TERUKUR |
| R2-020 | 0 dari 8 metode memenuhi syarat naik tier tanpa asumsi baru; hanya MC skor 5 | penilaian | KONVENSI | penilaian ahli kartu ini, dasar = tabel D0 §3/§4 + skor §8 RND_R2_STOKASTIK.md; bukan metrik, tidak boleh dibaca sebagai hasil eksperimen | 2026-10-27 | RND_R2_STOKASTIK.md §8, §10 butir 7 | BELUM |

---

## Bagian E0 (kartu `t_57e7d52b`, audit implementasi engine)

Lingkungan ukur: `/home/neonti/.venvs/rnd_r3/bin/python` 3.11.15, pandas 3.1.0, numpy 2.4.6, scikit-learn 1.9.1. Skrip: `scratch/e0_audit/*.py` (5 skrip, hanya baca). Tanggal akses seluruh baris: 2026-10-27 (WIB).

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| E0-001 | 292.954 baris (vib 23.922; ssi 35.906; shk 56.495; stuck_k1 5.555; stuck_k2 118.567; hyd_ki 52.509) | baris | RUN-KITA | `scratch/e0_audit/e0_audit_results.json` kunci `leakage.*.n_rows`; `python3 scratch/e0_audit/e0_audit.py` | 2026-10-27 | RND_E0_AUDIT_ENGINE.md §1.1 | TERUKUR |
| E0-002 | 0 pelanggaran `feat_ts_max >= lab_ts` pada 292.954 baris | baris | RUN-KITA | `e0_audit_results.json` kunci `leakage.*.n_feat_ts_max_ge_lab_ts` | 2026-10-27 | §1.1, ringkasan butir 1 | TERUKUR |
| E0-003 | maks(`feat_ts_max - lab_ts`) = -1 menit; min = -6 (lima dataset) dan -11 (stuck_k2) | menit | RUN-KITA | `e0_audit_results.json` kunci `max_feat_ts_max_minus_lab_ts`, `min_feat_ts_max_minus_lab_ts` | 2026-10-27 | §1.1 | TERUKUR |
| E0-004 | 40 fitur `hyd_ki`, 0 di antaranya prefiks SPPA/TFLO/SPM | kolom | RUN-KITA | `e0_audit_results.json` kunci `leakage.hyd_ki.n_features` dan `label_channel_in_features` | 2026-10-27 | §1.2 | TERUKUR |
| E0-005 | 55 fitur pada vib, ssi, shk, stuck_k1, stuck_k2; kanal labelnya (VIBLAT/CRPM/SHKRSK/STUCK) tidak termasuk | kolom | RUN-KITA | `e0_audit_results.json` `leakage.*.n_features`; `code/v9_d1_02_rig_windows.py:39-41` | 2026-10-27 | §1.2 | TERUKUR |
| E0-006 | hash prediksi rule identik antar dua kali jalan di 5 kelas | hash | RUN-KITA | `e0_audit_results.json` `rule.*.rule_bit_identik` (semua true), `rule_hash_run1/2` | 2026-10-27 | §4.1 | TERUKUR |
| E0-007 | vib rule: P 0,9193 R 0,4132 FP 197 FAR 15,34 | rasio; rasio; jendela; FP/24 jam | RUN-KITA | `e0_audit_results.json` `rule.vib.rule_all` | 2026-10-27 | §2.2 | TERUKUR |
| E0-008 | vib/shk/stuck rule: laju alarm pada `y_prev=0` = 0,0000 (tidak pernah menyala) | rasio | RUN-KITA | `e0_audit_results.json` `rule.{vib,shk,stuck_k1}.rule_pos_rate_pada_onset_baru` | 2026-10-27 | §2.2, K-1 | TERUKUR |
| E0-009 | shk rule: P 0,6134 FP 121; P persistence 0,3098 | rasio | RUN-KITA | `e0_audit_results.json` `rule.shk.rule_all`, `.persistence_all` | 2026-10-27 | §2.2 | TERUKUR |
| E0-010 | stuck K-i rule: P 0,9587 FP 49; P persistence 0,7819 | rasio | RUN-KITA | `e0_audit_results.json` `rule.stuck_k1.*` | 2026-10-27 | §2.2 | TERUKUR |
| E0-011 | ssi rule: P 0,2121 R 0,0115 TP 7 FP 26; presisi per fold 0,40/0,00/0,25/0,1111/0,50/0,20; n_aktif segmen 0 | rasio; jendela | RUN-KITA | `e0_audit_results.json` `rule.ssi.rule_all`; `e0_audit_results3.json` `rule_json.ssi`; `scratch/v9_i1/v9_i1_RESULTS.json` head `ssi/rule_display` | 2026-10-27 | §3.2, S-1 | TERUKUR |
| E0-012 | hyd rule: P 0,7261 total; 0,8416 saat `y_prev=1`; 0,3573 saat `y_prev=0`; laju 0,0404 pada onset baru | rasio | RUN-KITA | `e0_audit_results.json` `rule.hyd_ki.rule_all`, `.rule_subset_*`, `.rule_pos_rate_pada_onset_baru` | 2026-10-27 | §2.2, §2.6 | TERUKUR |
| E0-013 | P persistence: vib 0,7352 (FP 1.456); hyd 0,7298 (FP 1.941); stuck 0,7819; shk 0,3098; ssi 0,2415 | rasio | RUN-KITA | `e0_audit_results.json` `rule.*.persistence_all` | 2026-10-27 | §2.2, §3.3 | TERUKUR |
| E0-014 | cakupan waktu 0,0146 (ssi F-5: 4.714 baris / 322.772 menit) sampai 0,717 (ssi F-9_A: 841 / 1.173) | rasio | RUN-KITA | `e0_audit_results.json` `rule.*.cakupan_waktu_per_well` | 2026-10-27 | §5.2, K-4 | TERUKUR |
| E0-015 | menit negatif dipakai penyebut: vib 18.493; ssi 35.299; shk 54.490; stuck 3.548; hyd 45.337 | menit | RUN-KITA | `e0_audit_results.json` `rule.*.n_neg_dipakai_penyebut` | 2026-10-27 | §5.1, §5.2 | TERUKUR |
| E0-016 | identitas rule-jendela vs label: mismatch 0 di 4 kelas, 23 dari 52.509 (0,04%) di hyd_ki | baris | RUN-KITA | `e0_audit_results.json` `identity_rule_window_vs_label.*` | 2026-10-27 | §2.1, M-1 | TERUKUR |
| E0-017 | persistence_event stuck K-ii: 26 baris alarm; 15 positif; 11 FP; 0 dipicu event yang dikreditkan; 15 dipicu event lain | baris | RUN-KITA | `e0_audit_results2.json` `stuck_k2_alarm_provenance` | 2026-10-27 | §2.3, K-2 | TERUKUR |
| E0-018 | sebaran lead alarm persistence_event: 0x11, 1x2, 2x1, 4x1, 5x2, 6x2, 8x4, 9x1, 10x2 | menit | RUN-KITA | `e0_audit_results2.json` `alarm_lead_dist` | 2026-10-27 | §2.3 | TERUKUR |
| E0-019 | 11 FP alarm persistence_event = angka "FP alarm total 11" di EVAL_C | baris | RUN-KITA | `e0_audit_results2.json` + `docs/V9_EVAL_C_LAYERC.md:94` | 2026-10-27 | §2.3 (cek kesetiaan reproduksi) | TERUKUR |
| E0-020 | n_aktif head `stuck/persistence_event` di segmen V9 = 4 baris (0,0%) | baris | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json`; `e0_audit_results3.json` `v9_i1_head_metrics.stuck.persistence_event` | 2026-10-27 | §2.3 | TERUKUR |
| E0-021 | tool_wear op_far_calibrated: FP R01 1-3 dari 35-42 jendela; peluang minimal 1 alarm kebetulan 0,7603 / 0,9951 / 0,7603 / 0,9871 per alat; produk 4/4 = 0,5678 | rasio | DERIVASI aritmetik (model Poisson dari laju terukur) | `e0_audit_results4.json`; laju dari `v9_i1_RESULTS.json` `tool_wear/op_far_calibrated/per_alat` | 2026-10-27 | §2.4, K-3 | TERUKUR (laju) + DERIVASI (peluang, asumsi Poisson dicatat) |
| E0-022 | tool_wear segmen: recall 0,0542 (tp 13, fn 227), presisi 0,619, FAR 2,096 FP/menit; engine 5/27: FAR 34,585 | rasio; FP/menit | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json` head `tool_wear/op_far_calibrated.metrik_segmen`; `e0_audit_results4.json` `ringkas` | 2026-10-27 | §2.4, §5.3 | TERUKUR |
| E0-023 | `q` kuantil = 0,983333 untuk n = 100, 469, 1.000, 5.000 (konstanta) | rasio | RUN-KITA | `e0_audit_results.json` `tool_wear.rumus_kuantil`; `code/v9_i1_pipeline.py:631` | 2026-10-27 | §3.7, §5.3, M-4 | TERUKUR |
| E0-024 | bit_wear segmen F-14: n 47.645, tp 4.881, fp 36, fn 37, P 0,9927, R 0,9925, FAR 1,213 (unit jendela 60 dtk) | rasio; FP/24 jam | RUN-KITA | `v9_i1_RESULTS.json` head `bit_wear/persistence.metrik_segmen`; `e0_audit_results3.json` | 2026-10-27 | §2.5, §5.4 | TERUKUR |
| E0-025 | bit_wear global: 198.928 baris, 49.732 positif, prevalensi 0,25, P(label bertahan) 0,9903 | rasio | RUN-KITA | `e0_audit_results.json` `bit_wear`; `e0_audit_results3.json` `bit_wear_pipeline` | 2026-10-27 | §2.5, §9 butir 5 | TERUKUR |
| E0-026 | langkah kedalaman median 0,015 m pada 198.928 baris USROP | meter | RUN-KITA | `e0_audit_results3.json` `bit_wear_pipeline.depth_step_median` | 2026-10-27 | §5.4, S-6 | TERUKUR |
| E0-027 | RF: dua fit identik tidak bit-identik, selisih maks 2,22e-16 (n_jobs=-1, seed 42, 55 fitur, 300 pohon) | selisih probabilitas | RUN-KITA | `e0_audit_results.json` `determinisme_rf` | 2026-10-27 | §4.2, S-5 | TERUKUR |
| E0-028 | REGISTRY: 27 head (vib 4, ssi 4, shk 4, stuck 6, hyd 4, bit_wear 2, tool_wear 3); tier 12 SUPERV / 13 TREN / 2 NONE; layer L0 5 / L1 11 / L2 9 / L3 2 | head | RUN-KITA | `e0_audit_results3.json` `registry`; `code/v9_i1_pipeline.py:74-300` | 2026-10-27 | §3.1 | TERUKUR (dikoreksi di run 34: stuck 5 menjadi 6 agar total 27) |
| E0-029 | 65 skrip `.py` menyebut `/mnt/d/Capstone 1/`; 0 di antaranya berprefiks `v9_` | berkas | RUN-KITA | `e0_audit_results3.json` `arsip_refs` (pemeriksaan ulang dengan `grep -rn` di `code/`) | 2026-10-27 | §3.6, M-3 | TERUKUR |
| E0-030 | tool_wear: langkah `start_sample` tepat 1.000 sampel di 8 run; FS 1.000 Hz dan WIN 1.000 sampel di skrip pembentuk | sampel | RUN-KITA | `e0_audit_results.json` `tool_wear.langkah_start_sample`; `code/v6_e1_50_toolwear.py` | 2026-10-27 | §5.5, M-7 | TERUKUR |
| E0-031 | 4 fitur SPM (mean/std/slope/last) tanpa satu nilai pun pada segmen vib yang diuji → 51 fitur efektif dari 55 | kolom | RUN-KITA | peringatan `SimpleImputer` pada `e0_audit.py`; `e0_audit_results.json` `determinisme_rf.n_fitur` | 2026-10-27 | §4.4, M-5 | TERUKUR |
| E0-032 | Eksekusi ulang `e0_audit.py`: 466 dari 468 field JSON identik; 2 field berbeda hanya `determinisme_rf.hash1/hash2`; `max_abs_diff` sama 2,220446049250313e-16; hash rule lima kelas identik | field; hash | RUN-KITA | workspace `e0v_rerun_compare.json`, `e0_rerun_stdout.txt` (exit 0) | 2026-10-27 | §10.1 | TERUKUR |
| E0-033 | Fraksi onset baru di antara baris positif: vib 1.386/5.429 = 0,2553; shk 1.531/2.005 = 0,7636; ssi 522/607 = 0,8600; hyd 1.929/7.172 = 0,2690; stuck 444/2.007 = 0,2212 | baris; rasio | RUN-KITA | workspace `e0v_onset.json` (kolom `y_prev_*` resep D1) | 2026-10-27 | §2.2, §10.2 | TERUKUR |
| E0-034 | Presisi persistence `bit_wear` menurut urutan baris: 0,9903 (berkas mentah), 0,9903 (well+kedalaman), 0,5668 (kedalaman saja), 0,9927 (segmen F-14) | rasio | RUN-KITA | workspace `e0v_recheck.json` | 2026-10-27 | §5.6, S-8, §10.2 | TERUKUR |
| E0-035 | 133.539 dari 198.927 pasangan baris berurutan (0,6713) menyeberang well pada sort `Measured Depth m` global | pasangan; rasio | RUN-KITA | workspace `e0v_recheck.json` `bit_wear_depth_sort_global.n_pasangan_lintas_well` | 2026-10-27 | §5.6, S-8 | TERUKUR |
| E0-036 | DOI 10.1145/2382577.2382579, 10.1016/j.patter.2023.100804, 10.1371/journal.pone.0118432, 10.1145/1143844.1143874: lapis registrasi 302 (keempat), lapis metadata Crossref 200 (keempat), lapis akses penerbit 403 untuk dua DOI ACM | status HTTP | RUN-KITA | `curl -I https://doi.org/<doi>` tanpa redirect dan `curl https://api.crossref.org/works/<doi>`, 2026-10-27; `e0_doi.json` | 2026-10-27 | §7, §10.3 | TERUKUR |

---

## Bagian R1: metaheuristik kontinu (kartu `t_4ee3d4d1`)

Tanggal akses seluruh baris: 2026-10-27. Berkas bukti: `scratch` kartu `t_4ee3d4d1` pada workspace board `rnd-algo-2026` (`lit_r1.json`, `r1_selected.json`, `r1_round2.json`, `r1_round3.json`, `refs_registry.md`, `r1_verify_pass2.json`, `r1_publisher_status.json`); skrip `r1_harvest.py`, `r1_select.py`, `r1_round2.py`, `r1_round3.py`, `r1_registry.py`, `r1_stats.py`, `r1_verify_pass2.py`, `r1_publisher_status.py`, `r1_check309.py`.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R1-001 | 36 | string kueri | RUN-KITA | `r1_stats.py` atas `lit_r1.json`, field `algos[*][*].query`, dihitung unik | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-002 | 323 | record | RUN-KITA | `r1_stats.py` atas `lit_r1.json`, record dengan field `doi` tidak kosong | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-003 | 309 | DOI unik | RUN-KITA | `r1_stats.py`, `len(lit_r1.json["doi_checks"])` | 2026-10-27 | RND_R1 §0.1, §6 | TERUKUR |
| R1-004 | 309 dari 309 | DOI resolve | RUN-KITA | `lit_r1.json["doi_checks"]`, semua nilai `http` = 302; pemeriksaan HEAD ke `https://doi.org/<doi>` di `r1_harvest.py` | 2026-10-27 | RND_R1 §0.1, §0.2 | TERUKUR |
| R1-005 | 185 | kandidat | RUN-KITA | `r1_select.py`, jumlah seluruh entri `r1_selected.json` (filter judul mengandung nama algoritma + tahun 2019-2026 + jurnal tidak kosong + istilah domain) | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-006 | 80 | kandidat | RUN-KITA | `r1_round2.py`, jumlah entri `gaps` pada `r1_round2.json` | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-007 | 36 | kandidat | RUN-KITA | `r1_round2.py`, jumlah entri `foundations` pada `r1_round2.json` (12 pencarian judul, maksimum 3 kandidat per pencarian) | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-008 | 54 | rujukan | RUN-KITA | `r1_registry.py` atas empat berkas harvest, keluaran `refs_registry.md` (54 baris, 0 DOI hilang dari pool) | 2026-10-27 | RND_R1 §0.1, §2 | TERUKUR |
| R1-009 | 11 | algoritma berbeda | DERIVASI-ARITMETIK | 12 nama kartu dikurangi 1 (SMA = Slime Mould Algorithm, DOI 10.1016/j.future.2020.03.055 sama); penjelasan RND_R1 §0.3 | 2026-10-27 | RND_R1 §0.3, §3, §6 | TERVERIFIKASI |
| R1-010 | 14 | unit penilaian | DERIVASI-ARITMETIK | 12 nama kartu + 1 (SSA dibelah: Salp dan Sparrow) + 1 (Honey Badger sebagai pembanding), SMA dan Slime Mould tetap dua baris | 2026-10-27 | RND_R1 §0.3, §3 | TERVERIFIKASI |
| R1-011 | 9 | well | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §3; windows per well pada `scratch/rnd_d0/*` | 2026-10-27 | RND_R1 §1.1, §1.4 | TERUKUR |
| R1-012 | 55 | fitur | RUN-KITA | `docs/V9_R1_JUSTIFICATION.md:169` dan `docs/V9_PM1_ARCHITECTURE.md:255` (11 kanal MWD x 5 statistik = 55 fitur) | 2026-10-27 | RND_R1 §1.1, §2.9 | TERVERIFIKASI |
| R1-013 | 27 | fitur getaran | RUN-KITA | `docs/V9_PM1_ARCHITECTURE.md:276` (9 statistik x 3 sumbu X/Y/Z); ditegaskan `code/v9_i1_pipeline.py:605` (`assert len(feats) == 27`) | 2026-10-27 | RND_R1 §1.1 | TERVERIFIKASI |
| R1-014 | 27 | head | RUN-KITA | `scratch/v9_i1/_verify_stdout.txt:3` dan `:16` (`[PASS] V2: tier cocok dokumen: 27 head`) | 2026-10-27 | RND_R1 §1 | TERVERIFIKASI |
| R1-015 | 52.509 | jendela | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §3 (windows hyd_ki, 9 well); handoff kartu `t_34c20c78` | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-016 | 56.495 | jendela | RUN-KITA | idem R1-015 (shk, 9 well) | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-017 | 35.906 | jendela | RUN-KITA | idem R1-015 (ssi, 9 well) | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-018 | 23.922 | jendela | RUN-KITA | idem R1-015 (vib, 4 well) | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-019 | 118.567 | jendela | RUN-KITA | idem R1-015 (stuck_k2, 4 well) | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-020 | 5.555 | jendela | RUN-KITA | idem R1-015 (stuck_k1, 2 well) | 2026-10-27 | RND_R1 §1.1, §1.3 | TERUKUR |
| R1-021 | 28 fold E_ML (vib 4, ssi 9, shk 9, stuck_k2 4) + 9 fold hyd_ki + 4 fold stuck_E2 + 8 run tool_wear di 4 alat | fold | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md:76` (cakupan eksekusi) | 2026-10-27 | RND_R1 §1.3, §1.4 | TERUKUR |
| R1-022 | 4 sampai 6 | dimensi | KONVENSI | target desain kartu ini; parameter RF terverifikasi di `docs/V9_PM1_ARCHITECTURE.md:356` hanya `n_estimators`, seed, tanpa grid search | 2026-10-27 | RND_R1 §1.1 | KONVENSI |
| R1-023 | 55 | dimensi biner | RUN-KITA | sama dengan R1-012 (subset dari 55 fitur) | 2026-10-27 | RND_R1 §1.1, §2.9 | TERVERIFIKASI |
| R1-024 | 27 | dimensi biner | RUN-KITA | sama dengan R1-013 | 2026-10-27 | RND_R1 §1.1 | TERVERIFIKASI |
| R1-025 | 1 x jumlah well (9 untuk kelas 9 well; 4 vib; 2 stuck K-i) | dimensi | RUN-KITA | jumlah well per kelas per R1-011 sampai R1-019 | 2026-10-27 | RND_R1 §1.1 | TERUKUR |
| R1-026 | 300 | evaluasi fitness | KONVENSI | batas atas yang ditetapkan kartu ini untuk T1; bukan hasil ukur kapasitas mesin | 2026-10-27 | RND_R1 §1.3, §4.2 | KONVENSI |
| R1-027 | 100 | evaluasi per well | KONVENSI | batas yang ditetapkan kartu ini untuk T3 (ruang 1 dimensi) | 2026-10-27 | RND_R1 §1.3 | KONVENSI |
| R1-028 | 1.000 | evaluasi fitness | KONVENSI | batas atas yang ditetapkan kartu ini untuk T2 (55 dimensi) | 2026-10-27 | RND_R1 §1.3, §4.2 | KONVENSI |
| R1-029 | FAR 4,1 sampai 496 (119 kali) | FP/24 jam; rasio | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.1 baris C3 (`tau0,5: 4,1-496 = 119x`) | 2026-10-27 | RND_R1 §1.4, §4.4 | TERUKUR |
| R1-030 | 7 dari 9 | fold | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.3 (`CI RF memuat prev 7/9`) | 2026-10-27 | RND_R1 §1.4, §4.4 | TERUKUR |
| R1-031 | 30 | rasio sebar AUPRC | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.2 (`AUPRC 0,015-0,459 (30,4x)`) | 2026-10-27 | RND_R1 §1.4 | TERUKUR |
| R1-032 | 0 dari 9 | fold | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.5 (`CI95 persistence memuat prev 0/9`) | 2026-10-27 | RND_R1 §4.4 | TERUKUR |
| R1-033 | FAR 0,67 sampai 6,6 | FP/24 jam | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §2.3 baris C1 rule | 2026-10-27 | RND_R1 §4.4 | TERUKUR |
| R1-034 | kontrak hyperparameter seed 42, tanpa grid search | pernyataan | RUN-KITA | `docs/V9_PM1_ARCHITECTURE.md:356` ("hyperparam kontrak (seed 42, tanpa grid search)") | 2026-10-27 | RND_R1 §1.2, §4.2 | TERVERIFIKASI |
| R1-035 | 200 | pohon | RUN-KITA | `docs/V9_PM1_ARCHITECTURE.md:356` (RF 200 pohon) | 2026-10-27 | RND_R1 §1.1 | TERVERIFIKASI |
| R1-036 | 3.000 | evaluasi fitness | DERIVASI-ARITMETIK | 30 individu x 100 iterasi x 1 evaluasi per individu per iterasi (sifat algoritma, bukan hasil ukur); dipakai sebagai ilustrasi biaya bawaan | 2026-10-27 | RND_R1 §2.1 sampai §2.14 | TERVERIFIKASI |
| R1-037 | 19.176 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.advengsoft.2013.12.007`, field `is-referenced-by-count` Crossref | 2026-10-27 | RND_R1 §2.1 | TERUKUR |
| R1-038 | 14.089 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.advengsoft.2016.01.008` | 2026-10-27 | RND_R1 §2.2 | TERUKUR |
| R1-039 | 42.382 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1109/icnn.1995.488968` | 2026-10-27 | RND_R1 §2.3 | TERUKUR |
| R1-040 | 4.858 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.advengsoft.2017.07.002` | 2026-10-27 | RND_R1 §2.4 | TERUKUR |
| R1-041 | 3.816 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1080/21642583.2019.1708830` | 2026-10-27 | RND_R1 §2.5 | TERUKUR |
| R1-042 | 6.235 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.future.2019.02.028` | 2026-10-27 | RND_R1 §2.6 | TERUKUR |
| R1-043 | 674 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.knosys.2018.06.001` | 2026-10-27 | RND_R1 §2.7 | TERUKUR |
| R1-044 | 2.990 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.future.2020.03.055` | 2026-10-27 | RND_R1 §2.8, §2.14 | TERUKUR |
| R1-045 | 1.316 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.neucom.2015.06.083` | 2026-10-27 | RND_R1 §2.9 | TERUKUR |
| R1-046 | 2.249 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.knosys.2019.105190` | 2026-10-27 | RND_R1 §2.10 | TERUKUR |
| R1-047 | 367 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.eswa.2020.113702` | 2026-10-27 | RND_R1 §2.11 | TERUKUR |
| R1-048 | 376 | sitasi | RUN-KITA | `refs_registry.md`, DOI `10.1016/j.knosys.2020.106711` | 2026-10-27 | RND_R1 §2.13 | TERUKUR |
| R1-049 | 133 (Shao), 188 (Hu), 136 (Al-Tashi), 210 (Dhiman BEPO), 176 (Neggaz), 110 (Gao) | sitasi | RUN-KITA | `refs_registry.md` baris DOI `10.1016/j.measurement.2020.108580`, `10.1016/j.knosys.2021.107761`, `10.1109/access.2020.3000040`, `10.1016/j.knosys.2020.106560`, `10.1016/j.eswa.2019.113103`, `10.1109/access.2020.3013617` | 2026-10-27 | RND_R1 §2.6, §2.7, §2.8, §2.9, §2.10 | TERUKUR |
| R1-050 | 0,3333 (maksimum); Nyquist 0,1667 | Hz | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §2 (laju sampel maksimum terukur; implikasi VMD/EMD tidak layak) | 2026-10-27 | RND_R1 §2.5, §4.3 | TERUKUR |
| R1-051 | nol rujukan fault diagnosis untuk EO | jumlah | RUN-KITA | `r1_round2.json` grup `gaps.EO_fault` (16 kandidat, tidak ada yang berupa diagnosis getaran dengan EO; yang muncul "Adam optimizer" dan GWO) | 2026-10-27 | RND_R1 §2.10, §4.3 | TERUKUR |
| R1-052 | nol rujukan fault diagnosis atau PdM untuk Horse Herd | jumlah | RUN-KITA | `r1_round2.json` grup `gaps.HORSE_domain` (16 kandidat, tertinggi `10.1016/j.knosys.2020.106711` = paper dasar; sisanya seleksi fitur dan dispatch ekonomi) | 2026-10-27 | RND_R1 §2.13, §4.3 | TERUKUR |
| R1-053 | 55 | DOI | RUN-KITA | `r1_verify_pass2.py`, regex pola backtick atas `docs/RND_R1_METAHEURISTIK.md`, `len(rows)` | 2026-10-27 | RND_R1 §0.4 | TERUKUR |
| R1-054 | 55 dari 55 | DOI resolve 302 | RUN-KITA | `r1_verify_pass2.json` field `layer1_resolve_3xx`; HEAD ke `https://doi.org/<doi>` dengan redirect handler dimatikan | 2026-10-27 | RND_R1 §0.4 | TERUKUR |
| R1-055 | 55 dari 55 | metadata Crossref 200 | RUN-KITA | `r1_verify_pass2.json` field `layer2_crossref_200`; GET `https://api.crossref.org/works/<doi>` | 2026-10-27 | RND_R1 §0.4 | TERUKUR |
| R1-056 | 32 / 16 / 7 | halaman penerbit 200/403/202 | RUN-KITA | `r1_publisher_status.json` field `status_counts`; GET `https://doi.org/<doi>` dengan redirect diikuti dan UA browser | 2026-10-27 | RND_R1 §0.4, §5 | TERUKUR |
| R1-057 | 309 dari 309 | entri `doi_checks` bernilai 302 | RUN-KITA | `r1_check309.py` atas `lit_r1.json`: `len(d["doi_checks"])` = 309 dan seluruh nilai `http` = 302 | 2026-10-27 | RND_R1 §0.1, §0.4 | TERUKUR |
| R1-058 | 4 (pass 2), 9 total | pikiran sequ-mcp | RUN-KITA | respons `mcp__sequentialthinking__sequentialthinking`, `thoughtHistoryLength` 1 sampai 4 pada pass verifikasi | 2026-10-27 | RND_R1 §0.4 | TERUKUR |
| R1-059 | `issued` = `[null]`; `created` = 2002-11-19 | tanggal Crossref | JURNAL | Crossref `10.1109/icnn.1995.488968`, field `issued`, `created`, `type` (`proceedings-article`), `container-title` (`Proceedings of ICNN'95`) | 2026-10-27 | RND_R1 §0.2, §0.4 | TERVERIFIKASI |
| R1-060 | 58 | baris DOI di registry | RUN-KITA | `r1_diff_registry.py` atas `refs_registry.md`: baris tabel yang memuat pola DOI, dihitung unik | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-061 | 55 dikutip, 3 tidak dikutip | DOI | RUN-KITA | `r1_diff_registry.py`: himpunan DOI dokumen (regex backtick) dibandingkan himpunan registry; selisih `10.1007/s11761-023-00382-8`, `10.1038/s41598-024-53141-w`, `10.3390/fuels6020033` | 2026-10-27 | RND_R1 §0.1 | TERUKUR |
| R1-062 | 54 diganti 58 | koreksi angka | RUN-KITA | `r1_diff_registry.py`; angka 54 pada versi dokumen sebelumnya berasal dari keadaan registry sebelum `r1_registry.py` selesai menambah baris | 2026-10-27 | RND_R1 §0.1 | TERUKUR |

## Bagian R3: dekomposisi sinyal dan kernel (kartu `t_1fe4eed0`)

Dokumen pendamping: `docs/RND_R3_VMD_SVM.md`. Sumber angka: `m3_decomp.json` (timestamp `2026-10-27T04:52:02`), `m4_kanal_konstan.json`, dan `docs/RND_D0_DATA_FEASIBILITY.md` §2. Berkas pengukur `m3` tidak ditemukan di workspace, sehingga baris dari berkas itu berstatus TERUKUR-SATU-JALUR (keluaran ada, skrip tidak ada); nilai laju sampel dan jumlah sampel cocok dengan pengukur D0 yang lain. Perintah verifikasi DOI tersimpan: `verify_doi_r3.sh`, `verify_doi_r3b.sh`, `verify_doi_r3c.sh`, keluaran `doi_verify_r3.tsv` dan `doi_verify_r3c.tsv`.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R3-01 | 0,3333 | Hz | RUN-KITA | `m3_decomp.json` `A_cadence_dekomposisi` kanal F-15_S `VIBLAT_RT`/`CRPM_RT`/`SHKRSK_RT`, `laju_hz`; sama dengan D0 §2 | 2026-10-27 | RND_R3 §1.1, §7 | TERUKUR |
| R3-02 | 0,1667 | Hz | RUN-KITA | `m3_decomp.json` field `nyquist_hz` pada kanal laju 0,3333 Hz (fs/2) | 2026-10-27 | RND_R3 §1.1, §4 | TERUKUR |
| R3-03 | 0,0167 sampai 0,3333 | Hz | RUN-KITA | `m3_decomp.json`: F-14 `VIBLAT_RT` `laju_hz` 0,016653 sampai F-15_S 0,3333 | 2026-10-27 | RND_R3 §1.1, §4 | TERUKUR |
| R3-04 | 141.114 | sampel | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `n_sampel` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-05 | 4.126 | segmen | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `n_segmen` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-06 | 5.457 | sampel | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `segmen_terpanjang_sampel` (4,5475 jam) | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-07 | 475/214/91 | jendela | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `jendela.256/512/1024` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-08 | 137.170 / 4.139 / 5.413 / 464/208/87 | campuran | RUN-KITA | `m3_decomp.json` F-15_S `CRPM_RT`: `n_sampel`/`n_segmen`/`segmen_terpanjang_sampel`/`jendela` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-09 | 152.923 / 5.177 / 5.458 / 511/232/97 | campuran | RUN-KITA | `m3_decomp.json` F-15_S `SHKRSK_RT` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-10 | 2.247 / 60,048 / 1.551 / 4 sampel / 0 jendela | campuran | RUN-KITA | `m3_decomp.json` F-14 `VIBLAT_RT`: `n_sampel`/`dt_median_s`/`n_segmen`/`segmen_terpanjang_sampel`/`jendela` (256,512,1024 semuanya 0) | 2026-10-27 | RND_R3 §1.1, §1.5 | TERUKUR-SATU-JALUR |
| R3-11 | 21.643 / 5.409 / 1.644 / 31/6/2 | campuran | RUN-KITA | `m3_decomp.json` F-14 `SHKRSK_RT` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-12 | 45.927 / 67 / 3.828 / 149/66/26 | campuran | RUN-KITA | `m3_decomp.json` F-9_A `SHKRSK_RT` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-13 | 69.192 / 327 / 3.484 / 179/73/25 | campuran | RUN-KITA | `m3_decomp.json` F-10 `SHKRSK_RT` | 2026-10-27 | RND_R3 §1.1 | TERUKUR-SATU-JALUR |
| R3-14 | 6,108e-05 | Hz | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `spektral.freq_resolution_hz` | 2026-10-27 | RND_R3 §1.2 | TERUKUR-SATU-JALUR |
| R3-15 | 0,005559 | Hz | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `spektral.dominant_freq_hz` | 2026-10-27 | RND_R3 §1.2 | TERUKUR-SATU-JALUR |
| R3-16 | 0,1246 | fraksi | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `spektral.peak_share` | 2026-10-27 | RND_R3 §1.2 | TERUKUR-SATU-JALUR |
| R3-17 | 0,9586 | fraksi daya | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `spektral.frac_power_below_0p05hz` | 2026-10-27 | RND_R3 §1.2, §7 | TERUKUR-SATU-JALUR |
| R3-18 | 0,9528 | fraksi energi | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `dekomposisi.wavelet.bands` level `a5`, `energy_frac` (tidak ternormalisasi) | 2026-10-27 | RND_R3 §1.2, §8 | TERUKUR-SATU-JALUR |
| R3-19 | 1,192 | fraksi energi (jumlah) | DERIVASI-ARITMETIK | jumlah `energy_frac` seluruh pita wavelet db4 level 5 pada F-15_S `VIBLAT_RT`: 0,9528+0,1437+0,0536+0,0217+0,0118+0,0082 | 2026-10-27 | RND_R3 §1.2, §8 | TERUKUR |
| R3-20 | 5 | IMF | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `dekomposisi.emd.n_imfs` | 2026-10-27 | RND_R3 §1.2 | TERUKUR-SATU-JALUR |
| R3-21 | 0,0107 / 0,6809 | Hz / fraksi | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `imfs[0]` IMF1: `f_hz` 0,0107421875, `energy_frac` 0,6809 | 2026-10-27 | RND_R3 §1.2 | TERUKUR-SATU-JALUR |
| R3-22 | 2,45 | fraksi energi (jumlah) | DERIVASI-ARITMETIK | jumlah `energy_frac` 5 IMF pada F-15_S `VIBLAT_RT`: 0,6809+1,3647+0,1948+0,1969+0,0142 | 2026-10-27 | RND_R3 §1.2, §8 | TERUKUR |
| R3-23 | 0,0205 sampai 0,0043 | fraksi residu | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `vmd[].resid_frac` pada alpha 500, K 2 sampai K 6 | 2026-10-27 | RND_R3 §1.3 | TERUKUR-SATU-JALUR |
| R3-24 | 0,1125 sampai 0,0449 | fraksi residu | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `vmd[].resid_frac` pada alpha 5000, K 2 sampai K 6 | 2026-10-27 | RND_R3 §1.3 | TERUKUR-SATU-JALUR |
| R3-25 | 1,27e-09 sampai 6,45e-06 | Hz | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `vmd[].spacing_min_hz` minimum dan maksimum pada 15 kombinasi | 2026-10-27 | RND_R3 §1.3, §7 | TERUKUR-SATU-JALUR |
| R3-26 | 0,0833 / 0,1111 / 0,125 / 0,1333 | Hz | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `vmd[].cf_max_hz` untuk K=2..5 | 2026-10-27 | RND_R3 §1.3 | TERUKUR-SATU-JALUR |
| R3-27 | (K-1) x fs / (2K) | rumus | DERIVASI-ARITMETIK | kecocokan `cf_max_hz` dengan grid inisialisasi seragam: K=2 -> 0,0833; K=3 -> 0,1111; K=4 -> 0,125; K=5 -> 0,1333 pada fs 0,3333 Hz | 2026-10-27 | RND_R3 §1.3 | TERUKUR |
| R3-28 | 0,0120 sampai 0,3533 | detik | RUN-KITA | `m3_decomp.json` F-15_S `VIBLAT_RT` `vmd[].runtime_s` | 2026-10-27 | RND_R3 §1.3 | TERUKUR-SATU-JALUR |
| R3-29 | 105 | percobaan VMD | RUN-KITA | `grep -c '"alpha":' m3_decomp.json` = 105 (7 kanal x 15 kombinasi) | 2026-10-27 | RND_R3 §1.3, §7 | TERUKUR |
| R3-30 | 75 | percobaan gagal | RUN-KITA | `grep -c '"error":' m3_decomp.json` = 75; lima rentang baris 9772-9842, 9919-9989, 10064-10134, 10211-10281, 10358-10428 | 2026-10-27 | RND_R3 §1.3, §7 | TERUKUR |
| R3-31 | 23.922 | jendela | RUN-KITA | `m3_decomp.json` `C_biaya.svm.n`; sama dengan D0 §1 (dataset `vib`) | 2026-10-27 | RND_R3 §2.1, §2.2 | TERUKUR |
| R3-32 | 10 | fitur | RUN-KITA | `m3_decomp.json` `C_biaya.svm.n_fitur` | 2026-10-27 | RND_R3 §2.1 | TERUKUR-SATU-JALUR |
| R3-33 | 5.429 | positif | RUN-KITA | `m3_decomp.json` `C_biaya.svm.positif`; sama dengan D0 §1 (prevalensi 22,7%) | 2026-10-27 | RND_R3 §2.1 | TERUKUR |
| R3-34 | 0,8876 / 0,8041 / 0,6803 / 0,8448 | AUC | RUN-KITA | `m3_decomp.json` `C_biaya.svm.tanpa_standardisasi.auc` untuk F-14/F-15A/F-15_S/F-5 | 2026-10-27 | RND_R3 §2.1 | TERUKUR-SATU-JALUR |
| R3-35 | 0,8245 | median AUC | RUN-KITA | `m3_decomp.json` `C_biaya.svm.tanpa_standardisasi.median_auc` | 2026-10-27 | RND_R3 §2.1, §5, §7 | TERUKUR-SATU-JALUR |
| R3-36 | 0,7592 | median AUC | RUN-KITA | `m3_decomp.json` `C_biaya.svm.dengan_standardisasi.median_auc` | 2026-10-27 | RND_R3 §2.1 | TERUKUR-SATU-JALUR |
| R3-37 | 0,0653 | selisih AUC | DERIVASI-ARITMETIK | 0,8244588215376123 dikurangi 0,7591984952446993 | 2026-10-27 | RND_R3 §2.1, §8 | TERUKUR |
| R3-38 | 36,36 / 16,36 / 7,99 / 0,05 | detik | RUN-KITA | `m3_decomp.json` `C_biaya.svm`: `total_fit_s` tanpa dan dengan standardisasi, `rbf_all.fit_s`, `linear_all.fit_s` | 2026-10-27 | RND_R3 §2.1, §7 | TERUKUR-SATU-JALUR |
| R3-39 | 0,8431 / 2,7576 / 14,5964 / 49,2067 / 220,3579 / 864,2339 | ms per pasangan | RUN-KITA | `m3_decomp.json` `C_biaya.dtw[].ms_pasangan` untuk n = 32, 64, 128, 256, 512, 1024 | 2026-10-27 | RND_R3 §2.2 | TERUKUR-SATU-JALUR |
| R3-40 | 134,01 / 438,33 / 2.320,17 / 7.821,65 / 35.027,00 / 137.374,35 | jam | RUN-KITA | `m3_decomp.json` `C_biaya.dtw[].est_jam_1nn_23922` (estimasi 1-NN atas 23.922 jendela) | 2026-10-27 | RND_R3 §2.2, §7 | TERUKUR-SATU-JALUR |
| R3-41 | 0,00039 / 0,00044 / 0,00076 | detik per query | RUN-KITA | `m3_decomp.json` `C_biaya.matrix_profile[].satu_query_s` untuk n = 3.000/6.000/12.000, m=60 | 2026-10-27 | RND_R3 §2.3 | TERUKUR-SATU-JALUR |
| R3-42 | 10,4107 / 10,3981 / 10,2860 | jarak minimum | RUN-KITA | `m3_decomp.json` `C_biaya.matrix_profile[].profil_min` | 2026-10-27 | RND_R3 §2.3 | TERUKUR-SATU-JALUR |
| R3-43 | 69.192 / 4 / 69.062 / 99,81% | baris, nilai unik, nol, persen | RUN-KITA | `m4_kanal_konstan.json` F-10 `SHKRSK_RT`: `n`, `n_unik`, `5_nilai_teratas[0][1]`, `fraksi_dominan` | 2026-10-27 | RND_R3 §4 | TERUKUR |
| R3-44 | 141.114 / 36 / 16,087025 / 40,57% | baris, nilai unik, nilai dominan, persen | RUN-KITA | `m4_kanal_konstan.json` F-15_S `VIBLAT_RT` | 2026-10-27 | RND_R3 §4 | TERUKUR |
| R3-45 | 1 kHz sampai 10 kHz | Hz | KONVENSI | usulan syarat akuisisi `RND_R3` §4, diturunkan dari kebutuhan Nyquist di atas pita BPFO/BPFI (Randall & Antoni 2011 DOI `10.1016/j.ymssp.2010.07.017`); bukan angka terukur pada data ini | 2026-10-27 | RND_R3 §4 | USULAN-SYARAT |
| R3-46 | 60.000 | sampel | KONVENSI | usulan syarat segmen: 60 detik x 1.000 Hz, `RND_R3` §4; bukan angka terukur | 2026-10-27 | RND_R3 §4 | USULAN-SYARAT |
| R3-47 | 469 x 27 | jendela x fitur | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` §6 (tool wear bengkel), sudah tercatat pada bagian D0 | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-48 | 0,441 sampai 0,912 | AUPRC | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris `vib` (RF AUPRC antar fold) | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-49 | 0,87 sampai 0,95 | presisi | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris `vib` (rule P stabil) dan `code/v9_i1_pipeline.py` REGISTRY `vib.heads.rule_display.badge_far` (P 0,87-0,95) | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-50 | 2.091 ke 927 | jumlah FP | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris `ssi` (FP-cut hybrid, -55,7%, 9/9 well) | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-51 | 0,67 sampai 6,6 | FAR per 24 jam | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris `shk` (rule FAR, lolos <= 6 di 7/9 fold) | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-52 | 0,516 sampai 0,612 | AUPRC | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` §1 baris `tool_wear` (canary AUPRC antar alat) | 2026-10-27 | RND_R3 §5 | TERUKUR |
| R3-53 | 19 | rujukan ber-DOI | RUN-KITA | `verify_doi_r3.sh` (12 DOI) dan `verify_doi_r3c.sh` (7 DOI tambahan), semua `doi.org` = 302 dan Crossref `status: ok` | 2026-10-27 | RND_R3 §6 | TERUKUR |
| R3-54 | 2 | rujukan salah label | JURNAL | Crossref `10.1007/978-3-540-30075-5_46` = Bellatreche 2004 (bukan Ratanamahatana & Keogh); Crossref `10.1098/rsta.2010.0331` = Ellis 2011 (bukan Randall & Antoni) | 2026-10-27 | RND_R3 §2.2, §6 | TERVERIFIKASI |
| R3-55 | 5 | pikiran sequ-mcp | RUN-KITA | respons `mcp__sequentialthinking__sequentialthinking`, `thoughtHistoryLength` 1 sampai 5 | 2026-10-27 | RND_R3 §0 | TERUKUR |

---

## Bagian R6: metrik, uji statistik, dan desain eksperimen (kartu `t_5ffc95c0`)

Dokumen pendamping: `docs/RND_R6_METRIK.md` (9 bagian, 0 sampai 8). Sumber angka: `rnd_r6_RESULTS.json` (19.595 B, 12 bagian S2 sampai S11), `rnd_r6_SUPPLEMENT.json` (8.727 B, 7 bagian S5FIX dan S12 sampai S16), `doi_verify_r6.json` (10 rujukan), ditambah `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` untuk hitungan per fold ssi. Kedua JSON dihasilkan `rnd_r6_compute.py` dan `rnd_r6_supplement.py` di workspace kartu dan dapat dijalankan ulang.

Setiap baris yang bersumber dari JSON di-assert oleh `verify_r6_ledger_rows.py` terhadap path yang tertulis di kolom rujukan, dan baris tidak ditulis bila assert gagal. Baris berkelas DERIVASI di-assert lewat rumusnya (mis. 3,6889 x 24 / (786/60) = 6,758), bukan lewat angka bulat yang sudah ditampilkan. Baris KONVENSI dan BELUM tidak punya assert karena tidak ada nilai hasil ukur yang bisa diuji.

Jumlah baris: 134 (R6-01 sampai R6-134). Tanggal akses seluruh baris: 2026-10-27 (WIB).

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R6-01 | 1440 | faktor jendela 1 menit ke 24 jam | DERIVASI | 24 x 60 = 1440; implementasi `code/v9_e_ML_01_train.py:20` dan `:118` (`far24 = 1440.0 * fp / n_neg`) | 2026-10-27 | §1.1 | TERVERIFIKASI (kode + aritmetika) |
| R6-02 | 24 x FP / jam_neg | alarm palsu per 24 jam | KONVENSI (rumus internal) | `code/v9_e_STAT_01_hyd_ki.py:70` (`far_24 = (fp / jam_neg * 24)`); L-27 bagian P0 | 2026-10-27 | §1.1, §2.7 | TERVERIFIKASI (kode terbaca) |
| R6-03 | 26 | fold | RUN-KITA | `rnd_r6_RESULTS.json` S2b_reproduksi_far_ml_tau05.n_fold | 2026-10-27 | §1.1 | TERUKUR |
| R6-04 | 5,684e-14 | selisih FAR per 24 jam | RUN-KITA | `rnd_r6_RESULTS.json` S2b_reproduksi_far_ml_tau05.maks_selisih_abs | 2026-10-27 | §1.1 | TERUKUR |
| R6-05 | 1,9229 | per 24 jam | RUN-KITA | `rnd_r6_RESULTS.json` S2_reproduksi_far_hyd_ki.maks_selisih_abs (fold F-12) | 2026-10-27 | §1.1 | TERUKUR |
| R6-06 | 0,0228 | per 24 jam | RUN-KITA | `rnd_r6_RESULTS.json` S2...folds[3].selisih_abs (F-15A, nilai terkecil dari 9 fold) | 2026-10-27 | §1.1 | TERUKUR |
| R6-07 | 98,0195 | per 24 jam | RUN-KITA | `rnd_r6_RESULTS.json` S2...folds[1].far_tersimpan (F-12) | 2026-10-27 | §1.1 | TERUKUR |
| R6-08 | 96,0966 | per 24 jam | RUN-KITA | `rnd_r6_RESULTS.json` S2...folds[1].far_recompute (F-12) | 2026-10-27 | §1.1 | TERUKUR |
| R6-09 | 1,34919 | alarm palsu per jam negatif | DERIVASI | 32,38064200749552 / 24 = 1,3491934 dari S2...folds[0].far_tersimpan (F-10) | 2026-10-27 | §1.1 | TERVERIFIKASI (aritmetika) |
| R6-10 | 102,28 | jam negatif tersirat | DERIVASI | 138 / 1,34919 = 102,284 dari S2...folds[0].fp dibagi laju tersirat | 2026-10-27 | §1.1 | TERVERIFIKASI (aritmetika) |
| R6-11 | 102,95 | jam negatif | RUN-KITA | `rnd_r6_RESULTS.json` S2...folds[0].jam_neg; sama dengan 6177/60 | 2026-10-27 | §1.1 | TERUKUR |
| R6-12 | 2,0 | persen relatif | DERIVASI | 1,9229 / 96,096579 = 2,001 persen (selisih maksimum dibagi nilai hitung ulang) | 2026-10-27 | §1.1 | TERVERIFIKASI (aritmetika) |
| R6-13 | 32,38 | per 24 jam (nilai hyd terendah) | RUN-KITA | `rnd_r6_RESULTS.json` S4_poisson_ci_far_hyd_ki.folds[0].far_24jam | 2026-10-27 | §1.1, §2.7 | TERUKUR |
| R6-14 | 6 | alarm palsu per 24 jam (ambang) | KONVENSI | `docs/RND_ALGO_RESEARCH_PLAN.md` §6 butir 2; L-26 bagian P0; `code/v9_eval_a_01_compute.py:37` | 2026-10-27 | §1.1, §3.4, §4 | BELUM (ambang keputusan, bukan hasil ukur) |
| R6-15 | 10 | menit (horizon H) | KONVENSI | `code/v9_d1_02_rig_windows.py:31` (`W = 10`); `code/v9_e_RULE_04_hyd_k2.py:30` (`H = 10`); L-28 | 2026-10-27 | §1.2, §1.3 | BELUM |
| R6-16 | 281 | onset | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.total_onsets (sama dengan S10_b1_onset.total_onsets) | 2026-10-27 | §1.2, §3.4 | TERUKUR |
| R6-17 | 93; 61; 55; 72 | onset per well (F-10, F-14, F-9, F-9_A) | RUN-KITA | `rnd_r6_RESULTS.json` S10_b1_onset.folds[0..3].onsets | 2026-10-27 | §1.2 | TERUKUR |
| R6-18 | 0,1281 | proporsi | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.b1_engine_pool | 2026-10-27 | §1.2 | TERUKUR |
| R6-19 | [0,0940; 0,1723] | proporsi | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.b1_engine_wilson | 2026-10-27 | §1.2 | TERUKUR |
| R6-20 | 0,8719 | proporsi | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.b1_persistence_pool | 2026-10-27 | §1.2 | TERUKUR |
| R6-21 | [0,8277; 0,9060] | proporsi | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.b1_persistence_wilson | 2026-10-27 | §1.2 | TERUKUR |
| R6-22 | 0,0036 dan 0,356 | proporsi per onset dan poin persen | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.resolusi_b1_min (0,00356) dan resolusi_b1_persen (0,356); 1/281 = 0,0035587 | 2026-10-27 | §1.2, §3.4 | TERUKUR |
| R6-23 | 1,82 | poin persen per onset (F-9, 55 onset) | DERIVASI | 100 / 55 = 1,818 dari S10_b1_onset.folds[2].onsets | 2026-10-27 | §1.2, §3.4 | TERVERIFIKASI (aritmetika) |
| R6-24 | 7,0 | menit (median TLead F-10) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.folds[0].tlead | 2026-10-27 | §1.3 | TERUKUR |
| R6-25 | [3,0; 10,0] | menit (IQR TLead F-10) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.folds[0].iqr | 2026-10-27 | §1.3 | TERUKUR |
| R6-26 | 2,5 dan [1,75; 5,5] | menit (median dan IQR TLead F-14) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.folds[1].tlead dan .iqr | 2026-10-27 | §1.3 | TERUKUR |
| R6-27 | 8,0 dan [2,0; 10,0] | menit (median dan IQR TLead F-9_A) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.folds[3].tlead dan .iqr | 2026-10-27 | §1.3 | TERUKUR |
| R6-28 | 15; 8; 13; 0 | onset terdeteksi per well | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S12_b1_wilson.folds[0..3].det | 2026-10-27 | §1.3 | TERUKUR |
| R6-29 | 0,8986 | proporsi (presisi F-10) | RUN-KITA | `rnd_r6_RESULTS.json` S3_wilson_presisi_hyd_ki.folds[0].presisi | 2026-10-27 | §1.4 | TERUKUR |
| R6-30 | 0,18412 | proporsi (prevalensi F-10) | RUN-KITA | `rnd_r6_RESULTS.json` S2...folds[0].prev (0,184124) | 2026-10-27 | §1.4 | TERUKUR |
| R6-31 | 0,6313 | proporsi (presisi F-14) | RUN-KITA | `rnd_r6_RESULTS.json` S3...folds[2].presisi | 2026-10-27 | §1.4 | TERUKUR |
| R6-32 | 0,08317 | proporsi (prevalensi F-14) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[2].prev | 2026-10-27 | §1.4 | TERUKUR |
| R6-33 | 150,205 | rasio (lift ssi F-7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[6].lift | 2026-10-27 | §1.6 | TERUKUR |
| R6-34 | 0,00305 | proporsi (prevalensi ssi F-7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[6].prev | 2026-10-27 | §1.6 | TERUKUR |
| R6-35 | 327,333 | rasio (plafon ssi F-7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[6].plafon_1_per_prev; dihitung dari prevalensi tak dibulatkan 0,003055 | 2026-10-27 | §1.6 | TERUKUR |
| R6-36 | 327,87 | rasio (plafon dari prevalensi bulat) | DERIVASI | 1 / 0,00305 = 327,8689; dicatat supaya angka 327,3 pada JSON tidak tampak bertentangan | 2026-10-27 | §1.6 | TERVERIFIKASI (aritmetika) |
| R6-37 | 12,252 | rasio (lift ssi F-15A) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[3].lift | 2026-10-27 | §1.6 | TERUKUR |
| R6-38 | 0,00515 | proporsi (prevalensi ssi F-15A) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[3].prev | 2026-10-27 | §1.6 | TERUKUR |
| R6-39 | 194,194 | rasio (plafon ssi F-15A) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[3].plafon_1_per_prev | 2026-10-27 | §1.6 | TERUKUR |
| R6-40 | 0,4589 | proporsi (AUPRC ssi F-7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14b_lift_ml_rf.ssi[6].auprc | 2026-10-27 | §1.6 | TERUKUR |
| R6-41 | 3 | jendela positif (ssi F-7) | RUN-KITA | `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` folds[6].pos_test; menggantikan angka 9 pada draf pertama dokumen | 2026-10-27 | §1.6 | TERUKUR |
| R6-42 | 982 dan 979 | jendela uji dan jendela negatif (ssi F-7) | RUN-KITA | `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` folds[6].n_test dan folds[6].models.rf.tau_metrics.0.5.n_neg | 2026-10-27 | §1.6 | TERUKUR |
| R6-43 | 6,103 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[5].lift (well F-5) | 2026-10-27 | §1.6 | TERUKUR |
| R6-44 | 10,196 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[5].plafon_1_per_prev (well F-5) | 2026-10-27 | §1.6 | TERUKUR |
| R6-45 | 5,340 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[2].lift (well F-14) | 2026-10-27 | §1.6 | TERUKUR |
| R6-46 | 12,024 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[2].plafon_1_per_prev (well F-14) | 2026-10-27 | §1.6 | TERUKUR |
| R6-47 | 4,576 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[0].lift (well F-10) | 2026-10-27 | §1.6 | TERUKUR |
| R6-48 | 5,431 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[0].plafon_1_per_prev (well F-10) | 2026-10-27 | §1.6 | TERUKUR |
| R6-49 | 4,320 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[3].lift (well F-15A) | 2026-10-27 | §1.6 | TERUKUR |
| R6-50 | 8,820 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[3].plafon_1_per_prev (well F-15A) | 2026-10-27 | §1.6 | TERUKUR |
| R6-51 | 3,609 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[8].lift (well F-9_A) | 2026-10-27 | §1.6 | TERUKUR |
| R6-52 | 6,665 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[8].plafon_1_per_prev (well F-9_A) | 2026-10-27 | §1.6 | TERUKUR |
| R6-53 | 3,572 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[4].lift (well F-15_S) | 2026-10-27 | §1.6 | TERUKUR |
| R6-54 | 8,414 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[4].plafon_1_per_prev (well F-15_S) | 2026-10-27 | §1.6 | TERUKUR |
| R6-55 | 3,331 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[1].lift (well F-12) | 2026-10-27 | §1.6 | TERUKUR |
| R6-56 | 5,182 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[1].plafon_1_per_prev (well F-12) | 2026-10-27 | §1.6 | TERUKUR |
| R6-57 | 2,984 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[6].lift (well F-7) | 2026-10-27 | §1.6 | TERUKUR |
| R6-58 | 5,895 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[6].plafon_1_per_prev (well F-7) | 2026-10-27 | §1.6 | TERUKUR |
| R6-59 | 2,388 | rasio (lift hyd K-i persistence) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[7].lift (well F-9) | 2026-10-27 | §1.6 | TERUKUR |
| R6-60 | 3,820 | rasio (plafon 1/prevalensi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S14_lift_hyd_ki.folds[7].plafon_1_per_prev (well F-9) | 2026-10-27 | §1.6 | TERUKUR |
| R6-61 | 0,8186 | proporsi (AUC sintetis) | RUN-KITA | `rnd_r6_RESULTS.json` S9_delong.uji_sintetis.auc | 2026-10-27 | §2.2 | TERUKUR (uji kewajaran fungsi, bukan kinerja engine) |
| R6-62 | 0,0141 | proporsi (galat baku sintetis) | RUN-KITA | `rnd_r6_RESULTS.json` S9_delong.uji_sintetis.se | 2026-10-27 | §2.2 | TERUKUR |
| R6-63 | [0,7910; 0,8463] | proporsi (CI95 sintetis) | RUN-KITA | `rnd_r6_RESULTS.json` S9_delong.uji_sintetis.ci95 | 2026-10-27 | §2.2 | TERUKUR |
| R6-64 | 9 | well (unit independen) | RUN-KITA | `docs/RND_D0_DATA_FEASIBILITY.md` (9 well) dan S7/S15 desain | 2026-10-27 | §2.1, §2.3 | TERUKUR |
| R6-65 | 800 | jendela negatif per well (simulasi) | RUN-KITA | `rnd_r6_RESULTS.json` S7_mde_delta_auprc_simulasi.desain; S15_mde_delta_auprc_halus.desain | 2026-10-27 | §2.3 | TERUKUR |
| R6-66 | 120 | resampel bootstrap | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[].n_boot = 120; catatan: string desain menulis 150 kali sehingga nilai 120 yang dipakai | 2026-10-27 | §2.3 | TERUKUR |
| R6-67 | 0,0056; 0,0090; 0,0145 | delta AUPRC (prevalensi 1,69 persen) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[0..2].delta_median | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-68 | 0,30; 0,412; 0,55 | daya | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[0..2].daya | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-69 | 0,0232 | delta AUPRC (prevalensi 1,69 persen, pemisahan 0,50) | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[0].delta_median | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-70 | 0,792 | daya | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[0].daya | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-71 | 0,0804 dan 0,1904 | delta AUPRC | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[1].delta_median dan hasil[2].delta_median | 2026-10-27 | §2.3 | TERUKUR |
| R6-72 | 1,0 | daya (pada delta 0,0804 dan 0,1904) | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[1].daya dan hasil[2].daya | 2026-10-27 | §2.3 | TERUKUR |
| R6-73 | 0,0192 | delta AUPRC (prevalensi 13,66 persen, pemisahan 0,15) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[3].delta_median | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-74 | 0,838 | daya | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[3].daya | 2026-10-27 | §2.3, §3.3 | TERUKUR |
| R6-75 | 0,0346 dan 0,0525 | delta AUPRC (prevalensi 13,66 persen) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[4].delta_median dan hasil[5].delta_median | 2026-10-27 | §2.3 | TERUKUR |
| R6-76 | 0,0829 | delta AUPRC (prevalensi 13,66 persen, pemisahan 0,50) | RUN-KITA | `rnd_r6_RESULTS.json` S7...hasil[3].delta_median | 2026-10-27 | §2.3 | TERUKUR |
| R6-77 | 0,0453; 0,0260; 0,57 | proporsi dan rasio (lebar CI jendela lawan blok) | RUN-KITA | `rnd_r6_RESULTS.json` S7b_lebar_ci_jendela_vs_blok.lebar_ci95_jendela, .lebar_ci95_blok_well, .rasio | 2026-10-27 | §2.3, §8 | TERUKUR |
| R6-78 | 0,0321 dan 0,1024 | proporsi (lebar CI95 presisi terendah dan terlebar) | RUN-KITA | `rnd_r6_RESULTS.json` S3_wilson_presisi_hyd_ki.lebar_min dan .lebar_maks | 2026-10-27 | §2.4 | TERUKUR |
| R6-79 | 1361 dan 298 | alarm (penyebut presisi) | RUN-KITA | `rnd_r6_RESULTS.json` S3...folds[0].n (F-10) dan folds[8].n (F-9_A) | 2026-10-27 | §2.4 | TERUKUR |
| R6-80 | [0,5836; 0,9135] | proporsi (batas bawah dan atas seluruh selang presisi) | RUN-KITA | `rnd_r6_RESULTS.json` S3...folds[4].wilson_lo (0,5836) dan folds[0].wilson_hi (0,9135) | 2026-10-27 | §2.4 | TERUKUR |
| R6-81 | 6 sampai 10 | poin persen (jarak presisi yang belum dapat dibedakan) | DERIVASI | lebar CI95 0,0321 sampai 0,1024 pada S3 dikonversi ke 3,2 sampai 10,2 poin persen | 2026-10-27 | §2.4 | TERVERIFIKASI (aritmetika) |
| R6-82 | 3,0859 | rasio odds | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S13_fisher_presisi.odds_ratio | 2026-10-27 | §2.5 | TERUKUR |
| R6-83 | 0,0 | p dua sisi (underflow float64, batas sebenarnya di bawah 2,2e-308) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S13_fisher_presisi.p_fisher_dua_sisi | 2026-10-27 | §2.5 | TERUKUR |
| R6-84 | 1223/138 dan 1143/398 | hitungan TP/FP | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S13_fisher_presisi.tabel.F-10 dan .F-12 | 2026-10-27 | §2.5 | TERUKUR |
| R6-85 | 0,125 | p minimum yang mungkin (n = 4) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.4.p_min_mungkin | 2026-10-27 | §2.6, §3.1 | TERUKUR |
| R6-86 | 0 | daya (n = 4 pada semua konkordansi) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.4.daya_analitik | 2026-10-27 | §2.6, §3.1 | TERUKUR |
| R6-87 | 7 | well sepakat minimum (n = 7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.7.k_min_sepakat | 2026-10-27 | §2.6 | TERUKUR |
| R6-88 | 0,015625 | p kritis (n = 7, k = 7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.7.p_krit | 2026-10-27 | §2.6 | TERUKUR |
| R6-89 | 8 | well sepakat minimum (n = 9) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.9.k_min_sepakat | 2026-10-27 | §2.6, §3.1 | TERUKUR |
| R6-90 | 0,039063 | p kritis (n = 9, k = 8) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.9.p_krit | 2026-10-27 | §2.6 | TERUKUR |
| R6-91 | 0,003906 | p minimum yang mungkin (n = 9) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.9.p_min_mungkin | 2026-10-27 | §2.6 | TERUKUR |
| R6-92 | 0,0824; 0,2097; 0,4783; 1,0 | daya pada konkordansi 0,7; 0,8; 0,9; 1,0 (n = 7) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.7.daya_analitik | 2026-10-27 | §2.6, §3.1 | TERUKUR |
| R6-93 | 0,1960; 0,4362; 0,7748; 1,0 | daya pada konkordansi 0,7; 0,8; 0,9; 1,0 (n = 9) | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S5FIX_uji_tanda.n_well.9.daya_analitik | 2026-10-27 | §2.6, §3.1 | TERUKUR |
| R6-94 | 5; 8; 10 | k minimum pada versi cacat (n = 4, 7, 9) | RUN-KITA | `rnd_r6_RESULTS.json` S5_uji_tanda_unit_well.n_well.4/7/9.k_min_sepakat; cacat karena k = n+1 | 2026-10-27 | §2.6 | TERUKUR (bukti bug, bukan hasil sah) |
| R6-95 | 1,25; 1,1429; 1,1111 | proporsi pada versi cacat (n = 4, 7, 9) | RUN-KITA | `rnd_r6_RESULTS.json` S5_uji_tanda_unit_well.n_well.4/7/9.proporsi_min; proporsi di atas 1 adalah penanda mustahil | 2026-10-27 | §2.6 | TERUKUR (bukti bug) |
| R6-96 | [27,03; 38,01] | per 24 jam (CI95 eksak F-10) | RUN-KITA | `rnd_r6_RESULTS.json` S4...folds[0].poisson_lo dan .poisson_hi | 2026-10-27 | §2.7 | TERUKUR |
| R6-97 | 110,71 | per 24 jam (F-7) | RUN-KITA | `rnd_r6_RESULTS.json` S4...folds[6].far_24jam | 2026-10-27 | §2.7 | TERUKUR |
| R6-98 | [93,21; 128,26] | per 24 jam (CI95 eksak F-7) | RUN-KITA | `rnd_r6_RESULTS.json` S4...folds[6].poisson_lo dan .poisson_hi | 2026-10-27 | §2.7 | TERUKUR |
| R6-99 | 1,22 dan 1,60 | rasio batas atas terhadap batas bawah | RUN-KITA | `rnd_r6_RESULTS.json` S4...folds[1].rasio_hi_lo (1,22) dan folds[7].rasio_hi_lo (1,60) | 2026-10-27 | §2.7 | TERUKUR |
| R6-100 | 20 sampai 160 | jam negatif (rentang paparan) | DERIVASI | jam_neg terendah 19,883 (F-9, S2...folds[7]) dan tertinggi 158,933 (F-14, S2...folds[2]) | 2026-10-27 | §2.7 | TERVERIFIKASI (aritmetika dari JSON) |
| R6-101 | 4; 3; 3; 3 | jumlah uji dan jumlah signifikan (mentah; Holm; BH) keluarga F1 | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1_engine_ml_rf_tau05.n_uji, .n_sig_mentah, .n_sig_holm, .n_sig_bh | 2026-10-27 | §2.8 | TERUKUR |
| R6-102 | 0,0 | p mentah (vib) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[0].p_mentah | 2026-10-27 | §2.8 | TERUKUR |
| R6-103 | 3,263e-09 | p mentah (shk) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[2].p_mentah | 2026-10-27 | §2.8 | TERUKUR |
| R6-104 | 9,789e-09 | p Holm (shk) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[2].p_holm | 2026-10-27 | §2.8 | TERUKUR |
| R6-105 | 6,526e-09 | p BH (shk) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[2].p_bh | 2026-10-27 | §2.8 | TERUKUR |
| R6-106 | 0,009521 | p mentah (stuck_k2) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[3].p_mentah | 2026-10-27 | §2.8 | TERUKUR |
| R6-107 | 0,019042 | p Holm (stuck_k2) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[3].p_holm | 2026-10-27 | §2.8 | TERUKUR |
| R6-108 | 0,012695 | p BH (stuck_k2) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[3].p_bh | 2026-10-27 | §2.8 | TERUKUR |
| R6-109 | 1,0 dan TP 0 dari FP 4 | p dan hitungan (ssi) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[1].p_mentah, .tp, .fp | 2026-10-27 | §2.8 | TERUKUR |
| R6-110 | 9; 9; 9 | jumlah uji dan jumlah signifikan keluarga F2 | RUN-KITA | `rnd_r6_RESULTS.json` S8...F2_hyd_ki_persistence_9fold.n_uji, .n_sig_mentah, .n_sig_holm, .n_sig_bh | 2026-10-27 | §2.8 | TERUKUR |
| R6-111 | 0,0457 dan 0,01666 | proporsi (presisi terkumpul dan prevalensi terkumpul stuck_k2) | RUN-KITA | `rnd_r6_RESULTS.json` S8...F1.baris[3].presisi dan .prev_pool | 2026-10-27 | §2.8 | TERUKUR |
| R6-112 | 2,7 | rasio presisi terhadap prevalensi | DERIVASI | 0,0457 / 0,01666 = 2,743 dari S8...F1.baris[3] | 2026-10-27 | §2.8 | TERVERIFIKASI (aritmetika) |
| R6-113 | 157 | hitungan FP (laju dasar median 9 fold hyd K-i) | RUN-KITA | `rnd_r6_RESULTS.json` S6_mde_selisih_laju_far.lam_base_fp_per_periode_negatif | 2026-10-27 | §3.2 | TERUKUR |
| R6-114 | 1,40 | rasio laju (MDE pada daya 80 persen) | RUN-KITA | `rnd_r6_RESULTS.json` S6_mde_selisih_laju_far.rr_mde_80 | 2026-10-27 | §3.2, §4 | TERUKUR |
| R6-115 | 1,10 sampai 4,00 (31 titik) | rasio laju (grid pencarian MDE) | DERIVASI (kode) | `rnd_r6_compute.py:197` (`grid = [1.0 + 0.1 * i for i in range(1, 31)]`); catatan S6 di JSON menulis 1,05..3,00 dan dinyatakan keliru | 2026-10-27 | §3.2, §6 | TERVERIFIKASI (kode terbaca) |
| R6-116 | 29 | persen (penurunan FAR minimum yang dapat dibuktikan) | DERIVASI | 1 - 1/1,40 = 0,2857 dari S6...rr_mde_80 | 2026-10-27 | §3.2 | TERVERIFIKASI (aritmetika) |
| R6-117 | 0 dan null | hitungan FP dan rasio (shk F-10 ambang 0,5) | RUN-KITA | `rnd_r6_RESULTS.json` S6...lam_base_shk_f10_tau05 = 0 dan .rr_mde_80_shk = null | 2026-10-27 | §3.2 | TERUKUR |
| R6-118 | 80 dan 120 | ulangan simulasi | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S15...hasil[].n_sims = 80; `rnd_r6_RESULTS.json` S7...hasil[].n_sims = 120 | 2026-10-27 | §3.3 | TERUKUR |
| R6-119 | 0,023 | delta AUPRC (MDE daya 80 persen pada prevalensi 1,69 persen) | DERIVASI | S7...hasil[0]: delta 0,0232 dengan daya 0,792, dibulatkan 0,023 | 2026-10-27 | §3.3, §4 | TERVERIFIKASI (aritmetika) |
| R6-120 | 4,0; 8,0; 12,0; 24,0; 48,0; 120,0 | jam negatif minimum untuk FAR <= 6 pada 1, 2, 3, 6, 12, 30 FP | RUN-KITA | `rnd_r6_RESULTS.json` S11_resolusi_far.tabel[0..5].jam_neg_min_untuk_FAR_le_6 | 2026-10-27 | §3.4 | TERUKUR |
| R6-121 | 4 | jam negatif per satu FP (turunan ambang) | DERIVASI | 24 / 6 = 4, yaitu ekuivalensi FAR <= 6 terhadap jam_neg >= 4 x FP | 2026-10-27 | §3.4, §4 | TERVERIFIKASI (aritmetika) |
| R6-122 | 3,6889 | batas atas per jam bila 0 FP | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S16_resolusi_far_eksak.tabel[0].far_hi_jika_0fp_per_jam | 2026-10-27 | §3.4 | TERUKUR |
| R6-123 | 14,756 | jam negatif minimum agar batas atas FAR <= 6 | RUN-KITA | `rnd_r6_SUPPLEMENT.json` S16_resolusi_far_eksak.tabel[0].jam_neg_min_agar_hi_le_6 | 2026-10-27 | §3.4, §4 | TERUKUR |
| R6-124 | 786 | jendela negatif (ssi F-9_A) | RUN-KITA | `scratch/v9_e_ml/v9_e_ML_ssi_RESULTS.json` folds[8].models.rf.tau_metrics.0.5.n_neg | 2026-10-27 | §3.4 | TERUKUR |
| R6-125 | 13,1 | jam negatif (ssi F-9_A) | DERIVASI | 786 / 60 = 13,1 dari baris R6-124 | 2026-10-27 | §3.4 | TERVERIFIKASI (aritmetika) |
| R6-126 | 6,76 | per 24 jam (batas atas 95 persen dengan 0 FP) | DERIVASI | 3,6889 x 24 / 13,1 = 6,758 dari S16...tabel[0] dan baris R6-125 | 2026-10-27 | §3.4, §4 | TERVERIFIKASI (aritmetika) |
| R6-127 | 10 | rujukan | RUN-KITA | `doi_verify_r6.json` (10 entri) | 2026-10-27 | §5 | TERUKUR |
| R6-128 | 9 | rujukan TERVERIFIKASI | JURNAL | `doi_verify_r6.json`: 9 entri dengan Crossref 200 dan doi.org 200 atau 403 (blokir bot), lihat §5 dokumen | 2026-10-27 | §5 | TERVERIFIKASI |
| R6-129 | 1 | rujukan BELUM TERVERIFIKASI | JURNAL | Holm 1979, DOI 10.2307/4615733: Crossref 404 dan doi.org 404 pada `doi_verify_r6.json`; tidak dipakai sebagai dasar rekomendasi | 2026-10-27 | §5, §8 | BELUM |
| R6-130 | 9 | pikiran sequ-mcp (5 pada run dokumen, 4 pada run provenance) | RUN-KITA | respons `mcp__sequentialthinking__sequentialthinking` dengan thoughtHistoryLength 5 dan 4 | 2026-10-27 | §0 | TERUKUR |
| R6-131 | DeLong pada data nyata | tidak ada nilai | BELUM-TERUKUR | `rnd_r6_RESULTS.json` S9_delong.status: skor per jendela tidak disimpan di JSON V9 | 2026-10-27 | §2.2, §8 | BELUM TERUKUR |
| R6-132 | McNemar untuk dua engine pada jendela sama | tidak ada nilai | BELUM-TERUKUR | `rnd_r6_SUPPLEMENT.json` S13_fisher_presisi.catatan: hitungan ketidaksesuaian berpasangan tidak tersedia | 2026-10-27 | §2.5, §8 | BELUM TERUKUR |
| R6-133 | Kestabilan lintas seed | tidak ada nilai | BELUM-TERUKUR | semua skrip memakai SEED = 42; penggantian seed belum dijalankan | 2026-10-27 | §4 butir A4, §8 | BELUM TERUKUR |
| R6-134 | MDE pada data heterogen | tidak ada nilai | BELUM-TERUKUR | S7 dan S15 memakai asumsi well homogen (800 jendela negatif, parameter identik) | 2026-10-27 | §3.3, §8 | BELUM TERUKUR |

### Rekap kelas sumber R6

| Kelas | Jumlah baris |
|---|---|
| BELUM-TERUKUR | 4 |
| DERIVASI | 15 |
| JURNAL | 2 |
| KONVENSI | 3 |
| RUN-KITA | 110 |
| TOTAL | 134 |

### Koreksi yang dicatat pada run ini

1. R6-41 dan R6-42: jumlah jendela positif ssi F-7 adalah 3 dari 982 (bukan 9 seperti pada draf pertama `RND_R6_METRIK.md` §1.6).
2. R6-35 dan R6-36: plafon lift ssi F-7 adalah 327,333 (JSON, prevalensi tak dibulatkan), sedangkan 1/0,00305 = 327,87. Keduanya dicatat agar tidak tampak bertentangan.
3. R6-115: grid rasio laju pada `rnd_r6_compute.py:197` adalah 1,10 sampai 4,00 (31 titik). Catatan `S6` di JSON menulis 1,05..3,00 dan catatan itu keliru; dokumen sudah dikoreksi.
4. R6-66: string `S7...desain` menulis 150 kali bootstrap, sedangkan `n_boot` yang dipakai 120. Yang dilaporkan 120.

### Yang tetap belum terukur (baris R6-131 sampai R6-134)

DeLong pada data nyata, McNemar untuk dua engine pada jendela yang sama, kestabilan lintas seed, dan MDE pada data heterogen. Keempatnya ditulis sebagai BELUM TERUKUR, bukan sebagai hasil nol atau hasil negatif.

---

## Bagian E1: matriks kelayakan algoritma x engine dan shortlist (kartu `t_9abcb3b3`)

Dokumen pendamping: `docs/RND_E1_MATRIKS.md`. Sumber angka: `scratch/rnd_e1/e1_scores.json` (dibuat 2026-10-27 06:24:16 oleh `scratch/rnd_e1/e1_build.py`), `scratch/rnd_e1/doi_check.json`, dan baris ledger R1, R3, R4, R5, D0 yang dirujuk ulang.

Baris E1 tidak menduplikasi angka hasil ukur yang sudah punya baris sendiri. Yang ditulis di sini adalah bobot, rubrik, rumus, hasil derivasi skor, dan status verifikasi baru.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| E1-001 | 0,50 | bobot | KONVENSI | keputusan dokumen ini; diturunkan dari `docs/RND_ALGO_RESEARCH_PLAN.md` bagian 6 (tier hanya naik bila C, A, B terpenuhi bersamaan) | 2026-10-27 | bagian 5.1 | TERVERIFIKASI sebagai aritmetik (jumlah bobot 1,000) |
| E1-002 | 0,25 | bobot | KONVENSI | keputusan dokumen ini; alasan di `docs/RND_D0_DATA_FEASIBILITY.md` bagian 2 tentang blokir laju sampel | 2026-10-27 | bagian 5.1 | TERVERIFIKASI sebagai aritmetik |
| E1-003 | 0,15 | bobot | KONVENSI | keputusan dokumen ini; alasan di `docs/RND_E0_AUDIT_ENGINE.md` bagian 6 (5 temuan Kritis) | 2026-10-27 | bagian 5.1 | TERVERIFIKASI sebagai aritmetik |
| E1-004 | 0,10 | bobot | KONVENSI | keputusan dokumen ini; biaya ekstrem sudah tertangkap di sel (ledger R3-40) | 2026-10-27 | bagian 5.1 | TERVERIFIKASI sebagai aritmetik |
| E1-005 | 0,50*tier + 0,25*data + 0,15*risiko + 0,10*biaya | rumus skor 0-3 | DERIVASI | `scratch/rnd_e1/e1_build.py` fungsi `skor_prioritas`, dengan gerbang skor 0 bila tier 0 | 2026-10-27 | bagian 5.1, 5.2 | TERVERIFIKASI (rumus dijalankan skrip, hasil di `e1_scores.json`) |
| E1-006 | 0 sampai 3 | rubrik | KONVENSI | rubrik kesesuaian sel di `docs/RND_E1_MATRIKS.md` bagian 1.1 | 2026-10-27 | bagian 1.1, 2, 3 | BELUM (definisi dokumen, bukan temuan) |
| E1-007 | 3 / 1 / 0 | skor data | KONVENSI | pemetaan ADA ke 3, SEBAGIAN ke 1, TIDAK ke 0 di `e1_build.py` `DATA_SCORE` | 2026-10-27 | bagian 5.1 | BELUM (keputusan dokumen) |
| E1-008 | 196 | sel | DERIVASI | 28 algoritma x 7 engine; assert `len(D['pasangan']) == 196` di `e1_doc.py` | 2026-10-27 | bagian 0, 2 | TERVERIFIKASI (assert lolos) |
| E1-009 | 28 | algoritma | DERIVASI | `len(D['matriks']) == 28`; daftar di `docs/RND_E1_MATRIKS.md` bagian 2 | 2026-10-27 | bagian 0, 2 | TERVERIFIKASI (assert lolos) |
| E1-010 | 6 | pikiran | RUN-KITA | `mcp__sequentialthinking__sequentialthinking` thoughtNumber 1..6, thoughtHistoryLength 6 | 2026-10-27 | bagian Riset pendahuluan | TERUKUR |
| E1-011 | 2,85 | skor prioritas | DERIVASI | A10 conformal pada hyd: 0,50*3 + 0,25*3 + 0,15*2 + 0,10*3 = 2,85 | 2026-10-27 | bagian 5.2, 6, 7.1 | TERVERIFIKASI (assert aritmetik) |
| E1-012 | 2,35 | skor prioritas | DERIVASI | A16 Page-Hinkley pada tool_wear: 0,50*2 + 0,25*3 + 0,15*2 + 0,10*3 = 2,35 | 2026-10-27 | bagian 5.2, 6, 7.2 | TERVERIFIKASI (assert aritmetik) |
| E1-013 | 2,15 | skor prioritas | DERIVASI | A06 LightGBM atau XGBoost pada shk: 0,50*2 + 0,25*3 + 0,15*2 + 0,10*1 = 2,15 | 2026-10-27 | bagian 5.2, 6, 7.3 | TERVERIFIKASI (assert aritmetik) |
| E1-014 | 0,00 | skor prioritas Monte Carlo | DERIVASI | gerbang tier=0 memaksa A14 ke 0; assert atas D['pasangan'] untuk A14 di `e1_doc.py` | 2026-10-27 | bagian 5.1 | TERVERIFIKASI (assert lolos) |
| E1-015 | 7 | algoritma | DERIVASI | hitung dari `e1_scores.json` peringkat_algoritma dengan ambang skor > 2,0 | 2026-10-27 | bagian 0 | TERVERIFIKASI (hitung ulang di `e1_doc.py`) |
| E1-016 | 13 / 5 | algoritma ditolak / ditunda | KONVENSI | hitungan baris tabel `docs/RND_E1_MATRIKS.md` bagian 8.1 dan 8.2, dihitung ulang oleh `rows_of()` di `e1_doc.py` | 2026-10-27 | bagian 0, 8 | TERVERIFIKASI (hitung baris tabel) |
| E1-017 | 10.1214/18-AOS1801 | DOI | JURNAL | Crossref 200 mengembalikan Chen 2020 tentang inferensi SGD, bukan Romano 2019; lihat `scratch/rnd_e1/doi_check.json` | 2026-10-27 | bagian 8.3, 10 | DITOLAK (tidak dipakai) |
| E1-018 | BELUM TERUKUR | detik biaya latih | BELUM-TERUKUR | run pembanding R4 tidak selesai; sebelum diberi angka, tidak ada nilai yang boleh ditulis | 2026-10-27 | bagian 5.1 butir 2, 9 butir 1 | BELUM |
| E1-019 | 302 / 200 | status HTTP | RUN-KITA | tujuh DOI di `scratch/rnd_e1/doi_check.py`: doi.org 302 tanpa mengikuti redirect, Crossref 200 dengan penulis dan tahun cocok | 2026-10-27 | bagian 10 | TERUKUR |
| E1-020 | 200 | status HTTP | RUN-KITA | empat URL arXiv dan prosiding di `scratch/rnd_e1/` diperiksa dengan `curl -L`, judul halaman cocok | 2026-10-27 | bagian 10 | TERUKUR |
| E1-021 | 14,6 sampai 58,4 | FAR per 24 jam, hybrid hyd K-i | RUN-KITA | docs/V9_EVAL_C_LAYERC.md bagian 1 baris hyd K-i | 2026-10-27 | bagian 7.1 | TERUKUR (kutipan diverifikasi ada di sumber) |
| E1-022 | 0,50 | presisi run tool_wear | RUN-KITA | docs/V9_EVAL_C_LAYERC.md bagian 1 baris tool_wear K-i | 2026-10-27 | bagian 7.2 | TERUKUR (kutipan diverifikasi ada di sumber) |
| E1-023 | 1,8 | rasio TLead tool_wear | RUN-KITA | docs/V9_EVAL_C_LAYERC.md bagian 1 baris tool_wear K-i | 2026-10-27 | bagian 7.2 | TERUKUR (kutipan diverifikasi ada di sumber) |
| E1-024 | 0,775 | daya uji tanda 9 well | RUN-KITA | docs/RND_R6_METRIK.md bagian 3.1 | 2026-10-27 | bagian 7.1, 7.3 | TERUKUR (kutipan diverifikasi ada di sumber) |
| E1-025 | 1,46 sampai 71,7 | cakupan waktu teramati per well (persen) | RUN-KITA | docs/RND_E0_AUDIT_ENGINE.md temuan Kritis K-4 | 2026-10-27 | bagian 7, 9 | TERUKUR (kutipan diverifikasi ada di sumber) |
| E1-026 | 6,65 | rasio laju alarm One-Class SVM terhadap parameter nu | RUN-KITA | docs/RND_R5_DRIFT.md bagian 5 tabel skor (baris One-Class SVM) | 2026-10-27 | bagian 3.5 A23 | TERUKUR (kutipan diverifikasi ada di sumber) |

Rekap kelas: 7 KONVENSI (E1-001..E1-004, E1-006, E1-007, E1-016), 8 DERIVASI (E1-005, E1-008, E1-009, E1-011..E1-015), 9 RUN-KITA (E1-010, E1-019, E1-020, E1-021..E1-026), 1 JURNAL ditolak (E1-017), 1 BELUM (E1-018).

Catatan koreksi yang ditemukan pada run ini: DOI `10.1214/18-AOS1801` tidak menunjuk Romano 2019 (conformalized quantile regression) melainkan Chen 2020. DOI itu dibuang, dan conformal disandarkan pada Vovk 2005 serta arXiv 1905.03222.

## Bagian E2: protokol pilot tiga kandidat (kartu `t_79811fae`)

Dokumen pendamping: `docs/RND_E2_PROTOKOL.md`. Sumber: `scratch/rnd_e2/e2_final.json`, `e2_stats.json`, `e2_probe.json`, `e2_doi.json`, plus JSON primer `scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json`. Baris di bawah tidak menduplikasi angka yang sudah punya baris di bagian lain; yang ditulis di sini adalah hasil ukur langsung, derivasi, konvensi protokol, dan status ketiadaan angka.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| E2-001 | 9 | well | RUN-KITA | `scratch/rnd_e2/e2_probe.py` menghitung kolom `well` unik pada `scratch/v9_d1/datasets/hyd_ki.csv.gz` | 2026-10-27 | bagian 1, 2.1, 4.1 | TERUKUR |
| E2-002 | 9 | well | RUN-KITA | `e2_probe.py` pada `scratch/v9_d1/datasets/shk.csv.gz` | 2026-10-27 | bagian 1, 4.3 | TERUKUR |
| E2-003 | 4 | alat | RUN-KITA | `scratch/rnd_e2/e2_toolwear.py` menghitung kolom `tool` unik pada `scratch/v6_e1/toolwear_windows.csv` | 2026-10-27 | bagian 1, 2.5, 5.1 | TERUKUR |
| E2-004 | 469 | jendela | RUN-KITA | `e2_toolwear.py` `n_rows` pada berkas yang sama | 2026-10-27 | bagian 1, 4.2 | TERUKUR |
| E2-005 | 32 | kolom | RUN-KITA | `e2_toolwear.py` `n_cols` pada berkas yang sama | 2026-10-27 | bagian 1 | TERUKUR |
| E2-006 | 120 / 112 / 121 / 116 | jendela per alat T01..T04 | RUN-KITA | `e2_toolwear.py` `per_unit` | 2026-10-27 | bagian 1 | TERUKUR |
| E2-007 | 27 | head | RUN-KITA | `scratch/v9_i1/v9_i1_RESULTS.json` dihitung ulang: jumlah `heads` seluruh engine = 27 | 2026-10-27 | bagian 1 | TERUKUR |
| E2-008 | 12 / 13 / 2 / 0 | head per tier (PERINGATAN / TREN / BELUM LAYAK / ALARM-OTOMATIS) | RUN-KITA | `v9_i1_RESULTS.json` hitung tier per head; kunci ALARM-OTOMATIS tidak muncul satu kali pun | 2026-10-27 | bagian 1, 5.5 | TERUKUR |
| E2-009 | 21,55 | detik | RUN-KITA | `v9_i1_RESULTS.json` `meta.elapsed_s`, satu lintasan prototipe 7 engine | 2026-10-27 | bagian 3.4 | TERUKUR |
| E2-010 | 42 | seed | RUN-KITA | `v9_i1_RESULTS.json` `meta.seed` | 2026-10-27 | bagian 3.1 | TERUKUR |
| E2-011 | 1 / 3 / 1 / 3 | FP pada segmen evaluasi R01 per alat | RUN-KITA | `scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json` `part_C_operating_far_calibrated`, target 1,0 FP/menit | 2026-10-27 | bagian 4.2, 5.2 | TERUKUR |
| E2-012 | 1,43 / 1,43 / 4,50 / 5,14 | FP per menit segmen evaluasi | DERIVASI | fp_R01 dibagi (n_eval_R01/60) dengan n_eval 42, 35, 42, 40 jendela 1 detik; assert di `e2_compute.py` | 2026-10-27 | bagian 4.2, 5.2, ringkasan | TERVERIFIKASI (assert lolos) |
| E2-013 | 0 | alat yang lulus FAR <= 1 per menit | DERIVASI | hitung dari baris E2-012 terhadap ambang 1,0; tidak satu pun <= 1,0 | 2026-10-27 | bagian 4.2, 5.2, ringkasan | TERVERIFIKASI (assert lolos) |
| E2-014 | 20 / 24 / 25 / 36 | detik TLead per alat | RUN-KITA | `part_C` `TLead_s` pada target 1,0 FP/menit; cocok dengan `docs/V9_EVAL_C_LAYERC.md` bagian 2.7 | 2026-10-27 | bagian 4.2, 5.3 | TERUKUR |
| E2-015 | 24,5 | detik median TLead | DERIVASI | median (24, 25) dari baris E2-014 | 2026-10-27 | bagian 4.2 | TERVERIFIKASI |
| E2-016 | 1,8 | rasio maks/min TLead | DERIVASI | 36/20 = 1,8 dari baris E2-014 | 2026-10-27 | bagian 4.2, 5.1 | TERVERIFIKASI |
| E2-017 | 0,50 | presisi run | RUN-KITA | `part_A_change_point` `run_level_sig_p05_v8`: tp 4, fp 4, precision 0,5, recall 1,0 | 2026-10-27 | bagian 4.2, 5.3 | TERUKUR |
| E2-018 | 1 / 3 / 1 / 3 | FP pada target kalibrasi 0,2 FP/menit | RUN-KITA | `part_C` target 0,2; identik dengan target 1,0 karena ambang berbasis hitungan fitur terkuantisasi | 2026-10-27 | bagian 4.2 | TERUKUR |
| E2-019 | 9 | kolom berawalan Y_ yang BUKAN label | RUN-KITA | `e2_toolwear.py`: kolom `Y_mean`, `Y_rms`, dan seterusnya adalah statistik sinyal sumbu Y; deteksi label otomatis pada probe sempat salah menandainya | 2026-10-27 | bagian 1 | TERUKUR (koreksi dicatat) |
| E2-020 | 8 dari 9, p = 0,0390625 | uji tanda dua sisi | DERIVASI | `e2_stats.py` `sign_krit(9)` dan `sign_p_two_sided(8,9)` = 20/512 = 0,0390625; cocok dengan R6 bagian 2.6 (S5FIX) yang menulis 0,039063 pada 6 desimal | 2026-10-27 | bagian 5.1, 6.1 | TERVERIFIKASI |
| E2-021 | 0,7748 | daya pada konkordansi 0,90, n = 9 | DERIVASI | `e2_stats.py` `sign_power(9, 0.9)`; cocok R6 bagian 3.1 | 2026-10-27 | bagian 5.1 | TERVERIFIKASI |
| E2-022 | 7 dari 7, p = 0,015625, daya 0,4783 | uji tanda dua sisi, n = 7 | DERIVASI | `e2_stats.py` `sign_krit(7)` | 2026-10-27 | bagian 5.1 | TERVERIFIKASI |
| E2-023 | 0,125 | p minimum yang mungkin pada n = 4 | DERIVASI | `e2_stats.py`; tidak ada k yang mencapai alpha 0,05 sehingga daya nol | 2026-10-27 | bagian 2.5, 5.1 | TERVERIFIKASI |
| E2-024 | 0,1685 / 0,1710 / 0,2007 / 0,2462 / 0,3747 | setengah lebar Wilson 95% pada p = 0,5 | DERIVASI | `e2_stats.py` untuk n = 30, 29, 20, 12, 3; k dipakai sebagai pecahan 0,5*n supaya p tetap 0,5 pada n ganjil. Batas pada n = 30: 0,3315 sampai 0,6685 | 2026-10-27 | bagian 6.3, ringkasan | TERVERIFIKASI |
| E2-025 | 93 / 381 | positif yang dibutuhkan untuk setengah lebar 0,10 / 0,05 | DERIVASI | `e2_stats.py` `n_untuk_setengah_lebar` | 2026-10-27 | bagian 6.3 | TERVERIFIKASI |
| E2-026 | 3,6889 | batas atas Garwood 95% dua sisi untuk 0 kejadian per satuan paparan | DERIVASI | chi2(0,975; 2)/2 = 7,3778/2; nilai satu sisi 2,9957 dilaporkan sebagai bandingan dan TIDAK dipakai | 2026-10-27 | bagian 5.2, ringkasan | TERVERIFIKASI |
| E2-027 | 14,7555 | jam negatif minimum untuk menyertifikasi FAR <= 6 dengan 0 FP | DERIVASI | 3,6889 x 24 / 6 = 14,7555 | 2026-10-27 | bagian 5.2, 8 | TERVERIFIKASI |
| E2-028 | 4,0 / 12,0 / 24,0 / 120,0 | jam negatif minimum untuk 1 / 3 / 6 / 30 FP | DERIVASI | `FP <= jam_neg/24 x 6` ekuivalen `jam_neg >= 4 x FP`; nilai pada `e2_stats.json` `jam_neg_min_per_fp` | 2026-10-27 | bagian 5.2 | TERVERIFIKASI |
| E2-029 | 13,1 / 6,7583 | jam negatif dan batas atas FAR pada ssi F-9_A | DERIVASI | 786 jendela x 60 detik / 3600 = 13,1 jam; 3,6889 x 24 / 13,1 = 6,7583 > 6 sehingga tidak dapat disertifikasi | 2026-10-27 | bagian 5.2 | TERVERIFIKASI |
| E2-030 | 14,6 sampai 58,4 | FAR per 24 jam, hybrid hyd K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` bagian 1 dan 2.5 (dikutip ulang, teks sumber diperiksa memuat angka ini) | 2026-10-27 | bagian 1, 4.1, 5.2 | TERUKUR (kutipan diverifikasi) |
| E2-031 | 2091 menjadi 927 | FP hybrid hyd K-i | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` bagian 2.5, tertulis `2091→927 (−55,7%)` konsisten 9/9 (sumber tanpa pemisah ribuan) | 2026-10-27 | bagian 4.1 | TERUKUR (kutipan diverifikasi) |
| E2-032 | 0,67 sampai 6,6 | FAR per 24 jam rule shk | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` bagian 1 (FAR <= 6 di 7 dari 9 well) | 2026-10-27 | bagian 1, 4.3, 5.2 | TERUKUR (kutipan diverifikasi) |
| E2-033 | 0,007 sampai 0,193 | AUPRC RF shk antar well | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` bagian 2.3 (CI memuat prevalensi 7 dari 9) | 2026-10-27 | bagian 1, 4.3 | TERUKUR (kutipan diverifikasi) |
| E2-034 | 1,46 sampai 71,7 | persen cakupan waktu teramati per well | RUN-KITA | `docs/RND_E0_AUDIT_ENGINE.md` temuan Kritis K-4 | 2026-10-27 | bagian 0, 5.2, 13 | TERUKUR (kutipan diverifikasi) |
| E2-035 | di atas 0,97 | autokorelasi lag-1 | RUN-KITA | `docs/RND_R6_METRIK.md` bagian 2.1 yang merujuk `docs/RND_R5_DRIFT.md` | 2026-10-27 | bagian 2.1 | TERUKUR (kutipan diverifikasi) |
| E2-036 | 1,40 / 0,023 / 0,0192 | MDE rasio laju FAR / delta AUPRC prevalensi 1,69% / 13,66% | RUN-KITA | `docs/RND_R6_METRIK.md` bagian 3.2 dan 3.3 | 2026-10-27 | bagian 4.1, 4.3, 5.2, 8 | TERUKUR (kutipan diverifikasi) |
| E2-037 | 12 / 110 / 1.320 | menit per fold / fold-run / menit total | KONVENSI | ditetapkan dokumen ini; jumlah fold 22 berasal dari D0 (9 hyd, 9 shk, 4 alat) dan 5 seed. Angka 12 menit BUKAN hasil ukur karena biaya latih boosting belum terukur | 2026-10-27 | bagian 0, 3.4, 8 | BELUM (konvensi, bukan temuan) |
| E2-038 | 30 | positif minimum per fold | KONVENSI | ditetapkan dokumen ini, disandarkan pada lebar Wilson (baris E2-024): pada 30 positif setengah lebar 0,1685; kartu E2 juga menyebut ambang 30 | 2026-10-27 | bagian 0, 6.3 | BELUM (konvensi, bukan temuan) |
| E2-039 | 5 | seed (42, 43, 44, 45, 46) | KONVENSI | ditetapkan dokumen ini mengikuti R6 A4 yang mensyaratkan uji ganti seed | 2026-10-27 | bagian 3.1 | BELUM (konvensi, bukan temuan) |
| E2-040 | 3 per shift / 10 menit / 50 persen | ambang beban shift, asumsi menit per alarm, cakupan minimum | KONVENSI | ditetapkan dokumen ini; cakupan 50 persen dipilih dari sebaran terukur E2-034, bukan hasil optimasi | 2026-10-27 | bagian 5.3, 13 | BELUM (konvensi, bukan temuan) |
| E2-041 | 17 / 16 / 4 | DOI diperiksa / terverifikasi / URL non-DOI status 200 | RUN-KITA | `scratch/rnd_e2/e2_doi.py` dan `e2_doi.json`: doi.org tanpa redirect + Crossref; 1 DOI gagal (Holm 1979, 404/404) | 2026-10-27 | bagian 11 | TERUKUR |
| E2-042 | 7 | pikiran | RUN-KITA | `mcp__sequentialthinking__sequentialthinking` thoughtNumber 1..7, thoughtHistoryLength 7 | 2026-10-27 | bagian Riset pendahuluan | TERUKUR |
| E2-043 | BELUM TERUKUR | versi pustaka pilot | BELUM-TERUKUR | `e2_probe.py` pada host ini: numpy, pandas, scikit-learn, scipy, statsmodels, lightgbm, xgboost, catboost, pyarrow tidak terpasang (Python 3.14.9 tanpa pip). Protokol memblokir run tanpa `pip freeze` | 2026-10-27 | bagian 3.2, 13 butir 1 | BELUM |
| E2-044 | BELUM TERUKUR | detik biaya latih boosting per fold | BELUM-TERUKUR | belum pernah dijalankan pada data kita; angka 12 menit adalah konvensi (E2-037) | 2026-10-27 | bagian 3.4, 13 butir 2 | BELUM |
| E2-045 | BELUM TERUKUR | FAR dan recall finalis setelah kalibrasi bersarang | BELUM-TERUKUR | pilot belum dijalankan; kriteria bagian 4 adalah ambang keputusan, bukan hasil | 2026-10-27 | bagian 4, 13 butir 3 | BELUM |
| E2-046 | 0,3315 sampai 0,6685 | batas CI95 Wilson pada 30 positif, p = 0,5 | DERIVASI | `e2_stats.py` `wilson_p05["30"]` `lo` dan `hi`; dipakai sebagai angka pada kalimat 0,3315 dan 0,6685 di bagian 6.3 | 2026-10-27 | bagian 6.3 | TERVERIFIKASI |
| E2-047 | 331 sampai 1.426 / 30 sampai 760 | positif per fold minimum sampai maksimum (hyd / shk) | RUN-KITA | `e2_probe.py`: `y_hyd` minimum 331 di F-9_A, maksimum 1.426 di F-12; `y_shk` minimum 30 di F-9_A, maksimum 760 di F-14 | 2026-10-27 | bagian 1, 6.3 | TERUKUR |
| E2-048 | 52.509 / 56.495 / 7.571 | baris dataset hyd / shk / baris well F-10 pada hyd | RUN-KITA | `e2_probe.py` `rows` dan `rows_per_well['F-10']` | 2026-10-27 | bagian 1, 2.1 | TERUKUR |
| E2-049 | 0,615 sampai 0,793 / 32,2 sampai 109,7 | presisi dan FAR persistence hyd K-i | RUN-KITA | presisi dari `code/v9_i1_pipeline.py` REGISTRY head hyd/persistence (`P 0,615-0,793`); FAR dari `docs/V9_EVAL_C_LAYERC.md` bagian 2.5 (`32,2–109,7`) | 2026-10-27 | bagian 4.1 | TERUKUR (kutipan diverifikasi) |
| E2-050 | 42,857 sampai 58,571 | FP per menit engine 5/27 pada segmen R01 | RUN-KITA | `part_B_within_tool_calibration` `engine_5of27.far_fp_per_min_R01` per alat (58,571 / 46,286 / 42,857 / 51,0) | 2026-10-27 | bagian 4.2 | TERUKUR |
| E2-051 | 41 / 33 / 40 / 36 | FP rule 3-RMS pada segmen R01 per alat | RUN-KITA | `part_B_within_tool_calibration` `baseline_rule_3RMS.fp_R01` | 2026-10-27 | bagian 4.2 | TERUKUR |
| E2-052 | 0,80 / 0,50 | ambang presisi gate B untuk F2 / F1 dan F3 | KONVENSI | ditetapkan dokumen ini; 0,50 adalah presisi run terukur (baris E2-017) sehingga F2 diminta naik, sedangkan F1 dan F3 diminta tidak turun | 2026-10-27 | bagian 4.2, 5.3 | BELUM (konvensi, bukan temuan) |
| E2-053 | 1.740 / 1.770 | detik batas satu proses / batas terminal kartu | KONVENSI | 1.740 ditetapkan dokumen ini (di bawah batas terminal); 1.770 adalah `Terminal timeout` pada metadata kartu `t_79811fae` | 2026-10-27 | bagian 3.4 | BELUM (konvensi dan batas lingkungan) |
| E2-054 | 301 / 302 / 200 / 404 | status HTTP lapis registrasi dan metadata | RUN-KITA | `e2_doi.py`: doi.org tanpa redirect (301 atau 302 = terdaftar, 404 = tidak), Crossref 200 = metadata cocok; rincian per DOI di `e2_doi.json` | 2026-10-27 | bagian 11 | TERUKUR |
| E2-055 | 178 / 890 | latih model per seed / untuk 5 seed | DERIVASI | bagian 2.4 dokumen ini: F1 9 x 9 = 81, F2 4 x 4 = 16, F3 9 x 9 = 81, jumlah 178; dikali 5 seed = 890 | 2026-10-27 | bagian 2.4, 3.4 | TERVERIFIKASI (aritmetik) |
| E2-056 | 119 | rasio sebar FAR antar well, vib ambang 0,5 | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` bagian 1 baris vib (`FAR 4,1–496 (119×)`) dan REGISTRY `code/v9_i1_pipeline.py` head vib/rf_lowo | 2026-10-27 | bagian 0, 2.1 | TERUKUR (kutipan diverifikasi) |

Rekap kelas: BELUM-TERUKUR 3, DERIVASI 16, KONVENSI 6, RUN-KITA 31 (total 56 baris).

Rekap status: BELUM 9, TERUKUR 31, TERVERIFIKASI 16.

Koreksi yang ditemukan pada run ini dan dicatat terbuka:

1. Skrip `e2_stats.py` versi pertama memakai `chi2(0,95;2)/2 = 2,9957` dan melabelinya "batas 95% satu sisi". Angka yang dipakai dokumen hulu (3,6889) adalah batas dua sisi 95%. Untuk sertifikasi FAR dipakai yang konservatif (3,6889), dan nilai satu sisi dilaporkan sebagai bandingan (baris E2-026, E2-027). Akibatnya ssi F-9_A tetap tidak dapat disertifikasi (6,7583 > 6), bukan lolos seperti yang akan disimpulkan angka satu sisi (5,4884).
2. Rekonsiliasi angka TLead tool_wear sempat dicurigai tidak cocok antara dokumen hulu (20 sampai 36 detik, median 24,5) dan `part_A.t_lead_s` (21 sampai 39, median 31,5). Setelah ditelusuri, kedua angka benar untuk medan berbeda: 20 sampai 36 dan median 24,5 berasal dari `part_C` (titik operasi terkalibrasi FAR), sedangkan 21 sampai 39 berasal dari `part_A` (change point SSE). Yang dipakai protokol adalah `part_C` (baris E2-014).
3. Deteksi kolom label otomatis pada `e2_toolwear.py` salah menandai 9 kolom `Y_*` (statistik sinyal sumbu Y) sebagai label karena awalan `Y_`. Berkas bengkel tidak punya kolom label `y_*`; labelnya adalah perubahan regime di dalam run (baris E2-019).
4. Rujukan Holm 1979 tetap tidak dapat dibuka (doi.org 404, Crossref 404) sehingga tidak dipakai sebagai dasar rekomendasi, konsisten dengan keputusan R6 (baris E2-041).

## Bagian V1: audit provenance dan resolusi sitasi (kartu `t_3a2b1d40`)

Tanggal akses seluruh baris: 2026-10-27 (WIB). Bukti mentah: `scratch/rnd_v1/` pada workspace kartu `t_3a2b1d40` (`v1_extract.json`, `v1_verify.json`, `v1_number_cov.json`, `claims.json`).

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |
|---|---|---|---|---|---|---|
| V1-01 | 11 | dokumen | RUN-KITA | daftar `docs/RND_*.md` dikurangi ledger dan plan; `scratch/rnd_v1/extract.py` (workspace board `rnd-algo-2026`) | §1.1 | TERUKUR |
| V1-02 | 1.586 (sebelum bagian V1 ditulis) dan 1.620 (sesudahnya) | baris | RUN-KITA | `wc -l docs/RND_PROVENANCE_LEDGER.md` sebelum dan sesudah penambahan 34 baris bagian V1 | §1.1 | TERUKUR |
| V1-03 | 1.395 | baris ledger ber-ID | RUN-KITA | `grep -c '^| [A-Z]' docs/RND_PROVENANCE_LEDGER.md` | §1.1 | TERUKUR |
| V1-04 | 1.185 | nilai numerik unik | DERIVASI | normalisasi `numcov.py` atas ledger: koma desimal ke titik, pemisah ribuan dibuang, pembulatan 9 desimal | §1.1 | TERUKUR |
| V1-05 | 3.227 | token angka data | RUN-KITA | `scratch/rnd_v1/v1_number_cov.json` kunci `docs.*.total_data_numbers` | §3 | TERUKUR |
| V1-06 | 3.118 | token cocok | RUN-KITA | `v1_number_cov.json` kunci `docs.*.matched` | §3 | TERUKUR |
| V1-07 | 109 | token tidak cocok | RUN-KITA | `v1_number_cov.json` kunci `docs.*.unmatched` | §3 | TERUKUR |
| V1-08 | 96,62 | persen | DERIVASI | 3.118 / 3.227 = 0,966222, dibulatkan 96,62 | §3 | TERUKUR |
| V1-09 | 58 | token struktural | RUN-KITA | `scratch/rnd_v1/classify.py` (nomor halaman rujukan, nomor baris kode, nomor standar) | §1.3, §3 | TERUKUR |
| V1-10 | 51 | kandidat angka | DERIVASI | 109 dikurangi 58 = 51 | §3 | TERUKUR |
| V1-11 | 12 | temuan nyata | DERIVASI | hasil pemeriksaan manual 51 kandidat, tabel §4 dokumen ini | §4 | TERUKUR |
| V1-12 | 143 | DOI unik | RUN-KITA | `scratch/rnd_v1/v1_extract.json` (gabungan 11 dokumen) | §2.1 | TERUKUR |
| V1-13 | 177 | kemunculan DOI | RUN-KITA | `scratch/rnd_v1/doistat.py` (jumlah DOI per dokumen, dobel antar dokumen dihitung) | §2.1 | TERUKUR |
| V1-14 | 174 | kemunculan lolos dua lapis | RUN-KITA | `scratch/rnd_v1/v1_verify.json` (doi.org 3xx dan Crossref 200) | §2.1 | TERUKUR |
| V1-15 | 3 | kemunculan gagal | RUN-KITA | `v1_verify.json` (doi.org 404 dan Crossref 404) | §2.1 | TERUKUR |
| V1-16 | 2 | DOI unik gagal | JURNAL | `10.1109/TII.2019.2950661` (doi.org 404, Crossref 404) dan `10.2307/4615733` Holm 1979 (doi.org 404, Crossref 404); keduanya sudah ditandai gagal di dokumen sumber | §2.2, §5 | BELUM TERVERIFIKASI |
| V1-17 | 17 | URL diuji | RUN-KITA | `v1_verify.json` kunci `url` (GET, redirect diikuti) | §2.3 | TERUKUR |
| V1-18 | 11 / 3 / 3 | status 200 / 403 / 202 | RUN-KITA | `v1_verify.json` kunci `url.*.status` | §2.3 | TERUKUR |
| V1-19 | 21 | DOI R3 lolos dua lapis | RUN-KITA | `v1_verify.json` untuk 21 DOI di `docs/RND_R3_VMD_SVM.md` | §2.4 | TERUKUR |
| V1-20 | 5 | DOI menunjuk makalah lain dalam 4 rujukan | RUN-KITA | pembacaan dokumen sumber: `RND_R3_VMD_SVM.md:140` (dua DOI), `RND_E1_MATRIKS.md:433` (satu DOI), `RND_R4_BOOSTING.md:280` (dua DOI kandidat) | §2.4, §5 | TERUKUR |
| V1-21 | 74 | baris klaim komparatif | RUN-KITA | `scratch/rnd_v1/claims.json` (pola lebih baik, unggul, menang, terbaik, superior) | §4.1 | TERUKUR |
| V1-22 | 9 | dokumen dengan klaim komparatif | RUN-KITA | `claims.json` kunci (D0 dan P0 tidak memuat) | §4.1 | TERUKUR |
| V1-23 | 87,95 | persen cakupan E0 (terendah) | DERIVASI | 387 / 440 = 0,879545, dibulatkan 87,95 | §3 | TERUKUR |
| V1-24 | 100,00 | persen cakupan E1 (tertinggi) | DERIVASI | 181 / 181 = 1,0 | §3 | TERUKUR |

Catatan: tabel bagian ini memakai 7 kolom data. Bagian P0 memakai 8 kolom karena menyertakan kolom "Tanggal akses" terpisah; tanggal akses seluruh baris V1 dinyatakan satu kali di atas tabel.

## Bagian E3: eksekusi pilot pada hyd K-i (kartu `t_13309129`)

Dokumen pendamping: `docs/RND_E3_HASIL.md`. Sumber: `scratch/rnd/e3/e3_a_conformal_results.json`, `e3_a1b_lag_results.json`, `e3_b_cusum_results.json`, `e3_baseline_results.json`, `e3_budget.json`, `e3_cakupan.json`, `e3_verify.json`, `e3_doi.json`, `e3_run_summary.json`. Setiap baris di-assert terhadap path JSON oleh `code/rnd_e3_ledger.py`; assert yang gagal membatalkan seluruh penulisan.

| No | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| E3-001 | 52509 | baris | RUN-KITA | `scratch/rnd/e3/e3_verify.json` ``v6_total.n_baris`` | 2026-10-27 | bagian 2 | TERUKUR |
| E3-002 | 9 | well/fold | RUN-KITA | `scratch/rnd/e3/e3_run_summary.json` ``n_folds`` | 2026-10-27 | bagian 2, 4 | TERUKUR |
| E3-003 | 41 | fitur A1 | RUN-KITA | `scratch/rnd/e3/e3_verify.json` ``v5_audit_fitur.n_fitur_A1`` | 2026-10-27 | bagian 3.1 | TERUKUR |
| E3-004 | 43 | fitur A1b | RUN-KITA | `scratch/rnd/e3/e3_verify.json` ``v5_audit_fitur.n_fitur_A1b`` | 2026-10-27 | bagian 3.2 | TERUKUR |
| E3-005 | 233.7 | detik | RUN-KITA | `scratch/rnd/e3/e3_run_summary.json` ``elapsed_s`` | 2026-10-27 | bagian 2, 6 | TERUKUR |
| E3-006 | 1941 | FP | RUN-KITA | `scratch/rnd/e3/e3_baseline_results.json` ``total_fp.persistence`` | 2026-10-27 | bagian 4.1 | TERUKUR |
| E3-007 | 195 | FP | RUN-KITA | `scratch/rnd/e3/e3_baseline_results.json` ``total_fp.hybrid_rule_lag1_and_persistence`` | 2026-10-27 | bagian 4.1 | TERUKUR |
| E3-008 | 32,17 sampai 109,69 | FP per 24 jam | DERIVASI | `scratch/rnd/e3/e3_baseline_results.json` ``folds[].far_per_24h` model persistence` ; FAR = FP/(n_neg/60)*24 | 2026-10-27 | bagian 4.1 | TERVERIFIKASI (assert V1, deviasi 0,0) |
| E3-009 | 2,77 sampai 19,31 | FP per 24 jam | DERIVASI | `scratch/rnd/e3/e3_baseline_results.json` ``folds[].far_per_24h` model hybrid proxy` ; FAR = FP/(n_neg/60)*24 | 2026-10-27 | bagian 4.1 | TERVERIFIKASI (assert V1) |
| E3-010 | 0 dari 9 | fold lulus gate A | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v3b_gate_A_baseline_hitung_manual.persistence`` | 2026-10-27 | bagian 4.1, 5 | TERVERIFIKASI |
| E3-011 | 4 dari 9 | fold lulus gate A | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v3b_gate_A_baseline_hitung_manual.hybrid_proxy`` = F-10, F-14, F-15A, F-5 | 2026-10-27 | bagian 4.1, 5 | TERVERIFIKASI |
| E3-012 | 0,00 sampai 543,50 | FP per 24 jam | DERIVASI | `scratch/rnd/e3/e3_a_conformal_results.json` ``folds[]` seed 42 `far_per_24h`` ; median 86,72 | 2026-10-27 | bagian 4.2, 5 | TERVERIFIKASI (assert V1) |
| E3-013 | 63,29 | FP per 24 jam median 45 fold-run | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v4_rentang.A1_semua_seed_far.median`` | 2026-10-27 | bagian 4.2 | TERVERIFIKASI |
| E3-014 | 0,0010 sampai 0,5057 | recall | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v4_rentang.A1_seed42_recall`` ; median 0,0740 | 2026-10-27 | bagian 4.2 | TERVERIFIKASI |
| E3-015 | 2 dari 9 | fold lulus gate A seed 42 | DERIVASI | `scratch/rnd/e3/e3_run_summary.json` ``fold_gate_A_A1_seed42`` | 2026-10-27 | bagian 4.2, 5 | TERVERIFIKASI |
| E3-016 | 3 dari 45 | fold-run lulus gate A semua seed | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v3_gate_A.A1.n_gate_A_lulus` = 3 dari `n_fold` = 45` | 2026-10-27 | bagian 4.2, 5 | TERVERIFIKASI |
| E3-017 | 0,05 sampai 0,20 | alpha conformal terpilih | DERIVASI | `scratch/rnd/e3/e3_budget.json` ``A1_alpha_vs_anggaran_seed42[].alpha_dipilih`` | 2026-10-27 | bagian 4.2, 6.2 | TERVERIFIKASI |
| E3-018 | 127,49 sampai 232,66 | FP per 24 jam A2 reset | DERIVASI | `scratch/rnd/e3/e3_b_cusum_results.json` ``varian.reset.folds[].far_per_24h`` | 2026-10-27 | bagian 4.3, 5 | TERVERIFIKASI (assert V1) |
| E3-019 | 0,3871 sampai 0,8038 | recall A2 reset | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v4_rentang.A2_reset_recall`` | 2026-10-27 | bagian 4.3 | TERVERIFIKASI |
| E3-020 | 1330,94 sampai 1440,00 | FP per 24 jam A2 tanpa reset | DERIVASI | `scratch/rnd/e3/e3_b_cusum_results.json` ``varian.tanpa_reset.folds[].far_per_24h`` | 2026-10-27 | bagian 4.3, 5 | TERVERIFIKASI (assert V1) |
| E3-021 | 0,8882 sampai 1,0000 | recall A2 tanpa reset | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v4_rentang.A2_tanpa_reset_recall`` | 2026-10-27 | bagian 4.3 | TERVERIFIKASI |
| E3-022 | 0 dari 9 | fold lulus gate A A2 (kedua varian) | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v3_gate_A.A2_reset` dan `A2_tanpa_reset`` | 2026-10-27 | bagian 4.3, 5 | TERVERIFIKASI |
| E3-023 | 0,00 sampai 24,14 | FP per 24 jam A1b | DERIVASI | `scratch/rnd/e3/e3_a1b_lag_results.json` ``folds[].far_per_24h`` | 2026-10-27 | bagian 4.4 | TERVERIFIKASI |
| E3-024 | 0,4737 sampai 0,9645 | presisi A1b (8 fold berpresisi terdefinisi) | DERIVASI | `scratch/rnd/e3/e3_verify.json` ``v4_rentang.A1b_precision`` ; F-9_A presisi tidak terdefinisi (0 alarm) | 2026-10-27 | bagian 4.4 | TERVERIFIKASI |
| E3-025 | 2 | kolom turunan label dipakai A1b | RUN-KITA | `scratch/rnd/e3/e3_verify.json` ``v5_audit_fitur.kolom_turunan_label_dipakai_A1b`` = y_prev_hyd, valid_prev_hyd ; melanggar E2 §2.3 L3 | 2026-10-27 | bagian 4.4, 5 | TERVERIFIKASI |
| E3-026 | 0,00416667 | fraksi menit negatif yang boleh menyala | KONVENSI | 6 alarm / 1440 menit ; ambang gate A dari docs/RND_ALGO_RESEARCH_PLAN.md §6 dan docs/RND_E2_PROTOKOL.md §5.2 ; dihitung ulang di `code/rnd_e3_budget.py` | 2026-10-27 | bagian 6.1 | TERVERIFIKASI |
| E3-027 | 12 sampai 48 | kali lipat di atas anggaran (alpha A1) | DERIVASI | `scratch/rnd/e3/e3_budget.json` ``A1_alpha_vs_anggaran_seed42[].kelebihan_kali`` = 12, 12, 12, 48, 12, 48, 12, 12, 24 | 2026-10-27 | bagian 6.1 | TERVERIFIKASI |
| E3-028 | 0,377428 | fraksi menit negatif menyala tertinggi A1 | DERIVASI | `scratch/rnd/e3/e3_budget.json` ``A1_seed42[].fraksi_menit_menyala` maks` ; 90,6 kali anggaran | 2026-10-27 | bagian 6.1 | TERVERIFIKASI |
| E3-029 | 0,0885 sampai 0,1616 | fraksi menit negatif menyala A2 reset | DERIVASI | `scratch/rnd/e3/e3_budget.json` ``A2_reset[].fraksi_menit_menyala`` ; 21,2 sampai 38,8 kali anggaran | 2026-10-27 | bagian 6.1 | TERVERIFIKASI |
| E3-030 | 0,9243 sampai 1,0000 | fraksi menit negatif menyala A2 tanpa reset | DERIVASI | `scratch/rnd/e3/e3_budget.json` ``A2_tanpa_reset[].fraksi_menit_menyala`` ; 221,8 sampai 240,0 kali anggaran | 2026-10-27 | bagian 6.1 | TERVERIFIKASI |
| E3-031 | 0,0171 sampai 0,6730 | cakupan waktu teramati per fold | DERIVASI | `scratch/rnd/e3/e3_cakupan.json` ``per_fold[].fraksi`` | 2026-10-27 | bagian 3, 5.1 | TERUKUR |
| E3-032 | 1 dari 9 | fold dengan cakupan >= 50 persen | DERIVASI | `scratch/rnd/e3/e3_cakupan.json` ``per_fold[].fraksi` ; hanya F-10 = 0,6730` ; E2 §4.1 butir (d) melarang sertifikasi fold dengan cakupan < 50 persen | 2026-10-27 | bagian 5.1 | TERVERIFIKASI |
| E3-033 | 113 | pemeriksaan verifikasi | RUN-KITA | `scratch/rnd/e3/e3_verify.json` ``checks` panjang ; 0 gagal` ; `code/rnd_e3_verify.py` | 2026-10-27 | bagian 3, 7 | TERUKUR |
| E3-034 | 7 dari 7 | rujukan dengan metadata terverifikasi | RUN-KITA | `scratch/rnd/e3/e3_doi.json` ``refs[].metadata_terverifikasi`` ; `code/rnd_e3_doi.py` | 2026-10-27 | bagian 8 | TERUKUR |
| E3-035 | 4 | penerbit membalas 403 (blokir bot) | RUN-KITA | `scratch/rnd/e3/e3_doi.json` ``refs[].lapis3_akses` = 403` ; Lei, Page, Garwood, Siffer | 2026-10-27 | bagian 8 | TERUKUR |
| E3-036 | BELUM TERUKUR | jam orang gate B | BELUM-TERUKUR | tidak ada data durasi pemeriksaan manusia per alarm pada repo; gate B tidak dapat dihitung | 2026-10-27 | bagian 5.3 | BELUM TERUKUR |

Jumlah baris: 36. Baris BELUM-TERUKUR: 1 (E3-036, gate B).

### Rekap kelas sumber E3

- RUN-KITA: 11 baris
- DERIVASI: 23 baris
- KONVENSI: 1 baris
- BELUM-TERUKUR: 1 baris

### Yang tetap belum terukur pada E3

- Jam orang dan beban pemeriksaan manusia (gate B), karena tidak ada data durasi inspeksi per alarm di repo ini.
- FAR pada satuan bengkel untuk hyd, karena hyd adalah engine rig dan konvensinya per 24 jam.
- Kestabilan gate C antar seed untuk A2, karena ambang CUSUM dikalibrasi deterministik sehingga seed tidak berlaku.

## Bagian R7: review R&D atas hasil engineer (kartu `t_f366fdcf`)

Tanggal: 2026-10-27. Dokumen: `docs/RND_R7_REVIEW.md`. Semua baris di bawah di-assert oleh
`scratch/rnd/r7/r7_ledger.py` terhadap berkas JSON yang disebut. Baris BELUM-TERUKUR ditulis
tanpa angka tebakan.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| R7-001 | 2105 | FP | RUN-KITA | `scratch/rnd/r7/r7_measure.json` `total_fp.rule`; skrip `scratch/rnd/r7/r7_measure.py` | 2026-10-27 | bagian 3.2, 6.1, 8 | TERUKUR |
| R7-002 | 927 | FP | RUN-KITA | `scratch/rnd/r7/r7_measure.json` `total_fp.hyb` | 2026-10-27 | bagian 3.2, 6.1 | TERUKUR |
| R7-003 | 195 | FP | RUN-KITA | `scratch/rnd/e3/e3_baseline_results.json` `total_fp.hybrid_rule_lag1_and_persistence` | 2026-10-27 | bagian 3.2, 6.1, 10 | TERUKUR |
| R7-004 | 1941 | FP | RUN-KITA | `scratch/rnd/e3/e3_baseline_results.json` `total_fp.persistence` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-005 | 2091 | FP | RUN-KITA | `docs/V9_EVAL_C_LAYERC.md` baris 177 (angka kampanye V9, hybrid FP 2091 turun 927) | 2026-10-27 | bagian 3.2, 4.2 | TERUKUR |
| R7-006 | 14.624 | FAR per 24 jam | RUN-KITA | `r7_measure.json` `baseline` model `hybrid_jujur`, min `far24` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-007 | 58.431 | FAR per 24 jam | RUN-KITA | `r7_measure.json` `baseline` model `hybrid_jujur`, maks `far24` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-008 | 2.774 | FAR per 24 jam | RUN-KITA | `r7_measure.json` `baseline` model `hybrid_proxy_E3`, min | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-009 | 19.313 | FAR per 24 jam | RUN-KITA | `r7_measure.json` `baseline` model `hybrid_proxy_E3`, maks | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-010 | 0.7236 | presisi | RUN-KITA | `r7_measure.json` `baseline` `hybrid_jujur` min `prec` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-011 | 0.9484 | presisi | RUN-KITA | `r7_measure.json` `baseline` `hybrid_jujur` maks `prec` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-012 | 0.5247 | recall | RUN-KITA | `r7_measure.json` `baseline` `hybrid_jujur` min `rec` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-013 | 0.8702 | recall | RUN-KITA | `r7_measure.json` `baseline` `hybrid_jujur` maks `rec` | 2026-10-27 | bagian 3.2 | TERUKUR |
| R7-014 | 0 | fold | DERIVASI | hitung dari `r7_measure.json` `baseline` `hybrid_jujur` `gateA` (syarat FAR tidak lebih dari 6) | 2026-10-27 | bagian 3.2, 4.1 | TERUKUR |
| R7-015 | 4 | fold | DERIVASI | hitung dari `r7_measure.json` `baseline` `hybrid_proxy_E3` `gateA` | 2026-10-27 | bagian 3.2, 4.1 | TERUKUR |
| R7-016 | 4.75 | rasio | DERIVASI | 927 / 195 dari R7-002 dan R7-003 | 2026-10-27 | bagian 3.2, 6.1 | TERUKUR |
| R7-017 | 86.722 | FAR per 24 jam | RUN-KITA | `scratch/rnd/r7/r7_measure2.json` `a1.asis_alpha_E2` median `far_per_24h` | 2026-10-27 | bagian 3.1, 4.1, 5.1 | TERUKUR |
| R7-018 | 2.718 | FAR per 24 jam | RUN-KITA | `r7_measure2.json` `a1.asis_alpha_budget` median | 2026-10-27 | bagian 4.1, 5.1, 9.2 | TERUKUR |
| R7-019 | 0.0 | recall | RUN-KITA | `r7_measure2.json` `a1.asis_alpha_budget` median `recall` | 2026-10-27 | bagian 4.1, 5.1, 13 | TERUKUR |
| R7-020 | 6 | fold | DERIVASI | hitung fold dengan `recall` = 0 pada `a1.asis_alpha_budget` | 2026-10-27 | bagian 5.1, 13 | TERUKUR |
| R7-021 | 6 | fold | DERIVASI | hitung `gateA` pada `a1.asis_alpha_budget` | 2026-10-27 | bagian 4.1, 5.1, 9.2 | TERUKUR |
| R7-022 | 121.911 | FAR per 24 jam | RUN-KITA | `r7_measure2.json` `a1.clean_alpha_E2` median | 2026-10-27 | bagian 5.2, 6.2 | TERUKUR |
| R7-023 | 0.1384 | AUPRC | RUN-KITA | `r7_measure2.json` `a1.clean_alpha_E2` median `auprc` | 2026-10-27 | bagian 5.1, 5.2, 6.2 | TERUKUR |
| R7-024 | 0.1549 | AUPRC | RUN-KITA | `r7_measure2.json` `a1.asis_alpha_E2` median `auprc` | 2026-10-27 | bagian 5.1, 5.2, 6.2 | TERUKUR |
| R7-025 | 7 | fold | DERIVASI | hitung `gateA` pada `a1.clean_alpha_budget` | 2026-10-27 | bagian 9.2 | TERUKUR |
| R7-026 | 151.158 | FAR per 24 jam | RUN-KITA | `r7_measure2.json` `a2_kejadian` median `far24_baris` | 2026-10-27 | bagian 3.3, 5.2, 7 | TERUKUR |
| R7-027 | 69.17 | FAR per 24 jam | RUN-KITA | `r7_measure2.json` `a2_kejadian` median `far24_kejadian` | 2026-10-27 | bagian 3.3, 4.1, 7 | TERUKUR |
| R7-028 | 2.862 | rasio | DERIVASI | median `rasio_baris_per_kejadian` pada `a2_kejadian` | 2026-10-27 | bagian 3.3, 5.2, 7 | TERUKUR |
| R7-029 | 1.412 | rasio | DERIVASI | min `rasio_baris_per_kejadian` | 2026-10-27 | bagian 3.3 | TERUKUR |
| R7-030 | 6.917 | rasio | DERIVASI | maks `rasio_baris_per_kejadian` | 2026-10-27 | bagian 3.3 | TERUKUR |
| R7-031 | 41 | fitur | RUN-KITA | `scratch/rnd/r7/r7_probe.json` `n_feats` | 2026-10-27 | bagian 3.4, 6.2, 8 | TERUKUR |
| R7-032 | 40 | fitur | RUN-KITA | `r7_probe.json` `n_feats_tanpa_ts_bin` | 2026-10-27 | bagian 3.4, 6.2, 8 | TERUKUR |
| R7-033 | 0.00416667 | fraksi menit negatif | KONVENSI | `scratch/rnd/e3/e3_budget.json` `anggaran_fraksi_menit_negatif`; konvensi FAR tidak lebih dari 6 per 24 jam (V9, plan bagian 6) | 2026-10-27 | bagian 5.1, 8 | TERUKUR |
| R7-034 | 5427 | FP | DERIVASI | jumlah `fp` sembilan fold `a1.asis_alpha_E2` | 2026-10-27 | bagian 4.2 | TERUKUR |
| R7-035 | 1919 | FP | DERIVASI | jumlah `fp_kejadian` sembilan well `a2_kejadian` | 2026-10-27 | bagian 4.2 | TERUKUR |
| R7-036 | 1.0 | menit | RUN-KITA | `scratch/rnd/r7/r7_delay.json` min `delay_median` | 2026-10-27 | bagian 3.2, 14 | TERUKUR |
| R7-037 | 10.0 | menit | RUN-KITA | `r7_delay.json` maks `delay_median` | 2026-10-27 | bagian 3.2, 14 | TERUKUR |
| R7-038 | 8 | DOI | RUN-KITA | `scratch/rnd/r7/r7_doi.json`, lapis 1 HEAD doi.org tanpa redirect (302) | 2026-10-27 | bagian 11 | TERUKUR |
| R7-039 | 8 | DOI | RUN-KITA | `r7_doi.json`, lapis 2 Crossref atau DataCite (200) | 2026-10-27 | bagian 11 | TERUKUR |
| R7-040 | 6 | pikiran | RUN-KITA | `mcp__sequentialthinking__sequentialthinking` thoughtNumber 1 sampai 6, thoughtHistoryLength 6 | 2026-10-27 | bagian pembuka | TERUKUR |
| R7-041 | 63.29 | FAR per 24 jam | BELUM-TERUKUR | median 45 fold-run semua seed di `docs/RND_E3_HASIL.md`; tidak dihitung ulang pada review ini | 2026-10-27 | bagian 3.1, 14 | BELUM TERUKUR |
| R7-042 | 3.5 | menit | BELUM-TERUKUR | delay terbit tidak lebih dari 3,5 menit; rekonstruksi jujur memberi 1,0 sampai 10,0 menit sehingga definisi berbeda dan angka terbit tidak sahih pada definisi R7 | 2026-10-27 | bagian 3.2, 4.2, 14 | BELUM TERUKUR |
| R7-043 | 0 | jam orang | BELUM-TERUKUR | gate B beban manusia; tidak ada data durasi inspeksi per alarm di repo | 2026-10-27 | bagian 1, 14 | BELUM TERUKUR |
| R7-044 | 0 | eksperimen | BELUM-TERUKUR | usulan dua tahap (deteksi kandidat lalu klasifikasi) belum diukur; penyempitan kandidat tanpa kehilangan onset masih hipotesis | 2026-10-27 | bagian 9.1, 14 | BELUM TERUKUR |

### Rekap kelas sumber R7

- RUN-KITA: 28 baris
- DERIVASI: 11 baris
- KONVENSI: 1 baris
- BELUM-TERUKUR: 4 baris

### Yang tetap belum terukur pada R7

- Delay baseline terbit tidak lebih dari 3,5 menit: rekonstruksi jujur memberi 1,0 sampai 10,0 menit, jadi angka terbit tidak sahih pada definisi `detection_stats` dan penyebabnya belum dipisahkan (definisi berbeda atau alarm berbeda).
- Median FAR 63,29 pada 45 fold-run semua seed: tidak dihitung ulang, hanya seed 42 yang diverifikasi.
- Dampak pembuangan `ts_bin` pada empat seed lain: belum diukur.
- Usulan dua tahap: belum ada pengukuran penyempitan kandidat.
- Audit label hyd pada ambang 2,5 dan 3: belum dijalankan.
- Gate B beban manusia: belum terukur.

---

## Bagian E4: engineer menjawab temuan R7 (kartu `t_61edf756`)

Sumber angka: `scratch/rnd/e4/*.json`. Setiap baris RUN-KITA dan DERIVASI di-assert terhadap path JSON oleh `scratch/rnd/e4/e4_ledger2.py`; baris yang gagal assert tidak ditulis.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Tanggal akses | Dipakai di | Status |
|---|---|---|---|---|---|---|---|
| E4-001 | 2105 | FP | RUN-KITA | scratch/rnd/e4/e4_baseline.json total_fp.rule_t0m1; 9 fold seed 42+7; python3 code/rnd_e4_pilot.py --seeds 42,7 (run 11:32) | 2026-10-27 | RND_E4 3 R7-1 | TERUKUR |
| E4-002 | 927 | FP | RUN-KITA | scratch/rnd/e4/e4_baseline.json total_fp.hybrid_rule_persistence | 2026-10-27 | RND_E4 3 R7-1 | TERUKUR |
| E4-003 | 1941 | FP | RUN-KITA | scratch/rnd/e4/e4_baseline.json total_fp.persistence | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-004 | 195 | FP | RUN-KITA | scratch/rnd/e4/e4_baseline.json total_fp.hybrid_proxy_E3 (proksi E3, ditolak) | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-005 | 2091 | FP | RUN-KITA | docs/RND_E3_HASIL.md angka terbit; direproduksi R7 3.2 | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-006 | 0.67 | persen | DERIVASI | (2105-2091)/2091 x 100 | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-007 | 0.0 | persen | DERIVASI | (927-927)/927 x 100 | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-008 | 5.0 | persen | KONVENSI | kriteria selesai R7 8 butir 1 | 2026-10-27 | RND_E4 3 | TERUKUR |
| E4-009 | 40 | fitur | RUN-KITA | scratch/rnd/e4/e4_summary.json n_fitur; assert di code/rnd_e4_pilot.py | 2026-10-27 | RND_E4 3 R7-2 | TERUKUR |
| E4-010 | 28.416 | FP/24 jam | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json hybrid_rule_persistence.far24_baris | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-011 | 8.3208 | FP kejadian/24 jam | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json hybrid_rule_persistence.far24_kej | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-012 | 4.0984 | FP/24 jam kalender | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json hybrid_rule_persistence.far24_kal | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-013 | 0.6519 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json hybrid_rule_persistence.recall | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-014 | 0.8243 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json hybrid_rule_persistence.precision | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-015 | 6.7404 | FP/24 jam kalender | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json persistence.far24_kal | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-016 | 0.6791 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json persistence.recall | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-017 | 0.7114 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json persistence.precision | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-018 | 6.932 | FP/24 jam kalender | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json rule_t0m1.far24_kal | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-019 | 0.7507 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json rule_t0m1.recall | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-020 | 0.6835 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json rule_t0m1.precision | 2026-10-27 | RND_E4 4 | TERUKUR |
| E4-021 | 121.9111 | FP/24 jam | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json A1_alpha_E2_lama_seed42.far24_baris; sama dengan R7 P3 tanpa ts_bin | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-022 | 0.133 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json A1_alpha_E2_lama_seed42.recall | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-023 | 0.0 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json A1_alpha_anggaran_seed42.recall | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-024 | 7 | fold | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json A1_alpha_anggaran_seed42.gateA_lama dari 9 | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-025 | 0.0 | FP/24 jam | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json A1_alpha_anggaran_seed42.far24_baris nol alarm | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-026 | 18 | fold-run | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json H_and_hybrid_ML_pooled.gateA_lama dari 18 | 2026-10-27 | RND_E4 5 R7-4 | TERUKUR |
| E4-027 | 0.0 | rasio | RUN-KITA | scratch/rnd/e4/e4_beforeafter.json H_and_hybrid_ML_pooled.recall | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-028 | 13 | fold-run | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json H_and_hybrid_ML.fold_tanpa_alarm dari 18 | 2026-10-27 | RND_E4 5 | TERUKUR |
| E4-029 | 7 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.far_ok_baris dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-030 | 9 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.far_ok_kejadian dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-031 | 9 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.recall_ok dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-032 | 1 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.cakupan_ok dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-033 | 0 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.ketiga_baris dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-034 | 1 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_rule_persistence.ketiga_kejadian dari 9 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-035 | 0.0171 | rasio | RUN-KITA | scratch/rnd/e4/e4_baseline.json folds cakupan.fraksi minimum F-5 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-036 | 0.673 | rasio | RUN-KITA | scratch/rnd/e4/e4_baseline.json folds cakupan.fraksi maksimum F-10 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-037 | 39.36 | kali | DERIVASI | 0,673 / 0,0171 | 2026-10-27 | RND_E4 6 | TERUKUR |
| E4-038 | 0.169119 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.0.laju; python3 scratch/rnd/e4/e4_audit_label.py | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-039 | 2446 | kejadian | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.0.onset_total | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-040 | 1.0 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.0.retensi_vs_2 | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-041 | 0.129673 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.5.laju; python3 scratch/rnd/e4/e4_audit_label.py | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-042 | 2158 | kejadian | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.5.onset_total | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-043 | 0.7668 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.5.retensi_vs_2 | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-044 | 0.093008 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_3.0.laju; python3 scratch/rnd/e4/e4_audit_label.py | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-045 | 1626 | kejadian | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_3.0.onset_total | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-046 | 0.55 | rasio | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_3.0.retensi_vs_2 | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-047 | 87412 | menit teramati | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.0.total_obs 9 well | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-048 | 14783 | menit positif | RUN-KITA | scratch/rnd/e4/e4_audit_label.json agregat.thr_2.0.total_pos | 2026-10-27 | RND_E4 7 | TERUKUR |
| E4-049 | 6.0 | alarm/24 jam | KONVENSI | docs/V9_EVAL_C_LAYERC.md EC-4; R7 4.1 | 2026-10-27 | RND_E4 2 gate A | TERUKUR |
| E4-050 | 0.5 | rasio | KONVENSI | docs/RND_E2_PROTOKOL.md 4.1 butir (d) cakupan | 2026-10-27 | RND_E4 2 gate A | TERUKUR |
| E4-051 | 0.5 | rasio | KONVENSI | docs/RND_R7_REVIEW.md 6.4 syarat recall | 2026-10-27 | RND_E4 2 gate A | TERUKUR |
| E4-052 | 0.004167 | alpha | DERIVASI | 1/240; FAR tidak lebih dari 6/24 jam setara alpha tidak lebih dari 6/1440 | 2026-10-27 | RND_E4 2 | TERUKUR |
| E4-053 | 8 | DOI | RUN-KITA | scratch/rnd/e4/e4_doi.json lapis1 3xx; python3 scratch/rnd/e4/e4_doi.py (run 11:31) | 2026-10-27 | RND_E4 9 | TERUKUR |
| E4-054 | 8 | DOI | RUN-KITA | scratch/rnd/e4/e4_doi.json lapis2 200 crossref/datacite | 2026-10-27 | RND_E4 9 | TERUKUR |
| E4-055 | BELUM TERUKUR | - | BELUM-TERUKUR | tidak ada sumber | 2026-10-27 | RND_E4 10 | BELUM TERUKUR |
| E4-056 | BELUM TERUKUR | - | BELUM-TERUKUR | tidak ada sumber | 2026-10-27 | RND_E4 10 | BELUM TERUKUR |
| E4-057 | BELUM TERUKUR | - | BELUM-TERUKUR | tidak ada sumber | 2026-10-27 | RND_E4 10 | BELUM TERUKUR |
| E4-058 | BELUM TERUKUR | - | BELUM-TERUKUR | tidak ada sumber | 2026-10-27 | RND_E4 10 | BELUM TERUKUR |

### Rekap kelas sumber E4

| Kelas | Jumlah baris |
|---|---|
| RUN-KITA | 46 |
| DERIVASI | 4 |
| KONVENSI | 4 |
| BELUM-TERUKUR | 4 |

Total baris: 58. Baris BELUM-TERUKUR sengaja disertakan supaya cakupan tidak terlihat penuh.

### Yang tetap belum terukur pada E4

1. Gate B beban manusia per alarm tidak terukur karena tidak ada data durasi inspeksi.
2. Delay deteksi pada definisi R7 belum tereproduksi.
3. Penyempitan kandidat dua tahap belum dijalankan.
4. Tidak ada label kegagalan fisik independen, sehingga kesetiaan label proksi belum terukur.

## Bagian R8: evaluasi berlapis per tugas dan uji hybrid (kartu `t_42096685`)

Tanggal akses seluruh baris: 2026-10-27. Dokumen: `docs/RND_R8_EVALUASI_BERLAPIS.md`.
Semua baris RUN-KITA dan DERIVASI di-assert oleh `code/rnd_r8_ledger.py` terhadap berkas JSON
`scratch/rnd/r8/*.json`; baris yang gagal assert tidak ditulis. Tujuh kolom sesuai kartu.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |
|---|---|---|---|---|---|---|
| R8-001 | 2105 | FP | RUN-KITA | r8_hyd.json ringkas.rule_kanal.fp_total | bagian 4.1, 8 | TERUKUR |
| R8-002 | 4361 | FP | RUN-KITA | r8_hyd.json ringkas.stat_cusum.fp_total | bagian 4.1, 8 | TERUKUR |
| R8-003 | 935 | FP | RUN-KITA | r8_hyd.json ringkas.H1_stat_dan_rule.fp_total | bagian 4.1, 8 | TERUKUR |
| R8-004 | 55.58 | persen | DERIVASI | (1 - 935/2105) x 100 | bagian 4.1, 8, 9 | TERUKUR |
| R8-005 | 78.56 | persen | DERIVASI | (1 - 935/4361) x 100 | bagian 4.1, 9 | TERUKUR |
| R8-006 | 5579 | TP | RUN-KITA | r8_hyd.json ringkas.rule_kanal.tp_total | bagian 4.1, 8 | TERUKUR |
| R8-007 | 3804 | TP | RUN-KITA | r8_hyd.json ringkas.H1_stat_dan_rule.tp_total | bagian 4.1, 8 | TERUKUR |
| R8-008 | 31.82 | persen | DERIVASI | (1 - 3804/5579) x 100 | bagian 4.1, 8 | TERUKUR |
| R8-009 | 0.6835 | presisi median | RUN-KITA | r8_hyd.json per_fold.*.precision model rule_kanal | bagian 4.1, 8 | TERUKUR |
| R8-010 | 0.7789 | presisi median | RUN-KITA | r8_hyd.json per_fold.*.precision model H1_stat_dan_rule | bagian 4.1, 8 | TERUKUR |
| R8-011 | 0.5638 | recall median | RUN-KITA | r8_hyd.json per_fold.*.recall model H1 | bagian 4.1, 8, 9 | TERUKUR |
| R8-012 | 3.5302 | FAR per 24 jam | RUN-KITA | r8_hyd.json per_fold.*.far24 model H1 | bagian 4.1, 8, 9 | TERUKUR |
| R8-013 | 6.932 | FAR per 24 jam | RUN-KITA | r8_hyd.json per_fold.*.far24 model rule_kanal | bagian 4.1, 8 | TERUKUR |
| R8-014 | 7 | fold | RUN-KITA | r8_hyd.json ringkas.H1_stat_dan_rule.fold_far_le6 (dari 9) | bagian 4.1, 8 | TERUKUR |
| R8-015 | 3 | fold | RUN-KITA | r8_hyd.json ringkas.rule_kanal.fold_far_le6 (dari 9) | bagian 4.1, 8 | TERUKUR |
| R8-016 | 11.5 | menit | RUN-KITA | r8_hyd.json per_fold.*.lead.lead_median_min model H1 | bagian 4.2, 8, 9 | TERUKUR |
| R8-017 | 6.0 | menit | RUN-KITA | r8_hyd.json per_fold.*.lead.lead_median_min model rule_kanal | bagian 4.2, 8 | TERUKUR |
| R8-018 | 219 | onset | RUN-KITA | r8_hyd.json ringkas.H1_stat_dan_rule.n_diperingatkan | bagian 4.2, 8 | TERUKUR |
| R8-019 | 307 | onset | RUN-KITA | r8_hyd.json ringkas.rule_kanal.n_diperingatkan | bagian 4.2, 8 | TERUKUR |
| R8-020 | 390 | onset | RUN-KITA | r8_hyd.json ringkas.H1_stat_dan_rule.n_onset | bagian 4.2, 8 | TERUKUR |
| R8-021 | 5531 | FP | RUN-KITA | r8_hyd.json ringkas.H1b_stat_atau_rule.fp_total | bagian 4.1 | TERUKUR |
| R8-022 | 0.8195 | recall median | RUN-KITA | r8_hyd.json per_fold.*.recall model H1b | bagian 4.1 | TERUKUR |
| R8-023 | 8.9132 | FAR per 24 jam | RUN-KITA | r8_hyd.json per_fold.F-10.far24 model H1 (nilai terburuk) | bagian 4.1, 8 | TERUKUR |
| R8-024 | 0.4059 | FAR per 24 jam | RUN-KITA | r8_hyd.json per_fold.F-5.far24 model H1 (nilai terbaik) | bagian 4.1, 8 | TERUKUR |
| R8-025 | 2633 | FP | RUN-KITA | r8_shk.json ringkas.ML_saja.fp_total | bagian 5.1, 8 | TERUKUR |
| R8-026 | 667 | FP | RUN-KITA | r8_shk.json ringkas.H2_ML_dan_stat.fp_total | bagian 5.1, 8 | TERUKUR |
| R8-027 | 74.67 | persen | DERIVASI | (1 - 667/2633) x 100 | bagian 5.1, 8 | TERUKUR |
| R8-028 | 192 | TP | RUN-KITA | r8_shk.json ringkas.ML_saja.tp_total | bagian 5.1, 8 | TERUKUR |
| R8-029 | 46 | TP | RUN-KITA | r8_shk.json ringkas.H2_ML_dan_stat.tp_total | bagian 5.1, 8 | TERUKUR |
| R8-030 | 76.04 | persen | DERIVASI | (1 - 46/192) x 100 | bagian 5.1, 8 | TERUKUR |
| R8-031 | 0.0829 | recall median | RUN-KITA | r8_shk.json per_fold.*.recall model ML_saja | bagian 5.1, 8, 9 | TERUKUR |
| R8-032 | 0.0499 | AUPRC median | RUN-KITA | r8_shk.json per_fold.*.auprc model ML_saja | bagian 5.1, 9 | TERUKUR |
| R8-033 | 0.024311 | prevalensi median | RUN-KITA | r8_shk.json per_fold.*.prev model ML_saja | bagian 5.1, 9 | TERUKUR |
| R8-034 | 3.6217 | FAR per 24 jam | RUN-KITA | r8_shk.json per_fold.*.far24 model ML_saja | bagian 5.1, 8 | TERUKUR |
| R8-035 | 8 | fold | RUN-KITA | r8_shk.json ringkas.H2_ML_dan_stat.fold_far_le6 (dari 9) | bagian 5.1, 8 | TERUKUR |
| R8-036 | 908 | FP | RUN-KITA | r8_shk.json ringkas.H2b_ML_dan_stat_atau_rule.fp_total | bagian 5.2 | TERUKUR |
| R8-037 | 0.0375 | recall median | RUN-KITA | r8_shk.json per_fold.*.recall model H2b | bagian 5.2 | TERUKUR |
| R8-038 | 7422 | FP | RUN-KITA | r8_shk.json ringkas.rule_kanal.fp_total | bagian 5.1 | TERUKUR |
| R8-039 | 27.479 | FAR per 24 jam | RUN-KITA | r8_shk.json per_fold.*.far24 model rule_kanal | bagian 5.1 | TERUKUR |
| R8-040 | 0.1723 | recall median | RUN-KITA | r8_shk.json per_fold.*.recall model stat_cusum | bagian 5.1 | TERUKUR |
| R8-041 | 64 | onset | RUN-KITA | r8_shk.json ringkas.ML_saja.n_diperingatkan | bagian 5.2, 8 | TERUKUR |
| R8-042 | 181 | onset | RUN-KITA | r8_shk.json ringkas.ML_saja.n_onset | bagian 5.2, 8 | TERUKUR |
| R8-043 | 0.3385 | balanced accuracy median | RUN-KITA | r8_toolwear.json ringkas model default per_fold.*.bacc | bagian 6.1, 8, 9 | TERUKUR |
| R8-044 | 0.5 | balanced accuracy median | RUN-KITA | r8_toolwear.json ringkas model GWO objF1 per_fold.*.bacc | bagian 6.1, 8, 9 | TERUKUR |
| R8-045 | 0.3993 | balanced accuracy median | RUN-KITA | r8_toolwear.json ringkas model GWO objBacc per_fold.*.bacc | bagian 6.1, 8, 9 | TERUKUR |
| R8-046 | 63 | TP | RUN-KITA | r8_toolwear.json ringkas.ML_default.tp_total | bagian 6.1, 8 | TERUKUR |
| R8-047 | 148 | FP | RUN-KITA | r8_toolwear.json ringkas.ML_default.fp_total | bagian 6.1, 8 | TERUKUR |
| R8-048 | 240 | TP | RUN-KITA | r8_toolwear.json ringkas.H3a_GWO_objF1.tp_total (semua positif) | bagian 6.1, 8 | TERUKUR |
| R8-049 | 229 | FP | RUN-KITA | r8_toolwear.json ringkas.H3a_GWO_objF1.fp_total | bagian 6.1, 8 | TERUKUR |
| R8-050 | 0 | FN | RUN-KITA | r8_toolwear.json ringkas.H3a_GWO_objF1.fn_total | bagian 6.1, 8 | TERUKUR |
| R8-051 | 47 | TP | RUN-KITA | r8_toolwear.json ringkas.H3b_GWO_objBacc.tp_total | bagian 6.1, 8 | TERUKUR |
| R8-052 | 95 | FP | RUN-KITA | r8_toolwear.json ringkas.H3b_GWO_objBacc.fp_total | bagian 6.1, 8 | TERUKUR |
| R8-053 | 469 | jendela | RUN-KITA | scratch/v6_e1/toolwear_windows.csv jumlah baris (T01 120, T02 112, T03 121, T04 116) | bagian 6.1 | TERUKUR |
| R8-054 | 4 | alat | RUN-KITA | scratch/v6_e1/toolwear_windows.csv kolom tool nilai unik | bagian 6.1, 8 | TERUKUR |
| R8-055 | 0.0833 | balanced accuracy | RUN-KITA | r8_toolwear.json per_fold.T01.bacc model ML_default | bagian 6.1, 8 | TERUKUR |
| R8-056 | 0.5323 | balanced accuracy | RUN-KITA | r8_toolwear.json per_fold.T02.bacc model ML_default | bagian 6.1, 8 | TERUKUR |
| R8-057 | 0.2986 | balanced accuracy | RUN-KITA | r8_toolwear.json per_fold.T03.bacc model H3b_GWO_objBacc | bagian 6.1, 8 | TERUKUR |
| R8-058 | 205 | FP | RUN-KITA | r8_stuck.json ringkas.ML_saja.fp_total | bagian 7.1, 8 | TERUKUR |
| R8-059 | 41 | FP | RUN-KITA | r8_stuck.json ringkas.H4_tiga_komponen.fp_total | bagian 7.1, 8 | TERUKUR |
| R8-060 | 79 | TP | RUN-KITA | r8_stuck.json ringkas.ML_saja.tp_total | bagian 7.1, 8 | TERUKUR |
| R8-061 | 17 | TP | RUN-KITA | r8_stuck.json ringkas.H4_tiga_komponen.tp_total | bagian 7.1, 8 | TERUKUR |
| R8-062 | 0.6404 | presisi median | RUN-KITA | r8_stuck.json per_fold.*.precision model H4 (fold berpresisi) | bagian 7.1, 8 | TERUKUR |
| R8-063 | 0.0635 | recall maksimum | RUN-KITA | r8_stuck.json per_fold.*.recall model ML_saja nilai terbesar | bagian 7.1, 8, 9 | TERUKUR |
| R8-064 | 0.133 | recall median | RUN-KITA | r8_stuck.json per_fold.*.recall model stat_cusum | bagian 7.1, 8 | TERUKUR |
| R8-065 | 0.0808 | recall median | RUN-KITA | r8_stuck.json per_fold.*.recall model rule_kanal | bagian 7.1, 8 | TERUKUR |
| R8-066 | 148 | onset | RUN-KITA | r8_stuck.json ringkas.H4_tiga_komponen.n_onset | bagian 7.1, 8 | TERUKUR |
| R8-067 | 13 | onset | RUN-KITA | r8_stuck.json ringkas.H4_tiga_komponen.n_diperingatkan | bagian 7.1, 8 | TERUKUR |
| R8-068 | 25 | FP | RUN-KITA | r8_stuck.json ringkas.H4b_strict_ML_dan_stat_dan_rule.fp_total | bagian 7.1 | TERUKUR |
| R8-069 | 0.0322 | recall median | RUN-KITA | r8_stuck.json per_fold.*.recall model ML_saja | bagian 7.1, 8 | TERUKUR |
| R8-070 | 0.0635 | recall maksimum | RUN-KITA | r8_stuck.json per_fold.*.recall model ML_saja nilai terbesar | bagian 7.1 | TERUKUR |
| R8-071 | 118567 | baris | RUN-KITA | scratch/v9_d1/datasets/stuck_k2.csv.gz jumlah baris data | bagian 7 | TERUKUR |
| R8-072 | 148 | onset | RUN-KITA | r8_stuck.json ringkas.ML_saja.n_onset | bagian 7 | TERUKUR |
| R8-073 | 4 | hybrid | RUN-KITA | empat hybrid dijalankan: H1 hyd, H2 shk, H3 toolwear, H4 stuck (r8_*.json) | bagian 0, 3 | TERUKUR |
| R8-074 | 0.004167 | fraksi menit negatif | KONVENSI | 6 alarm per 24 jam = 6/1440 (RND_EVALUATION_POLICY.md tidak menetapkan; dipakai FAR_MAKS E4) | bagian 3.2 | TERUKUR |
| R8-075 | 9 | fold | RUN-KITA | scratch/v9_d1/lowo_hyd_ki.json n_folds | bagian 4 | TERUKUR |
| R8-076 | 9 | fold | RUN-KITA | scratch/v9_d1/lowo_shk.json n_folds | bagian 5 | TERUKUR |
| R8-077 | 4 | fold | RUN-KITA | scratch/v9_d1/lowo_stuck_k2.json n_folds | bagian 7 | TERUKUR |
| R8-078 | 52509 | baris | RUN-KITA | scratch/v9_d1/datasets/hyd_ki.csv.gz jumlah baris | bagian 4 | TERUKUR |
| R8-079 | 56495 | baris | RUN-KITA | scratch/v9_d1/datasets/shk.csv.gz jumlah baris | bagian 5 | TERUKUR |
| R8-080 | 42 | seed | RUN-KITA | code/rnd_r8_hybrid.py SEED | bagian 3.2 | TERUKUR |
| R8-081 | 60 | menit | KONVENSI | lead time horizon LEAD_HORIZON pada code/rnd_r8_hybrid.py | bagian 4.2, 5.2, 7.1 | TERUKUR |
| R8-082 | 302 | status registrasi doi.org (10.1093/biomet/41.1-2.100) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-083 | 200 | status metadata crossref (10.1093/biomet/41.1-2.100) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-084 | 302 | status registrasi doi.org (10.1007/b106715) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-085 | 200 | status metadata crossref (10.1007/b106715) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-086 | 302 | status registrasi doi.org (10.1109/ICDM.2008.17) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-087 | 200 | status metadata crossref (10.1109/ICDM.2008.17) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-088 | 302 | status registrasi doi.org (10.1016/j.advengsoft.2013.12.007) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-089 | 200 | status metadata crossref (10.1016/j.advengsoft.2013.12.007) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-090 | 302 | status registrasi doi.org (10.48550/arXiv.1803.03639) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-091 | 200 | status metadata datacite (10.48550/arXiv.1803.03639) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-092 | 302 | status registrasi doi.org (10.1145/1541880.1541882) | JURNAL | r8_doi.json lapis1_registrasi; HEAD tanpa redirect | bagian 11 | TERUKUR |
| R8-093 | 200 | status metadata crossref (10.1145/1541880.1541882) | JURNAL | r8_doi.json lapis2.status; judul dan penulis pertama diperiksa | bagian 11 | TERUKUR |
| R8-094 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada sumber terukur untuk nilai maintenance dalam rupiah atau jam henti terhindar | bagian 9, 12 | BELUM TERUKUR |
| R8-095 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada sumber terukur untuk pengurangan pemeriksaan fisik per kejadian (butuh data jadwal inspeksi) | bagian 8, 12 | BELUM TERUKUR |
| R8-096 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada sumber terukur untuk recall pada titik operasi di luar anggaran FAR 6 per 24 jam untuk shk dan stuck | bagian 5, 7, 12 | BELUM TERUKUR |
| R8-097 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada sumber terukur untuk kestabilan lintas kampanye pengeboran 2026-10-12 (tanggal kampanye tidak tersedia per baris) | bagian 9, 12 | BELUM TERUKUR |

## Bagian PM: vonis akhir dan roadmap tier (kartu `t_776c0a03`)

Tanggal akses seluruh baris: 2026-10-27. Dokumen: `docs/RND_PM_VERDICT.md`.
Baris RUN-KITA, DERIVASI, dan JURNAL di-assert terhadap JSON mentah oleh `code/rnd_pm_ledger.py`; baris yang gagal assert tidak ditulis dan proses berhenti.
Tujuh kolom sesuai kartu. Angka yang tidak punya sumber ditulis BELUM TERUKUR.

| # | Angka | Satuan | Kelas sumber | Rujukan persis | Dipakai di | Status |
|---|---|---|---|---|---|---|
| PM-001 | 2.105 | FP | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.fp_total; python3 code/rnd_r8_hybrid.py --task hyd (seed 42) | bagian 2, 3, 4 | TERUKUR |
| PM-002 | 935 | FP | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.fp_total | bagian 2, 3, 4 | TERUKUR |
| PM-003 | 55,58 | persen | DERIVASI | (2105-935)/2105x100 = 55,5819; r8_agg.json turunan.hyd.potong_FP_pct | bagian 2, 4 | TERUKUR |
| PM-004 | 0,6835 | rasio | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.precision_median | bagian 2, 4 | TERUKUR |
| PM-005 | 0,7789 | rasio | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.precision_median | bagian 2, 4 | TERUKUR |
| PM-006 | 0,7507 | rasio | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.recall_median | bagian 2, 4 | TERUKUR |
| PM-007 | 0,5638 | rasio | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.recall_median | bagian 2, 4 | TERUKUR |
| PM-008 | 6 | menit | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.lead_median_median | bagian 2, 4 | TERUKUR |
| PM-009 | 11,5 | menit | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.lead_median_median | bagian 2, 4 | TERUKUR |
| PM-010 | 3 | fold | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.fold_far_le6 dari n_fold 9 | bagian 2, 4 | TERUKUR |
| PM-011 | 7 | fold | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.fold_far_le6 dari n_fold 9 | bagian 2, 4 | TERUKUR |
| PM-012 | 6,932 | alarm/24jam | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.far24_median | bagian 2, 4 | TERUKUR |
| PM-013 | 3,5302 | alarm/24jam | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.far24_median | bagian 2, 4 | TERUKUR |
| PM-014 | 390 | onset | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.n_onset | bagian 2 | TERUKUR |
| PM-015 | 307 | onset | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.n_diperingatkan | bagian 2 | TERUKUR |
| PM-016 | 219 | onset | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.n_diperingatkan | bagian 2 | TERUKUR |
| PM-017 | 5.579 | TP | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.rule_kanal.tp_total | bagian 4 | TERUKUR |
| PM-018 | 3.804 | TP | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1_stat_dan_rule.tp_total | bagian 4 | TERUKUR |
| PM-019 | 31,82 | persen | DERIVASI | (5579-3804)/5579x100 = 31,8157 (r8_hyd ringkas; r8_agg turunan.hyd) | bagian 4 | TERUKUR |
| PM-020 | 5.531 | FP | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.H1b_stat_atau_rule.fp_total (stat ATAU rule) | bagian 2 | TERUKUR |
| PM-021 | 11,0013 | alarm/24jam | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.stat_cusum.far24_median (statistik saja) | bagian 2 | TERUKUR |
| PM-022 | 0,5832 | rasio | RUN-KITA | scratch/rnd/r8/r8_hyd.json ringkas.stat_cusum.recall_median | bagian 2 | TERUKUR |
| PM-023 | 2.633 | FP | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.ML_saja.fp_total | bagian 2, 3 | TERUKUR |
| PM-024 | 192 | TP | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.ML_saja.tp_total | bagian 2, 3 | TERUKUR |
| PM-025 | 667 | FP | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.fp_total | bagian 2, 3 | TERUKUR |
| PM-026 | 46 | TP | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.tp_total | bagian 2, 3 | TERUKUR |
| PM-027 | 74,67 | persen | DERIVASI | (2633-667)/2633x100 = 74,6677; r8_agg.json turunan.shk.potong_FP_pct | bagian 2 | TERUKUR |
| PM-028 | 76,04 | persen | DERIVASI | (192-46)/192x100 = 76,0417; r8_agg.json turunan.shk.drop_TP_pct | bagian 2 | TERUKUR |
| PM-029 | 0,0499 | AUPRC | DERIVASI | median AUPRC 9 fold dari r8_agg.json turunan.shk.auprc; median aritmetik 9 nilai | bagian 2 | TERUKUR |
| PM-030 | 0,024311 | rasio | DERIVASI | median prevalensi 9 fold dari r8_agg.json turunan.shk.prev | bagian 2 | TERUKUR |
| PM-031 | 0,0037 | rasio | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.recall_median | bagian 2 | TERUKUR |
| PM-032 | 181 | onset | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.n_onset | bagian 2 | TERUKUR |
| PM-033 | 21 | onset | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.n_diperingatkan | bagian 2 | TERUKUR |
| PM-034 | 64 | onset | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.ML_saja.n_diperingatkan | bagian 2 | TERUKUR |
| PM-035 | 13 | menit | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.ML_saja.lead_median_median | bagian 2 | TERUKUR |
| PM-036 | 22 | menit | RUN-KITA | scratch/rnd/r8/r8_shk.json ringkas.H2_ML_dan_stat.lead_median_median | bagian 2 | TERUKUR |
| PM-037 | 0,3385 | balanced accuracy | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.bacc_median | bagian 2, 3 | TERUKUR |
| PM-038 | 0,5 | balanced accuracy | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.bacc_median | bagian 2 | TERUKUR |
| PM-039 | 0,3993 | balanced accuracy | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.bacc_median | bagian 2 | TERUKUR |
| PM-040 | 240 | TP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.tp_total (objektif F1 semua-positif) | bagian 2 | TERUKUR |
| PM-041 | 229 | FP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3a_GWO_objF1.fp_total | bagian 2 | TERUKUR |
| PM-042 | 47 | TP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.tp_total | bagian 2 | TERUKUR |
| PM-043 | 95 | FP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.H3b_GWO_objBacc.fp_total | bagian 2 | TERUKUR |
| PM-044 | 63 | TP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.tp_total | bagian 2 | TERUKUR |
| PM-045 | 148 | FP | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.fp_total | bagian 2 | TERUKUR |
| PM-046 | 4 | alat | RUN-KITA | scratch/rnd/r8/r8_toolwear.json ringkas.ML_default.n_fold (LOTO 4 alat) | bagian 2, 6 | TERUKUR |
| PM-047 | 41 | FP | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.fp_total | bagian 2, 3 | TERUKUR |
| PM-048 | 17 | TP | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.tp_total | bagian 2, 3 | TERUKUR |
| PM-049 | 0,6404 | rasio | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.precision_median | bagian 2 | TERUKUR |
| PM-050 | 0,001 | rasio | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.recall_median | bagian 2 | TERUKUR |
| PM-051 | 148 | onset | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.n_onset | bagian 2 | TERUKUR |
| PM-052 | 13 | onset | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.n_diperingatkan | bagian 2 | TERUKUR |
| PM-053 | 0,0322 | rasio | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.ML_saja.recall_median | bagian 3 | TERUKUR |
| PM-054 | 0,133 | rasio | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.stat_cusum.recall_median | bagian 3 | TERUKUR |
| PM-055 | 0,0808 | rasio | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.rule_kanal.recall_median | bagian 3 | TERUKUR |
| PM-056 | 4 | fold | RUN-KITA | scratch/rnd/r8/r8_stuck.json ringkas.H4_tiga_komponen.fold_far_le6 dari n_fold 4 | bagian 3 | TERUKUR |
| PM-057 | 2.091 | FP | RUN-KITA | scratch/rnd/e4/e4_summary.json assert_r7_1.fp_rule_terbit (baseline bins t-1) | bagian 2, 4 | TERUKUR |
| PM-058 | 0,67 | persen | DERIVASI | abs(2105-2091)/2091x100 = 0,6695; e4_summary.json assert_r7_1.selisih_rule_pct | bagian 2, 4 | TERUKUR |
| PM-059 | 927 | FP | RUN-KITA | scratch/rnd/e4/e4_summary.json assert_r7_1.fp_hybrid_terbit | bagian 2, 4 | TERUKUR |
| PM-060 | 0 | persen | DERIVASI | e4_summary.json assert_r7_1.selisih_hybrid_pct (0,00 persen, identik) | bagian 2, 4 | TERUKUR |
| PM-061 | 40 | fitur | RUN-KITA | scratch/rnd/e4/e4_summary.json n_fitur (ts_bin dibuang, 40 fitur) | bagian 4 | TERUKUR |
| PM-062 | 1 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_proxy_E3.ketiga_kejadian dari n 9 | bagian 2, 3, 4 | TERUKUR |
| PM-063 | 9 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json hybrid_proxy_E3.far_dan_recall_kejadian | bagian 2, 4 | TERUKUR |
| PM-064 | 1 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json rule_t0m1.cakupan_ok dari n 9 | bagian 2, 3 | TERUKUR |
| PM-065 | 12 | fold | RUN-KITA | scratch/rnd/e4/e4_gate_decomp.json A1_alpha_anggaran.fold_tanpa_alarm dari n 18 | bagian 2, 5 | TERUKUR |
| PM-066 | 1 | fold | RUN-KITA | scratch/rnd/e4/e4_summary.json ringkas.hybrid_proxy_E3.fold_gate_A_baru | bagian 2, 5 | TERUKUR |
| PM-067 | 0,673 | fraksi cakupan | RUN-KITA | scratch/rnd/e3/e3_cakupan.json per_fold F-10 fraksi = 7571/11249 | bagian 2, 3 | TERUKUR |
| PM-068 | 0,0171 | fraksi cakupan | RUN-KITA | scratch/rnd/e3/e3_cakupan.json per_fold F-5 fraksi = 6332/369549 | bagian 2, 3 | TERUKUR |
| PM-069 | 1 | well | DERIVASI | hitung fraksi >= 0,50 pada e3_cakupan.json per_fold (9 well) | bagian 2, 3 | TERUKUR |
| PM-070 | 3 | fold-run | RUN-KITA | scratch/rnd/e3/e3_verify.json v3_gate_A.A1.n_gate_A_lulus dari n_fold 45 | bagian 2, 5 | TERUKUR |
| PM-071 | 45 | fold-run | RUN-KITA | scratch/rnd/e3/e3_verify.json v3_gate_A.A1.n_fold (5 seed x 9 fold) | bagian 2, 5 | TERUKUR |
| PM-072 | 0 | fold | RUN-KITA | scratch/rnd/e3/e3_verify.json v3_gate_A.A2_reset.n_gate_A_lulus dari 9 | bagian 2 | TERUKUR |
| PM-073 | 63,288391 | alarm/24jam | RUN-KITA | scratch/rnd/e3/e3_verify.json v4_rentang.A1_semua_seed_far.median | bagian 2 | TERUKUR |
| PM-074 | 543,495786 | alarm/24jam | RUN-KITA | scratch/rnd/e3/e3_verify.json v4_rentang.A1_semua_seed_far.max | bagian 2 | TERUKUR |
| PM-075 | 1440 | alarm/24jam | RUN-KITA | scratch/rnd/e3/e3_verify.json v4_rentang.A2_tanpa_reset_far.max (1440 = alarm tiap menit) | bagian 2 | TERUKUR |
| PM-076 | 27 | head | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json jumlah heads pada 7 engines | bagian 0, 3 | TERUKUR |
| PM-077 | 7 | engine | RUN-KITA | scratch/v9_i1/v9_i1_RESULTS.json len(engines) | bagian 3 | TERUKUR |
| PM-078 | 0 | slot | KONVENSI | scratch/v9_i1/v9_i1_RESULTS.json auto_critical_alarm_slots; docs/V9_EVAL_C_LAYERC.md tier | bagian 3, 4, 6 | TERUKUR |
| PM-079 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json page1954 lapis1_status; HEAD doi.org tanpa redirect; 10.1093/biomet/41.1-2.100 | bagian 8 | TERVERIFIKASI |
| PM-080 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json page1954 lapis2_status (crossref); 10.1093/biomet/41.1-2.100 | bagian 8 | TERVERIFIKASI |
| PM-081 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json vovk2005 lapis1_status; HEAD doi.org tanpa redirect; 10.1007/b106715 | bagian 8 | TERVERIFIKASI |
| PM-082 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json vovk2005 lapis2_status (crossref); 10.1007/b106715 | bagian 8 | TERVERIFIKASI |
| PM-083 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json mirjalili2014 lapis1_status; HEAD doi.org tanpa redirect; 10.1016/j.advengsoft.2013.12.007 | bagian 8 | TERVERIFIKASI |
| PM-084 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json mirjalili2014 lapis2_status (crossref); 10.1016/j.advengsoft.2013.12.007 | bagian 8 | TERVERIFIKASI |
| PM-085 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json dragomiretskiy2014 lapis1_status; HEAD doi.org tanpa redirect; 10.1109/TSP.2013.2288675 | bagian 8 | TERVERIFIKASI |
| PM-086 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json dragomiretskiy2014 lapis2_status (crossref); 10.1109/TSP.2013.2288675 | bagian 8 | TERVERIFIKASI |
| PM-087 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json liu2008 lapis1_status; HEAD doi.org tanpa redirect; 10.1109/ICDM.2008.17 | bagian 8 | TERVERIFIKASI |
| PM-088 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json liu2008 lapis2_status (crossref); 10.1109/ICDM.2008.17 | bagian 8 | TERVERIFIKASI |
| PM-089 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json tatbul2018 lapis1_status; HEAD doi.org tanpa redirect; 10.48550/arXiv.1803.03639 | bagian 8 | TERVERIFIKASI |
| PM-090 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json tatbul2018 lapis2_status (datacite); 10.48550/arXiv.1803.03639 | bagian 8 | TERVERIFIKASI |
| PM-091 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json rabiner1989 lapis1_status; HEAD doi.org tanpa redirect; 10.1109/5.18626 | bagian 8 | TERVERIFIKASI |
| PM-092 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json rabiner1989 lapis2_status (crossref); 10.1109/5.18626 | bagian 8 | TERVERIFIKASI |
| PM-093 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json cox1972 lapis1_status; HEAD doi.org tanpa redirect; 10.1111/j.2517-6161.1972.tb00899.x | bagian 8 | TERVERIFIKASI |
| PM-094 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json cox1972 lapis2_status (crossref); 10.1111/j.2517-6161.1972.tb00899.x | bagian 8 | TERVERIFIKASI |
| PM-095 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json ishwaran2008 lapis1_status; HEAD doi.org tanpa redirect; 10.1214/08-AOAS169 | bagian 8 | TERVERIFIKASI |
| PM-096 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json ishwaran2008 lapis2_status (crossref); 10.1214/08-AOAS169 | bagian 8 | TERVERIFIKASI |
| PM-097 | 302 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json chandola2009 lapis1_status; HEAD doi.org tanpa redirect; 10.1145/1541880.1541882 | bagian 8 | TERVERIFIKASI |
| PM-098 | 200 | status HTTP | JURNAL | scratch/rnd/pm/pm_doi.json chandola2009 lapis2_status (crossref); 10.1145/1541880.1541882 | bagian 8 | TERVERIFIKASI |
| PM-099 | 4,1 sampai 496 (119 kali) | alarm/24jam; rasio | RUN-KITA | baris R1-029 (di-assert di Bagian R1) dan R5-072; sumber primer docs/V9_EVAL_C_LAYERC.md 2.1 baris C3; tidak dihitung ulang di kartu PM | bagian 2, 3 | TERUKUR (kutipan) |
| PM-100 | 62,3 | persen baris | RUN-KITA | baris R4-26 (di-assert di Bagian R4); n_nodata 22.385/35.906 pada docs/V9_EVAL_C_LAYERC.md 2.2; tidak dihitung ulang di kartu PM | bagian 3 | TERUKUR (kutipan) |
| PM-101 | 0,5678 | rasio | RUN-KITA | baris E0-021 (di-assert di Bagian E0); peluang minimal satu alarm kebetulan 4/4 alat; tidak dihitung ulang di kartu PM | bagian 3, 4 | TERUKUR (kutipan) |
| PM-102 | 0,0542 | rasio | RUN-KITA | baris E0-022 (di-assert di Bagian E0); recall segmen tool_wear head op_far_calibrated; tidak dihitung ulang di kartu PM | bagian 3, 4 | TERUKUR (kutipan) |
| PM-103 | 0,3333 | Hz | RUN-KITA | baris R3-02 (di-assert di Bagian R3); laju sampel tertinggi kanal; tidak dihitung ulang di kartu PM | bagian 2, 6 | TERUKUR (kutipan) |
| PM-104 | 0,1667 | Hz | RUN-KITA | baris R3-02 (di-assert di Bagian R3); Nyquist = fs/2; tidak dihitung ulang di kartu PM | bagian 2, 6 | TERUKUR (kutipan) |
| PM-105 | 105 | percobaan VMD | RUN-KITA | baris R3-29 (di-assert di Bagian R3); m3_decomp.json; tidak dihitung ulang di kartu PM | bagian 2, 6 | TERUKUR (kutipan) |
| PM-106 | 75 | percobaan gagal | RUN-KITA | baris R3-30 (di-assert di Bagian R3); m3_decomp.json; tidak dihitung ulang di kartu PM | bagian 2, 6 | TERUKUR (kutipan) |
| PM-107 | 134,01 sampai 137.374,35 | jam | RUN-KITA | baris R3-40 (di-assert di Bagian R3); estimasi 1-NN kNN-DTW; tidak dihitung ulang di kartu PM | bagian 2, 6 | TERUKUR (kutipan) |
| PM-108 | 52,293 sampai 60,000 | menit alarm per jam | RUN-KITA | baris R5-032 (di-assert di Bagian R5); CUSUM tanpa reset di luar baseline; tidak dihitung ulang di kartu PM | bagian 2, 3 | TERUKUR (kutipan) |
| PM-109 | 0,0109 | laju alarm baseline | RUN-KITA | baris R5-045 (di-assert di Bagian R5); Isolation Forest median; tidak dihitung ulang di kartu PM | bagian 2 | TERUKUR (kutipan) |
| PM-110 | 6.377 dari 8.107 (78,7 persen) | jendela | RUN-KITA | baris R5-067 (kutipan terverifikasi); sign-flip hyd K-ii; tidak dihitung ulang di kartu PM | bagian 3 | TERUKUR (kutipan) |
| PM-111 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada data biaya dan tidak ada catatan jam henti per kejadian | bagian 3, 6, 7 | BELUM TERUKUR |
| PM-112 | tidak terukur | n/a | BELUM-TERUKUR | tidak ada data jadwal inspeksi dan beban pemeriksaan aktual | bagian 3, 6, 7 | BELUM TERUKUR |
| PM-113 | tidak terukur | n/a | BELUM-TERUKUR | label hanya urutan jendela tanpa stempel waktu | bagian 3, 7 | BELUM TERUKUR |
| PM-114 | tidak terukur | n/a | BELUM-TERUKUR | R8 memakai seed 42 tunggal; E4 memakai dua seed untuk satu assert baseline | bagian 6, 7 | BELUM TERUKUR |
| PM-115 | tidak terukur | n/a | BELUM-TERUKUR | tanggal kampanye tidak tersedia per baris | bagian 6, 7 | BELUM TERUKUR |
| PM-116 | tidak terukur | n/a | BELUM-TERUKUR | R8 hanya menguji hyd, shk, tool_wear, stuck | bagian 3, 6, 7 | BELUM TERUKUR |
| PM-117 | tidak terukur | n/a | BELUM-TERUKUR | belum ada satu run; R1 hanya menilai kelayakan dari literatur | bagian 2, 5, 6 | BELUM TERUKUR |
| PM-118 | tidak terukur | n/a | BELUM-TERUKUR | run pembanding R4 tidak selesai dalam anggaran waktu; E1-018 | bagian 2, 5, 7 | BELUM TERUKUR |
| PM-119 | tidak terukur | n/a | BELUM-TERUKUR | belum pernah dijalankan; hanya usul D-A4 di EVAL_C | bagian 4, 6, 7 | BELUM TERUKUR |
| PM-120 | tidak terukur | n/a | BELUM-TERUKUR | baris pada grid kedalaman 0,015 m, bukan deret waktu; E0 S-6 | bagian 3, 7 | BELUM TERUKUR |
| PM-121 | tidak terukur | n/a | BELUM-TERUKUR | pra-registrasi label belum terbit; REGISTRY menandai BELUM LAYAK PAKAI | bagian 3, 6, 7 | BELUM TERUKUR |
