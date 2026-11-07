import json, pathlib
S5 = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd/s5")
d = json.loads((S5 / "s5_rerun_audit.json").read_text(encoding="utf-8"))
print("rerun.42 keys:", list(d["rerun"]["42"].keys()))
print("ringkas keys:", list(d["rerun"]["42"]["ringkas"].keys()))
print("ringkas 42:", json.dumps(d["rerun"]["42"]["ringkas"], ensure_ascii=False)[:600])
print()
r = json.loads((S5 / "s5_resolve3.json").read_text(encoding="utf-8"))
for k in ("S1", "S2", "S3", "S4"):
    v = r["ledger"][k]
    print(k, "keys:", list(v.keys()))
    print("   kelas_hasil:", v.get("kelas_hasil"), "| kelas_sumber:", v.get("kelas_sumber"), "| n:", v.get("n"))
print()
print("artefak kartu:", {})
from collections import Counter
print(Counter(a["kartu"] for a in r["artefak"]))
print()
k = json.loads((S5 / "s5_kode_doi_lapisan.json").read_text(encoding="utf-8"))
for c in ("S1", "S2", "S3", "S4"):
    print(c, "kode:", k[c]["n_kode_dikutip"], "| dois:", len(k[c]["dois"]), "| urls:", len(k[c]["urls"]),
          "| lapisan:", json.dumps(k[c]["lapisan"], ensure_ascii=False)[:200],
          "| literatur:", str(k[c]["literatur"])[:120])
print()
s = json.loads((S5 / "a1_struktur.json").read_text(encoding="utf-8"))
for c in ("S1", "S2", "S3", "S4"):
    print(c, "lines", s[c]["lines"], "bytes", s[c]["bytes"], "em", s[c]["em_dash"],
          "sequ", s[c]["sequ_count"], "belum_lines", len(s[c]["belum_lines"]))
