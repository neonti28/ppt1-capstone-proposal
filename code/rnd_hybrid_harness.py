#!/usr/bin/env python3
"""RND hybrid harness bersama untuk kartu S1, S2, dan S3.

Tujuan: satu tempat untuk memuat data, membangun gerbang rule kanal, menjalankan
detektor statistik, mengevaluasi per fold pada satuan yang konsisten, dan menulis
artefak JSON. Kartu S2 (vib, ssi) dan S3 (bit_wear) WAJIB memakai modul ini,
bukan menulis harness kedua.

API publik
----------
Muat data
    muat_dataset(path) -> DataFrame
    pecah_well(df) -> dict[str, DataFrame]        # tiap well diurutkan per ts_bin
    muat_fold(path) -> list[dict]                 # daftar fold LOWO/LOTO

Komponen detektor
    seri_z(well, ts, chan, binsd) -> (z, ok)      # residual kanal per bin aliran
    gerbang_rule(well, ts, chan, thr, binsd)      # rule kanal kausal, bin t-1
    cusum_alarm(z, h, k, reset)                   # CUSUM dua sisi
    jendela_alarm(alarm, w)                       # alarm ditahan w menit
    pilih_h(z_cal, budget, grid)                  # ambang CUSUM dari well kalibrasi
    detektor_stat_rule(well, ts, cal_well, cal_ts, chan, ...) -> dict
        Kunci hasil: rule, stat, h1 (stat DAN rule), h1b (stat ATAU rule), h.

Komponen ML (dipakai S2 dan S3)
    fitur_dari(df) -> list[str]                   # membuang kolom bocor dan meta
    latih_lgb(X, y, seed) -> model
    threshold_conformal(y_cal, skor_cal, alpha) -> float
    skor_ml_fold(well_df, fold, target, feats, seed, alpha) -> dict
        Kunci hasil: skor, ambang, cal_well, n_latih, n_pos_latih.

Evaluasi
    evaluasi_fold(y, pred, ts) -> dict
        Memuat rows, events, cakupan, far24_kalender, far24_kalender_kejadian,
        far24_baris (satuan V9), garwood_atas_fp, lead, separuh, prev.
    ringkas_records(records, model) -> dict
        Median, min, maks, total, dan jumlah fold yang lolos FAR <= 6.

Penulisan
    tulis_json(path, obj) -> str
    sidik_metrik(records, model) -> dict          # sidik determinisme antar seed

Aturan yang dipegang modul ini
------------------------------
1. Semua sinyal pada titik keputusan t hanya memakai informasi sampai t-1
   (gerbang rule) atau sampai t (CUSUM pada z yang sudah tersedia), tanpa label.
2. Ambang CUSUM dipilih dari well kalibrasi di dalam daftar train_wells, bukan
   dari well uji.
3. FAR dilaporkan pada dua satuan sekaligus: kalender dan baris negatif. Satuan
   kalender adalah satuan gate; satuan baris dipakai supaya sebanding dengan
   angka pra-riset V9 yang memakai satuan itu.
4. Seed hanya memengaruhi komponen ML. H1 (statistik + rule) tidak memakai RNG,
   sehingga seed dicatat untuk kelengkapan artefak dan untuk uji determinisme.
"""

from __future__ import annotations

import json
import os
import time

import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
DSD = f"{BASE}/scratch/v9_d1/datasets"
BINSD = f"{BASE}/scratch/v9_d1/bins"
LOWOD = f"{BASE}/scratch/v9_d1"

# Konvensi gate dan operasi (sama dengan R8 supaya bisa direproduksi).
ALPHA_BUDGET = 6.0 / 1440.0   # FAR 6 per 24 jam kalender
LEAD_HORIZON = 60             # menit
W_JENDELA = 10                # menit, alarm ditahan
CUSUM_K = 0.5
H_GRID = (0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30)
FAR_MAKS = 6.0
RECALL_MIN = 0.50
CAKUPAN_MIN = 0.50

LABEL_COLS = ("y_", "valid_prev_", "obs_", "anom_", "lab_")
META_COLS = ("well", "ts_bin", "feat_ts_max", "lab_ts", "lab_kind", "tool", "run",
             "file", "start_sample")


# --------------------------------------------------------------------- utilitas
def log(msg, store=None):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if store is not None:
        store.append(line)
    return line


def tulis_json(path, obj):
    """Tulis JSON dengan indent 1 dan kembalikan path absolutnya."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=float)
    return os.path.abspath(path)


def muat_dataset(path):
    """Muat dataset menit dari CSV/CSV.GZ."""
    return pd.read_csv(path)


def pecah_well(df, kolom="well"):
    """Pecah DataFrame jadi dict per well, terurut ts_bin, indeks direset."""
    out = {}
    for w in sorted(df[kolom].unique()):
        out[w] = df[df[kolom] == w].sort_values("ts_bin").reset_index(drop=True)
    return out


def muat_fold(path):
    """Muat daftar fold dari lowo_*.json (kunci 'folds')."""
    with open(path) as f:
        return json.load(f)["folds"]


# ------------------------------------------------------------ komponen detektor
def seri_z(well, ts, chan="SPPA", flow="TFLO", binsd=BINSD):
    """Residual kanal per bin aliran, diselaraskan ke grid ts.

    Resep sama dengan pembentuk label: qcut(flow, 10), median dan MAD per bin,
    z = (x - median) / (1.4826 * MAD). Fungsi ini tidak menyentuh label.
    Mengembalikan (z, ok): z bernilai 0 di luar cakupan, ok menandai baris yang
    benar-benar punya nilai z.
    """
    b = pd.read_csv(f"{binsd}/{well}.csv.gz")
    d = b.dropna(subset=[f"{chan}_mean", f"{flow}_mean"]).copy()
    d = d[d[f"{flow}_mean"] > 0]
    if len(d) < 50:
        return np.zeros(len(ts)), np.zeros(len(ts), bool)
    try:
        d["qbin"] = pd.qcut(d[f"{flow}_mean"], 10, labels=False, duplicates="drop")
    except ValueError:
        d["qbin"] = 0
    med = d.groupby("qbin")[f"{chan}_mean"].transform("median")
    mad = d.groupby("qbin")[f"{chan}_mean"].transform(lambda s: (s - s.median()).abs().median())
    d["z"] = (d[f"{chan}_mean"] - med) / (1.4826 * mad.replace(0, np.nan))
    d = d.dropna(subset=["z"]).sort_values("ts_bin")
    m = pd.Series(d["z"].to_numpy(), index=d["ts_bin"].to_numpy()).reindex(np.asarray(ts, dtype=int))
    return np.nan_to_num(m.to_numpy(dtype=float), nan=0.0), m.notna().to_numpy()


def gerbang_rule(well, ts, chan="SPPA", thr=2.0, binsd=BINSD):
    """Rule kanal kausal: |z| kanal pada bin (t-1) melewati ambang dan teramati."""
    zv, ok = seri_z(well, np.asarray(ts, dtype=int) - 1, chan=chan, binsd=binsd)
    return ((np.abs(zv) > thr) & ok).astype(int)


def cusum_alarm(z, h, k=CUSUM_K, reset=True):
    """CUSUM dua sisi pada deret z. reset=True mengembalikan akumulator ke 0."""
    z = np.asarray(z, float)
    n = len(z)
    cp = np.zeros(n)
    cn = np.zeros(n)
    a = np.zeros(n, int)
    for i, v in enumerate(z):
        pp = cp[i - 1] if i else 0.0
        pn = cn[i - 1] if i else 0.0
        cp[i] = max(0.0, pp + (v - k))
        cn[i] = max(0.0, pn + (-v - k))
        if cp[i] > h or cn[i] > h:
            a[i] = 1
            if reset:
                cp[i] = 0.0
                cn[i] = 0.0
    return a


def jendela_alarm(alarm, w=W_JENDELA):
    """Tahan alarm selama w menit ke depan (zona peringatan)."""
    a = np.asarray(alarm, int)
    if w <= 1:
        return a
    out = np.zeros_like(a)
    for i in np.flatnonzero(a):
        out[i:i + w] = 1
    return out


def pilih_h(z_cal, budget=ALPHA_BUDGET, grid=H_GRID):
    """Ambil h terkecil pada grid yang laju alarmnya masih di bawah anggaran.

    Grid diurut naik, sehingga nilai pertama yang memenuhi anggaran adalah h
    terkecil yang sah. Bila tidak ada yang memenuhi, pakai grid terbesar.
    """
    for h in grid:
        if cusum_alarm(z_cal, h).mean() <= budget:
            return float(h)
    return float(grid[-1])


def detektor_stat_rule(well, ts, cal_well, cal_ts, chan="SPPA", alpha=ALPHA_BUDGET,
                       w=W_JENDELA, binsd=BINSD):
    """Rakit empat sinyal satu fold: rule, stat, h1, h1b.

    h1  = stat DAN rule   (komposisi H1 pada R8)
    h1b = stat ATAU rule  (pembanding cakupan)
    """
    zv, _ = seri_z(well, ts, chan=chan, binsd=binsd)
    zc, _ = seri_z(cal_well, cal_ts, chan=chan, binsd=binsd)
    h = pilih_h(zc, budget=alpha)
    stat = jendela_alarm(cusum_alarm(zv, h), w)
    rule = gerbang_rule(well, ts, chan=chan, binsd=binsd)
    return dict(rule=rule, stat=stat,
                h1=((stat == 1) & (rule == 1)).astype(int),
                h1b=((stat == 1) | (rule == 1)).astype(int), h=h)


# ---------------------------------------------------------------- komponen ML
def fitur_dari(df):
    """Kolom numerik yang sah jadi fitur: tanpa kolom label dan tanpa kolom meta."""
    drop = [c for c in df.columns if c.startswith(LABEL_COLS) or c in META_COLS]
    feats = [c for c in df.columns if c not in drop and pd.api.types.is_numeric_dtype(df[c])]
    assert "ts_bin" not in feats and "feat_ts_max" not in feats, "kolom bocor masuk fitur"
    return feats


def latih_lgb(X, y, seed=42):
    """LightGBM klasifikasi dengan setelan R8 (dipakai S2 supaya sebanding)."""
    import lightgbm as lgb
    m = lgb.LGBMClassifier(n_estimators=150, learning_rate=0.08, num_leaves=31,
                           min_child_samples=40, subsample=0.9, subsample_freq=1,
                           colsample_bytree=0.9, random_state=seed, n_jobs=2,
                           verbose=-1)
    m.fit(X, y)
    return m


def threshold_conformal(y_cal, skor_cal, alpha=ALPHA_BUDGET):
    """Ambang conformal sederhana: kuantil (1-alpha) dari skor negatif kalibrasi."""
    neg = np.asarray(skor_cal)[np.asarray(y_cal) == 0]
    if len(neg) == 0:
        return float(np.max(skor_cal))
    return float(np.quantile(neg, 1.0 - alpha))


def skor_ml_fold(well_df, fold, target, feats, seed=42, alpha=ALPHA_BUDGET):
    """Latih ML pada train_wells kecuali satu well kalibrasi, nilai well uji.

    Well kalibrasi = train_wells[0], sama dengan R8. Well uji tidak pernah masuk
    pelatihan maupun kalibrasi.
    """
    w = fold["test_well"]
    cal = fold["train_wells"][0]
    tr = [t for t in fold["train_wells"] if t != cal]
    Xtr = pd.concat([well_df[t][feats] for t in tr])
    ytr = pd.concat([well_df[t][target] for t in tr]).to_numpy(int)
    m = latih_lgb(Xtr, ytr, seed=seed)
    skor_cal = m.predict_proba(well_df[cal][feats])[:, 1]
    y_cal = well_df[cal][target].to_numpy(int)
    ambang = threshold_conformal(y_cal, skor_cal, alpha)
    skor = m.predict_proba(well_df[w][feats])[:, 1]
    return dict(skor=skor, ambang=ambang, cal_well=cal,
                n_latih=int(len(Xtr)), n_pos_latih=int(ytr.sum()))


# ------------------------------------------------------------------- evaluasi
def rows_metrics(y, pred):
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    return dict(tp=tp, fp=fp, fn=fn, tn=tn,
                precision=(tp / (tp + fp)) if (tp + fp) else None,
                recall=(tp / (tp + fn)) if (tp + fn) else None,
                menit_alarm=int(pred.sum()), n_pos=int(y.sum()),
                n_neg=int((y == 0).sum()))


def event_metrics(y, pred):
    """Satuan kejadian: satu deret pred==1 berurutan dihitung satu kejadian."""
    y = np.asarray(y).astype(int)
    pred = np.asarray(pred).astype(int)
    runs, i, n = [], 0, len(pred)
    while i < n:
        if pred[i] == 1:
            j = i
            while j < n and pred[j] == 1:
                j += 1
            runs.append((i, j))
            i = j
        else:
            i += 1
    tp_ev = sum(1 for a, b in runs if y[a:b].sum() > 0)
    fp_ev = sum(1 for a, b in runs if y[a:b].sum() == 0)
    return dict(tp_kejadian=int(tp_ev), fp_kejadian=int(fp_ev), n_kejadian=len(runs))


def garwood_atas(k, menit_neg_kal, alpha=0.95):
    """Batas atas dua sisi 95 persen (Garwood) untuk laju alarm per 24 jam."""
    from scipy.stats import chi2
    hi = chi2.ppf(1 - (1 - alpha) / 2, 2 * (k + 1)) / 2.0
    return round(float(hi / (menit_neg_kal / 1440.0)), 4)


def lead_time(y, alarm, horizon=LEAD_HORIZON):
    """Untuk tiap onset, cari alarm terakhir di dalam [onset-horizon, onset)."""
    y = np.asarray(y).astype(int)
    alarm = np.asarray(alarm).astype(int)
    onset_idx = np.flatnonzero((y[1:] == 1) & (y[:-1] == 0)) + 1
    if len(y) and y[0] == 1:
        onset_idx = np.concatenate([[0], onset_idx])
    leads, warned = [], 0
    for o in onset_idx:
        lo = max(0, o - horizon)
        seg = np.flatnonzero(alarm[lo:o])
        if len(seg):
            warned += 1
            leads.append(int(o - (lo + seg[-1])))
    return dict(n_onset=int(len(onset_idx)), n_diperingatkan=int(warned),
                lead_median_min=float(np.median(leads)) if leads else None,
                lead_min_min=int(min(leads)) if leads else None,
                lead_maks_min=int(max(leads)) if leads else None)


def separuh(ts, y, pred):
    """Lapisan C dalam well yang sama: pecah pada median waktu."""
    med = float(np.median(ts))
    out = {}
    for nama, m in (("awal", ts <= med), ("akhir", ts > med)):
        if m.sum() == 0:
            continue
        r = rows_metrics(y[m], pred[m])
        out[nama] = dict(precision=r["precision"], recall=r["recall"],
                         fp=r["fp"], n_pos=r["n_pos"])
    return out


def evaluasi_fold(y, pred, ts):
    """Rekap satu fold pada dua satuan FAR plus cakupan, lead, dan separuh.

    far24_kalender = fp / ((menit_kalender - n_pos) / 1440), satuan gate.
    far24_baris    = fp / ((n_neg / 60) / 24), satuan yang dipakai V9 pra-riset.
    """
    r = rows_metrics(y, pred)
    ev = event_metrics(y, pred)
    ts = np.asarray(ts)
    menit_kal = float(ts.max() - ts.min() + 1)
    menit_neg_kal = max(menit_kal - r["n_pos"], 1.0)
    jam_neg = max(r["n_neg"] / 60.0, 1e-9)
    return dict(
        rows=r, events=ev,
        cakupan=round(len(ts) / menit_kal, 4) if menit_kal else None,
        menit_kalender=menit_kal,
        menit_neg_kalender=round(menit_neg_kal, 1),
        far24_kalender=round(r["fp"] / (menit_neg_kal / 1440.0), 4),
        far24_kalender_kejadian=round(ev["fp_kejadian"] / (menit_neg_kal / 1440.0), 4),
        far24_baris=round(r["fp"] / jam_neg * 24.0, 4),
        garwood_atas_fp=garwood_atas(r["fp"], menit_neg_kal),
        lead=lead_time(y, pred),
        separuh=separuh(ts, y, pred),
        prev=round(float(np.asarray(y).mean()), 6),
        gate_A_baru=bool(r["fp"] / (menit_neg_kal / 1440.0) <= FAR_MAKS
                         and (len(ts) / menit_kal) >= CAKUPAN_MIN
                         and (r["recall"] or 0) >= RECALL_MIN),
    )


# ------------------------------------------------------------------ peringkat
def _vals(xs):
    return [x for x in xs if x is not None]


def _med(xs):
    v = _vals(xs)
    return round(float(np.median(v)), 4) if v else None


def _min(xs):
    v = _vals(xs)
    return round(float(min(v)), 4) if v else None


def _maks(xs):
    v = _vals(xs)
    return round(float(max(v)), 4) if v else None


def _rentang(xs):
    v = _vals(xs)
    return round(float(max(v) - min(v)), 4) if v else None


def ringkas_records(records, model=None):
    """Ringkas daftar rekaman satu model: total, median, min, maks, rentang."""
    sub = [r for r in records if model is None or r.get("model") == model]
    if not sub:
        return dict(n_fold=0)
    return dict(
        n_fold=len(sub),
        fp_total=int(sum(r["rows"]["fp"] for r in sub)),
        tp_total=int(sum(r["rows"]["tp"] for r in sub)),
        fp_kejadian_total=int(sum(r["events"]["fp_kejadian"] for r in sub)),
        precision_median=_med([r["rows"]["precision"] for r in sub]),
        precision_min=_min([r["rows"]["precision"] for r in sub]),
        precision_maks=_maks([r["rows"]["precision"] for r in sub]),
        recall_median=_med([r["rows"]["recall"] for r in sub]),
        recall_min=_min([r["rows"]["recall"] for r in sub]),
        recall_maks=_maks([r["rows"]["recall"] for r in sub]),
        far24_kalender_median=_med([r["far24_kalender"] for r in sub]),
        far24_kalender_min=_min([r["far24_kalender"] for r in sub]),
        far24_kalender_maks=_maks([r["far24_kalender"] for r in sub]),
        far24_kalender_rentang=_rentang([r["far24_kalender"] for r in sub]),
        far24_baris_median=_med([r["far24_baris"] for r in sub]),
        far24_baris_min=_min([r["far24_baris"] for r in sub]),
        far24_baris_maks=_maks([r["far24_baris"] for r in sub]),
        cakupan_median=_med([r["cakupan"] for r in sub]),
        lead_median_median=_med([r["lead"]["lead_median_min"] for r in sub]),
        lead_median_min=_min([r["lead"]["lead_median_min"] for r in sub]),
        lead_median_maks=_maks([r["lead"]["lead_median_min"] for r in sub]),
        n_onset=int(sum(r["lead"]["n_onset"] for r in sub)),
        n_diperingatkan=int(sum(r["lead"]["n_diperingatkan"] for r in sub)),
        fold_far_le6=int(sum(1 for r in sub if r["far24_kalender"] <= FAR_MAKS)),
        fold_gate_A_baru=int(sum(1 for r in sub if r["gate_A_baru"])),
        fold_recall_gt0=int(sum(1 for r in sub if (r["rows"]["recall"] or 0) > 0)),
    )


def sidik_metrik(records, model):
    """Sidik determinisme: nilai yang dipakai membandingkan seed.

    Kembaliannya tuple-tuple yang bisa dibandingkan langsung antar seed, tanpa
    pembulatan tambahan, supaya delta nol benar-benar nol.
    """
    sub = [r for r in records if r.get("model") == model]
    return dict(
        fp_per_fold=[int(r["rows"]["fp"]) for r in sub],
        tp_per_fold=[int(r["rows"]["tp"]) for r in sub],
        far24_kalender_per_fold=[r["far24_kalender"] for r in sub],
        precision_per_fold=[r["rows"]["precision"] for r in sub],
        recall_per_fold=[r["rows"]["recall"] for r in sub],
        lead_per_fold=[r["lead"]["lead_median_min"] for r in sub],
        h_per_fold=[r.get("h_terpilih") for r in sub],
    )


# ------------------------------------------------------------------ runner H1
def jalankan_h1(seed=42, dataset=None, fold_path=None, chan="SPPA",
                alpha=ALPHA_BUDGET, well_df=None, folds=None):
    """Jalankan H1 (statistik DAN rule) pada hyd K-i, sembilan fold LOWO.

    Parameter seed hanya dicatat di rekaman. H1 tidak memakai RNG: z, rule,
    CUSUM, dan pemilihan h semuanya deterministik. Kalau pemanggil butuh
    komponen stokastik, pakai skor_ml_fold dan rakit sendiri di kartu S2/S3.
    """
    if well_df is None:
        well_df = pecah_well(muat_dataset(dataset or f"{DSD}/hyd_ki.csv.gz"))
    if folds is None:
        folds = muat_fold(fold_path or f"{LOWOD}/lowo_hyd_ki.json")
    rows = []
    for f in folds:
        w = f["test_well"]
        d = well_df[w]
        y = d["y_hyd"].to_numpy(int)
        ts = d["ts_bin"].to_numpy(int)
        cal = f["train_wells"][0]
        dc = well_df[cal]
        sig = detektor_stat_rule(w, ts, cal, dc["ts_bin"].to_numpy(int), chan=chan, alpha=alpha)
        for nama, pred in (("rule_kanal", sig["rule"]), ("stat_cusum", sig["stat"]),
                           ("H1_stat_dan_rule", sig["h1"]), ("H1b_stat_atau_rule", sig["h1b"])):
            rec = evaluasi_fold(y, pred, ts)
            rec.update(dict(fold=w, model=nama, seed=int(seed), h_terpilih=sig["h"],
                            cal_well=cal, n=len(y), n_pos=int(y.sum())))
            rows.append(rec)
    return rows
