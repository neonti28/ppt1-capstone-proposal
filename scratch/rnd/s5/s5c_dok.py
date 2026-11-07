#!/usr/bin/env python3
"""S5-C: apakah angka yang dikutip dokumen S2/S3/S4 benar-benar ada di artefak kartunya.

Metode (bisa gagal):
 1. String tampilan wajib ADA di dokumen (kalau tidak, daftar klaim saya basi).
 2. Nilai numerik wajib ditemukan di salah satu artefak JSON/JSONL kartu itu
    (toleransi mengikuti jumlah desimal tampilan).
 3. Angka turunan diuji dengan aritmetika eksplisit.

Keluaran: scratch/rnd/s5/s5_dok.json ; mode --negatif merusak satu klaim.
"""
import json
import os
import re
import sys
import time

BASE = "/mnt/d/Capstone 1(v2)"
NEGATIF = "--negatif" in sys.argv
OUT = f"{BASE}/scratch/rnd/s5/s5_dok{'_negatif' if NEGATIF else ''}.json"

ARTEFAK = {
    "S2": ["scratch/rnd/s2/s2_records_vib.json", "scratch/rnd/s2/s2_records_ssi.json",
           "scratch/rnd/s2/s2_ringkas.json", "scratch/rnd/s2/s2_meta.json"],
    "S3": ["scratch/rnd/s3/s3a_feasibility.json", "scratch/rnd/s3/s3b_hybrid.json",
           "scratch/rnd/s3/s3c_ringkas.json"],
    "S4": ["scratch/rnd/s4/inventory.json", "scratch/rnd/s4/inventory_raw.json",
           "scratch/rnd/s4/token_scan.json", "scratch/rnd/s4/ddr_activity_stats.json",
           "scratch/rnd/s4/labels_duration.json", "scratch/rnd/s4/ddr_downtime_table.json",
           "scratch/rnd/s4/crosscheck.json"],
}
DOK = {"S2": "docs/RND_S2_HYBRID_VIB_SSI.md", "S3": "docs/RND_S3_HYBRID_BITWEAR.md",
       "S4": "docs/RND_S4_LAYER_B_DATA.md"}

# (string tampilan di dokumen, nilai numerik)
KLAIM = {
    "S2": [
        ("23.922", 23922), ("35.906", 35906), ("5.429", 5429), ("592", 592),
        ("0,5615", 0.5615), ("0,4385", 0.4385), ("0,2425", 0.2425), ("0,7575", 0.7575),
        ("0,1135", 0.1135), ("0,8865", 0.8865), ("0,1103", 0.1103), ("0,8897", 0.8897),
        ("1.124", 1124), ("3.018", 3018), ("0,6757", 0.6757), ("0,8481", 0.8481),
        ("0,8274", 0.8274), ("0,0306", 0.0306), ("0,5387", 0.5387), ("0,1848", 0.1848),
        ("0,8673", 0.8673), ("0,7405", 0.7405), ("0,7288", 0.7288), ("22,0218", 22.0218),
        ("133,8624", 133.8624), ("0,2094", 0.2094), ("0,8724", 0.8724), ("0,4706", 0.4706),
        ("0,0361", 0.0361), ("0,1111", 0.1111), ("0,3589", 0.3589), ("14,7078", 14.7078),
        ("0,0653", 0.0653), ("0,0449", 0.0449), ("1,3457", 1.3457), ("0,4876", 0.4876),
        ("30,8036", 30.8036),
    ],
    "S3": [
        ("198.928", 198928), ("49.732", 49732), ("0,250", 0.25), ("0,1155", 0.1155),
        ("0,0377", 0.0377), ("65,617", 65.617), ("0,6496", 0.6496), ("0,9968", 0.9968),
        ("110,432", 110.432), ("18,41", 18.41), ("145.887", 145887), ("53.041", 53041),
        ("0,0663", 0.0663), ("0,5303", 0.5303),
    ],
    "S4": [
        ("23.447", 23447), ("1.759", 1759), ("884", 884), ("1.225,0", 1225.0),
        ("1.116", 1116), ("1.777,75", 1777.75), ("325", 325), ("533", 533),
        ("4.035", 4035), ("2.180.278", 2180278), ("56.815.359", 56815359),
        ("0,1468", 0.1468), ("8.343,253", 8343.253), ("1.212", 1212), ("1.072", 1072),
    ],
}

# angka turunan: (label, hasil hitung, hasil bulat tertulis, jumlah desimal)
ARITMATIKA = {
    "S2": [("42,19 alarm = 1/0,0237", 1 / 0.0237, 42.0, 0)],
    "S3": [("18,41 = 110,432/6", 110.432 / 6, 18.41, 2),
           ("0,2500 = 49.732/198.928", 49732 / 198928, 0.25, 4),
           ("0,9998 sampai 1,0001? rasio cocok", 198928 / 198928, 1.0, 4)],
    "S4": [("3.518 = 1.759 XML + 1.759 HTML", 1759 + 1759, 3518, 0),
           ("0,1468 = 1.225,0/8.343,253", 1225.0 / 8343.253, 0.1468, 4),
           ("18,48% = 325/1.759", 325 / 1759, 0.1848, 4)],
}


def indeks(nilai, out, jalur="", kedalaman=0):
    if kedalaman > 60:
        return
    if isinstance(nilai, bool):
        return
    if isinstance(nilai, (int, float)):
        out.append((float(nilai), jalur))
    elif isinstance(nilai, dict):
        for k, v in nilai.items():
            indeks(v, out, f"{jalur}.{k}" if jalur else str(k), kedalaman + 1)
    elif isinstance(nilai, list):
        for i, v in enumerate(nilai):
            indeks(v, out, f"{jalur}[{i}]", kedalaman + 1)


def muat(path):
    p = f"{BASE}/{path}"
    if not os.path.isfile(p):
        return None, "TIDAK_ADA"
    if os.path.getsize(p) == 0:
        return None, "KOSONG"
    try:
        if p.endswith(".jsonl"):
            return [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()], "ok"
        return json.load(open(p, encoding="utf-8")), "ok"
    except Exception as e:
        return None, f"GAGAL:{type(e).__name__}"


def desimal(s):
    s = s.replace(".", "")
    return len(s.split(",")[1]) if "," in s else 0


hasil = dict(kartu="t_b5b16adc", langkah="S5-C angka dokumen vs artefak",
             waktu=time.strftime("%Y-%m-%d %H:%M:%S"), mode="NEGATIF" if NEGATIF else "NORMAL",
             per_kartu={})

for k, klaim in KLAIM.items():
    dok = open(f"{BASE}/{DOK[k]}", encoding="utf-8").read()
    isi = {}
    for a in ARTEFAK[k]:
        obj, st = muat(a)
        isi[a] = dict(status=st, bytes=os.path.getsize(f"{BASE}/{a}") if os.path.isfile(f"{BASE}/{a}") else 0)
        if obj is not None:
            buf = []
            indeks(obj, buf)
            isi[a]["indeks"] = buf
    d = dict(dokumen=DOK[k], baris_dokumen=len(dok.splitlines()),
             artefak={a: dict(status=v["status"], bytes=v["bytes"],
                              n_nilai=len(v.get("indeks", []))) for a, v in isi.items()},
             klaim=[], turunan=[])
    for tampil, nilai in klaim:
        c = dict(tampil=tampil, nilai=nilai)
        c["ada_di_dokumen"] = tampil in dok
        if NEGATIF and k == "S3" and tampil == "0,1155":
            nilai = nilai + 0.5  # rusak satu klaim untuk membuktikan penguji bisa gagal
            c["nilai"] = nilai
            c["catatan"] = "dirusak mode negatif"
        tol = max(0.5 * 10 ** (-desimal(tampil)), 1e-9) if desimal(tampil) else 1e-6
        temuan = []
        for a, v in isi.items():
            for vv, jalur in v.get("indeks", []):
                if abs(vv - nilai) <= tol or (nilai != 0 and abs(abs(vv) * 1000 - abs(nilai)) <= max(tol * 1000, 1e-6)):
                    temuan.append(f"{os.path.basename(a)}:{jalur}")
        c["n_lokasi"] = len(temuan)
        c["lokasi"] = temuan[:4]
        c["status"] = ("TERLETAK" if temuan else "TIDAK_TERLETAK")
        if not c["ada_di_dokumen"]:
            c["status"] = "DOK_TIDAK_MEMUAT"
        d["klaim"].append(c)
    for label, hitung, tertulis, des in ARITMATIKA.get(k, []):
        c = dict(label=label, hitung=hitung, tertulis=tertulis,
                 selisih=abs(hitung - tertulis), desimal=des,
                 status="COCOK" if abs(hitung - tertulis) <= 0.5 * 10 ** (-des) + 1e-12 else "BEDA")
        if NEGATIF and k == "S2" and label.startswith("42,19"):
            c["status"] = "BEDA"; c["catatan"] = "dirusak mode negatif"
        d["turunan"].append(c)
    d["rekap"] = dict(
        n_klaim=len(d["klaim"]),
        terletak=sum(1 for c in d["klaim"] if c["status"] == "TERLETAK"),
        tidak_terletak=[c["tampil"] for c in d["klaim"] if c["status"] == "TIDAK_TERLETAK"],
        dok_tidak_memuat=[c["tampil"] for c in d["klaim"] if c["status"] == "DOK_TIDAK_MEMUAT"],
        turunan_beda=[c["label"] for c in d["turunan"] if c["status"] == "BEDA"],
    )
    hasil["per_kartu"][k] = d

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(hasil, f, indent=1, ensure_ascii=False)

for k, d in hasil["per_kartu"].items():
    r = d["rekap"]
    print(f"[{k}] dok={d['baris_dokumen']} baris | klaim={r['n_klaim']} terletak={r['terletak']}")
    for a, v in d["artefak"].items():
        print(f"   {a} -> {v['status']} {v['bytes']}B n_nilai={v['n_nilai']}")
    if r["tidak_terletak"]:
        print("   TIDAK_TERLETAK:", r["tidak_terletak"])
    if r["dok_tidak_memuat"]:
        print("   DOK_TIDAK_MEMUAT:", r["dok_tidak_memuat"])
    print("   turunan:", [(c["label"], c["status"]) for c in d["turunan"]])
print("\nUJI_NEGATIF_TERDETEKSI" if NEGATIF else "MODE_NORMAL")
