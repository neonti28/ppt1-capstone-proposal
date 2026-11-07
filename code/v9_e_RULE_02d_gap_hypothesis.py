"""Hipotesis-gap: 13 scorable onset tak punya anchor unik di dataset.

H_overwrite: onset berdekatan (Δt < H=10 mnt) -> horizon tumpang-tindih ->
lab_ts ditulis ulang oleh onset lewat (loop urut waktu) -> onset awal kehilangan
SEMUA anchor unik (baris tetap ada, berlabel onset lewat).
H_mask: seluruh baris horizon onset gagal mask (ops/win_present) -> onset tak
terekspor sama sekali.

Pembeda: hitung onset ffill dari raw + Δt antar-onset berurutan.
Prediksi H_overwrite: jumlah pasangan Δt<10 mnt ≈ gap (13).
Prediksi H_mask: jumlah pasangan Δt<10 mnt ≈ 0 (gap tetap tak terjelaskan).
"""
import json
import numpy as np
import pandas as pd

BASE = "/mnt/d/Capstone 1(v2)"
WELLS = ["F-9", "F-9_A", "F-10", "F-14"]
GAP_SEG = 30
H = 10


def onsets_ffill(vals):
    out, prev = [], None
    for t, v in vals:
        if np.isnan(v):
            continue
        if prev is not None and prev < 1 and v >= 1:
            out.append(t)
        prev = v
    return out


res = {}
for w in WELLS:
    p = f"{BASE}/data/volve/witsml_parsed/{w}.csv"
    hdr = pd.read_csv(p, nrows=0).columns.tolist()
    if "STUCK_RT" not in hdr:
        res[w] = {"error": "no STUCK_RT"}
        print(w, res[w])
        continue
    parts = []
    for ch in pd.read_csv(p, usecols=["timestamp", "STUCK_RT"], chunksize=250_000,
                          low_memory=False):
        parts.append(ch)
    df = pd.concat(parts, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601",
                                     utc=True, errors="coerce")
    df = df[df["timestamp"].notna()].sort_values("timestamp")
    df = df.drop_duplicates("timestamp", keep="last").set_index("timestamp")
    s = pd.to_numeric(df["STUCK_RT"], errors="coerce")
    # resep D1 VERBATIM: ffill di RAW dulu, baru resample max per menit
    ff = s.ffill(limit=None)
    g = ff.resample("60s").max()
    # segment utk jeda besar (resep D1) — onset hanya dalam segmen sama
    dt = g.index.to_series().diff()
    seg = (dt.isna() | (dt > pd.Timedelta(minutes=GAP_SEG))).cumsum()
    ons = onsets_ffill(list(g.items()))  # g sudah ffill-raw-then-resample (resep D1)
    # Δt antar onset berurutan (menit), pisah-segmen
    deltas = []
    for a, b in zip(ons, ons[1:]):
        if seg.loc[a] == seg.loc[b]:
            deltas.append((b - a).total_seconds() / 60.0)
    n_close = sum(1 for d in deltas if d < H)
    res[w] = dict(n_onsets=len(ons), n_gaps=len(deltas), n_delta_lt_10min=n_close,
                  deltas_lt10=[round(d, 1) for d in deltas if d < H][:20])
    print(w, res[w])

json.dump(res, open(f"{BASE}/scratch/v9_e_rule/v9_e_RULE_02d_gap_hypothesis.json",
                    "w"), indent=1, default=str)
print("total Δt<10:", sum(v.get("n_delta_lt_10min", 0) or 0 for v in res.values()),
      "| dataset gap = 13")
