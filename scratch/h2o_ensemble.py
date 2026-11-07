"""Apakah menggabungkan kandidat AutoML mengalahkan leader dan RF?

Per sumur (LOO): latih AutoML dengan setelan identik h2o_eksperimen.py, lalu ambil
prediksi setiap kandidat pada sumur uji dan bandingkan cara kombinasi:
- leader (baseline AutoML)
- rata-rata probabilitas top-3 / top-5 / top-10 (urut AUCPR internal)
- rata-rata peringkat top-5 (rank-average, tahan beda kalibrasi antar model)
- StackedEnsemble_* bila H2O membentuknya
Metrik dihitung dengan average_precision_score sklearn, sama seperti baseline RF.
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
BATAS = 600
MAKS_MODEL = 100
SEED = 42
TOPN_PREDIKSI = 15


def main(daftar_sumur):
    import h2o
    from h2o.automl import H2OAutoML
    from sklearn.metrics import average_precision_score
    import h2o_eksperimen as he

    df, fitur, _ = he.muat()
    baseline = json.loads((OUT / "baseline_only.json").read_text())
    baseline = baseline.get("per_sumur", baseline)

    ip = __import__("subprocess").run(["ip", "-4", "-o", "addr", "show", "eth0"],
                                      capture_output=True, text=True).stdout.split()[3].split("/")[0]
    h2o.connect(url=f"http://{ip}:54322")
    hf = h2o.H2OFrame(df)
    hf["target"] = hf["target"].asfactor()
    hf["wellbore"] = hf["wellbore"].asfactor()
    hf = hf.drop("sumber")

    hasil = {"setelan": {"batas_detik": BATAS, "max_models": MAKS_MODEL,
                         "sort_metric": "AUCPR", "balance_classes": True,
                         "fold_column": "wellbore", "seed": SEED,
                         "kombinasi": ["leader", "mean_top3", "mean_top5", "mean_top10",
                                       "rankmean_top5", "stacked_ensemble"]},
             "hasil": {}}

    for sumur in daftar_sumur:
        latih = hf[hf["wellbore"] != sumur]
        uji = hf[hf["wellbore"] == sumur]
        aml = H2OAutoML(max_models=MAKS_MODEL, max_runtime_secs=BATAS, seed=SEED,
                        balance_classes=True, sort_metric="AUCPR", verbosity="warn")
        print(f"[{sumur}] mulai AutoML", flush=True)
        aml.train(x=fitur, y="target", training_frame=latih, fold_column="wellbore")
        lb = aml.leaderboard.as_data_frame()
        ids = [str(m) for m in lb["model_id"].tolist()]
        internal = dict(zip(ids, [None if np.isnan(v) else float(v)
                                  for v in lb.get("aucpr", [np.nan] * len(ids))]))
        print(f"[{sumur}] kandidat: {len(ids)} | ada StackedEnsemble: "
              f"{any(i.startswith('StackedEnsemble') for i in ids)}", flush=True)

        yu = uji["target"].as_data_frame()["target"].to_numpy(int)
        skor = {}
        for mid in ids[:TOPN_PREDIKSI]:
            m = h2o.get_model(mid)
            pr = m.predict(uji).as_data_frame()
            kol = [c for c in pr.columns if c == "p1" or c.endswith("p1")][0]
            skor[mid] = pr[kol].to_numpy(float)
        se_ids = [i for i in ids if i.startswith("StackedEnsemble")]
        for mid in se_ids:
            if mid in skor:
                continue
            m = h2o.get_model(mid)
            pr = m.predict(uji).as_data_frame()
            kol = [c for c in pr.columns if c == "p1" or c.endswith("p1")][0]
            skor[mid] = pr[kol].to_numpy(float)

        def auprc(v):
            return round(float(average_precision_score(yu, v)), 4)

        urut = [i for i in ids[:TOPN_PREDIKSI]]
        leader = ids[0]
        catat = {"n_kandidat": len(ids), "n_uji": int(len(yu)), "n_positif": int(yu.sum()),
                 "leader": leader, "leader_auprc_uji": auprc(skor[leader]),
                 "leader_aucpr_internal": internal.get(leader),
                 "leaderboard_top": [{"model": i, "aucpr_internal": internal.get(i)} for i in urut]}
        for k in (3, 5, 10):
            pakai = [i for i in urut[:k] if i in skor]
            if len(pakai) >= 2:
                catat[f"mean_top{k}"] = auprc(np.mean([skor[i] for i in pakai], axis=0))
        pakai5 = [i for i in urut[:5] if i in skor]
        if len(pakai5) >= 2:
            from scipy.stats import rankdata
            r = np.mean([rankdata(skor[i]) for i in pakai5], axis=0)
            catat["rankmean_top5"] = auprc(r)
        if se_ids:
            catat["stacked_ensemble"] = {"model": se_ids[0], "auprc": auprc(skor[se_ids[0]])}
        sk = baseline.get(sumur)
        sk = sk.get("per_sumur", sk) if isinstance(sk, dict) and "per_sumur" in sk else sk
        catat["rf_auprc"] = sk["rf"]["auprc"]
        catat["reglog_auprc"] = sk["reglog"]["auprc"]
        catat["mayoritas_auprc"] = sk["mayoritas"]["auprc"]
        hasil["hasil"][sumur] = catat
        (OUT / "h2o_ensemble.json").write_text(json.dumps(hasil, indent=2, default=str))
        nilai = {k: v for k, v in catat.items() if k.endswith("auprc") or k.startswith("mean") or k == "rankmean_top5"}
        print(f"[{sumur}] selesai | {nilai}", flush=True)
        for mid in ids:
            try:
                h2o.remove(h2o.get_model(mid))
            except Exception:
                pass
        h2o.remove(uji)
        h2o.remove(latih)
    print("[tulis]", OUT / "h2o_ensemble.json", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or ["F-14", "F-15A", "F-15_S", "F-5", "F-7", "F-9", "F-9_A"])
