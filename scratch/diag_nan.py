"""Diagnostik lanjutan: pola NaN pada 480 fitur, penyebab DL divergen."""
import numpy as np
import pathlib

DATA = pathlib.Path("/mnt/d/ARCT-9F2/data/predictive")
k = np.load(DATA / "features_timeseries_controls_berdata.npz", allow_pickle=True)
X = np.asarray(k["X"], dtype=np.float64)
nama = [str(n) for n in k["feature_names"]]
nan_kolom = np.isnan(X).sum(axis=0)
tot = X.size
print("NaN total %d / %d (%.1f%%)" % (int(np.isnan(X).sum()), tot, 100 * np.isnan(X).sum() / tot))
print("kolom punya NaN:", int((nan_kolom > 0).sum()), "dari", X.shape[1])
print("\n12 kolom paling banyak NaN:")
for i in np.argsort(nan_kolom)[-12:][::-1]:
    if nan_kolom[i] == 0:
        break
    print("   %-46s NaN %6d (%.0f%%)" % (nama[i][:46], nan_kolom[i], 100 * nan_kolom[i] / X.shape[0]))
nan_baris = np.isnan(X).sum(axis=1)
print("\nbaris NaN per baris: p50 %d, maks %d | baris >50%% NaN: %d | baris seluruhnya NaN: %d" % (
    np.median(nan_baris), nan_baris.max(), int((nan_baris > 0.5 * X.shape[1]).sum()),
    int((nan_baris == X.shape[1]).sum())))
print("\nsebaran banyaknya kolom ber-NaN pada satu baris:")
for q in (50, 75, 90, 99, 100):
    print("   p%-3d: %d kolom" % (q, int(np.percentile(nan_baris, q))))

# Setelah imputasi median: apakah ada kolom jadi konstan (varian 0)?
med = np.nanmedian(X, axis=0)
Xi = np.where(np.isnan(X), med, X)
print("\nsetelah imputasi median: kolom konstan:", int((Xi.var(axis=0) == 0).sum()),
      "| nilai abs maks %.4g" % np.abs(Xi).max())
# Berapa banyak kolom yang setelah imputasi hampir seluruhnya satu nilai
uniq = [len(np.unique(Xi[:, j])) for j in range(X.shape[1])]
print("kolom dengan <5 nilai unik setelah imputasi:", int(sum(1 for u in uniq if u < 5)))
