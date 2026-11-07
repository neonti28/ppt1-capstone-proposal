import importlib
for m in ['numpy','scipy','sklearn','pandas','PyEMD','vmdpy','aeon']:
    try:
        mod=importlib.import_module(m); print(m, getattr(mod,'__version__','?'))
    except Exception:
        print(m,'MISSING')
