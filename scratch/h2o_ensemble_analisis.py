"""Cari strategi kombinasi kandidat AutoML terbaik, dipisah jalur adil dan jalur oracle.

Jalur ADIL: pemilihan kandidat dan bobot hanya memakai AUCPR CV internal (tersedia sebelum
sumur uji dilihat). Jalur ORACLE: pemilihan memakai AUPRC di sumur uji, hanya sebagai batas
atas, bukan hasil yang boleh diklaim.
"""
import json
import pathlib

import numpy as np
from scipy.stats import rankdata, spearmanr
from sklearn.metrics import average_precision_score

PRED = pathlib.Path("/mnt/d/ARCT-9F2/scratch/h2o/pred")
OUT = pathlib.Path("/mnt/d/ARCT-9F2/scratch/h2o/ensemble_hasil.json")
BASE = json.loads(pathlib.Path("/mnt/d/ARCT-9F2/scratch/h2o/baseline_only.json").read_text())
BASE = BASE.get("per_sumur", BASE)


def auprc(y, s):
    return float(average_precision_score(y, s))


def kombinasi_fair(y, skor, internal):
    """Return dict nama strategi -> skor AUPRC di sumur uji."""
    urut = np.argsort(-internal)
    hasil = {}
    hasil["leader_cv"] = auprc(y, skor[urut[0]])
    for k in (2, 3, 5, 10, 20):
        pilih = urut[:min(k, len(urut))]
        if len(pilih) < 2:
            continue
        hasil[f"mean_top{k}"] = auprc(y, skor[pilih].mean(axis=0))
        hasil[f"median_top{k}"] = auprc(y, np.median(skor[pilih], axis=0))
        hasil[f"rankmean_top{k}"] = auprc(y, np.mean([rankdata(skor[i]) for i in pilih], axis=0))
    # bobot dari AUCPR internal, tanpa melihat sumur uji
    w = np.clip(internal, 1e-9, None)
    hasil["weighted_cv_all"] = auprc(y, (skor * w[:, None]).sum(axis=0) / w.sum())
    w_top5 = np.zeros_like(w)
    w_top5[urut[:5]] = np.clip(internal[urut[:5]], 1e-9, None)
    hasil["weighted_cv_top5"] = auprc(y, (skor * w_top5[:, None]).sum(axis=0) / w_top5.sum())
    # Borda seluruh kandidat
    hasil["borda_all"] = auprc(y, np.mean([rankdata(s) for s in skor], axis=0))
    hasil["mean_all"] = auprc(y, skor.mean(axis=0))
    return hasil


def kombinasi_oracle(y, skor):
    """Batas atas: pemilihan memakai AUPRC sumur uji (bocor kalau diklaim sebagai hasil)."""
    tunggal = np.array([auprc(y, s) for s in skor])
    hasil = {"best_single_uji": float(tunggal.max()),
             "indeks_best_single": int(tunggal.argmax())}
    urut = np.argsort(-tunggal)
    for k in (2, 3, 5, 10):
        if len(urut) >= k:
            hasil[f"best_mean_top{k}_uji"] = auprc(y, skor[urut[:k]].mean(axis=0))
    # greedy forward: tambah kandidat yang paling menaikkan AUPRC uji
    pilih, sisa, terbaik = [int(urut[0])], list(urut[1:]), tunggal[urut[0]]
    jejak = [terbaik]
    while sisa:
        kandidat = [(auprc(y, skor[pilih + [j]].mean(axis=0)), j) for j in sisa]
        nilai, j = max(kandidat)
        if nilai <= terbaik + 1e-6:
            break
        pilih.append(int(j)); sisa.remove(j); terbaik = nilai; jejak.append(nilai)
    hasil["greedy_uji"] = float(terbaik)
    hasil["greedy_uji_anggota"] = [int(i) for i in pilih]
    return hasil


def main():
    ringkas = {"per_sumur": {}, "catatan": {
        "adil": "pemilihan dan bobot hanya dari AUCPR CV internal AutoML",
        "oracle": "pemilihan memakai AUPRC sumur uji, hanya batas atas, tidak boleh diklaim"}}
    adil_kunci = set()
    oracle_kunci = set()
    for f in sorted(PRED.glob("*.npz")):
        z = np.load(f, allow_pickle=True)
        y, skor = z["y"], z["skor"]
        internal = z["aucpr_cv"]
        model = [str(m) for m in z["model"]]
        fair = kombinasi_fair(y, skor, internal)
        orc = kombinasi_oracle(y, skor)
        sumur = f.stem
        sk = BASE.get(sumur)
        sk = sk.get("per_sumur", sk) if isinstance(sk, dict) and "per_sumur" in sk else sk
        fair["rf_baseline"] = sk["rf"]["auprc"]
        fair["reglog_baseline"] = sk["reglog"]["auprc"]
        fair["lantai_mayoritas"] = sk["mayoritas"]["auprc"]
        ringkas["per_sumur"][sumur] = {
            "n_kandidat": int(len(model)), "n_uji": int(len(y)), "n_positif": int(y.sum()),
            "adil": {k: round(v, 4) for k, v in fair.items()},
            "oracle": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in orc.items()},
            "kandidat_teratas": [{"model": model[i], "aucpr_cv": round(float(internal[i]), 4)}
                                 for i in np.argsort(-internal)[:5]],
        }
        adil_kunci |= {k for k in fair if k not in ("rf_baseline", "reglog_baseline", "lantai_mayoritas")}
        oracle_kunci |= {k for k in orc if not k.startswith("greedy_uji_anggota") and not k.startswith("indeks")}
        print(f"[{sumur}] adil terbaik: "
              f"{max((v, k) for k, v in fair.items() if k not in ('rf_baseline','reglog_baseline','lantai_mayoritas'))} "
              f"| RF {fair['rf_baseline']} | leader {fair['leader_cv']}", flush=True)

    # agregat rata-rata antar sumur per strategi
    def rerata(bagian):
        hasil = {}
        kunci = set()
        for s in ringkas["per_sumur"]:
            kunci |= {k for k, v in ringkas["per_sumur"][s][bagian].items()
                      if isinstance(v, (int, float)) and not k.startswith("indeks")}
        for k in sorted(kunci):
            nilai = [ringkas["per_sumur"][s][bagian][k] for s in ringkas["per_sumur"]
                     if isinstance(ringkas["per_sumur"][s][bagian].get(k), (int, float))]
            if nilai:
                hasil[k] = round(float(np.mean(nilai)), 4)
        return hasil

    ringkas["rerata_adil"] = rerata("adil")
    ringkas["rerata_oracle"] = rerata("oracle")
    OUT.write_text(json.dumps(ringkas, indent=2, default=str))
    print("\nrata-rata antar sumur (jalur adil):")
    for k, v in sorted(ringkas["rerata_adil"].items(), key=lambda kv: -kv[1]):
        print(f"   {k:22s} {v}")
    print("\nrata-rata antar sumur (batas atas oracle):")
    for k, v in sorted(ringkas["rerata_oracle"].items(), key=lambda kv: -kv[1]):
        print(f"   {k:22s} {v}")
    print("\ntersimpan:", OUT)


if __name__ == "__main__":
    main()
