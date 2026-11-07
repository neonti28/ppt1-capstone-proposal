"""Kenapa clip p99.9 masih menyisakan 2,2e27? Periksa batas per kolom."""
import numpy as np
import pandas as pd
import pathlib

DATA = pathlib.Path("/mnt/d/ARCT-9F2/data/predictive")
k = np.load(DATA / "features_timeseries_controls_berdata.npz", allow_pickle=True)
e = np.load(DATA / "features_timeseries.npz", allow_pickle=True)
nama = [str(n) for n in k["feature_names"]]
X = np.vstack([np.asarray(k["X"], np.float64), np.asarray(e["X"], np.float64)])
print("gabungan:", X.shape)
for p in (99.0, 99.9, 99.99):
    b = np.nanpercentile(np.abs(X), p, axis=0)
    print("batas p%-6s maks %.4g | kolom batas >1e3: %d" % (p, b.max(), int((b > 1e3).sum())))
b999 = np.nanpercentile(np.abs(X), 99.9, axis=0)
urut = np.argsort(b999)[::-1][:8]
print("\nkolom dengan batas p99.9 terbesar:")
for i in urut:
    kol = X[:, i]
    fin = kol[np.isfinite(kol)]
    print("  %-42s p99.9 %-11.4g | maks %-11.4g | jml >1e6: %d / %d" % (
        nama[i][:42], b999[i], np.abs(fin).max(), int((np.abs(fin) > 1e6).sum()), len(fin)))
