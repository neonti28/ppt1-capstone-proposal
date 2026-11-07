import sys, os, json
print("PY", sys.version.split()[0], sys.executable)
for m in ["pandas", "pyarrow", "numpy", "scipy"]:
    try:
        mod = __import__(m)
        print("LIB", m, getattr(mod, "version", getattr(mod, "__version__", "?")))
    except Exception as e:
        print("LIB", m, "MISSING", type(e).__name__)
