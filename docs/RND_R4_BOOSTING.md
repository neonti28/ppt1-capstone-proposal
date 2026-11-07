# RND-R4: BOOSTING MODERN + KALIBRASI (LightGBM / XGBoost / CatBoost / isotonic / conformal)

Kartu: `t_246de62e` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Folder arsip `/mnt/d/Capstone 1` tidak disentuh.
Ruang lingkup: 7 mode (vib, ssi, shk, stuck, hyd, bit_wear, tool_wear), 11 klaim (K-i/K-ii), 27 head.

## Riset pendahuluan

Riset pendahuluan: literature-review, paper-lookup, scikit-learn, statsmodels, scientific-critical-thinking, verification-mandatory

- **literature-review** : dipakai untuk menyusun pencarian bertahap per sumbu (boosting, kalibrasi, conformal, imbalance) dan untuk aturan bahwa setiap sitasi diverifikasi ke sumbernya, bukan dikutip dari ingatan.
- **paper-lookup** : dipakai untuk lookup identifier ke Crossref (`api.crossref.org/works/<DOI>`) dan pengecekan HTTP landing DOI/arXiv, supaya status "TERVERIFIKASI" punya jejak endpoint, bukan klaim.
- **scikit-learn** : dipakai untuk memilih estimator dan protokol yang benar: RF kontrak V9 (`n_estimators=300`, `min_samples_leaf=5`, `class_weight="balanced_subsample"`, `random_state=42`), `SimpleImputer(strategy="median")` yang di-fit hanya pada set latih (fold-safe), dan `average_precision_score` untuk AUPRC.
- **statsmodels** : dipakai sebagai rujukan metode inferensi: regresi logistik 1D sebagai dasar Platt scaling, dan perbandingan model berbasis uji (DeLong untuk AUC berkorelasi, bukan uji beda rata-rata).
- **scientific-critical-thinking** : dipakai untuk memisahkan empat klaim yang sering dicampur: ranking (AUPRC), probabilitas (Brier/ECE), keputusan (FAR empiris), dan titik operasi (bobot kelas); serta untuk menolak klaim "algoritma X lebih baik" tanpa baseline dan uji statistik.
- **verification-mandatory** : dipakai untuk menandai setiap angka dengan kelas sumber (STANDAR/JURNAL/RUN-KITA/KONVENSI) dan menulis "BELUM TERUKUR" ketika pengukuran gagal, bukan menggantinya dengan angka literatur.

Riset pendahuluan: sequentialthinking, **5 pikiran** (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1..5, `thoughtHistoryLength` 5). Ringkas: (1) memisahkan empat sumbu (ranking, probabilitas, keputusan, titik operasi) supaya tidak diuji dengan satu metrik; (2) biaya latih wajib diukur pada data kita karena skala data kita 3 orde lebih kecil dari benchmark literatur; (3) syarat jumlah sampel kalibrasi adalah pertanyaan utama, bukan pilihan metode; (4) jaminan conformal bergantung pada exchangeability yang justru dilanggar lintas-well, jadi harus diuji tiga varian ambang; (5) imbalance menggeser titik operasi, bukan menaikkan kualitas ranking, sehingga efeknya dilaporkan pada presisi dan FAR.

---

## 1. Jawaban ringkas (5 baris)

1. Pada data kita, keluarga boosting **belum boleh diklaim lebih baik** dari RF kontrak V9: satu-satunya angka yang terukur hari ini adalah RF (AUPRC 0,9117 pada fold F-14, lihat §4), sedangkan biaya dan AUPRC LightGBM/XGBoost/CatBoost pada data kita berstatus **BELUM TERUKUR** karena run pembanding tidak selesai dalam anggaran waktu kartu.
2. Kalibrasi (isotonic/Platt) **tidak menaikkan AUPRC**; ia hanya mengubah skor jadi probabilitas yang bisa dibaca operator. Yang harus diuji adalah Brier/ECE dan **portabilitas kalibrasi antar well**, bukan akurasi ranking.
3. Conformal memberi jaminan frekuensi salah yang bergantung pada asumsi **exchangeability** antara himpunan kalibrasi dan data uji. Ambang kuantil yang dipakai sekarang (`np.quantile` pada well uji sendiri) justru **melanggar** sifat itu karena memakai label well uji (hindsight), sehingga angkanya bukan jaminan melainkan deskripsi setelah kejadian.
4. Untuk imbalance, `class_weight`/`scale_pos_weight`/focal loss adalah **pemindah titik operasi**. Klaim manfaatnya harus diukur pada presisi dan FAR di titik operasi yang sama, bukan pada akurasi.
5. Rekomendasi: jalankan satu pilot pembanding 4 keluarga model + 3 varian ambang (kuantil-hindsight, conformal lintas-well, conformal dalam-well) pada **vib dan shk** dengan LOWO, metrik FAR/B1/TLead/AUPRC, dan uji DeLong/bootstrap sebelum ada satu pun perubahan tier.

---

## 2. Kerangka: empat sumbu yang tidak boleh dicampur

Kesalahan paling mahal di topik ini adalah memakai satu metrik untuk empat pekerjaan berbeda. Pemisahan yang dipakai dokumen ini:

| Sumbu | Pertanyaan | Objek yang diubah | Metrik sah | Metrik yang menyesatkan |
|---|---|---|---|---|
| Ranking | urutan mana yang lebih baik? | fungsi skor | AUPRC, ΔB vs prevalensi/canary | akurasi, F1 pada ambang 0,5 |
| Probabilitas | berapa keyakinan sebenarnya? | skor jadi p | Brier, ECE, kurva reliabilitas | AUPRC (tidak berubah oleh kalibrasi monoton) |
| Keputusan | seberapa sering salah kalau alarm dipasang? | p jadi alarm/true | FAR empiris vs target, B1, TLead | AUC |
| Titik operasi | di mana kita memotong? | ambang tau | presisi, recall, FP per shift | AUPRC (tidak sensitif pada bobot kelas) |

Konsekuensi langsung untuk kartu ini: boosting diuji di sumbu ranking dan biaya, kalibrasi di sumbu probabilitas, conformal di sumbu keputusan, imbalance di sumbu titik operasi. Tidak ada satu tabel "model mana yang menang" yang bisa menjawab keempatnya.

---

## 3. LightGBM vs XGBoost vs CatBoost vs RF

### 3.1 Kapan masing-masing secara teori menang atau kalah

| Keluarga | Kekuatan struktural | Kapan kalah | Parameter kunci | Catatan untuk kasus kita |
|---|---|---|---|---|
| **Random Forest (RF kontrak V9)** | tahan noise label, tidak butuh tuning, `class_weight="balanced_subsample"` menangani imbalance tanpa menggeser struktur pohon, deterministik dengan seed | boros memori pada data lebar, tidak mengeksploitasi interaksi aditif secara efisien, probabilitas mentahnya kasar (banyak nilai diskret) | `n_estimators`, `min_samples_leaf`, `max_features`, `class_weight` | sudah dipakai di 4 kelas (vib 4 fold, ssi 9, shk 9, stuck_k2 4, total 28 fold per `docs/V9_EVAL_C_LAYERC.md` baris 76) |
| **LightGBM** | histogram + leaf-wise growth, sangat cepat pada data besar, `num_leaves` mengontrol kompleksitas langsung | overfit pada data kecil (leaf-wise mudah membuat daun dalam), sensitif `min_child_samples`, tidak stabil pada fitur dengan missing tinggi | `num_leaves`, `min_child_samples`, `learning_rate`, `feature_fraction`, `bagging_fraction` | menarik untuk stuck_k2 (118.567 baris) dan shk (56.495) karena volume; berisiko untuk vib (23.922) dan stuck_k1 (5.555) |
| **XGBoost** | regularisasi eksplisit (`lambda`, `alpha`), `scale_pos_weight` baku, `tree_method="hist"` cepat | lebih banyak parameter yang harus dijaga, `scale_pos_weight` menyesatkan bila dipakai tanpa menyesuaikan ambang | `max_depth`, `eta`, `subsample`, `colsample_bytree`, `scale_pos_weight`, `min_child_weight` | `scale_pos_weight` relevan untuk stuck_k2 (prevalensi 0,0167) |
| **CatBoost** | handling kategori dan ordering target otomatis, `auto_class_weights="Balanced"`, stabil tanpa tuning berat | paling mahal secara komputasi pada CPU, kontrol halus lebih sedikit | `iterations`, `depth`, `learning_rate`, `l2_leaf_reg`, `auto_class_weights` | kandidat untuk tool_wear (fitur 27, jendela 469) yang kecil dan berkategori alat |

Sumber klaim struktural: Ke et al. 2017 (LightGBM), Chen & Guestrin 2016 (XGBoost), Prokhorenkova et al. 2018 (CatBoost). Status verifikasi DOI/URL ada di §8.

### 3.2 Biaya latih pada data kita

Angka volume data (terukur, `RUN-KITA`):

| Kelas | Baris | Well | Fitur | Sumber |
|---|---|---|---|---|
| vib | 23.922 | 4 (F-14 1.989; F-5 4.548; F-15A 6.482; F-15_S 10.903) | 55 | `scratch/v9_d1/datasets/vib.csv.gz`, dihitung ulang 2026-10-27 |
| ssi | 35.906 | 9 | 55 | `ssi.csv.gz` |
| shk | 56.495 | 9 | 55 | `shk.csv.gz` |
| stuck_k1 | 5.555 | 2 | 55 | `stuck_k1.csv.gz` |
| stuck_k2 | 118.567 | 4 | 55 | `stuck_k2.csv.gz` |
| hyd_ki | 52.509 | 9 | 40 | `hyd_ki.csv.gz` |

Satu pengukuran biaya yang **berhasil** (RF kontrak V9, fold F-14, `n_jobs=-1` pada mesin 18 core):

| Model | Fold uji | n latih | n uji | AUPRC | Prevalensi | ΔB vs prevalensi | fit (detik) | predict (detik) |
|---|---|---|---|---|---|---|---|---|
| RF kontrak V9 | vib / F-14 | 21.933 | 1.989 | 0,9117 | 0,5651 | +0,3466 | 7,41 | 0,30 |

Sumber: `/home/neonti/.hermes/cache/scratch/rnd_r4/bench_vib.log` (baris JSON pertama), skrip `bench_a_models.py`, eksekusi 2026-10-27 03:56 WIB.

Angka pembanding silang: AUPRC 0,9117 berada di batas atas rentang RF vib yang sudah dilaporkan `docs/V9_EVAL_C_LAYERC.md` §2.1 (0,441 sampai 0,912), jadi fold ini konsisten dengan hasil kampanye sebelumnya, bukan angka baru yang menyimpang.

**Yang gagal diukur dan harus ditulis apa adanya:**

- Run pembanding 4 keluarga model (RF, LightGBM, XGBoost, CatBoost) pada fold yang sama **tidak selesai** dalam anggaran waktu. Gejala terukur: proses dengan `n_jobs=-1` pada 18 core berjalan lebih dari 420 detik pada 21.933 x 55 baris setelah fold RF pertama selesai, dengan utilisasi CPU sekitar 1.300 persen. Ini indikasi *thread over-subscription* pada data berukuran kecil, bukan bukti bahwa pustaka lambat secara umum.
- Karena itu **biaya latih LightGBM, XGBoost, dan CatBoost pada data kita = BELUM TERUKUR**. Angka benchmark literatur (misalnya klaim kecepatan pada dataset jutaan baris) **tidak dipakai** sebagai pengganti, karena skala data kita berbeda tiga orde dan hasilnya tidak dapat dipindahkan.

### 3.3 Rekomendasi pemilihan (berbasis struktur data, bukan selera)

| Kelas | Kandidat utama | Alasan struktural | Syarat sebelum dipakai |
|---|---|---|---|
| vib, stuck_k1 | RF sekarang dipertahankan | data kecil sampai sedang, label bising (anchor gap 4,6 persen dilaporkan di `docs/V9_EVAL_C_LAYERC.md` §2.4), boosting leaf-wise berisiko overfit | boosting hanya masuk bila AUPRC > RF pada ≥75 persen fold LOWO dengan CI bootstrap tidak memuat nol selisih |
| shk, ssi | LightGBM/XGBoost diuji sebagai pembanding | volume 56 ribu dan 36 ribu baris, banyak missing (ssi 62,3 persen baris tanpa data CRPM) | wajib dilaporkan bersama biaya latih terukur dan FAR di titik operasi tetap |
| stuck_k2 | XGBoost atau LightGBM | volume 118.567 baris, prevalensi 0,0167 (imbalance ekstrem) | `scale_pos_weight` wajib disertai kalibrasi ulang, kalau tidak probabilitas tidak bisa dibaca |
| tool_wear | CatBoost diuji, RF sebagai baseline | 469 jendela x 27 fitur, ada variabel kategori alat | hasil lintas-alat (LOTO), bukan lintas-run |

---

## 4. Kalibrasi: isotonic regression dan Platt scaling

### 4.1 Apa yang sebenarnya dilakukan

- **Platt scaling**: memasang regresi logistik satu dimensi pada skor mentah, `p = 1 / (1 + exp(A*s + B))`. Dua parameter, sangat hemat sampel, tetapi mengasumsikan bentuk sigmoid. Pada skor RF yang banyak bernilai diskret dan menumpuk di dekat 0 dan 1, asumsi ini sering tidak pas.
- **Isotonic regression**: memasang fungsi monoton naik nonparametrik (pool adjacent violators). Lebih luwes, tetapi jumlah blok yang bisa dibentuk sebanding dengan jumlah nilai skor unik, sehingga mudah overfit bila himpunan kalibrasi kecil.

Keduanya **monoton**, jadi tidak mengubah AUPRC (selain pergeseran tie kecil). Ini sebabnya kalibrasi tidak boleh dijual sebagai peningkatan akurasi.

### 4.2 Syarat jumlah sampel kalibrasi

Aturan yang dapat dipertanggungjawabkan tanpa mengarang angka literatur:

1. Himpunan kalibrasi **wajib terpisah** dari himpunan latih dan himpunan uji. Kalau tidak, hasil kalibrasi adalah in-sample fit.
2. Untuk isotonic, jumlah sampel kalibrasi harus jauh lebih besar daripada jumlah blok yang mungkin; aturan operasional yang dipakai di dokumen ini adalah **minimal 10 kali jumlah titik operasi yang ingin dibedakan**, dan **tidak boleh lebih kecil dari jumlah kejadian positif** yang ingin diresolusi di ekor atas kurva.
3. Untuk Platt, 2 parameter, sehingga pembatasnya bukan ukuran sampel melainkan apakah data kalibrasi **mewakili** distribusi uji. Syarat ke-2 ini yang lebih sering gagal di kasus kita.
4. Jumlah positif di himpunan kalibrasi adalah pembatas keras: kalibrasi probabilitas di sekitar `p = 0,9` tidak bisa dipercaya bila hanya ada belasan positif.

**Angka yang kita punya untuk syarat ini (terukur):** baris per well pada kelas vib adalah 1.989 (F-14), 4.548 (F-5), 6.482 (F-15A), 10.903 (F-15_S). Artinya skema "kalibrasi pakai satu well lain" hanya menyediakan 1.989 sampai 10.903 baris kalibrasi, dengan prevalensi yang berbeda 4 kali antar well (vib 0,14 sampai 0,57 per `docs/V9_EVAL_C_LAYERC.md` §2.1). Untuk kelas dengan prevalensi rendah, jumlah positif di himpunan kalibrasi menjadi jauh lebih kecil dari angka baris tersebut dan **belum dihitung pada dokumen ini**.

Status: **jumlah sampel kalibrasi minimum untuk data kita = BELUM TERUKUR**. Yang tersedia hanya ukuran himpunan, bukan hasil uji kelayakan.

### 4.3 Rancangan uji kalibrasi yang benar untuk kasus lintas-well

Kalau kalibrasi di-fit pada well uji, hasilnya curang (label uji dipakai). Rancangan yang sah:

```
untuk setiap fold LOWO (well uji = W):
    W_fit   = well lain (mayoritas)  -> latih model
    W_calib = satu well lain         -> fit isotonic / Platt
    W_test  = W                      -> evaluasi Brier, ECE, FAR

variasikan:
    (a) kalibrasi lintas-well (W_calib != W_test)
    (b) kalibrasi dalam-well dengan potongan waktu awal (kalibrasi prospektif, bukan hindsight)
```

Yang dibandingkan bukan hanya Brier, tetapi **selisih Brier antara (a) dan (b)**. Kalau (a) jauh lebih buruk, kesimpulannya: kalibrasi tidak portabel antar well, dan skema yang dipakai harus per-well prospektif. Ini sejalan dengan temuan EVAL_C bahwa ambang global tidak portabel (vib FAR menyebar 119 kali, 4,1 sampai 496).

---

## 5. Conformal prediction vs ambang kuantil yang sekarang

### 5.1 Apa yang dipakai sekarang

Di kode yang berjalan, ambang bukan probabilitas melainkan **kuantil skor yang dihitung dari data evaluasi itu sendiri**:

- `code/v9_i1_pipeline.py:633`: `thr = float(np.quantile(s1, q))`, dengan `q = 1.0 - TARGET_FP_PER_MIN * (len(ev1) / 60.0) / max(len(ev1), 1)` dan `TARGET_FP_PER_MIN = 1.0` (baris 615). Artinya level kuantil dipilih supaya **FP yang diharapkan** sekitar 1 per menit pada segmen kalibrasi.
- `code/v9_e_STAT_02_stuck_e2.py`: ambang q95 dilatih pada himpunan latih then diterapkan; hasilnya dilaporkan di `docs/V9_EVAL_C_LAYERC.md` §2.4 (`q95: P=R=0`, FP 177).

Dua sifat penting: (i) ambang di atas adalah **deskriptif** (kuantil empiris), bukan jaminan; (ii) pada tool_wear, kuantil dihitung dari porsi awal run yang sama, sehingga yang dijamin hanyalah perilaku di run itu, bukan run berikutnya.

### 5.2 Apa yang ditawarkan conformal

Split conformal untuk keputusan biner bekerja dengan skor nonkonformitas dan himpunan kalibrasi terpisah. Untuk pengendalian **false alarm**, analog yang dipakai adalah ambang pada kuantil ke-`ceil((n+1)(1-alpha))` dari skor negatif di himpunan kalibrasi:

```
alpha      = target FAR (mis. 0,05)
n          = jumlah sampel kalibrasi negatif
k          = ceil((n + 1) * (1 - alpha))
tau_conf   = skor negatif terurut ke-k pada himpunan kalibrasi
```

Sifat yang diklaim: bila sampel kalibrasi dan sampel uji **exchangeable**, maka FAR yang diharapkan pada data baru dibatasi sekitar `alpha`, tanpa asumsi bentuk distribusi skor. Perhatikan yang **tidak** dijamin: tidak ada jaminan untuk setiap well, tidak ada jaminan bila ada drift, dan tidak ada jaminan bila komposisi kelas berubah.

### 5.3 Perbandingan jujur untuk kasus kita

| Aspek | Ambang kuantil sekarang | Conformal (split) |
|---|---|---|
| Asal ambang | kuantil dari data evaluasi itu sendiri (sering termasuk well uji) | kuantil dari himpunan kalibrasi terpisah |
| Sifat klaim | deskriptif: "sekian FP terjadi" | jaminan marginal: "FAR diharapkan <= alpha" bila exchangeable |
| Ketergantungan asumsi | tidak ada asumsi, tetapi tidak ada jaminan | exchangeability antar kalibrasi dan uji |
| Kekuatan pada data kita | angka FAR per well bisa dilaporkan apa adanya | jaminan **gugur lintas well** karena prevalensi berbeda 4 kali (vib) dan ambang menyebar 119 kali |
| Kegagalan khas | operator membaca FAR well lain sebagai janji | operator membaca jaminan sebagai janji per well |

Kesimpulan yang dapat dipertanggungjawabkan: conformal **bukan** obat portabilitas. Ia memindahkan masalah dari "ambang tidak portabel" ke "asumsi exchangeability tidak terpenuhi". Nilainya tetap nyata pada satu pemakaian: **kalibrasi prospektif dalam-well** (potongan waktu awal untuk kalibrasi, sisanya untuk uji) yang memang sesuai dengan cara alat dipakai, dan di situ conformal memberi batas yang bisa diaudit terhadap `alpha` yang dipilih.

### 5.4 Rencana uji conformal (tiga varian, satu tabel)

Untuk setiap fold LOWO pada vib dan shk, hitung tiga ambang dan laporkan FAR empiris pada well uji:

| Varian | Himpunan kalibrasi | Himpunan uji | Yang diuji |
|---|---|---|---|
| V1 kuantil-hindsight | well uji itu sendiri | well uji itu sendiri | cara yang dipakai sekarang (batas bawah yang tidak bisa dicapai produksi) |
| V2 conformal lintas-well | satu well lain | well uji | apakah jaminan bertahan antar well |
| V3 conformal dalam-well prospektif | potongan waktu awal well uji | sisa waktu well uji | pemakaian realistis |

Metrik keluaran: FAR per 24 jam (konvensi kampanye `FP/(n_neg/60)*24`), presisi, recall, dan **selisih FAR empiris dikurangi alpha**. Kalau V2 melanggar alpha secara sistematis sementara V3 tidak, itu bukti operasional bahwa yang harus dipakai adalah V3, dan dokumen ini tidak boleh mengklaim jaminan lintas well.

Status pengukuran: **BELUM TERUKUR**. Belum ada satu pun baris V1/V2/V3 yang dieksekusi.

---

## 6. Penanganan imbalance

### 6.1 Tiga mekanisme dan apa yang sebenarnya berubah

| Mekanisme | Implementasi | Yang berubah | Yang tidak berubah |
|---|---|---|---|
| Cost-sensitive / `class_weight` | `class_weight="balanced_subsample"` (RF, kode `code/v9_i1_pipeline.py:423-426`), `auto_class_weights="Balanced"` (CatBoost) | kriteria split dan bobot daun, sehingga titik operasi bergeser | kualitas ranking umumnya hampir tetap, tetapi bisa berubah karena struktur pohon ikut berubah |
| `scale_pos_weight` | XGBoost, `sum(neg)/sum(pos)` | skala log-odds, efektif seperti menggeser ambang | urutan skor hampir tidak berubah bila model konvergen |
| Focal loss | modifikasi loss `(1-p_t)^gamma * log(p_t)` | menekan kontribusi contoh mudah, memusatkan gradien pada contoh sulit | bukan penanganan imbalance yang setara; ia menangani *hard negative*, bukan rasio kelas |

### 6.2 Dampak ke presisi dan FAR

Karena `class_weight` dan `scale_pos_weight` pada dasarnya memindahkan ambang, tabel yang harus dilaporkan adalah **presisi dan FAR pada titik operasi yang dipatok**, bukan akurasi. Kesalahan yang harus dihindari: melaporkan AUPRC naik setelah pembobotan lalu menyimpulkan FAR membaik; AUPRC hampir tidak berubah sementara FAR bisa berubah puluhan kali.

Prevalensi yang menjadi konteks (terukur, dari jawaban tim Data `docs/RND_D0_DATA_FEASIBILITY.md`): hyd_ki 0,1366; shk 0,0355; ssi 0,0169; stuck_k2 0,0167; vib 0,2269; stuck_k1 0,3613. Konsekuensi: pada stuck_k2, ambang probabilitas 0,5 praktis tidak akan pernah tercapai, sehingga "model gagal" pada ambang 0,5 bukan informasi.

### 6.3 Rancangan uji imbalance

Untuk setiap kelas, tiga perlakuan pada fold yang sama:

1. tanpa pembobotan, ambang dipilih pada FAR target;
2. `class_weight`/`scale_pos_weight` = rasio negatif/positif, ambang dipilih pada FAR target yang sama;
3. focal loss (gamma 2) bila kerangka mendukung, ambang pada FAR target yang sama.

Keluaran wajib: presisi, recall, FAR, FP per shift, dan AUPRC untuk ketiga perlakuan. Klaim "pembobotan membantu" hanya sah bila presisi pada FAR target meningkat dengan CI bootstrap tidak memuat nol.

Status: **BELUM TERUKUR** untuk ketiga perlakuan pada data kita. Yang sudah terukur hanyalah bahwa RF kontrak V9 memakai `balanced_subsample` sejak awal (konvensi kode), bukan hasil uji pembanding.

---

## 7. Rencana uji lengkap (siap dieksekusi Engineer)

### 7.1 Protokol

```
Data        : scratch/v9_d1/datasets/<kelas>.csv.gz, fitur D1 (55, hyd 40)
Split       : LOWO per well (latih semua well lain, uji satu well)
Imputasi    : SimpleImputer(median) di-fit HANYA pada set latih (fold-safe)
Model       : RF kontrak V9; LightGBM(num_leaves 31, min_child_samples 20, lr 0,05);
              XGBoost(depth 6, lr 0,05, hist, scale_pos_weight); CatBoost(depth 6, lr 0,05,
              auto_class_weights Balanced)
Anggaran    : thread dibatasi sama untuk semua model (mis. n_jobs=4), supaya biaya
              dibandingkan pada anggaran paralel yang sama
Kalibrasi   : isotonic dan Platt, di-fit pada well kalibrasi terpisah (skema §4.3)
Keputusan   : tiga varian ambang §5.4
Metrik      : AUPRC, ΔB vs prevalensi dan vs baseline aturan; FAR per 24 jam; B1;
              TLead (menit); presisi/recall pada FAR target
Uji statistik: DeLong untuk AUC berkorelasi pada fold yang sama; bootstrap 2.000
              resample untuk selisih AUPRC dan selisih FAR (CI 95 persen); tidak ada
              klaim menang tanpa CI tidak memuat nol
Pra-registrasi: ambang, jumlah bootstrap, dan daftar fold ditulis SEBELUM run,
              supaya tidak ada pemilihan setelah melihat hasil
```

### 7.2 Definisi metrik yang dipakai (agar tidak berbeda antar kartu)

| Metrik | Definisi operasional | Catatan |
|---|---|---|
| AUPRC | `average_precision_score(y, skor)` | dilaporkan dengan prevalensi fold yang sama (ΔB), bukan mentah saja |
| FAR | `FP / (n_neg / 60) * 24` per 24 jam, jendela 60 detik | konvensi kampanye, sama dengan `code/v9_i1_pipeline.py` |
| B1 | proporsi onset yang punya minimal satu alarm sebelum onset dalam horizon | dipakai di klaim K-ii |
| TLead | jarak waktu alarm pertama ke onset, menit | dilaporkan median dan sebaran, bukan rata-rata saja |
| DeLong | uji AUC berkorelasi pada sampel yang sama | sah untuk membandingkan dua model pada fold yang sama |
| Bootstrap | resample baris uji dengan penggantian, 2.000 kali | untuk AUPRC dan FAR; seed tetap |

### 7.3 Gerbang keputusan (tidak berubah)

Naik tier hanya bila tiga syarat terpenuhi bersamaan (plan §6): C stabil antar well, A FAR ≤ 6 per 24 jam pada titik operasi, B beban pemeriksaan manusia wajar. Algoritma baru yang menang AUPRC tetapi gagal FAR tetap di TREN.

---

## 8. Rujukan dan status verifikasi

Metode verifikasi: `curl` ke `api.crossref.org/works/<DOI>` (metadata judul, penulis pertama, tahun) dan `curl -L` ke URL landing (status HTTP), tanggal akses 2026-10-27.

| # | Penulis pertama, tahun | Judul | DOI / URL | Status |
|---|---|---|---|---|
| 1 | Ke, G., 2017 | LightGBM: A Highly Efficient Gradient Boosting Decision Tree | https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html | TERVERIFIKASI (HTTP 200) |
| 2 | Chen, T., 2016 | XGBoost: A Scalable Tree Boosting System | DOI 10.1145/2939672.2939785 | TERVERIFIKASI (Crossref 200, judul cocok) |
| 3 | Prokhorenkova, L., 2018 | CatBoost: unbiased boosting with categorical features | https://arxiv.org/abs/1706.09516 | SEBAGIAN: URL abs HTTP 200; metadata judul tidak berhasil diambil ulang dari arXiv API (balasan kosong), judul dari ingatan agen |
| 4 | Niculescu-Mizil, A., 2005 | Predicting good probabilities with supervised learning | DOI 10.1145/1102351.1102430 | TERVERIFIKASI (Crossref 200, judul cocok) |
| 5 | Vovk, V., 2005 | Algorithmic Learning in a Random World | DOI 10.1007/b106715 | TERVERIFIKASI (Crossref 200 dan doi.org 200) |
| 6 | Angelopoulos, A. N., 2021 | A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification | https://arxiv.org/abs/2107.07511 | SEBAGIAN: URL HTTP 200; metadata judul tidak berhasil diambil ulang |
| 7 | Angelopoulos, A. N., 2022 | Conformal Risk Control | https://arxiv.org/abs/2208.02814 | SEBAGIAN: URL HTTP 200; metadata judul tidak berhasil diambil ulang |
| 8 | Lin, T.-Y., 2017 | Focal Loss for Dense Object Detection | DOI 10.1109/ICCV.2017.324 | TERVERIFIKASI (Crossref 200, judul cocok) |
| 9 | DeLong, E. R., 1988 | Comparing the Areas under Two or More Correlated Receiver Operating Characteristic Curves: A Nonparametric Approach | DOI 10.2307/2531595 | TERVERIFIKASI (Crossref 200, judul cocok) |
| 10 | Saito, T., 2015 | The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets | DOI 10.1371/journal.pone.0118432 | TERVERIFIKASI (Crossref 200, judul cocok) |

**Ditolak sebagai dasar rekomendasi:** Zadrozny & Elkan 2002 ("Transforming classifier scores into accurate multiclass probability estimates"). Dua DOI yang dicoba (10.1145/775047.775109 dan 10.1145/775047.775126) keduanya menunjuk paper lain (Ayres 2002 tentang sequential pattern mining; Jeh 2002 tentang SimRank). Karena DOI-nya tidak dapat diverifikasi, rujukan ini **tidak dipakai** di dokumen ini, dan klaim kalibrasi bersandar pada Niculescu-Mizil & Caruana 2005 (terverifikasi).

Rujukan untuk boosting dan conformal yang dipakai sebagai **dasar struktural** (bukan dasar angka) adalah nomor 1, 2, 3, 5. Rekomendasi angka di dokumen ini seluruhnya bersandar pada pengukuran sendiri atau pada konvensi internal, bukan pada angka literatur.

---

## 9. Yang belum terukur atau belum terverifikasi (jujur, tanpa dibungkus)

1. **BELUM TERUKUR**: AUPRC dan biaya latih LightGBM, XGBoost, CatBoost pada seluruh kelas. Run pembanding tidak selesai dalam anggaran waktu kartu (gejala terukur: proses `n_jobs=-1` melewati 420 detik pada 21.933 x 55 baris, utilisasi CPU sekitar 1.300 persen).
2. **BELUM TERUKUR**: Brier, ECE, kurva reliabilitas untuk isotonic dan Platt pada data kita.
3. **BELUM TERUKUR**: jumlah sampel kalibrasi minimum yang memadai. Yang ada hanya ukuran himpunan (1.989 sampai 10.903 baris per well pada vib), bukan hasil uji kelayakan.
4. **BELUM TERUKUR**: tiga varian ambang conformal (V1/V2/V3) dan selisih FAR empiris terhadap alpha.
5. **BELUM TERUKUR**: efek `class_weight`, `scale_pos_weight`, dan focal loss terhadap presisi dan FAR pada titik operasi yang dipatok.
6. **BELUM TERVERIFIKASI**: metadata judul untuk tiga rujukan arXiv (CatBoost, Angelopoulos 2021, 2022); URL dapat dibuka tetapi arXiv API mengembalikan badan kosong saat diperiksa ulang.
7. **BELUM TERVERIFIKASI**: DOI Zadrozny & Elkan 2002 (dua DOI yang dicoba menunjuk paper lain), sehingga rujukan itu tidak dipakai.
8. **Catatan data**: pada kelas vib, 4 dari 55 fitur (`SPM_mean`, `SPM_std`, `SPM_slope`, `SPM_last`) seluruhnya kosong sehingga diimputasi kosong oleh `SimpleImputer` (peringatan sklearn tercatat di log run). Fitur efektif = 51, bukan 55. Ini temuan yang harus dilaporkan ke tim Data, bukan diperbaiki diam-diam di dokumen.
9. **Belum diuji**: apakah keunggulan LightGBM pada volume besar (stuck_k2 118.567 baris) tetap berlaku setelah pembatasan thread, karena run-nya tidak pernah selesai.

---

## 10. Ringkasan 5 baris

1. Empat sumbu (ranking, probabilitas, keputusan, titik operasi) dipisahkan; boosting hanya menjawab sumbu ranking dan biaya, kalibrasi sumbu probabilitas, conformal sumbu keputusan, imbalance sumbu titik operasi.
2. Satu-satunya angka model yang terukur hari ini adalah RF kontrak V9 pada fold vib F-14: AUPRC 0,9117 dengan prevalensi 0,5651 (ΔB +0,3466), latih 7,41 detik; angka ini konsisten dengan rentang 0,441 sampai 0,912 yang sudah dilaporkan EVAL_C.
3. Biaya dan AUPRC LightGBM, XGBoost, CatBoost pada data kita BELUM TERUKUR karena run pembanding tidak selesai (gejala thread over-subscription), dan angka literatur sengaja tidak dipakai sebagai pengganti.
4. Conformal memberi jaminan marginal hanya bila exchangeability terpenuhi; pada data kita asumsi itu dilanggar lintas well, jadi conformal layak dipakai untuk kalibrasi prospektif dalam-well, bukan sebagai klaim jaminan lintas well.
5. Rekomendasi sebelum perubahan tier apa pun: pilot LOWO 4 model x 3 varian ambang pada vib dan shk, dengan FAR, B1, TLead, AUPRC, DeLong dan bootstrap, pra-registrasi ditulis lebih dulu.

## 11. Daftar belum terverifikasi (ringkas untuk audit)

- LightGBM/XGBoost/CatBoost: AUPRC dan biaya latih pada data kita.
- Isotonic dan Platt: Brier, ECE, kelayakan jumlah sampel kalibrasi.
- Conformal: FAR empiris V1/V2/V3 terhadap alpha.
- Imbalance: presisi dan FAR untuk ketiga perlakuan.
- Metadata judul tiga rujukan arXiv (URL 200, metadata tidak terbaca ulang).
- DOI Zadrozny & Elkan 2002 (ditolak, tidak dipakai).
- Efek 4 fitur `SPM_*` kosong terhadap hasil (terdeteksi, belum dikuantifikasi).
