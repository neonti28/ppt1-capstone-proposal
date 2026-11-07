"""R6: peta struktur v9_i1_RESULTS.json (kunci tingkat atas + contoh)."""
import json
from pathlib import Path

P = Path("/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json")
d = json.loads(P.read_text(encoding="utf-8"))


def walk(o, prefix="", depth=0, maxdepth=3):
    if depth >= maxdepth:
        return
    if isinstance(o, dict):
        for k in list(o.keys())[:14]:
            v = o[k]
            kind = type(v).__name__
            extra = ""
            if isinstance(v, (int, float, str)) and not isinstance(v, bool):
                extra = f" = {v!r}"[:90]
            elif isinstance(v, list):
                extra = f" (len {len(v)})"
            elif isinstance(v, dict):
                extra = f" (keys {len(v)})"
            print(f"{'  ' * depth}{prefix}{k}: {kind}{extra}")
            walk(v, "", depth + 1, maxdepth)


walk(d)
print("\n--- meta ---")
print(json.dumps(d.get("meta", {}), indent=1, ensure_ascii=False)[:1200])
