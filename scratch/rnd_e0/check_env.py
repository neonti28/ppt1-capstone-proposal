import sys
print("python", sys.version.split()[0])
for m in ["pandas", "numpy", "sklearn"]:
    try:
        mod = __import__(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "MISSING", type(e).__name__)
