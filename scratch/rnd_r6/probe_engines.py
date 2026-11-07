"""R6: dump isi engines[] v9_i1_RESULTS.json supaya metrik nyata bisa diambil."""
import json
from pathlib import Path

P = Path("/mnt/d/Capstone 1(v2)/scratch/v9_i1/v9_i1_RESULTS.json")
d = json.loads(P.read_text(encoding="utf-8"))

for i, e in enumerate(d["engines"]):
    print(f"=== engine[{i}] keys={list(e.keys())}")
    print("   engine =", e.get("engine"), "| tier =", e.get("tier"))
    heads = e.get("heads") or e.get("head") or {}
    if isinstance(heads, dict):
        for hname, h in heads.items():
            if isinstance(h, dict):
                print(f"   head {hname}: keys={list(h.keys())}")
                print("     ", json.dumps(h, ensure_ascii=False)[:700])
            else:
                print(f"   head {hname}: {h!r}"[:300])
    else:
        print("   ", json.dumps(heads, ensure_ascii=False)[:1500])
