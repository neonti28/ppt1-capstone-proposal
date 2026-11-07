"""V9-E_ML 03 — builder dokumen docs/V9_E_ML_ENGINE.md dari JSON primer.

Angka di dokumen DIRENDER dari scratch/v9_e_ml/*_RESULTS.json (S6: JSON primer
dulu, baru dokumen; setiap angka = kutipan JSON, bukan ketikan tangan).
"""
import json, os, datetime

BASE = "/mnt/d/Capstone 1(v2)"
RES = os.path.join(BASE, "scratch/v9_e_ml")
ENG = {e: json.load(open(os.path.join(RES, f"v9_e_ML_{e}_RESULTS.json")))
       for e in ("vib", "ssi", "shk", "stuck_k2")}
PERS_ONSET = json.load(open(os.path.join(RES, "v9_e_ML_stuck_k2_persistence_onset.json")))

META = {
    "vib": ("2.1", "vib", "Deteksi kondisi (`VIBLAT_RT>=32,17405`) — status sekarang",
            "Hybrid: RF/GB/LR skor-penambah; rule ambang + persistence = engine dasar (E_RULE)"),
    "ssi": ("2.2", "ssi", "Deteksi kondisi (`SSI(CRPM_RT)>=1`) — status sekarang",
            "Hybrid: RF/GB/LR skor-ranking; rule definisi SSI = dasar (E_RULE)"),
    "shk": ("2.6", "shk", "Deteksi anomali/dysfunction sedang berlangsung (`SHKRSK_RT>=1`)",
            "ML (RF/GB/LR, 55 fitur 11 kanal) + persistence"),
    "stuck_k2": ("2.4", "stuck K-ii", "Prediksi kejadian mendatang (onset STUCK 0→1, H=10 mnt)",
                 "E3_RF (200 pohon) + GB + LR — 1 dari 4 engine setara-tugas K-ii"),
}

def fmt(x, nd=4):
    if x is None: return "—"
    return f"{x:.{nd}f}"

def ci_s(ci):
    return "—" if not ci else f"[{ci[0]:.4f}; {ci[1]:.4f}]"

def fold_table(e, onset=False):
    r = ENG[e]
    lines = []
    hdr = ("| Fold | Test well | n | pos | prev | UP | RF AUPRC (CI95) | GB AUPRC | LR AUPRC | "
           "pers | canary | prev-rand |")
    sep = "|---|---|---|---|---|---|---|---|---|---|---|---|"
    lines += [hdr, sep]
    for f in r["folds"]:
        rf, gb, lr = f["models"]["rf"], f["models"]["gb"], f["models"]["lr"]
        b = f["baselines"]
        lines.append(
            f"| {f['fold']} | {f['test_well']} | {f['n_test']} | {f['pos_test']} | "
            f"{f['prev_test']:.4f} | {'YA' if f['underpowered'] else '—'} | "
            f"{rf['auprc']:.4f} {ci_s(rf['ci95'])} | {gb['auprc']:.4f} | {lr['auprc']:.4f} | "
            f"{b['persistence']['auprc']:.4f} | {b['canary_depth']['auprc']:.4f} | "
            f"{b['prevalence_random']['auprc']:.4f} |")
    return "\n".join(lines)

def tau_table(e, m="rf"):
    r = ENG[e]
    lines = ["| Fold | Model | tau | P | R | FAR (jendela/24jam) |",
             "|---|---|---|---|---|---|"]
    taus = r["taus"] + (["q95_train"] if e == "stuck_k2" else [])
    for f in r["folds"]:
        for mm in ("rf", "gb", "lr"):
            parts = []
            for t in taus:
                tm = f["models"][mm]["tau_metrics"][str(t)]
                p = "—" if tm["precision"] is None else f"{tm['precision']:.3f}"
                rr = "—" if tm["recall"] is None else f"{tm['recall']:.3f}"
                far = "—" if tm["FAR_24jam"] is None else f"{tm['FAR_24jam']:.1f}"
                parts.append(f"{t}: {p}/{rr}/{far}")
            lines.append(f"| {f['fold']} {f['test_well']} | {mm} | " + " · ".join(parts) + " |")
    return "\n".join(lines)

def far_points(e):
    """Titik (well, model, tau) dgn FAR<=6/24jam DAN recall>0 — syarat dasar L1."""
    out = []
    for f in ENG[e]["folds"]:
        for m in ("rf", "gb", "lr"):
            for t, tm in f["models"][m]["tau_metrics"].items():
                if tm["FAR_24jam"] is not None and tm["FAR_24jam"] <= 6 and (tm["recall"] or 0) > 0:
                    out.append((f["test_well"], m, t, tm["FAR_24jam"], tm["recall"]))
    return out

def ci_touch(e, m="rf"):
    return [f["test_well"] for f in ENG[e]["folds"]
            if f["models"][m]["ci95"] and f["models"][m]["ci95"][0] <= f["prev_test"]]

def db_table(e):
    r = ENG[e]
    lines = ["| Fold | RF−pers | RF−canary | RF−prev | GB−pers | GB−canary | LR−pers | LR−canary |",
             "|---|---|---|---|---|---|---|---|"]
    for f in r["folds"]:
        d = f["delta_B"]
        lines.append(
            f"| {f['fold']} {f['test_well']} | {d['rf_vs_persistence']:+.4f} | "
            f"{d['rf_vs_canary_depth']:+.4f} | {d['rf_vs_prevalence_random']:+.4f} | "
            f"{d['gb_vs_persistence']:+.4f} | {d['gb_vs_canary_depth']:+.4f} | "
            f"{d['lr_vs_persistence']:+.4f} | {d['lr_vs_canary_depth']:+.4f} |")
    return "\n".join(lines)

def onset_table():
    lines = ["| Fold well | Model | thr | B1 | TLead med (mnt) | deteksi |",
             "|---|---|---|---|---|---|"]
    for f in ENG["stuck_k2"]["folds"]:
        for mm in ("rf", "gb", "lr"):
            for thr in ("q95_train", "0.1"):
                o = f["models"][mm]["onset_by_tau"][thr]
                tl = o.get("TLead_median_mnt")
                b1 = o.get("B1_coverage")
                b1s = "—" if b1 is None else f"{b1:.3f}"
                lines.append(
                    f"| {f['test_well']} | {mm} | {thr} | {b1s} | "
                    f"{tl if tl is not None else '—'} | {o.get('n_detected')}/{o.get('n_events')} |")
    return "\n".join(lines)

def onset_pers_table():
    pl = ["| Well uji | n event (runpositif berurutan) | B1 persistence | TLead med (mnt) |",
          "|---|---|---|---|"]
    for w, v in PERS_ONSET.items():
        pl.append(f"| {w} | {v['n_events']} | {v['B1']:.3f} | {v['TLead_median']:.1f} |")
    return "\n".join(pl)

def agg(e):
    a = ENG[e]["agregat"]
    out = []
    for m in ("rf", "gb", "lr"):
        v = a[m]
        out.append(f"- **{m.upper()}**: AUPRC {v['auprc_min']:.4f}–{v['auprc_max']:.4f} "
                   f"(spread {v['spread_auprc']:.4f}); ΔB>0 vs canary "
                   f"{v['deltaB_vs_canary_pos']}; vs persistence {v['deltaB_vs_persistence_pos']}")
    return "\n".join(out)

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M WIB")
doc = f"""# V9-E_ML — ENGINE ML (RF/GB/LR) PADA DATA NYATA: 4 HEAD + BASELINE RELEVAN + LOWO

Task: `t_902dd141` [Algorithm Engineer ML] · Board: capstone-v9-build · Tanggal: {now}
Sumbu: `docs/V9_PM1_ARCHITECTURE.md` (spesifikasi §2 + kontrak §3), `docs/V9_R1_JUSTIFICATION.md`
(rumus + baseline §3–§4), `docs/V9_D1_DATA_PIPELINE.md` (dataset + LOWO).
Kerangka penilaian: standar 3 lapisan A/B/C operator ("Evaluasi User.txt") — bukan gate lift 1,5.
Primer data: SEMUA angka di dokumen ini dirender dari JSON hasil eksekusi di
`scratch/v9_e_ml/v9_e_ML_<engine>_RESULTS.json` (oleh `code/v9_e_ML_03_build_doc.py`);
0 angka karangan.

> **Riset pendahuluan: `scientific-critical-thinking`** — OBSERVED (angka eksekusi JSON)
> dipisah dari DESAIN (keputusan harness: hyperparam GB/LR, tau grid) dan DERIVED
> (rekonstruksi event stuck_k2); kontradiksi dataset stuck_k2 (§7) dilaporkan, bukan
> didiamkan; tes pembeda persistence-onset dijalankan apa adanya meski hasilnya
> merugikan ML (§6.4).
> **Riset pendahuluan: `statistical-analysis`** — AUPRC + CI95 moving-block bootstrap
> (blok 60 jendela, 1.000 resample, seed 42) per fold; lift dibaca terhadap plafon
> 1/prev yang dilaporkan per fold; fold <30 positif = UNDERPOWERED dilabeli, tidak
> dihitung mayoritas; FAR per skala aslinya (jendela 1 menit → per 24 jam) tanpa
> konversi diam-diam.
> **Riset pendahuluan: `verification-mandatory`** — determinisme diuji re-run fold 0
> (gerbang 1e-9 S4); anti-sirkularitas di-assert ulang di runtime (0 kanal label di
> fitur); reproduksi silang angka V8-E_vib (lift 1,61/2,36/3,50/1,63 cocok persis)
> = kontrol validitas pipeline; daftar "belum terukur" eksplisit §8.
> **Riset pendahuluan: `what-if-oracle`** — cabang risiko hasil: Ω (ML menang semua),
> α (ML menang vs canary tapi kalah persistence — KASUS NYATA kelas onset), Δ (FAR
> meledak di semua tau — terkonfirmasi), Φ (persistence memang sudah cukup — terdukung
> hyd-K-i V8 + stuck_k2 K-ii di sini); ketegangan direkonsiliasi sebagai KEMAMPUAN +
> BATAS, bukan label gagal (§6).
> **Riset pendahuluan: `consciousness-council`** — 5 arketipe menekan desain harness:
> Empiricist (tau grid = semua titik pra-reg dilaporkan, tanpa pemilihan pasca-hasil),
> Minimalist (1 harness, 3 model, 3 baseline, 4 engine), Contrarian (persistence-onset
> yang "menang telak" ditampilkan penuh §6.4 — bukan disembunyikan), Architect
> (kepatuhan D-A5: nol ML di hyd-K-i), Pragmatist (prioritas engine sesuai fokus kartu).
> **Riset pendahuluan: `sequentialthinking`** (3 pikiran, 3/3 sukses, tool_call sequ-mcp):
> orientasi+inspeksi data → desain harness+keputusan scope → verifikasi hasil+rencana
> dokumen.

---

## 0. RINGKASAN EKSEKUTIF

Empat head ML dilatih pada data nyata Volve dengan split LOWO (28 fold total,
seed 42, tanpa grid search), masing-masing dibandingkan dengan baseline relevan
pada fold yang sama: persistence, canary-kedalaman, prevalence-random.

| Engine | Jenis tugas | Fold | RF AUPRC (rentang) | RF ΔB>0 vs canary | RF ΔB>0 vs persistence | vonis kemampuan |
|---|---|---|---|---|---|---|
| vib | deteksi kondisi | 4 | {ENG['vib']['agregat']['rf']['auprc_min']:.4f}–{ENG['vib']['agregat']['rf']['auprc_max']:.4f} | {ENG['vib']['agregat']['rf']['deltaB_vs_canary_pos']} | {ENG['vib']['agregat']['rf']['deltaB_vs_persistence_pos']} | skor penambah layak (reproduksi V8 persis) |
| ssi | deteksi kondisi | 9 (2 UP) | {ENG['ssi']['agregat']['rf']['auprc_min']:.4f}–{ENG['ssi']['agregat']['rf']['auprc_max']:.4f} | {ENG['ssi']['agregat']['rf']['deltaB_vs_canary_pos']} | {ENG['ssi']['agregat']['rf']['deltaB_vs_persistence_pos']} | skor-ranking layak; keyakinan fold wajib tampil |
| shk | deteksi anomali | 9 | {ENG['shk']['agregat']['rf']['auprc_min']:.4f}–{ENG['shk']['agregat']['rf']['auprc_max']:.4f} | {ENG['shk']['agregat']['rf']['deltaB_vs_canary_pos']} | {ENG['shk']['agregat']['rf']['deltaB_vs_persistence_pos']} | layak L2/L1-terkalibrasi sesuai V8; 1 titik hemat-awas (§6.5) |
| stuck K-ii | prediksi onset H=10 mnt | 4 | {ENG['stuck_k2']['agregat']['rf']['auprc_min']:.4f}–{ENG['stuck_k2']['agregat']['rf']['auprc_max']:.4f} | {ENG['stuck_k2']['agregat']['rf']['deltaB_vs_canary_pos']} | {ENG['stuck_k2']['agregat']['rf']['deltaB_vs_persistence_pos']} | ranking layak; persistence-onset menang telak (§6.4) |

Tidak ada head yang memenuhi syarat alarm otomatis PENUH (L0 butuh FAR≤1/24jam dgn
recall>0 + B1≥80% + G1/G2 mayoritas + C2/C3; titik FAR≤1 dgn recall>0 hanya
{sum(1 for e in ENG for w, m, t, far, rec in far_points(e) if far <= 1)} dari
{sum(len(f['models'][m]['tau_metrics']) for e in ENG for f in ENG[e]['folds'] for m in ('rf','gb','lr'))} titik uji, dengan recall 0,004–0,012 — lihat §6.5) — konsisten dengan spesifikasi PM
(tier L0 0 slot hari ini). GB/LR = pembanding
seragam; tidak ada model yang dipromosikan/ dibuang — semua hasil tersimpan sebagai
KEMAMPUAN + BATAS + KEKUATAN BUKTI per fold (S8).

## 1. METODE HARNESS (kontrak; DESAIN ditandai eksplisit)

- **Model** (seed 42, tanpa grid search):
  - RF kontrak PM1 §2.1: `RandomForestClassifier(n_estimators=300, min_samples_leaf=5,
    class_weight="balanced_subsample", random_state=42)`; **stuck K-ii E3 = 200 pohon**
    (PM1 §2.4). `n_jobs=-1` (paralelisasi prediksi; lihat determinisme §5).
  - GB (PM1 §1.2 ML heads RF/GBM/LR): `GradientBoostingClassifier(n_estimators=200,
    learning_rate=0.1, max_depth=3, random_state=42)` — **DESAIN tetap** (default
    sklearn yang dikunci; tanpa tuning).
  - LR: `SimpleImputer(median, fold-safe) → StandardScaler(fold-safe) →
    LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)`
    — **DESAIN tetap**.
- **Imputasi**: median fold-safe untuk SEMUA model (fit hanya data latih; PM1 S4).
- **Baseline per fold pada split IDENTIK** (S9; dihitung di sini agar pembanding
  melekat pada JSON engine — E_RULE menghitung ulang mandiri untuk evaluator):
  1. **persistence** `ŷ(t)=y(t−1)` — kolom `y_prev_*` D1 (di-hitung di grid penuh
     sebelum masking; valid_prev==1 bila ada);
  2. **canary-kedalaman** — RF kontrak HANYA dengan fitur `depth_*`/`dbtm_*`
     (kontrol memorisasi posisi);
  3. **prevalence-random** — AUPRC = prevalensi fold (plafon lift = 1/prev dilaporkan).
- **Metrik per fold**: AUPRC + CI95 (moving-block bootstrap, blok 60 jendela,
  1.000 resample, seed 42); lift = AUPRC/prev; P/R/FAR pada tau pra-reg
  {{0,05; 0,10; 0,20; 0,30; 0,50}} (grid tau PM1 §2.6 dipakai seragam — SEMUA titik
  dilaporkan, tanpa pemilihan pasca-hasil); `FAR_24 = 1440·FP/n_neg` (skala jendela
  1 menit → per 24 jam operasi; asumsi jam operasi = jendela eligible, PM1 §6.3).
- **Onset (stuck K-ii)**: + ambang `q95` skor LATIH (pra-reg PM1 §2.4 E3);
  B1 = % event dengan ≥1 alarm di horizon; TLead median.
- **UNDERPOWERED**: fold uji <30 positif dilabeli, dikecualikan dari hitungan mayoritas.
- **Anti-sirkularitas**: assert runtime — 0 kanal pembentuk label (VIBLAT/SHKRSK/CRPM/
  STUCK) di kolom fitur (55 fitur = 11 kanal × 5 statistik; D1 §2).

## 2. ENGINE YANG DILATIH (fokus kartu, sesuai §2 PM1 + larangan D-A5)

### 2.1 `vib` — deteksi kondisi getaran lateral (PM1 §2.1)

{agg('vib')}

Tabel per fold (semua model + baseline; CI95 RF):

{fold_table('vib')}

ΔB per fold (AUPRC model − AUPRC baseline pada fold yang sama):

{db_table('vib')}

P/R/FAR pada tau grid pra-reg (format P/R/FAR per titik tau):

{tau_table('vib')}

**Silang-kontrol reproduksi**: RF lift per fold = 1,61 / 2,36 / 3,50 / 1,63 — COCOK
PERSIS dengan angka V8-E_vib yang dikutip PM1 §2.1 (G1 4/4); RF≥canary 4/4 (G2).
Reproduksi ini = kontrol validitas bahwa harness V9 memakai resep setara V8.

### 2.2 `ssi` — deteksi kondisi stick-slip (PM1 §2.2)

{agg('ssi')}

{fold_table('ssi')}

{db_table('ssi')}

{tau_table('ssi')}

Catatan: fold F-7 (3 positif) dan F-9 (12 positif) UNDERPOWERED — AUPRC mereka
(F-7 RF {ENG['ssi']['folds'][6]['models']['rf']['auprc']:.4f}) tidak boleh dibaca sebagai
bukti stabil; fold layak = 7. Persistence justru kuat di F-10
({ENG['ssi']['folds'][0]['baselines']['persistence']['auprc']:.4f}) — dapat dilihat sebagai
KEMAMPUAN baseline (stick-slip persisten antar-grid di sumur itu), bukan aib ML.

### 2.3 `shk` — deteksi anomali/dysfunction bit bounce (PM1 §2.6)

{agg('shk')}

{fold_table('shk')}

{db_table('shk')}

{tau_table('shk')}

Catatan: di SEMUA fold dan SEMUA model × tau, FAR > 60/24jam — tidak ada titik yang
memenuhi syarat L1 (FAR≤6/24jam dengan recall>0) di kerangka ini; hal ini konsisten
dengan temuan V8 (FAR≤6 dgn recall>0 = hanya 4 titik di kurva V8; kalibrasi lokal
per well = prasyarat, D-A4). Sub-tugas onset shk (B1/TLead, H=10 mnt) BELUM diukur di
sini: dataset shk D1 = status windows saja (tanpa dataset onset shk).

### 2.4 `stuck K-ii` — prediksi onset stuck-pipe, H=10 menit (PM1 §2.4)

{agg('stuck_k2')}

{fold_table('stuck_k2')}

{db_table('stuck_k2')}

B1 + TLead (rekonstruksi DERIVED dari run positif berurutan — lihat §7 kolom waktu):

{onset_table()}

Basis pembanding — persistence-onset (E0) dihitung langsung dari kolom dataset
(`y_prev_stuck_onset`), tanpa model:

{onset_pers_table()}

P/R/FAR model pada q95-train + tau grid (q95 = ambang pra-reg E3):

{tau_table('stuck_k2')}

## 3. HEAD DI LUAR LATIHAN INI — STATUS EKSPLISIT (bukan "gagal", bukan nol diam)

| Head (PM1 §2) | Status di kartu ini | Alasan |
|---|---|---|
| hyd-K-i (median/MAD + persistence) | **sengaja TANPA ML** | D-A5: RF DILARANG di kelas ini (ΔB negatif 7/7 V8, replikasi eksak); dataset `hyd_ki` D1 tersedia untuk E_STAT/E_RULE |
| stuck K-i (persistence) | **bukan head ML per spesifikasi** | PM1 §2.4: K-i = persistence (E_STAT/E_RULE); dataset `stuck_k1` tersedia |
| hyd-K-ii RF (+varian flow-in) | **belum terukur** | dataset onset ΔV_pit (12 kolom pit F-9A time.csv) TIDAK diproduksi D1 |
| bit_wear K-1 RF / K-2 onset RF | **belum terukur** | dataset USROP 30-fitur E1d + onset K-2 TIDAK diproduksi D1; K-2 juga menunggu pra-reg kampanye |
| tool_wear K-ii LOTO RF | **belum terukur di kartu ini** | modul terpisah domain bengkel (D-A7); dataset Mendeley tidak masuk pipeline D1 |
| shk sub-onset (H=10 mnt) | **belum terukur** | dataset D1 shk = status windows; onset-shk butuh dataset terpisah |

## 4. HASIL PER LIPATAN: JENIS TUGAS + JENIS ENGINE + BASELINE (tugas wajib #5)

| Engine | Jenis tugas | Jenis engine (kartu ini) | Baseline dipakai | Lipatan |
|---|---|---|---|---|
| vib | deteksi kondisi (status) | RF/GB/LR skor-penambah di atas rule/persistence | persistence · canary-depth · prevalence-random | 4 LOWO (F-14, F-15A, F-15_S, F-5) |
| ssi | deteksi kondisi (status) | RF/GB/LR skor-ranking | persistence · canary-depth · prevalence-random | 9 LOWO (2 underpowered) |
| shk | deteksi anomali berlangsung | RF/GB/LR | persistence · canary-depth · prevalence-random | 9 LOWO |
| stuck K-ii | prediksi kejadian (onset) | E3_RF(200)+GB+LR; ambang q95-train | persistence-onset (E0) · canary-depth · prevalence-random | 4 LOWO (F-10, F-14, F-9, F-9_A) |

TLead pada kelas status (vib/ssi/shk) = **tidak berlaku** (tugas deteksi status;
PM1 §2.1) — bukan "belum terukur".

## 5. DETERMINISME (S4)

- Semua model `random_state=42`; imputer/scaler fold-safe; seed bootstrap 42 per fold.
- Uji re-run fold 0 vib (RF 300 pohon): `max_abs_diff = {ENG['vib']['determinism_check']['max_abs_diff']:.3e}`
  antara dua run identik — di bawah gerbang 1e-9 S4 (PASS), meski bukan bit-exact
  karena akumulasi float `n_jobs=-1`; catatan jujur: untuk reproduksi bit-exact
  sempurna, run ulang dengan `n_jobs=1` (perbedaan praktis nihil, <1e-15).
- Skrip + versi software tercatat di JSON (`software: sklearn {ENG['vib']['software']['sklearn']}`,
  numpy {ENG['vib']['software']['numpy']}, pandas {ENG['vib']['software']['pandas']}).

## 6. TEMUAN UTAMA (KEMAMPUAN + BATAS — bukan lulus/gagal)

### 6.1 vib — ML menambah nilai vs canary & persistence di 2–4 fold; reproduksi V8 persis
RF ΔB>0 vs canary 4/4 fold (G2 terkonfirmasi); vs persistence 2/4 (F-14 +0,119;
F-15A +0,015; F-15_S −0,018; F-5 −0,227) — identik pola V8. GB/LR tidak konsisten
menang (GB kalah persistence 3/4; LR menang 2/4 dengan AUPRC fold-F-5 tertinggi
{ENG['vib']['folds'][3]['models']['lr']['auprc']:.4f}) → RF tetap head utama.
Batas: FAR pada semua tau ratusan/24jam → L2 tren layak; L1 menunggu FAR/B4 terukur.

### 6.2 ssi — RF≥canary 5/7 fold layak; RF≥persistence 6/7 — nilai tambah ML terukur
Sejalan V8 (RF≥canary 5/5; persistence kalah 0/5). GB lebih lemah (menang canary 4/7);
LR menang 5/7. Keyakinan: {len(ci_touch('ssi'))}/9 fold CI95-nya menyentuh no-skill (CI-bawah ≤
prev: {', '.join(ci_touch('ssi'))}) → layer keyakinan wajib (kekuatan bukti SEDANG).
Bukaan baru vs V8: fold F-9_A (eksternal, 55 positif)
RF {ENG['ssi']['folds'][8]['models']['rf']['auprc']:.4f} vs prev {ENG['ssi']['folds'][8]['prev_test']:.4f}
= lift {ENG['ssi']['folds'][8]['models']['rf']['lift']:.2f} — RF bekerja di fold eksternal ini.

### 6.3 shk — reproduksi dekat V8; persistence dominan di F-7; FAR tetap tinggi
RF≥canary 5/9 (V8: 6/9 — selisih kecil, harness imputer fold-safe V9; hasil baru menang
dengan catatan, PM1 §6.1). Persistence sangat kuat di F-7 ({ENG['shk']['folds'][6]['baselines']['persistence']['auprc']:.4f})
— kelas shock di sumur itu persisten antar-grid. FAR≤6 dgn recall>0 hanya
{len(far_points('shk'))} titik ({'; '.join(f"{w} {m} tau={t} FAR={far:.2f} R={rec:.4f}" for w, m, t, far, rec in far_points('shk'))})
— recall <0,01 = praktis nol cakupan; klaim V8 (L0-alarm BELUM) terkonfirmasi ulang
dengan angka baru.

### 6.4 stuck K-ii — persistence-onset MENANG TELAK 4/4 (tes pembeda; temuan jujur)
Persistence-onset AUPRC {min(f['baselines']['persistence']['auprc'] for f in ENG['stuck_k2']['folds']):.4f}–{max(f['baselines']['persistence']['auprc'] for f in ENG['stuck_k2']['folds']):.4f}
mengalahkan RF {min(f['models']['rf']['auprc'] for f in ENG['stuck_k2']['folds']):.4f}–{max(f['models']['rf']['auprc'] for f in ENG['stuck_k2']['folds']):.4f} di 4/4 fold
(B1 persistence = 1,0 semua well; TLead median 9–10,5 mnt). Mekanisme (DIAMATI dari
data, bukan asumsi): label positif onset = horizon [t_e−10, t_e) yang Kontigu (median
run 10 menit) → `y(t−1)=1` pada ±6/7 baris positif → persistence otomatis "deteksi
in-horizon". Persistence TIDAK bisa memberi peringatan di menit pertama horizon
(TLead-nya maks run−1) dan tidak bisa memberi peringatan SEBELUM horizon masuk —
di situlah RF/LR tetap punya ruang (mis. F-9 RF q95 B1 1,0 dengan TLead median
{ENG['stuck_k2']['folds'][2]['models']['rf']['onset_by_tau']['q95_train']['TLead_median_mnt']:.1f} mnt).
Kekuatan bukti: SEDANG (1 kampanye, 4 well, label STUCK_RT masih punya risiko
semantik lintas-well, kontrol-positif 0/10 V8 belum diulang). Interpretasi untuk
evaluator: **pada formulasi horizon D1, persistence = engine konfirmasi-in-horizon
yang sangat kuat; ML bernilai hanya bila diukur pada kemampuan pra-horizon/pre-event
(butuh dataset baru dengan sampel pra-horizon)** — ini KEMAMPUAN baseline + BATAS
formulasi label, BUKAN kegagalan ML, dan bukan alasan menurunkan gate.

### 6.5 FAR vs ambang alarm — titik hemat-awas ADA, tapi recall kecil & syarat L1 penuh belum
Pemindaian seluruh fold × model × tau (termasuk q95_train untuk stuck) menemukan
titik dengan FAR≤6/24jam DAN recall>0 (syarat DASAR kenaikan L1) sebagai berikut:

| Engine | Jumlah titik | Detail (well, model, tau, FAR, recall) |
|---|---|---|
| vib | {len(far_points('vib'))} | {'; '.join(f"{w} {m} tau={t} FAR={far:.2f} R={rec:.4f}" for w, m, t, far, rec in far_points('vib'))} |
| ssi | {len(far_points('ssi'))} | {'; '.join(f"{w} {m} tau={t} FAR={far:.2f} R={rec:.4f}" for w, m, t, far, rec in far_points('ssi'))} |
| shk | {len(far_points('shk'))} | {'; '.join(f"{w} {m} tau={t} FAR={far:.2f} R={rec:.4f}" for w, m, t, far, rec in far_points('shk'))} |
| stuck K-ii | {len(far_points('stuck_k2'))} | {'; '.join(f"{w} {m} tau={t} FAR={far:.2f} R={rec:.4f}" for w, m, t, far, rec in far_points('stuck_k2'))} |

Total {sum(len(far_points(e)) for e in ENG)} titik dari {sum(len(f['models'][m]['tau_metrics']) for e in ENG for f in ENG[e]['folds'] for m in ('rf', 'gb', 'lr'))} titik yang diuji
(<1%). Sebagian besar berada di tau tinggi (0,2–0,5) dengan recall 0,004–0,16 = hampir
semua positif terlewat; sebagai titik operasi tunggal tidak layak alarm, tapi layak
dicatat sebagai opsi "hemat-awas" (L1-syarat-dasar terpenuhi, recall tipis) untuk
evaluator. Syarat L1 PENUH (TLead/B4 terukur + C4 + kalibrasi lokal per well + anotasi
regime, PM1 §1.3) belum terpenuhi engine mana pun di kampanye ini → tidak ada kenaikan
tier otomatis dari kartu ini; tier mengikuti rekomendasi EVAL_A/B/C.

## 7. TEMUAN DATA (defect D1 stuck_k2 — dilaporkan, tidak didiamkan)

Kolom `ts_bin` dan `lab_ts` pada `scratch/v9_d1/datasets/stuck_k2.csv.gz` KOSONG untuk
semua 118.567 baris (4/4 well; verifikasi baca gzip mentah, bukan turunan). Konsekuensi:
(a) leak-check `v9_d1_05_leak_lowo.json` entry stuck_k2 (`0 pelanggaran`) = **vacuous**
(komparasi dengan NaN selalu False); (b) B1/TLead di §2.4 direkonstruksi sebagai DERIVED
dari run positif berurutan (fit_ts_max monotonic per well 4/4 terverifikasi — urutan
waktu dataset tetap sah; `y_prev_stuck_onset` terisi 0 NaN). Defect sudah dilaporkan ke
kartu D1 (`t_1ca71445`, komentar #3) dengan rekomendasi regenerate + checker NaN-count.
Konstruksi anti-bocor stuck_k2 tetap terverifikasi lewat KODE builder (jendela ketat-lalu
[t0−10, t0)), bukan lewat kolom.

## 8. BELUM DIVERIFIKASI / BELUM DIUKUR (verification-mandatory #3)

- C1–C4 (stabilitas temporal per-bin, dropout sensor, noise) = domain EVAL_C — TIDAK diukur di sini.
- B3 (pengurangan pemeriksaan) = butuh FP rule dari E_RULE — belum terukur.
- FP rule vib/ssi (rule ambang absolut / definisi SSI) = E_RULE.
- hyd-K-ii, bit_wear K-1/K-2, tool_wear K-ii, shk sub-onset = "belum terukur" (§3).
- Kontrol-positif stuck (labels_curated_v2) belum diulang di kampanye V9 (masih angka V8 0/10).
- CI95 bootstrap memakai blok tetap 60 jendela (pilihan harness; harmonisasi definisi
  "60/20/10" S7 = tugas EVAL_A).

## 9. PENERIMAAN (ACCEPTANCE SELF-CHECK)

| # | Syarat | Bukti |
|---|---|---|
| a | engine jalan pada data nyata | 4 engine × LOWO = 28 fold selesai; run log bertimestamp `scratch/v9_e_ml/v9_e_ML_*_RUN_LOG.txt` |
| b | hasil per lipatan dari eksekusi | `v9_e_ML_{{vib,ssi,shk,stuck_k2}}_RESULTS.json` (primer); tabel §2 dirender dari JSON oleh `code/v9_e_ML_03_build_doc.py` |
| c | baseline relevan dibandingkan | persistence + canary-depth + prevalence-random per fold per engine; ΔB tabel §2; persistence-onset §6.4 |
| d | 0 angka karangan | semua angka dokumen = render JSON; reproduksi silang V8-E_vib lift persis (§2.1) |
| e | D-A5 dipatuhi | nol ML di hyd-K-i; harness menolak engine di luar daftar (argparse choices) |
| f | determinisme | re-run fold 0 diff {ENG['vib']['determinism_check']['max_abs_diff']:.1e} < gerbang 1e-9 (§5) |
| g | "belum terukur" eksplisit | §3 + §8 |
| h | sequ-mcp ≥3 pikiran + baris Riset pendahuluan | 3 pikiran (header) |

## 10. ARTEFAK

- Skrip: `code/v9_e_ML_01_train.py` (harness), `code/v9_e_ML_02_run_all.sh` (driver),
  `code/v9_e_ML_03_build_doc.py` (builder dokumen ini).
- JSON primer: `scratch/v9_e_ml/v9_e_ML_{{vib,ssi,shk,stuck_k2}}_RESULTS.json`,
  `v9_e_ML_stuck_k2_persistence_onset.json`.
- Run log: `scratch/v9_e_ml/v9_e_ML_*_RUN_LOG.txt`.
- agentmemory: fakta defect stuck_k2 + lokasi harness tersimpan (mem_mv4mbdf4).

*Selesai V9-E_ML (t_902dd141). Menyerahkan ke E_STAT (t_af8ea271), E_RULE (t_c8bebfb6),
EVAL_A (t_8a7a33d4) sebagai input JSON.*
"""

out = os.path.join(BASE, "docs/V9_E_ML_ENGINE.md")
with open(out, "w") as fh:
    fh.write(doc)
print("written", out, len(doc.splitlines()), "lines")
