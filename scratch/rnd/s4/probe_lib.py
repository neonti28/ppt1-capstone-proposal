import sys
print("VER", sys.version.split()[0])
ok = []
for m in ["pandas", "pyarrow", "numpy", "scipy"]:
    try:
        mod = __import__(m)
        ok.append(f"{m}={getattr(mod,'__version__','?')}")
    except Exception:
        ok.append(f"{m}=MISSING")
print("LIBS", " ".join(ok))
