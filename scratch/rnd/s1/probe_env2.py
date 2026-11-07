import sys
print("python", sys.executable, sys.version.split()[0])
for m in ("numpy", "pandas", "scipy", "sklearn", "lightgbm"):
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "TIDAK ADA:", type(e).__name__)
