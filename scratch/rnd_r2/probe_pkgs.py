import importlib
for m in ["numpy", "pandas", "scipy", "sklearn", "statsmodels", "sksurv", "lifelines", "matplotlib"]:
    try:
        mod = importlib.import_module(m)
        print(m, "OK", getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "MISSING", type(e).__name__, e)
