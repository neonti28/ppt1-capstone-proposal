import importlib, sys
for m in ["numpy", "pandas", "scipy", "sklearn", "lightgbm", "xgboost", "catboost", "statsmodels"]:
    try:
        mod = importlib.import_module(m)
        print(m, getattr(mod, "__version__", "?"))
    except Exception as e:
        print(m, "MISSING", type(e).__name__)
print(sys.version)
