# V10 BAB 6 — RULE, PERSISTENCE & WORKFLOW HIBRIDA: CARA KERJA + PENGARUH ANTAR-KOMPONEN

Task: `t_258c7550` [Algorithm Engineer Rule/Persistence/Hybrid] · Board: `capstone-v10-proposal` · 2026-10-14 (WIB)
Peran: **Algorithm Engineer Rule/Persistence/Hybrid** — menulis Bab 6 proposal V10 (porsi **(e)-hybrid**:
workflow hibrida & pengaruh antar-komponen), langsung dari sudut pandang peran sendiri.
Kontrak bab: `docs/V10_PM1_OUTLINE.md` §3 (Bab 6) + §4 aturan lintas-bab.
Sumbu angka: `docs/V9_E_RULE_ENGINE.md` (dokumen hasil induk) + **JSON primer eksekusi**
`scratch/v9_e_rule/v9_e_RULE_0{1,2,3,4}_*_results.json` + kode `code/v9_e_RULE_0*.py`.

> **Prinsip dokumen (aturan lintas-bab PM1 §4):** SEMUA angka dikutip dari JSON/dokumen/kode sumber —
> **nol angka karangan**. Setiap angka di bab ini **dihitung ulang dari JSON primer** di sesi ini
> (skrip `verify*.py` di workspace kartu). Dokumen ini adalah **solusi** (apa yang dijalankan,
> bagaimana mekanismenya, pada tingkat apa layak dipakai), **bukan riwayat kegagalan**.

> **Riset pendahuluan: `scientific-critical-thinking`** — klaim "rule ≡ label (sirkular)" TIDAK
> ditulis sebagai fakta tanpa bukti: diuji lewat recompute independen dari `bins/` (mismatch = **0
> di 5/5 kelas**, §1.2). Klaim "hibrida memangkas FP" **dipisah tegas** antara **degenerasi
> struktural** (vib/shk/stuck_k1, di mana hibrida ≡ rule) dan **non-degenerasi** (ssi/hyd) — tidak
> diklaim seragam (§3.4).
> **Riset pendahuluan: `verification-mandatory`** — semua angka = kutipan JSON eksekusi yang
> **direproduksi ulang** di sesi ini (ssi FP 26→7; hyd FP 2.091→927; AUPRC hyb 0,6024); determinisme
> rerun 4/4 identik (`v9_e_RULE_05_determinism.py`); baseline punya cross-check eksternal (bit_wear
> identik digit V6; canary 3-RMS = rentang V8). Sirkularitas rule-jendela dinyatakan terbuka (§1.2),
> bukan disembunyikan.
> **Riset pendahuluan: `statistical-analysis`** — tidak ada baseline universal: tiap engine butuh
> **baseline relevan sendiri** (S9); fold UNDERPOWERED (positif < 30) **dilabeli**; AUPRC/lift
> **tidak dirata-ratakan** antar kelas (plafon lift = 1/prev beda per kelas); persistence dinilai
> pada subset `valid_prev` (konvensi V8) **dan** semua-baris; persistence-horizon onset dianotasi
> **HINDSIGHT** (bukan standar "mengalahkan" yang fair) — §5.
> **Riset pendahuluan: `sequentialthinking`** — 4 pikiran (4/4 sukses, `sequ-mcp`): verifikasi angka
> JSON → struktur bab (5 sub-tugas kartu) → kejujuran degenerasi vs non-degenerasi → rencana output.

---

## 0. RINGKASAN BAB (satu paragraf untuk dosen)

Jawaban peran Rule/Persistence/Hybrid untuk pertanyaan proposal **(e) "kalau hybrid: workflow-nya &
pengaruh antar-komponen"** adalah: lapisan non-ML pada alat PdM = **tiga mesin yang saling menumpuk,
bukan satu model gabungan baru**. (1) **Rule** — aturan transparan **nol-pelatihan** per kelas,
dibaca pada menit **t0−1 (strict-past)** agar tidak membaca labelnya sendiri. (2) **Persistence**
`ŷ(t)=y(t−1)` — baseline naive standar deret waktu **sekaligus engine status terkuat** yang terbukti
pada data ini. (3) **Hibrida** `h(t)=rule(t0−1) AND persistence(t)` — menyatukan **dua pemotong
orthogonal** (rule memotong status **kini**, persistence memotong status **kemarin**) sehingga gerbang
AND **memangkas false alarm** tanpa melatih model apa pun. Efeknya terukur: **ssi FP 26→7 (−73,1%)**
dan **hyd-K-i FP 2.091→927 (−55,7%, 9/9 well)**, dengan **hyd AUPRC naik ke 0,6024 > rule 0,5751 >
persistence 0,5555**. Di kelas lain (vib/shk/stuck_k1) hibrida **≡ rule** karena rule t0−1 sudah
himpunan-bagian dari persistence — sifat **struktural yang dinyatakan terbuka**, bukan kemenangan.
Seluruh baseline relevan (**S9**: persistence, canary-kedalaman, prevalence-random, rule ambang)
dihitung pada fold **identik** tim lain dan siap menjadi syarat masuk evaluator.

---

## 1. (Sub-tugas 1) RULE PER KELAS — DEFINISI ATURAN & KENAPA

Rule = aturan **tanpa pelatihan**, transparan, dapat diaudit baris-per-baris. Satu rule kanal per
kelas (kode: `code/v9_e_RULE_01_status.py`).

| Kelas | Rule (kanal) | Rumus operasional | Basis waktu |
|---|---|---|---|
| **vib** | ambang getaran lateral | `status(t) = 1[VIBLAT_RT(t) ≥ 32,17405 ft/s²]` | **t0−1 strict-past** |
| **ssi** | **definisi kanal** stick-slip | `SSI(CRPM) = (max − min)/(2·mean)`; alarm bila `SSI ≥ 1` (min 10 sampel, `crpm_mean>0`) | **t0−1 strict-past** |
| **shk** | ambang bit-bounce/shock | `status(t) = 1[SHKRSK_RT(t) ≥ 1]` | **t0−1 strict-past** |
| **stuck_k1** | rule blok + **E1 2-dari-3** (independen) | `alarm = 1[ (z(TQA)>2) + (z(HKLD)>2) + (ROP-drop≥30%) ≥ 2 ]`, `z = 0,6745·(x−median)/MAD` jendela **60 mnt strict-past** | t0−1 + jendela 60 mnt |
| **hyd_ki** | **rule z-pit** (residu tekanan, resep V6-31) | `\|z\|>2` atas `SPPA_mean` vs bin `TFLO_mean` (qcut-10, median/MAD per bin); alarm-jendela bila `anom/obs ≥ 0,5`, `MIN_OBS=5` | t0−1 + jendela 10 mnt |

**Kenapa rule dipakai (bukti, bukan selera):** (i) **transparan & nol-pelatihan** → dapat dipakai di
kelas di mana RF **dilarang** (hyd-K-i, keputusan D-A5); (ii) merepresentasikan **sistem hari-ini**
(status quo rig), sehingga menjadi pembanding jujur untuk ML; (iii) menghasilkan **FP nyata** yang
membuka perhitungan B3 (pengurangan pemeriksaan). **FP rule lintas fold (dari JSON, direproduksi
sesi ini): vib 197 · ssi 26 · shk 121 · stuck_k1 49 · hyd_ki 2.091.**

### 1.1 KENAPA "STRICT-PAST" (t0−1) — INTI KEJUJURAN METODE

Label setiap kelas dibentuk dari **jendela `[t0, t0+10)`** (positif = kanal terpicu di dalam jendela).
Konsekuensinya:

- **Cek identitas sirkular** (`rule_window_identity`, recompute independen dari `bins/`): rule yang
  dievaluasi **pada jendela label** menghasilkan **mismatch = 0 di 5/5 kelas** — vib 23.922 baris,
  ssi 35.906, shk 56.495, stuck_k1 5.555, hyd_ki 52.509. Artinya rule-jendela **≡ label (pembentuk
  label)**, jadi FP-nya 0 **by construction** — bukan "detektor sempurna".
- **Konsekuensi metodologis:** membaca bin **t0** (bagian dari jendela label) = **membaca label
  sendiri** (bocor). Maka pembanding operasional yang sah = rule pada **menit t0−1** — hanya membaca
  data **sebelum** t0. Inilah invariant anti-bocor S5 (`feat_ts_max < lab_ts`).
- **Bukti strict-past bekerja:** FP rule t0−1 **NYATA dan besar** (vib 197 … hyd 2.091) — justru
  karena tidak lagi "menyalin" label, rule menjadi detektor yang jujur dan bisa dikritik. E1 stuck
  memakai median+MAD jendela 60 mnt yang juga **strict-past** (`≤ m`); MAD=0 → z=0 (konservatif,
  didokumentasikan).

> **Ringkas:** "strict-past" = **aturan etika pengukuran**, bukan optimasi. Ia memastikan angka rule
> bukan artefak sirkularitas, sehingga perbandingan ML-vs-rule dan hibrida berdiri di atas dasar bersih.

---

## 2. (Sub-tugas 2) PERSISTENCE `ŷ(t)=y(t−1)` — BASELINE SEKALIGUS ENGINE STATUS

**Definisi:** `ŷ(t) = y(t−1)` pada grid **60 detik**; dibaca dari kolom `y_prev_*` (resep D1, jendela
`[t0−10, t0)`), dinilai pada subset `valid_prev=1` (konvensi V8 claim1) **dan** versi semua-baris.

**Dua peran sekaligus:**

1. **Baseline naive** (S9) — pembanding minimum yang harus dilewati detektor apa pun. Lift =
   `AUPRC / prevalence`; plafon lift = `1/prev`.
2. **Engine status terbaik** yang terbukti pada data ini — bukan aib, tapi **kemampuan** yang dicatat
   terbuka. Ringkasan AUPRC rata-rata (JSON `01_status`, per kelas, direproduksi sesi ini):

| Kelas | persistence | rule(t0−1) | canary-depth | prevalence-random | pemenang (jumlah fold) |
|---|---|---|---|---|---|
| vib | **0,6299** | 0,5625 | 0,4141 | 0,3029 | persistence 3/4 fold |
| ssi | **0,0410** | 0,0226 | 0,0401 | 0,0209 | persistence 5/9 fold |
| shk | **0,0913** | 0,0836 | 0,0460 | 0,0371 | seri 4/9–4/9 |
| stuck_k1 | 0,6516 | **0,6682** | 0,5893 | 0,3934 | rule 1/2 (seri 1/2) |
| hyd_ki | 0,5555 | 0,5751 | 0,1980 | 0,1502 | rule 7/9 |

**Persistence sebagai engine status terbaik di hyd/bit_wear** (peran yang diminta kartu):

- **hyd_ki**: persistence AUPRC mean **0,5555** — konsisten mengalahkan canary-depth (0,1980) &
  prevalence-random (0,1502) di **9/9 fold**, kalah tipis dari rule z-pit (0,5751). Persistence =
  engine status non-ML terkuat kedua di kelas ini (rule sedikit lebih baik; hibrida terbaik, §3).
- **bit_wear K-1** (LOWO 7 well): persistence AUPRC mean **0,6699** — **identik digit** dengan E1d
  V6 (mis. F-14 0,6792052825924018), menang vs canary-depth (0,3888) di **4/4 fold layak** & vs random
  **4/4**. Replikasi independen = pipeline baseline terverifikasi silang.
- **tool_wear K-ii**: persistence **N/A per PM1 §2.7** — label konstan dalam run → `y(t−1)` ≡
  identitas-run; angka diagnostik 0,9915–0,9929 = **memorisasi struktur run, bukan deteksi keausan**
  (dinyatakan terbuka, angka dicetak agar transparan).

**Mengapa persistence kuat di kelas status:** label status **kontinu dalam blok** (blok
getaran/stick-slip/stuck berlangsung beberapa menit) → `y(t−1)` hampir selalu benar di dalam blok.
Ini sifat **struktur label status**, dijelaskan apa adanya.

**Batas persistence (jujur):** (i) recall rendah di kelas langka (ssi 0–0,40); (ii) FAR24 tinggi
(ssi F-10 17,6; shk F-10 29,3) → hanya untuk **tier tren/L1 terkalibrasi**; (iii) N/A di tool_wear
(§ di atas).

---

## 3. (Sub-tugas 3) HIBRIDA `h(t)=rule(t0−1) AND persistence(t)` — WORKFLOW & MEKANISME

### 3.1 RUMUS & PRINSIP

```
        h(t) = rule(t0−1)  AND  persistence(t)
                ─────┬────          ──────┬─────
   "pemotong STATUS-KINI"     "pemotong STATUS-KEMARIN"
   (kanal sedang aktif        (kanal sudah aktif
    di menit t0−1)             di menit t0−1, dibaca
                               sebagai y(t−1))
```

Dua komponen **memotong dari dua arah yang berbeda** dan digabung dengan **AND (konfirmasi-status
D-A3)** — bukan model gabungan baru, bukan rata-rata skor. Hibrida hanya menyalakan alarm bila
**kedua** sumber setuju bahwa kanal relevan sedang aktif.

### 3.2 WORKFLOW LANGKAH DEMI LANGKAH (diagram alur hybrid)

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  INPUT: bins per well (grid 60 dtk) + dataset D1 (kolom y, y_prev_*)          │
 └───────────────────────────────┬─────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┴────────────────────────┐
        │ LANGKAH 1 — Rule pada t0−1 (strict-past)          │
        │  baca kanal hanya < t0:                           │
        │   vib  → VIBLAT_RT(t0−1) ≥ 32,17405                │
        │   ssi  → SSI(CRPM)(t0−1) ≥ 1                       │
        │   shk  → SHKRSK_RT(t0−1) ≥ 1                       │
        │   stuck→ stuck_max(t0−1) ≥ 1  /  E1 2-dari-3       │
        │   hyd  → z-pit anom(t0−1)                          │
        │  → r ∈ {0,1}                                       │
        └────────────────────────┬──────────────────────────┘
                                 │
        ┌────────────────────────┴──────────────────────────┐
        │ LANGKAH 2 — Persistence pada t                        │
        │  ŷ(t) = y(t−1)   (kolom y_prev_*, subset valid_prev)   │
        │  → p ∈ {0,1}                                           │
        └────────────────────────┬──────────────────────────┘
                                 │
        ┌────────────────────────┴──────────────────────────┐
        │ LANGKAH 3 — GERBANG AND (konfirmasi-status D-A3)  │
        │  h(t) = r AND p                                    │
        │  alarm menyala ⟺ rule setuju DAN persistence setuju │
        └────────────────────────┬──────────────────────────┘
                                 │
        ┌────────────────────────┴──────────────────────────┐
        │ LANGKAH 4 — METRIK per fold (S9 harness)           │
        │  AUPRC, lift, plafon 1/prev, P, R, TP/FP/FN/TN,    │
        │  FAR_24h = FP/(n_neg/60)·24  (konvensi V8 claim1)  │
        └────────────────────────┬──────────────────────────┘
                                 │
                                 ▼
              JSON primer  scratch/v9_e_rule/v9_e_RULE_01_status_results.json
```

### 3.3 MEKANISME PENGARUH ANTAR-KOMPONEN (inti bab)

**Mengapa AND memangkas false alarm — dua pemotong orthogonal:**

- **Rule (t0−1) = pemotong STATUS-KINI.** Ia menyalakan alarm bila kanal aktif **sekarang**.
  Kelemahannya: kanal bisa aktif sesaat (transien) → **FP**.
- **Persistence (t) = pemotong STATUS-KEMARIN.** Ia menyalakan alarm bila kanal **sudah aktif
  semenit sebelumnya** → menuntut **kontinuitas** (bukan kilatan sesaat).
- **AND** hanya meloloskan alarm yang **lolos kedua saringan** → setiap alarm hibrida sudah
  "diperkuat" oleh bukti kontinuitas → **FP turun**, karena alarm rule yang terisolasi (kanal nyala
  di t0−1 tapi sudah mati di t0) **dibuang**.

**Efek terukur pada kelas definisi-kanal (non-degenerasi) — angka dari JSON, direproduksi sesi ini:**

| Kelas | Rule FP (lintas fold) | Hybrid FP | Δ FP | Recall rule → hybrid | P rule → hybrid | AUPRC rule → hybrid |
|---|---|---|---|---|---|---|
| **ssi** | 26 | **7** | **−19 (−73,1%)** | 0,0105 → 0,0014 | 0,2435 → 0,1333 | 0,0226 → 0,0206 |
| **hyd_ki** | 2.091 | **927** | **−1.164 (−55,7%)** | 0,7515 → 0,6555 | 0,7094 → 0,8334 | 0,5751 → **0,6024** |

- **ssi:** FP dipangkas **26→7 (−73,1%)**; pemangkasan terjadi di **6/7 fold ber-FP** (memotong 6/7
  fold ber-FP; F-14 tie di 0). Ini contoh gerbang AND mengubah "nyaris tanpa recall" rule menjadi
  **deteksi hemat-awas** (FAR turun, mis. F-10 FAR24 0,62 → 0,21).
- **hyd_ki:** FP dipangkas **2.091→927 (−55,7%)** di **9/9 well**; **precision naik 0,709→0,833**;
  **AUPRC naik ke 0,6024** > rule 0,5751 > persistence 0,5555 → **hibrida mengalahkan persistence di
  8/9 fold** (Δ −0,017…+0,092; F-9 satu-satunya fold kalah −0,017). Ini bukti empiris D-A3:
  **konfirmasi dua-kondisi menaikkan presisi** di kelas di mana RF dilarang.

**Dampak terhadap RECALL (dinyatakan terbuka):**

| Kelas | Δrecall (hybrid − rule) | Catatan |
|---|---|---|
| vib | **+0,0000** | degenerasi — hibrida ≡ rule |
| shk | **+0,0000** | degenerasi — hibrida ≡ rule |
| stuck_k1 | **+0,0000** | degenerasi — hibrida ≡ rule |
| ssi | **−0,0091** | trade-off presisi; recall rule memang ~0 |
| hyd_ki | **−0,0960** | trade-off sengaja: tukar recall sedikit untuk presisi besar |

→ **Mekanisme = trade-off presisi-vs-recall yang terkendali:** di kelas di mana rule sudah bersih
(vib/shk/stuck_k1), hibrida **tidak mengubah apa pun** (recall & FP identik, AUPRC identik). Di kelas
di mana rule berisik (ssi/hyd), hibrida **menukar sedikit recall demi pengurangan FP besar**.

### 3.4 KAPAN HIBRIDA DEGENERASI (≡ RULE) — DAN MENGAPA

Di **vib, shk, stuck_k1**: hibrida **≡ rule** (AUPRC identik: vib 0,5625; shk 0,0836; stuck_k1
0,6682). Penyebab struktural: pada kelas definisi-kanal, **rule(t0−1) sudah himpunan-bagian dari
persistence(t)** — bila kanal aktif di t0−1, maka label jendela di t−1 juga aktif, sehingga
`persistence(t)=y(t−1)` juga 1. Akibatnya `rule AND persistence = rule`. **Ini sifat struktural yang
dinyatakan terbuka**, bukan kegagalan: menambah gerbang AND di kelas yang rule-nya sudah
presisi-tinggi (vib P 0,87–0,95; stuck P 0,92–0,97) memang tidak mengubah hasil. Efek nyata hibrida
muncul justru di kelas dengan **rule berisik** (ssi/hyd).

### 3.5 CATATAN STUCK_K1 — HIBRIDA E1 (alternatif)

Untuk stuck_k1 juga dihitung **hibrida E1 AND persistence**: F-14 FP 125→12 (E1 AUPRC 0,1337, lift
0,9908 ≈ prevalence → **hasil negatif terukur**: aturan mekanis 2-dari-3 **tidak** mendeteksi blok
STUCK di sumur ini). Konsisten: E1 mentah ≈ prevalence, sehingga AND-nya juga ≈ prevalence.

### 3.6 KELAS SEKUNDER — HYBRID DEGRADASI (dinyatakan)

- **bit_wear K-1:** rule layer = label Teale (`high_MSE`, kanal terlarang anti-sirkular) → **hibrida
  degradasi ke persistence** (dinyatakan terbuka di JSON `meta.hybrid`).
- **tool_wear K-ii:** persistence N/A → tidak ada hibrida rule AND persistence yang bermakna.

---

## 4. (Sub-tugas 4) BASELINE S9 — KENAPA TIAP ENGINE BUTUH BASELINE RELEVAN SENDIRI

**Definisi S9** (PM1 §4.5): baseline relevan dihitung E_RULE **per tugas pada fold yang sama** dengan
engine utama — persistence, canary-kedalaman, prevalence-random, rule ambang; angka baseline = syarat
masuk evaluator. Konvensi (JSON `meta`): seed 42; `FAR_24h = FP/(n_neg/60)·24`; AUPRC detektor biner =
`average_precision_score(y, pred)`; fold dari `lowo_<engine>.json` (identik E_ML/E_STAT).

**Kenapa tidak ada satu baseline universal:**

1. **Tugas beda → baseline beda.** Deteksi-kondisi (label jendela 10 mnt) dan prediksi-onset
   (label horizon/transisi) punya distribusi & makna berbeda. Persistence yang literal-deployable
   (`persistence-event`) di onset ≈ prevalence; persistence-horizon justru hindsight (§5).
2. **Prevalensi beda → plafon lift beda.** `plafon = 1/prev` (vib prev 0,14–0,57 vs hyd 0,08–0,26 vs
   ssi 0,003–0,065). Karena itu **AUPRC/lift dilarang dirata-ratakan antar kelas** — angka dilaporkan
   per kelas/fold.
3. **Kelas langka → canary (ML posisi) bisa lebih relevan** (ssi: persistence > canary hanya 2/9;
   V8 juga menemukan ssi = kelas di mana ML dibenarkan). Baseline "canary-depth" mengontrol apakah
   sinyal nyata atau hanya memorisasi posisi/depth.
4. **Prevalence-random** = lantai statistik: skor `default_rng(42).uniform` per fold; membuktikan
   detektor mengalahkan tebakan acak ber-prevalensi sama.
5. **Rule ambang** = baseline "sistem hari-ini" (status quo) yang wajib dikalahkan sebelum sebuah
   metode ML dianggap menambah nilai.

---

## 5. (Sub-tugas 5) HASIL PER FOLD DARI JSON

Semua tabel di bawah = kutipan **langsung** JSON primer, **dihitung ulang** di sesi ini
(`verify*.py`). Format ringkas; tabel penuh ada di `docs/V9_E_RULE_ENGINE.md` §2.

### 5.1 vib (4 fold LOWO) — DEGENERASI (hyb ≡ rule)

| fold | well | n | prev | pers | rule(t0−1) | FP | P | R | hyb FP | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 1989 | 0,5651 | 0,7925 | 0,7372 | 30 | 0,9444 | 0,4537 | 30 | 0,6124 | 0,5746 |
| 1 | F-15A | 6482 | 0,2380 | 0,5473 | 0,4119 | 65 | 0,8676 | 0,2761 | 65 | 0,4578 | 0,2329 |
| 2 | F-15_S | 10903 | 0,1405 | 0,5137 | 0,4250 | 65 | 0,8984 | 0,3753 | 65 | 0,2770 | 0,1384 |
| 3 | F-5 | 4548 | 0,2704 | 0,6660 | 0,6760 | 37 | 0,9519 | 0,5951 | 37 | 0,3093 | 0,2657 |

persistence > canary 4/4 & > random 4/4. Rule-display P 0,87–0,95, recall 0,28–0,60. Hibrida ≡ rule.

### 5.2 ssi (9 fold LOWO) — HIBRIDA NON-DEGENERASI (FP 26→7)

| fold | well | n | pos | prev | pers | rule(t0−1) | FP | P | R | hyb FP | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7133 | 161 | 0,0226 | 0,1884 | 0,0273 | 3 | 0,4000 | 0,0124 | **1** | 0,0302 | 0,0219 |
| 1 | F-12 | 4293 | 83 | 0,0193 | 0,0210 | 0,0193 | 6 | 0,0000 | 0,0000 | **1** | 0,0709 | 0,0191 |
| 2 | F-14 | 5455 | 75 | 0,0137 | 0,0140 | 0,0137 | 0 | – | 0,0000 | 0 | 0,0305 | 0,0148 |
| 3 | F-15A | 6020 | 31 | 0,0051 | 0,0086 | 0,0130 | 3 | 0,2500 | 0,0323 | **2** | 0,0139 | 0,0045 |
| 4 | F-15_S | 5342 | 85 | 0,0159 | 0,0166 | 0,0170 | 8 | 0,1111 | 0,0118 | **1** | 0,0243 | 0,0157 |
| 5 | F-5 | 4714 | 102 | 0,0216 | 0,0334 | 0,0310 | 2 | 0,5000 | 0,0196 | **0** | 0,0751 | 0,0195 |
| 6 | F-7 | 982 | 3 | 0,0031 | 0,0031 | 0,0031 | 0 | – | 0,0000 | 0 | 0,0201 | 0,0145 |
| 7 | F-9 | 1126 | 12 | 0,0107 | 0,0107 | 0,0107 | 0 | – | 0,0000 | 0 | 0,0097 | 0,0102 |
| 8 | F-9_A | 841 | 55 | 0,0654 | 0,0732 | 0,0678 | 4 | 0,2000 | 0,0182 | **2** | 0,0860 | 0,0675 |

**Total FP rule 26 → hybrid 7 (−73,1%).** Pemangkasan di 6/7 fold ber-FP. Persistence ≥ random 7/9;
2 fold UNDERPOWERED (F-7/F-9, pos<30) dilabeli.

### 5.3 shk (9 fold LOWO) — DEGENERASI (hyb ≡ rule)

| fold | well | n | prev | pers | rule(t0−1) | FP | P | R | hyb FP | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7899 | 0,0185 | 0,0236 | 0,0295 | 15 | 0,2857 | 0,0411 | 15 | 0,0212 | 0,0188 |
| 1 | F-12 | 5405 | 0,0401 | 0,0531 | 0,0675 | 8 | 0,5789 | 0,0507 | 8 | 0,0652 | 0,0411 |
| 2 | F-14 | 11205 | 0,0678 | 0,1599 | 0,1016 | 48 | 0,5340 | 0,0724 | 48 | 0,0630 | 0,0718 |
| 3 | F-15A | 6484 | 0,0063 | 0,0063 | 0,0063 | 3 | 0,0000 | 0,0000 | 3 | 0,0121 | 0,0080 |
| 4 | F-15_S | 11394 | 0,0227 | 0,0390 | 0,0449 | 22 | 0,4054 | 0,0579 | 22 | 0,0251 | 0,0234 |
| 5 | F-5 | 7140 | 0,0336 | 0,0451 | 0,0344 | 14 | 0,1250 | 0,0083 | 14 | 0,0487 | 0,0341 |
| 6 | F-7 | 2761 | 0,0967 | 0,4428 | 0,4139 | 7 | 0,9352 | 0,3783 | 7 | 0,0789 | 0,0967 |
| 7 | F-9 | 1851 | 0,0243 | 0,0380 | 0,0312 | 2 | 0,3333 | 0,0222 | 2 | 0,0611 | 0,0257 |
| 8 | F-9_A | 2356 | 0,0127 | 0,0140 | 0,0234 | 2 | 0,3333 | 0,0333 | 2 | 0,0388 | 0,0146 |

Rule-display shk **FAR24 0,67–6,62 = satu-satunya titik lintas-fold dengan FAR ≤ 6/24 jam dengan
recall > 0** (4 titik: F-10/F-12/F-15_S/F-7). Hibrida ≡ rule (degenerasi).

### 5.4 stuck_k1 (2 fold LOWO) + E1

| fold | well | n | pos | prev | pers | rule(t0−1) | FP | P | R | hyb FP | E1 AUPRC | E1 FP/P | hybrid-E1 FP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-14 | 3201 | 432 | 0,1350 | 0,5200 | 0,4892 | 16 | 0,9238 | 0,4491 | 16 | 0,1337 | 125 / 0,0458 | 12 |
| 1 | F-9_A | 2354 | 1575 | 0,6691 | 0,7832 | 0,8472 | 33 | 0,9662 | 0,5994 | 33 | 0,6659 | 35 / 0,5513 | 29 |

**Hasil negatif terukur:** E1 2-dari-3 AUPRC 0,1337 vs prev 0,1350 (lift 0,99) di F-14 → aturan
mekanis **tidak** mendeteksi blok STUCK pada sumur ini (FP 125; total E1 FP lintas fold = 160).

### 5.5 hyd_ki (9 fold LOWO) — HIBRIDA NON-DEGENERASI (FP 2.091→927; RF DILARANG D-A5)

| fold | well | n | pos | prev | pers | rule(t0−1) | FP | P | R | hyb FP | hyb P | can | rand |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 7571 | 1394 | 0,1841 | 0,8110 | 0,8354 | 166 | 0,8862 | 0,9275 | **66** | 0,9484 | 0,2388 | 0,1826 |
| 1 | F-12 | 7390 | 1426 | 0,1930 | 0,6328 | 0,6556 | 368 | 0,7598 | 0,8163 | **242** | 0,8158 | 0,1616 | 0,1927 |
| 2 | F-14 | 10401 | 865 | 0,0832 | 0,4336 | 0,4617 | 368 | 0,6226 | 0,7017 | **110** | 0,8243 | 0,0805 | 0,0873 |
| 3 | F-15A | 6156 | 698 | 0,1134 | 0,4897 | 0,5345 | 253 | 0,6744 | 0,7507 | **103** | 0,8154 | 0,1273 | 0,1117 |
| 4 | F-15_S | 8355 | 993 | 0,1189 | 0,4188 | 0,4826 | 359 | 0,6531 | 0,6808 | **199** | 0,7236 | 0,1285 | 0,1164 |
| 5 | F-5 | 6332 | 621 | 0,0981 | 0,5890 | 0,5886 | 194 | 0,7172 | 0,7923 | **58** | 0,8849 | 0,1559 | 0,0926 |
| 6 | F-7 | 2482 | 421 | 0,1696 | 0,4980 | 0,5251 | 189 | 0,6316 | 0,7696 | **76** | 0,7853 | 0,2220 | 0,1676 |
| 7 | F-9 | 1616 | 423 | 0,2618 | 0,6170 | 0,5709 | 108 | 0,7238 | 0,6690 | **36** | 0,8676 | 0,5117 | 0,2456 |
| 8 | F-9_A | 2206 | 331 | 0,1500 | 0,5096 | 0,5212 | 86 | 0,7162 | 0,6556 | **37** | 0,8356 | 0,1556 | 0,1552 |

**Hibrida non-degenerasi: AUPRC mean 0,6024 > rule 0,5751 > persistence 0,5555; FP 2.091→927
(−55,7%) di 9/9 well; mengalahkan persistence 8/9 fold.** Persistence > canary 9/9 & > random 9/9.

### 5.6 stuck_k2 (ONSET, 4 fold LOWO) — persH (hindsight) vs persE (deployable) vs E1

| fold | well | n | pos | onsets | persH AUPRC | B1 | TLead med | persE AUPRC | E1 AUPRC | E1 FP | canary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | F-10 | 4216 | 772 | 91 | **0,9016** | 0,967 | 1 mnt | 0,1860 | 0,1932 | 57 | 0,1762 |
| 1 | F-14 | 95925 | 389 | 57 | **0,8438** | 0,930 | 1 mnt | 0,0066 | 0,0043 | 307 | 0,0093 |
| 2 | F-9 | 16184 | 311 | 52 | **0,8265** | 0,962 | 3 mnt | 0,0333 | 0,0192 | 23 | 0,0401 |
| 3 | F-9_A | 2242 | 503 | 68 | **0,8890** | 0,941 | 1 mnt | 0,2244 | 0,2357 | 35 | 0,2532 |

- **persH = persistence-horizon** `y(t−1)` pada label horizon H=10 mnt — AUPRC 0,827–0,902, B1 93–97%.
  **Dianotasi HINDSIGHT** (mengetahui `y(t−1)` pada label horizon butuh tahu t_e lampau) →
  **UPPER-BOUND tes formulasi, BUKAN detektor deployable**.
- **persE = persistence-event** (literal R1, deployable) ≈ prevalence (lift 1,0–1,6).
- **E1 2-dari-3 ≈ prevalence** pada onset (AUPRC 0,0043–0,2357; B1 0–6,6%) → hasil negatif terukur.

### 5.7 Kelas SEKUNDER (bit_wear K-1, tool_wear K-ii, hyd-K-ii)

- **bit_wear K-1** (LOWO 7 well): persistence 0,6699 mean (4/4 fold layak menang vs canary & random);
  angka **identik digit** dengan E1d V6 (mis. F-14 0,6792052825924018). K-2 onset: **BELUM**
  (pra-reg K-2 belum terbit).
- **tool_wear K-ii** (LOTO 4 alat): canary 3-RMS 0,5164–0,6124 = rentang V8 (reproduksi); persistence
  **N/A per PM1 §2.7** (diagnostik 0,9915–0,9929 = memorisasi run).
- **hyd-K-ii** (split temporal 70/30): episode 124 = V8 ✓; prev_test 0,0037005 = V8 0,0037 ✓;
  rule z-pit **TLead = 0 menit di 124/124 onset** (deteksi saat-kejadian, bukan peringatan-dini).

---

## 6. (f) RINGKAS "7 vs 11 vs 27" DARI SUDUT RULE/HIBRIDA

| Angka | Arti (rujuk PM1 §1) | Porsi peran ini |
|---|---|---|
| **7** | jumlah **masalah/engine** (vib, ssi, shk, stuck, hyd, bit_wear, tool_wear) | rule & persistence & hibrida dijalankan untuk **ketujuh** kelas |
| **11** | jumlah **klaim/sub-tugas** yang dinilai A/B/C (3 engine 1 klaim + 4 engine 2 klaim = `3×1+4×2`) | baseline S9 disediakan **per sub-tugas** (K-i/K-ii) pada fold identik |
| **27** | jumlah **head** pada registry prototipe I1 (rule/persistence/hybrid/RF per kelas) | **3 head non-ML** per kelas (rule · persistence · hybrid) = sumber head L0/L1 di I1 |

---

## 7. VERIFIKASI & BATAS JUJUR

**Bukti mentah (semua direproduksi ulang di sesi ini dari JSON primer):**

| # | Klaim | Bukti |
|---|---|---|
| 1 | Semua angka dari eksekusi | JSON primer `scratch/v9_e_rule/v9_e_RULE_0{1,2,3,4}_*_results.json` + run log |
| 2 | Determinisme seed 42 | rerun 4 skrip → **4/4 JSON fold identik** (`v9_e_RULE_05_determinism.py`) |
| 3 | Fold identik tim lain | `lowo_*.json` D1 (37 fold rig); bit_wear 7/7 cocok E1d; hyd-K-ii = V8 |
| 4 | Baseline reproduksi silang | bit_wear identik digit V6; canary 3-RMS = rentang V8; vib persistence ≈ V8 |
| 5 | Rule sirkular terbuka | recompute independen: mismatch **0** di 5/5 kelas (§1.1) |
| 6 | Hibrida non-degenerasi | hyd AUPRC 0,6024 (8/9 > persistence), FP 2.091→927; ssi FP 26→7 |
| 7 | Angka sesi ini direproduksi | skrip `verify*.py` workspace kartu: FP ssi 26→7, hyd 2.091→927, AUPRC hyb 0,6024 — cocok dokumen induk |

**Batas jujur (BELUM / tidak diklaim):**

1. Persistence-horizon onset **TIDAK deployable** (hindsight) — jangan dipakai sebagai standar
   "mengalahkan" ML yang fair; pembanding adil = persistence-event & E1 (keduanya ≈ prevalence).
2. Hibrida **degenerasi (≡ rule)** di vib/shk/stuck_k1 — sifat struktural, bukan kemenangan.
3. FAR memakai konvensi V8 (`n_neg/60`) — asumsi 1 keputusan/menit walau jendela label 10 mnt
   tumpang-tindih; harmonisasi antar-kelas = tugas EVAL_A.
4. hyd-K-ii: 1 wellbore, split temporal (bukan LOWO); bit_wear K-2 & dataset-D1 hyd_k2 belum ada.
5. Generalisasi lintas-lapangan **TIDAK diklaim** (satu lapangan Volve + satu dataset bengkel Mendeley).
6. E1 ROP-drop "≥30% vs median60" — basis tidak eksplisit di R1 → change-control terbuka.

---

## 8. SUMBER ANGKA (traceability)

- `docs/V9_E_RULE_ENGINE.md` — dokumen hasil induk (semua angka & tabel).
- `scratch/v9_e_rule/v9_e_RULE_01_status_results.json` — 5 kelas status (33 fold rig): §1, §2, §5.1–5.5.
- `scratch/v9_e_rule/v9_e_RULE_02_stuck_onset_results.json` — 4 fold onset: §5.6.
- `scratch/v9_e_rule/v9_e_RULE_03_bitwear_toolwear_results.json` — bit_wear K-1 + tool_wear K-ii: §2, §5.7.
- `scratch/v9_e_rule/v9_e_RULE_04_hyd_k2_results.json` — hyd-K-ii split temporal: §5.7.
- `code/v9_e_RULE_01_status.py` (rule per kelas + gerbang AND) · `code/v9_e_RULE_02_stuck_onset.py`
  (persistence-horizon/event + E1) · `code/v9_e_RULE_03_bitwear_toolwear.py` · `code/v9_e_RULE_04_hyd_k2.py`
  · `code/v9_e_RULE_05_determinism.py`.
- Kontrak bab: `docs/V10_PM1_OUTLINE.md` §1 (7/11/27), §3 (Bab 6), §4 (aturan lintas-bab).
- Sumbu arsitektur: `docs/V9_PM1_ARCHITECTURE.md` (S9, D-A3, D-A5) · `docs/V9_R1_JUSTIFICATION.md` (metode+baseline).

---

## 9. BARIS RISET PENDAHULUAN (ringkas)

- Riset pendahuluan: `scientific-critical-thinking` — klaim "rule ≡ label (sirkular)" diuji lewat recompute independen (mismatch 0 di 5/5 kelas); klaim "hibrida memangkas FP" dipisah degenerasi (vib/shk/stuck_k1) vs non-degenerasi (ssi/hyd).
- Riset pendahuluan: `verification-mandatory` — semua angka = kutipan JSON eksekusi yang direproduksi ulang sesi ini; determinisme 4/4; sirkularitas rule-jendela dinyatakan terbuka.
- Riset pendahuluan: `statistical-analysis` — baseline relevan per tugas (tidak ada baseline universal); fold UNDERPOWERED dilabeli; AUPRC/lift tidak dirata-ratakan antar kelas; persistence-horizon onset dianotasi HINDSIGHT.
- Riset pendahuluan: `sequentialthinking` — 4 pikiran, 4/4 sukses (verifikasi angka → struktur bab → kejujuran degenerasi → rencana output).

*Selesai Bab 6 V10-E_RULE (`t_258c7550`) — porsi (e)-hybrid: workflow hibrida + pengaruh
antar-komponen. Siap digabung ke proposal V10 (perakit `t_0720bde5`).*
