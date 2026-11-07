import sys

print("PY", sys.version.split()[0], sys.executable)
for m in ("numpy", "pandas", "scipy", "sklearn", "lightgbm", "pyarrow"):
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "MISSING", type(e).__name__)
