"""R6 probe: cek modul yang tersedia untuk perhitungan metrik + power."""
import sys

print("python", sys.version.split()[0])
for m in ("numpy", "scipy", "statsmodels", "sklearn", "pandas"):
    try:
        mod = __import__(m)
        print(m, "OK", getattr(mod, "__version__", "?"))
    except Exception as e:  # noqa: BLE001
        print(m, "GAGAL", type(e).__name__, e)
