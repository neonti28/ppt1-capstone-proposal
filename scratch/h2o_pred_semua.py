"""Simpan prediksi SEMUA kandidat AutoML per sumur supaya strategi kombinasi bisa diuji offline.

Untuk tiap sumur (leave-one-well-out): latih AutoML setelan identik h2o_eksperimen.py,
lalu simpan skor p1 setiap kandidat di sumur uji beserta AUCPR CV internal dan label uji.
Keluaran: scratch/h2o/pred/<sumur>.npz
"""
import json
import os
import sys
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
os.environ.setdefault("JAVA_HOME", "/home/neonti/.local/jdk17")
sys.path.insert(0, "/home/neonti/.hermes/cache/scratch")
OUT = Path("/mnt/d/ARCT-9F2/scratch/h2o")
PRED = OUT / "pred"
PRED.mkdir(parents=True, exist_ok=True)
BATAS = int(os.environ.get("H2O_BATAS", "600"))
MAKS_MODEL = 100
SEED = 42


def main(daftar_sumur):
    import h2o
    from h2o.automl import H2OAutoML
    import h2o_eksperimen as he

    df, fitur, _ = he.muat()
    ip = __import__("subprocess").run(["ip", "-4", "-o", "addr", "show", "eth0"],
                                      capture_output=True, text=True).stdout.split()[3].split("/")[0]
    h2o.connect(url=f"http://{ip}:54322")
    hf = h2o.H2OFrame(df)
    hf["target"] = hf["target"].asfactor()
    hf["wellbore"] = hf["wellbore"].asfactor()
    hf = hf.drop("sumber")

    for sumur in daftar_sumur:
        latih = hf[hf["wellbore"] != sumur]
        uji = hf[hf["wellbore"] == sumur]
        aml = H2OAutoML(max_models=MAKS_MODEL, max_runtime_secs=BATAS, seed=SEED,
                        balance_classes=True, sort_metric="AUCPR", verbosity="warn")
        print(f"[{sumur}] mulai AutoML", flush=True)
        aml.train(x=fitur, y="target", training_frame=latih, fold_column="wellbore")
        lb = aml.leaderboard.as_data_frame()
        ids = [str(m) for m in lb["model_id"].tolist()]
        internal = [float(v) if not np.isnan(v) else 0.0 for v in lb.get("aucpr", [np.nan] * len(ids))]
        yu = uji["target"].as_data_frame()["target"].to_numpy(int)
        skor, dipakai, intern = [], [], []
        for mid, aucpr_cv in zip(ids, internal):
            try:
                m = h2o.get_model(mid)
                pr = m.predict(uji).as_data_frame()
                kol = [c for c in pr.columns if c == "p1" or c.endswith("p1")][0]
                v = pr[kol].to_numpy(float)
            except Exception as exc:
                print(f"   lewati {mid}: {type(exc).__name__}", flush=True)
                continue
            skor.append(v)
            dipakai.append(mid)
            intern.append(aucpr_cv)
        np.savez_compressed(PRED / f"{sumur}.npz", y=yu,
                            skor=np.vstack(skor), model=np.array(dipakai),
                            aucpr_cv=np.array(intern))
        print(f"[{sumur}] tersimpan {len(dipakai)} kandidat | n_uji {len(yu)} | positif {int(yu.sum())}", flush=True)
        for mid in ids:
            try:
                h2o.remove(h2o.get_model(mid))
            except Exception:
                pass
        h2o.remove(uji)
        h2o.remove(latih)
    print("[selesai] seluruh prediksi kandidat tersimpan di", PRED, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["F-14", "F-15A", "F-15_S", "F-5", "F-7", "F-9", "F-9_A"])
