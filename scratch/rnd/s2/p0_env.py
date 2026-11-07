#!/usr/bin/env python3
"""Probe lingkungan: python mana yang punya pandas, numpy, sklearn, lightgbm, scipy."""
import sys
import json

out = {"exe": sys.executable, "version": sys.version.split()[0], "mods": {}}
for m in ("numpy", "pandas", "scipy", "sklearn", "lightgbm"):
    try:
        mod = __import__(m)
        out["mods"][m] = getattr(mod, "__version__", "?")
    except Exception as e:
        out["mods"][m] = f"MISSING: {type(e).__name__}: {e}"
print(json.dumps(out, indent=1))
