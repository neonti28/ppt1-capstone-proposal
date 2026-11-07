"""Uji C: clip p99 per kolom -> apa DeepLearning akhirnya konvergen?"""
import os
import pathlib
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
os.environ.setdefault("JAVA_HOME", "/home/neonti/.local/jdk17")
DATA = pathlib.Path("/mnt/d/ARCT-9F2/data/predictive")
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


def main():
    import h2o
    from h2o.estimators import H2ODeepLearningEstimator
    df, fitur = muat()
    d3 = df.copy()
    X = d3[fitur].to_numpy(np.float64)
    batas = np.nanpercentile(np.abs(X), 99.0, axis=0)
    batas = np.maximum(batas, 1e-9)
    d3[fitur] = np.clip(X, -batas, batas)
    print("[C] nilai abs maks setelah clip p99: %.4g" % np.nanmax(np.abs(d3[fitur].to_numpy())), flush=True)

    ip = __import__("subprocess").run(["ip", "-4", "-o", "addr", "show", "eth0"],
                                      capture_output=True, text=True).stdout.split()[3].split("/")[0]
    h2o.connect(url=f"http://{ip}:54324")
    hf = h2o.H2OFrame(d3)
    hf["target"] = hf["target"].asfactor()
    hf["wellbore"] = hf["wellbore"].asfactor()
    m = H2ODeepLearningEstimator(epochs=10, hidden=[64, 32], seed=42,
                                 fold_column="wellbore", standardize=True)
    m.train(x=fitur, y="target", training_frame=hf)
    met = m.cross_validation_metrics()
    print(f"[C clip p99] SUKSES: logloss CV {met.logloss():.4f} auc CV {met.auc():.4f}", flush=True)
    h2o.cluster().shutdown(prompt=False)


if __name__ == "__main__":
    main()
