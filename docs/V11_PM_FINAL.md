# V11-PM_FINAL: VONIS AKHIR PERTANDINGAN PROPOSAL (BUKA ANONIMISASI)

Task: `t_0fe5b8fa` [Project Manager] · Board: `capstone-v11-vs` · 2026-10-15 (WIB).
Peran: satu-satunya penilai yang membuka identitas kandidat, memverifikasi ulang skor
EVAL-CMP, dan menetapkan vonis akhir mengikuti protokol terkunci `docs/V11_PROTOCOL.md` §3.

> Riset pendahuluan: `scientific-critical-thinking` - data (angka primer, skor) dipisah dari
> interpretasi (vonis); dua anomali skor dicari secara aktif (bukti yang membantah skor
> dicari, bukan dikonfirmasi); standar koreksi diterapkan simetris ke kedua kandidat.
> Riset pendahuluan: `verification-mandatory` - 15+ angka kunci dihitung ulang dengan
> eksekusi sendiri di sesi ini (bukan kutip kartu tim); cek parity .ipynb memakai skrip
> dengan negative control supaya tesnya bisa gagal; daftar "belum diverifikasi" eksplisit
> di §7.
> Riset pendahuluan: `statistical-analysis` - aritmetika skor dijumlahkan ulang per
> kriteria; sensitivitas vonis diuji dengan menggeser skor yang diperselisihkan ke ekstrem
> pro masing-masing kandidat; tidak ada rata-rata lintas kampanye.
> Riset pendahuluan: `what-if-oracle` - enam cabang kemungkinan (Ω/α/Δ/Ψ/Φ/∞) diuji
> terhadap vonis; vonis harus tetap berdiri di cabang kontrarian dan worst-case (§5).
> Riset pendahuluan: `consciousness-council` - lima arketipe (Empiricist, Contrarian,
> Strategist, Pragmatist, Ethicist) menekan vonis dengan ketegangan nyata (§6).
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 6 pikiran, 6/6 sukses): inventaris
> bukti -> verifikasi aritmetika -> pencarian anomali skor -> penilaian a-e -> uji
> kejujuran terhadap kepentingan operator -> rencana output.

---

## 0. BUKA ANONIMISASI

**Kandidat 1 = PROPOSAL VERSI ARSIP** (`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md`
dan `.ipynb`, versi 3.0 per 12 Oktober 2026, 352 baris).
**Kandidat 2 = PROPOSAL BARU / V10** (`docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` dan
`.ipynb`, 15 Oktober 2026, 3.557 baris).

Seluruh skor paruh-atas (EVAL-CMP) memakai label kandidat 1/2; di dokumen ini identitas
dibuka untuk pertama kalinya. Pertanyaan operator, "benarkah proposal baru lebih baik, atau
justru proposal lama?", dijawab di §3 berdasar bukti eksekusi, bukan berdasar siapa yang
membuat kandidat mana.

---

## 1. TABEL VERIFIKASI SKOR INDEPENDEN (eksekusi sesi ini, bukan kutip)

### 1a. Aritmetika skor EVAL-CMP dijumlahkan ulang

| Uji | Kandidat 1 (arsip) | Kandidat 2 (baru) | Status |
|---|---|---|---|
| Kriteria 1: 0+1+1+3 | = 5 | 9+6+7+5 = 27 | OK |
| Kriteria 2: 4,2+3+4 / 18+5+6 | = 11,2 | = 29 | OK |
| Kriteria 3: 5+4+4+6+3 / 6+5+5+6+3 | = 22 | = 25 | OK |
| Kriteria 4: 4+0+4+0 / 4+4+4+3 | = 8 | = 15 | OK |
| Total | 5+11,2+22+8 = **46,2** | 27+29+25+15 = **96** | OK |
| Bobot kriteria | 30+30+25+15 = 100 | sama | OK |
| Skor 2a = 18 x cocok/30 | 18 x 7/30 = 4,2 (7 COCOK) | 18 x 30/30 = 18 (30 COCOK) | OK |

### 1b. Anomali yang dicari (poin 3 tugas)

1. **"Kalah di kriteria akurasi tapi total menang": TIDAK ADA.** Kandidat 2 memimpin di
   4/4 kriteria, termasuk akurasi primer (29 vs 11,2). Kedua syarat protokol §3 (mayoritas
   kriteria + tidak kalah akurasi) terpenuhi oleh kandidat 2, ganda.
2. **Koreksi dari temuan AUD-CLAIM/AUDIT** (dua temuan, keduanya tidak membalik vonis):
   - `2b kandidat 2`: temuan **KOREKSI** kartu E_ML (klaim "kolom `ts_bin`/`lab_ts` kosong
     118.567 baris" pada stuck_k2 gagal direproduksi; `docs/V11_ML.md` §4.3) **tidak
     tercatat** di skor 2b EVAL-CMP. Jika diperhitungkan, 2b = 4 atau 5 (band rubrik "4-5 =
     satu-dua gagal" tetap berlaku); total kandidat 2 = 95 atau 96.
   - `2c kandidat 1`: EVAL memberi −2 karena angka `8.474.172` nihil di seluruh primer
     (rubrik harfiah: "nol angka tanpa sumber"), sedangkan AUD-CLAIM §D menyebut kandidat 1
     "0 angka karangan" (kesalahan = keliru kutip). Keduanya dapat dibela; jika 2c diberi
     penuh (6/6), total kandidat 1 = 48,2.
   - **Sensitivitas:** rentang kandidat 1 = 46,2..48,2; rentang kandidat 2 = 95..96. Pemenang
     tidak berubah di kedua ekstrem. Tidak ada koreksi yang mengubah vonis.

### 1c. Angka kunci diverifikasi ulang dengan eksekusi sendiri (15 kelompok, bukan kutip)

| # | Angka kunci | Sumber primer (eksekusi sesi ini) | Hasil |
|---|---|---|---|
| 1 | USROP 198.928 baris / 18 kolom / 12 sensor | `csv reader data/USROP_labeled.csv` | 198928 / 18 / 12, COCOK |
| 2 | 6 dataset latih total 292.954 baris | gzip+csv `scratch/v9_d1/datasets/*.csv.gz` | 23.922+35.906+56.495+5.555+52.509+118.567 = 292.954, COCOK |
| 3 | TSPP 52.905 baris | csv `data/bo_tspp/TSPP{1..4}.csv` | 21.120+8.499+12.533+10.753 = 52.905, COCOK |
| 4 | 884 label = 571/263/50 | json `data/volve/labels_curated_v2_log.json` | 571+263+50 = 884, COCOK |
| 5 | 37 fold LOWO | json `scratch/v9_d1/lowo_*.json` | 4+9+9+2+4+9 = 37, COCOK |
| 6 | n_features 55; SEED 42; 26 fold kampanye; `rerun_identical=False` | json `scratch/v9_e_ml/v9_e_ML_*_RESULTS.json` | 55 (4/4), 42 (4/4), 4+9+9+4 = 26, vib `rerun_identical=False`, COCOK |
| 7 | WITSML 10 CSV = 9.935.698; 8 CSV = 7.080.457 | `wc -l data/volve/witsml_parsed/*.csv` | 9.935.708 baris termasuk 10 header = 9.935.698 data; 8 CSV = 9.935.698−773.674−2.081.567 = 7.080.457; **8.474.172 nihil** |
| 8 | REGISTRY: 7 engine / 27 head / tier 12-13-2 / lapisan 5-11-9-2 / slot 0 / seed 42 | `importlib exec code/v9_i1_pipeline.py` | 7 engine; 27 head; PERINGATAN 12, TREN 13, BELUM 2; L0 5, L1 11, L2 9, L3 2; 0; 42, COCOK |
| 9 | hyd persistence P 0,615-0,899 | json `scratch/v9_eval_a/...` jalur `hyd_ki/persistence/per_fold` (n=9) | min 0,6145 maks 0,8986. Kandidat 2 baris 628 menulis 0,615-0,793 (SALAH), baris 2088 menulis 0,615-0,899 (BENAR) |
| 10 | em-dash U+2014 | `grep -o` kedua .md | arsip **14**, baru **0** |
| 11 | "8.474.172" vs "7.080.457" | `grep -c` kedua .md | arsip: 1 vs 0; baru: 0 vs 7 |
| 12 | penanda "11 klaim" / "27 head" | `grep -ci` kedua .md | arsip: 0 / 0; baru: 24 / 40 |
| 13 | 5 klaim salah kandidat arsip | `sed` baris 127/158/174/182 | semua terbaca: 8.474.172; Histogram-based Gradient Boosting; "rerun wajib identik"; "tujuh sumur"; "tujuh nilai lipatan" |
| 14 | parity md = ipynb | skrip `parity_check.py` milik PM-FINAL + negative control | arsip: 0 dari 191 baris substansial hilang; baru: 2 dari 2.538 hilang = satu baris tergabung dengan literal backslash-n (isi tetap ada, token angka hilang 0); negative control (md baru vs ipynb arsip) = 2.450 hilang, jadi tesnya terbukti bisa gagal |
| 15 | kehadiran angka checklist utama | `grep` kedua .md | 292.954: 0 vs 8; 52.905: 0 vs 7; 32,17405: 0 vs 12; "37 fold/lipatan": 0 vs 7 |

JSON primer: `scratch/v11/v11_pm_final.json`. Skrip: `verify_part1..5.py`,
`parity_check.py` (workspace task ini).

---

## 2. EVALUASI USER.TXT: PENILAIAN PIKIRAN (BAGIAN ii VONIS)

Sumber: `/mnt/d/Capstone 1(v2)/Evaluasi User.txt` (39 baris), dipetakan per butir di
`V11_PROTOCOL.md` §5. Penilaian di bawah berlaku untuk **pemenang (kandidat 2)**, dengan
pembanding kandidat 1 di tiap baris.

| Poin | Terpenuhi (kandidat 2)? | Bukti seksi (dibuka langsung di dokumen kandidat) | Pembanding kandidat 1 |
|---|---|---|---|
| (a) Lapisan A/B/C dipakai per tugas | **YA** | Bab 7 judul "Hasil A/B/C" (baris 2868); baris 320: metrik per blok "A (P/R/FAR/AUPRC/lift/CI vs baseline), B (TLead/B1-B4), C (C1-C4)"; Bab 8 §8.1 tiga lapisan penilaian; Bab 1 §1.3 tier/lapisan per head | YA di tingkat desain (§11.2/§13/§15.1) tetapi **tanpa angka metrik per lapisan** di dokumennya |
| (b) Baseline relevan per tugas, bukan satu universal | **YA** | Bab 6 §4 (baris 2675): definisi S9, baseline dihitung per tugas pada fold yang sama (persistence, canary-kedalaman, prevalence-random, rule ambang) + aturan lintas-bab #4 (baris 364) | Prinsip tegas (§12 "satu baseline universal ditolak") tetapi **tanpa penetapan baseline per daftar tugas** |
| (c) Bedakan jenis tugas | **YA** | Bab 1 §1.2 (baris 209-221): tabel 11 klaim dengan kolom "Jenis tugas" (deteksi kondisi, deteksi anomali, prediksi kejadian mendatang, prediksi onset, ranking); label dan baseline mengikuti jenis tugas (Bab 4/5) | Keempat jenis disebut (§5/§9.1) + kolom jenis tugas §15.1 memakai label turunan; **dangkal** |
| (d) Kemampuan + batas + kekuatan bukti, tanpa vonis biner | **YA** | baris 2877: "**BUKAN vonis LULUS/GAGAL** ... memenuhi untuk X / belum untuk Y / belum terukur"; Bab 7 §4 (baris 3083) "BELUM TERUKUR dipisah tegas dari gagal"; Bab 8 §9 batas jujur | **Unggul relatif di poin ini**: 0 kemunculan kata LULUS/GAGAL di seluruh 352 baris (hitungan AUDIT §3); kandidat 2 punya 3 "LULUS" pada tabel acceptance internal PM1, bukan vonis mesin |
| (e) Nilai di tingkat alat, bukan jumlah model lolos gate | **YA** | baris 2905: "vonis ditaruh di tingkat alat, bukan 'N model lolos gate'"; Bab 8 §7 hitungan alat 0 alarm + 3 peringatan + 2 bersyarat + 2 tren; Bab 8 §8.1-§8.2 cara membaca L0-L3 | Sintesis "7 dari 7 punya peran" + rekap 3/2/2/0 (§1, §15.2, §19) |

**Kesimpulan (b): kandidat 2 MEMENUHI kelima poin a-e Evaluasi User.txt**, masing-masing
dengan bukti seksi yang dibuka, bukan matriks klaim dokumennya. Skor kriteria 3 (25 vs 22)
konsisten dengan penilaian ini: selisihnya kecil karena kandidat 1 justru sangat patuh pada
inti larangan vonis biner.

---

## 3. VONIS TEGAS (TIGA BAGIAN)

### (i) MANA YANG LEBIH BAIK

**PROPOSAL BARU (V10, kandidat 2) lebih baik, dan BUKAN dengan selisih tipis.**
Selisih total 49,8 poin (96 vs 46,2) jauh di atas ambang selisih tipis protokol (< 5 poin);
kandidat 2 memimpin di 4 dari 4 kriteria dan tidak kalah di kriteria akurasi, sehingga
kedua syarat MENANG protokol §3 terpenuhi ganda. Koreksi sensitivitas terburuk (§1b) bahkan
menggeser angka menjadi 95..96 vs 46,2..48,2: pemenang tetap sama.

Kriteria penentu, diurutkan dari yang paling menentukan:
1. **Akurasi terhadap primer (+17,8):** kandidat arsip mengklaim 34 angka dengan 5 di
   antaranya terbukti salah menurut eksekusi saya juga (8.474.172 vs primer 7.080.457;
   "tujuh sumur"; "tujuh nilai lipatan"; nama model GB; "rerun wajib identik"), sedangkan
   kandidat baru hanya 1 klaim salah dari 48 (P persistence 0,615-0,793 di baris 628) plus
   1 tak-terverifikasi (481/329).
2. **Kedalaman teknis (+22):** kandidat arsip berisi **nol rumus** (hanya nama metode), 0/7
   skema label per kelas, hibrida disebut tanpa mekanisme; kandidat baru punya rumus eksak
   yang dicocokkan literal ke kode E_RULE/E_STAT, asersi anti-sirkular runtime, dan workflow
   hibrida berangka (hyd FP 2091→927 di 9/9 fold; ssi 26→7 di 7/7 fold).
3. **Struktur (+7):** kandidat arsip tidak pernah menjelaskan 11 klaim/27 head (0
   kemunculan, termasuk 0 penjelasan aritmetika 3x1+4x2), 14 em-dash dengan ≥6 pelanggaran;
   kandidat baru menjelaskan 7/11/27 tegas (27/27 baris tabel head cocok REGISTRY yang
   dieksekusi) dan 0 em-dash.

**Kejujuran terhadap kepentingan operator (poin 5 tugas):** ya, proposal baru lebih baik.
Vonis ini diambil dengan rubrik yang dikunci sebelum isi kandidat dibuka (anti-shopping),
dan kandidat arsip memang punya keunggulan nyata yang saya akui: 0 kata LULUS/GAGAL,
kejujuran "0 alarm otomatis", ringkas (352 baris), dan prinsip metodologis yang benar.
Keunggulan itu kalah karena proposal teknis dituntut punya rumus operasional dan angka yang
benar terhadap primer, dan di dua tuntutan itu kandidat arsip gagal secara terukur.

### (ii) APAKAH PEMENANG MEMENUHI EVALUASI USER.TXT

**YA, seluruh poin a-e terpenuhi** (tabel bukti seksi lengkap di §2):
- (a) YA: lapisan A/B/C dipakai menilai dengan metrik per blok (Bab 7, baris 320).
- (b) YA: baseline berbeda per tugas lewat S9 + aturan lintas-bab (Bab 6 §4).
- (c) YA: jenis tugas dibedakan tegas di tabel 11 klaim, label & baseline mengikuti jenis.
- (d) YA: kemampuan + batas + kekuatan bukti ada per klaim; "belum terukur" dipisah dari
  "gagal"; vonis biner ditolak eksplisit (baris 2877, Bab 7 §4).
- (e) YA: nilai dinilai di tingkat alat (hitungan alat + peta L0-L3), larangan "N model lolos
  gate" ditulis eksplisit; validitas data dan uji temporal tetap dituntut (aturan #2 dan #5).

### (iii) KELEMAHAN PEMENANG YANG MASIH PERLU DIPERBAIKI

1. **Klaim KOREKSI stuck_k2** ("kolom `ts_bin`/`lab_ts` kosong untuk 118.567 baris, verifikasi
   baca gzip mentah") gagal direproduksi dua parser di dua path dan hash dataset tercatat
   tidak cocok file sekarang (`V11_ML.md` §4.3). Hapus klaim verifikasi langsungnya atau
   beri anotasi historis lengkap dengan bukti hash versi lama.
2. **Inkonsistensi internal angka**: baris 628 menulis "P 0,615-0,793" (salah; primer
   0,6145-0,8986) sedangkan baris 2088 menulis "0,615-0,899" (benar). Samakan ke 0,615-0,899.
3. **Label provenance kabur**: sub-bab berlabel "Bukti empiris V9" memuat angka kampanye V8
   (hyd ΔB 7/7, bit_wear persistence 4/4). Angkanya benar, sumber versinya harus dianotasi
   per butir (`V11_RND.md` §3.1-3.2).
4. **Kode sitasi menggantung**: `[A-19]..[A-21]` dipakai di BAGIAN C (baris 3504/3514) tetapi
   tidak ada di tabel sitasi. Tambahkan ke tabel rujukan.
5. **Artefak tampilan .ipynb**: satu sel memuat literal backslash-n pada baris yang di .md
   terpisah (md baris 648-649). Isi tidak hilang, tetapi pembaca notebook melihat "\n" di
   tengah kalimat. Perbaiki selnya.
6. **Angka 481/329** ("kandidat onset terverifikasi") tidak punya primer data di luar kutipan
   dokumen (`AUD-CLAIM` C.2 K2-X15). Tandai "belum terverifikasi" atau lampirkan primernya.
7. **Pembulatan FAR**: "FAR_t 32-111/24jam" (baris 628) berasal dari dokumen sumber, tetapi
   JSON primer berakhir di 109,69. Samakan dengan primer agar 2b steril dari sengketa.
8. **Keterbacaan**: 3.557 baris sangat padat untuk pembaca dosen; ringkasan eksekutif bab
   dan pemisahan lampiran data akan menaikkan keterbacaan tanpa kehilangan angka.
9. **Minor konsistensi** (temuan DATA2): `MIN_OBS=5` hyd tidak eksplisit; istilah "11 kanal
   MWD" (seharusnya surface/depth); §3.5 bit_wear memuat 4 dari 8 kolom primer.

---

## 4. KEPUTUSAN MENANG MENURUT PROTOKOL §3 (PENERAPAN LITERAL)

| Syarat MENANG (protokol §3) | Hasil | Dasar skor EVAL-CMP terverifikasi |
|---|---|---|
| 1. Unggul di mayoritas kriteria (>= 3 dari 4) | **TERPENUHI** oleh kandidat 2 (4/4) | K1: 5 / 11,2 / 22 / 8 vs K2: 27 / 29 / 25 / 15 |
| 2. Tidak kalah di kriteria 2 (akurasi) | **TERPENUHI** oleh kandidat 2 (29 >= 11,2) | 2a 18 vs 4,2; 2b 5 vs 3; 2c 6 vs 4 |
| Kandidat yang memenuhi kedua syarat | **Kandidat 2 = PROPOSAL BARU (V10)** | Kandidat 1 memenuhi nol syarat; SERI tidak terjadi |

---

## 5. WHAT-IF-ORACLE: ENAM CABANG VONIS

| Cabang | Prob. | Narasi | Pengaruh ke vonis |
|---|---|---|---|
| Ω Best | 15% | Temuan kartu tim 100% akurat dan seluruh "belum diverifikasi" ternyata positif bagi kandidat baru | Vonis menguat; selisih melebar |
| **α Likely** | **55%** | Kedua koreksi kecil (§1b) terkonfirmasi; seluruh angka kunci berdiri | **Vonis berlaku: kandidat 2 menang 95..96 vs 46,2..48,2** |
| Δ Worst | 15% | Semua keputusan sub-kriteria yang diperselisihkan dibalik pro arsip (2c=6, 2b K1=6, 1d K1=6) | Total arsip 48,2 sampai ~56; tetap kalah jauh dari 95 |
| Ψ Wild card | 8% | Output execution cell .ipynb atau hasil training ulang mengandung angka besar yang mengubah penilaian | Tidak teruji (§7); protokol §6.4 hanya mengikat sel markdown, jadi dampaknya terbatas pada 4c |
| Φ Contrarian | 5% | Rubrik dianggap bias: checklist 30 angka menghukum dokumen yang memang tidak mengutip inventaris data | Ditolak: 2b/2c memakai penyebut klaim nyata (bukan ketidakhadiran), kriteria 3 dan 4 yang bebas "kutipan angka" juga dimenangkan kandidat baru, dan kalah 4/4 kriteria bukan wajah bias satu kriteria |
| ∞ Second order | 2% | Kemenangan dokumen besar membuat proses selanjutnya lambat/ditolak dosen | Risiko nyata untuk keterbacaan, bukan untuk vonis; ditangani perbaikan (iii).8 |

Robust action di semua cabang: perbaiki 9 kelemahan §3(iii) sebelum dokumen dipakai
berkarya.

---

## 6. CONSCIOUSNESS-COUNCIL: LIMA ARKETIPE MENEKAN VONIS

🎭 **Empiricist**: Posisi: vonis = 46,2 vs 96, dan 15 kelompok angka dihitung ulang dari
primer; tidak ada yang dekat. Risiko yang ia lihat: satu klaim kandidat baru (stuck_k2) sudah
KOREKSI, jadi "sempurna" itu salah. Wawasan tak terduga: bahkan dengan memberi kandidat arsip
seluruh poin yang diperselisihkan, ia tetap kalah telak, jadi vonis tidak bergantung pada
penilaian subjektif mana pun.

🎭 **Contrarian**: Posisi: "rubrik ini memang dibuat oleh tim yang juga membuat kandidat
baru; mungkin menang karena rubrik mencerminkan kekuatannya." Risiko: konfirmasi bias
in-house. Jawaban setelah diuji: rubrik dikunci sebelum isi kandidat dibuka (PROTOCOL §8.1),
kriteria 3 (Evaluasi User.txt) dan 4 (struktur) dinilai dari instrumen eksternal milik
operator, dan kandidat arsip tetap kalah di keduanya; kontrarian tidak menemukan mekanisme
bias yang bekerja, hanya asumsinya.

🎭 **Strategist**: Posisi: menyarankan menerima kemenangan kandidat baru TANPA membersihkan
9 kelemahannya adalah kemenangan pirotik; kelemahan no. 1 (klaim verifikasi langsung yang
gagal) adalah yang paling merusak kredibilitas jika ditemukan penguji. Risiko: vonis benar
lalu dokumen runtuh di sidang. Permainan keduanya: umumkan menang + perbaiki sekarang.

🎭 **Pragmatist**: Posisi: kandidat arsip 352 baris enak dibaca dosen, kandidat baru 3.557
baris berat; "yang lebih baik" untuk tugas akhir bisa berarti yang bisa dipertahankan di
sidang. Ketegangan nyata dengan Empiricist. Titik temu: keterbacaan masuk daftar perbaikan
(§3(iii).8), bukan sebagai kriteria baru (anti-shopping: menambah kriteria setelah skor
dibuka dilarang protokol §3).

🎭 **Ethicist**: Posisi: kejujuran menuntut vonis menyebut keunggulan arsip (0 kata
LULUS/GAGAL, "0 alarm" jujur) dan kelemahan pemenang (klaim stuck_k2), bukan sekadar
kemenangan. Risiko yang ia lihat: penilaian tim terhadap hasil kerjanya sendiri. Pengendali:
sensitivitas §1b ditulis eksplisit sehingga pembaca bisa membalik koreksi dan tetap sampai
hasil sama.

**Sintesis dewan:** konvergensi pada pemenang (semua arketipe menyetujui kandidat 2 di atas
data yang sama); ketegangan inti = keunggulan kejujuran-biner arsip vs kelengkapan bukti
kandidat baru, dan ketegangan itu diselesaikan oleh instrumen operator sendiri (poin a-e
mensyaratkan angka kemampuan, bukan hanya penolakan vonis). Blind spot dewan: tidak ada yang
menguji isi output cell .ipynb (masuk §7). Keyakinan: **tinggi**.

---

## 7. BELUM DIVERIFIKASI (eksplisit, verification-mandatory #3)

1. Output execution cell .ipynb kedua kandidat tidak dibaca (protokol §6.4 hanya mengikat
   isi sel markdown).
2. Kampanye ML tidak dilatih ulang; determinisme dibaca dari JSON `determinism_check`.
3. Angka "481/329" (kandidat baru) tidak punya primer data di luar kutipan dokumen.
4. Klaim historis "kolom stuck_k2 kosong" tidak bisa dipastikan: file dataset semasa run
   (hash `a8307db3...`) sudah tidak ada di disk (`V11_ML.md` §10.2).
5. Sitasi DOI eksternal tidak dibuka ulang di sesi ini (cakupan kartu R1).
6. Seluruh rumus Bab 5/6 dicocokkan literal oleh kartu STAT/HYB per slice; PM-FINAL
   membaca sampel langsung (qcut desil, persistence ŷ(t)=y(t−W), S9) tetapi tidak mengulang
   seluruhnya dari nol.

---

## 8. RINGKASAN EKSEKUTIF (5 BARIS)

1. Pemenang: **PROPOSAL BARU (V10)**, bukan proposal arsip; skor 96 vs 46,2 (selisih 49,8,
   bukan selisih tipis), memimpin 4/4 kriteria dan lolos kedua syarat MENANG protokol §3.
2. Verifikasi mandiri: 15 kelompok angka kunci dihitung ulang dari primer (USROP, dataset,
   TSPP, label, fold, REGISTRY, WITSML, persistence P, em-dash, parity) semuanya konsisten
   dengan skor EVAL-CMP; aritmetika skor dijumlahkan ulang dan cocok.
3. Dua koreksi ditemukan (KOREKSI stuck_k2 tak masuk 2b; status 2c arsip dapat dibela
   dua arah), keduanya tidak membalik vonis pada uji sensitivitas terburuk (95..96 vs
   46,2..48,2).
4. Pemenang MEMENUHI seluruh poin a-e Evaluasi User.txt dengan bukti seksi; poin (d) justru
   lebih dipegang kandidat arsip (0 kata LULUS/GAGAL), tetapi a-c yang menuntut angka dan
   baseline per tugas jauh dipegang kandidat baru.
5. Sisa perbaikan pemenang: 9 butir konkret (klaim stuck_k2, angka baris 628, anotasi
   provenance V8, kode [A-19..A-21], artefak backslash-n, 481/329, pembulatan FAR,
   keterbacaan, minor konsistensi).

*Selesai V11-PM_FINAL (`t_0fe5b8fa`): anonimisasi dibuka, skor diverifikasi + sensitivitas,
pemenang = proposal baru (V10) dengan selisih 49,8, Evaluasi User.txt dinilai a-e dengan
bukti seksi, 9 perbaikan sisa, JSON primer `scratch/v11/v11_pm_final.json`.*
