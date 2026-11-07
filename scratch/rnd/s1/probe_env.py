import sys
print("python", sys.version)
for m in ("numpy", "pandas", "scipy", "sklearn", "lightgbm"):
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "TIDAK ADA:", e)
