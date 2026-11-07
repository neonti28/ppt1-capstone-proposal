"""E0 verifikasi ulang (run 34). Mengukur ulang tiga hal yang bergantung konstruksi:
1. presisi persistence bit_wear pada tiga urutan (berkas mentah, depth-sort global, well+depth)
2. jumlah pasangan baris berurutan yang menyeberang well pada depth-sort global
3. proporsi onset baru (y_prev=0) di antara baris positif vib
Semua angka ditulis ke JSON supaya bisa dirujuk ledger.
"""
import json
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
OUT = "/home/neonti/.hermes/kanban/boards/rnd-algo-2026/workspaces/t_57e7d52b/e0v_recheck.json"
DS = f"{BASE}/scratch/v9_d1/datasets"

res = {}

u = pd.read_csv(f"{BASE}/data/USROP_labeled.csv",
                usecols=["well", "Measured Depth m", "label"])
is_mse_raw = (u["label"] == "high_MSE_bit_wear").to_numpy().astype(int)


def pers_precision(y):
    pers = np.concatenate([[0], y[:-1]])
    m = pers == 1
    return {
        "n_rows": int(len(y)),
        "n_pos": int(y.sum()),
        "n_prev_pos": int(m.sum()),
        "P_y1_given_prev_pos": round(float(y[m].mean()), 4),
    }


res["bit_wear_urutan_berkas"] = pers_precision(is_mse_raw)

d_sort = u.sort_values("Measured Depth m").reset_index(drop=True)
y_depth = (d_sort["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
cross = int((d_sort["well"].to_numpy()[1:] != d_sort["well"].to_numpy()[:-1]).sum())
res["bit_wear_depth_sort_global"] = pers_precision(y_depth)
res["bit_wear_depth_sort_global"]["n_pasangan_lintas_well"] = cross
res["bit_wear_depth_sort_global"]["fraksi_pasangan_lintas_well"] = round(cross / (len(d_sort) - 1), 4)

d_wd = u.sort_values(["well", "Measured Depth m"]).reset_index(drop=True)
y_wd = (d_wd["label"] == "high_MSE_bit_wear").to_numpy().astype(int)
res["bit_wear_well_depth_sort"] = pers_precision(y_wd)

# F-14 saja, urutan kedalaman (persis segmen yang dilaporkan kampanye)
f14 = u[u["well"] == "USROP_A 2 N-SH_F-14d.csv"].sort_values("Measured Depth m")
res["bit_wear_F14_saja"] = pers_precision((f14["label"] == "high_MSE_bit_wear").to_numpy().astype(int))

# vib: proporsi onset baru di antara positif
v = pd.read_csv(f"{DS}/vib.csv.gz", usecols=["well", "ts_bin", "y_vib"])
v = v.sort_values(["well", "ts_bin"]).reset_index(drop=True)
yv = v["y_vib"].to_numpy().astype(int)
prev = np.concatenate([[0], yv[:-1]])
same_well = np.concatenate([[False], v["well"].to_numpy()[1:] == v["well"].to_numpy()[:-1]])
prev_ok = prev * same_well  # bin pertama tiap well tidak punya riwayat
pos = yv == 1
res["vib_positif"] = {
    "n_pos": int(pos.sum()),
    "n_pos_dgn_y_prev_1": int(((prev_ok == 1) & pos).sum()),
    "n_pos_onset_baru": int(((prev_ok == 0) & pos).sum()),
    "fraksi_onset_baru": round(float(((prev_ok == 0) & pos).sum() / pos.sum()), 4),
    "konsisten_dgn_persistence_R": round(float(((prev_ok == 1) & pos).sum() / pos.sum()), 4),
}

json.dump(res, open(OUT, "w"), indent=1)
print(json.dumps(res, indent=1))
