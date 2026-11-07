#!/usr/bin/env python3
"""V6-E1 50 — ekstraksi jendela akselerometer dataset tool wear Mendeley th4yv974r2.

Label primer (deskripsi dataset Mendeley — dikutip di prereg E1c):
  Run 1 = alat BARU saat mulai, diinspeksi di akhir Run 1;
  Run 2 = alat sama dilanjutkan sampai TUMPUL di akhir Run 2.
  => y = 1 (R02, blunt) / 0 (R01, new); group = tool T01..T04 (4 grup).

Struktur xlsx (diprobe): baris 0-3 blok metadata (Tool:, Run:), baris 4 header
'Sample No.|X|Y|Z', data mulai baris 5.

Jendela 1000 sampel (1 detik @1000 Hz), sisa dibuang.
Fitur (27, TANPA index baris/nama file — dilarang masuk model):
  per sumbu X/Y/Z: mean, std, rms, kurtosis, skew, peak2peak, crest, zcr (24)
  + freq_dominan per sumbu (3): argmax |FFT| setelah buang DC (Hz, 1000 Hz rate)

Output: scratch/v6_e1/toolwear_windows.csv + ch50_toolwear_summary.json (hitungan, BUKAN hasil model)
"""
import json
import os
import numpy as np
import pandas as pd

SRC = "/mnt/d/Capstone 1/scratch/v6_e1/toolwear"
OUT = "/mnt/d/Capstone 1/scratch/v6_e1/toolwear_windows.csv"
SUM = "/mnt/d/Capstone 1/scratch/v6_e1/ch50_toolwear_summary.json"
FS = 1000.0
WIN = 1000
AX = ["X", "Y", "Z"]


def feats(w):  # w: dict axis -> np.array (1000,)
    f = {}
    for a in AX:
        x = w[a]
        sd = float(np.std(x))
        f[f"{a}_mean"] = float(np.mean(x))
        f[f"{a}_std"] = sd
        f[f"{a}_rms"] = float(np.sqrt(np.mean(x ** 2)))
        f[f"{a}_kurt"] = float(pd.Series(x).kurt())
        f[f"{a}_skew"] = float(pd.Series(x).skew())
        f[f"{a}_p2p"] = float(x.max() - x.min())
        f[f"{a}_crest"] = float(np.max(np.abs(x)) / sd) if sd > 0 else np.nan
        zc = np.mean(np.abs(np.diff(np.sign(x))) > 0) if len(x) > 1 else 0.0
        f[f"{a}_zcr"] = float(zc)
        sp = np.abs(np.fft.rfft(x - x.mean()))[1:]
        f[f"{a}_fdom"] = float((np.argmax(sp) + 1) * FS / (2 * len(sp))) if sp.size else np.nan
    return f


rows = []
per_file = {}
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".xlsx"):
        continue
    raw = pd.read_excel(os.path.join(SRC, fn), header=None, skiprows=5, names=["n", "X", "Y", "Z"])
    parts = fn.replace(".xlsx", "").split("_")
    tool, run = parts[-2], parts[-1]   # e.g. DrillingToolWearDataset_T01_R01
    y = 1 if run == "R02" else 0
    nwin = 0
    for s in range(0, len(raw) // WIN * WIN, WIN):
        seg = raw.iloc[s:s + WIN]
        w = {a: pd.to_numeric(seg[a], errors="coerce").dropna().to_numpy() for a in AX}
        if any(len(w[a]) < WIN for a in AX):
            continue
        fr = feats(w)
        fr.update({"tool": tool, "run": run, "file": fn, "start_sample": int(s), "y": y})
        rows.append(fr)
        nwin += 1
    per_file[fn] = {"rows": int(len(raw)), "windows": nwin, "tool": tool, "run": run, "y": y}
    print(f"== {fn}: rows={len(raw)} windows={nwin} label={y}", flush=True)

df = pd.DataFrame(rows)
df.to_csv(OUT, index=False)
summary = {"per_file": per_file,
           "n_windows": int(len(df)),
           "n_features": int(len([c for c in df.columns if c not in
                                  ("tool", "run", "file", "start_sample", "y")])),
           "per_tool": {}}
for t, g in df.groupby("tool"):
    summary["per_tool"][t] = {"windows": int(len(g)),
                              "pos_R02": int(g["y"].sum()),
                              "neg_R01": int((g["y"] == 0).sum())}
json.dump(summary, open(SUM, "w"), indent=1)
# sanity: parsing label harus menghasilkan 2 kelas dan 4 tool
assert df["y"].sum() > 0 and (df["y"] == 0).sum() > 0, "label parsing gagal (1 kelas saja)"
assert sorted(df["tool"].unique()) == ["T01", "T02", "T03", "T04"], df["tool"].unique()
assert set(df["run"].unique()) == {"R01", "R02"}, df["run"].unique()
print("sanity: 2 kelas + 4 tool + R01/R02 OK")
print("total windows:", len(df), "features:", summary["n_features"])
print(json.dumps(summary["per_tool"], indent=1))
print("saved", OUT)
