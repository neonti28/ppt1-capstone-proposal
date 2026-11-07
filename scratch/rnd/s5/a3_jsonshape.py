import json, os, pathlib, sys

BASE = pathlib.Path("/mnt/d/Capstone 1(v2)")


def bentuk(o, depth=0, maxdepth=3):
    if isinstance(o, dict):
        if depth >= maxdepth:
            return "dict(n=%d)" % len(o)
        ks = list(o.keys())[:12]
        return {k: bentuk(o[k], depth + 1, maxdepth) for k in ks}
    if isinstance(o, list):
        if not o:
            return "list(0)"
        return ["list(n=%d)" % len(o), bentuk(o[0], depth + 1, maxdepth)]
    return type(o).__name__


def nrec(o):
    if isinstance(o, list):
        return len(o)
    if isinstance(o, dict):
        tot = 0
        for v in o.values():
            tot += nrec(v)
        return tot
    return 0


for card in ("s1", "s2", "s3", "s4"):
    print("=" * 78)
    print("CARD", card)
    for p in sorted((BASE / "scratch/rnd" / card).glob("*.json*")):
        try:
            if p.suffix == ".jsonl":
                rows = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
                print(f"  {p.name}: JSONL ok, {len(rows)} records, keys={list(rows[0].keys())[:8]}")
                continue
            d = json.loads(p.read_text(encoding="utf-8"))
            print(f"  {p.name}: ok, bytes={p.stat().st_size}, top={type(d).__name__}, "
                  f"len={len(d) if hasattr(d,'__len__') else '-'}, nested_records={nrec(d)}")
            print("     bentuk:", json.dumps(bentuk(d), ensure_ascii=False)[:400])
        except Exception as e:
            print(f"  {p.name}: GAGAL BUKA -> {type(e).__name__}: {e}")
