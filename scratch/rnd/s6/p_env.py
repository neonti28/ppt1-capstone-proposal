import sys
pandas = __import__("pandas")
numpy = __import__("numpy")
sklearn = __import__("sklearn")
lightgbm = __import__("lightgbm")
print("PY", sys.version.split()[0], "pandas", pandas.__version__, "numpy", numpy.__version__,
      "sklearn", sklearn.__version__, "lightgbm", lightgbm.__version__)
print("EXE", sys.executable)
