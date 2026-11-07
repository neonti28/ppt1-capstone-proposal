#!/usr/bin/env python3
"""S5 probe: struktur artefak JSON S2, S3, S4."""
import json
import os

BASE = "/mnt/d/Capstone 1(v2)"


def ringkas(obj, pref="", depth=0, maks=3):
    out = []
    if depth > maks:
        return out
    if isinstance(obj, dict):
        for k, v in list(obj.items())[:14]:
            if isinstance(v, (dict, list)):
                out.append(f"{pref}{k}: {type(v).__name__}[{len(v)}]")
                out += ringkas(v, pref + "  ", depth + 1, maks)
            else:
                out.append(f"{pref}{k} = {v!r}"[:160])
    elif isinstance(obj, list):
        if obj:
            out.append(f"{pref}[0] {type(obj[0]).__name__}")
            out += ringkas(obj[0], pref + "  ", depth + 1, maks)
    return out


for kode in ("s2", "s3", "s4"):
    d = f"{BASE}/scratch/rnd/{kode}"
    print(f"\n########## {kode} ##########")
    for f in sorted(os.listdir(d)):
        p = f"{d}/{f}"
        if not (f.endswith(".json") or f.endswith(".jsonl")):
            continue
        sz = os.path.getsize(p)
        print(f"\n--- {f} ({sz} byte) ---")
        if f.endswith(".jsonl"):
            n = 0
            bad = 0
            contoh = None
            with open(p, encoding="utf-8") as fh:
                for ln in fh:
                    ln = ln.strip()
                    if not ln:
                        continue
                    n += 1
                    try:
                        o = json.loads(ln)
                        if contoh is None:
                            contoh = o
                    except Exception:
                        bad += 1
            print(f"jsonl: {n} baris, {bad} gagal parse")
            if contoh:
                for ln in ringkas(contoh):
                    print(" ", ln)
            continue
        try:
            o = json.load(open(p, encoding="utf-8"))
        except Exception as e:
            print("GAGAL DIBUKA:", type(e).__name__, e)
            continue
        print("tipe:", type(o).__name__, "len:", len(o) if hasattr(o, "__len__") else "-")
        for ln in ringkas(o):
            print(" ", ln)
