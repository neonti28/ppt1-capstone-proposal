#!/usr/bin/env python3
"""Daftar artefak gelombang 2 dengan jumlah record yang dapat dihitung ulang.

Untuk setiap berkas: tipe top-level, jumlah kunci top-level, koleksi terpanjang
(path dan panjangnya), kunci hitung eksplisit, byte, dan sha256 dua belas digit.
Metrik diberi label apa adanya supaya tidak dikira sebagai "jumlah record" yang
disepakati: yang diukur adalah kunci top-level dan daftar terpanjang.
"""
import hashlib
import json
import pathlib

B = pathlib.Path("/mnt/d/Capstone 1(v2)")

BERKAS = [
    ("S1", "scratch/rnd/s1/s1_h_saturasi.json"),
    ("S1", "scratch/rnd/s1/s1_hluas.json"),
    ("S1", "scratch/rnd/s1/s1_hyd_seeds.json"),
    ("S1", "scratch/rnd/s1/s1_meta.json"),
    ("S2", "scratch/rnd/s2/p2_probe.json"),
    ("S2", "scratch/rnd/s2/p3_kanal.json"),
    ("S2", "scratch/rnd/s2/s2_meta.json"),
    ("S2", "scratch/rnd/s2/s2_records_ssi.json"),
    ("S2", "scratch/rnd/s2/s2_records_vib.json"),
    ("S2", "scratch/rnd/s2/s2_ringkas.json"),
    ("S3", "scratch/rnd/s3/s3a_feasibility.json"),
    ("S3", "scratch/rnd/s3/s3b_hybrid.json"),
    ("S3", "scratch/rnd/s3/s3c_ringkas.json"),
    ("S4", "scratch/rnd/s4/crosscheck.json"),
    ("S4", "scratch/rnd/s4/ddr_activity_stats.json"),
    ("S4", "scratch/rnd/s4/ddr_downtime_records.jsonl"),
    ("S4", "scratch/rnd/s4/ddr_downtime_table.json"),
    ("S4", "scratch/rnd/s4/inventory.json"),
    ("S4", "scratch/rnd/s4/inventory_raw.json"),
    ("S4", "scratch/rnd/s4/labels_duration.json"),
    ("S4", "scratch/rnd/s4/token_scan.json"),
]

KUNCI_HITUNG = ("n_baris", "n_record", "n_records", "n_kejadian", "n_fold", "n_total",
                "n_rows", "n_pos", "n_neg", "n_well", "n_laporan", "n_seed", "jumlah")


def panen(daun, jalur, daftar, hitung):
    if isinstance(daun, list):
        daftar.append((jalur, len(daun)))
        for v in daun[:50]:
            panen(v, jalur + "[]", daftar, hitung)
    elif isinstance(daun, dict):
        for k, v in daun.items():
            anak = f"{jalur}.{k}" if jalur else k
            if k in KUNCI_HITUNG and isinstance(v, int) and not isinstance(v, bool):
                hitung.append((anak, v))
            panen(v, anak, daftar, hitung)


hasil = []
for kartu, rel in BERKAS:
    p = B / rel
    data = p.read_bytes()
    entri = dict(kartu=kartu, berkas=p.name, jalur=rel, byte=len(data),
                 sha12=hashlib.sha256(data).hexdigest()[:12])
    if rel.endswith(".jsonl"):
        n = len([ln for ln in data.decode("utf-8").splitlines() if ln.strip()])
        entri.update(tipe="JSONL", kunci_top=None, koleksi=["baris JSONL", n], hitung=[])
    else:
        d = json.loads(data.decode("utf-8"))
        if isinstance(d, dict):
            daftar, hitung = [], []
            panen(d, "", daftar, hitung)
            terpanjang = max(daftar, key=lambda x: x[1]) if daftar else ["-", 0]
            entri.update(tipe="objek", kunci_top=len(d),
                         koleksi=[terpanjang[0] or "top-level", terpanjang[1]],
                         hitung=hitung[:6])
        else:
            entri.update(tipe="daftar", kunci_top=None,
                         koleksi=["daftar top-level", len(d)], hitung=[])
    hasil.append(entri)

assert len(hasil) == len(BERKAS), len(hasil)
assert all(h["byte"] > 0 and h["sha12"] for h in hasil)
assert all(h["koleksi"][1] > 0 for h in hasil), [h["berkas"] for h in hasil if h["koleksi"][1] <= 0]

for h in hasil:
    print(h["kartu"], h["berkas"], h["tipe"], "kunci", h["kunci_top"], "byte", h["byte"],
          "| koleksi", h["koleksi"], "| hitung", h["hitung"][:3])

(B / "scratch/rnd/s5/s5_artefak.json").write_text(
    json.dumps(dict(n_berkas=len(hasil), daftar=hasil), indent=1, ensure_ascii=False),
    encoding="utf-8")
print("berkas:", len(hasil))
