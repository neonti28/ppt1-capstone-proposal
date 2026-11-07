"""Eksperimen H2O vs baseline pada dataset Volve (skema terverifikasi dari npz).

Sumber data, diperiksa langsung dari berkas:
- features_timeseries_controls_berdata.npz : 3.958 baris kontrol, kolom y seluruhnya 0, 480 fitur.
- features_timeseries.npz                  : 661 kejadian, 480 fitur identik, punya kolom
  category, fold, wellbore.

Definisi kelas, dinyatakan terbuka supaya bisa diuji ulang:
- Positif = kejadian dengan bukti kegagalan: bha_stuck_fishing, bha_downhole_equipment,
  wellbore_fluid, surface_rig_equipment, wireline_completion_intervention, safety_personnel.
- Negatif = 3.958 kontrol + kejadian routine_no_failure_evidence, mixed_evidence,
  failure_unlocated.

Uji: leave-one-well-out pada 7 sumur. Baseline mayoritas, regresi logistik, Random Forest.
Pembanding H2O AutoML dengan fold_column internal. Metrik utama AUPRC karena kelas tidak
seimbang, disertai AUC serta presisi/recall pada ambang 0,5.

Keluaran: JSON di scratch/h2o/. Tidak ada angka yang ditulis tanpa berasal dari eksekusi.
"""
import json
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
os.environ.setdefault("JAVA_HOME", "/home/neonti/.local/jdk17")

DATA = Path("/mnt/d/ARCT-9F2/data/predictive")
OUT = Path("/mnt/d/ARCT-9F2/scratch/h2o")
OUT.mkdir(parents=True, exist_ok=True)
SEED = 42

POSITIF = {
    "bha_stuck_fishing", "bha_downhole_equipment", "wellbore_fluid",
    "surface_rig_equipment", "wireline_completion_intervention", "safety_personnel",
}


def bersihkan(nama):
    """Nama kolom harus tanpa spasi dan tanda baca agar aman di H2O maupun sklearn."""
    hasil, dilihat = [], {}
    for n in nama:
        s = "".join(c if c.isalnum() else "_" for c in str(n)).strip("_") or "kolom"
        if s in dilihat:
            dilihat[s] += 1
            hasil.append(f"{s}_{dilihat[s]}")
        else:
            dilihat[s] = 0
            hasil.append(s)
    return hasil


def metrik(y_true, skor, ambang=0.5):
    y_pred = (skor >= ambang).astype(int)
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"presisi": round(prec, 4), "recall": round(rec, 4), "f1": round(f1, 4),
            "tp": tp, "fp": fp, "fn": fn}


def muat():
    k = np.load(DATA / "features_timeseries_controls_berdata.npz", allow_pickle=True)
    e = np.load(DATA / "features_timeseries.npz", allow_pickle=True)
    nama_k = list(map(str, k["feature_names"]))
    nama_e = list(map(str, e["feature_names"]))
    if nama_k != nama_e:
        raise SystemExit("nama fitur dua berkas tidak identik; berhenti supaya tidak salah gabung")
    fitur = bersihkan(nama_k)

    dk = pd.DataFrame(k["X"], columns=fitur)
    dk["target"] = 0
    dk["sumber"] = "kontrol"
    dk["wellbore"] = [str(x) for x in k["fold"]]

    de = pd.DataFrame(e["X"], columns=fitur)
    kategori = np.array([str(c) for c in e["category"]])
    de["target"] = np.isin(kategori, list(POSITIF)).astype(int)
    de["sumber"] = kategori
    de["wellbore"] = [str(x) for x in e["fold"]]

    df = pd.concat([dk, de], ignore_index=True)
    return df, fitur, kategori


def baseline_sklearn(df, fitur, sumur_uji):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    latih = df[df.wellbore != sumur_uji]
    uji = df[df.wellbore == sumur_uji]
    Xl, yl = latih[fitur].to_numpy(np.float32), latih["target"].to_numpy(int)
    Xu, yu = uji[fitur].to_numpy(np.float32), uji["target"].to_numpy(int)
    hasil = {"mayoritas": {"auc": 0.5, "auprc": round(float(yu.mean()), 4),
                           **metrik(yu, np.zeros(len(yu)))}}
    for nama, model in [
        ("reglog", make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                                 LogisticRegression(max_iter=3000, class_weight="balanced"))),
        ("rf", make_pipeline(SimpleImputer(strategy="median"),
                             RandomForestClassifier(n_estimators=400, min_samples_leaf=3,
                                                    n_jobs=-1, random_state=SEED,
                                                    class_weight="balanced_subsample"))),
    ]:
        model.fit(Xl, yl)
        s = model.predict_proba(Xu)[:, 1]
        hasil[nama] = {"auc": round(float(roc_auc_score(yu, s)), 4),
                       "auprc": round(float(average_precision_score(yu, s)), 4),
                       **metrik(yu, s)}
    return hasil, len(yu), int(yu.sum())



def _aucpr_h2o(perf):
    """Metrik internal H2O ada di nama berbeda antar versi; kalau tidak ada, catat null."""
    for nama in ("aucpr", "average_precision", "pr_auc"):
        try:
            return round(float(getattr(perf, nama)()), 4)
        except Exception:
            continue
    return None


def jalankan(daftar_sumur, batas_detik=600, max_models=100):
    import h2o
    from h2o.automl import H2OAutoML
    from sklearn.metrics import average_precision_score, roc_auc_score

    df, fitur, kategori = muat()
    ringkas = {
        "setelan": {"nthreads": 18, "max_models": max_models,
                    "max_runtime_secs_per_sumur": batas_detik,
                    "metrik_utama": "AUPRC via sklearn average_precision_score",
                    "cv": "fold_column wellbore (6 fold internal)"},
        "data": {"baris": int(len(df)), "fitur": len(fitur),
                 "positif": int(df.target.sum()), "negatif": int((df.target == 0).sum()),
                 "sumur": sorted(df.wellbore.unique().tolist()),
                 "positif_per_kategori": {c: int((kategori == c).sum()) for c in sorted(set(kategori))},
                 "definisi_positif": sorted(POSITIF)},
        "hasil": {},
    }
    print(f"[data] {len(df)} baris | positif {ringkas['data']['positif']} | "
          f"sumur {ringkas['data']['sumur']}", flush=True)

    ip_eth0 = subprocess.run(["ip", "-4", "-o", "addr", "show", "eth0"],
                             capture_output=True, text=True).stdout.split()[3].split("/")[0]
    print(f"[h2o] ikat ke eth0 {ip_eth0}", flush=True)
    h2o.connect(url=f"http://{ip_eth0}:54322")

    berkas_baseline = OUT / "baseline_only.json"
    baseline_tersimpan = {}
    if berkas_baseline.exists():
        isi = json.loads(berkas_baseline.read_text())
        baseline_tersimpan = isi.get("per_sumur", isi)
        print(f"[baseline] dipakai hasil tersimpan untuk {len(baseline_tersimpan)} sumur", flush=True)
    hf = h2o.H2OFrame(df)
    print(f"[frame] upload selesai: {hf.nrows} baris x {hf.ncols} kolom", flush=True)
    hf["target"] = hf["target"].asfactor()
    hf["wellbore"] = hf["wellbore"].asfactor()
    if "sumber" in df.columns:
        hf = hf.drop("sumber")

    for sumur in daftar_sumur:
        latih = hf[hf["wellbore"] != sumur]
        uji = hf[hf["wellbore"] == sumur]
        aml = H2OAutoML(max_models=max_models, max_runtime_secs=batas_detik, seed=SEED,
                        balance_classes=True, sort_metric="AUCPR", verbosity="warn")
        print(f"[{sumur}] mulai train", flush=True)
        aml.train(x=fitur, y="target", training_frame=latih, fold_column="wellbore")
        print(f"[{sumur}] train selesai, evaluasi uji", flush=True)
        perf = aml.leader.model_performance(test_data=uji)
        pr = aml.leader.predict(uji).as_data_frame()
        kolom_p1 = [c for c in pr.columns if c == "p1" or c.endswith("p1")][0]
        skor = pr[kolom_p1].to_numpy(float)
        yu = uji["target"].as_data_frame()["target"].to_numpy(int)
        w = baseline_tersimpan.get(sumur)
        sk = w.get("per_sumur", w) if w and "per_sumur" not in w else w
        if w is None:
            sk, n_uji, n_pos = baseline_sklearn(df, fitur, sumur)
        else:
            n_uji = int(w["n_uji"])
            n_pos = int(w["n_positif_uji"])
        lb = aml.leaderboard.as_data_frame()[["model_id", "auc", "aucpr"]].head(5)
        ringkas["hasil"][sumur] = {
            "n_uji": n_uji, "n_positif": n_pos,
            "h2o": {"model": aml.leader.model_id,
                    "auc": round(float(roc_auc_score(yu, skor)), 4),
                    "auprc": round(float(average_precision_score(yu, skor)), 4),
                    "aucpr_h2o_internal": _aucpr_h2o(perf),
                    **metrik(yu, skor),
                    "leaderboard": lb.to_dict("records")},
            "baseline": sk,
        }
        h = ringkas["hasil"][sumur]["h2o"]
        print(f"[{sumur}] H2O {h['model']}: AUC {h['auc']} AUPRC {h['auprc']} | "
              f"RF AUPRC {sk['rf']['auprc']} | reglog AUPRC {sk['reglog']['auprc']}", flush=True)
        h2o.remove(uji)
        h2o.remove(latih)
        (OUT / "h2o_kontrol.json").write_text(json.dumps(ringkas, indent=2, default=str))

    print("[tulis]", OUT / "h2o_kontrol.json", flush=True)
    return ringkas


if __name__ == "__main__":
    sumur = sys.argv[1:] or ["F-7", "F-9_A", "F-14"]
    r = jalankan(sumur)
    print(json.dumps({s: {"h2o": d["h2o"]["auprc"], "rf": d["baseline"]["rf"]["auprc"],
                          "reglog": d["baseline"]["reglog"]["auprc"],
                          "mayoritas": d["baseline"]["mayoritas"]["auprc"]}
                      for s, d in r["hasil"].items()}, indent=2))
