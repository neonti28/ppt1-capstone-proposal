# V10 — BAB 5: METODE STATISTIK (LABELING, RUMUS PER ENGINE, HASIL)

Task: `t_656ee8de` [Algorithm Engineer Statistik] · Board: `capstone-v10-proposal` · 2026-10-14 (WIB)
Peran: **[Algorithm Engineer Statistik] V10-E_STAT** — menulis **Bab 5 proposal V10** (kontrak Bab 5 =
"Metode statistik", `docs/V10_PM1_OUTLINE.md` §2/§3), menjawab keluhan operator butir **(e) bagian
statistik** ("kalau statistik: statistiknya gimana") + menyinggung (a)–(d) dari sudut peran sendiri.
Sumbu angka: **KODE** `code/v9_e_STAT_01..04.py` (rumus dibaca dari kode, bukan ingatan) + **JSON
primer** `scratch/v9_e_stat/v9_e_stat_0{1,2,3,4}_*_RESULTS.json` (hasil) + dokumen hasil induk
`docs/V9_E_STAT_ENGINE.md`. Kosakata angka 7/11/27 mengikuti `docs/V10_PM1_OUTLINE.md` §1.

> **Prinsip bab (kontrak PM1 §4):** SEMUA angka = kutipan kode/JSON sumber — **nol angka karangan**;
> setiap rumus ditulis dalam **notasi matematika** + **penjelasan awam** + **lokasi baris kode**;
> hasil dilaporkan **apa adanya** (termasuk yang tidak layak); yang belum terukur ditulis
> "belum terukur", bukan 0 dan bukan dihapus. Bab ini **solusi** (apa yang dihitung, mengapa, hasilnya),
> bukan riwayat kegagalan.

> **Riset pendahuluan: `scientific-critical-thinking`** — tiap klaim dipisah OBSERVED (angka JSON) vs
> INTERPRETASI (makna persistence, sirkularitas rule-|z|) vs BELUM-TERUKUR; ancaman validitas yang
> berbeda per tugas (deteksi-kondisi ≠ prediksi-onset) diberi baseline berbeda; hasil negatif
> (spesifisitas change-point 0,50; Fisher 0 TP) ditulis apa adanya tanpa dilunakkan.
> **Riset pendahuluan: `verification-mandatory`** — label hyd dihitung ULANG dari sumber kedua
> (`bins/`) dan dibandingkan baris-per-baris (**0/52.509 mismatch**; `y_prev` 0/45.758); onset stuck
> cocok persis D1 (93/61/55/72); label K-ii reproduksi persis V8 (124 episode = 39 kick/85 loss);
> determinisme re-run penuh **4/4 JSON IDENTIK** (kecuali `elapsed_s`); daftar belum-diverifikasi §5.4.
> **Riset pendahuluan: `statistical-analysis`** — baseline **relevan per tugas** (tidak ada baseline
> universal); plafon lift 1/prev dilaporkan tiap fold; CI95 moving-block bootstrap (blok 60, 1.000,
> seed 42); <30 positif = UNDERPOWERED dilabeli; FAR dibaca pada skala aslinya (rig = jendela/24 jam,
> bengkel = alarm/menit) — perbandingan lintas-kelas tanpa konversi dilarang.
> **Riset pendahuluan: `sequentialthinking`** (4 pikiran, 4/4 sukses, `sequ-mcp`) — scope 4 workstream →
> verifikasi angka terprogram dari JSON → struktur bab yang menutup (e) → cek terakhir (dataset + RF 7/7).

---

## 5.0 RINGKASAN BAB 5 UNTUK DOSEN (satu paragraf)

Lapisan statistika pada alat PdM ini **bukan ML**: ia empat prosedur robust yang mengubah kanal sensor
mentah menjadi **label** dan **detektor yang dapat diaudit baris-per-baris**. (1) **hyd-K-i** — label
kondisi hidrolik dibentuk dengan **z robust median/MAD per desil `TFLO`** (bukan mean/std yang rusak
oleh outlier), lalu dideteksi dengan **persistence** `ŷ(t)=y(t−W)`, W=10 menit; Random Forest
**dilarang** di kelas ini karena secara empiris kalah (ΔB negatif 7/7). (2) **stuck-E2** — skor onset
= `z(TQA)+z(HKLD)+ROP-drop` di atas median/MAD jendela 60 menit, dengan **ambang q95 yang dikalibrasi
hanya dari TRAIN** (anti-peeking): ranking di atas prevalensi di 4/4 fold tetapi **belum signifikan**
(CI95 memuat prevalensi 4/4). (3) **tool_wear-K-i** — deteksi perubahan-regime dalam-run dengan
**change-point SSE + permutation 500×**, dikalibrasi within-tool median/MAD; titik operasi
**FAR-terkalibrasi** mendeteksi **4/4** alat tumpul dengan hanya **1–3 alarm palsu** di alat baru dan
**lead 20–36 detik**. (4) **Fisher/Pearson** sebagai baseline klasik hyd K-ii — **tidak bisa dijalankan
literal** karena kanal aliran-keluar absen di F-9A (terverifikasi: 4 kanal flow saling berkorelasi
r=0,995–1,000 = semuanya aliran masuk). Empat angka kunci kejujuran metode: **0/52.509 mismatch** label
tereproduksi, **4/4 JSON identik** saat re-run, **8/8 change-point signifikan di dua ambang** (hasil tak
bergantung pilihan ambang), dan **0 true-positive** Fisher di q95. Semua angka dari eksekusi nyata pada
data lapangan Volve + dataset bengkel Mendeley.

**Kedudukan dalam kosakata PM1 (7 engine / 11 klaim / 27 head):** peran statistik menyumbang rumus &
hasil untuk **sub-tugas K-i/K-ii** dari 3 dari **7 engine** — `hyd`, `stuck`, `tool_wear` (Bab 1 §1.2
klaim #5–#7, #10 dari **11 klaim**) — dan mengukur **head statistik** di REGISTRY prototipe I1
(`docs/V10_PM1_OUTLINE.md` §1.3, daftar **27 head**): `hyd/persistence` (head 20), `stuck/e1_2of3` +
`stuck/persistence_event` (head 16–17), `tool_wear/calib_5of27` + `tool_wear/op_far_calibrated`
(head 25–26), `hyd/k2_tidak_tersedia` (head 22). Ketiga angka (7 engine ⊂ 11 klaim ⊂ 27 head) merujuk
daftar eksak §1.1–§1.3 kerangka PM1, bukan dijumlahkan (aturan lintas-bab §4.1).

---

## 5.1 (e.1) hyd-K-i — RUMUS LABEL + ENGINE PERSISTENCE + KENAPA RF DILARANG

**Jenis tugas:** deteksi **kondisi/status** residu tekanan `SPPA` (`|z|>2`) per menit — **bukan**
prediksi onset, sehingga TLead tidak berlaku (kelas status dinilai dengan margin/konfirmasi, B4).
**Data:** `scratch/v9_d1/datasets/hyd_ki.csv.gz`, **52.509 baris**, **9 wellbore**, split **LOWO 9
fold** (`lowo_hyd_ki.json`). **Engine:** persistence `ŷ(t)=y(t−W)`, W=10 menit (kolom `y_prev_hyd`,
subset `valid_prev_hyd`). Kode: `code/v9_e_STAT_01_hyd_ki.py`.

### 5.1.1 Rumus pembentuk label (label-forming statistic) — `v9_e_STAT_01.py` baris 103–123

Label dibentuk langsung dari kanal fisik `SPPA` (standpipe pressure) yang dinormalisasi terhadap laju
aliran `TFLO` (total flow-out proxy). Empat langkah:

**Langkah 1 — binning desil `TFLO`** (baris 111, `pd.qcut(d["TFLO_mean"], NQ=10, ...)`):

```
q_j = qcut(TFLO, 10),   j = 1..10      (bin = desil laju aliran)
```

*Awam:* tekanan hidrolik bergantung pada berapa banyak lumpur dipompa, jadi tekanan tidak dibandingkan
dengan angka mutlak melainkan dengan tekanan "normal untuk laju aliran itu". Desil = 10 zona laju aliran.

**Langkah 2 — z robust per bin, median/MAD** (baris 114–117):

```
median_bin = median( SPPA | bin j )
MAD_bin    = median( | SPPA − median_bin| | bin j )

z = 0,6745 · ( SPPA − median_bin ) / MAD_bin
  = ( SPPA − median_bin ) / ( 1,4826 · MAD_bin )
```

Faktor `0,6745 = 1/1,4826` adalah pengali baku MAD→σ untuk distribusi normal (NIST). Skrip menulis
bentuk ekuivalen `(SPPA − med)/(1,4826·MAD)`.

*Awam:* median = nilai tengah (tahan pencilan); MAD = "sebaran tipikal" ala median. Ini mengukur
"seberapa aneh" satu nilai tekanan dibanding kebiasaan di zona aliran itu **tanpa** tertipu lonjakan
ekstrem (beda dari mean/std yang rusak oleh satu outlier).

**Langkah 3 — anomali per menit** (baris 118, `(z.abs() > 2)`):

```
anom(t) = 1[ |z(t)| > 2 ]
```

**Langkah 4 — agregasi jendela W=10 menit** (baris 142–150; `MIN_OBS=5`, ambang 0,5):

```
n_obs (t0)  = jumlah menit dalam [t0, t0+10) dengan SPPA & TFLO terisi
n_anom(t0)  = jumlah menit anomali dalam jendela

valid(t0)  = 1[ n_obs ≥ MIN_OBS = 5 ]
y_hyd(t0)  = 1[ valid(t0) ∧ ( n_anom / n_obs ≥ 0,5 ) ]
```

*Awam:* satu menit aneh bisa kebetulan; "kondisi anomali hidrolik" baru dinyatakan bila **paling
sedikit setengah** dari 10 menit ke depan menunjukkan tekanan menyimpang (dan minimal 5 menit punya
data). Mencegah label "kedip-kedip" karena satu spike.

### 5.1.2 Engine persistence `ŷ(t) = y(t−W)` — baris 195

```
ŷ(t) = y(t − W),   W = 10 menit      (kolom y_prev_hyd, subset valid_prev_hyd)
```

*Awam:* engine berasumsi "kondisi hidrolik sekarang = kondisi 10 menit lalu". Karena label kondisi
memang **persisten** (satu blok anomali berlangsung banyak menit), prediktor naive ini justru kuat —
inilah sebabnya ML tidak otomatis menang.

### 5.1.3 Kenapa Random Forest DILARANG di kelas ini (D-A5) — keputusan empiris

Bukan dogma anti-ML. Bukti (OBSERVED, cross-check `docs/V10_R1_ALASAN.md` baris 57 & `docs/V9_E_STAT_ENGINE.md`
baris 80): Random Forest di kelas hyd-K-i menghasilkan **ΔB = AUPRC(RF) − AUPRC(persistence) NEGATIF
di 7/7 fold**. Menambah model kompleks tidak menambah daya deteksi, malah merugikan. Karena label
dibentuk dari kanal (`SPPA`,`TFLO`) yang juga **dilarang** jadi fitur (anti-sirkular), ML hanya bisa
"menebak" label yang sama lewat jalan memutar — dan kalah oleh persistence yang langsung membacanya.
Nilai ML dipindahkan ke K-ii (prediksi kegagalan), di mana ada estimand nyata.

### 5.1.4 Hasil per lipatan (LOWO 9 fold) — kutipan JSON `v9_e_stat_01`

**Kontrol validitas (verification-mandatory #2):** label dihitung ULANG independen dari `bins/`
(resep identik), dibandingkan baris-per-baris:

| Cek | Hasil |
|---|---|
| `y_hyd` recompute vs dataset | **0 mismatch / 52.509 baris** (9/9 well 100%) |
| `y_prev_hyd` recompute (pasangan ts−W yang ada) | **0 mismatch / 45.758 pasangan** |

**Hasil engine persistence (9 fold, semua ≥331 positif → tidak ada UNDERPOWERED):**

| Test well | n | pos | prev | AUPRC (CI95) | lift (plafon 1/prev) | P | R | FAR/24jam-neg | delay med (mnt) |
|---|---|---|---|---|---|---|---|---|---|
| F-10 | 7.571 | 1.394 | 0,1841 | 0,843 [0,734; 0,915] | 4,58 (5,43) | 0,899 | 0,922 | 32,4 | 3,5 |
| F-12 | 7.390 | 1.426 | 0,1930 | 0,643 [0,543; 0,734] | 3,33 (5,18) | 0,742 | 0,820 | 98,0 | 0,0 |
| F-14 | 10.401 | 865 | 0,0832 | 0,444 [0,284; 0,580] | 5,34 (12,02) | 0,631 | 0,659 | 49,6 | 0,0 |
| F-15A | 6.156 | 698 | 0,1134 | 0,490 [0,269; 0,677] | 4,32 (8,82) | 0,668 | 0,679 | 62,3 | 0,0 |
| F-15_S | 8.355 | 993 | 0,1189 | 0,424 [0,279; 0,553] | 3,57 (8,41) | 0,615 | 0,617 | 74,9 | 3,0 |
| F-5 | 6.332 | 621 | 0,0981 | 0,599 [0,383; 0,757] | 6,10 (10,20) | 0,754 | 0,764 | 38,8 | 0,0 |
| F-7 | 2.482 | 421 | 0,1696 | 0,506 [0,321; 0,648] | 2,98 (5,89) | 0,648 | 0,705 | 110,7 | 2,0 |
| F-9 | 1.616 | 423 | 0,2618 | 0,625 [0,394; 0,799] | 2,39 (3,82) | 0,793 | 0,687 | 89,7 | 0,0 |
| F-9_A | 2.206 | 331 | 0,1500 | 0,541 [0,266; 0,715] | 3,61 (6,67) | 0,711 | 0,702 | 67,5 | 1,5 |

Ringkas JSON `summary`: AUPRC layak **0,4245–0,8426**; lift **2,39–6,10**; **lift>1 di 9/9 fold**;
**ΔB persistence>0 di 9/9 fold**; P 0,615–0,899.

**Baseline relevan:** (a) prevalence-random → AUPRC = prev, lift by definition 1,0 → **ΔB persistence
> 0 di 9/9 fold** (AUPRC − prev = 0,306–0,659); (b) rule `|z|` manual = **pembentuk label** →
**tautologi** (P=R=1,0 by construction) sehingga **bukan** pembanding keunggulan; perannya = B3
(beban alarm: 32–111 alarm/24jam-negatif pada label itu sendiri).

**Kemampuan:** status anomali hidrolik persisten antar-menit → persistence menang semua fold (delay
median **0–3,5 mnt**). **Batas:** FAR 32–111/24jam skala jendela = beban blok, **bukan** alarm (gate
L1 butuh FAR≤6 terukur — belum).

---

## 5.2 (e.2) stuck-E2 — SKOR z(TQA)+z(HKLD)+ROP-drop, AMBANG q95-TRAIN ANTI-PEEKING

**Jenis tugas:** **prediksi onset** 0→1 dengan horizon **H=10 menit** (kejadian mendatang → TLead
berlaku). **Data:** `scratch/v9_d1/datasets/stuck_k2.csv.gz`, **118.567 baris**, split **LOWO 4
fold**. **Engine:** `E2_stats`. Kode: `code/v9_e_STAT_02_stuck_e2.py`.

### 5.2.1 Rumus skor E2 (label-blind, dari `bins/` grid 60 dtk) — baris 68–89

Skor dihitung **tanpa melihat label**, per segmen (gap >30 menit = segmen baru; `GAP_SEG_MIN=30`):

```
med60(x)  = rolling(60 mnt, min 20).median().shift(1)                     x ∈ {TQA, HKLD, ROP}
mad60(x)  = | x − med60(x) | .rolling(60 mnt, min 20).median().shift(1)    x ∈ {TQA, HKLD}
mean10(x) = rolling(10 mnt, min 3).mean()

z_TQA  = ( mean10(TQA)  − med60(TQA)  ) / ( 1,4826 · mad60(TQA)  + ε )
z_HKLD = ( mean10(HKLD) − med60(HKLD) ) / ( 1,4826 · mad60(HKLD) + ε )

ROP_drop = clip( ( med60(ROP) − mean10(ROP) ) / | med60(ROP) | , 0 , ∞ )

score_E2(t) = z_TQA(t) + z_HKLD(t) + ROP_drop(t)
```

`shift(1)` = **strict-past** (hanya memakai informasi sebelum t — tidak ada look-ahead); `ε=1e-9`
menghindari bagi-nol.

*Awam:* torsi (TQA) dan beban kait (HKLD) yang tiba-tiba menyimpang dari kebiasaan 60 menit terakhir,
ditambah penurunan laju penetrasi (ROP) yang mendadak, dijumlahkan menjadi satu angka "seberapa
mencurigakan situasi ini". Tiga gejala khas sebelum pipa terjepit digabung.

### 5.2.2 Ambang q95 TRAIN (anti-peeking) — baris 153–165

Ambang **tidak** dioptimasi pada data uji. Ia kuantil-95 skor yang **dipool dari well TRAIN saja**,
dengan topeng hanya pada baris operasi & di luar blok stuck:

```
thr = quantile_95( { score_E2(t) : t ∈ TRAIN-wells, ops(t)=1, in-block(t)=0 } )
pred(t) = 1[ score_E2(t) ≥ thr ]
```

*Awam:* garis alarm ditetapkan **sebelum** melihat data uji (menetapkan nilai kelulusan sebelum ujian),
jadi hasil tidak bisa "dicurangi" dengan menggeser ambang pasca-hasil. Anti-sirkular: `STUCK_RT` hanya
dipakai sebagai topeng in-block, **bukan** fitur skor. Ambang per fold: **2,4649 / 2,8219 / 2,7621 /
2,5144**.

### 5.2.3 Hasil per lipatan (LOWO 4 fold) — kutipan JSON `v9_e_stat_02`

| Test well | n | pos | prev | thr q95-train | AUPRC (CI95) | lift (plafon) | P@q95 | R@q95 | FAR/24jam-neg | onset(run) | R@H | TLead med (mnt) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F-10 | 4.216 | 772 | 0,1831 | 2,4649 | 0,231 [0,167; 0,306] | 1,26 (5,46) | 0,313 | 0,104 | 73,6 | 93 | 0,161 | 7,0 |
| F-14 | 95.925 | 389 | 0,00406 | 2,8219 | 0,0073 [0,0036; 0,0149] | 1,80 (246,6) | 0,022 | 0,031 | 8,0 | 61 | 0,131 | 2,5 |
| F-9 | 16.184 | 311 | 0,0192 | 2,7621 | 0,0203 [0,0085; 0,0352] | 1,06 (52,0) | 0,000 | 0,000 | 2,4 | 55 | 0,000 | – |
| F-9_A | 2.242 | 503 | 0,2244 | 2,5144 | 0,324 [0,192; 0,496] | 1,45 (4,46) | 0,487 | 0,151 | 66,2 | 72 | 0,181 | 8,0 |

Ringkas JSON `summary`: AUPRC layak **0,0073–0,324**; lift **1,057–1,797** (= 1,06–1,80);
**lift>1 di 4/4 fold**; **CI95 memuat prev di 4/4 fold**; total onset-run **281**.

**Kontrol konstruksi:** onset-run hasil segmentasi positif = **93/61/55/72 = PERSIS invarian D1 (V8)**
— crosscheck horizon terpenuhi 4/4. **CI95 AUPRC memuat prev di 4/4 fold** → lift titik >1 di 4/4
tetapi **TIDAK signifikan** (konsisten V8 "CI memuat prev 5/5").

**Baseline relevan:** (a) prevalence-random → AUPRC = prev; (b) **E0 persistence LITERAL**
(`y_prev_stuck_onset`): AUPRC 0,827–0,902, R@H 0,78–0,94 — **namun ini ORACLE**, bukan detektor
deployable (y(t−1) pada menit horizon ke-2..H hanya diketahui setelah onset terjadi); (c) **E0
persistence konstruksi V8** (alarm hanya tepat di t_e) → recall@H = 0 by construction (alarm jatuh di
luar horizon `[t_e−H, t_e)`).

**Kemampuan:** skor E2 memberi ranking di atas prevalensi di semua fold (poin), TLead median 2,5–8 mnt
pada fold yang mendeteksi. **Batas:** signifikansi 0/4; FAR 2,4–74/24jam; P di F-9 = 0 → **L3 triage
(skor-ranking), L1/L0 belum.**

---

## 5.3 (e.3) tool_wear-K-i — CHANGE-POINT SSE + PERMUTATION 500× + KALIBRASI WITHIN-TOOL

**Jenis tugas:** deteksi **perubahan-regime dalam-run** (bengkel, satuan **detik**) — bukan prediksi
horizon (D-A7: lead = detik bengkel, **tidak** dijumlah dengan menit rig). **Data:**
`scratch/v6_e1/toolwear_windows.csv` — **469 jendela 1 detik**, **27 fitur getaran**, **4 alat × 2
run**; label = identitas run (desain dataset → anti-sirkular terpenuhi). Kode:
`code/v9_e_STAT_03_tool_wear.py`.

### 5.3.1 Bagian A — rumus change-point + permutation — baris 56–84

**Change-point 1-split SSE.** Untuk seri `x_1..x_n` (di sini vektor 12-dim: kurt/crest/fdom/rms ×
X/Y/Z, distandarisasi in-run):

```
SSE(τ) = Σ_{t≤τ} (x_t − μ₁)²  +  Σ_{t>τ} (x_t − μ₂)²
τ* = argmin_τ SSE(τ),    μ₁=mean(x_1..x_τ), μ₂=mean(x_{τ+1}..x_n)
drop = SSE_total − SSE(τ*)
```

*Awam:* cari satu titik potong yang paling memisahkan data menjadi "sebelum" dan "sesudah" dengan dua
perilaku berbeda. Semakin besar `drop`, semakin tajam perubahan regime.

**Uji signifikansi permutation 500×** (seed 42):

```
p = ( 1 + #{ SSE_perm ≥ drop_obs } ) / ( 1 + 500 )        (= 1/501 minimal)
```

Yakni acak urutan seri 500 kali, hitung ulang `drop` tiap kali, hitung berapa kali acakan
menyamai/mengalahkan drop asli. Arah `≥` benar (drop besar = signifikan); teks R1 §3.7 menulis `≤`
**terbalik** → dicatat sebagai change-control CC-1 dan dieksekusi dengan arah benar (sama dgn V8
`v8e_cp_validity.py`).

**Ambang ganda (CC-2):** dijalankan **DUA** ambang — p≤0,05 (resep V8) **dan** p≤0,002 (literal spek;
p minimal tercapai dengan 500 permutasi = 1/501 = 0,001996) — supaya tidak "memilih hasil".

**Tes pembeda artefak termal:** bila `t_cp` dominan di detik awal (<5 jendela) di >50% run →
sub-klaim gugur. Hasil: **0/8 run** early → lanjut dinilai.

### 5.3.2 Bagian B — kalibrasi within-tool (median/MAD) — baris 190–238

Kalibrasi "normal" tiap alat dari **30% awal run R01 (alat baru)**, lalu hitung z tiap fitur dan alarm
bila cukup banyak fitur menyimpang:

```
med = median( 30% awal R01 )          (per fitur, 27 fitur)
MAD = median( |x − med| ) · 1,4826
z(t) = ( x(t) − med ) / MAD
alarm(t) = 1[ #{ fitur dengan |z| > 3 } ≥ 5 dari 27 ]
```

*Awam:* pelajari "cara normal alat baru berjalan" dari awal rekaman, lalu bunyikan alarm bila ≥5 dari
27 pengukuran getaran menyimpang lebih dari 3 "simpangan tipikal". Baseline rule 3-RMS: alarm bila ≥1
kanal RMS `|z|>3` (kalibrasi sama).

### 5.3.3 Bagian C — titik operasi FAR-terkalibrasi — baris 243–277

Ambang dipilih sebagai kuantil skor R01-eval agar **laju alarm palsu** pada alat baru ≤ target (1,0
dan 0,2 alarm/menit):

```
thr = quantile( score_R01eval , q ),   q dipilih agar FP/menit ≤ target
alarm(t) = 1[ score(t) ≥ thr ]
```

### 5.3.4 Hasil — kutipan JSON `v9_e_stat_03`

**Bagian A (change-point):**

| Cek | Hasil |
|---|---|
| Signifikansi p≤0,05 (V8) | **8/8 run** |
| Signifikansi p≤0,002 (literal) | **8/8 run** (semua p = 0,0020 = 1/501) |
| Spesifisitas keausan (R01 = alat baru) | **GUGUR**: cp signifikan 4/4 di R01 → precision run-level = 4/8 = **0,50**, recall 1,0 |
| TLead cp → akhir R02 (alat tumpul) | 34/36/39/27 dtk, median **35 dtk** (min 27) |
| Kesepakatan antar-family (kurt/crest/fdom/rms) | selisih t_cp median **16,5 dtk** (rentang 8–40); per family p≤0,05: kurt 7/8, crest 8/8, fdom 8/8, rms 8/8; cp gabungan 12-dim 8/8 dua ambang |
| n=8 run | **UNDERPOWERED** (<30) → metrik = proporsi, bukan klaim populasi |

**Bagian B (kalibrasi within-tool, ambang baku ≥5/27 |z|>3):**

| Alat | FP R01 (alat baru) | FAR FP/menit | % jendela R01 alarm | Deteksi R02 | first alarm (dtk) | TLead→akhir R02 (dtk) | baseline rule 3-RMS (FP R01 / deteksi) | kurangi_ragu |
|---|---|---|---|---|---|---|---|---|
| T01 | 41/42 | 58,6 | 97,6% | ✓ | 0 | 60 | 41 / ✓ | 0,00 |
| T02 | 27/35 | 46,3 | 77,1% | ✓ | 14 | 48 | 33 / ✓ | 0,18 |
| T03 | 30/42 | 42,9 | 71,4% | ✓ | 0 | 60 | 40 / ✓ | 0,25 |
| T04 | 34/40 | 51,0 | 85,0% | ✓ | 0 | 58 | 36 / ✓ | 0,06 |

Interpretasi jujur: deteksi 4/4 **TAPI** alarm nyala 71–98% di alat BARU → "terdeteksi" **tidak
bermakna** pada ambang baku 5/27 (FAR 43–59 alarm/menit >> tier).

**Bagian C (titik operasi FAR-terkalibrasi) — hasil kunci:**

| Target alarm/menit | FP R01 per alat | Deteksi R02 | first alarm (dtk) | TLead (dtk) | % R02 alarmed |
|---|---|---|---|---|---|
| ≤1,0 | 1 / 3 / 1 / 3 | **4/4** | 35 / 26 / 36 / 38 | 25 / 36 / 24 / 20 | 3,3–6,9% |
| ≤0,2 | 1 / 3 / 1 / 3 | **4/4** | 35 / 26 / 36 / 38 | 25 / 36 / 24 / 20 | 3,3–6,9% |

**Inilah hasil yang LAYAK dipakai**: dengan hanya **1–3 alarm palsu** di alat baru, keempat alat
tumpul tetap terdeteksi, dengan lead **20–36 detik** — cukup untuk gating inspeksi (bukan alarm
otomatis). **Bagian D (ranking):** AUPRC engine = **0,589**, prev = 0,512, lift **1,151**, plafon
1,954, ΔB vs identity-majority **+0,077**; persistence **N/A** (label konstan dalam run — DINYATAKAN,
bukan dihilangkan).

**Kemampuan:** detektor perubahan-regime + gating inspeksi via FAR-terkalibrasi (4/4, FP 1–3).
**Batas:** spesifisitas cp gagal (0,50); kalibrasi baku 5/27 tidak spesifik; transfer ke rig **tidak
diklaim** (confound urutan-run); n=8 UNDERPOWERED.

---

## 5.4 (e.4) FISHER/PEARSON (baseline hyd K-ii) + HASIL P=R=0 @ q95

**Jenis tugas:** prediksi kegagalan hidrolik (kick/loss **proxy**), H=10 mnt, split temporal 70/30
pada 1 wellbore F-9A. **Engine:** korelasi Pearson + transformasi Fisher-z. Kode:
`code/v9_e_STAT_04_fisher_pearson.py`.

### 5.4.1 Rumus — baris 165–169

**Pearson (korelasi product-moment):**

```
r = Σ (x−x̄)(y−ȳ) / √( Σ(x−x̄)² · Σ(y−ȳ)² )
```

di sini `x = dV_active/dt` (neraca tank aktif) dan `y = dV_pit` (perubahan volume pit), pada jendela
rolling **30 menit**.

**Transformasi Fisher-z** (stabilisasi varians korelasi):

```
z' = atanh(r) = ½ · ln( (1+r) / (1−r) ),    SE(z') = 1/√(n−3)
```

**Skor detektor:** deviasi `z'` dari baseline rolling 60 menit (shift(1)):

```
score(t) = | z'(t) − med_base(t) | / ( 1,4826 · MAD_base(t) ),   alarm = 1[ score ≥ q95_TRAIN ]
```

*Awam:* ukur seberapa erat dua besaran bergerak bersama (aliran masuk vs perubahan volume pit).
Normalnya mereka sejalan (r tinggi). Bila hubungan itu tiba-tiba rusak/berbalik, itu tanda
ketidakcocokan neraca lumpur (indikasi kick/loss).

### 5.4.2 Status literal — TIDAK BISA DIJALANKAN (bukan asumsi, hasil tes diskriminatif)

Rumus literal butuh `FlowIn − FlowOut`. **F-9A tidak punya kanal aliran-keluar.** Bukti probe: `Flow
Pumps` 345.442 non-null, `Mud Flow In` 83.565, `TFLO30s` 64.757, `FLOW-TRPM` 34.115; korelasi antar
mereka **r = 0,995–1,000** → **semuanya aliran MASUK**; dari 239 kolom F-9A tidak ada flow-out. Status:
**belum-terukur** (literal ≠ varian). Varian terdokumentasi (imbalance = `dV_active/dt`) dijalankan &
dilaporkan **terpisah** dengan anotasi **risiko sirkularitas** (tank aktif bisa diturunkan dari pit →
r bisa mekanis tinggi; angka varian **bukan** bukti keunggulan literal).

### 5.4.3 Hasil — kutipan JSON `v9_e_stat_04`

**Kontrol validitas label K-ii** (resep literal V8 claim2: 13 kolom pit, sentinel [−5,150], r10, z
`0,6745`-scaled, `|z|>2` sustain ≥5 mnt, merge onset <30 mnt, sirkulasi ≥500 L/min): **124 episode
(39 kick / 85 loss)** — **reproduksi persis V8**; `prev_test = 0,003701` = angka V8 0,0037.

| Metrik (test 30% akhir, n=8.107, pos=30) | Nilai |
|---|---|
| AUPRC (CI95) | **0,022** [0,0025; 0,0684] — **memuat prev 0,0037** |
| lift (plafon 270,2) | 5,95 |
| **P / R @q95** | **0,000 / 0,000** (TP=0, FP=177, FN=30) |
| FAR @q95 | 31,6 / 24jam-negatif |
| B1 / TLead | 0/3 onset uji (3 onset = UNDERPOWERED) |
| Baseline prevalence-random | AUPRC = 0,0037 (analitik) |
| Baseline rule z-pit | deteksi di menit t_e (DI LUAR horizon) → B1 = 0 by construction; TLead = 0 |

**Kemampuan varian:** ranking di atas prevalensi (poin) tetapi **tidak signifikan** (CI memuat prev)
dan **nol deteksi** di ambang operasi (P=R=0). **Perbandingan diskriminatif (R1 §4.5):** AUPRC RF K-ii
V8 = **0,2279** vs varian Fisher/Pearson = **0,022** (split/label sama) → **RF mempertahankan
nilai-tambah** atas baseline statistika termurah. **Batas:** 1 wellbore; label = PROXY; sirkularitas
parsial varian.

---

## 5.5 (a)–(f) DARI SUDUT PERAN STATISTIK (ringkas) + VERIFIKASI & BATAS

### 5.5.1 Jawaban keluhan operator (porsi statistik)

| Pertanyaan operator | Jawaban porsi statistik |
|---|---|
| **(a) 7 engine + apa yang dideteksi** | Peran statistik menangani **4 prosedur**: hyd-K-i (kondisi residu SPPA), stuck-E2 (onset H=10 mnt), tool_wear-K-i (perubahan-regime bengkel), Fisher/Pearson (baseline hyd K-ii). Empat lainnya (vib, ssi, bit_wear, shk) = porsi E_RULE/E_ML. |
| **(b) cara kerja engine** | hyd-K-i: label median/MAD per desil TFLO + persistence W=10. stuck-E2: skor `z(TQA)+z(HKLD)+ROP-drop` vs median/MAD 60 mnt, ambang q95-train. tool_wear: change-point SSE+permutation + kalibrasi within-tool. Fisher: Pearson + atanh(r). |
| **(c) kenapa metode dipilih** | Data sensor **skewed/non-normal** → z median/MAD tahan outlier (bukan mean/std). 469 jendela 1 dtk non-normal & n kecil → **permutation tanpa asumsi distribusi**. Ambang **q95-TRAIN** → anti-peeking. **RF dilarang di hyd-K-i** karena ΔB negatif 7/7 (empiris). |
| **(d) peran data** | Data = sumber tunggal semua angka; kontrol kejujuran lewat **recompute independen dari `bins/`** (0/52.509 mismatch). Data bengkel = 4 alat × 2 run, 469 jendela, 27 fitur. |
| **(e) labeling ML / rumus statistik / workflow hybrid** | Inilah dokumen ini (§5.1–§5.4): label dibentuk statistik robust (median/MAD), engine = persistence/change-point/korelasi, semua di atas baseline relevan per tugas. |
| **(f) 7 vs 11 vs 27** | **7 engine** = kelas masalah; **11 klaim** = sub-tugas/estimand; **27 head** = varian metode di registry prototipe I1 (`docs/V10_PM1_OUTLINE.md` §1). Peran statistik menyumbang **sub-tugas K-i/K-ii** hyd, stuck-E2, tool_wear-K-i + baseline K-ii, dan mengukur head `hyd/persistence`, `stuck/e1_2of3`, `stuck/persistence_event`, `tool_wear/calib_5of27`, `tool_wear/op_far_calibrated`, `hyd/k2_tidak_tersedia`. |

### 5.5.2 Verifikasi (verification-mandatory)

**Bukti mentah** (JSON primer `scratch/v9_e_stat/` + run log bertimestamp):

| # | Klaim | Bukti |
|---|---|---|
| 1 | Semua angka dari eksekusi | JSON primer `scratch/v9_e_stat/v9_e_stat_0*_RESULTS.json` + run log |
| 2 | Determinisme seed 42 | re-run penuh → **4/4 JSON IDENTIK** (kecuali `elapsed_s`) |
| 3 | Label hyd tereproduksi | recompute independen dari `bins/` → **0/52.509 mismatch** |
| 4 | Label K-ii reproduksi V8 | 124 episode (39/85), prev_test 0,0037 — persis |
| 5 | Onset stuck cocok D1 | 93/61/55/72 = persis invarian D1 |
| 6 | Ambang permutation ganda | 8/8 signifikan di p≤0,05 **dan** p≤0,002 → kesimpulan invariant |

**Change-control tercatat (bukan disembunyikan):**

- **CC-1** — R1 §3.7 menulis arah permutasi `≤` (terbalik) → eksekusi pakai `≥` (arah benar, sama V8).
- **CC-2** — ambang permutasi tunggal = memilih hasil → **dua ambang** dijalankan & dilaporkan (8/8 keduanya).
- **CC-3** — Fisher/Pearson literal butuh FlowOut yang **absen** → literal tidak dijalankan; varian proxy dijalankan terpisah + anotasi sirkularitas.
- **CC-4** — PM1 menyebut "12 kolom pit", F-9A punya **13** → memakai 13 (resep V8).
- **CC-5** — persistence-onset literal stuck = **ORACLE** → dilaporkan dua-frame (literal + konstruksi V8 recall@H=0).

### 5.5.3 Batas jujur (BELUM / tidak diklaim)

1. **Fisher/Pearson literal (FlowIn−FlowOut)** = belum-terukur (kanal flow-out tidak ada di F-9A); varian ≠ literal.
2. Perbandingan final baseline K-ii vs **RF E_ML V9** menunggu kartu E_ML/EVAL (angka lintas-run 0,022 vs 0,2279 = V8).
3. `y_prev_hyd` 45.758/45.758 pasangan cocok; sisa pasangan di luar ekspor D1 tidak diverifikasi.
4. FAR hyd-K-i/E2 = FP/(jendela negatif/60)×24 (asumsi jam-operasi V8); harmonisasi antar-kelas = tugas EVAL.
5. tool_wear: n=8 UNDERPOWERED; transfer ke rig **tidak diklaim** (confound urutan-run).
6. Generalisasi lintas-lapangan **tidak diklaim** (satu lapangan Volve + satu dataset bengkel Mendeley).

**Tidak ada satupun engine statistik yang diklaim layak alarm otomatis** (L0-alarm 0/7) — gate tidak
digeser; angka di sini = bahan evaluasi A/B/C, bukan label lolos.

---

## 5.6 SUMBER ANGKA (traceability)

- **Kode (rumus dibaca dari sini):** `code/v9_e_STAT_01_hyd_ki.py` · `code/v9_e_STAT_02_stuck_e2.py` ·
  `code/v9_e_STAT_03_tool_wear.py` · `code/v9_e_STAT_04_fisher_pearson.py`.
- **JSON primer (hasil):** `scratch/v9_e_stat/v9_e_stat_01_hyd_ki_RESULTS.json` ·
  `..._02_stuck_e2_RESULTS.json` · `..._03_tool_wear_RESULTS.json` · `..._04_fisher_pearson_RESULTS.json`
  (+ run log `v9_e_stat_0N_run_log.txt`).
- **Dokumen hasil induk:** `docs/V9_E_STAT_ENGINE.md`.
- **Kerangka V10 (kosakata & kontrak):** `docs/V10_PM1_OUTLINE.md` (§1 daftar 7/11/27, §3 Bab 5, §4 aturan lintas-bab).
- **Sumbu internal-engine:** `docs/V9_PM1_ARCHITECTURE.md` §2.4/§2.5/§2.7 · `docs/V9_R1_JUSTIFICATION.md`
  §3.4/§3.5/§3.7/§4.1/§4.5 · `docs/V9_D1_DATA_PIPELINE.md` (dataset + LOWO).
- **Data:** `scratch/v9_d1/datasets/hyd_ki.csv.gz` (52.509) · `.../stuck_k2.csv.gz` (118.567) ·
  `scratch/v6_e1/toolwear_windows.csv` (469) · `data/witsml/Norway-NA-15_47_9-F-9 A time.csv` (419.745).

*Selesai Bab 5 V10-E_STAT (`t_656ee8de`) — porsi (e)-statistik: rumus per engine statistik (hyd-K-i,
stuck-E2, tool_wear-K-i, Fisher/Pearson) + hasil dari JSON, siap digabung ke bab proposal V10 bersama
keluaran peran lain (PM1 Bab 1/8, R1 Bab 2, D1 Bab 3, E_ML Bab 4, E_RULE Bab 6, EVAL Bab 7).*
