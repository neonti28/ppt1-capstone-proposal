# V11-EVAL: SKOR BLIND DUA KANDIDAT (RUBRIK PM-0) + PERBANDINGAN PER KRITERIA

Task: `t_b15f4c50` [Evaluator] · Board: `capstone-v11-vs` · 2026-10-15 (WIB).
Peran: menilai dua kandidat TANPA menyimpulkan identitas versinya (blind), memakai rubrik
terkunci PM-0 `docs/V11_PROTOCOL.md` §2, lalu membandingkan skor per kriteria. Penetapan
MENANG/SERI final mengikuti protokol §3 dan tetap kewenangan PM-FINAL; bagian ini hanya
menyatakan pemimpin + selisih poin per kriteria, dengan rujukan bukti.

> Riset pendahuluan: `scientific-critical-thinking` - data (angka primer/tabel tim) dipisah
> dari interpretasi (skor); tiap sub-kriteria punya falsifier berupa angka; kekuatan bukti
> diberi status (eksekusi langsung vs kutipan kartu tim); standar diterapkan sama untuk
> kedua kandidat.
> Riset pendahuluan: `verification-mandatory` - seluruh angka kunci diuji ulang dengan
> eksekusi mandiri (grep/hitung pada file primer) sebelum masuk skor, bukan sekadar kutip
> kartu tim; daftar "belum diverifikasi" ditulis eksplisit di §8; temuan inkonsistensi
> internal kandidat 2 (baris 628 vs 2088) dilaporkan apa adanya.
> Riset pendahuluan: `statistical-analysis` - bobot sub-kriteria dipakai persis PM-0 tanpa
> diubah; skor 2a dihitung dari rumus protokol 18 × (cocok/30), bukan penilaian subjektif;
> angka kampanye dinilai per anotasi kampanye; tidak ada rata-rata lintas kampanye.
> Riset pendahuluan: `sequentialthinking` (sequ-mcp, 4 pikiran, 4/4 sukses): inventaris
> bahan + rumus skor -> skoring kriteria 1 -> skoring kriteria 2/3/4 + gate anonimisasi ->
> keputusan pelaporan & output.

---

## 0. PETA KANDIDAT (kode opaque; identitas versi tidak dipakai sebagai dasar)

| Kode | File .md | File .ipynb (pasangan) |
|---|---|---|
| Kandidat 1 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.v3_arsip.md` (352 baris) | `...v3_arsip.ipynb` |
| Kandidat 2 | `/mnt/d/Capstone 1(v2)/docs/ML_PROJECT_PROPOSAL_TECHNICAL_DESIGN.md` (3.557 baris) | `...TECHNICAL_DESIGN.ipynb` |

Path diperlakukan sebagai kode kandidat (protokol §1.2). Kata di dalam path tidak ditafsirkan
sebagai penanda kualitas; jumlah baris/ukuran/mtime tidak dipakai sebagai argumen penilaian.

**Bias disclosure (protokol §1.6):** badan kartu tugas memuat pemetaan kedua path, sehingga
penilai mengetahui pasangan file mana yang saling bersaing. Penilaian di bawah berpatokan
pada rubrik tertulis PM-0 dan bukti eksekusi/kartu tim, bukan pada penanda apa pun di path.

**Bahan skor (dibaca semua):** `docs/V11_PROTOCOL.md`, `V11_AUDIT.md`, `V11_AUD_CLAIM.md`,
`V11_DATA1.md`, `V11_DATA2.md`, `V11_ML.md`, `V11_STAT.md`, `V11_HYB.md`, `V11_RND.md`
plus pembacaan langsung kedua kandidat dan verifikasi grep mandiri (§7).

---

## 1. TABEL SKOR PER SUB-KRITERIA (bobot persis PM-0 §2)

| Krit. | Sub | Bobot | Kandidat 1 | Kandidat 2 | Pemimpin (selisih) |
|---|---|---|---|---|---|
| 1 Kedalaman teknis | 1a rumus per engine/head | 10 | **0** | **9** | K2 (+9) |
| | 1b labeling + anti-sirkular | 7 | **1** | **6** | K2 (+5) |
| | 1c workflow hybrid + interaksi | 7 | **1** | **7** | K2 (+6) |
| | 1d bukti per klaim | 6 | **3** | **5** | K2 (+2) |
| | **Jumlah** | **30** | **5** | **27** | **K2 (+22)** |
| 2 Akurasi primer | 2a checklist 30 angka (18 × cocok/30) | 18 | **4,2** | **18,0** | K2 (+13,8) |
| | 2b angka luar checklist | 6 | **3** | **5** | K2 (+2) |
| | 2c nihil angka karangan | 6 | **4** | **6** | K2 (+2) |
| | **Jumlah** | **30** | **11,2** | **29** | **K2 (+17,8)** |
| 3 Evaluasi User.txt | 3a lapisan A/B/C | 6 | **5** | **6** | K2 (+1) |
| | 3b baseline per tugas | 5 | **4** | **5** | K2 (+1) |
| | 3c jenis tugas | 5 | **4** | **5** | K2 (+1) |
| | 3d kemampuan+batas+bukti, tanpa vonis biner | 6 | **6** | **6** | seri (0) |
| | 3e nilai tingkat alat | 3 | **3** | **3** | seri (0) |
| | **Jumlah** | **25** | **22** | **25** | **K2 (+3)** |
| 4 Struktur | 4a outline | 4 | **4** | **4** | seri (0) |
| | 4b penjelasan 7/11/27 | 4 | **0** | **4** | K2 (+4) |
| | 4c md = ipynb | 4 | **4** | **4** | seri (0) |
| | 4d aturan em-dash | 3 | **0** | **3** | K2 (+3) |
| | **Jumlah** | **15** | **8** | **15** | **K2 (+7)** |
| **TOTAL** | | **100** | **46,2** | **96** | **K2 (+49,8)** |

Selisih total 49,8 poin: **bukan selisih tipis** (ambang protokol < 5 poin).
Total hanyalah pelengkap; penentu menang = syarat mayoritas kriteria + tidak kalah di
akurasi (protokol §3): penerapannya ada di PM-FINAL.

---

## 2. ANALISIS KRITERIA 1: KEDALAMAN TEKANIS (30)

**Skor: Kandidat 1 = 5 · Kandidat 2 = 27 · Pemimpin: Kandidat 2 (+22).**

### 2a. Rumus/definisi operasional (10): K1: 0 · K2: 9

- **Kandidat 1, kelemahan fatal:** bacaan penuh 352 baris oleh V11_AUDIT menemukan **nol
  rumus/definisi operasional**; yang ada hanya nama metode (AUDIT §8, skor 1a = 0/10).
  E_STAT mengonfirmasi pada cakupannya: "Rumus per engine 0/4" (STAT §6). E_HYB:
  definisi rule per kelas 0/5 (HYB §6).
  *Bukti angka: 0 rumus; 0/4 engine E_STAT; 0/5 rule E_HYB.*
- **Kandidat 1, keunggulan (kecil):** nama keluarga metode dipilih tetap konsisten dengan
  primer (median/MAD+persistence utk hyd, change-point utk tool_wear = benar vs kode,
  STAT §6; HYB §3).
- **Kandidat 2, keunggulan:** seluruh keluarga metode punya rumus eksak yang dicocokkan
  literal ke kode: 5 rumus rule + persistence + hibrida cocok 100% (HYB §4.1-4.3 →
  1a = 10/10 pada cakupannya); 4/4 engine statistik dengan notasi matematika + sitasi
  baris kode yang diperiksa literal (STAT §6); kontrak RF/GB/LR + CI95 bootstrap +
  `UNDERPOWERED_POS=30` di Bab 4 (E_ML §2-§3).
- **Kandidat 2, kelemahan:** sebagian rumus hanya dijelaskan dengan kata, bukan notasi
  (mis. kuantil FAR; STAT §6) → dikurangi 1 → **9/10**.

### 2b. Labeling per kelas + anti-sirkularitas (7): K1: 1 · K2: 6

- **Kandidat 1:** skema label per kelas = **0/7 tertulis**; yang ada satu kalimat
  anti-sirkularitas (AUDIT baris 137; D2 §1: semua kelas "tidak ditulis") → termasuk
  kategori "dangkal" (rubrik 1-3) → **1/7**.
  Catatan: frasa "MSE/SSI sbg fitur bila relevan" tidak selaras dengan larangan primer
  per kelas (D2 §7).
- **Kandidat 2:** skema per kelas lengkap dan cocok kode (7 kelas: VIB 32,17405; SSI
  `(max-min)/(2·mean)`; SHK ≥1; stuck onset H=10 mnt; hyd `|z|>2` ekuivalen 0,6745;
  D2 §1) + asersi runtime anti-sirkular di kode yang dikutip (E_ML: assert baris 192-193)
  + aturan inblock/strict-past. Celah minor: `MIN_OBS=5` tidak disebut eksplisit (D2 §1)
  → **6/7**.

### 2c. Workflow hybrid + interaksi antar-komponen (7): K1: 1 · K2: 7

- **Kandidat 1:** hibrida hanya disebut dua kali (baris 90, 159) tanpa rumus h(t), tanpa
  langkah workflow, tanpa angka pemangkasan FP (AUDIT §1 poin (e)) → "disebut tanpa
  mekanisme" → **1/7**.
- **Kandidat 2:** workflow 4 langkah + mekanisme "dua pemotong" + pemangkasan FP
  berangka (hyd 2091→927 = −55,7% di 9/9 fold; ssi 26→7 = −73,1% di 7/7 fold) + trade-off
  recall + kasus degenerasi (HYB §4.3 → 1c = 7/7) → **7/7**.

### 2d. Bukti per klaim (6): K1: 3 · K2: 5

- **Kandidat 1:** sitasi internal [A-1]..[A-13] + angka rekap tier + kutipan audit
  "121 klaim" ada, tetapi (i) klaim kemampuan per mesin tanpa angka inline, (ii) angka
  tingkat pemakaian menempel ke kode [A-19]/[A-20] yang **menggantung** (tabel sitasi
  hanya [A-1]..[A-13]; RND §4) → **3/6**.
- **Kandidat 2:** tiap bab punya seksi traceability; ketujuh engine menaut angka/rujukan
  primer; "tidak ditemukan pemilihan metode tanpa bukti" (RND §4). Kelemahan: dua label
  provenance kabur (angka V8 di sub-bab berlabel V9; RND §3.1-3.2) dan kode
  [A-19]..[A-21] juga menggantung di BAGIAN C (RND §4) → **5/6**.

---

## 3. ANALISIS KRITERIA 2: AKURASI TERHADAP PRIMER (30)

**Skor: Kandidat 1 = 11,2 · Kandidat 2 = 29 · Pemimpin: Kandidat 2 (+17,8).**
Sumber utama: V11_AUD_CLAIM (ledger 60 klaim angka, semua dihitung ulang dari primer
dengan 17 skrip eksekusi), diperkuat V11_DATA1/V11_DATA2/V11_ML/V11_STAT/V11_HYB.

### 2a. Checklist 30 angka (18): K1: 4,2 · K2: 18,0

Rumus protokol: skor = 18 × (jumlah cocok / 30); ketidakhadiran = tidak cocok.

- **Kandidat 1: 7 cocok + 2 parsial + 1 salah + 20 tidak hadir → 18 × 7/30 = 4,2.**
  Cocok: butir 1 (7 engine), 6 (alarm otomatis 0), 10 (seed 42), 11 (198.928),
  12 (884), 15 (55 fitur), 29 (rekap 0/3/2/2). Salah: butir 19 ("8.474.172 baris";
  primer 7.080.457). Parsial (20, 30) tidak dihitung cocok per rubrik.
  *Verifikasi mandiri: grep `8.474.172` = 1 kemunculan, `7.080.457` = 0;
  `292.954`/`52.905`/`32,17405` = 0 kemunculan.*
- **Kandidat 2: 30 cocok, 0 salah, 0 tidak hadir → 18 × 30/30 = 18,0.**
  *Verifikasi mandiri: `7.080.457` = 7, `292.954` = 8, `52.905` = 7,
  `32,17405` = 12, `37 fold|37 lipatan` = 7, `8.474.172` = 0 kemunculan.*

### 2b. Angka di luar checklist (6): K1: 3 · K2: 5

- **Kandidat 1:** 15 klaim ekstra, **5 SALAH**: 8.474.172 (primer 7.080.457; nihil di
  seluruh primer), "tujuh sumur LOWO" (primer 9 wellbore), "tujuh nilai lipatan"
  (primer 37 fold), "Histogram-based Gradient Boosting" (kode
  `GradientBoostingClassifier`), "rerun wajib identik" (JSON `rerun_identical=False`);
  + 1 tak-terverifikasi (Brier&ECE). 5 dari 15 gagal = kategori "banyak gagal"
  (rubrik 2b) → **3/6**. (AUD-CLAIM §C.1/§D; E_ML temuan 4.)
- **Kandidat 2:** 15 klaim ekstra, **1 SALAH**: "P 0,615–0,793" (primer 0,615–0,899;
  0,793 = fold F-9), 1 tak-terverifikasi (481/329), 2 didukung; ditambah dua isu minor
  kartu tim (atribusi "32–111" yang di JSON 130,6–510,6 pada STAT D1; path katalog
  tanpa `/external/` pada D1) = "satu-dua gagal" → **5/6**.
  *Verifikasi mandiri: baris 628 menulis 0,615–0,793 sedangkan baris 2088 dokumen yang
  sama menulis 0,615–0,899 → inkonsistensi internal; klaim tetap 1 yang salah.*

### 2c. Nihil angka karangan (6): K1: 4 · K2: 6

- **Kandidat 2:** ledger AUD-CLAIM §D: 0 angka tanpa sumber; seluruh angka memuat
  rujukan primer (bahkan 481/329, yang punya sumber kutipan dokumen meski tak bisa
  dihitung ulang) → **6/6**.
- **Kandidat 1:** tidak ada pola fabrikasi angka baru (kesalahan = keliru kutipan),
  tetapi rubrik 2c berbunyi "nol angka **tanpa sumber**": angka 8.474.172 terbukti
  nihil di seluruh primer (D1 §4: enumerasi seluruh 45 pasangan 8-dari-10 file tidak
  menghasilkan angka itu; AUDIT §7) = 1 angka tanpa sumber → −2 → **4/6**.

---

## 4. ANALISIS KRITERIA 3: KEPATUHAN EVALUASI USER.TXT (25)

**Skor: Kandidat 1 = 22 · Kandidat 2 = 25 · Pemimpin: Kandidat 2 (+3).**
Bukti utama: V11_AUDIT §2 (kartu yang membaca `Evaluasi User.txt` 39 baris dan membuka
seksi yang ditunjuk); kartu domain (STAT/HYB/E_ML) mencatat skor a-e mereka provisional
dan menyerahkan ke pembacaan ini.

| Poin | K1 | K2 | Dasar (AUDIT §2) |
|---|---|---|---|
| (a) lapisan A/B/C | 5/6 | 6/6 | K1: ketiga lapisan ada & dipakai di tingkat desain (§11.2/§13/§15) tetapi tanpa angka metrik per lapisan di dokumen. K2: Bab 7 hasil A/B/C + metrik per blok (baris 320) + tier/lapisan per head (baris 260-261). |
| (b) baseline per tugas | 4/5 | 5/5 | K1: prinsip tegas (canary pembanding wajib, persistence status-quo; "satu baseline universal ditolak") tapi tanpa penetapan baseline per daftar tugas; HYB mencatat komponen baseline tidak lengkap (tanpa prevalence-random/canary-depth). K2: Bab 6 §4 empat baseline berbeda per tugas + aturan lintas-bab #4. |
| (c) jenis tugas | 4/5 | 5/5 | K1: keempat jenis disebut (§5/§9.1) + kolom jenis tugas §15.1 memakai label turunan. K2: tabel jenis tugas per 11 klaim (Bab 1 §1.2) dengan label & baseline mengikuti jenis. |
| (d) kemampuan+batas+bukti, tanpa vonis biner | 6/6 | 6/6 | K1: §15.1 semua 7 mesin punya Tingkat + Batas; penolakan vonis eksplisit §11.2; 0 kata LULUS/GAGAL (hitung kata AUDIT §3). K2: "belum terukur" dipisah tegas (baris 3083), "BUKAN vonis LULUS/GAGAL" (baris 2877); 3 "LULUS" = acceptance outline internal PM1, bukan vonis mesin. |
| (e) nilai tingkat alat | 3/3 | 3/3 | K1: sintesis "7 dari 7 punya peran" + rekap 3/2/2/0. K2: hitungan alat 0 alarm + 3 peringatan + 2 bersyarat + 2 tren + larangan "N model lolos gate" (baris 2905). |

Kandidat 1 unggul pada keteguhan penolakan vonis biner (0 kemunculan kata LULUS/GAGAL di
seluruh dokumennya), tetapi kalah pada kedalaman pelaksanaan a-c (tanpa angka lapisan,
tanpa baseline per tugas terpetakan, jenis tugas memakai label turunan).

---

## 5. ANALISIS KRITERIA 4: STRUKTUR & KETERBACAAN (15)

**Skor: Kandidat 1 = 8 · Kandidat 2 = 15 · Pemimpin: Kandidat 2 (+7).**

| Sub | K1 | K2 | Bukti |
|---|---|---|---|
| 4a outline | 4 | 4 | K1: daftar isi 19 seksi, BAGIAN A/B/C (43 heading); K2: 8 bab + daftar isi, 208 heading (AUDIT §8). |
| 4b penjelasan 7/11/27 | 0 | 4 | K1: "11 klaim" = 0, "27 head" = 0, `4+4+4+6+4+2+3` = 0 (grep mandiri + AUDIT §6) → rubrik "salah atau tidak ada" = 0. K2: Bab 1 §0-§1.4 penjelasan tegas; tabel 27 head cocok **27/27** vs REGISTRY yang dieksekusi; 0 kontradiksi lintas bab (AUDIT §6). |
| 4c md = ipynb | 4 | 4 | K1: 0 dari 255 baris substansial hilang; 8 baris ekstra = blok arsip berlabel non-narasi. K2: 0 dari 2.829 baris substansial hilang; kehadiran 30 butir checklist identik antar format; 1 artefak kosmetik literal backslash-n (bukan selisih angka/klaim/struktur) dicatat (AUDIT §5; AUD-CLAIM §F; RND §5). |
| 4d em-dash | 0 | 3 | K1: 14 em-dash, **≥6 pelanggaran penghubung klausa** (baris 62, 136, 182, 352 + 8 gaya label berulang) → rubrik ≥4 pelanggaran = 0. K2: **0** em-dash di .md maupun sel .ipynb; 225 en-dash semuanya rentang/sel kosong → 3. *Grep mandiri U+2014: K1 = 14, K2 = 0 (cocok dengan JSON AUDIT).* |

---

## 6. PENILAIAN .IPYNB (paket wajib; selisih isi = cacat 4c)

Ulangi penilaian format .ipynb per kandidat (protokol §6):

| Uji (eksekusi kartu tim, silang-diverifikasi 4 kartu independen) | Kandidat 1 .ipynb | Kandidat 2 .ipynb |
|---|---|---|
| Baris substansial .md hilang di .ipynb | **0** (dari 255) | **0 substantif** (dari 2.829; 2 baris tergabung oleh literal backslash-n) |
| Kehadiran 30 butir checklist md vs ipynb | **identik** (7/30 di kedua format) | **identik** (30/30 di kedua format) |
| Token angka md yang hilang di ipynb | **0** (224 vs 226 token; +2 = blok arsip) | **0** (7.510 vs 7.512; +2 = blok arsip + artefak backslash-n) |
| Cell code vs angka markdown | konsisten (tidak ada angka code yang menabrak markdown) | konsisten |
| **Skor 4c (md & ipynb)** | **4** | **4** (catatan: 1 artefak kosmetik tampilan) |

**Tidak ada cacat 4c (selisih substantif) di kedua kandidat**; skor 4c penuh untuk
kedua paket; artefak kosmetik kandidat 2 dicatat, bukan dikurangi (tidak mengubah angka,
klaim, tabel, atau struktur). Sub-kriteria lain pada .ipynb mengikuti .md karena isi
substantifnya identik (satu paket); karenanya total .ipynb = total .md per kandidat:
**K1 = 46,2 · K2 = 96**.

---

## 7. VERIFIKASI MANDIRI (eksekusi sesi ini, bukan kutipan)

| Tes | Perintah/objek | Hasil |
|---|---|---|
| Em-dash U+2014 | `grep -o '—'` kedua .md | K1 = **14**, K2 = **0** (cocok JSON `emdash_counts.json`) |
| Penanda 11 klaim / 27 head | `grep -c -F` | K1 = 0/0; K2 = 18/34 |
| Sebaran 27 head | `grep -c -F '4+4+4+6+4+2+3'` | K1 = 0; K2 = 5 |
| Checklist kunci | grep pola per butir | K1: `8.474.172`=1, `7.080.457`=0, `292.954`=0, `52.905`=0; K2: `7.080.457`=7, `292.954`=8, `52.905`=7, `32,17405`=12, `8.474.172`=0 |
| Klaim keliru K1 | grep literal | "tujuh nilai lipatan" + "tujuh sumur" baris 182; "Histogram-based Gradient Boosting" baris 158 |
| Klaim keliru K2 + inkonsistensi internal | grep `0,615|0,899|0,793` | baris 628 = 0,615–0,793 (SALAH); baris 2088 = 0,615–0,899 (benar) |
| JSON primer skor (S6) | ditulis sebelum dokumen ini | `scratch/v11/v11_eval_scorecard.json` |

Kartu tim yang diandalkan beserta status buktinya: AUD-CLAIM (recompute 17 skrip),
AUDIT (8 skrip eksekusi), DATA1/D2 (hitung ulang disk), ML (286 sel angka tabel),
STAT (±240 sel + re-run modul), HYB (recompute penuh E_RULE), RND (pembukaan sitasi).

---

## 8. BELUM DIVERIFIKASI (eksplisit, verification-mandatory #3)

1. Output execution cell .ipynb kedua kandidat tidak dibaca (protokol §6.4 hanya mengikat
   isi sel markdown; AUDIT §9.4).
2. Kampanye ML tidak dilatih ulang; determinisme dibaca dari JSON `determinism_check`
   (E_ML §10).
3. Angka "481/329 kandidat onset terverifikasi" (kandidat 2) tak punya primer data di
   luar kutipan dokumen (AUD-CLAIM §C.2 K2-X15).
4. Kelengkapan literal 100% rumus Bab 5/6 vs kode E_STAT/E_RULE: diuji oleh STAT/HYB per
   slice; penilai ini tidak mengulang seluruhnya dari nol.
5. Sitasi DOI eksternal: dibuka sebagian oleh kartu R1; tidak dibuka ulang di sini.

---

## 9. KESIMPULAN PER KRITERIA (pemimpin + selisih; menang final = PM-FINAL)

| Kriteria | K1 | K2 | Pemimpin | Selisih |
|---|---|---|---|---|
| 1. Kedalaman teknis (30) | 5 | 27 | Kandidat 2 | +22 |
| 2. Akurasi terhadap primer (30) | 11,2 | 29 | Kandidat 2 | +17,8 |
| 3. Kepatuhan Evaluasi User.txt (25) | 22 | 25 | Kandidat 2 | +3 |
| 4. Struktur & keterbacaan (15) | 8 | 15 | Kandidat 2 | +7 |
| **Total (pelengkap)** | **46,2** | **96** | Kandidat 2 | **+49,8 (bukan selisih tipis)** |

- Kandidat 2 memimpin di **4 dari 4 kriteria** dan **tidak kalah di kriteria akurasi**
  (malah unggul 17,8 poin), sehingga kedua syarat protokol §3 terpenuhi dari sudut skor ini;
  penetapan MENANG/SERI tetap keputusan PM-FINAL setelah membuka pemetaan (protokol §1.5).
- Satu-satunya sub-kriteria yang imbang sempurna: 3d, 3e, 4a, 4c. Kandidat 1 tidak
  memimpin sub-kriteria mana pun; keunggulan relatifnya ada pada 3d (0 kata
  LULUS/GAGAL) yang imbang dengan kandidat 2.
- Kandidat 1 kehilangan poin terbesar pada 2a (−13,8: 20 dari 30 angka kunci tidak
  hadir), 1a (−9: tanpa rumus), dan 4b (−4: 11 klaim/27 head tak pernah dijelaskan).

*Selesai V11-EVAL (`t_b15f4c50`): skor per sub-kriteria kedua kandidat (46,2 vs 96),
analisis per kriteria dengan rujukan angka kartu tim + verifikasi grep mandiri, penilaian
paket .md & .ipynb, JSON primer di `scratch/v11/v11_eval_scorecard.json`. Tanpa
kesimpulan identitas versi; keputusan menang = PM-FINAL.*
