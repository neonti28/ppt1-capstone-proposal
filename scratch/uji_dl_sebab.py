"""Uji sebab-akibat: apakah outlier 1e30 SPPA yang membuat DeepLearning divergen?

Perlakuan: frame identik dengan h2o_eksperimen.py, target factor, fold_column wellbore.
A: tanpa perlakuan  -> harap gagal
B: nilai di-clip ke persentil 99.9 per kolom -> harap konvergen
"""
import os
import subprocess
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
os.environ.setdefault("JAVA_HOME", "/home/neonti/.local/jdk17")
DATA = __import__("pathlib").Path("/mnt/d/ARCT-9F2/data/predictive")
POSITIF = {"bha_stuck_fishing", "bha_downhole_equipment", "wellbore_fluid",
           "surface_rig_equipment", "wireline_completion_intervention", "safety_personnel"}


def bersihkan(nama):
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


def muat():
    k = np.load(DATA / "features_timeseries_controls_berdata.npz", allow_pickle=True)
    e = np.load(DATA / "features_timeseries.npz", allow_pickle=True)
    fitur = bersihkan([str(n) for n in k["feature_names"]])
    dk = pd.DataFrame(k["X"], columns=fitur)
    dk["target"], dk["wellbore"] = 0, [str(x) for x in k["fold"]]
    de = pd.DataFrame(e["X"], columns=fitur)
    kat = np.array([str(c) for c in e["category"]])
    de["target"] = np.isin(kat, list(POSITIF)).astype(int)
    de["wellbore"] = [str(x) for x in e["fold"]]
    return pd.concat([dk, de], ignore_index=True), fitur


def uji(nama, df, fitur, h2o, port=54324):
    from h2o.estimators import H2ODeepLearningEstimator
    hf = h2o.H2OFrame(df)
    hf["target"] = hf["target"].asfactor()
    hf["wellbore"] = hf["wellbore"].asfactor()
    try:
        m = H2ODeepLearningEstimator(epochs=10, hidden=[64, 32], seed=42,
                                     fold_column="wellbore", reproducible=True,
                                     standardize=True, stopping_rounds=0)
        m.train(x=fitur, y="target", training_frame=hf)
        print(f"[{nama}] SUKSES: logloss CV {m.cross_validation_metrics().logloss():.4f}, "
              f"auc {m.cross_validation_metrics().auc():.4f}", flush=True)
        return "sukses"
    except Exception as exc:
        pesan = str(exc).replace("\n", " ")[:220]
        print(f"[{nama}] GAGAL: {pesan}", flush=True)
        return "gagal"


def main():
    df, fitur = muat()
    print(f"[data] {len(df)} baris x {len(fitur)} fitur, positif {int(df.target.sum())}", flush=True)
    import h2o
    import subprocess as _sp
    _ip = _sp.run(["ip","-4","-o","addr","show","eth0"],capture_output=True,text=True).stdout.split()[3].split("/")[0]
    print("[h2o] ikat", _ip, flush=True)
    h2o.connect(url=f"http://{_ip}:54324")
    uji("A tanpa perlakuan", df.copy(), fitur, h2o)

    d2 = df.copy()
    batas = np.nanpercentile(np.abs(d2[fitur].to_numpy(np.float64)), 99.9, axis=0)
    batas = np.maximum(batas, 1e-9)
    d2[fitur] = np.clip(d2[fitur].to_numpy(np.float64), -batas, batas)
    print("[clip] nilai abs maks setelah clip: %.4g" % np.nanmax(np.abs(d2[fitur].to_numpy())), flush=True)
    uji("B clip p99.9", d2, fitur, h2o)
    h2o.cluster().shutdown(prompt=False)


if __name__ == "__main__":
    main()
