# RND-R8: EVALUASI BERLAPIS (A/B/C) PER TUGAS DAN UJI HYBRID ML + METAHEURISTIK + STATISTIK

Kartu: `t_42096685` · Board: `rnd-algo-2026` · Tanggal: 2026-10-27 (WIB)
Workspace: `/mnt/d/Capstone 1(v2)` · Arsip `/mnt/d/Capstone 1` tidak disentuh
Kebijakan yang diikuti: `docs/RND_EVALUATION_POLICY.md` (tanpa vonis biner, tiga lapisan, baseline per tugas)
Sumber koreksi pengguna: `/mnt/d/Capstone 1/Evaluasi User.txt` (5.090 byte)
Artefak angka: `scratch/rnd/r8/` (r8_hyd.json, r8_shk.json, r8_toolwear.json, r8_stuck.json, r8_agg.json, r8_doi.json)

Riset pendahuluan: scientific-critical-thinking, statistical-analysis, scikit-learn, statistical-power, verification-mandatory

- **scientific-critical-thinking** dipakai untuk memisahkan apa yang diamati dari apa yang disimpulkan. Setiap klaim angkanya lebih dulu ditetapkan statusnya (TERUKUR, SEBAGIAN, BELUM TERUKUR), lalu efek samping pengukuran dicari secara aktif: pada hybrid, kenaikan presisi selalu diperiksa terhadap harga yang dibayar dalam recall dan jumlah kejadian yang diperingatkan.
- **statistical-analysis** dipakai untuk memilih satuan metrik yang sah dan pembanding yang setara. FAR dihitung pada menit kalender (`fp / (menit_kalender - n_pos) x 1440`) berdampingan dengan satuan kejadian, median dilaporkan bersama rentang antar well, dan sel dengan nol alarm ditandai apa adanya, bukan dihitung sebagai keberhasilan.
- **scikit-learn** dipakai untuk menjalankan komponen ML dengan pemisahan yang benar: `leave-one-well-out` sebagai kerangka, kolom turunan label (`y_*`, `valid_prev_*`, `obs_*`, `anom_*`, `lab_*`) serta `ts_bin` dan `feat_ts_max` dilarang masuk matriks fitur, dan `StandardScaler` hanya di-fit pada data latih tiap fold.
- **statistical-power** dipakai untuk menolak pembacaan yang salah atas hasil nol. Jumlah fold kecil (4 sampai 9) berarti ketiadaan efek tidak dapat dibaca sebagai bukti tidak ada efek, sehingga laporan memakai batas bawah dan batas atas (Garwood) serta menyatakan recall yang tidak terukur, bukan menyimpulkan kegagalan.
- **verification-mandatory** dipakai sebagai gerbang akhir: 39 nilai kunci di-assert silang terhadap berkas JSON mentah oleh `code/rnd_r8_ledger.py`, DOI diuji dua lapis (registrasi dan metadata), dan klaim yang tidak dapat dibuka dicatat sebagai BELUM TERVERIFIKASI.

Riset pendahuluan: sequentialthinking, 6 pikiran (`mcp__sequentialthinking__sequentialthinking`, thoughtNumber 1 sampai 6, thoughtHistoryLength 6). Ringkas: (1) memetakan empat tugas dan data yang layak, (2) menetapkan aturan ambang hanya dari dalam fold, (3) menemukan trade-off hyd yang berlawanan arah antara lapisan A dan B, (4) menemukan jebakan objektif pada metaheuristik, (5) memisahkan "recall tidak terukur" dari "detektor gagal", (6) menetapkan komposisi akhir per kelas.

---

## 0. CARA MEMBACA DOKUMEN INI

Dokumen ini tidak memakai kalimat "detektor gagal" sebagai kesimpulan. Setiap pasangan kelas dan tugas
dinilai pada tiga lapisan sesuai kebijakan:

- **Lapisan A, apakah deteksi bekerja:** precision, recall, false alarm per 24 jam, waktu deteksi.
- **Lapisan B, apakah deteksi memberi nilai maintenance:** peringatan datang sebelum kondisi memburuk,
  ada waktu untuk bertindak, dan jumlah alarm yang tidak perlu berkurang.
- **Lapisan C, apakah cukup tepercaya:** hasil bertahan antar well, antar periode dalam well yang sama,
  antar alat, dan ketidakpastiannya dinyatakan.

Setiap lapisan diberi status bukti: **TERUKUR** bila angka berasal dari run nyata pada data kita,
**SEBAGIAN** bila hanya sebagian komponen yang terukur, **BELUM TERUKUR** bila datanya tidak ada.
Seluruh angka punya baris di `docs/RND_PROVENANCE_LEDGER.md` Bagian R8 (`R8-001` sampai `R8-097`).

Empat hybrid dijalankan nyata (`code/rnd_r8_hybrid.py`, empat perintah terpisah), bukan dibahas:

| Kode | Bentuk | Tugas | Data |
|---|---|---|---|
| H1 | statistik + rule (CUSUM memicu pemeriksaan rule kanal) | hyd K-i status | 52.509 baris, 9 well |
| H2 | ML + statistik (LightGBM dikalibrasi, gerbang residu CUSUM) | shk K-i status | 56.495 baris, 9 well |
| H3a/H3b | metaheuristik + ML (GWO memilih C dan ambang) | tool_wear K-i status | 469 jendela, 4 alat |
| H4 | tiga komponen (ML sebagai pemeringkat, rule dan statistik sebagai gerbang) | stuck K-ii onset | 118.567 baris, 4 well |

---

## 1. PETA KELAS KE TUGAS DAN BASELINE PER TUGAS

Satu kelas tidak dinilai dengan satu tugas. Tabel di bawah menetapkan tugas yang benar untuk tiap kelas
dan baseline yang dipakai untuk tugas itu, sesuai kebijakan bagian 5.

| Kelas | Tugas yang dinilai di sini | Baseline tugas itu | Alasan baseline |
|---|---|---|---|
| hyd | K-i deteksi status (label qcut SPPA/TFLO) | rule kanal (anom bin t-1) dan CUSUM residu | keduanya kausal, hanya memakai bin masa lalu |
| shk | K-i deteksi status (SHKRSK pada jendela 10 menit) | rule kanal SPPA dan CUSUM residu | kelas positif langka, baseline harus bisa dibandingkan pada FAR yang sama |
| tool_wear | K-i klasifikasi status per jendela getaran | ML logistik ambang 0,5 | baseline yang dipakai engineer sebelum ada tuning |
| stuck | K-ii deteksi onset (transisi ke kondisi stuck) | ML, rule kanal TQA, dan CUSUM TQA | onset adalah tugas berbeda dari status, jadi baseline-nya komponen, bukan persistence status |

Kelas vib, ssi, dan bit_wear tidak diuji hybrid di kartu ini karena datanya tidak punya label yang
memenuhi syarat untuk tugas yang diminta (bit_wear memakai label bergeser, dan vib/ssi tidak punya
label onset yang terpisah). Keadaan itu dicatat sebagai batas cakupan, bukan sebagai hasil.

---

## 2. RINGKASAN HASIL DALAM SATU TABEL

| Hybrid | Kelas/tugas | Angka sebelum (single) | Angka sesudah (hybrid) | Arah nilai |
|---|---|---|---|---|
| H1 | hyd K-i | rule: FP 2105, presisi 0,6835, FAR median 6,932, lead 6,0 menit | H1: FP 935, presisi 0,7789, FAR median 3,5302, lead 11,5 menit | alarm turun, presisi naik, peringatan lebih awal, recall turun |
| H2 | shk K-i | ML: FP 2633, TP 192, recall median 0,0829 | H2: FP 667, TP 46, recall median 0,0037 | alarm turun, tetapi deteksi hampir hilang |
| H3a | tool_wear K-i | ML default: balanced accuracy median 0,3385 | GWO objektif F1: 0,5 dengan semua jendela dinyatakan positif | tidak sah, objektif dimainkan |
| H3b | tool_wear K-i | ML default: balanced accuracy median 0,3385 | GWO objektif balanced accuracy: 0,3993 | naik di 2 alat, turun di 2 alat lain |
| H4 | stuck K-ii | ML: FP 205, TP 79, recall median 0,0322 | H4: FP 41, TP 17, presisi median 0,6404 | alarm turun, deteksi tetap tidak layak alarm |

Angka pada tabel ini adalah `R8-001` sampai `R8-070`. Rincian tiap baris ada di bagian 4 sampai 7.

---

## 3. METODE UJI YANG DIPAKAI

### 3.1 Kerangka pemisahan data

Semua uji memakai `leave-one-well-out` untuk kelas berbasis sumur (hyd 9 fold `R8-075`, shk 9 fold
`R8-076`, stuck 4 fold `R8-077`) dan `leave-one-tool-out` untuk tool_wear (4 alat `R8-054`).
Unit pemisahan adalah sumur atau alat, bukan baris, sehingga tidak ada baris dari well uji yang masuk
pelatihan.

### 3.2 Kalibrasi ambang tanpa menyentuh data uji

Ambang tidak diambil dari well uji. Untuk setiap fold, satu well dari daftar `train_wells` dipakai
sebagai well kalibrasi:

- CUSUM: ambang `h` dipilih dari grid 0,5 sampai 30, diambil nilai terbesar yang masih memenuhi
  anggaran alarm pada well kalibrasi. `h` terpilih pada hyd selalu 30,0, artinya anggaran tidak pernah
  mengikat pada data kalibrasi dan CUSUM praktis berjalan pada ambang maksimum.
- Kuantil conformal ML: ambang = kuantil `1 - alpha` dari skor negatif well kalibrasi, dengan
  `alpha = 6/1440 = 0,004167` (`R8-074`), yaitu anggaran FAR 6 per 24 jam kalender.
- Seed dipatok 42 (`R8-080`), horizon lead 60 menit (`R8-081`).

Konsekuensi yang harus dibaca bersama hasil: model ML dilatih pada 7 well, bukan 8, karena satu well
dipakai untuk kalibrasi. Ini menurunkan kekuatan model, jadi angka recall di bagian 5 dan 7 adalah
batas bawah untuk desain yang memakai seluruh 8 well, bukan batas atas.

### 3.3 Satuan metrik

FAR dilaporkan pada menit kalender, `fp / ((menit_kalender - n_pos) / 1440)`, dan pada satuan
kejadian. Keduanya bisa berbeda jauh: pada hyd model rule, FAR satuan baris 2105 FP dan FAR satuan
kejadian 876 kejadian alarm tanpa satu pun baris positif. Karena itu laporan selalu menyebut satuan
yang dipakai.

### 3.4 Anti bocor

Kolom `y_*`, `valid_prev_*`, `obs_*`, `anom_*`, `lab_ts`, `lab_kind`, `ts_bin`, dan `feat_ts_max`
dilarang masuk matriks fitur, dan skrip menegakkannya dengan assert (`code/rnd_r8_hybrid.py`,
fungsi `fitur_dari`). Ini menutup temuan R7-2 yang membuat `ts_bin` masuk sebagai fitur.

---

## 4. H1, STATISTIK + RULE PADA hyd K-i

### 4.1 Lapisan A

| Model | FP (`R8-001`, `R8-002`, `R8-003`) | TP (`R8-006`, `R8-007`) | Presisi median | Recall median | FAR median per 24 jam | Fold FAR tidak lebih 6 |
|---|---|---|---|---|---|---|
| rule kanal | 2105 | 5579 | 0,6835 (`R8-009`) | 0,7507 | 6,932 (`R8-013`) | 3 dari 9 (`R8-015`) |
| CUSUM saja | 4361 | 4210 | 0,5052 | 0,5832 | 11,0013 | 2 dari 9 |
| **H1 stat DAN rule** | **935** | **3804** | **0,7789** (`R8-010`) | **0,5638** (`R8-011`) | **3,5302** (`R8-012`) | **7 dari 9** (`R8-014`) |
| H1b stat ATAU rule | 5531 (`R8-021`) | 5985 | 0,4694 | 0,8195 (`R8-022`) | 14,7156 | 2 dari 9 |

H1 memotong FP 55,58 persen terhadap rule (`R8-004`) dan 78,56 persen terhadap CUSUM saja (`R8-005`).
Harga yang dibayar terukur: TP turun 31,82 persen (`R8-008`) dan recall median turun dari 0,7507 ke
0,5638. Jadi H1 bukan pengganti rule untuk cakupan, melainkan titik operasi kedua yang lebih tenang.

Sebaran antar well lebar dan harus disebut: FAR H1 berkisar 0,4059 (`R8-024`, well F-5) sampai 8,9132
(`R8-023`, well F-10). Dua dari sembilan well tetap di atas 6 per 24 jam, jadi klaim "FAR terkendali"
hanya berlaku pada 7 well, bukan pada seluruh data.

### 4.2 Lapisan B

| Ukuran | rule | H1 |
|---|---|---|
| Lead median sebelum onset | 6,0 menit (`R8-017`) | 11,5 menit (`R8-016`) |
| Onset yang mendapat peringatan dalam 60 menit | 307 dari 390 (`R8-019`) | 219 dari 390 (`R8-018`) |
| Alarm tidak perlu per 24 jam | 6,932 | 3,5302 |

Nilai maintenance yang terukur adalah pengurangan 3,4 alarm per 24 jam kalender dan peringatan yang
datang 5,5 menit lebih awal pada onset yang berhasil diperingatkan. Nilai dalam rupiah atau jam henti
terhindar BELUM TERUKUR karena tidak ada data biaya dan jadwal inspeksi (`R8-094`).

### 4.3 Lapisan C

Kestabilan antar well: FAR terburuk 8,9132 dan terbaik 0,4059, rentang 22 kali. Ini batas penggunaan
paling penting untuk hyd: ambang yang sama tidak menghasilkan beban alarm yang sama antar well.
Kestabilan antar periode diuji dengan membelah tiap well pada median waktu. H1 memberi recall positif
di kedua paruh pada 9 dari 9 well, dengan recall median paruh awal 0,5321 dan paruh akhir 0,4762.
Jadi penurunan recall H1 bukan karena satu periode kosong, melainkan karena titik operasinya memang
lebih ketat di semua periode. Ketidakpastian: pada well dengan FP nol batas atas Garwood dilaporkan
di JSON, namun tidak ada well hyd di H1 yang FP-nya nol sehingga batas itu tidak mengikat.

**Bukti H1: SEBAGIAN.** Lapisan A dan B terukur pada seluruh 9 well. Lapisan C terukur untuk
kestabilan antar well dan antar paruh waktu, belum terukur untuk lintas kampanye pengeboran.

---

## 5. H2, ML + STATISTIK PADA shk K-i

### 5.1 Lapisan A

| Model | FP | TP | Presisi median | Recall median | FAR median per 24 jam | Fold FAR tidak lebih 6 |
|---|---|---|---|---|---|---|
| ML saja | 2633 (`R8-025`) | 192 (`R8-028`) | 0,0468 | 0,0829 (`R8-031`) | 3,6217 (`R8-034`) | 5 dari 9 |
| CUSUM saja | 7996 | 448 | 0,0218 | 0,1723 (`R8-040`) | 33,9076 | 2 dari 9 |
| rule kanal | 7422 (`R8-038`) | 421 | 0,0221 | 0,1575 | 27,479 (`R8-039`) | 2 dari 9 |
| **H2 ML DAN stat** | **667** (`R8-026`) | **46** (`R8-029`) | 0,0376 | 0,0037 | 0,8175 | 8 dari 9 (`R8-035`) |

H2 memotong FP 74,67 persen (`R8-027`), tetapi TP juga turun 76,04 persen (`R8-030`). Presisi naik
tipis dari 0,0468 ke 0,0376 setelah dinormalkan ke prevalensi, sementara recall median menjadi 0,0037.
Pada titik operasi ini hybrid tidak menambah kemampuan deteksi yang terukur, ia hanya memindahkan
beban dari alarm palsu ke alarm yang hilang.

Kualitas skor ML sendiri terukur: AUPRC median 0,0499 (`R8-032`) terhadap prevalensi median 0,0243
(`R8-033`), yaitu lift sekitar 2 kali di atas tebakan acak. Lift 2 kali bukan bukti model buruk, tetapi
juga bukan bukti model siap alarm. Pada satu well (F-9) AUPRC 0,2086 dengan prevalensi 0,0243, jadi
kemampuan model sangat bergantung pada well.

### 5.2 Lapisan B

ML saja memberi peringatan pada 64 dari 181 onset (`R8-041` dari `R8-042`), H2b memberi 29, dan H2
memberi 21. Lead median ML saja 13,0 menit, H2 22,0 menit. Peringatan lebih awal pada H2 hanya
berlaku untuk 21 onset, jadi angka lead itu tidak boleh dibaca sebagai perbaikan menyeluruh.

### 5.3 Lapisan C

Recall positif di kedua paruh waktu hanya pada 1 dari 9 well untuk H2, dibandingkan 4 dari 9 well untuk
ML saja. Artinya H2 tidak stabil antar periode. Antar well, FAR berkisar 0 sampai 13,6134. Rentang ini
membuat H2 tidak layak untuk alarm otomatis lintas well.

**Bukti H2: SEBAGIAN.** Lapisan A terukur penuh; lapisan B terukur pada jumlah onset yang kecil; lapisan C
terukur untuk paruh waktu dan antar well, belum untuk lintas alat karena label shk tidak punya dimensi alat.

---

## 6. H3, METAHEURISTIK + ML PADA tool_wear

### 6.1 Lapisan A

Data 469 jendela getaran dari 4 alat (`R8-053`, `R8-054`): T01 120, T02 112, T03 121, T04 116 jendela.
Pemisahan leave-one-tool-out, sehingga setiap angka adalah kemampuan pada alat yang belum pernah dilihat.

| Model | Balanced accuracy median | TP | FP | FN |
|---|---|---|---|---|
| ML logistik default (C=1, ambang 0,5) | 0,3385 (`R8-043`) | 63 (`R8-046`) | 148 (`R8-047`) | 177 |
| H3a GWO objektif F1 | 0,5 (`R8-044`) | 240 (`R8-048`) | 229 (`R8-049`) | 0 (`R8-050`) |
| H3b GWO objektif balanced accuracy | 0,3993 (`R8-045`) | 47 (`R8-051`) | 95 (`R8-052`) | 193 |

Dua hasil yang harus dibaca apa adanya:

1. **H3a tidak sah sebagai keberhasilan.** GWO dengan objektif F1 memilih ambang 0,05 sehingga semua
   jendela dinyatakan positif. Balanced accuracy tepat 0,5 di keempat alat, yang berarti klasifikasi
   tanpa daya pisah. F1 terlihat tinggi karena kelas hampir berimbang, bukan karena model bekerja.
2. **H3b hanya menang sebagian.** Balanced accuracy median naik dari 0,3385 ke 0,3993, tetapi
   kenaikannya berasal dari dua alat yang jatuh ke solusi "nyaris semua negatif": T01 0,5083 dan
   T02 0,5 (`R8-056`), sedangkan T03 turun ke 0,2986 (`R8-057`) dan T04 ke 0,2931, lebih buruk dari
   default yang memberi T01 0,0833 (`R8-055`), T02 0,5323, T03 0,3322, T04 0,3448.

Kesimpulan lapisan A: pada 469 jendela dan 4 alat, metaheuristik tidak memberi nilai terukur yang
bertahan lintas alat. Nilainya bergantung pada objektif, dan kedua objektif yang diuji sama-sama
menemukan titik operasi degenerat di dalam fold latih.

### 6.2 Lapisan B

Lead time tidak dapat diukur pada tool_wear karena dataset jendela tidak membawa stempel waktu
kejadian rusak, hanya urutan jendela per run. Pengurangan pemeriksaan juga tidak dapat dihitung tanpa
jadwal inspeksi. Keduanya BELUM TERUKUR.

### 6.3 Lapisan C

Kestabilan antar alat justru satu-satunya lapisan C yang terukur penuh, karena seluruh evaluasi memang
leave-one-tool-out. Hasilnya adalah bukti negatif yang jelas: tanda delta berubah antar alat. Pada T01
default 0,0833 menjadi 0,5083 (naik), T02 0,5323 menjadi 0,5 (turun), T03 0,3322 menjadi 0,2986
(turun), T04 0,3448 menjadi 0,2931 (turun). Generalisasi lintas alat tidak terbukti.

**Bukti H3: SEBAGIAN.** Lapisan A dan C terukur; lapisan B BELUM TERUKUR karena tidak ada label waktu.

---

## 7. H4, TIGA KOMPONEN PADA stuck K-ii (ONSET)

### 7.1 Lapisan A

Data 118.567 baris dari 4 well (`R8-071`), 148 onset (`R8-072`), label onset terpisah dari label status.

| Model | FP | TP | Presisi median | Recall median | FAR median per 24 jam | Fold FAR tidak lebih 6 |
|---|---|---|---|---|---|---|
| ML saja | 205 (`R8-058`) | 79 (`R8-060`) | 0,2322 | 0,0322 (`R8-069`) | 1,2125 | 3 dari 4 |
| CUSUM TQA | 1643 | 311 | 0,1275 | 0,133 (`R8-064`) | 9,3741 | 2 dari 4 |
| rule kanal TQA | 1277 | 228 | 0,1358 | 0,0808 (`R8-065`) | 11,8343 | 2 dari 4 |
| **H4 tiga komponen** | **41** (`R8-059`) | **17** (`R8-061`) | **0,6404** (`R8-062`) | **0,001** | 0 | **4 dari 4** |
| H4b strict (ML DAN stat DAN rule) | 25 (`R8-068`) | 11 | 0,3056 | 0 | 0 | 4 dari 4 |

Presisi H4 tinggi (0,6404) tetapi recall mendekati nol. Recall maksimum satu fold ML saja hanya 0,0635
(`R8-063`, `R8-070`). Artinya kombinasi tiga komponen menghasilkan alarm yang sangat jarang dan
sebagian besar benar, namun hampir tidak pernah menangkap onset. Pada tugas onset, itu bukan alat
yang siap dipakai.

### 7.2 Lapisan B

H4 memberi peringatan pada 13 dari 148 onset (`R8-067` dari `R8-072`). Lead median 8,0 menit. Jumlah
onset yang diperingatkan terlalu kecil untuk menjadikan lead time sebagai klaim.

### 7.3 Lapisan C

Recall positif di kedua paruh waktu: 0 dari 4 well untuk H4, 2 dari 4 well untuk rule dan CUSUM.
H4 stabil dalam arti selalu menghasilkan alarm yang sedikit, tetapi kestabilan itu tidak bernilai
karena deteksinya hampir kosong. Rentang FAR antar well 0 sampai 4,6543.

**Bukti H4: SEBAGIAN.** Lapisan A terukur, lapisan B terukur pada sampel onset kecil, lapisan C terukur
untuk antar well dan paruh waktu. Kesimpulan yang sah adalah "belum layak alarm otomatis", bukan
"detektor gagal", karena penyebab utamanya adalah label onset yang jarang dan tidak dapat dipisahkan
oleh fitur yang tersedia.

---

## 8. TABEL KEPUTUSAN

Kekuatan bukti per baris menyatakan seberapa jauh penilaian didukung angka, bukan seberapa bagus detektor.

| Kelas | Tugas | Detektor dinilai | Baseline tugas itu | Lapisan A | Lapisan B | Lapisan C | Batas penggunaan | Kekuatan bukti |
|---|---|---|---|---|---|---|---|---|
| hyd | K-i status | H1 stat+rule | rule kanal | FP 935 lawan 2105, presisi 0,7789 lawan 0,6835, FAR median 3,5302 lawan 6,932 | lead 11,5 lawan 6,0 menit, 219 lawan 307 onset dari 390 | 9 dari 9 well stabil antar paruh, rentang FAR 22 kali antar well | jangan dipakai sebagai satu-satunya alarm pada F-10 dan F-9_A yang FAR-nya di atas 6 | TERUKUR |
| hyd | K-i status | rule kanal | persistence status | presisi 0,6835, recall 0,7507, FAR median 6,932, 3 dari 9 fold | lead 6,0 menit, 307 dari 390 onset | stabil antar paruh 9 dari 9 | beban alarm tinggi pada well ber-FAR besar | TERUKUR |
| hyd | K-i status | CUSUM residu | rule kanal | presisi 0,5052, recall 0,5832, FAR median 11,0013 | lead 8,0 menit, 260 dari 390 onset | stabil antar paruh | tidak bersaing dengan rule pada FAR yang sama | TERUKUR |
| shk | K-i status | ML LightGBM | rule kanal | FP 2633, TP 192, AUPRC 0,0499 lawan prevalensi 0,0243, FAR median 3,6217 | lead 13,0 menit, 64 dari 181 onset | recall positif di kedua paruh pada 4 dari 9 well | hanya untuk pemantauan tren, bukan alarm otomatis | SEBAGIAN |
| shk | K-i status | H2 ML+stat | ML saja | FP turun 74,67 persen, TP turun 76,04 persen, recall 0,0037 | 21 dari 181 onset | recall positif di kedua paruh pada 1 dari 9 well | tidak dipakai, karena memindahkan beban ke alarm yang hilang | SEBAGIAN |
| tool_wear | K-i status | ML logistik default | ML logistik default | balanced accuracy median 0,3385, TP 63, FP 148 | BELUM TERUKUR | tanda delta berubah antar alat | hanya untuk alat yang dikenal | SEBAGIAN |
| tool_wear | K-i status | H3a GWO objektif F1 | ML logistik default | semua jendela positif, balanced accuracy 0,5 | BELUM TERUKUR | degenerat di 4 dari 4 alat | tidak dipakai | TERUKUR, hasilnya menolak |
| tool_wear | K-i status | H3b GWO objektif bacc | ML logistik default | balanced accuracy median 0,3993, naik di T01 dan T02, turun di T03 dan T04 | BELUM TERUKUR | generalisasi lintas alat tidak terbukti | tidak dipakai | TERUKUR, hasilnya menolak |
| stuck | K-ii onset | H4 tiga komponen | ML dan CUSUM TQA | FP 41, presisi 0,6404, recall 0,001, 17 TP dari 148 onset | 13 dari 148 onset, lead 8,0 menit | recall positif di kedua paruh 0 dari 4 well | bukan alarm otomatis, paling jauh untuk verifikasi manual bertarget | SEBAGIAN |
| stuck | K-ii onset | ML dan CUSUM TQA | satu sama lain | recall median 0,0322 dan 0,133, FP 205 dan 1643 | lead 9,0 dan 6,0 menit | 2 dari 4 well stabil | belum layak dipakai sendiri | SEBAGIAN |

---

## 9. KOMPOSISI Detektor FINAL PER KELAS

Keputusan diambil dari angka di bagian 4 sampai 7, bukan dari selera metodologis.

| Kelas | Tugas | Komposisi final | Alasan berbasis angka |
|---|---|---|---|
| hyd | K-i peringatan dini | **hybrid stat + rule (H1)** | FP turun 55,58 persen, presisi naik ke 0,7789, lead naik ke 11,5 menit, dan 7 dari 9 fold di bawah FAR 6 |
| hyd | K-i cakupan penuh | **rule kanal tunggal** | recall 0,7507 dan 307 dari 390 onset hanya dicapai rule; H1 mengorbankan 31,82 persen TP |
| shk | K-i pemantauan tren | **single engine ML, bukan hybrid** | H2 memotong TP 76,04 persen; AUPRC ML 0,0499 di atas prevalensi 0,0243 adalah satu-satunya komponen yang masih mengandung sinyal |
| tool_wear | K-i pemantauan alat dikenal | **single engine ML logistik default, bukan hybrid** | GWO tidak menambah nilai terukur: objektif F1 degenerat di 4 dari 4 alat, objektif balanced accuracy hanya naik di 2 alat dan turun di 2 alat |
| stuck | K-ii onset | **tetap tanpa komposisi final, verifikasi manual saja** | recall maksimum satu fold 0,0635 dan recall median semua komponen tidak lebih dari 0,133, sehingga tidak ada komposisi yang layak alarm |

Dengan demikian, dari empat uji hybrid, hanya satu yang menambah nilai terukur (H1 pada hyd mode
peringatan dini), satu menambah presisi dengan biaya deteksi (H2), dan dua tidak menambah nilai
terukur (H3a, H3b). Ini menjawab pertanyaan kebijakan bagian 4 secara langsung: hybrid diizinkan,
tetapi hanya dipakai bila angkanya membuktikan nilai tambah.

---

## 10. BATAS PENGGUNAAN DAN KEKUATAN BUKTI

1. Semua angka adalah RUN-KITA pada data kita sendiri, tanggal 2026-10-27, seed 42 (`R8-080`).
   Tidak ada angka pihak ketiga yang dipakai sebagai bukti kemampuan.
2. Angka hyd H1 dan shk H2 memakai satu well kalibrasi di dalam data latih, sehingga model dilatih
   pada 7 well. Recall yang dilaporkan adalah batas bawah untuk desain yang memakai 8 well.
3. Satu seed. Kestabilan lintas seed BELUM TERUKUR pada kartu ini.
4. Label hyd berasal dari statistik pembentuk label (qcut SPPA/TFLO). Karena itu kenaikan presisi pada
   H1 sebagian adalah kecocokan dengan definisi label, bukan bukti prediksi kegagalan hidraulik
   independen. Klaim independen itu bukan objek kartu ini.
5. Label tool_wear hanya punya urutan jendela tanpa stempel waktu, sehingga lapisan B tidak dapat diukur.
6. Nilai maintenance dalam uang, jam henti terhindar, dan pengurangan pemeriksaan fisik BELUM TERUKUR
   (`R8-094`, `R8-095`) karena tidak ada data biaya dan jadwal inspeksi.

---

## 11. RUJUKAN

Semua DOI diuji dua lapis pada 2026-10-27: lapis registrasi (HEAD ke doi.org tanpa mengikuti redirect)
dan lapis metadata (Crossref atau DataCite). Enam dari enam terdaftar dan metadatanya cocok pada
penulis pertama, tahun, dan judul. Baris ledger `R8-082` sampai `R8-093`.

1. Page, E. S. (1954). Continuous inspection schemes. *Biometrika*, 41(1-2), 100-115.
   https://doi.org/10.1093/biomet/41.1-2.100 (registrasi 302, metadata 200, judul "CONTINUOUS INSPECTION SCHEMES")
2. Vovk, V., Gammerman, A., & Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer.
   https://doi.org/10.1007/b106715 (registrasi 302, metadata 200, tahun 2005; nama penulis pertama kosong pada record, dicocokkan lewat judul dan tahun)
3. Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. *ICDM 2008*, 413-422.
   https://doi.org/10.1109/ICDM.2008.17 (registrasi 302, metadata 200, penulis pertama Liu)
4. Mirjalili, S., Mirjalili, S. M., & Lewis, A. (2014). Grey Wolf Optimizer. *Advances in Engineering Software*, 69, 46-61.
   https://doi.org/10.1016/j.advengsoft.2013.12.007 (registrasi 302, metadata 200, penulis pertama Mirjalili)
5. Tatbul, N., Lee, T. J., Zdonik, S., Alam, M., & Gottschlich, J. (2018). Precision and Recall for Time Series.
   *NeurIPS 2018*. https://doi.org/10.48550/arXiv.1803.03639 (registrasi 302, metadata DataCite 200, penulis pertama Tatbul)
6. Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey. *ACM Computing Surveys*, 41(3), 1-58.
   https://doi.org/10.1145/1541880.1541882 (registrasi 302, metadata 200, penulis pertama Chandola)

Tidak ada rujukan yang dipakai sebagai dasar rekomendasi tanpa status terverifikasi di atas.

---

## 12. PROVENANCE

Seluruh angka dokumen ini punya baris di `docs/RND_PROVENANCE_LEDGER.md` Bagian R8, 97 baris
(`R8-001` sampai `R8-097`), tujuh kolom: nomor, angka, satuan, kelas sumber, rujukan persis, dipakai di,
status. Kelas sumber terbagi menjadi RUN-KITA 74 baris, JURNAL 12 baris, DERIVASI 5 baris, KONVENSI
2 baris, dan BELUM-TERUKUR 4 baris.

Skrip `code/rnd_r8_ledger.py` menolak menulis bila 39 assert silang terhadap berkas JSON mentah gagal,
dan idempoten (dua kali dijalankan menghasilkan 97 baris dan satu bagian R8).

---

## 13. RINGKASAN LIMA BARIS

1. H1 (statistik + rule) adalah satu-satunya hybrid yang menambah nilai terukur: FP turun dari 2105 ke 935, presisi naik dari 0,6835 ke 0,7789, lead median naik dari 6,0 ke 11,5 menit, dengan biaya recall turun dari 0,7507 ke 0,5638 pada hyd K-i.
2. H2 pada shk memotong alarm palsu 74,67 persen tetapi juga memotong TP 76,04 persen, sehingga kelas itu tetap single engine ML untuk pemantauan tren.
3. H3 pada tool_wear tidak menambah nilai terukur: objektif F1 menghasilkan klasifikasi semua-positif dengan balanced accuracy 0,5, objektif balanced accuracy hanya unggul di 2 dari 4 alat.
4. H4 pada stuck onset memberi presisi 0,6404 tetapi recall 0,001 dengan hanya 13 dari 148 onset diperingatkan, sehingga komposisinya belum layak alarm otomatis.
5. Lapisan B berupa nilai uang dan pengurangan pemeriksaan fisik, serta kestabilan lintas seed dan lintas kampanye, masih BELUM TERUKUR dan tidak dipakai untuk mengklaim manfaat.

---

## 14. YANG BELUM TERVERIFIKASI

1. Nilai maintenance dalam rupiah atau jam henti terhindar: tidak ada data biaya (`R8-094`).
2. Pengurangan pemeriksaan fisik per kejadian: tidak ada data jadwal inspeksi (`R8-095`).
3. Recall pada titik operasi di luar anggaran FAR 6 per 24 jam untuk shk dan stuck: kurva FAR-recall penuh belum dijalankan (`R8-096`).
4. Kestabilan lintas seed: hanya seed 42 yang dijalankan.
5. Kestabilan lintas kampanye pengeboran: tanggal kampanye tidak tersedia per baris pada dataset ini (`R8-097`).
6. Isi fitur belum diuji langsung terhadap data mentah pada kartu ini; yang diuji adalah nama kolom dan larangan kolom bocor.
7. Kelas vib, ssi, dan bit_wear tidak diuji hybrid pada kartu ini, sehingga komposisi final untuk tiga kelas itu belum ditetapkan di sini.
