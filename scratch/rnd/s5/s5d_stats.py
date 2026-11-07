import json, pathlib, re
B = pathlib.Path("/mnt/d/Capstone 1(v2)")
F = {"S1": "docs/RND_S1_SEED_ROBUSTNESS.md", "S2": "docs/RND_S2_HYBRID_VIB_SSI.md",
     "S3": "docs/RND_S3_HYBRID_BITWEAR.md", "S4": "docs/RND_S4_LAYER_B_DATA.md"}
out = {}
for k, rel in F.items():
    t = (B / rel).read_text(encoding="utf-8")
    lines = t.splitlines()
    # bagian belum terverifikasi: header terakhir yang memuat 'BELUM TERVERIFIKASI' (case-insensitive)
    idx = [i for i, l in enumerate(lines) if l.startswith("#") and "BELUM TERVERIFIKASI" in l.upper()]
    n_butir = 0
    if idx:
        i0 = idx[-1]
        for l in lines[i0 + 1:]:
            if l.startswith("#"):
                break
            if re.match(r"^\s*(?:-|\d+\.)\s+\S", l):
                n_butir += 1
    m = re.search(r"sequ-mcp[^.]*?([0-9]+)\s*pikiran", t)
    n_sequ = int(m.group(1)) if m else None
    out[k] = dict(header=lines[idx[-1]] if idx else None, n_butir=n_butir,
                  sequ_declared=n_sequ,
                  em=t.count("\u2014"), en=t.count("\u2013"),
                  baris=len(lines), byte=len(t.encode()),
                  riset=[l.strip()[:60] for l in lines if l.startswith("Riset pendahuluan")])
    print(k, out[k])
(B / "scratch/rnd/s5/s5_stats.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
