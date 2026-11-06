# V9-I1 — INTEGRASI 7 ENGINE: PROTOTIPE ALAT PdM ADVISORY + HASIL UJI INTEGRASI

Task: `t_34e9b879` [Integration Engineer] · Board: capstone-v9-build · 2026-10-12 (WIB)
Status: SELESAI — prototipe berjalan pada data nyata Volve (segmen F-14) + USROP +
data bengkel tool_wear; verifikasi independen 13/13 PASS.
Kerangka penilaian: instruksi operator ("Evaluasi User.txt", standar 3 lapisan A/B/C)
— BUKAN gate lift 1,5. Tier pemakaian = milik `docs/V9_EVAL_C_LAYERC.md` §1; I1
memakainya apa adanya (dilarang menaikkan tier → diuji otomatis, cek V2).

Sumbu: `docs/V9_PM1_ARCHITECTURE.md` §1 (pipeline 5 lapis) + §2 (spesifikasi 7 engine)
+ §4.9 (DoD I1) + semua `docs/V9_E_*_ENGINE.md` + `docs/V9_EVAL_{A,B,C}_LAYER*.md`.

Output tugas ini:

| Artefak | Path |
|---|---|
| Dokumen (ini) | `docs/V9_I1_INTEGRATION.md` |
| Pipeline 7 engine + registry + lapisan keputusan | `code/v9_i1_pipeline.py` |
| Driver replay (CLI) | `code/v9_i1_run.py` |
| Verifikasi independen | `code/v9_i1_verify.py` |
| JSON primer (S6) | `scratch/v9_i1/v9_i1_RESULTS.json` (45.879 byte) |
| Log uji integrasi (cetakan laporan manusia + log run) | `scratch/v9_i1/v9_i1_TEST_LOG.txt` (288 baris), `scratch/v9_i1/v9_i1_RUN_LOG.txt` |
| Log verifikasi | `scratch/v9_i1/v9_i1_VERIFY.txt` (ringkas), `scratch/v9_i1/v9_i1_VERIFY_FULL.txt` (per cek) |

> **Riset pendahuluan: `scientific-critical-thinking`** — dokumen ini memisahkan
> OBSERVED (angka replay F-14 + kutipan EVAL/E_RULE/E_STAT dengan sumber per baris)
> vs DESAIN (registry/lapisan = keputusan I1) vs BELUM-TERUKUR (hyd K-ii, bit_wear
> K-2, tool_wear K-ii RF); setiap klaim punya pembanding baseline kampanye, bukan
> angka tunggal; kontradiksi yang ditemukan (badge tool_wear vs engine 5/27) direkonsiliasi
> dengan memecah head, bukan dipilih yang nyaman (§5.2).
> **Riset pendahuluan: `statistical-analysis`** — FAR dilaporkan pada SKALA JENDELA ASLI
> (rig: FP/24jam-negatif, konvensi `FP/(n_neg/60)*24`; bengkel: FP/menit-negatif,
> jendela 1 dtk) dan TIDAK dirata-ratakan antar kelas; metrik biner ML pada ambang 0,5
> dilabeli "ilustrasi" (ambang operasi pra-reg tidak ditetapkan di prototipe) — yang
> dipakai untuk ranking = AUPRC; fold UNDERPOWERED tidak dihitung mayoritas.
> **Riset pendahuluan: `verification-mandatory`** — verifikasi independen terpisah
> (`code/v9_i1_verify.py`, implementasi TIDAK memanggil ulang fungsi driver): 13 cek
> meliputi recompute dari data mentah, cross-check ke JSON kampanye E_RULE/E_STAT,
> determinisme rerun, dan daftar "belum diverifikasi" eksplisit di §10.
> **Riset pendahuluan: `what-if-oracle`** — 5 cabang Ω/α/Δ/Ψ/Φ dipakai untuk menguji
> keputusan lapisan (§8.1); kunci: cabang Δ ("promosikan engine jadi alarm") ditolak
> berdasar angka + assertion, bukan opini.
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe (Architect, Empiricist,
> Minimalist, Pragmatist, Contrarian) menekan rancangan lapisan keputusan; ketegangan
> "cepat terlihat berguna" vs "jujur soal bukti" dipertahankan, tidak dihapus (§8.2).
> **Riset pendahuluan: `sequentialthinking`** (4 pikiran, 4/4 sukses tool_call sequ-mcp)
> — inventaris data segmen → rancang pipeline 5 lapis → audit risiko kejujuran
> (rule≡label, kenaikan tier, ML non-terpakai) → rencana uji integrasi + acceptance.

---

## 0. RUANG LINGKUP DAN YANG TIDAK BOLEH BERUBAH

1. Keberhasilan = ALAT PdM koheren & layak pakai; ML = satu komponen bila beri nilai
   tambah (rule-based/statistical/persistence/hybrid/ML semuanya dipakai sesuai tugasnya).
2. Tiap engine punya jenis tugas berbeda (deteksi kondisi / deteksi anomali / prediksi
   kejadian mendatang / ranking) → tier & metriknya boleh berbeda; TIDAK ada gate seragam.
3. Tier pemakaian = hasil EVAL_C (TREN / PERINGATAN-BERPENGAWAS / BELUM LAYAK PAKAI).
   I1 **dilarang menaikkan tier** (DoD §4.9) — diverifikasi otomatis (cek V2: rank tier
   prototipe ≤ rank tier dokumen per klaim).
4. **Alarm otomatis kritis = 0 slot** (EVAL_C §3: tidak ada engine memenuhi syarat
   ALARM-OTOMATIS) — di-assert di kode dan di verifikasi (cek V3).

## 1. PIPELINE YANG DIRAKIT (5 lapis, mengikuti PM1 §1)

```
LAYER-0 DATA     : dataset D1 (grid 60 dtk, anti-bocor sudah diverifikasi D1) + USROP
                   (grid Kedalaman) + toolwear_windows.csv (grid 1 dtk, bengkel)
LAYER-1 FITUR    : 55 fitur rig/kelas (11 kanal × mean/std/slope/last/frac) dari D1;
                   30 fitur USROP; 27 fitur getaran bengkel. I1 TIDAK membuat fitur baru
                   (kontrak D1) — hanya memilih kolom & membuang kolom label (anti-sirkular)
LAYER-2 ENGINE   : 7 engine = 27 head (registry §2). Rule/persistence/hybrid MENGIMPOR
                   modul kampanye E_RULE langsung (v9_e_RULE_01/02) = integrasi, bukan salinan;
                   ML = RF kontrak seed 42 dilatih LOWO; tool_wear = resep E_STAT §B+§C
LAYER-3 KEPUTUSAN: L0 status otomatis · L1 peringatan human-in-loop · L2 tren/skor ·
                   L3 keputusan manusia; asersi: tier TREN/BELUM-LAYAK tidak boleh L1;
                   semua L1 wajib human_review_required=true; slot alarm otomatis = 0
LAYER-4 MANUSIA  : laporan cetak per engine (status + skor + badge FAR + label keyakinan
                   + batas pemakaian + flag human review) + JSON utk dasbor
```

Kode: `code/v9_i1_pipeline.py` (registry + 7 engine + decision layer),
`code/v9_i1_run.py` (driver), `code/v9_i1_verify.py` (verifikasi independen).

Rekaman wajib anti-bocor yang dipertahankan: semua head rule membaca **menit t0−1**
(strict-past; memang `rule_display` E_RULE) — membaca bin t0 = membaca label.

## 2. REGISTRY: TIER + LAPISAN + BADGE + BATAS PER HEAD (27 head)

Tier/badge/keyakinan/batas di bawah dikutip dari `V9_EVAL_C_LAYERC.md` §1–§2,
`V9_EVAL_A/B`, dan `V9_E_{RULE,STAT}_*`. Kolom "layer" = keputusan I1 (DESAIN).

| Engine / head | Klaim | Tier (EVAL_C) | Layer | Badge FAR (sumber) | Batas pemakaian tertulis |
|---|---|---|---|---|---|
| vib · rule_display | kondisi | PERINGATAN-BERPENGAWAS | L1 | FAR 10,0–49,9/24jam (4 well); P 0,87–0,95 | tanpa klaim lead-time; kalibrasi per-well dulu (D-A4) |
| vib · persistence | kondisi | TREN | L0 | baseline konfirmasi-status (AUPRC V8 0,517–0,796) | konfirmasi-status saja |
| vib · hybrid | kondisi | PERINGATAN-BERPENGAWAS | L1 | hibrida ≡ rule (E_RULE §2.1) | sama dengan rule |
| vib · rf_lowo | kondisi | TREN | L2 | FAR τ0,5 menyebar 4,1–496 (**119×**, EVAL_C C3) | ranking saja; jangan ambang global |
| ssi · rule_display | kondisi | PERINGATAN-BERPENGAWAS | L1 | FP 26 total lintas fold | nodata CRPM 62,3% (global) |
| ssi · persistence | kondisi | TREN | L0 | kalah 0/5 vs RF (V8) | baseline lemah, bukan detektor |
| ssi · hybrid | kondisi | PERINGATAN-BERPENGAWAS | L1 | FP 26→7 (−73,1%); ≤ rule di 7/7 fold layak (memotong 6/7, F-14 tie); FAR 0–3,7 | hemat-pemeriksaan, bukan alarm |
| ssi · rf_lowo | kondisi | TREN | L2 | τ0,3 FAR 0–15,6; well ≤6 hanya 2/7 | ranking; nodata = keterbatasan sensor |
| shk · rule_display | anomali | PERINGATAN-BERPENGAWAS | L1 | FAR 0,67–6,6; **≤6 di 7/9 well** | badge FAR wajib tampil; B3 negatif |
| shk · persistence | anomali | TREN | L0 | ≥ prevalence-random 7/9 | konfirmasi-status saja |
| shk · hybrid | anomali | PERINGATAN-BERPENGAWAS | L1 | hibrida ≡ rule | sama dengan rule |
| shk · rf_lowo | anomali | TREN | L2 | τ0,3 FAR 0–96,5; well ≤6 hanya 1/9; CI 7/9 memuat prev | screening tau 0,05–0,10; jangan alarm |
| stuck · rule_display | K-i | PERINGATAN-BERPENGAWAS | L1 | P 0,92–0,97; FAR 8,3–61,0 (hanya F-14, F-9_A) | cakupan 2 well; portabilitas belum terukur |
| stuck · persistence | K-i | TREN | L0 | 0,787 (F-9_A, kutipan V6) | K-i saja, tanpa peringatan dini |
| stuck · hybrid | K-i | PERINGATAN-BERPENGAWAS | L1 | E_RULE §2.4 (2 fold) | cakupan 2 well |
| stuck · e1_2of3 | K-ii | TREN | L2 | FAR 2,1–29,0; B1 0–0,066; FP 422 | TRIAGE ranking — belum peringatan |
| stuck · persistence_event | K-ii | TREN | L2 | FAR 0–2,9; FP total 11 | peringatan-dini berbeban-wajar utk tinjauan; bukan alarm |
| stuck · rf_lowo | K-ii | TREN | L2 | τ0,5 B1 0–0,045; signifikan CI 1/4 | ranking saja |
| hyd · rule_display | K-i | PERINGATAN-BERPENGAWAS | L1 | FP 2.091 total lintas fold | FAR skala jendela = beban blok, bukan alarm |
| hyd · persistence | K-i | PERINGATAN-BERPENGAWAS | L0 | P 0,615–0,793; FAR_t 32,2–109,7 | **RF DILARANG** (D-A5, ΔB − 7/7) |
| hyd · hybrid | K-i | PERINGATAN-BERPENGAWAS | L1 | FAR 14,6–58,4 (9/9 well); FP-cut −55,7% 9/9 | BELUM alarm-otomatis; naik tier bila kalibrasi per-well |
| hyd · k2_tidak_tersedia | K-ii | BELUM LAYAK PAKAI | L3 | q95 P=R=0; CI memuat prev | **TIDAK DIJALANKAN** (data pit/FlowOut belum ada) — status eksplisit |
| bit_wear · persistence | K-1 | TREN | L2 | P/R/FAR = belum terukur (field tak ada) | ranking saja; USROP ≠ rig Volve |
| bit_wear · k2_onset_belum | K-2 | BELUM LAYAK PAKAI | L3 | nol angka (kampanye belum jalan) | **BELUM DIJALANKAN** (pra-reg belum terbit) |
| tool_wear · calib_5of27 | K-i | TREN | L2 | engine 5/27 E_STAT §B: FP_R01 27–41 jendela (71–98% jendela eval); deteksi 4/4 | gating/skor saja; terlalu sensitif utk peringatan |
| tool_wear · op_far_calibrated | K-i | PERINGATAN-BERPENGAWAS | L1 | FAR-terkalibrasi ≤1 alarm/menit: FP 1–3/alat; deteksi 4/4; TLead 20–36 dtk | bukan "keausan spesifik" (precision 0,50); domain bengkel (D-A7) |
| tool_wear · canary_3rms | K-ii | TREN | L2 | canary AUPRC 0,516–0,612 (1,19×) | ranking lintas-alat; jangan alarm |

## 3. HASIL REPLAY SATU SEGMEN DATA NYATA (F-14 + USROP-F-14d + 4 alat bengkel)

Run: `python3 code/v9_i1_run.py --ml` → 21,55 s, python 3.14.7, seed 42
(log: `scratch/v9_i1/v9_i1_TEST_LOG.txt`). Segmen rig F-14 = satu-satunya wellbore
yang ADA di keenam dataset rig (vib 1.989 · ssi 5.455 · shk 11.205 · stuck_k1 3.201 ·
stuck_k2 95.925 · hyd_ki 10.401 jendela).

Angka di bawah = metrik REPLAY segmen ini (bukan badge kampanye; keduanya ditampilkan
terpisah di laporan). FAR rig = FP/24jam-negatif; FAR bengkel = FP/menit-negatif.

### 3.1 Kelas status rig (rule-display t0−1 · persistence · hybrid)

| Engine | Head | aktif/n | P | R | FP | FAR segmen | Catatan segmen |
|---|---|---|---|---|---|---|---|
| vib | rule | 540/1.989 | 0,9444 | 0,4537 | 30 | 49,9 | sesuai badge (10–49,9); n_nodata 356 |
| vib | persistence | 1.142/1.989 | 0,8336 | 0,8470 | 190 | 316,3 | ≡ fold kampanye F-14 (V10) |
| ssi | rule | 0/5.455 | None | 0,0 | 0 | 0,0 | **nodata CRPM F-14 = 5.268/5.455 (96,6%)** — jauh lebih buruk dari rata-rata 62,3% |
| ssi | persistence | 31/5.455 | 0,0323 | 0,0133 | 30 | 8,03 | baseline lemah (konsisten V8: kalah 0/5) |
| shk | rule | 103/11.205 | 0,5340 | 0,0724 | 48 | 6,618 | di ujung atas badge (0,67–6,6) |
| shk | persistence | 623/11.205 | 0,3708 | 0,3039 | 392 | 54,0 | ≡ fold kampanye F-14 (V10) |
| stuck K-i | rule | 210/3.201 | 0,9238 | 0,4491 | 16 | 8,32 | presisi di dalam rentang kampanye 0,92–0,97 |
| stuck K-i | persistence | 451/3.201 | 0,6785 | 0,7083 | 145 | 75,4 | ≡ fold kampanye (V10) |
| hyd K-i | rule | 975/10.401 | 0,6226 | 0,7017 | 368 | 55,6 | ≡ fold kampanye (V10) |
| hyd K-i | persistence | 876/10.401 | 0,6313 | 0,6393 | 323 | 48,8 | CI95 kampanye memuat prev 0/9 |
| hyd K-i | **hybrid** | 626/10.401 | **0,8243** | 0,5965 | **110** | 16,6 | FP rule 368→110 (**−70% di segmen**; kampanye −55,7% 9/9) |

Hybrid hyd = head paling bersih di segmen ini: presisi naik 0,62→0,82, FAR turun
55,6→16,6, arah sama dengan kampanye (V10 memastikan rule/persistence identik fold).

### 3.2 Onset / ranking (stuck K-ii, semua tier TREN = L2, tanpa peringatan)

| Head | aktif/n | P | R | FP | FAR segmen | AUPRC segmen |
|---|---|---|---|---|---|---|
| e1_2of3 (rule 2-dari-3, z/MAD 60 mnt) | 313/95.925 | 0,0192 | 0,0154 | 307 | 4,63 | ≈ prevalence (konsisten E_RULE §4) |
| persistence_event (E0b) | 4/95.925 | 0,50 | 0,0051 | 2 | 0,03 | FAR sangat rendah, recall kecil (kampanye: TLead med 7,0 mnt) |
| persistence_horizon (E0a, referensi) | 328/95.925 | — | — | — | — | **0,8438 = HINDSIGHT**, batas-atas teori saja |
| rf_lowo (200 pohon, latih F-10/F-9/F-9_A) | 42/95.925 | 0,0476 | 0,0051 | 40 | 0,60 | 0,0704 (rank lemah — canary ≥ RF di kampanye) |

### 3.3 ML head (RF kontrak, LOWO, seed 42) — skor RANKING (L2)

| Head | latih (well lain) | fitur | AUPRC segmen | aktif @0,5 | FAR @0,5 |
|---|---|---|---|---|---|
| vib rf_lowo | F-15A, F-15_S, F-5 | 55 | **0,9117** | 1.271/1.989 | 496,1 |
| ssi rf_lowo | 8 well selain F-14 | 55 | 0,0286 | 0/5.455 | 0,0 |
| shk rf_lowo | 8 well selain F-14 | 55 | 0,1036 | 0/11.205 | 0,0 |
| stuck rf_lowo | F-10, F-9, F-9_A | 55 | 0,0704 | 42/95.925 | 0,60 |

Catatan jujur (tercetak di JSON `ambang_operasi`):
- ambang 0,5 hanya **ilustrasi cetak** — ambang operasi pra-reg TIDAK ditetapkan di
  prototipe (S3); untuk ssi/shk ambang 0,5 menghasilkan 0 alarm → baca AUPRC/rank,
  bukan angka biner;
- FAR vib RF @0,5 = 496/24jam → **tepat mengapa vib RF tetap TREN** (kampanye: τ0,5
  menyebar 119×) — contoh nyata "engine tren tidak memunculkan alarm";
- fitur `SPM_*` (4 kolom) bernilai kosong di sebagian fold → imputer sklearn
  men-skip-nya (peringatan tercatat di `scratch/v9_i1/_ml_stderr.txt`); kehilangan
  fitur dinyatakan, bukan disembunyikan.

### 3.4 bit_wear K-1 (USROP F-14d, grid Kedalaman, 47.645 baris)

- persistence: aktif 4.917/47.645 · P 0,9927 · R 0,9925 · FP 36 · FAR 1,213/24jam.
- **Interpretasi kritis (jangan disalahbaca):** label `high_MSE_bit_wear` membentuk
  blok kontigu pada sumbu Kedalaman → y(t−1)≈y(t) sehingga P/R nyaris 1 = sifat
  autokorelasi grid, **bukan kemenangan detektor**; EVAL_C sudah menilai klaim ini
  TREN dengan "P/R/FAR belum terukur di kampanye". Dipakai untuk dasbor tren saja.
- komposisi label segmen: normal 34.674 · low_ROP_efficiency 8.053 · high_MSE 4.918.
- K-2 onset: **BELUM DIJALANKAN** (pra-reg belum terbit) → status eksplisit di L3.

### 3.5 tool_wear (4 alat × 2 run, 469 jendela 1 dtk — domain terpisah)

| Alat | engine 5/27: FP_R01 / det / TLead | op_far_calibrated: thr / FP_R01 / det / TLead |
|---|---|---|
| T01 | 41 (97,6%) / ya / 60 dtk | 12,317 / 1 / ya / 25 dtk |
| T02 | 27 (77,1%) / ya / 48 dtk | 10,0 / 3 / ya / 36 dtk |
| T03 | 30 (71,4%) / ya / 60 dtk | 8,633 / 1 / ya / 24 dtk |
| T04 | 34 (85,0%) / ya / 58 dtk | 10,0 / 3 / ya / 20 dtk |

- Head L1 = `op_far_calibrated` (FP 1–3/alat, deteksi 4/4, TLead 20–36 dtk) =
  **identik dengan kampanye E_STAT §C** (cek V9: fp/det/first/TLead/thr cocok 4/4 alat).
- Head `calib_5of27` diturunkan ke **L2** (gating/skor): ambang tetap 5/27 memicu
  71–98% jendela evaluasi pada alat BARU → tidak layak jadi peringatan (lihat §5.2).
- FAR bengkel dilaporkan **per menit** (jendela 1 dtk), bukan per 24 jam.

## 4. LAPISAN KEPUTUSAN (hasil run)

```
L0 status otomatis   : 5 head  (rule/persistence = sistem hari-ini, tanpa notifikasi)
L1 peringatan L-In-L : 11 head (semua tier PERINGATAN-BERPENGAWAS, semua human_review_required=true)
L2 tren/skor         : 9 head  (semua tier TREN — tidak ada satu pun yang boleh berbunyi)
L3 keputusan manusia : 2 head  (hyd K-ii belum tersedia; bit_wear K-2 belum dijalankan)
Slot ALARM OTOMATIS  : 0
Keputusan akhir      : MANUSIA (insinyur pengeboran)
```

Aturan keras di `decision_layer()` (dijalankan tiap run, bukan sekadar dokumentasi):

1. `tier != "ALARM-OTOMATIS"` untuk SEMUA head (assert);
2. head bertier TREN / BELUM-LAYAK **tidak boleh** jatuh ke L1 → engine tren tidak
   memunculkan peringatan (assert);
3. semua entri L1 wajib `human_review_required == true` (assert);
4. `auto_critical_alarm_slots == 0` di meta dan di decision_layer (assert).

## 5. UJI INTEGRASI + VERIFIKASI INDEPENDEN

### 5.1 Cek (13/13 PASS — `scratch/v9_i1/v9_i1_VERIFY.txt`)

| Cek | Isi | Hasil |
|---|---|---|
| V1a | 7 engine ada di JSON | PASS (`bit_wear, hyd, shk, ssi, stuck, tool_wear, vib`) |
| V1b | tiap head punya tier+layer+badge+keyakinan+batas | PASS (0 kekurangan) |
| V2 | tier prototipe TIDAK lebih tinggi dari baris klaim EVAL_C (27 head) | PASS — 0 kenaikan tier |
| V3a/b | 0 head ALARM-OTOMATIS; slot alarm = 0 | PASS |
| V4a/b | L1 hanya utk PERINGATAN-BERPENGAWAS; 11/11 L1 `human_review_required=true` | PASS |
| V5 | recompute INDEPENDEN dari data mentah: persistence+rule+hybrid vib, persistence hyd, persistence bit_wear, deteksi tool_wear T01 | PASS 6/6 |
| V6 | klaim belum-tersedia eksplisit (bukan nol diam, tanpa metrik palsu) | PASS |
| V7 | determinisme: 2× run ulang → JSON identik setelah meta waktu dibuang | PASS |
| V8 | determinisme ML: AUPRC shk RF dihitung ulang = 0,1036 == JSON | PASS |
| V9 | **konsistensi kampanye**: titik operasi tool_wear == E_STAT §C (4 alat: fp, det, first, TLead, thr) | PASS 4/4 |
| V10 | **konsistensi kampanye**: replay F-14 == fold F-14 E_RULE untuk 5 kelas × 2 head (tp, fp, precision, FAR) | PASS 10/10 |

V10 adalah bukti integrasi terkuat: pipeline prototipe menghasilkan **angka identik**
dengan kampanye untuk well yang sama (mis. vib rule P 0,9444 / FP 30 / FAR 49,942 di
keduanya) — artinya rule/persistence yang dirakit memang engine kampanye yang sama,
bukan reimplementasi yang menyimpang.

### 5.2 Temuan yang diperbaiki SELAMA pengujian (dicatat, bukan disembunyikan)

1. **Badge tool_wear tertukar** (ditemukan saat menyusun verifikasi): badge
   "FP 1–3/alat" milik titik operasi FAR-terkalibrasi (E_STAT §C), sedangkan head yang
   saya pasang saat itu adalah engine 5/27 (E_STAT §B) yang FP-nya 71–98% jendela
   evaluasi. Perbaikan: dipecah jadi dua head — `op_far_calibrated` = L1 (membawa badge
   §C), `calib_5of27` = L2 gating; keduanya diverifikasi terhadap JSON E_STAT (V9).
2. **FAR segmen 60× salah** pada run awal (pakai menit, kampanye pakai jam → n_neg/60).
   Ditemukan lewat V10 (selisih persis 60×) → formula dikoreksi ke konvensi kampanye;
   V10 lalu cocok 10/10.
3. **ML set latih kosong** pada percobaan pertama (data sudah ter-filter ke segmen) →
   driver kini memuat dua salinan: segmen (replay) + semua well (latih LOWO);
   `train_lowo` kini meng-assert set latih/uji tidak kosong.
4. **Timestamp segmen sempat dicetak sebagai tanggal 1970** (ts_bin bukan epoch) →
   diganti menjadi rentang indeks menit + catatan "asal kalender tidak diverifikasi".

## 6. CARA PAKAI

```bash
cd "/mnt/d/Capstone 1"
python3 code/v9_i1_run.py --ml      # replay F-14 + 4 RF head (≈22 detik)
python3 code/v9_i1_run.py           # tanpa ML (≈9 detik)
python3 code/v9_i1_verify.py        # 13 cek independen (≈60 detik; exit 0 = semua PASS)
```

Argumen: `--well <WELLBORE>` (default F-14; well harus ada di dataset D1),
`--outdir <DIR>` (default `scratch/v9_i1`). Keluaran: JSON primer + 2 log (lihat header).

Yang ditampilkan ke manusia per head: `tier`, `layer`, `n_aktif/n`, metrik segmen
(P/R/FP/FAR+satuan), AUPRC (bila head ML), **badge FAR kampanye**, **label keyakinan**,
**batas pemakaian**, `human_review_required`. Ketiadaan data/skala selalu dicetak
dengan kata (BELUM TERSEDIA / BELUM DIJALANKAN / nodata n), bukan angka 0.

## 7. BATAS DAN KETIDAKPASTIAN YANG DITAMPILKAN (wajib dibaca pemakai)

1. **Bukan alarm.** 0 slot alarm otomatis; 11 peringatan L1 = usul yang butuh
   konfirmasi insinyur pengeboran. Keputusan operasional selalu manusia.
2. **Badge FAR = angka kampanye lintas fold; FAR segmen = angka replay F-14.** Keduanya
   dicetak terpisah. FAR segmen BUKAN perkiraan FAR di sumur lain (D-A4: ambang
   tidak portabel — vib τ0,5 menyebar 119× antar well).
3. **Satu lapangan (Volve).** Generalisasi ke lapangan lain belum terukur. Tool_wear =
   domain bengkel (lead detik) — tidak boleh dijumlah dengan lead menit rig (D-A7).
4. **Label proxy / semantik**: hyd = residu SPPA (proxy); hyd K-ii label = proxy +
   data belum ada; STUCK_RT/SHKRSK_RT semantik lintas-well = risiko pra-reg Fase 0;
   bit_wear K-1 P/R tinggi = sifat blok kedalaman (§3.4).
5. **ML di prototipe = ranking.** Ambang operasi pra-reg tidak ditetapkan di sini;
   angka biner pada ambang 0,5 ilustratif. RF hyd-K-i tidak ada (D-A5, by design).
6. **Klaim non-aktif eksplisit**: hyd K-ii (data pit/GAINLOSSTOT belum diparse —
   kendala sensor terukur), bit_wear K-2 (pra-reg belum terbit), tool_wear K-ii RF
   (V9 tidak menjalankan; V8 = referensi).
7. **Waktu**: `ts_bin` = indeks menit internal D1; asal kalender TIDAK diverifikasi di
   sesi ini → jangan ditampilkan sebagai tanggal kalender.
8. **Kualitas sensor terukur di segmen**: nodata CRPM F-14 96,6% (5.268/5.455) —
   deteksi SSI F-14 praktis mati; `SPM_*` kosong di sebagian fold (imputer skip).

## 8. STRESS-TEST DESAIN (what-if-oracle + consciousness-council)

### 8.1 What-if 5 cabang (diterapkan pada keputusan lapisan, bukan spekulasi umum)

| Cabang | Bobot | Skenario | Keputusan I1 yang diuji / hasil |
|---|---|---|---|
| Ω Best | 15% | FAR/B4 terukur penuh → ada kandidat alarm | Prototipe TIDAK menaikkan tier sendiri; jalur kenaikan = syarat §1.3 EVAL_C (per-well calibration) — dicatat sebagai rekomendasi, bukan klaim |
| α Likely | 45% (prioritas 61,8%) | Alat live = L0+L2+L1 terbatas | **Kondisi yang dirakit**: 5 L0 + 9 L2 + 11 L1 (shk/vib/stuck/hyd/tool_wear) + 2 L3 |
| Δ Worst | 20% | FAR tak pernah terukur untuk beberapa engine | Badge menampilkan "belum terukur" (bit_wear P/R/FAR) alih-alih 0; alat tetap koheren di L0+L2 |
| Ψ Wildcard | 10% | Semantik label salah lintas-well | Cek V6 memaksa status non-aktif eksplisit; label proxy dianotasi per head; belum ada klaim onset yang dipakai utk peringatan (B1 rendah → tetap L2) |
| Φ Contrarian | 10% | Rule/persistence sudah cukup, ML tak bernilai | ML dipertahankan sebagai L2 ranking dgn AUPRC tercetak (vib 0,9117) — nilainya TREND, bukan status; hyd tanpa RF (D-A5) = bukti konsistensi pada cabang ini |

Robust lintas cabang: registry tier-terkunci + badge FAR selalu tampil + status
non-aktif eksplisit + assertion 0 alarm.

### 8.2 Consciousness-council (5 arketipe; ketegangan dipertahankan)

- **The Architect**: 7 engine ≠ 7 codebase — modul rule/persistence diimpor dari
  E_RULE (sekali jalan, dipakai ulang); lapisan keputusan tunggal memetakan semua head.
  Risiko over-engineering dijaga: hanya prototipe replay, bukan platform.
- **The Empiricist**: satu-satunya angka yang boleh menentukan tier = EVAL_C; metrik
  segmen hanya bukti konsistensi (V9/V10), bukan dasar kenaikan.
- **The Minimalist**: fitur = kontrak D1 (55/30/27), tanpa rekayasa fitur baru;
  satu driver, satu registry, satu verifier.
- **The Pragmatist**: prioritas cabang α — L0+L2 langsung bernilai hari ini; L1 hanya
  untuk 3 engine rig + tool_wear yang buktinya memang layak.
- **The Contrarian**: "0 alarm" bisa dibaca gagal → kontra: alarm dini tanpa FAR
  terukur justru berbahaya (bukti shk B3 negatif). Ketegangan TIDAK diresolusi dengan
  menurunkan ambang — diresolusi dengan memisahkan L1 (perlu konfirmasi) dari L2 (tren).

**Sintesis**: modularitas + kunci tier + pemisahan L1/L2/L3 + bukti konsistensi
kampanye (V9/V10) = alat koheren yang jujur soal bukti.

## 9. PEMENUHAN ACCEPTANCE KARTU

| Acceptance | Bukti |
|---|---|
| (a) prototipe berjalan di data nyata + output tercetak | `v9_i1_TEST_LOG.txt` 288 baris (7 engine, 27 head, lapisan keputusan), run 21,55 s, JSON 45.879 byte |
| (b) 7 engine terintegrasi | `meta.n_engine = 7`; vib·ssi·shk·stuck(K-i+K-ii)·hyd(K-i+K-ii)·bit_wear·tool_wear semuanya menghasilkan head; cek V1a PASS |
| (c) batas pemakaian dihormati | cek V2 (0 kenaikan tier), V3 (0 alarm otomatis), V4 (engine tren tidak pernah L1; 11/11 L1 ber-badge + ber-batas + human review); tiap head punya kolom `batas_pemakaian` (V1b) |
| (d) keputusan manusia dipertahankan | `human_review_required=true` pada 11 entri L1 + 2 entri L3 (V4b); `keputusan_akhir = MANUSIA`; 0 komponen mencetak output sbg alarm kritis (V3b) |
| (bonus) konsistensi kampanye | V9 (tool_wear == E_STAT §C 4/4 alat) + V10 (replay F-14 == fold E_RULE 10/10) |
| (bonus) determinisme | V7 (2 rerun identik) + V8 (AUPRC ML reproduksi) |

## 10. BELUM DIVERIFIKASI / BELUM TERUKUR (verification-mandatory #3)

- Asal kalender `ts_bin` TIDAK diverifikasi (hanya struktur indeks menit yang diuji).
- FAR segmen F-14 tidak dibandingkan ke fold kampanye untuk head **onset** (E1,
  persistence_event) — V10 hanya mencakup 5 kelas status × 2 head; klaim onset dievaluasi
  kampanye dengan metrik B1/TLead, bukan FAR segmen.
- RF `vib/ssi/shk/stuck` divalidasi lewat AUPRC rerun (V8: 1 head) + determinisme
  run ulang tanpa-ML (V7); kecocokan per-fold AUPRC vs JSON E_ML TIDAK dihitung ulang
  di sesi ini (beda skema: E_ML memakai fold kembar yang sama — belum dicek silang).
- C3/dropout sensor, CI95 bootstrap, dan rekomputasi B1/TLead kampanye = tugas EVAL_*,
  tidak diulang di I1 (bukan bagian DoD).
- Transfer lintas lapangan & kenaikan tier apa pun = BELUM (syarat §1.3 EVAL_C).
- Peringatan L1 pada segmen ini belum diuji terhadap kejadian operasional nyata
  (data inspeksi Volve tidak tersedia) = nilai-B lapisan B untuk run ini BELUM TERUKUR.

## 11. SUMBER

`docs/V9_PM1_ARCHITECTURE.md` (§1 arsitektur, §2 spesifikasi, §4.9 DoD I1) ·
`docs/V9_EVAL_A_LAYERA.md` · `docs/V9_EVAL_B_LAYERB.md` · `docs/V9_EVAL_C_LAYERC.md`
(tier §1, detail §2) · `docs/V9_E_RULE_ENGINE.md` · `docs/V9_E_STAT_ENGINE.md` ·
`docs/V9_E_ML_ENGINE.md` · JSON primer kampanye `scratch/v9_e_rule/v9_e_RULE_01_status_results.json`,
`scratch/v9_e_stat/v9_e_stat_03_tool_wear_RESULTS.json` (dibaca langsung verifikasi) ·
dataset D1 `scratch/v9_d1/datasets/*.csv.gz` + `scratch/v9_d1/bins/F-14.csv.gz` ·
`data/USROP_labeled.csv` · `scratch/v6_e1/toolwear_windows.csv` ·
hasil prototipe `scratch/v9_i1/*`.

*Selesai V9-I1 (`t_34e9b879`). Serah-terima ke: `t_0b5671e0` (A1 audit) → `t_07d88981` (PM2).*
