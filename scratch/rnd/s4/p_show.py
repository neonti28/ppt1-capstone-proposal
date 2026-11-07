"""Printer ringkas untuk JSON hasil S4."""
import json, sys, os
ROOT = "/mnt/d/Capstone 1(v2)"
which = sys.argv[1] if len(sys.argv) > 1 else "labels"
if which == "labels":
    d = json.load(open(os.path.join(ROOT, "scratch/rnd/s4/labels_duration.json"), encoding="utf-8"))
    print("per_source_code:")
    for k, v in d["per_source_code"].items():
        print("  ", k, "|", v)
    print("per_outcome (5):")
    for k, v in list(d["per_outcome"].items())[:5]:
        print("  ", k, "|", v)
    print("per_wellbore:")
    for k, v in d["per_wellbore"].items():
        print("  ", k, "|", v)
elif which == "ddr":
    d = json.load(open(os.path.join(ROOT, "scratch/rnd/s4/ddr_activity_stats.json"), encoding="utf-8"))
    print("interruption per_kode:")
    for k, v in d["activity"]["interruption"]["per_kode"].items():
        print("  ", k, "|", v)
    print("maintenance terkait:")
    for k, v in d["activity"]["maintenance_terkait"]["per_kode"].items():
        print("  ", k, "|", v)
