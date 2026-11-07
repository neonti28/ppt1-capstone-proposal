# RND-E0: AUDIT IMPLEMENTASI Detektor (KEBOCORAN, SIRKULARITAS, KONSISTENSI)

Kartu: `t_57e7d52b` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace audit: `/mnt/d/Capstone 1(v2)` (baca saja, tidak ada file detektor yang diubah)
Objek audit: 7 mode, 11 klaim (K-i/K-ii), 27 head di `REGISTRY` (`code/v9_i1_pipeline.py:74`)
Dokumen pendamping: `docs/RND_PROVENANCE_LEDGER.md` (baris `E0-001` sampai `E0-031`)

Riset pendahuluan: **systematic-debugging**. Dipakai untuk memisahkan gejala dari penyebab: angka presisi yang dilaporkan (gejala) tidak langsung dianggap sebagai akibat bug, melainkan diuji dengan hipotesis bersaing (kebocoran stempel waktu, sirkularitas konstruksi, penyebut FAR, ambang dokumen) lalu tiap hipotesis diuji dengan satu pengukuran yang bisa gagal.

Riset pendahuluan: **statistical-analysis**. Dipakai untuk memilih ukuran yang tidak menipu: presisi dan recall dipecah per subpopulasi (status sudah berlangsung versus onset baru), karena rata-rata tunggal menyembunyikan perbedaan itu; peluang alarm kebetulan dihitung sebagai proses Poisson dari laju alarm terukur, bukan dari intuisi; tidak ada angka yang dirata-ratakan lintas kelas.

Riset pendahuluan: **verification-mandatory**. Dipakai sebagai gerbang: setiap angka di dokumen ini berasal dari eksekusi skrip yang disimpan (`scratch/e0_audit/`), pembacaan ulang `file:baris` yang disebut, dan pemeriksaan silang terhadap angka yang sudah ada di `scratch/v9_i1/v9_i1_RESULTS.json`; angka yang tidak dapat dibuka ditandai BELUM TERVERIFIKASI, bukan dikarang.

Riset pendahuluan: **file-editing**. Dipakai untuk memastikan audit tidak mengubah mesin: semua penulisan hanya menambah satu file baru (`docs/RND_E0_AUDIT_ENGINE.md`) dan menambah baris di ujung `docs/RND_PROVENANCE_LEDGER.md`; tidak ada patch pada `code/`, tidak ada penyentuhan `/mnt/d/Capstone 1` (arsip).

Riset pendahuluan: **sequentialthinking**, total 9 pikiran: 5 pikiran pada penulisan audit (`thoughtNumber` 1 sampai 5, `thoughtHistoryLength` 5, mencakup definisi jendela fitur/label, uji kebocoran pada dataset yang dipakai, pemecahan onset baru versus status berlangsung, pemisahan dua cacat FAR, dan desain uji determinisme dua lapis) ditambah 4 pikiran pada verifikasi ulang (`thoughtNumber` 1 sampai 4, `thoughtHistoryLength` 4, mencakup urutan verifikasi, pembacaan 466 dari 468 field JSON identik, dua koreksi angka yang ditemukan, dan rencana koreksi terbuka).

---

## 0. METODE, ALAT, DAN BATAS

Pengukuran dijalankan dengan `/home/neonti/.venvs/rnd_r3/bin/python` (Python 3.11.15, pandas 3.1.0, numpy 2.4.6, scikit-learn 1.9.1). Skrip audit mengimpor modul detektor apa adanya lewat `importlib`, sehingga angka yang diukur berasal dari fungsi yang sama dengan yang diaudit, bukan reimplementasi.

Lima skrip, semuanya dapat dijalankan ulang (`scratch/e0_audit/`):

| Skrip | Yang diukur | Keluaran |
|---|---|---|
| `e0_audit.py` | stempel waktu kebocoran 6 dataset, presisi rule per subpopulasi, cakupan waktu, determinisme rule, determinisme RF, satuan tool_wear | `e0_audit_results.json` |
| `e0_audit2.py` | asal-usul tiap baris alarm `persistence_event` (stuck K-ii) | `e0_audit_results2.json` |
| `e0_audit3.py` | metrik per head dari `v9_i1_RESULTS.json`, tier/klaim `REGISTRY`, rujukan folder arsip | `e0_audit_results3.json` |
| `e0_audit4.py` | peluang alarm kebetulan tool_wear per alat | `e0_audit_results4.json` |
| `e0_doi.py` | verifikasi DOI lewat Crossref dan `doi.org` | `e0_doi.json` |

Batas yang harus dibaca lebih dulu:

1. Angka di dokumen ini adalah **pengukuran ulang pada dataset yang tersimpan**, bukan eksekusi ulang seluruh kampanye V9. Lingkungan pustaka berbeda dari lingkungan run asli (2026-10-12), jadi selisih kecil terhadap angka yang dilaporkan tidak otomatis berarti angka lama salah. Yang diuji adalah sifat yang tidak bergantung versi: stempel waktu, himpunan alarm, penyebut, dan konsistensi tier.
2. Dataset `vib`, `ssi`, `shk`, `stuck_k1`, `hyd_ki`, `stuck_k2` di `scratch/v9_d1/datasets/` adalah artefak yang dipakai kampanye V9. Audit ini tidak memverifikasi bahwa bins sumbernya masih identik dengan bins saat kampanye.
3. `bit_wear` dan `tool_wear` memakai sumber berbeda (USROP dan toolwear windows), sehingga keduanya diaudit dengan uji yang berbeda dan tidak dibandingkan langsung.

---

## 1. KEBOCORAN MASA DEPAN

### 1.1 Hasil: tidak ada kebocoran pada tingkat stempel waktu

Uji: untuk setiap dataset, hitung `feat_ts_max - lab_ts` per baris. Jika ada satu baris dengan nilai `>= 0`, fitur memakai data yang setara atau melewati awal jendela label, dan itu kebocoran.

| Dataset | baris | `feat_ts_max >= lab_ts` | maks(`feat_ts_max - lab_ts`) | min | `feat_ts_max >= ts_bin` |
|---|---|---|---|---|---|
| vib | 23.922 | 0 | -1 | -6 | 0 |
| ssi | 35.906 | 0 | -1 | -6 | 0 |
| shk | 56.495 | 0 | -1 | -6 | 0 |
| stuck_k1 | 5.555 | 0 | -1 | -6 | 0 |
| stuck_k2 | 118.567 | 0 | -1 | -11 | 0 |
| hyd_ki | 52.509 | 0 | -1 | -6 | 0 |

Nol pelanggaran, nol `feat_ts_max` kosong. Batas atas `-1` berarti menit terakhir yang dipakai fitur selalu `t0-1`, tepat satu menit sebelum jendela label `[t0, t0+10)` dibuka. Ini **VERIFIKASI POSITIF**, bukan temuan.

Mekanismenya di kode konsisten dengan hasil:
`code/v9_d1_02_rig_windows.py:54` menggeser seluruh kanal satu bin sebelum agregasi (`shift(1)`), dan `code/v9_d1_04_stuck_k2.py:209` menghitung `last_present` lalu `.shift(1)` sebelum dicatat sebagai `feat_ts_max`. Tidak ada tempat di dua builder itu yang membaca `ts >= t0`.

### 1.2 Hasil: kanal pembentuk label tidak masuk daftar fitur ML

Uji: periksa apakah kolom fitur memuat kanal yang dipakai membentuk label kelasnya.

- `hyd_ki`: label dibentuk dari residual `SPPA`/`TFLO` (`code/v9_d1_03_rig_datasets.py:119-120`). Dataset `hyd_ki` punya 40 fitur dan **0** di antaranya `SPPA_*`, `TFLO_*`, atau `SPM_*`.
- `vib`, `ssi`, `shk`, `stuck_k1`, `stuck_k2`: memuat `SPPA_*`/`TFLO_*`, tetapi label kelas-kelas itu dibentuk dari `VIBLAT_RT`, `CRPM_RT`, `SHKRSK_RT`, `STUCK_RT` (`code/v9_d1_02_rig_windows.py:39-41`), dan kanal-kanal itu **tidak** ada di daftar fitur. Jadi bukan sirkularitas.
- `code/v9_e_ML_01_train.py:191-193` memuat assert eksplisit yang menolak nama fitur yang mengandung pola label. Assert ini adalah pertahanan yang benar dan patut dipertahankan.

### 1.3 Temuan K-5 (Kritis): kolom masa depan tetap dikirim di dataset

`code/v9_d1_03_rig_datasets.py:104-105` menghitung `obs_hyd` dan `anom_hyd`, lalu `:120` memasukkannya ke daftar kolom yang ditulis ke dataset. Keduanya dihitung **di dalam jendela label** `[t0, t0+10)`, jadi nilainya mengintip masa depan.

Pipeline aman karena `feature_cols()` (`code/v9_i1_pipeline.py:302`) membuang prefiks `obs_`/`anom_` lewat `LABEL_PREFIXES` (`:64`). Tetapi pertahanan itu hanya berlaku untuk kode yang memakai `feature_cols()`. Dataset yang sama dipakai juga oleh `code/v9_e_ML_01_train.py` dan skrip E_STAT di kartu lain, dan siapa pun yang melakukan `df.select_dtypes("number")` pada file ini akan mendapat dua kolom masa depan tanpa peringatan.

Bukti angka: `hyd_ki` 52.509 baris; jumlah baris dengan `anom_hyd > 0` adalah bagian dari jendela label, bukan riwayat. Tidak ada metadata di file yang menyatakan dua kolom itu terlarang sebagai fitur.

Usulan: ganti nama menjadi `ywin_obs_hyd` dan `ywin_anom_hyd` (prefiks `y` sudah masuk `LABEL_PREFIXES`), atau pindahkan keduanya ke file label terpisah, atau tambahkan `README` kolom di `scratch/v9_d1/datasets/` yang menyatakan daftar kolom terlarang. Opsi pertama paling murah dan menutup celah tanpa mengubah perilaku pipeline.

### 1.4 Temuan M-6 (Minor): gerbang kebocoran hanya memeriksa stempel, bukan isi

`code/v9_d1_04_stuck_k2.py` mencatat `feat_ts_max`, dan itu yang diperiksa (termasuk oleh audit ini). Stempel yang benar tidak menjamin isi benar: kalau suatu fitur dihitung dari agregat yang jendelanya ditutup di `t0` tetapi digeser dua kali, stempelnya bisa tetap `t0-1` sementara isinya berasal dari bin lain. Uji isi yang murah: untuk satu fitur `*_mean`, bandingkan nilainya dengan rata-rata manual kanal mentah pada bin `t0-10..t0-1` untuk 20 baris acak. Audit ini tidak melakukannya (lihat §9).

---

## 2. SIRKULARITAS LABEL

Tiga bentuk sirkularitas diakui di kartu: rule `vib`/`shk` memakai kanal yang sama dengan label, `bit_wear` hibrida adalah label itu sendiri, dan label `hyd` adalah proksi SPPA. Ketiganya benar. Yang belum ada adalah **ukuran dampaknya ke presisi yang dilaporkan**, dan itu yang diukur di sini.

### 2.1 Bukti konstruksi: rule adalah label yang dipotong satu bin

`code/v9_e_RULE_01_status.py:229` (`rule_window_identity`) sengaja menghitung ulang label memakai fungsi rule pada jendela 10 bin. Hasilnya:

| Kelas | baris diperiksa | mismatch | identitas |
|---|---|---|---|
| vib | 23.922 | 0 | True |
| ssi | 35.906 | 0 | True |
| shk | 56.495 | 0 | True |
| stuck_k1 | 5.555 | 0 | True |
| hyd_ki | 52.509 | 23 | False |

Empat kelas pertama: label dapat direproduksi **persis** dari fungsi rule. Artinya rule dan label bukan dua pengukuran berbeda atas fenomena yang sama, melainkan satu fungsi pada dua jendela berbeda (rule: bin `t0-1`; label: maksimum `t0..t0+9`). `hyd_ki` gagal 23 baris (0,04%), dibahas sebagai M-1.

### 2.2 Temuan K-1 (Kritis): rule vib/shk/stuck tidak pernah menyala saat status belum aktif

Uji: bagi populasi menjadi `y_prev = 1` (status sudah berlangsung) dan `y_prev = 0` (onset baru), lalu hitung laju alarm dan presisi rule di tiap subpopulasi.

| Mode | P semua | P saat sudah berlangsung | P saat onset baru | laju alarm saat onset baru | FP persistence saja | P persistence saja |
|---|---|---|---|---|---|---|
| vib | 0,9193 | 0,9193 | tidak terdefinisi (0 alarm) | **0,0000** | 1.456 | 0,7352 |
| shk | 0,6134 | 0,6134 | tidak terdefinisi (0 alarm) | **0,0000** | 1.056 | 0,3098 |
| stuck K-i | 0,9587 | 0,9587 | tidak terdefinisi (0 alarm) | **0,0000** | 436 | 0,7819 |
| ssi | 0,2121 | 0,2222 | 0,2083 | 0,0007 | 267 | 0,2415 |
| hyd K-i | 0,7261 | 0,8416 | 0,3573 | 0,0404 | 1.941 | 0,7298 |

Komposisi populasi positif (kolom `y_prev_*`, resep D1): vib 25,53% positif adalah onset baru (1.386 dari 5.429), shk **76,36%** (1.531 dari 2.005), ssi **86,00%** (522 dari 607), hyd 26,90% (1.929 dari 7.172), stuck K-i 22,12% (444 dari 2.007). Untuk vib, rule menyala **nol kali** pada 1.386 baris onset baru itu. Jadi P 0,9193 bukan pernyataan "rule mendeteksi getaran berlebih dengan presisi 92%", melainkan "bila status sudah aktif dan bin terakhir masih melewati ambang, maka status masih aktif 92% dari waktu". Itu pernyataan persistensi, dan memang sesuai dengan `keyakinan` yang ditulis registry (`"rule ⊆ persistence utk kelas definisi-kanal"`, `code/v9_i1_pipeline.py:155-158`). Masalahnya bukan definisi internal, melainkan **cara angka itu dipakai di dokumen evaluasi**: `docs/V9_EVAL_C_LAYERC.md:90` menulis "deteksi rule berpresisi (P 0,87-0,95 di 4 well)" tanpa menyebut bahwa recall terhadap onset baru adalah nol, padahal untuk shk dan ssi mayoritas positif justru onset baru dan rule shk menyala nol kali di sana.

Catatan keadilan: rule tetap memberi nilai di atas persistence murni (vib 0,9193 lawan 0,7352 dengan FP 197 lawan 1.456; shk 0,6134 lawan 0,3098; stuck 0,9587 lawan 0,7819). Jadi rule bukan tak berguna; ia **pengonfirmasi status**, bukan pendeteksi kejadian, dan tier L1-nya harus dibaca begitu.

Usulan: tambah dua kolom wajib di tabel tier EVAL_C, yaitu `P/R pada y_prev=0` dan `P/R pada y_prev=1`, dan ubah kalimat klaim menjadi "konfirmasi status berpresisi, tanpa kemampuan onset". Angka di tabel 2.2 sudah cukup untuk mengisi kolom itu.

### 2.3 Temuan K-2 (Kritis): `persistence_event` memberi kredit lead time ke kejadian yang salah

`code/v9_e_RULE_02_stuck_onset.py:41-51` menaruh alarm pada baris `t` bila `t-1` adalah menit onset. `:54-95` lalu menghitung lead sebagai `lab_ts - ts_bin` pada baris alarm, dan `lab_ts` pada baris itu adalah onset **berikutnya** yang tercatat di jendela 10 menit.

Pengukuran atas `stuck_k2` (118.567 baris, 268 onset):

| Besaran | Nilai |
|---|---|
| baris alarm total | 26 |
| alarm pada baris berlabel positif | 15 |
| alarm pada baris berlabel negatif (FP) | 11 |
| alarm yang pemicunya = onset yang dikreditkan | **0** |
| alarm yang pemicunya onset lain | 15 |
| sebaran lead (menit) | 0×11, 1×2, 2×1, 4×1, 5×2, 6×2, 8×4, 9×1, 10×2 |

Angka FP 11 ini **sama persis** dengan "FP alarm total 11" yang dilaporkan `docs/V9_EVAL_C_LAYERC.md:94`, yang berarti reproduksi audit ini setia. Tetapi 15 alarm yang dianggap "menutup" onset ternyata semuanya dipicu oleh onset yang berbeda dari onset yang diberi kredit. Lead median 7,0 menit karena itu mengukur **jarak ke onset berikutnya**, bukan jarak dari penyebab alarm ke akibatnya.

Dampak: klaim tier "peringatan-dini berbeban rendah dgn arah benar (TLead median 7,0 mnt ... konsisten 3 well)" (`EVAL_C:94`) tidak punya dasar pada mekanisme ini. Dengan himpunan alarm 26 baris dan 0 pemicu yang benar, `n_aktif` head ini di segmen V9 hanya 4 baris (`v9_i1_RESULTS.json`, head `stuck/persistence_event`).

Usulan: hitung lead hanya untuk alarm yang pemicunya sama dengan onset yang dikreditkan, lalu laporkan hasilnya apa adanya (kemungkinan besar 0). Kalau tujuan head ini adalah "konfirmasi onset satu menit setelah kejadian", nyatakan itu dan hapus kata "peringatan-dini" dari badge. Perbaikan mekanis yang lebih berguna: ganti `ts-1 ∈ evset` dengan alarm pada `ts = t_e` (deteksi) atau pada `t_e - H` (sinyal dari fitur, bukan dari daftar event).

### 2.4 Temuan K-3 (Kritis): `tool_wear` L1 berdiri di atas kriteria "pernah menyala sekali"

`code/v9_i1_pipeline.py:594-660` menilai deteksi sebagai `det_R02 = bool(o2.any())` pada run R02 yang panjangnya 58 sampai 62 jendela satu detik. Kriteria itu tidak mengukur recall, hanya "ada minimal satu alarm".

Laju alarm pada data evaluasi R01 terukur 1 sampai 3 FP per 35 sampai 42 jendela (`v9_i1_RESULTS.json`, `tool_wear/op_far_calibrated/per_alat`). Dengan laju itu, peluang mendapat minimal satu alarm di dalam run R02 **tanpa sinyal apa pun** adalah:

| Alat | FP R01 | jendela evaluasi R01 | laju per detik | jendela R02 | harapan alarm kebetulan | P(minimal 1 alarm) |
|---|---|---|---|---|---|---|
| T01 | 1 | 42 | 0,0238 | 60 | 1,43 | 0,7603 |
| T02 | 3 | 35 | 0,0857 | 62 | 5,31 | 0,9951 |
| T03 | 1 | 42 | 0,0238 | 60 | 1,43 | 0,7603 |
| T04 | 3 | 40 | 0,0750 | 58 | 4,35 | 0,9871 |

Peluang "4 dari 4 alat terdeteksi" secara kebetulan = **0,5678**. Sementara metrik segmen pada titik operasi yang sama memberi **recall 0,0542** (tp 13, fn 227) dan **FAR 2,096 alarm per menit negatif** terhadap target 1,0 (`far_unit` di `metrik_segmen`). Jadi klaim "deteksi 4/4 alat, TLead 20-36 dtk" (`EVAL_C:98` dan `:104`) secara statistik tidak dapat dibedakan dari derau pada laju alarm yang dipakai sendiri.

Perhitungan kebetulan ini adalah DERIVASI (model Poisson dari laju terukur), bukan pengukuran langsung; statusnya dicatat di ledger `E0-021` dan tidak dipakai sebagai satu-satunya dasar rekomendasi.

Usulan: ganti `det_R02` dengan recall jendela per alat (angka 0,0542 itu sudah ada dan cukup), laporkan berdampingan dengan peluang kebetulan, lalu turunkan tier L1 `tool_wear` sampai recall pada titik operasi membaik. Kalau ingin tetap L1, titik operasinya harus dipilih untuk recall, bukan hanya untuk FAR.

### 2.5 Temuan S-7 (Sedang): `bit_wear` memang label itu sendiri

`code/v9_i1_pipeline.py:576-592`: label `is_mse` diambil dari kolom `label` USROP, lalu head "persistence" didefinisikan sebagai `is_mse` yang digeser satu baris. Presisi head itu karena itu bukan kinerja model, melainkan autokorelasi label.

Terukur: 198.928 baris, 49.732 positif (prevalensi 0,25). Presisi persistence bergantung pada urutan baris, dan ini diukur tiga kali: 0,9903 pada urutan berkas mentah (yang berkelompok per well), 0,9903 pada urutan `well` lalu `Measured Depth m`, dan **0,5668** pada urutan yang benar-benar dipakai `run_bit_wear` yaitu sort `Measured Depth m` saja (`code/v9_i1_pipeline.py:578`). Pada urutan itu 133.539 dari 198.927 pasangan baris berurutan (67,13%) menyeberang well, jadi "satu baris kemudian" sering bukan lubang sumur yang sama. Angka resmi 0,9927 berasal dari segmen F-14 saja (n 47.645, tp 4.881, fp 36, fn 37, R 0,9925) dan sah untuk segmen itu karena satu well diurutkan kedalaman. Registry menuliskannya sebagai `"bit_wear persistence P0,9927"` dengan tier TREN dan batas `"konfirmasi-status, bukan prediksi onset"`. Itu sudah jujur soal batas. Yang belum: angka 0,9927 mudah dibaca sebagai kinerja model oleh pembaca luar, padahal recall 0,9925 hanya berarti label hampir tidak pernah berubah di antara dua baris berurutan, dan fungsi yang sama menghasilkan 0,5668 bila diberi tujuh well sekaligus.

Usulan: ganti label metrik menjadi `P(label bertahan)` di semua tempat, dan sertakan baseline acak prevalensi (0,25) di sebelahnya supaya pembaca melihat bahwa 0,99 adalah sifat label, bukan sifat detektor.

### 2.6 Temuan S-4 (Sedang): presisi `hyd` jatuh 2,4 kali pada onset baru, tier tidak membedakan

Hyd K-i rule: P 0,8416 saat status berlangsung, P 0,3573 saat onset baru (tabel 2.2). Laju alarmnya turun dari 0,8144 menjadi 0,0404. Ini satu-satunya rule yang benar-benar menyala pada onset baru, dan justru di situ presisinya paling rendah. Tier L1 di `code/v9_i1_pipeline.py:217-221` tidak membedakan kedua rezim, sehingga badge "rule P 0,62-0,96" mencampur keduanya.

Usulan: laporkan dua angka di badge (`P_status` dan `P_onset`), dan pertimbangkan ambang berbeda per rezim.

---

## 3. KONSISTENSI DOKUMEN VERSUS KODE

### 3.1 Yang konsisten (verifikasi positif)

| Butir | Dokumen | Kode | Status |
|---|---|---|---|
| jumlah head | 27 head, 11 klaim | `REGISTRY` menghasilkan 27 head, `decision_layer.ringkasan` L0=5 L1=11 L2=9 L3=2 | cocok |
| tier terlarang | EVAL_C §3, 0 mode ALARM-OTOMATIS | `TIER_FORBIDDEN` + assert `:352`, `:714-718` | cocok |
| jumlah fitur tool_wear | 27 | assert `:605` dan `v9_e_RULE_03_bitwear_toolwear.py:145` | cocok |
| tier vib rule | PERINGATAN-BERPENGAWAS | `:112` | cocok |
| tier shk rule | PERINGATAN-BERPENGAWAS | `:143` | cocok |
| tier bit_wear K-1 | TREN | `:248` | cocok |
| FAR segmen vib F-14 | 10,0-49,9 | 49,942 | cocok |
| FAR segmen hyd | 14,6-58,4 | 16,611 | cocok |

### 3.2 Temuan S-1 (Sedang): `ssi` rule diberi L1 padahal dokumen hanya memberi L1 ke hybrid

`docs/V9_EVAL_C_LAYERC.md:91` menetapkan ssi = "TREN (RF) + PERINGATAN-BERPENGAWAS hemat (hybrid: FP 26→7)" dan `:128` mengulang "TIER: TREN (RF) + PERINGATAN-BERPENGAWAS hemat (hybrid)". Kode memberi tier yang sama ke **dua** head: `rule_display` (`code/v9_i1_pipeline.py:143`) dan `hybrid_rule_and_persistence` (`:155`).

Ukuran rule ssi yang sebenarnya, dari `scratch/v9_e_rule` dan pengukuran ulang:

| Metrik | Nilai |
|---|---|
| presisi kumulatif | 0,2121 |
| presisi per fold (6 fold) | 0,4000 / 0,0000 / 0,2500 / 0,1111 / 0,5000 / 0,2000 |
| recall kumulatif | 0,0115 |
| TP / FP | 7 / 26 |
| `n_aktif` di segmen V9 | **0** |

Head berlabel PERINGATAN-BERPENGAWAS/L1 dengan presisi 0,21 dan nol aktivasi di segmen yang dikirim tidak dapat dipertahankan. Hybrid memang memotong FP 26 menjadi 7 seperti diklaim dokumen, jadi yang perlu diperbaiki hanya tier `rule_display`.

Usulan: turunkan `rule_display` ssi ke TREN/L0 (sama seperti ssi persistence), atau hapus head itu dari registry karena hybrid sudah mencakupnya dengan tier yang benar.

### 3.3 Temuan S-2 (Sedang): `hyd` persistence L1 bertabrakan dengan definisi L0 dan dengan perlakuan detektor lain

`code/v9_i1_pipeline.py:223` memberi `hyd/persistence` tier SUPERV dengan layer L0. Definisi L0 ada di `:289-291`: "status otomatis (rule/persistence = sistem hari-ini, tanpa notifikasi)". Tier PERINGATAN-BERPENGAWAS pada lapisan yang secara definisi tidak memunculkan notifikasi adalah kontradiksi internal.

Bandingkan perlakuan tiga detektor dengan presisi persistence yang sebanding atau lebih tinggi:

| Mode | presisi persistence | FP persistence | tier/layer di kode | presisi tercatat |
|---|---|---|---|---|
| vib | 0,7352 | 1.456 | TREN / L0 (`:118`) | 0,7352 |
| hyd | 0,7298 | 1.941 | **SUPERV / L0** (`:223`) | 0,7298 |
| shk | 0,3098 | 1.056 | TREN / L0 (`:149`) | 0,3098 |

Dua detektor dengan presisi hampir identik mendapat tier berbeda tanpa alasan yang tertulis. `docs/V9_EVAL_C_LAYERC.md` bahkan menempatkan seluruh klaim K-i hyd di SUPERV, jadi kemungkinan sumbernya dokumen, bukan kode. Tetap saja dua sumber itu sekarang tidak sinkron secara internal.

Usulan: pilih satu. Kalau dokumen yang menang, pindahkan hyd persistence ke L1 (dengan `human_review_required`), dan ubah definisi L0. Kalau kode yang menang, turunkan ke TREN.

### 3.4 Temuan M-1 (Minor): identitas `rule_window_identity` gagal untuk `hyd` pada 23 baris

`code/v9_e_RULE_01_status.py:229`: mask observabilitas yang dipakai untuk menghitung ulang label tidak identik dengan mask yang dipakai `code/v9_d1_03_rig_datasets.py` saat membentuk label. 23 dari 52.509 baris (0,04%) berbeda. Kecil, tetapi artinya klaim "rule adalah pembentuk label" tidak persis benar untuk hyd, dan pembaca yang memakai pemeriksa identitas ini akan mendapat `False` tanpa penjelasan.

Usulan: satukan definisi mask (satu fungsi dipakai dua tempat) dan naikkan toleransi mismatch ke 0 dengan penjelasan bila memang ada baris yang sengaja dikecualikan.

### 3.5 Temuan M-2 (Minor): `TLead` tool_wear adalah jarak ke akhir run, bukan jarak ke kerusakan

`code/v9_i1_pipeline.py:653-660`: `TLead_s = len(r02) - first_alarm`. Karena seluruh jendela R02 berlabel 1 (y = 1 untuk 60 jendela penuh, diperiksa pada `scratch/v6_e1/toolwear_windows.csv`), tidak ada "waktu kerusakan" di dalam run yang bisa dijadikan acuan. TLead 20-36 detik karena itu berarti "alarm pertama muncul 20-36 detik sebelum run berakhir".

Usulan: nyatakan definisi ini di dokumen, atau ubah acuan ke titik perubahan kondisi yang sebenarnya (R01 ke R02) dan laporkan waktu dari awal R02 sampai alarm pertama. Angka kedua itu bisa dihitung dari data yang ada.

### 3.6 Temuan M-3 (Minor): rantai `tool_wear` masih bergantung pada folder arsip

`code/v6_e1_50_toolwear.py` menulis keluarannya ke `/mnt/d/Capstone 1/scratch/v6_e1/...` (folder arsip, dilarang disentuh kartu ini). Rantai V9 membaca salinan di `scratch/v6_e1/toolwear_windows.csv`, jadi audit V9 tidak menyentuh arsip. Tetapi **derivasi ulang** fitur tool_wear dari data mentah tidak dapat dilakukan di dalam workspace v2 tanpa memindahkan jalur itu.

Diperiksa: 65 skrip `.py` di `code/` masih menyebut `/mnt/d/Capstone 1/`, dan **0 dari 65** di antaranya berprefiks `v9_`. Jadi rantai V9 bersih, hanya hulunya yang tidak.

Usulan: ganti `SRC`/`OUT` di `v6_e1_50_toolwear.py` ke jalur v2 dan salin data mentah toolwear ke `data/`, atau tandai skrip itu sebagai "tidak dapat dijalankan ulang di v2" di README.

### 3.7 Temuan M-4 (Minor): `q` kuantil tool_wear adalah konstanta yang menyamar sebagai rumus

`code/v9_i1_pipeline.py:631`: `q = 1.0 - TARGET_FP_PER_MIN * (len(ev1)/60.0) / max(len(ev1), 1)`. Faktor `len(ev1)` muncul di pembilang dan penyebut, jadi hasilnya selalu `1 - 1/60 = 0,983333` untuk setiap ukuran data (diperiksa pada n = 100, 469, 1.000, 5.000, semuanya 0,983333). Rumus ini tidak menyesuaikan diri dengan panjang jendela; kalau `win_s` berubah dari 60, angkanya menjadi salah tanpa error.

Usulan: tulis `q = 1.0 - TARGET_FP_PER_MIN * win_s / 60.0` dan pakai `win_s` yang sama dengan `seg_metrics`.

---

## 4. DETERMINISME

### 4.1 Lapis rule: deterministik penuh

`rule_display` dijalankan dua kali pada dataset yang sama untuk lima kelas. Hash SHA-256 array prediksi dan array `nodata` identik di kelima kelas (vib, ssi, shk, stuck_k1, hyd_ki). Ini **VERIFIKASI POSITIF**.

### 4.2 Lapis RF: tidak bit-identik, selisih pada skala epsilon mesin

Uji: `RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)` dilatih dua kali pada data dan hyperparameter identik, lalu `predict_proba` dibandingkan.

| Besaran | Nilai |
|---|---|
| fold uji | well F-14, latih 21.933 baris, uji 1.989 baris, 55 fitur |
| hash skor run 1 | `04515f105be41673` |
| hash skor run 2 | `4bf4487e1749a400` |
| bit identik | **False** |
| selisih absolut maksimum | 2,22e-16 |

Selisih 2,22e-16 adalah epsilon mesin (2⁻⁵² ≈ 2,22e-16), tanda penjumlahan paralel `n_jobs=-1` yang urutannya tidak dijamin. Dampak praktis nol setelah pembulatan 4 desimal, dan itu sebabnya angka kampanye tidak berubah. Yang menjadi temuan bukan selisihnya, melainkan **gerbangnya**:

### 4.3 Temuan S-5 (Sedang): gerbang determinisme tidak mencakup jalur ML

`code/v9_e_RULE_05_determinism.py` hanya menjalankan ulang empat skrip RULE (`v9_e_RULE_01` sampai `04`). Jalur RF (`v9_e_ML_01_train.py`) dan jalur driver (`v9_i1_run.py`) tidak ikut diuji. Akibatnya `n_jobs=-1` pada `code/v9_i1_pipeline.py` dan `v9_e_ML_01_train.py` tidak pernah terkena pemeriksaan, padahal justru di situ satu-satunya ketidakidentikan bit ditemukan.

Usulan: tambahkan dua entri ke daftar skrip gerbang, dan bandingkan skor setelah pembulatan 6 desimal (bukan bit) supaya epsilon tidak memicu alarm palsu. Seed 42 sudah dipakai konsisten di kedua jalur, jadi sisanya hanya cakupan tes.

### 4.4 Temuan M-5 (Minor): empat fitur kosong total di dataset vib

`SimpleImputer` mengeluarkan peringatan bahwa `SPM_mean`, `SPM_std`, `SPM_slope`, `SPM_last` tidak memiliki satu nilai pun pada segmen vib yang diuji. Jadi 55 kolom fitur efektif menjadi 51. Tidak ada filter yang membuang kolom kosong, dan tidak ada laporan `n_fitur_efektif` di hasil. Ini tidak mengubah angka (imputer mengabaikannya), tetapi menyembunyikan bahwa dataset punya fitur mati.

Usulan: laporkan `n_fitur_efektif` per fold, atau buang kolom dengan `n_notnull == 0` sebelum melatih.

---

## 5. PENYEBUT FAR DAN SATUAN

### 5.1 Rumus yang dipakai

`code/v9_i1_pipeline.py:307-332`: `neg_h = n_neg * win_s / 3600`, lalu `far = fp / neg_h * 24`. Untuk semua detektor rig, `win_s = 60`. Jadi FAR = `fp × 24 × 60 / n_neg`, yaitu **FP per 24 jam dari menit negatif yang dapat dievaluasi**.

`code/v9_e_RULE_01_status.py:93` memakai bentuk yang sama dengan `jam_neg`. Cocok dengan `code/v9_i1_pipeline.py:36-38` yang menyebut "konvensi kampanye FP/(n_neg/60)*24 (per 24 jam, skala jendela 60 dtk)".

### 5.2 Temuan K-4 (Kritis): menit negatif yang dievaluasi hanya sebagian kecil dari waktu kalender

Uji: bandingkan jumlah baris per well dengan rentang `ts_bin` per well (`max - min + 1`).

| Mode | cakupan terendah | cakupan tertinggi | menit negatif dipakai penyebut | jam negatif |
|---|---|---|---|---|
| vib | 0,1179 (F-15_S, 10.903 baris / 92.501 menit) | 0,659 (F-14, 1.989 / 3.018) | 18.493 | 308,2 |
| ssi | **0,0146** (F-5, 4.714 / 322.772) | 0,717 (F-9_A, 841 / 1.173) | 35.299 | 588,3 |
| shk | 0,0193 (F-5, 7.140 / 369.665) | 0,677 (F-10, 7.899 / 11.668) | 54.490 | 908,2 |
| stuck K-i | 0,3201 (F-9_A, 2.354 / 7.354) | 0,605 (F-14, 3.201 / 5.289) | 3.548 | 59,1 |
| hyd K-i | 0,0171 (F-5, 6.332 / 369.549) | 0,673 (F-10, 7.571 / 11.249) | 45.337 | 755,6 |

Konsekuensinya: "FAR ≤ 6 per 24 jam" pada ssi F-5 berarti 6 alarm per 24 jam **dari menit yang teramati**, dan menit yang teramati itu 1,46% dari rentang kalender. Untuk mencapai 24 jam teramati dibutuhkan sekitar 1.644 jam kalender (68 hari) pada well itu. Gate "well FAR ≤ 6" di tabel tier karena itu tidak sebanding antar well: F-9_A (cakupan 0,717) dan F-5 (0,0146) dinilai dengan besaran yang berbeda 49 kali.

Ini bukan bug aritmetika; rumusnya konsisten. Yang bermasalah adalah **pembacaannya sebagai laju kalender** dan pemakaiannya sebagai gate lintas well.

Usulan: tambahkan kolom `cakupan` di setiap tabel FAR, dan laporkan dua besaran: `FAR per 24 jam negatif-teramati` (yang sekarang) dan `FAR per 24 jam kalender` (= nilai sekarang × cakupan). Gate lintas well hanya boleh memakai bentuk kedua, atau gate harus mensyaratkan cakupan minimum (misal 0,25) sebelum dipakai.

### 5.3 Temuan S-3 (Sedang): ambang kuantil tidak mencapai target FAR, melebihi 2 kali

`code/v9_i1_pipeline.py:631-636`: `thr = np.quantile(s1, 0,983333)` lalu `o1 = s1 >= thr`. Skor `s` adalah bilangan bulat 0 sampai 27 (jumlah fitur dengan |z| > 3, `:625`). Pada distribusi diskret, kuantil 98,33% sering jatuh di antara dua nilai bulat, dan pembandingan `>=` mengambil seluruh massa nilai di atasnya.

Hasil terukur pada titik operasi:

| Besaran | Target kode | Terukur |
|---|---|---|
| FP per menit negatif (seluruh segmen) | 1,0 | **2,096** |
| FP per alat di R01 | 0-1 | 1 sampai 3 (dari 35 sampai 42 jendela) |
| laju alarm per menit | 1,0 | 1,43 sampai 5,14 |
| ambang `thr` per alat | kuantil 0,9833 | 12,32 / 10,0 / 8,63 / 10,0 |

Jadi target FAR yang tertulis di resep tidak tercapai oleh resepnya sendiri, dan penyimpangannya bukan kecil (2,1 kali pada agregat, 5 kali pada alat terburuk).

Usulan: pakai ambang pada skor yang dibuat kontinu (misal rata-rata |z| atau jumlah berbobot) supaya kuantil punya resolusi, atau kalibrasi dengan mencari nilai bulat terkecil yang membuat FP R01 ≤ target (pencarian satu dimensi atas 28 kandidat, murah dan eksak).

### 5.4 Temuan S-6 (Sedang): FAR `bit_wear` berlabel "per 24 jam" padahal barisnya grid kedalaman

`code/v9_i1_pipeline.py:578` mengurutkan USROP per `Measured Depth m`, dan `:580` membentuk persistence pada grid kedalaman itu. `seg_metrics` dipanggil dengan `win_s = 60` bawaan, sehingga baris diperlakukan sebagai jendela 60 detik. Padahal jarak antar baris adalah 0,015 m (median langkah kedalaman pada 198.928 baris), bukan waktu.

Angka yang dilaporkan: `far_segmen = 1,213` dengan `far_unit = "FP/menit-negatif (jendela 60 dtk)"`. Angka itu sebenarnya FP per 24 × 60 = 1.440 sampel kedalaman negatif. Tidak ada jam di dalamnya.

Usulan: set `win_s` eksplisit untuk bit_wear dan ganti satuannya menjadi `FP per 1.000 sampel kedalaman`, atau jangan laporkan FAR untuk bit_wear sama sekali (head-nya TREN, FAR bukan gate-nya).

### 5.5 Temuan M-7 (Minor): satuan jendela tool_wear perlu ditulis di dokumen

`start_sample` pada `scratch/v6_e1/toolwear_windows.csv` berlangkah tepat 1.000 sampel untuk seluruh 8 run (`langkah_unik = [1000]`), dan `code/v6_e1_50_toolwear.py` memakai `FS = 1000` Hz dengan `WIN = 1000` sampel. Jadi satu jendela = satu detik, dan `TLead` dalam detik benar. Kesimpulan: satuan 60 detik versus 1 detik yang disebut kartu **bukan** kontradiksi, melainkan dua domain berbeda (rig memakai jendela 60 detik, bengkel memakai 1 detik). Ini diverifikasi, bukan diasumsikan.

Yang perlu ditambahkan hanya satu baris di dokumen: `win_s` per domain, supaya pembaca tidak membandingkan FAR rig dengan FAR bengkel.

### 5.6 Temuan S-8 (Sedang): grid kedalaman `bit_wear` mencampur tujuh sumur

`code/v9_i1_pipeline.py:578` mengurutkan seluruh USROP hanya dengan `sort_values("Measured Depth m")`, tanpa `well`. Tujuh sumur punya rentang kedalaman yang bertumpuk (225,171 m sampai 4.090,001 m), sehingga urutan itu mencampur sumur: 133.539 dari 198.927 pasangan baris berurutan (**67,13%**) menyeberang well.

Akibat terukur pada kuantitas yang sama (label `high_MSE_bit_wear`, 198.928 baris, 49.732 positif):

| Urutan baris | P(label 1 | baris sebelumnya 1) | Catatan |
|---|---|---|
| berkas mentah (berkelompok per well) | 0,9903 | dipakai dokumen sebagai "global" |
| `well` lalu `Measured Depth m` | 0,9903 | urutan yang benar secara fisik |
| `Measured Depth m` saja (fungsi pipeline) | **0,5668** | 67,13% pasangan lintas well |
| segmen F-14 saja (yang dilaporkan kampanye) | 0,9927 | satu well, tidak tercampur |

Kampanye V9 tidak terkena angka 0,5668 hanya karena `code/v9_i1_run.py:112-119` memotong satu segmen well sebelum memanggil `run_bit_wear`. Fungsi itu sendiri tidak aman untuk dataset penuh: siapa pun yang memanggil `run_bit_wear(pd.read_csv(USROP))` akan mendapat "persistence" yang sebagian besar membandingkan dua lubang sumur berbeda, tanpa error dan tanpa peringatan.

Usulan: urutkan `["well", "Measured Depth m"]` di `:578`, atau tolak input dengan lebih dari satu well (`assert df["well"].nunique() == 1`). Tambahkan uji regresi: presisi persistence pada dataset penuh harus 0,9903, bukan 0,5668.

---

## 6. DAFTAR TEMUAN BERURUT BAHAYA

### Kritis (5)

| # | Temuan | Bukti | Usulan |
|---|---|---|---|
| K-1 | rule vib/shk/stuck tidak pernah menyala pada status belum aktif; P 0,92/0,61/0,96 adalah presisi kondisional, bukan kemampuan deteksi | `e0_audit_results.json` `rule.*.rule_pos_rate_pada_onset_baru = 0,0`; `code/v9_e_RULE_01_status.py:162-227`; `EVAL_C:90` | pecah P/R per rezim di EVAL_C; ubah bunyi klaim |
| K-2 | `persistence_event` mengkreditkan lead ke onset yang salah; 0 dari 15 alarm dipicu oleh event yang dikreditkan | `e0_audit_results2.json`; `code/v9_e_RULE_02_stuck_onset.py:41-95` | hitung lead hanya bila pemicu = event; tarik klaim TLead 7,0 mnt |
| K-3 | `tool_wear` L1 memakai kriteria "pernah menyala sekali"; peluang kebetulan 4/4 = 0,5678, recall segmen 0,0542 | `e0_audit_results4.json`; `code/v9_i1_pipeline.py:631-660`; `EVAL_C:98,104` | ganti ke recall jendela; turunkan tier sampai recall naik |
| K-4 | penyebut FAR adalah menit teramati, bukan kalender; cakupan 1,46% sampai 71,7% | `e0_audit_results.json` `cakupan_waktu_per_well`; `code/v9_i1_pipeline.py:321-324` | laporkan FAR kalender dan cakupan; gate butuh cakupan minimum |
| K-5 | `obs_hyd`/`anom_hyd` (dihitung di jendela label) dikirim di dataset tanpa penanda terlarang | `code/v9_d1_03_rig_datasets.py:119-120`; `code/v9_i1_pipeline.py:64,302` | ganti nama berprefiks `y`, atau pisahkan file label |

### Sedang (8)

| # | Temuan | Bukti | Usulan |
|---|---|---|---|
| S-1 | ssi `rule_display` SUPERV/L1 dengan P 0,2121 dan n_aktif 0, padahal dokumen hanya memberi L1 ke hybrid | `code/v9_i1_pipeline.py:143`; `EVAL_C:91,128` | turunkan ke TREN/L0 atau hapus |
| S-2 | hyd `persistence` SUPERV/L0 bertabrakan dengan definisi L0 dan dengan perlakuan vib/shk | `code/v9_i1_pipeline.py:223,289-291` | samakan perlakuan, pilih satu sumber |
| S-3 | ambang kuantil diskret melampaui target FAR 2,1 kali (5,1 kali pada alat terburuk) | `code/v9_i1_pipeline.py:631-636`; `far_segmen 2,096` | kalibrasi pencarian nilai bulat, bukan kuantil |
| S-4 | presisi hyd rule jatuh 0,8416 ke 0,3573 pada onset baru; tier tidak membedakan | `e0_audit_results.json` `rule.hyd_ki` | laporkan dua rezim di badge |
| S-5 | gerbang determinisme hanya 4 skrip RULE; jalur RF tidak diuji; RF tidak bit-identik (2,2e-16) | `code/v9_e_RULE_05_determinism.py`; `e0_audit_results.json` `determinisme_rf` | tambah skrip ML, bandingkan setelah pembulatan 6 desimal |
| S-6 | bit_wear melaporkan FAR "per 24 jam" pada grid kedalaman 0,015 m | `code/v9_i1_pipeline.py:578-580`; `far_unit` | ganti satuan ke sampel kedalaman, atau jangan laporkan FAR |
| S-7 | `bit_wear` persistence = label digeser; P 0,9927 adalah autokorelasi label (0,9903 pada urutan per well, 0,5668 pada urutan pipeline) | `code/v9_i1_pipeline.py:580`; `e0_audit_results.json`; `e0v_recheck.json` | ganti label metrik + tampilkan baseline prevalensi 0,25 |
| S-8 | `run_bit_wear` mengurutkan hanya `Measured Depth m`, 67,13% pasangan baris berurutan menyeberang well; P persistence jatuh 0,9903 ke 0,5668 | `code/v9_i1_pipeline.py:578`; `e0v_recheck.json` | urutkan `["well","Measured Depth m"]` atau tolak input multi-well |

### Minor (7)

| # | Temuan | Bukti | Usulan |
|---|---|---|---|
| M-1 | identitas rule-jendela gagal 23/52.509 (0,04%) untuk hyd | `code/v9_e_RULE_01_status.py:229` | satukan definisi mask |
| M-2 | `TLead` tool_wear = jarak ke akhir run, bukan ke kerusakan | `code/v9_i1_pipeline.py:653-660` | tulis definisi, atau ubah acuan ke awal R02 |
| M-3 | hulu tool_wear menulis ke folder arsip; 65 skrip legacy menyebut arsip, 0 dari `v9_*` | `code/v6_e1_50_toolwear.py` | pindahkan jalur, atau tandai tidak dapat dijalankan ulang |
| M-4 | `q` kuantil konstanta 0,983333, tidak diturunkan dari `win_s` | `code/v9_i1_pipeline.py:631` | pakai `win_s` eksplisit |
| M-5 | 4 fitur SPM kosong total (55 menjadi 51 efektif) tanpa laporan | peringatan `SimpleImputer`; `e0_audit_results.json` | laporkan `n_fitur_efektif` |
| M-6 | gerbang kebocoran hanya memeriksa stempel, bukan isi fitur | `code/v9_d1_04_stuck_k2.py:209` | tambah uji isi 20 baris acak |
| M-7 | `win_s` per domain belum ditulis di dokumen | diverifikasi: 1.000 sampel/jendela, `FS = 1000` | tambah satu baris di EVAL_C |

Ringkasan hitungan: 5 Kritis, 8 Sedang, 7 Minor; 8 verifikasi positif (nol kebocoran stempel, nol kanal label di fitur hyd, rule deterministik, 27 head konsisten, tier terlarang nol, 8 angka dokumen cocok kode, assert anti-sirkularitas ada di jalur ML, satuan tool_wear terverifikasi). Satu koreksi pada dokumen ini sendiri dicatat di §10: fraksi onset baru vib adalah 25,53%, bukan 74,47%.

---

## 7. RUJUKAN ILMIAH

Semua DOI di bawah diperiksa pada 2026-10-27 lewat `api.crossref.org` (metadata judul/tahun/wadah) dan `doi.org` (resolusi). Perintah: `e0_doi.py`, keluaran `e0_doi.json`.

1. Kaufman, S., Rosset, S., Perlich, C., Stitelman, O. (2012). *Leakage in data mining: Formulation, detection, and avoidance*. ACM Transactions on Knowledge Discovery from Data 6(4). DOI: 10.1145/2382577.2382579. Crossref HTTP 200, judul dan tahun cocok; halaman penerbit menolak bot (HTTP 403), jadi verifikasi berhenti di metadata Crossref. **TERVERIFIKASI (metadata)**, dipakai sebagai dasar taksonomi kebocoran di §1.
2. Kapoor, S., Narayanan, A. (2023). *Leakage and the reproducibility crisis in machine-learning-based science*. Patterns 4(9):100804. DOI: 10.1016/j.patter.2023.100804. Crossref HTTP 200 dan `doi.org` HTTP 200. **TERVERIFIKASI**, dipakai untuk argumen bahwa kolom turunan label (§1.3) adalah kebocoran yang paling sering lolos.
3. Saito, T., Rehmsmeier, M. (2015). *The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets*. PLOS ONE 10(3):e0118432. DOI: 10.1371/journal.pone.0118432. Crossref HTTP 200 dan `doi.org` HTTP 200. **TERVERIFIKASI**, dipakai untuk memilih presisi/recall per subpopulasi di §2 alih-alih satu angka agregat.
4. Davis, J., Goadrich, M. (2006). *The relationship between Precision-Recall and ROC curves*. ICML '06. DOI: 10.1145/1143844.1143874. Crossref HTTP 200, judul dan tahun cocok; `doi.org` HTTP 403 (penerbit menolak bot). **TERVERIFIKASI (metadata)**, dipakai untuk menjelaskan mengapa AUPRC 0,054 tidak boleh dibaca sebagai "hampir bekerja".

Dua DOI diuji dan **ditolak** karena tidak dapat dipakai: `10.1109/TII.2019.2950661` (Crossref 404, tidak ada), `10.1016/j.ress.2020.106889` (terverifikasi tetapi topiknya model keandalan satelit, bukan evaluasi PdM, jadi tidak relevan sebagai dasar rekomendasi). Keduanya tidak dipakai di dokumen ini.

Catatan kejujuran: tidak ada rujukan yang dipakai untuk mengklaim ambang operasional mana pun. Ambang FAR 6/24 jam dan 1 alarm/menit tetap KONVENSI internal seperti yang sudah dicatat di `RND_PROVENANCE_LEDGER.md` baris `L-*`, bukan hasil standar.

---

## 8. CARA REPRODUKSI

```
cd "/mnt/d/Capstone 1(v2)"
mkdir -p scratch/e0_audit
cp ~/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b/e0_audit*.py scratch/e0_audit/
PY=/home/neonti/.venvs/rnd_r3/bin/python
$PY scratch/e0_audit/e0_audit.py      # ~40 detik
$PY scratch/e0_audit/e0_audit2.py     # ~15 detik
$PY scratch/e0_audit/e0_audit3.py     # ~10 detik
$PY scratch/e0_audit/e0_audit4.py     # ~5 detik
$PY scratch/e0_audit/e0_doi.py        # ~20 detik, butuh internet
```

Skrip hanya membaca. Tidak ada penulisan ke `code/`, `scratch/v9_*`, atau `/mnt/d/Capstone 1`.

---

## 9. RINGKASAN DAN YANG BELUM TERVERIFIKASI

**Ringkasan lima baris**

1. Tidak ada kebocoran masa depan pada tingkat stempel waktu: 0 dari 292.954 baris di 6 dataset punya `feat_ts_max >= lab_ts`, dan batas atasnya tepat `-1` menit.
2. Sirkularitas rule terbukti dan dampaknya terukur: rule vib/shk/stuck **tidak pernah** menyala pada status belum aktif (laju 0,0000), jadi P 0,92/0,61/0,96 adalah pernyataan persistensi, bukan deteksi kejadian.
3. `persistence_event` stuck K-ii memberi kredit lead ke onset yang salah: 26 baris alarm, 11 FP (cocok dengan dokumen), dan 0 dari 15 alarm dipicu oleh event yang dikreditkan, sehingga TLead median 7,0 menit tidak sahih.
4. `tool_wear` L1 berdiri di atas kriteria "pernah menyala sekali" dengan peluang kebetulan 0,5678 untuk 4/4 alat, sementara recall segmen pada titik operasi itu hanya 0,0542 dan FAR 2,096/menit (target 1,0).
5. Penyebut FAR adalah menit teramati, bukan kalender: cakupan 1,46% (ssi F-5) sampai 71,7% (ssi F-9_A), sehingga gate "FAR ≤ 6/24 jam" tidak sebanding antar well sampai cakupan ikut dilaporkan.

**Belum terverifikasi (jangan dipakai sebagai dasar keputusan)**

1. Isi fitur belum diuji langsung terhadap data mentah. Audit ini memeriksa stempel `feat_ts_max` dan daftar nama kolom, bukan menghitung ulang nilai `*_mean` dari kanal mentah per baris (M-6). Kebocoran lewat isi, bila ada, tidak akan tertangkap.
2. Kesetiaan bins terhadap run asli 2026-10-12 belum diuji. Semua angka berasal dari dataset tersimpan; kalau bins berubah setelah itu, angka lama dan angka audit tidak sebanding.
3. `hyd` K-ii (survival/horizon) tidak diaudit secara mendalam. Head itu `BELUM LAYAK PAKAI` dan `n_aktif` kosong, jadi tidak ada perilaku untuk diukur.
4. Jalur ML lengkap (`v9_e_ML_01_train.py`, 28 fold, 3 model) tidak dijalankan ulang. Yang diuji hanya determinisme satu fold vib dan penolakan kanal label lewat assert.
5. `bit_wear` punya tiga angka presisi persistence yang berbeda menurut urutan baris: 0,9903 (berkas mentah dan `well`+`kedalaman`), 0,5668 (sort kedalaman saja, yaitu fungsi pipeline), 0,9927 (segmen F-14). Yang dipakai sebagai angka resmi tetap 0,9927 karena kampanye hanya menjalankan segmen F-14; angka 0,5668 dilaporkan sebagai sifat fungsi `run_bit_wear` (S-8), bukan sebagai angka kinerja.
6. Peluang kebetulan `tool_wear` 0,5678 adalah model Poisson atas laju alarm terukur, bukan simulasi langsung. Simulasi permutasi 10.000 kali akan memberi angka yang lebih kuat dan belum dijalankan.
7. Empat fitur SPM kosong total ditemukan pada segmen vib yang diuji; apakah kosong di seluruh dataset belum diperiksa.

---

## 10. VERIFIKASI ULANG INDEPENDEN (run 34, 2026-10-27)

Bagian ini ditulis oleh eksekusi ulang, bukan oleh penulis bagian 1 sampai 9. Tujuannya memastikan dokumen ini tidak berisi angka warisan yang tidak dapat direproduksi.

### 10.1 Eksekusi ulang penuh `e0_audit.py`

Perintah: `/home/neonti/.venvs/rnd_r3/bin/python e0_audit.py` (keluaran mentah `e0_rerun_stdout.txt`, exit 0). Hasil lama disalin lebih dulu ke `e0_audit_results_baseline04.json`, hasil baru dibandingkan field demi field dengan `e0v_compare.py`, ringkasan di `e0v_rerun_compare.json`.

| Besaran | Hasil |
|---|---|
| field JSON dibandingkan | 468 |
| field identik | **466** |
| field berbeda | 2, keduanya `determinisme_rf.hash1` dan `hash2` |
| `max_abs_diff` RF lama dan baru | sama persis `2.220446049250313e-16` |
| hash rule vib / ssi / shk / stuck_k1 / hyd_ki | identik dengan run sebelumnya (`8ac69651728df3db`, `71ff04a8e92b27c1`, `3f1025e236f6c655`, `35ef2718c148c5f0`, `4857a79b8e7abd0d`) |
| pelanggaran `feat_ts_max >= lab_ts` | 0 di keenam dataset |

Artinya: seluruh angka yang dilaporkan di bagian 1 sampai 5 stabil terhadap eksekusi ulang. Satu-satunya yang tidak bit-identik adalah skor RF, dan itu sudah dilaporkan sebagai S-5 dengan besaran epsilon mesin yang sama. Hash RF berubah antar run (bukan hanya antar dua fit dalam satu run), sehingga klaim "tidak bit-identik" bukan artefak satu proses.

### 10.2 Pengukuran baru: sensitivitas urutan dan komposisi onset

Dua skrip baru, keduanya hanya membaca:

| Skrip | Yang diukur | Keluaran |
|---|---|---|
| `e0v_recheck.py` | presisi persistence `bit_wear` pada tiga urutan baris, jumlah pasangan lintas well, presisi pada segmen F-14 | `e0v_recheck.json` |
| `e0v_onset.py` | fraksi onset baru per mode memakai kolom `y_prev_*` resep D1 | `e0v_onset.json` |

Hasilnya mengubah dua hal di dokumen ini:

1. **Koreksi angka (bagian 2.2).** Kalimat lama menyebut 74,47% positif vib adalah onset baru. Angka 0,7447 sebenarnya `P(y_prev=1 | y=1)`, yaitu fraksi positif yang **sudah berlangsung**. Fraksi onset baru terukur 0,2553 (1.386 dari 5.429). Sudah dikoreksi, dan angka detektor lain ditambahkan karena justru memperkuat K-1: shk 76,36% dan ssi 86,00% positifnya adalah onset baru, sementara rule shk menyala nol kali di sana.
2. **Temuan baru S-8 (bagian 5.6).** `run_bit_wear` mengurutkan hanya `Measured Depth m`; pada urutan itu 67,13% pasangan baris berurutan menyeberang well dan presisi persistence jatuh dari 0,9903 ke 0,5668.

### 10.3 Verifikasi DOI dua lapis (ulang 2026-10-27)

Lapis registrasi memakai HEAD ke `https://doi.org/<doi>` tanpa mengikuti redirect; lapis metadata memakai `https://api.crossref.org/works/<doi>`.

| DOI | Lapis registrasi | Lapis metadata | Status |
|---|---|---|---|
| 10.1145/2382577.2382579 | 302 | 200 | terdaftar + metadata cocok; akses penerbit 403 (blokir bot ACM) |
| 10.1016/j.patter.2023.100804 | 302 | 200 | terdaftar + metadata cocok + halaman terbuka |
| 10.1371/journal.pone.0118432 | 302 | 200 | terdaftar + metadata cocok + halaman terbuka |
| 10.1145/1143844.1143874 | 302 | 200 | terdaftar + metadata cocok; akses penerbit 403 (blokir bot ACM) |

Koreksi penulisan: "doi.org HTTP 403" pada dua DOI ACM adalah lapis akses penerbit, bukan kegagalan registrasi. Pada lapis registrasi keempat DOI menjawab 302, jadi keempatnya terdaftar. Keduanya tetap dipakai hanya pada tingkat metadata.

### 10.4 Pemeriksaan ledger dan koreksi yang dilakukan

| Objek | Temuan | Tindakan |
|---|---|---|
| baris ledger `E0-028` | menulis "stuck 5" sehingga total per mode menjadi 26, padahal `REGISTRY` menghasilkan stuck 6 dan total 27 | dikoreksi menjadi "stuck 6" |
| label temuan `S-1` sampai `S-7` | penomoran di badan dokumen (urutan kronologis) tidak sama dengan tabel ringkasan (urutan bahaya) | disamakan dengan tabel |
| baris ledger baru | angka verifikasi ulang belum punya baris | ditambah `E0-032` sampai `E0-036` |
| reproduksi `e0_audit.py` | skrip menulis JSON ke folder workspace (`OUTDIR` di baris 23), bukan ke `scratch/e0_audit/`, sehingga langkah salin di §8 perlu dibaca dua arah | dicatat di sini, tidak diubah karena mengubah kode audit di luar lingkup |

### 10.5 Yang tetap belum terverifikasi setelah run ini

1. Isi fitur belum diuji langsung terhadap data mentah (M-6). Semua verifikasi kebocoran masih pada tingkat stempel dan nama kolom.
2. Jalur ML lengkap belum dijalankan ulang. Yang diuji determinisme satu fold vib.
3. Peluang kebetulan `tool_wear` masih model Poisson, belum simulasi permutasi.
4. `hyd` K-ii tetap tanpa perilaku untuk diukur.
5. Kesetiaan bins terhadap kampanye 2026-10-12 belum diuji; angka audit dan angka kampanye hanya sebanding bila bins tidak berubah.
