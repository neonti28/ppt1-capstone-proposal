"""Cari sumber nilai ekstrem (~1e30) yang membuat bobot DeepLearning meledak."""
import numpy as np
import pathlib

DATA = pathlib.Path("/mnt/d/ARCT-9F2/data/predictive")
for berkas in ("features_timeseries_controls_berdata.npz", "features_timeseries.npz"):
    z = np.load(DATA / berkas, allow_pickle=True)
    X = np.asarray(z["X"], dtype=np.float64)
    nama = [str(n) for n in z["feature_names"]]
    mx = np.nanmax(np.abs(X), axis=0)
    print("==", berkas, X.shape, "| abs maks global %.4g" % mx.max())
    urut = np.argsort(mx)[::-1]
    print("  10 kolom dengan nilai absolut terbesar:")
    for i in urut[:10]:
        j = int(np.nanargmax(np.abs(X[:, i])))
        print("   %-44s maks %-12.4g di baris %d" % (nama[i][:44], mx[i], j))
    for amb in (1e6, 1e12, 1e20):
        print("   kolom dengan |nilai| > %.0e: %d" % (amb, int((mx > amb).sum())))
    print()
