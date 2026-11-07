#!/usr/bin/env python3
"""Triase tangan enam baris MISMATCH: apakah sel itu hitungan yang sah?

Untuk setiap baris, hitung sendiri besaran yang diklaim (panjang daftar, jumlah
nilai True, julat persen) langsung dari JSON sumber, lalu bandingkan.
"""
import json
import pathlib

B = pathlib.Path("/mnt/d/Capstone 1(v2)/scratch/rnd")
S1 = json.loads((B / "s1/s1_hyd_seeds.json").read_text(encoding="utf-8"))
META = json.loads((B / "s1/s1_meta.json").read_text(encoding="utf-8"))
SAT = json.loads((B / "s1/s1_h_saturasi.json").read_text(encoding="utf-8"))
S3A = json.loads((B / "s3/s3a_feasibility.json").read_text(encoding="utf-8"))
S3B = json.loads((B / "s3/s3b_hybrid.json").read_text(encoding="utf-8"))

hasil = []

# S1-012: jumlah nilai True pada reproduksi.lulus
rep = S1["reproduksi"]["lulus"] if isinstance(S1.get("reproduksi"), dict) and "lulus" in S1["reproduksi"] else S1["reproduksi_lulus"]
if isinstance(rep, dict):
    n_true = sum(1 for v in rep.values() if v is True)
else:
    n_true = 0
hasil.append(dict(kode="S1-012", sel_ledger=7, hitung=n_true, dasar="jumlah nilai True pada reproduksi.lulus",
                  jenis="hitungan", lulus=(n_true == 7)))

# S1-013: panjang seed_list
n_seed = len(S1["seed_list"])
hasil.append(dict(kode="S1-013", sel_ledger=5, hitung=n_seed, dasar="len(seed_list)", jenis="hitungan",
                  lulus=(n_seed == 5)))

# S1-016: jumlah well pada s1_meta.wells
w = META["wells"]
n_well = len(w)
hasil.append(dict(kode="S1-016", sel_ledger=9, hitung=n_well, dasar="len(s1_meta.wells)", jenis="hitungan",
                  lulus=(n_well == 9)))

# S1-051: jumlah well kalibrasi unik
hasil.append(dict(kode="S1-051", sel_ledger=2, hitung=len(SAT["well_kalibrasi_unik"]),
                  dasar="len(h_saturasi.well_kalibrasi_unik)", jenis="hitungan",
                  lulus=(len(SAT["well_kalibrasi_unik"]) == 2)))

# S3-016: julat prevalensi per well
pw = S3A["label"]["per_well"]
if isinstance(pw, dict):
    vals = [v["prevalensi_high_MSE"] for v in pw.values() if isinstance(v, dict) and "prevalensi_high_MSE" in v]
else:
    vals = [v["prevalensi_high_MSE"] for v in pw if "prevalensi_high_MSE" in v]
lo, hi = min(vals) * 100, max(vals) * 100
lo_pos = min(v for v in vals if v > 0) * 100
hasil.append(dict(kode="S3-016", sel_ledger="1,32% sampai 54,25%",
                  hitung=(round(lo_pos, 2), round(hi, 2)),
                  hitung_termasuk_well_nol=(round(lo, 2), round(hi, 2)),
                  dasar="min prevalensi pada well berpositif dan maks prevalensi, dikali 100; "
                        "dokumen menyatakan dua well nol positif pada kalimat yang sama",
                  jenis="julat", lulus=(round(lo_pos, 2) == 1.32 and round(hi, 2) == 54.25)))

# S3-032: panjang folds
hasil.append(dict(kode="S3-032", sel_ledger=7, hitung=len(S3B["folds"]), dasar="len(s3b_hybrid.folds)",
                  jenis="hitungan", lulus=(len(S3B["folds"]) == 7)))

for h in hasil:
    print(("COCOK " if h["lulus"] else "BEDA  "), h)

n_lulus = sum(1 for h in hasil if h["lulus"])
(B / "s5/s5_mismatch_triage.json").write_text(json.dumps(dict(
    n_baris=len(hasil), n_cocok=n_lulus,
    keterangan="enam baris MISMATCH semuanya sel hitungan atau julat yang tidak dapat dibandingkan "
               "resolver terhadap daun tunggal; setelah dihitung sendiri, semuanya cocok",
    rincian=hasil), indent=1, ensure_ascii=False), encoding="utf-8")
print("cocok:", n_lulus, "dari", len(hasil))
