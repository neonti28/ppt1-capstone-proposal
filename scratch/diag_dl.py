"""Diagnostik: kenapa DeepLearning H2O gagal konvergen pada 480 fitur Volve ini."""
import numpy as np
import pathlib

DATA = pathlib.Path("/mnt/d/ARCT-9F2/data/predictive")
k = np.load(DATA / "features_timeseries_controls_berdata.npz", allow_pickle=True)
e = np.load(DATA / "features_timeseries.npz", allow_pickle=True)
nama = [str(n) for n in k["feature_names"]]
X = np.asarray(k["X"], dtype=np.float64)
Xe = np.asarray(e["X"], dtype=np.float64)
print("kontrol:", X.shape, "| kejadian:", Xe.shape, "| fitur:", len(nama))

print("\n== nilai tidak finit ==")
print("  NaN:", int(np.isnan(X).sum()), "| Inf:", int(np.isinf(X).sum()))

mx = np.abs(X).max(axis=0)
print("\n== skala absolut per kolom (data kontrol) ==")
print("  p50 %.3g | p95 %.3g | p99 %.3g | maks %.3g" % (
    np.median(mx), np.percentile(mx, 95), np.percentile(mx, 99), mx.max()))
print("  kolom max > 1e6:", int((mx > 1e6).sum()))
print("  kolom max > 1e9:", int((mx > 1e9).sum()))

# kolom varian nol / hampir nol -> standardisasi membagi nol
var = X.var(axis=0)
nun = (X != 0).sum(axis=0)
print("\n== kolom degenerat ==")
print("  varian == 0 (konstan):", int((var == 0).sum()))
print("  nonzero <= 2 baris:", int((nun <= 2).sum()))
print("  nonzero <= 5 baris:", int((nun <= 5).sum()))

# rasio skala antar kolom -> conditioning buruk
pos = mx[mx > 0]
print("\n== rasio skala ==")
print("  kolom max terkecil %.3g | terbesar %.3g | rasio %.3g" % (pos.min(), pos.max(), pos.max() / pos.min()))

# kolom dengan max ekstrem dan nama
big = np.argsort(mx)[-8:][::-1]
print("\n== 8 kolom berskala terbesar (maks, nonzero, nama) ==")
for i in big:
    print("   %-46s maks %-12.4g nonzero %d" % (nama[i][:46], mx[i], nun[i]))

# distribusi positif per fitur di data kejadian, untuk melihat sparsity
print("\n== sparsity kejadian ==")
print("  kolom yang seluruhnya nol di data kejadian:", int(((Xe != 0).sum(axis=0) == 0).sum()))
print("  rata-rata nonzero per baris: %.1f dari %d" % ((Xe != 0).sum(axis=1).mean(), Xe.shape[1]))
